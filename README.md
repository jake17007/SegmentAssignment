# Redis HTTP Cache Proxy
Redis Cache Proxy Assignment for Segment

## Architecture Overview

![(ArchitectureImg.png)](https://raw.githubusercontent.com/jake17007/SegmentAssignment/master/ArchitectureImg.png)

The Redis HTTP Cache Proxy is a containerized service that allows clients to query data stored in a single Redis database via HTTP. It holds a "Least Recently Used" (LRU) cache, per-instance configurable, as a way of optimizing the efficiency of queries and reducing load on the Redis backing instance.

### API

The client facing API contains a GET endpoint that allows users to query by key, as if they were querying the Redis database. It is written in Flask and served by Gunicorn. The server is configurable at proxy instantiation with an options to limit the number of pending connections to the server and determine whether the processing of requests should run in a concurrent sequential or multi-threaded parallel manner (though the multi-threaded manner has not been sufficiently tested).

### Cache

The LRU cache stores recently queried data in key-value pairs. If it does not contain a given key at the time of a query, it will query the Redis backing instance to see if it contains the key; if the key is found, it will be added to the cache, and if by doing so the cache exceeds the maximum threshold (determined by number of keys), the least recently used key-value pair will be pushed out. The cache also implements a global expiry functionality per key, such that if any key has expired in the cache, it will be as if the key is not in the cache. The cache threshold, global expiry, and location of the Redis backing instance are configurable per-instance at proxy startup.

### Redis Backing Instance

There exists a single Redis backing instance in this architecture. That means that any proxy instantiated should access the same Redis instance.

### End-to-End Tests

End-to-end tests exist to test the functionality of the architecture.

### Docker

The Redis HTTP Cache Proxy, including the API and cache, Redis backing instance, and end-to-end testing unit are instatiated as separate Docker containers. For the purposes of this assignment, the containers are initialized in a docker-compose file.

## What the Code Does

```
├── Diagram.png
├── Makefile
├── README.md
├── RedisProxy
├── RedisProxyTest
└── docker-compose.yml
```

### RedisProxy

The `RedisProxy` directory contains the API and cache as well as a Dockerfile and requirements.txt for container instantiation.

```
├── RedisProxy
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── cache.py
│       ├── doubly_linked_list.py
│       ├── redis_engine.py
│       ├── redis_proxy.py
│       └── server.py
```

- `cache.py`: a `Cache` class and supporting classes that store key-value pair and handles LRU and global expiry functionality
- `doubly_linked_list.py`: a class for basic doubly-linked-list and node funtionality (from which the `Cache` class inherits)
- `redis_engine.py`: a `RedisEngine` class for connecting to the Redis backing instance; the `Cache` class uses this to load unknown key-value pairs
- `redis_proxy.py`: a Flask application that contains the client facing API endpoints; contains a `Cache` class to load data
- `server.py`: a file for instantiating the server with Gunicorn

### RedisProxyTest

The `RedisProxyTest` directory contains a test engine for manipulating the cache and Redis database for tests, end-to-end tests that make HTTP requests to a given Redis Cache Proxy instance, and a Dockerfile and requirements.txt for container instantiation. Tests are run the the PyTest Python package.

```
├── RedisProxyTest
│   ├── Dockerfile
│   ├── my_test_engine.py
│   ├── populate_for_fun.py
│   ├── requirements.txt
│   ├── test_cached_get.py
│   ├── test_global_expiry.py
│   ├── test_http_web_service.py
│   ├── test_lru_eviction_fixed_key_size.py
│   └── test_single_backing_instance.py
```

- `my_test_engine.py`: a `MyTestEngine` class for connecting to and manipulating the cache and Redis database
- `test_*.py`: end-to-end test files for testing system functionality

### Algorithmic Complexity of the Cache Operations

![(CacheImg.png)](https://raw.githubusercontent.com/jake17007/SegmentAssignment/master/CacheImg.png)
