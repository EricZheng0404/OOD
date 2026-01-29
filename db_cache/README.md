# Key Features
1. We store (expiration_time, key, value) tuples in the heap. When updating the dictionary, we validate that heap entries match dictionary entries before deletion, preventing premature removal of updated keys.
2. As an alternative, We could also implement an `entry_id` so that every single entry could have their own unique id so that we won't delete the unmatching ids.
3. Lazy deletion. Now, there is a synchronization between dictionary and heap. Before all the dictionary operations, we firt check if there are any expiring keys in the heap, and remove them from the dictionary.

# Future Improvements
## Background cleanup job 

- Redis: Using Probalistic search, Redis samples 20 keys every 100ms. If more than 25% of the keys are expired, Redis repeat the process. In this way, Redis keeps the memory clean without blocking the CPU. 
- Thread: 
1. We implement a `cleanup_thread` and wakes it up every `cleanup_interval` seconds. In this way, the thread cleans up the stale data in the background 
automatically and user experience would be smooth for the most of the time 
without a major latency spike. Say there're a large number of 
expired items sitting in the heap. In the old synchronous implementation, the 
user will experience a huge latency when they do any operations because the 
system is busy with the cleanup. But in this new async implementaion, all the 
expired items have already been cleaned up. 
1. **Locking contention leading to staleness (Zombie Read)**: Since the cleanup 
now runs on a regular interval, there's a possibility that a user get access to an expired  items when the next round of cleanup is not executed yet. So, it's safer to double check if the item is expired in the get() too.

# Things to notice and discuss
1. About TTL
- Per-key or Global? If TTL is global for all keys, then we do not need a heap because all the expiration times will be just in order.
- Resettable? If TTL can be reset using `get()`, for example, then heap will be very expensive since it takes O(N) to iterate through the heap and find the item. Instead, we can use a doubly linked list as in LRU problem. The value of the key corresponding to is a Node. And we can just add and remove these nodes in order.
- Strictness vs. Performance? How strict do we need to be for the real-time removal guarantee? If strict, we may need an active background thread aggressively checking. If not, lazy deletion or a slow background cleanup will be fine.
> In the planning phase, think about how to describe a requirement and the tradeoff between different implementations. 
2. About memory constraint: how much memory do we have? Do we need to evict items when the memory is run out even if the items in the dictionary are not expired?
2.  The tradeoff between cleanup frequency and data consistency: 
1. The tradeoff between performance and data availability.
1. The lifecycle of a product: how does the user call these functions and how often. To let me better understand the when the best cleanup time is


