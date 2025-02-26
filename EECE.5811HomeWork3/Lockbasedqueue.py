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
        self.head_lock = threading.Lock()
        self.tail_lock = threading.Lock()

    def enqueue(self, value):
        """
        Insert a new node at the tail of the queue.
        """
        new_node = Node(value)
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
        self.head_lock.acquire()
        try:
            old_head = self.head
            new_head = old_head.next
            if new_head is None:
                return None
            self.head = new_head
            return new_head.value
        finally:
            self.head_lock.release()

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

def run_benchmark(num_producers, num_consumers, items_per_producer):
    """
    Creates a queue, spawns num_producers producers and num_consumers consumers,
    each producer enqueuing 'items_per_producer' items, and measures the time.
    Returns (total_items_consumed, elapsed_time).
    """
    q = ConcurrentQueue()

    producers = []
    for _ in range(num_producers):
        t = threading.Thread(target=producer, args=(q, items_per_producer))
        producers.append(t)

    collected_items = []
    consumers_ = []
 
    for _ in range(num_consumers):
        t = threading.Thread(target=consumer, args=(q, items_per_producer, collected_items))
        consumers_.append(t)

    start_time = time.time()

    for t in producers:
        t.start()
    for t in consumers_:
        t.start()

    for t in producers:
        t.join()
    for t in consumers_:
        t.join()

    end_time = time.time()
    elapsed = end_time - start_time
    total_consumed = len(collected_items)

    return total_consumed, elapsed

if __name__ == "__main__":
    # We’ll test multiple concurrency levels to see how performance scales:
    workloads = [
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8)
    ]
    
    ITEMS_PER_PRODUCER = 5000

    print("ConcurrentQueue Benchmark")
    print(f"Items per producer: {ITEMS_PER_PRODUCER}")
    print("=============================================")
    print("Producers | Consumers | Total Items Consumed | Elapsed (s) | Throughput (ops/s)")
    print("-------------------------------------------------------------------------")

    for (p, c) in workloads:
        total_items, elapsed = run_benchmark(p, c, ITEMS_PER_PRODUCER)
      
        throughput = total_items / elapsed if elapsed > 0 else float('inf')
        
        print(f"{p:9d} | {c:9d} | {total_items:21d} | {elapsed:10.4f} | {throughput:14.2f}")

