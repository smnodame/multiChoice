from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import views

urlpatterns = [
    url(r'^upload-photo/$', views.NewPhotoUploadView.as_view(), name='upload-photo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)