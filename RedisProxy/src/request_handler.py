import json

from http.server import BaseHTTPRequestHandler
from urllib.parse import (
    parse_qs,
    urlparse
)


class RequestHandler(BaseHTTPRequestHandler):

    def __set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        '''
        print('getted')
        self.__set_headers()
        self.wfile.write(json.dumps({'a': 2}).encode())
        '''
        query_components = parse_qs(urlparse(self.path).query)
        key = query_components['myKey'][0]
        value = self.server.get(key)
        self.__set_headers()
        self.wfile.write(json.dumps(value).encode())
        return
