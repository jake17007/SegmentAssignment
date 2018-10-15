import time

import requests
from redis import Redis

REDIS_ADDRESS = 'redis-service'
PROXY_ADDRESS = 'redis-proxy-cache-service-0'
PROXY_PORT = '5000'

R = Redis(REDIS_ADDRESS, 6379, None)
P = 'http://' + PROXY_ADDRESS + ':' + PROXY_PORT


def clear_redis():
    R.flushall()


def populate_redis(d):
    for k, v in d.items():
        R.set(k, v)


def make_request(key):
    params = {'myKey': key}
    res = requests.get(url=P, params=params)
    return res


"""
These request tests are to be run in order against a new RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""


# Test simple request for key existing in backing instance
def test_request_good():
    clear_redis()
    populate_redis({'k1': 'v1'})
    res = make_request('k1')
    assert res.text == 'v1'


# Test simple request for key not existing in backing instance
def test_request_bad():
    clear_redis()
    res = make_request('k2')
    assert res.text == ''


# Test if KVs are added to cache
def test_request_cache_unexpired():
    populate_redis({'k3': 'v3'})
    make_request('k3')  # Dummy request
    clear_redis()
    res = make_request('k3')
    assert res.text == 'v3'


# Test if KVs are expiring
def test_request_cache_expired():
    populate_redis({'k4': 'v4'})
    make_request('k4')  # Dummy request
    clear_redis()
    time.sleep(3)
    res = make_request('k4')
    assert res.text == ''


# Test if LRU KVs are pushed out of cache
def test_request_cache_pushed_out():
    populate_redis({'k5.1': 'v5.1',
                    'k5.2': 'v5.2',
                    'k5.3': 'v5.3',
                    'k5.4': 'v5.4'})
    make_request('k5.1')
    make_request('k5.2')
    make_request('k5.3')
    make_request('k5.4')
    clear_redis()
    res_bad = make_request('k5.1')
    res_good = make_request('k5.2')
    assert res_bad.text == ''
    assert res_good.text == 'v5.2'


# Test if recently called KVs are renewed (sent to top)
def test_request_cache_renewed():
    populate_redis({'k6.1': 'v6.1',
                    'k6.2': 'v6.2',
                    'k6.3': 'v6.3',
                    'k6.4': 'v6.4'})
    make_request('k6.1')
    make_request('k6.2')
    make_request('k6.3')
    make_request('k6.1')  # Renew k6.1 so it doesn't get pushed out
    make_request('k6.4')
    clear_redis()
    res_bad = make_request('k6.2')  # k6.2 gets pushed out instead
    res_good = make_request('k6.1')
    assert res_bad.text == ''
    assert res_good.text == 'v6.1'


# Test that expired KVs are retrieved from the backing instance
def test_expired_retrieved_from_bi():
    populate_redis({'k7.1': 'v7.1'})
    make_request('k7.1')
    time.sleep(3)
    res = make_request('k7.1')
    assert res.text == 'v7.1'


# Test that KVs pushed out by more recent KVs are retrieved from the backing
# instance
def test_pushed_out_retrieved_from_bi():
    populate_redis({'k8.1': 'v8.1',
                    'k8.2': 'v8.2',
                    'k8.3': 'v8.3',
                    'k8.4': 'v8.4'})
    make_request('k8.1')
    make_request('k8.2')
    make_request('k8.3')
    make_request('k8.4')  # Pushes out k8.1
    res = make_request('k8.1')
    assert res.text == 'v8.1'
