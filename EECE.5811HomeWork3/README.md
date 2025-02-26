# EECE.5811 Homework 3 — Lock-Based Concurrent Queue

This repository contains a **Python implementation** of a lock-based concurrent queue, inspired by the Michael and Scott queue from Figure 29.8.

## Overview
- **File:** `Lockbasedqueue.py`
- **Concurrency Model:** Uses two locks (one for the head, one for the tail) to allow safe concurrent enqueues and dequeues.
- **Language/Dependencies:** Pure Python (no external dependencies).


## How It Works
1. **Node Class**  
   Each queue node has a `value` and a pointer to `next`.
2. **ConcurrentQueue Class**  
   - Maintains a dummy head and tail node.  
   - Uses two locks:
     - `head_lock` protects dequeue operations.
     - `tail_lock` protects enqueue operations.

3. **enqueue(value)**  
   - Acquires `tail_lock`.
   - Appends a new node and updates the `tail`.
   - Releases `tail_lock`.

4. **dequeue()**  
   - Acquires `head_lock`.
   - If the queue is empty (`head.next == None`), returns `None`.
   - Otherwise, removes the first real element and returns its value.
   - Releases `head_lock`.

## Usage Instructions

1. **Clone the Repo**  
   ```
   git clone https://github.com/vinadang/EECE.5811.git

2. Run the Python Script
   
## Dependencies

1. Python 3.x (required)


