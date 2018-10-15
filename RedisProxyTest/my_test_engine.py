import requests
from redis import Redis

# Local debugging
REDIS_ADDRESS = '127.0.0.1'
PROXY_ADDRESS = '127.0.0.1'
PROXY_PORT = '5000'
'''
# Docker debugging
REDIS_ADDRESS = 'redis-service'
PROXY_ADDRESS = 'redis-proxy-cache-service-0'
PROXY_PORT = '5000'
'''


class MyTestEngine:

    def __init__(self):
        self.redis_conn = Redis(REDIS_ADDRESS, 6379, None)
        self.proxy_url = 'http://' + PROXY_ADDRESS + ':' + PROXY_PORT

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
