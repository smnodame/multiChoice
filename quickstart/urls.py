# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import views

urlpatterns = [
    url(r'^upload-photo', views.upload_photo, name='upload_photo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
