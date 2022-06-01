from framework.wsgi import Framework
from framework.view import (HomeView, AskView, AboutView, CategoriesView,
                            CategoryEdit)
from framework.url import Url

# noinspection PyTypeChecker
urls = [
    Url('/', HomeView),
    Url('/ask', AskView),
    Url('/about', AboutView),
    Url('/categories', CategoriesView),
    Url('/category_edit', CategoryEdit),
]

app = Framework(urls)