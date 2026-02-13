"""
db_cache2.py 
Asynchronous implementation of database cache system.
====================================================================
This implementation employs a asychrnonous cleanup job.
There is a cleanup thread 

"""
import heapq
import time
import threading

class DB_Cache:
    def __init__(self, cleanup_interval=5):
        # A heap of (expiration_time, key, value) pairs
        self.heap: list[tuple[int, int, int]] = []
        # A dictionary to store key: (value, expiration_time) pairs
        self.dictionary: dict[int, tuple[int, float]] = {}
        self.cleanup_interval = cleanup_interval
        # Thread Safety: 
        # Since there are two thread (Main + Cleanup), we need a lock
        # to protect the critical section
        self.lock = threading.Lock()
        # Background worker
        self.cleanup_thread = threading.Thread(target=self._clean_up, 
                                               daemon=True)
        
        self.cleanup_thread.start()

    def _clean_up(self):
        while True:
            # Sleep for self.cleanup_interval seconds and run
            time.sleep(self.cleanup_interval)
            self._delete_expired()
        
    def _delete_expired(self):
        # We want to keep the critical section as small and fast as possible.
        # To get the current time is not something.
        # This section doesn't need the lock, so it's outside of `with`.
        curr_time = time.time()
        # Lock the critical section so that other opertions doesn't modify
        # the dict
        with self.lock:
            while self.heap and self.heap[0][0] <= curr_time:
                expiration_time, key, value = heapq.heappop(self.heap)
                # We do need this condition because we may have deleted it already
                # Or may have updated it
                if (key in self.dictionary and 
                    self.dictionary[key][1] == expiration_time and
                    self.dictionary[key][0] == value):
                    del self.dictionary[key]

    def put(self, key, value, ttl):
        expiration_time = time.time() + ttl
        with self.lock:
            # Update the dictionary
            self.dictionary[key] = (value, expiration_time)
            # Update the heap
            heapq.heappush(self.heap, (expiration_time, key, value))


    def check_valid_key(self, key):
        return key in self.dictionary
    
    def get(self, key):
        now = time.time()
        with self.lock:
            if not self.check_valid_key(key):
                raise KeyError("{key} not found")
            value, expiration_time = self.dictionary[key]
            if expiration_time <= now:
                del self.dictionary[key]
                raise KeyError("{key} not found")
            return value
    
    def delete(self, key):
        with self.lock:
            if not self.check_valid_key(key):
                raise KeyError("{key} not found")
            # We technically don't need to remove the key from the heap because it
            # will be removed when it's expired: Lazy deletion
            del self.dictionary[key]

    def contains(self, key):
        with self.lock:
            return self.check_valid_key(key)

