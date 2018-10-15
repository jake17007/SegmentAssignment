import time

from flask import (
    Flask,
    request
)

from cache import Cache


def configure_redis_proxy(redis_address, cache_exp_secs, cache_max_keys):

    app = Flask(__name__)
    cache = Cache(redis_address, '6379', None, cache_exp_secs, cache_max_keys)

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

    return app
