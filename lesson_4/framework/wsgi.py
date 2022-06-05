from .request import Request
from .response import Response
from .view import View
from .logger import Logger

logger = Logger('wsgi')

class Framework:
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, environ, start_response):
        request = Request(environ)
        view = self.get_view(request)
        response = self.get_response(request, view)
        logger.write(f'Served page {request.path}'
                     f' with status {response.status}')
        start_response(response.status, [
            ('Content-Type', 'text/html; charset=utf-8')])

        return [response.body.encode('utf-8')]

    def get_view(self, request: Request):
        path = request.base_url
        for url in self.urls:
            if url.path == path:
                return url.view
        return Response('404 ERROR', 'page not found')

    @staticmethod
    def get_response(request: Request, view: View) -> Response:
        if hasattr(view, request.method):
            return getattr(view, request.method)(view, request)
        return Response('400 ERROR', 'method not supported')
