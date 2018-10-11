from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.send_email),
    url(r'^thanks/$', views.thanks),
]