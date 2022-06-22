import datetime

URLS = []

def register(url):
    def decorator(f):
        URLS.append((url, f))
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator


def debug(f):
    def wrapper(*args, **kwargs):
        print(f'[{datetime.datetime.now()}] function {f.__qualname__} called.')
        return f(*args, **kwargs)
    return wrapper
