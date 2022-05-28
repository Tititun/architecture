from .response import Response
from jinja2 import Template
import os


class View:
    def get(self, request):
        return

    def post(self, request):
        return


class HomeView(View):
    def get(self, request):
        return Response('200 OK', 'get request')

    def post(self, request):
        return Response('201 OK', 'post request')


class AskView(View):

    def get(self, request):
        template = os.path.join(os.path.dirname(__file__),
                                'templates/ask_form.html')
        with open(template) as f:
            return Response('200 OK', Template(f.read()).render())

    def post(self, request):
        content_length_data = request.environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = request.environ['wsgi.input'].read(content_length)\
            if content_length > 0 else b''
        with open('user_data', 'wb') as f:
            f.write(data)
        return Response('201 OK', 'Form submitted')
