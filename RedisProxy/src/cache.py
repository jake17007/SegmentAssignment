import threading
import time

from redis_engine import RedisEngine
from doubly_linked_list import (
    Dllist,
    DllistNode
)

lock = threading.RLock()


class LocalKVNode(DllistNode):
    """
    Doubly-linked list node that holds a key-value (KV) pair.
    """

    def __init__(self, key, value):
        super(LocalKVNode, self).__init__({'k': key, 'v': value})
        self.k = key
        self.v = value
        self.timestamp = time.time()

    def expired(self, expiry_secs):
        """
        Check if the node is expired.
        Parameters:
            expiry_secs int: global expiry (in seconds)
        Returns:
            boolean: True if expired, else False
        """
        return time.time() - self.timestamp > expiry_secs


class CacheStorage(Dllist):
    """
    Doubly-linked list that holds `LocalKVNode`s
    """

    def __init__(self, expiry_secs, max_keys):
        super(CacheStorage, self).__init__()
        self.expiry_secs = expiry_secs
        self.max_keys = max_keys
        self.lookup = {}
        self.total_keys = 0

    def get(self, key):
        """
        Get the value for a given key
        Parameters:
            key str: the key to search for the value
        Returns:
            str or None: the value or None if not found
        """
        with lock:
            if key not in self.lookup:
                return
            local_kv_node = self.lookup[key]
            if not local_kv_node.expired(self.expiry_secs):
                self.move_to_top(local_kv_node)
                return local_kv_node.v

    def set(self, key, value):
        """
        Set the value for a given key
        Paramters:
            key str: the key to be set
            value str: the value to be set
        """
        with lock:
            if key in self.lookup:
                self.delete(self.lookup[key])
            if self.total_keys == self.max_keys:
                del self.lookup[self.bottom.k]
                self.trim_bottom()
            else:
                self.total_keys += 1
            local_kv_node = LocalKVNode(key, value)
            self.append_to_head(local_kv_node)
            self.lookup[key] = local_kv_node

    def clear_cache(self):
        """
        Clear the cache
        """
        with lock:
            self.lookup.clear()
            self.total_keys = 0
            self.top = None
            self.bottom = None


class Cache:

    def __init__(self, host, port, password, expiry_secs, max_keys):
        self.backing_instance = RedisEngine(host, port, password)
        self.cache_storage = CacheStorage(expiry_secs, max_keys)
        self.queued_keys = set()

    def get(self, key):
        """
        Get the value for a given key
        Paramters:
            key str: the key to search for the value
        Returns:
            str or None: the value or None if not found
        """
        # Yield execution to other threads if another thread is already
        # currently retrieving the key-value pair from Redis backing instance
        while key in self.queued_keys:
            time.sleep(0)

        # Attempt to retrieve the key-value pair from cache storage; return the
        # value if the key was found
        with lock:
            value = self.cache_storage.get(key)
            if value:
                return value

        # If the key was not found in cache storage, indicate (to other
        # threads) that this thread will attempt to retrieve the key-value pair
        # from the Redis backing instance, and do so
        self.queued_keys.add(key)
        value = self.backing_instance.get(key)  # non-blocking

        # If the key was found, set the key-value pair in the cache storage.
        # Then, even if it was not found, remove the key from queued keys
        # and return the result
        with lock:
            if value:
                self.cache_storage.set(key, value)
            self.queued_keys.remove(key)
            return value

    def clear_cache(self):
        """
        Clear the cache
        """
        self.cache_storage.clear_cache()
