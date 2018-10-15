"""
These request tests are to be run in order against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""

from my_test_engine import MyTestEngine
from unittest import TestCase


class LRUEvictionFixedKeySizeTest(TestCase):

    def setUp(self):
        self.engine = MyTestEngine()
        self.engine.clear_all()

    # Test if LRU KVs are pushed out of cache
    def test_request_cache_pushed_out(self):
        self.engine.populate_redis({'k1.1': 'v1.1',
                                    'k1.2': 'v1.2',
                                    'k1.3': 'v1.3',
                                    'k1.4': 'v1.4'})
        self.engine.make_request('k1.1')  # Dummy requests
        self.engine.make_request('k1.2')
        self.engine.make_request('k1.3')
        self.engine.make_request('k1.4')
        self.engine.clear_redis()
        res_bad = self.engine.make_request('k1.1')
        res_good = self.engine.make_request('k1.2')
        assert res_bad.text == ''
        assert res_good.text == 'v1.2'

    # Test if recently called KVs are renewed (sent to top)
    def test_request_cache_renewed(self):
        self.engine.populate_redis({'k2.1': 'v2.1',
                                    'k2.2': 'v2.2',
                                    'k2.3': 'v2.3',
                                    'k2.4': 'v2.4'})
        self.engine.make_request('k2.1')
        self.engine.make_request('k2.2')
        self.engine.make_request('k2.3')
        self.engine.make_request('k2.1')  # Renew k2.1 so it's not pushed out
        self.engine.make_request('k2.4')
        self.engine.clear_redis()
        res_bad = self.engine.make_request('k2.2')  # k2.2 gets pushed out
        res_good = self.engine.make_request('k2.1')
        assert res_bad.text == ''
        assert res_good.text == 'v2.1'

    # Test that KVs pushed out by more recent KVs are retrieved from the
    # backing instance
    def test_pushed_out_retrieved_from_bi(self):
        self.engine.populate_redis({'k3.1': 'v3.1',
                                    'k3.2': 'v3.2',
                                    'k3.3': 'v3.3',
                                    'k3.4': 'v3.4'})
        self.engine.make_request('k3.1')
        self.engine.make_request('k3.2')
        self.engine.make_request('k3.3')
        self.engine.make_request('k3.4')  # Pushes out k3.1
        res = self.engine.make_request('k3.1')
        assert res.text == 'v3.1'
