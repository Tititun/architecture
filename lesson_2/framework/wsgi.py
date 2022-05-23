from .request import Request
from .response import Response
from .view import View


class Framework:
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, environ, start_response):
        request = Request(environ)
        view = self.get_view(request)
        response = self.get_response(request, view)
        start_response(response.status, [('Content-Type', 'text/html')])

        return [response.body.encode('utf-8')]

    def get_view(self, request: Request):
        path = request.path
        for url in self.urls:
            if url.path == path:
                return url.view
        return

    @staticmethod
    def get_response(request:Request, view:View) -> Response:
        if hasattr(view, request.method):
            return getattr(view, request.method)(view, request)
        return Response('400', 'method not supported')
