from framework.wsgi import Framework
from framework.view import HomeView, AskView, AboutView
from framework.url import Url

urls = [
    Url('/', HomeView),
    Url('/ask', AskView),
    Url('/about', AboutView),
]

app = Framework(urls)