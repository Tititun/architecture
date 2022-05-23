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
        return Response('200', 'get request')

    def post(self, request):
        return Response('201', 'post request')


class AskView(View):

    def get(self, request):
        template = os.path.join('..', 'templates', 'ask_form.html')
        with open(template) as f:
            return Template(f.read())

    def post(self, request):
        return str(request.environ)
