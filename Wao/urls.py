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
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf.urls import handler404, handler500
from apps.footer.views import mi_error_404 
 
handler404 = mi_error_404
handler500 = mi_error_404



urlpatterns = [
    path('waomovies/', include('apps.peliculas.urls')),
    path('waomovies/', include('apps.usuarios.urls')),
    path('waomovies/', include('apps.comentarios.urls')),
    path('waomovies/', include('apps.vermas_tarde.urls')),
    path('waomovies/', include('apps.footer.urls')),
    path('send_email_contact/', include('apps.contacto.urls')),
    path('waomovies/', include('apps.dashboard.urls')),


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

   # path('waomovies/', include('apps.notificaciones.urls')),



    path('waomovies/', include('apps.series.urls')),


    path('admin/', admin.site.urls),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DIRS)