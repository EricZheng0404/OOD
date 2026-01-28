# Key Features
1. We save (expiration_time, key, value) in the heap so that when users update the dictionary and new tuples are updated to the help, we won't delete the not-expired keys. We make sure that key-value matches

dictionary = {1: (1, 3), 1: (3, 10)}
heap = [(1, 1, 3), (1, 3, 10)] 
- TODO: Potential bug when we have the same key and the same value but different TTL.


# Threads
[] DO MORE RESEARCH ON THREAD
1. **Locking contention leading to staleness**

# Things to notice and discuss
1. The tradeoff between cleanup frequency and data consistency: 
1. The tradeoff between performance and data availability.
1. The lifecycle of a product: how does the user call these functions and how often. To let me better understand the when the best cleanup time is

![alt text](image.png)
executors for the callback?
