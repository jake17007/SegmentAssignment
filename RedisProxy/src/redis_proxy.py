import sys
import time

from flask import (
    Flask,
    request
)

from cache import Cache

REDIS_ADDRESS = sys.argv[1]
CACHE_EXP_SECS = sys.argv[2]
CACHE_MAX_KEYS = sys.argv[3]
PROXY_PORT = sys.argv[4]

app = Flask(__name__)
cache = Cache(REDIS_ADDRESS, '6379', None, CACHE_EXP_SECS, CACHE_MAX_KEYS)


@app.route('/', methods=['GET'])
def get():
    value = cache.get(request.args.get('myKey'))
    return value


@app.route('/slow', methods=['GET'])
def slow():
    start = time.time()
    time.sleep(10)
    end = time.time()
    return 'Start: {}, End: {}'.format(start, end)


@app.route('/fast', methods=['GET'])
def fast():
    return 'fast finished'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PROXY_PORT, debug=True)
