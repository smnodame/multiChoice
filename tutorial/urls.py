# -*- coding: utf-8 -*-
import os

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from quickstart import views as qs_views
from tutorial import views as tt_views

router = routers.DefaultRouter()
router.register(r'users', qs_views.UserViewSet)
router.register(r'groups', qs_views.GroupViewSet)


# Wire up our API using automatAic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', tt_views.index, name='index'),
    url(r'^qrcode', tt_views.qrcode, name='qrcode'),
    url(r'^form-pdf', tt_views.form_pdf, name='form_pdf'),
    url(r'^send-pdf', tt_views.send_pdf, name='send_pdf'),

    url(r'^url/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^quickstart/', include('quickstart.urls')),
    url(r'^forms', tt_views.get_forms, name='get_forms'),
    url(r'^question/create', tt_views.create_question, name='create_question'),
    url(r'^question/update', tt_views.update_question, name='update_question'),
    url(r'^question/delete', tt_views.delete_question, name='delete_question'),
    url(r'^question/', tt_views.get_question, name='get_question'),
    url(r'^student/', tt_views.get_student, name='get_student'),

    url(r'^point_student', tt_views.get_point_form_student, name='get_point_form_student'),
    url(r'^point', tt_views.get_point, name='get_point'),
    url(r'^login', tt_views.login, name='login'),
    url(r'^auth', tt_views.auth, name='auth'),
] + static(settings.STATIC_URL) + static(settings.MEDIA_URL)
