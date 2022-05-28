from .response import Response
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

TEMPLATES_FOLDER = 'templates'


class View:
    def __init__(self):
        self.env = Environment()
        self.env.loader = FileSystemLoader(TEMPLATES_FOLDER)

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
