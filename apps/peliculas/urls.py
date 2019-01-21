from django.conf.urls import url, include
from django.urls import path, re_path
from apps.peliculas.views import (peliculas_list, peliculasO, Generos, 
	inicio, search, Orden, votaciono, reportar, VotacionFormView, list_moviejson, pelis,
     añadirfavorito, eliminar_añadirfavorito,
    answer_me, myview, peliculas_listodo,test,
    FavoritoFormView, EliminarFavoritoFormView, filtrar, cookies,
    GeneroF, GeneroF_eliminar,pelis_user_nove,añadiste,
    seguirviendo,seguirviendo_series,actualizar_tops, search_result_ajax,cambiar_votaciono,Read,CompRead,gettingembed,testing, search_result, genero_list, Notifi, Friendsitos, CompAPI)



urlpatterns = [

    path('actualizar/', actualizar_tops, name='actualizar_tops'),
    path('inicio/', inicio, name='inicio'),
    path('test/', test, name='test'),
    re_path(r'^generoz/(?P<genre>[\w-]+)/$', GeneroF, name='GeneroF'),
    re_path(r'^generoz_eliminar/(?P<genre>[\w-]+)/$', GeneroF_eliminar, name='GeneroF_eliminar'),



	re_path(r'^peliculas/(?P<slug>[\w-]+)/$', peliculasO, name='peliculasO'),
	path(r'geneross/', Generos, name='Generos'),
    re_path(r'ver%todo/(?P<filtro>\w+)/$', peliculas_list, name='peliculas_list'),
    re_path(r'peliculas_por_genero/(?P<generos>\w+)/(?P<filtro>\w+)/$', genero_list, name='genero_list'),
    re_path(r'get_embed/(?P<id>\d+)/$', gettingembed, name='gettingembed'),

    re_path(r'ver%todo/$', peliculas_listodo, name='peliculas_listodo'),

    path(r'search/', search, name='search'),
    path(r'search_ajax/', search_result_ajax, name='search_ajax'),

    re_path(r'^search/(?:search-(?P<src>.+)/)?$', search_result, name='search_result'),
    path(r'filter/', filtrar, name='filtrar'),

	re_path(r'^peliculas_por_genero/(?P<generos>\w+)/$', Orden, name='Orden'),
    re_path(r'votaciono/(?P<id>\d+)/as/$', votaciono, name='votaciono'),
    re_path(r'cambiar_votaciono/(?P<id>\d+)/asm/$', cambiar_votaciono, name='cambiar_votaciono'),

    re_path(r'reportar/(?P<id>\d+)/$', reportar, name='reportar'),
    re_path(r'^join/', VotacionFormView.as_view()),
#    re_path(r'^favorito/', FavoritoFormView.as_view()),
    re_path(r'^favorito/(?P<id>\d+)/$', FavoritoFormView, name='favorito'),
    re_path(r'^eliminar_favorito/(?P<id>\d+)/$', EliminarFavoritoFormView, name='eliminar_favorito'),


    path('list_moviejson/', list_moviejson, name='list_moviejson'),
    path('testing/', testing, name='testing'),

    path('pelis/', pelis.as_view(), name='pelis'),
    path('noti/', Notifi.as_view(), name='noti'),
    path('compartir/', CompAPI.as_view(), name='compartir'),
    path('read/', Read.as_view(), name='read'),
    path('compread/', CompRead.as_view(), name='compread'),




    path('friendsitos/', Friendsitos.as_view(), name='friendsitos'),

    path('pelis_user_novel/', pelis_user_nove.as_view(), name='pelis_user_nove'),
    path('añadiste/', añadiste.as_view(), name='añadiste'),
    path('seguirviendo/', seguirviendo.as_view(), name='seguirviendo'),
    path('seguirviendo_series/', seguirviendo_series.as_view(), name='seguirviendo_series'),



    re_path(r'^añadirfavorito/(?P<id>\d+)/$', añadirfavorito, name='añadirfavorito'),
    re_path(r'^eliminar_añadirfavorito/(?P<id>\d+)/$', eliminar_añadirfavorito, name='eliminar_añadirfavorito'),
    url(r'^ajax/get_response/$', answer_me.as_view(), name='get_response'),
    url(r'^ajax/myview/$', myview, name='myview'),
    url(r'^cookies/$', cookies, name='cookies')   










]
