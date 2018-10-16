import time

from redis_engine import RedisEngine
from doubly_linked_list import (
    Dllist,
    DllistNode
)


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
        if key not in self.lookup:
            return
        local_kv_node = self.lookup[key]
        if not local_kv_node.expired(self.expiry_secs):
            self.move_to_top(local_kv_node)
            return local_kv_node.v

    # May need to lock this for use with threading
    def set(self, key, value):
        """
        Set the value for a given key
        Paramters:
            key str: the key to be set
            value str: the value to be set
        """
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
        self.lookup.clear()
        self.total_keys = 0
        self.top = None
        self.bottom = None


class Cache:

    def __init__(self, host, port, password, expiry_secs, max_keys):
        self.backing_instance = RedisEngine(host, port, password)
        self.cache_storage = CacheStorage(expiry_secs, max_keys)

    def get(self, key):
        """
        Get the value for a given key
        Paramters:
            key str: the key to search for the value
        Returns:
            str or None: the value or None if not found
        """
        value = self.cache_storage.get(key)
        if value:
            return value
        value = self.backing_instance.get(key)
        if value:
            self.cache_storage.set(key, value)
            return value

    def clear_cache(self):
        """
        Clear the cache
        """
        self.cache_storage.clear_cache()
