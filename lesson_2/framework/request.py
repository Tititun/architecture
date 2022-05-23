class Request:
    def __init__(self, environ: dict):
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].lower()
        self.path = environ['RAW_URI'].lower()
        self.query_params = self.get_query_params()
        self.headers = self.get_headers()

    def get_headers(self) -> dict:
        return {k[5:]: v for k, v in self.environ if k.starts_with('HTTP_ ')}

    def get_query_params(self) -> dict:
        qs = self.environ.get('QUERY_STRING')
        params = {}
        if qs:
            pairs = qs.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                params[key] = value
        return params
