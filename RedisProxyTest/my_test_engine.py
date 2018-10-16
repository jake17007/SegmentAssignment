import os

import requests
from redis import Redis

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
        self.redis_conn.flushall()

    def clear_cache(self):
        requests.get(url=self.proxy_url+'/clear_cache')

    def clear_all(self):
        self.clear_redis()
        self.clear_cache()

    def populate_redis(self, d):
        for k, v in d.items():
            self.redis_conn.set(k, v)

    def make_request(self, key):
        params = {'requestedKey': key}
        res = requests.get(url=self.proxy_url, params=params)
        return res
