import re

class Request:
    def __init__(self, environ: dict,  params=None):
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].lower()
        self.path = environ['RAW_URI'].lower().split('?')[0]
        self.base_url = re.match(r'/[^/]*', self.path).group()
        self.query_params = params if params else self.get_query_params()
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


def get_request_redirect(view, request, method, params):
    request.environ['REQUEST_METHOD'] = method
    request = Request(request.environ, params=params)
    view = view()
    return getattr(view, method)(request)
