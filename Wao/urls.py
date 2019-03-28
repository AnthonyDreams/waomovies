"""Wao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout_then_login, password_reset_done, password_reset_confirm, password_reset_complete
from apps.usuarios.views import password_reset
from django.conf.urls import handler404, handler500
from apps.footer.views import mi_error_404 
import debug_toolbar
from django.http import HttpResponse
handler404 = mi_error_404
handler500 = mi_error_404
a = ['User-agent: *\n', 'Disallow: /admin/\n', 'Disallow: /accounts/\n', 'Disallow: /auth/\n', 'Disallow: /register/\n', 'Disallow: /login2/\n', 'Disallow: /logout/\n', 'Disallow: /cambiar/\n', 'Disallow: /profile\n', 'Disallow: /usuario/\n', 'Disallow: /edit/\n', 'Disallow: /user_delete/\n', 'Disallow: /ver_más_tarde/\n', 'Disallow: /user_ver_favoritos/\n', 'Disallow: /user_ver_amigos/\n', 'Disallow: /user_edit/\n', 'Disallow: /username_edit/\n', 'Disallow: /activate/\n', 'Disallow: /change_email/\n', 'Disallow: /user_ver_series_favoritos/\n', 'Disallow: /favoritos/\n', 'Disallow: /codegenerator/\n', 'Disallow: /agregaramigos/\n', 'Disallow: /removeamigos/\n', 'Disallow: /notificacionesfeed/\n', 'Disallow: /actividadfeed/\n', 'Disallow: /search/\n', 'Disallow: /get_embed/\n', 'Disallow: /search_ajax/\n', 'Disallow: /filter/\n', 'Disallow: /votaciono/\n', 'Disallow: /reportar/\n', 'Disallow: /pelis/\n', 'Disallow: /noti/\n', 'Disallow: /get/\n', 'Disallow: /compread/\n', 'Disallow: /añadiste/\n', 'Disallow: /ajax/\n', 'Disallow: /cookies/\n', 'Disallow: /seguirviendo/\n', 'Disallow: /seguirviendo_series/\n', 'Disallow: /join/\n', 'Disallow: /favorito/\n', 'Disallow: /testing/\n', 'Disallow: /read/\n', 'Disallow: /cast/\n', 'Disallow: /friendsitos/\n', 'Disallow: /compartir/\n', 'Disallow: /actualizar/\n', 'Disallow: /blog_search/redirect/\n', 'Disallow: /blog_search/search/\n', 'Disallow: /reating_articulos/\n', 'Disallow: /cambiar_votaciono_articulo/\n', 'Disallow: /terminosycondiciones/\n', 'Disallow: /derechosdeautor/\n', 'Disallow: /politicadeprivacidad/\n', 'Disallow: /dashboard/\n', 'Disallow: /thanks/\n', 'Disallow: /comentar/\n', 'Disallow: /comentar_articulo/\n', 'Disallow: /comentar_serie/\n', 'Disallow: /responder/\n', 'Disallow: /like/\n', 'Disallow: /dislike/\n', 'Disallow: /outdislike/\n', 'Disallow: /responder_update/\n', 'Disallow: /delete_res/\n', 'Disallow: /reportando_res/\n', 'Disallow: /reportando/\n', 'Disallow: /comentar_capitulo/\n', 'Disallow: /api/\n', 'Disallow: /responder_serie/\n', 'Disallow: /like_serie/\n', 'Disallow: /outlike_serie/\n', 'Disallow: /dislike_serie/\n', 'Disallow: /outdislike_serie/\n', 'Disallow: /responder_update_serie/\n', 'Disallow: /delete_res_serie/\n', 'Disallow: /get_embed_serie/\n', 'Disallow: /votacion_serie/\n', 'Disallow: /añadirfavorito_series/\n', 'Disallow: /eliminar_añadirfavorito_series/\n', 'Disallow: /reportar_serie/\n', 'Disallow: /series_list/\n', 'Disallow: /to/\n', 'Disallow: /buscar_series/\n', 'Disallow: /series/search/\n', 'Disallow: /filtrar_series/\n', 'Disallow: /temporadaon/\n', 'Disallow: /search_ajax_serie/\n', 'Disallow: /capitulo/like_capi/\n', 'Disallow: /capitulo/outlike_capi/\n', 'Disallow: /dislike_capi/\n', 'Disallow: /outdislike_capi/\n', 'Disallow: /reportar_capitulo/\n', 'Disallow: /cambiar_votacion_serie/\n', 'Disallow: /admin/\n']


urlpatterns = [
    url(r"^__debug__", include(debug_toolbar.urls)),
    url(r'^', include('apps.peliculas.urls')),
    url(r'^', include('apps.notificaciones.urls')),
    url(r'^', include('apps.usuarios.urls')),
    url(r'^', include('apps.comentarios.urls')),
    url(r'^', include('apps.vermas_tarde.urls')),
    url(r'^', include('apps.footer.urls')),
    path('send_email_contact/', include('apps.contacto.urls')),
    url(r'^', include('apps.dashboard.urls')),
    url(r'^', include('apps.news.urls')),

    url(r'^robots.txt', lambda x: HttpResponse(a, content_type="text/plain"), name="robots_file"),
    url(r'^reset/password_reset', password_reset, 
        {'template_name':'password_reset_form.html',
        'email_template_name': 'password_reset_email.html'}, 
        name='password_reset'), 
    url(r'^password_reset_done', password_reset_done, 
        {'template_name': 'password_reset_done.html'}, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, 
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),

   # url(r'^', include('apps.notificaciones.urls')),



    url(r'^', include('apps.series.urls')),


    path('admin/', admin.site.urls),
]


if settings.DEB:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DIRS)



