"""
db_cache.py 
Implementation of database cache system.
====================================================================
This implementation employs a synchronous cleanup job.
delete_expired() function will clean up any expired key-value in the databse 
before any user-accessible operations.

"""


import heapq
import time

class DB_Cache:
    def __init__(self):
        # A heap of (expiration_time, key, value) pairs
        self.heap: list[tuple[int, int, int]] = []
        # A dictionary to store key: (value, expiration_time) pairs
        self.dictionary: dict[int, tuple[int, float]] = {}

    def delete_expired(self):
        curr_time = time.time()
        while self.heap and self.heap[0][0] <= curr_time:
            expiration_time, key, value = heapq.heappop(self.heap)
            # We do need this condition because we may have deleted it already
            # Or may have updated it
            if (key in self.dictionary and 
                self.dictionary[key][1] == expiration_time and
                self.dictionary[key][0] == value):
                del self.dictionary[key]

    def put(self, key, value, ttl):
        self.delete_expired()
        expiration_time = time.time() + ttl
        # Update the dictionary
        self.dictionary[key] = (value, expiration_time)
        # Update the heap
        heapq.heappush(self.heap, (expiration_time, key, value))


    def check_valid_key(self, key):
        return key in self.dictionary
    
    def get(self, key):
        self.delete_expired()
        if not self.check_valid_key(key):
            raise KeyError("{key} not found")
        return self.dictionary[key][0]
    
    def delete(self, key):
        self.delete_expired()
        if not self.check_valid_key(key):
            raise KeyError("{key} not found")
        # We technically don't need to remove the key from the heap because it
        # will be removed when it's expired: Lazy deletion
        del self.dictionary[key]

    def contains(self, key):
        self.delete_expired()
        return self.check_valid_key(key)

