import time

from redis_engine import RedisEngine
from doubly_linked_list import (
    Dllist,
    DllistNode
)


class LocalKVNode(DllistNode):

    def __init__(self, key, value):
        super(LocalKVNode, self).__init__({'k': key, 'v': value})
        self.k = key
        self.v = value
        self.timestamp = time.time()

    def expired(self, expiry_secs):
        return time.time() - self.timestamp > expiry_secs


class CacheStorage(Dllist):

    def __init__(self, expiry_secs, max_keys):
        super(CacheStorage, self).__init__()
        self.expiry_secs = expiry_secs
        self.max_keys = max_keys
        self.lookup = {}
        self.total_keys = 0

    def get(self, key):
        if key not in self.lookup:
            return
        local_kv_node = self.lookup[key]
        if not local_kv_node.expired(self.expiry_secs):
            self.move_to_top(local_kv_node)
            print(local_kv_node.value)
            return local_kv_node.v

    # May need to lock this for use with threading
    def set(self, key, value):
        if key in self.lookup:
            self.delete(self.lookup[key])
        if self.total_keys == self.max_keys:
            print('trim_bottom called with {}'.format(key))
            print(self.bottom.value)
            del self.lookup[self.bottom.k]
            self.trim_bottom()
        else:
            print('+= 1 called with {}'.format(key))
            self.total_keys += 1
        local_kv_node = LocalKVNode(key, value)
        self.append_to_head(local_kv_node)
        self.lookup[key] = local_kv_node


class Cache:

    def __init__(self, host, port, password, expiry_secs, max_keys):
        self.backing_instance = RedisEngine(host, port, password)
        self.cache_storage = CacheStorage(expiry_secs, max_keys)

    def get(self, key):
        value = self.cache_storage.get(key)
        if value:
            return value
        value = self.backing_instance.get(key)
        if value:
            self.cache_storage.set(key, value)
            return value
