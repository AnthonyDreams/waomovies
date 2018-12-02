from django.conf.urls import url, include
from django.urls import path, re_path
from .views import (login_page, register_page, login, 
	auths_view,
	 succes, salir, user_profile, user_detail, 
	 change_password, profile_edit, user_delete, user_ver_mas_tarde,
      cambiar, user_ver_favoritos, user_ver_series_favoritos, user_detail_edit,
      username_detail_edit,activate_user_view, change_email,actividadfeed, favoritos_first,codetofriend,user_ver_amigos, agregaramigos, removeamigos, notificacionesfeed)



urlpatterns = [
	re_path(r'change_password/(?P<id>\d+)/$', change_password, name='change_password'),
    path(r'register/', register_page, name='register_page'),
    path(r'login2/', login, name='login'),
    path(r'auth/', auths_view, name='auth'),
    path(r'logout/', salir),
    path(r'cambiar/', cambiar),
    path(r'profile/', user_profile),
	re_path(r'^usuario/(?P<id>\w+)/$', user_detail, name='user_detail'),
    re_path(r'^edit/(?P<id>\d+)/$', profile_edit, name='profile_edit'),
    re_path(r'^user_delete/(?P<id>\d+)/$', user_delete, name='user_delete'),
    re_path(r'^ver_más_tarde/(?P<id>\w+)/$', user_ver_mas_tarde, name='user_ver_mas_tarde'),
    re_path(r'^user_ver_favoritos/(?P<id>\w+)/$', user_ver_favoritos, name='user_ver_favoritos'),
    re_path(r'^user_ver_amigos/(?P<id>\w+)/$', user_ver_amigos, name='user_ver_amigos'),
    re_path(r'^user_edit/(?P<id>\d+)/$', user_detail_edit, name='edit_edit'),
    re_path(r'^username_edit/(?P<username>\w+)/(?P<id>\w+)/$', username_detail_edit, name='user_edit_edit'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
   # path(r'change_email_for_validate/', change_email_for_validate, name='change_email_for_validate'),
    re_path(r'change_email/$', change_email, name='change_email'),
    
    re_path(r'^user_ver_series_favoritos/(?P<id>\w+)/$', user_ver_series_favoritos, name='user_ver_series_favoritos'),
    re_path(r'favoritos/$', favoritos_first, name='favoritos_first'),
    re_path(r'^codegenerator/$', codetofriend, name='codetofriend'),
    re_path(r'^agregaramigos/(?P<id>\w+)/$', agregaramigos, name='agregaramigos'),
    re_path(r'^removeamigos/(?P<code>\w+)/$', removeamigos, name='removeamigos'),
    re_path(r'^notificacionesfeed/(?P<id>\w+)/$', notificacionesfeed, name='notificacionesfeed'),
    re_path(r'^actividadfeed/(?P<id>\w+)/$', actividadfeed, name='actividadfeed'),







    




]
