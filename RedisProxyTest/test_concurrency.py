"""
These request tests are to be run against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os

from my_test_engine import MyTestEngine
from unittest import TestCase


class SingleBackingInstanceTest(TestCase):

    def setUp(self):
        proxy_addr = os.environ.get('PROXY_ADDRESS_0')
        proxy_port = os.environ.get('PROXY_PORT_0')
        self.engine = MyTestEngine(proxy_address=proxy_addr,
                                   proxy_port=proxy_port)
        self.engine.clear_all()

    def test_concurrency(self):
        self.engine.populate_redis({'k1': 'v1'})
        keys = ['k1'] * 2
        with ThreadPoolExecutor(max_workers=2) as executor:
            futs = {executor.submit(self.engine.make_request, key)
                    for key in keys}
            concurrent.futures.wait(futs)
        res = [fut.result().text for fut in futs]
        assert res == ['v1', 'v1']
