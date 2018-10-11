from django.conf.urls import url, include
from django.urls import path, re_path
from apps.vermas_tarde.views import (
    vermastarde, eliminar_vermastarde,
        vermastarde_series,
    eliminar_vermastarde_series,
    VerFormView,
    EliminarVerFormView
    )



urlpatterns = [
    re_path(r'^vermastarde/(?P<id>\d+)/$', vermastarde, name='vermastarde'),
    re_path(r'^eliminar_vermastarde/(?P<id>\d+)/$', eliminar_vermastarde, name='eliminar_vermastarde'),
    re_path(r'^eliminar_vermastarde_series/(?P<id>\d+)/$', eliminar_vermastarde_series, name='eliminar_vermastarde_series'),
    re_path(r'^vermastarde_series/(?P<id>\d+)/$', vermastarde_series, name='vermastarde_series'),
    #re_path(r'^vermastarde/(?P<id>\d+)/$', VerFormView, name='vermastarde'),
    #re_path(r'^eliminar_vermastarde/(?P<id>\d+)/$', EliminarVerFormView, name='eliminar_vermastarde'),







]
