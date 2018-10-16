import os

from flask import (
    Flask,
    request
)

from cache import Cache

# Configurations set through environment variables
REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', '0.0.0.0')
CACHE_EXP_SECS = float(os.environ.get('CACHE_EXP_SECS', 2))
CACHE_MAX_KEYS = int(os.environ.get('CACHE_MAX_KEYS', 3))

# Instantiate the API and cache
app = Flask(__name__)
cache = Cache(REDIS_ADDRESS, '6379', None, CACHE_EXP_SECS, CACHE_MAX_KEYS)


@app.route('/', methods=['GET'])
def get():
    """
    Get the value for a given key. Requires 'requestedKey'
    in request.
    """
    value = cache.get(request.args.get('requestedKey'))
    if value:
        return value
    return ('', 204)  # Key not found


# For testing
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    """
    Clear the cache. Used for testing. Would be modified in some way
    (injected / set in different place / in different environment /
    require authentication) in live setting.
    """
    cache.clear_cache()
    return('Cleared.')
