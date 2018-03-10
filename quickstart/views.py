from django.contrib.auth.models import User, Group
from django.conf import settings

from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_point
from tutorial.models import FormChoice

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


# def handle_uploaded_file(user_slug, example_slug, f):


@api_view(['POST', ])
@csrf_exempt
def upload_photo(request):
    user_slug = str(request.POST['user_slug'])
    example_slug = str(request.POST['example_slug'])

    form = FormChoice.objects.get(slug=example_slug)
    import ipdb;ipdb.set_trace()
    filename = 'test_12.png'.format(user_slug, example_slug)
    name = 'test_12'.format(user_slug, example_slug)
    # with open('media/{}'.format(filename), 'wb+') as destination:
    #     for chunk in request.FILES['file'].chunks():
    #         destination.write(chunk)
    point = calculate_point(filename, name)
    return Response(status=200, data={
        'point': point
    })
