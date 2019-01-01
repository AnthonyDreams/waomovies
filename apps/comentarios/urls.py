from django.conf.urls import url, include
from django.contrib import admin

from .views import (
	post_create,
	post_update,
	post_delete,
    post_create_articulo,
    post_update_articulo,
    post_delete_articulo,
    post_create_serie,
    post_update_serie,
    post_delete_serie,
    responder,
    like,
    unlike,
    dislike,
    outdislike,
    responder_update,
    delete_res,
    responder_serie,
    like_serie,
    unlike_serie,
    dislike_serie,
    outdislike_serie,
    responder_update_serie,
    delete_res_serie,
    ComentViewSet,
    indexa,
    reportes,
    reportes_res,
    post_create_capitulos
	)


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'coment', ComentViewSet)


urlpatterns = [
    url(r'^comentar/(?P<id>\d+)/$', post_create),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    url(r'^comentar_articulo/(?P<id>\d+)/$', post_create_articulo),
    url(r'^(?P<slug>[\w-]+)/edit_articulo/$', post_update_articulo, name='update_articulo'),
    url(r'^(?P<slug>[\w-]+)/delete_articulo/$', post_delete_articulo),
    url(r'^comentar_serie/(?P<id>\d+)/$', post_create_serie),
    url(r'^(?P<slug>[\w-]+)/edit_serie/$', post_update_serie, name='update_serie'),
    url(r'^(?P<slug>[\w-]+)/delete_serie/$', post_delete_serie),
    url(r'^responder/(?P<slug>\d+)/$', responder, name='responder'),
    url(r'^like/(?P<id>\d+)/$', like),
    url(r'^outlike/(?P<id>\d+)/$', unlike),
     url(r'^dislike/(?P<id>\d+)/$', dislike),
    url(r'^outdislike/(?P<id>\d+)/$', outdislike),
    url(r'^responder_update/(?P<id>\d+)/$', responder_update),
    url(r'^delete_res/(?P<id>\d+)/$', delete_res),
    url(r'^reportando/(?P<id>\d+)/$', reportes),
    url(r'^reportando_res/(?P<id>\d+)/$', reportes_res),
    url(r'^comentar_capitulo/(?P<id>\d+)/$', post_create_capitulos),







url(r'^$', indexa),
url(r'^api/', include(router.urls)),





    url(r'^responder_serie/(?P<slug>\d+)/$', responder_serie, name='responder'),
    url(r'^like_serie/(?P<id>\d+)/$', like_serie),
    url(r'^outlike_serie/(?P<id>\d+)/$', unlike_serie),
     url(r'^dislike_serie/(?P<id>\d+)/$', dislike_serie),
    url(r'^outdislike_serie/(?P<id>\d+)/$', outdislike_serie),
    url(r'^responder_update_serie/(?P<id>\d+)/$', responder_update_serie),
    url(r'^delete_res_serie/(?P<id>\d+)/$', delete_res_serie),






    

    #url(r'^posts/$', "<appname>.views.<function_name>"),
]