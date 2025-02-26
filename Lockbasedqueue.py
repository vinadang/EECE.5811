import threading
import time
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class ConcurrentQueue:
    def __init__(self):
        """
        Initialize the queue with a dummy node so that head and tail
        always point to a valid node.
        """
        dummy = Node(None)
        self.head = dummy
        self.tail = dummy
        # Two locks: one for head, one for tail
        self.head_lock = threading.Lock()
        self.tail_lock = threading.Lock()

    def enqueue(self, value):
        """
        Insert a new node at the tail of the queue.
        """
        new_node = Node(value)
        # Lock the tail while updating
        self.tail_lock.acquire()
        try:
            self.tail.next = new_node
            self.tail = new_node
        finally:
            self.tail_lock.release()

    def dequeue(self):
        """
        Remove a node from the head of the queue.
        Returns the value or None if the queue is empty.
        """
        # Lock the head while updating
        self.head_lock.acquire()
        try:
            old_head = self.head
            new_head = old_head.next
            if new_head is None:
                # Queue is empty
                return None
            self.head = new_head
            return new_head.value
        finally:
            self.head_lock.release()

# -----------------------------------------------------------------------
# Example usage and a simple benchmark test:

def producer(q, count):
    """Enqueue 'count' random integers into the queue."""
    for _ in range(count):
        q.enqueue(random.randint(1, 1000))

def consumer(q, count, collected):
    """
    Dequeue 'count' items from the queue, storing them in 'collected'.
    Will block-spin if the queue is empty momentarily.
    """
    for _ in range(count):
        val = None
        while val is None:
            val = q.dequeue()
            if val is None:
                time.sleep(0.0001)  # small wait to avoid busy spin
        collected.append(val)

if __name__ == "__main__":
    # Example: 2 producers, 2 consumers, each producing/consuming 5000 items
    NUM_PRODUCERS = 2
    NUM_CONSUMERS = 2
    ITEMS_PER_PRODUCER = 5000

    q = ConcurrentQueue()
    
    # Prepare threads
    producers = []
    for _ in range(NUM_PRODUCERS):
        t = threading.Thread(target=producer, args=(q, ITEMS_PER_PRODUCER))
        producers.append(t)
    
    collected_items = []
    consumers_ = []
    for _ in range(NUM_CONSUMERS):
        t = threading.Thread(target=consumer, args=(q, ITEMS_PER_PRODUCER, collected_items))
        consumers_.append(t)

    # Start timing
    start_time = time.time()

    # Start threads
    for t in producers:
        t.start()
    for t in consumers_:
        t.start()

    # Join threads
    for t in producers:
        t.join()
    for t in consumers_:
        t.join()

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"All producers/consumers have finished.")
    print(f"Total items consumed: {len(collected_items)}")
    print(f"Elapsed time: {elapsed:.4f} seconds")
