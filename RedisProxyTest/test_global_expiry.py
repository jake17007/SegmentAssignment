"""
These request tests are to be run against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""

import time
from unittest import TestCase

from my_test_engine import MyTestEngine


class GlobalExpiryTest(TestCase):

    def setUp(self):
        self.engine = MyTestEngine()
        self.engine.clear_all()

    # Test if KVs are expiring
    def test_request_cache_expired(self):
        self.engine.populate_redis({'k1': 'v1'})
        self.engine.make_request('k1')  # Dummy request
        self.engine.clear_redis()
        time.sleep(3)
        res = self.engine.make_request('k1')
        assert res.text == ''

    # Test that expired KVs are retrieved from the backing instance
    def test_expired_retrieved_from_bi(self):
        self.engine.populate_redis({'k2': 'v2'})
        self.engine.make_request('k2')  # Dummy request
        time.sleep(3)
        res = self.engine.make_request('k2')
        assert res.text == 'v2'
