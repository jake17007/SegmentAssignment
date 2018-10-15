"""
These request tests are to be run in order against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""
from unittest import TestCase

from my_test_engine import MyTestEngine


class HTTPWebServiceTest(TestCase):

    def setUp(self):
        self.engine = MyTestEngine()
        self.engine.clear_all()

    # Test simple request for key existing in backing instance
    def test_request_good(self):
        self.engine.populate_redis({'k1': 'v1'})
        res = self.engine.make_request('k1')
        assert res.text == 'v1'

    # Test simple request for key not existing in backing instance
    def test_request_bad(self):
        res = self.engine.make_request('k2')
        assert res.text == ''
