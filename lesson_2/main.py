from framework.wsgi import Framework
from framework.view import HomeView
from framework.url import Url

urls = [
    Url('/', HomeView)
]

app = Framework(urls)