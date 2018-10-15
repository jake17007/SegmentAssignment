"""
These request tests are to be run in order against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""
from unittest import TestCase

from my_test_engine import MyTestEngine


class CachedGETTest(TestCase):

    def setUp(self):
        self.engine = MyTestEngine()
        self.engine.clear_all()

    # Test if KVs not in cache are retrieved from backing instance
    def test_retrieved_from_bi(self):
        self.engine.populate_redis({'k1': 'v1'})
        res = self.engine.make_request('k1')
        assert res.text == 'v1'

    # Test if KVs are added to cache
    def test_request_cache_unexpired(self):
        self.engine.populate_redis({'k2': 'v2'})
        self.engine.make_request('k2')  # Dummy request
        self.engine.clear_redis()
        res = self.engine.make_request('k2')
        assert res.text == 'v2'
