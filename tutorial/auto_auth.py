from django.contrib.auth.models import User

class Middleware(object):
    def __init__(self, get_response):
        print('1')
        self.get_response = get_response

    def __call__(self, request):
        print('2')
        request.user = User.objects.filter()[0]
        return self.get_response(request)

    def process_request(self, request):
        print('3')
        request.user = User.objects.filter()[0]
