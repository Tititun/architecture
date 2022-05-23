from framework.wsgi import Framework
from framework.view import HomeView, AskView
from framework.url import Url

urls = [
    Url('/', HomeView),
    Url('ask', AskView)
]

app = Framework(urls)