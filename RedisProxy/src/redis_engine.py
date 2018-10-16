import redis


class RedisEngine:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.__connect()

    def __connect(self):
        """
        Connect to a redis instance
        """
        self.conn = redis.Redis(self.host, self.port, self.password)
        print('Connected to Redis instance at {}:{}'.format(self.host,
                                                            self.port))

    def get(self, key):
        """
        Get the value for a given key
        Returns:
            str or None: the value or None if not found
        """
        return self.conn.get(key)
