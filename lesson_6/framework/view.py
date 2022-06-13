import os
import datetime
from .response import Response
from .request import Request, get_request_redirect
from .entities import Category, Course, Student
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from urllib.parse import unquote

TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')

URLS = []


def register(url):
    def decorator(f):
        URLS.append((url, f))
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator


def debug(f):
    def wrapper(*args, **kwargs):
        print(f'[{datetime.datetime.now()}] function {f.__qualname__} called.')
        return f(*args, **kwargs)
    return wrapper



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
        for row in unquote(data.decode()).split('&'):
            k, v = row.split('=')
            res[k] = v
        return res

    def get(self, request):
        return

    def post(self, request):
        return


@register('/')
class HomeView(View):
    @debug
    def get(self, request):
        template = self.env.get_template('base.html')
        context = {'request_type': 'GET'}
        context.update(request.cookies)
        return Response('200 OK',
                        template.render(context), {})

    def post(self, request):
        template = self.env.get_template('base.html')
        context = {'request_type': 'POST'}
        context.update(request.cookies)
        return Response('200 OK', template.render(context),
                        {})


@register('/about')
class AboutView(View):
    def get(self, request):
        template = self.env.get_template('about.html')
        return Response('200 OK', template.render(request.cookies), {})

@register('/categories')
class CategoriesView(View):
    template = View.env.get_template('categories.html')

    def get(self, request):
        template = self.env.get_template('categories.html')
        categories = Category.list_all()
        courses = Course.list_all()
        context = {'categories': categories, 'courses': courses}
        context.update(request.cookies)
        return Response('200 OK', template.render(context), {})

    def post(self, request):
        data = self.process_post(request)
        context = request.cookies
        for k, v in data.items():
            if k == 'delete':
                Category(int(v)).delete()
            elif k == 'edit':
                template = View.env.get_template('category_form.html')
                context.update( {'category': Category(int(v)).__dict__,
                                 'success_message': ''})
                return Response('200 OK', template.render(context), {})
        categories = Category.list_all()
        context.update({'categories': categories})
        return Response('200 OK', self.template.render(context), {})


@register('/category_edit')
class CategoryEdit(View):
    def get(self, request: Request):
        params = request.get_query_params()
        action = params['action']
        id_ = params['id']
        if action == 'edit':
            template = View.env.get_template('category_form.html')
            context = {'category': Category(int(id_)).__dict__,
                 'success_message': ''}
            context.update(request.cookies)
            return Response('200 OK', template.render(context), {})

    def post(self, request):
        template = View.env.get_template('category_form.html')
        query_params = self.process_post(request)
        name = query_params.get('category_name')
        id_ = int(query_params.get('category_id'))
        submit = query_params['submit_type']
        context = request.cookies
        if submit == 'edit':
            success = Category(id_).update(name)
            if success:
                context.update({'category': Category(name).__dict__,
                                'success_message':
                                'Name has been changed successfully!'})
                return Response('200 OK', template.render(context), {})

        elif submit == 'delete':
            Category(id_).delete()
            return CategoriesView().get(request)

        return Response('400 ERROR', 'Something went wrong', {})

@register('/course')
class CourseView(View):
    def get(self, request: Request):
        params = request.query_params
        id_ = params['id']
        course = Course.get_course(id_)
        template = View.env.get_template('course.html')
        context = request.cookies
        context.update({'course': course.__dict__})
        return Response('200 OK',
                        template.render(context), {})

@register('/course_edit')
class CourseEdit(View):
    def get(self, request: Request):
        params = request.query_params
        id_ = params['id']
        template = View.env.get_template('course_form.html')
        context = request.cookies
        context.update({'course': Course(int(id_)).__dict__,
                             'success_message': ''})
        return Response('200 OK', template.render(context), {})
    def post(self, request):
        query_params = self.process_post(request)
        name = query_params.get('course_name')
        id_ = int(query_params.get('course_id'))
        address = query_params.get('course_address')
        is_online = query_params.get('is_online')
        category_id = query_params.get('category_id')
        to_update = {
            'address': address,
            'is_online': 1 if is_online else 0,
            'name': name,
            'id': id_,
            'category_id': category_id
        }
        submit = query_params['submit_type']
        if submit == 'edit':
            Course(id_).update(**to_update)
            return get_request_redirect(CourseView, request,
                                        'get', {'id': id_})
        elif submit == 'copy':
            to_update['name'] += ' [COPY]'
            del to_update['id']
            new_id = Course(**to_update).create()
            return get_request_redirect(CourseView, request,
                                        'get', {'id': new_id})

        elif submit == 'delete':
            Course(id_).delete()
            return CategoriesView().get(request)

        return Response('400 ERROR', 'Something went wrong', {})


@register('/login')
class LoginView(View):
    def get(self, request: Request):
        if request.cookies.get('user_id'):
            template = View.env.get_template('base.html')
            return Response('200 OK', template.render({}),
                            {'Set-Cookie': 'user_id='})
        template = View.env.get_template('login_form.html')
        context = request.cookies
        return Response('200 OK', template.render(context), {})

    def post(self, request: Request):
        query_params = self.process_post(request)
        submit = query_params['submit_type']
        if submit == 'register':
            name = query_params['register_name']
            student = Student(name).create()
            template = self.env.get_template('base.html')
            return Response('200 OK', template.render({}),
                            {'Set-Cookie': f'user_id={student.id}'})
        elif submit == 'Log+in':
            name = query_params['login_name']
            student = Student.fetch_user_by_name(name)
            if not student:
                return Response('404, NOT_FOUND', 'User with this'
                                                  ' name doesn\'t exist', {})
            else:
                template = self.env.get_template('base.html')
                return Response('200 OK', template.render({}),
                                {'Set-Cookie': f'user_id={student.id}'})


@register('/list_students')
class ListStudents(View):
    def get(self, request: Request):
        context = request.cookies
        template = View.env.get_template('list_students.html')
        context.update({'students': Student.list_all()})
        return Response('200 OK', template.render(context), {})
