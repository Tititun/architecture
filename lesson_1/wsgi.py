"""Module with the main function of the wsgi application"""
from urls import UrlDispatcher

def application(environ, start_response):
    """
    :param environ: server dictionary data
    :param start_response: function for the server response
    """
    start_response('200 OK', [('Content-Type', 'text/html')])
    url = environ['RAW_URI']
    method = environ['REQUEST_METHOD']
    page = UrlDispatcher(url, method).get_page()

    return [page.encode('utf-8')]
