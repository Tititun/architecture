import os
from .response import Response
from .entities import Category, Course
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')


class View:
    env = Environment()
    env.loader = FileSystemLoader(TEMPLATES_FOLDER)

    @staticmethod
    def process_post(request) -> dict:
        content_length_data = request.environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = request.environ['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        res = {}
        for row in data.decode('utf-8').split('\n'):
            k, v = row.split('=')
            res[k] = v
        return res

    def get(self, request):
        return

    def post(self, request):
        return


class HomeView(View):
    def get(self, request):
        template = self.env.get_template('base.html')
        return Response('200 OK', template.render({'request_type': 'GET'}))

    def post(self, request):
        template = self.env.get_template('base.html')
        return Response('200 OK', template.render({'request_type': 'POST'}))


class AboutView(View):
    def get(self, request):
        template = self.env.get_template('about.html')
        return Response('200 OK', template.render())


class CategoriesView(View):
    template = View.env.get_template('categories.html')

    def get(self, request):
        template = self.env.get_template('categories.html')
        categories = Category.list_all()
        return Response('200 OK', template.render({'categories': categories}))

    def post(self, request):
        data = self.process_post(request)
        for k, v in data.items():
            if k == 'delete':
                Category(int(v)).delete()
            elif k == 'edit':
                template = View.env.get_template('category_form.html')
                return Response('200 OK', template.render(
                    {'category': Category(int(v)).__dict__}))
        categories = Category.list_all()
        return Response('200 OK', self.template.render(
            {'categories': categories}))


# class CategoriyEdit(View):
#     template = View.env.get_template('category_form.html')
#     def get(self, request):
#         query_params = request.get_query_params()
#         category_id = query_params.get('id')
#         if category_id:
#             return Response('200 OK', self.template.render(
#                 {'category': Category(int(category_id).__dict__)}))
#         else:
#             return Response('200 OK', 'Something went wrong')

class AskView(View):

    def get(self, request):
        # template = os.path.join(os.path.dirname(__file__),
        #                         'templates/ask_form.html')
        template = self.env.get_template('ask_form.html')
        return Response('200 OK', template.render())

    def post(self, request):
        content_length_data = request.environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = request.environ['wsgi.input'].read(content_length)\
            if content_length > 0 else b''
        with open('user_data', 'wb') as f:
            f.write(data)
        return Response('201 OK', 'Form submitted')
