from pprint import pprint
from .entities import Student
from .request import Request
from .response import Response
from .view import View
from .logger import Logger
from.url import Url

logger = Logger('wsgi')


class Framework:
    def __init__(self, urls):
        self.urls = [Url(url[0], url[1]) for url in urls]

    def __call__(self, environ, start_response):
        request = Request(environ)
        if id_ := request.cookies.get('user_id'):
            user = Student.fetch_user_by_id(id_)
            request.cookies['user'] = user.__dict__
        view = self.get_view(request)
        response = self.get_response(request, view)
        logger.write(f'Served page {request.path}'
                     f' with status {response.status}')
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        if response.header:
            for k, v in response.header.items():
                headers.append((k, v))
        start_response(response.status, headers)

        return [response.body.encode('utf-8')]

    def get_view(self, request: Request):
        path = request.base_url
        for url in self.urls:
            if url.path == path:
                return url.view
        return Response('404 ERROR', 'page not found', {})

    @staticmethod
    def get_response(request: Request, view: View) -> Response:
        if hasattr(view, request.method):
            return getattr(view, request.method)(view, request)
        return Response('400 ERROR', 'method not supported', {})


class LoggingFramework(Framework):
    def get_view(self, request: Request):
        print('Request method:', request.method)
        print('Request parameters:', request.query_params)
        print('Request path:', request.path)
        print('========================')
        return super().get_view(request)


class FakeFramework(Framework):
    def __call__(self, environ, start_response):
        response = Response('200 OK', 'Hello from Fake', {})
        return [response.body.encode('utf-8')]
