from framework.wsgi import Framework
from framework.view import (HomeView, AboutView, CategoriesView,
                            CategoryEdit, CourseEdit, CourseView)
from framework.url import Url

# noinspection PyTypeChecker
urls = [
    Url('/', HomeView),
    Url('/about', AboutView),
    Url('/categories', CategoriesView),
    Url('/category_edit', CategoryEdit),
    Url('/course', CourseView),
    Url('/course_edit', CourseEdit),
]

app = Framework(urls)