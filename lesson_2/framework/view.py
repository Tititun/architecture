from .response import Response


class View:
    def get(self, request):
        return

    def post(self, request):
        return


class HomeView(View):
    def get(self, request):
        return Response(200, 'get request')

    def post(self, request):
        return Response(201, 'post request')
