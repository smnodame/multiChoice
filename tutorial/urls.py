import os

from django.conf.urls import url, include
from django.contrib import admin

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
    url(r'^url/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^quickstart/', include('quickstart.urls')),

]


