"""
These request tests are to be run against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""
import os

from my_test_engine import MyTestEngine
from unittest import TestCase


class SingleBackingInstanceTest(TestCase):

    def setUp(self):

        # First Proxy
        proxy_addr_0 = os.environ.get('PROXY_ADDRESS_0')
        proxy_port_0 = os.environ.get('PROXY_PORT_0')
        self.engine0 = MyTestEngine(proxy_address=proxy_addr_0,
                                    proxy_port=proxy_port_0)

        # Second Proxy
        proxy_addr_1 = os.environ.get('PROXY_ADDRESS_1')
        proxy_port_1 = os.environ.get('PROXY_PORT_1')
        self.engine1 = MyTestEngine(proxy_address=proxy_addr_1,
                                    proxy_port=proxy_port_1)

        self.engine0.clear_all()
        self.engine1.clear_all()

    def test_single_backing_instance(self):
        self.engine0.populate_redis({'k1': 'v1'})
        res = self.engine1.make_request('k1')
        assert res.text == 'v1'
