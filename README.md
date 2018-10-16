# Redis HTTP Cache Proxy
Redis Cache Proxy Assignment for Segment

## Architecture Overview

![(Diagram.png)](https://raw.githubusercontent.com/jake17007/SegmentAssignment/master/Diagram.png)

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
