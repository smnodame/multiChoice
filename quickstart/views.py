from django.contrib.auth.models import User, Group
from django.conf import settings

from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

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


class NewPhotoUploadView(APIView):
    def post(self, request, format=None):
        uploaded_file = request.FILES['file']
        path_fmt = '{}/{survey}-{response}-{question}-{filename}'
        with open(path_fmt.format(settings.MEDIA_ROOT, **request.data), 'wb+') as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)
        return Response(status=204)
