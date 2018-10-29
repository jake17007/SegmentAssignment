import os
import sys
from threading import Thread
import time
from unittest import mock

from cache import Cache


# Case: one key is requested that is already stored in the cache
@mock.patch('cache.RedisEngine')
@mock.patch('cache.CacheStorage')
def test_get_single(mock_cs, mock_redis):
    mock_cs.return_value.get = mock.Mock(return_value='bar')
    mock_redis.return_value.get = mock.Mock()
    cache = Cache('fake-host', 1234, None, 1, 3)
    assert cache.get('foo') == 'bar'
    mock_cs.return_value.get.assert_called_once_with('foo')
    mock_redis.return_value.get.assert_not_called()


# Case: one key is requested that is not stored in the cache but is stored in
# Redis
@mock.patch('cache.RedisEngine')
@mock.patch('cache.CacheStorage')
def test_get_single_none_but_in_redis(mock_cs, mock_redis):
    mock_cs.return_value.get = mock.Mock(return_value=None)
    mock_redis.return_value.get = mock.Mock(return_value='bar')
    mock_cs.return_value.set = mock.Mock()
    cache = Cache('fake-host', 1234, None, 1, 3)
    assert cache.get('foo') == 'bar'
    mock_cs.return_value.get.assert_called_once_with('foo')
    mock_redis.return_value.get.assert_called_once_with('foo')
    mock_cs.return_value.set.assert_called_once_with('foo', 'bar')


# Case: one key is requested that is not is the cache or Redis
@mock.patch('cache.RedisEngine')
@mock.patch('cache.CacheStorage')
def test_get_single_none(mock_cs, mock_redis):
    mock_cs.return_value.get = mock.Mock(return_value=None)
    mock_redis.return_value.get = mock.Mock(return_value=None)
    mock_cs.return_value.set = mock.Mock()
    cache = Cache('fake-host', 1234, None, 1, 3)
    assert cache.get('foo') == None
    mock_cs.return_value.get.assert_called_once_with('foo')
    mock_redis.return_value.get.assert_called_once_with('foo')
    mock_cs.return_value.set.assert_not_called()


def mock_redis_get_a(key):
    time.sleep(.05)
    return 'bar'


# Case: multiple threads request one key that is not stored in the cache but
# but exists in Redis
@mock.patch('cache.RedisEngine')
def test_multithreaded_same_keys(mock_redis):

    mock_redis.return_value.get = mock.Mock(side_effect=mock_redis_get_a)
    cache = Cache('fake-host', 1234, None, 1, 3)

    def call_get(key, result, idx):
        result[idx] = cache.get(key)

    threads = [None] * 2
    results = [None] * 2
    for i in range(len(threads)):
        threads[i] = Thread(target=call_get, args=('foo', results, i))
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
    assert results == ['bar', 'bar']

    # Although multiple threads are accessing the same key concurrently, the
    # call to Redis is only made once. The other thread waits while the other
    # has not yet removed the key from the queued_keys set
    mock_redis.return_value.get.assert_called_once_with('foo')


def mock_redis_get_b(key):
    time.sleep(1)
    return 'bar1'


# Case: multiple threads request two distinct keys. The first key requested
# does not exist in the cache, so it must be retrieved from Redis (which has
# been mocked to take 1 full second). While this is happening the other
# thread can retrieve the key that does exist in the cache; it will return
# first.
@mock.patch('cache.RedisEngine')
def test_multithreaded_different_keys(mock_redis):

    mock_redis.return_value.get = mock.Mock(side_effect=mock_redis_get_b)
    cache = Cache('fake-host', 1234, None, 1, 3)
    cache.cache_storage.set('foo2', 'bar2')

    def call_get(key, result, idx):
        res = cache.get(key)
        result[idx] = (res, time.time())

    keys = ['foo1', 'foo2']
    threads = [None] * 2
    results = [None] * 2
    for i in range(len(threads)):
        threads[i] = Thread(target=call_get, args=(keys[i], results, i))
        threads[i].start()
        time.sleep(.02)
    for i in range(len(threads)):
        threads[i].join()
    assert results[0][0] == 'bar1'
    assert results[1][0] == 'bar2'
    assert results[0][1] > results[1][1]  # second call finishes first

    mock_redis.return_value.get.assert_called_once_with('foo1')
