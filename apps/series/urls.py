from django.conf.urls import url, include
from django.urls import path, re_path
from apps.series.views import (
	series_detail, 
	votaciono,

	añadirfavorito,
	eliminar_añadirfavorito,
	reportar,
	series_list,
	temporada_detail,
	capitulos_detail,
	redirect,
	search_series,
	filtrar,
	ontemporada,
	like,
	unlike,
	outdislike,
	dislike,
	reportar_cap,
	cambiar_votaciono_serie,


	)
URL_CHARS = "[a-zA-Z_/-'·çÇñÑàèìòùÀÈÌÒÙáéíóúÁÉÍÓÚäëïöüÄËÏÖÜ]+"


urlpatterns = [
    re_path(r'^series/(?P<slug>[\w-]+)/$', series_detail, name='series_detail'),
    re_path(r'votacion_serie/(?P<id>\d+)/$', votaciono, name='votaciono'),
    re_path(r'^añadirfavorito_series/(?P<id>\d+)/$', añadirfavorito, name='añadirfavorito'),
    re_path(r'^eliminar_añadirfavorito_series/(?P<id>\d+)/$', eliminar_añadirfavorito, name='eliminar_añadirfavorito'),
    re_path(r'reportar_serie/(?P<id>\d+)/$', reportar, name='reportar'),
    re_path(r'series_list/(?P<filtro>\w+)/$', series_list, name='series_list'),
    re_path(r'^temporada/(?P<slug>\w+)/$', temporada_detail, name='temporada_detail'),
    re_path(r'^(?P<capitulo>[\w-]+)/(?P<slug>[\w-]+)/$', capitulos_detail, name='capitulos_detail'),
    re_path(r'^to/(?P<capitulo>\w+)/(?P<temporada>\w+)/$', redirect, name='capitulos_detail'),
    path(r'buscar_series/', search_series, name='search_series'),
    path(r'filtrar_series/', filtrar, name='filtrar_series'),
    re_path(r'temporadaon/(?P<id>\d+)/post/$', ontemporada, name='ontemporada'),
     re_path(r'^like_capi/(?P<id>\d+)/gustar/$', like),
    url(r'^outlike_capi/(?P<id>\d+)/outgustar/$', unlike),
     url(r'^dislike_capi/(?P<id>\d+)/disgustar/$', dislike),
    url(r'^outdislike_capi/(?P<id>\d+)/outdisgustar/$', outdislike),
    re_path(r'reportar_capitulo/(?P<id>\d+)/reportar/$', reportar_cap, name='reportar_cap'),
    re_path(r'cambiar_votaciono_serie/(?P<id>\d+)/as/$', cambiar_votaciono_serie, name='cambiar_votaciono_serie'),


	
	





	#re_path(r'^peliculas/(?P<id>\d+)/$', peliculasO, name='peliculasO'),
	#path(r'geneross/', Generos, name='Generos'),
    #path(r'ver%todo/', peliculas_list, name='peliculas_list'),
    #path(r'search/', search, name='search'),

]