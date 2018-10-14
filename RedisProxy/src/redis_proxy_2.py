from http.server import HTTPServer

from request_handler import RequestHandler
from cache import Cache


class RedisProxy(HTTPServer):

    def __init__(self, redis_host='redis-service', redis_port=6379,
                 redis_password=None, server_host='',
                 server_port=5000, max_connections=None, expiry_secs=10,
                 max_keys=100):
        super(RedisProxy, self).__init__((server_host, server_port),
                                         RequestHandler)
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.server_host = server_host
        self.server_port = server_port
        self.expiry_secs = expiry_secs
        self.max_keys = max_keys

    def start(self):
        self.cache = Cache(self.redis_host, self.redis_port,
                           self.redis_password, self.expiry_secs,
                           self.max_keys)
        print('HTTP server listening at {}:{}...'.format(self.server_host,
                                                         self.server_port))
        self.serve_forever()

    def get(self, key):
        value = self.cache.get(key)
        return value


def main():
    proxy = RedisProxy()
    proxy.start()


if __name__ == '__main__':
    main()
