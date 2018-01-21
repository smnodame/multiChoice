from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import views

urlpatterns = [
    url(r'^upload-photo/$', views.PointCalculation.as_view(), name='point-calculation'),
]

urlpatterns = format_suffix_patterns(urlpatterns)