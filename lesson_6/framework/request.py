import re

class Request:
    def __init__(self, environ: dict,  params=None, cookies=None):
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].lower()
        self.path = environ['RAW_URI'].lower().split('?')[0]
        self.base_url = re.match(r'/[^/]*', self.path).group()
        self.query_params = params if params else self.get_query_params()
        self.cookies = cookies if cookies else self.get_cookies()
        self.headers = self.get_headers()

    def get_headers(self) -> dict:
        return {k[5:]: v for k, v in self.environ.items()
                if k.startswith('HTTP_ ')}

    def get_query_params(self) -> dict:
        qs = self.environ.get('QUERY_STRING')
        params = {}
        if qs:
            pairs = qs.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                params[key] = value
        return params

    def get_cookies(self):
        qs = self.environ.get('HTTP_COOKIE')
        cookies = {}
        if qs:
            pairs = qs.split(';')
            for pair in pairs:
                key, value = pair.strip().split('=')
                cookies[key] = value
        return cookies


def get_request_redirect(view, request, method, params, cookies=None):
    request.environ['REQUEST_METHOD'] = method
    request = Request(request.environ, params=params, cookies=cookies)
    view = view()
    return getattr(view, method)(request)
