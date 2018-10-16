import os

import requests
from redis import Redis

# Default configurations can be set with environment variables
REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', 'redis-service')
PROXY_ADDRESS_0 = os.environ.get('PROXY_ADDRESS_0',
                                 'redis-proxy-cache-service-0')
PROXY_PORT_0 = os.environ.get('PROXY_PORT_0', 5000)
PROXY_ADDRESS_1 = os.environ.get('PROXY_ADDRESS_1',
                                 'redis-proxy-cache-service-1')
PROXY_PORT_1 = os.environ.get('PROXY_PORT_1', 5001)


class MyTestEngine:

    def __init__(self, proxy_address=PROXY_ADDRESS_0, proxy_port=PROXY_PORT_0):
        self.redis_conn = Redis(REDIS_ADDRESS, 6379, None)
        self.proxy_url = 'http://' + proxy_address + ':' + proxy_port

    def clear_redis(self):
        """
        Clear all key-values pairs from Redis backing instance
        """
        self.redis_conn.flushall()

    def clear_cache(self):
        """
        Clear cache of the proxy instance
        """
        requests.get(url=self.proxy_url+'/clear_cache')

    def clear_all(self):
        """
        Clear Redis and proxy data
        """
        self.clear_redis()
        self.clear_cache()

    def populate_redis(self, d):
        """
        Populate Redis backing instance from the given dictionary
        Parameters:
            d dict: a dictionary of key-value pairs
        """
        for k, v in d.items():
            self.redis_conn.set(k, v)

    def make_request(self, key):
        """
        Make an HTTP GET request to the proxy instance
        Parameters:
            key str: the string to search for the value
        """
        params = {'requestedKey': key}
        res = requests.get(url=self.proxy_url, params=params)
        return res
