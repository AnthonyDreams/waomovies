from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path


from .views import (
	NewsList, Categories,BlogDetail, SearchRedirect, BlogSearch, votaciono_art,cambiar_votaciono_articulo

	)



urlpatterns = [
    re_path(r'^blog/$', NewsList),
    re_path(r'^blog/(?P<categorie>[\w-]+)/$', Categories),
    re_path(r'^blog/(?P<categorie>[\w-]+)/(?P<slug>[\w-]+)/$', BlogDetail),
    path(r'blog_search/search/redirect/', SearchRedirect, name='search_redirect'),
    re_path(r'^blog_search/search/(?:s=(?P<searched>.+)/)?$', BlogSearch, name='blog_result'),
    re_path(r'^reating_articulos/(?P<id>\d+)/ar/$', votaciono_art, name='votaciono_art'),
    re_path(r'cambiar_votaciono_articulo/(?P<id>\d+)/arm/$', cambiar_votaciono_articulo, name='cambiar_votaciono_articulo'),














    

]