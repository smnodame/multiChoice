from django.contrib.auth.models import User, Group
from django.conf import settings

from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_point


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class PointCalculation(APIView):
#     def post(self, request, format=None):
#         uploaded_file = request.FILES['file']
#         filename = '{filename}'.format(**request.data)
#         path_fmt = '{}/{}'
#         with open(path_fmt.format(settings.MEDIA_ROOT, filename), 'wb+') as file:
#             for chunk in uploaded_file.chunks():
#                 file.write(chunk)
#         point = calculate_point(filename)
#         return Response(status=204, data={
#             'point': point
#         })


def handle_uploaded_file(user_slug, example_slug, f):
    with open('media/{}_{}.jpg'.format(user_slug, example_slug), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@api_view(['POST', ])
@csrf_exempt
def upload_photo(request):
    user_slug = str(request.POST['example_slug'])
    example_slug = str(request.POST['user_slug'])
    handle_uploaded_file(user_slug, example_slug, request.FILES['file'])
    filename = '{}_{}.jpg'.format(user_slug, example_slug)
    point = calculate_point('test_12.png')
    return Response(status=200, data={
        'point': point
    })
