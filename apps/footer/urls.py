from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path


from .views import (
	condiciones,
    privacidad,
    derechosdeautor,
    sobre,
    blog_de_ayuda

	)



urlpatterns = [
    re_path(r'^terminosycondiciones/$', condiciones),
    re_path(r'^politicadeprivacidad/$', privacidad),
    re_path(r'^derechosdeautor/$', derechosdeautor),
    re_path(r'^sobre/$', sobre),
    re_path(r'^blog/$', blog_de_ayuda),













    

    #url(r'^posts/$', "<appname>.views.<function_name>"),
]