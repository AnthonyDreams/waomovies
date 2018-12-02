from django.conf.urls import url, include
from django.urls import path, re_path
from apps.notificaciones.views import compartiR



urlpatterns = [
  
    url(r'^compartir/(?P<to>\d+)/(?P<toslug>[\w-]+)/$', compartiR, name="compartir"),





]
