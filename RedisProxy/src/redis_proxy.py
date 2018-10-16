import os
import time

from flask import (
    Flask,
    request
)

from cache import Cache

REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', '0.0.0.0')
CACHE_EXP_SECS = float(os.environ.get('CACHE_EXP_SECS', 2))
CACHE_MAX_KEYS = int(os.environ.get('CACHE_MAX_KEYS', 3))

app = Flask(__name__)
cache = Cache(REDIS_ADDRESS, '6379', None, CACHE_EXP_SECS, CACHE_MAX_KEYS)


@app.route('/', methods=['GET'])
def get():
    value = cache.get(request.args.get('requestedKey'))
    if value:
        return value
    return ('', 204)  # Key not found


# For testing
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    cache.clear_cache()
    return('Cleared.')


@app.route('/slow', methods=['GET'])
def slow():
    start = time.time()
    time.sleep(10)
    end = time.time()
    return 'Start: {}, End: {}'.format(start, end)


@app.route('/fast', methods=['GET'])
def fast():
    return 'fast finished'
