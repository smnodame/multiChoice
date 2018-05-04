# This Python file uses the following encoding: utf-8
from django.contrib.auth.models import User, Group
from django.conf import settings
import json
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_point
from tutorial.models import FormChoice, Student, Point
import base64


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

@api_view(['POST', ])
@csrf_exempt
def upload_photo(request):
    if request.data.get('platform') == 'android':
        png_recovered = base64.decodestring(request.data['base64'])

        user_slug = str(request.data['user_slug'])
        example_slug = str(request.data['example_slug'])
        filename = '{}_{}.jpg'.format(user_slug, example_slug)
        name = '{}_{}'.format(user_slug, example_slug)

        with open('media/{}'.format(filename), 'wb+') as destination:
            destination.write(png_recovered)


            form = FormChoice.objects.get(slug=example_slug)
            point = calculate_point(filename, name, json.loads(form.answers))
            s = Student.objects.get(slug=user_slug)
            f = FormChoice.objects.get(slug=example_slug)

            exist = Point.objects.filter(slug=name)
            if exist:
                exist = exist[0]
                exist.point=str(point)
                exist.save()
            else:
                Point.objects.create(slug=name, student=s, form=f, point=str(point))
            destination.close()
            return Response(status=200, data={
                'point': point
            })

    user_slug = str(request.POST['user_slug'])
    example_slug = str(request.POST['example_slug'])
    form = FormChoice.objects.get(slug=example_slug)
    filename = '{}_{}.jpg'.format(user_slug, example_slug)
    name = '{}_{}'.format(user_slug, example_slug)
    with open('media/{}'.format(filename), 'wb+') as destination:
        for chunk in request.FILES['file'].chunks():
            destination.write(chunk)
        point = calculate_point(filename, name, json.loads(form.answers))
        s = Student.objects.get(slug=user_slug)
        f = FormChoice.objects.get(slug=example_slug)

        exist = Point.objects.filter(slug=name)
        if exist:
            exist = exist[0]
            exist.point=str(point)
            exist.save()
        else:
            Point.objects.create(slug=name, student=s, form=f, point=str(point))
        return Response(status=200, data={
            'point': point
        })
