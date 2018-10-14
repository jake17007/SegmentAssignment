from flask import (
    Flask,
    request
)
from cache import Cache
import sys


app = Flask(__name__)
cache = Cache('redis-service', '6379', None, 10000, 100)


@app.route('/', methods=['GET'])
def get():
    value = cache.get(request.args.get('myKey'))
    return value


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=sys.argv[1], debug=True)
