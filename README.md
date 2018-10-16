# Redis HTTP Cache Proxy
Redis Cache Proxy Assignment for Segment

## Architecture Overview

![(ArchitectureImg.png)](https://raw.githubusercontent.com/jake17007/SegmentAssignment/master/readme_images/ArchitectureImg.png)

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

## Algorithmic Complexity of the Cache Operations

![(CacheImg.png)](https://raw.githubusercontent.com/jake17007/SegmentAssignment/master/readme_images/CacheImg.png)

The cache storage is composed of a hash map, mapping a given key to a respective node in a doubly-linked list. This nodes contains the value along with the key, timestamp, parent node (pertaining to a key that was used more recently), and child node (pertaining to a key that was used less recently).

The time complexity for any given operation on the cache is *O(1)*, i.e. constant time. The space complexity of the cache is *O(m)*, where *m* is the maximum threshold of key-value pairs, which has been configured at instantiation. The operations are explained in more detail below.

### Getting a Key Existing in Cache

The time complexity to retrieve the value for a given key that exists in the cache is O(1). This is because the keys existing in the cache are stored in a hash map, mapping the keys to nodes containing the value.

### Getting a Key Existing Only in Redis Backing Instance

If the cache does not contain a given key, it will attempt to load from the Redis backing instance. If it is found, it will be added to the top of the doubly-linked list and returned. Since we keep track of which node is `top`, this is done in *O(1)* time.

### Pushing Out LRU (Least-Recently Used) Keys

When the cache is at maximum capacity and a new key needs to be added, the LRU is removed from the linked list. We check which node is `bottom`, modify its parent to be the new bottom and remove its connection to the pushed out node, and remove the key from the lookup. This all happens in *O(1)* time.

### Moving MRU (Most-Recently Used) Keys to the Top

When key that had already existed in the cache is requested, it becomes the MRU key. Therefore, it needs to be moved to the top. We remove it from its current position by modifying parent/child links to/from surrounding nodes, and append it to the top. This happens in *O(1)* time.

### Checking Expiration

When a node is inserted into the doubly-linked list, we attached a timestamp. When we retrieve a node, we check that the node is not expired by comparing it to the current time and the global expiry. If the node is expired we attempt to retrieve it from the Redis backing instance. If it is retrieved, the new node will be added to the top (and before doing so delete the old node from the cache). If it is not found, while we could, it's not necessary to remove the expired node from the cache because all nodes less recently used will also be expired. They will just get pushed out as more nodes are added. This happens in O(1).

## Instructions for Running

To run the code and tests, make sure you have installed Git, Docker, docker-compose, and GNU Make (i.e. you can run `make test`) installed; then run the following commands.

```
$ git clone git@github.com:jake17007/SegmentAssignment.git
$ cd SegmentAssignment
$ make test
```

(If you don't have a GitHub SSH key setup clone with: `$ git clone https://github.com/jake17007/SegmentAssignment.git`)

This will run docker-compose to spin up the Docker containers -- a container for Redis, two separate Redis Proxy Cache on two separate containers, and a container to run end-to-end tests.

After the tests complete, the containers will still be running. At this time you can test the endpoints by pointing your browser to `127.0.0.1:5000?requestedKey=SEGMENT` (port `5001` will also work). You can also manipulate the Redis backing instance with `redis-cli` via the default port `6379`.

To run the code in a customized way, you should edit the `docker-compose.yml` and `Dockerfile`s.

I.e.:

- `RedisProxy/Dockerfile`
- `RedisProxyTest/Dockerfile`
- `docker-compose.yml`

For example, you can edit the MAX_CONNECTIONS, REDIS_ADDRESS, CACHE_EXP_SECS, CACHE_MAX_KEYS variables.

## How Long I Spent on Each Part of the Project

- HTTP Web Service (1.5 hours)
- Redis Setup (1.5 hours)
- Cache (1.5 hours)
- Platform (3 hours)
- Testing (1.5 hours)
- Documentation (1.5 hours)
- Note: I spent a bit longer on most of these items, to try to get them just right. The platform took a while because I did not have much experience with Docker and docker-compose (and they are confusing with convoluted documentation, but I wanted to learn them!).

## Requirements Not Implemented

I did not implement the bonus as of yet. While I would have liked to, I didn't have time. All other requirements should be implemented.
