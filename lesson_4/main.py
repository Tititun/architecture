from framework.wsgi import Framework
from framework.view import HomeView, AskView, AboutView, CategoriesView
from framework.url import Url

# noinspection PyTypeChecker
urls = [
    Url('/', HomeView),
    Url('/ask', AskView),
    Url('/about', AboutView),
    Url('/courses', CategoriesView),
]

app = Framework(urls)