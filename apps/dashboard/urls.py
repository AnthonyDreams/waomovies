from django.conf.urls import url, include
from django.urls import path, re_path
from apps.dashboard.views import dashboard_users_data, get_data_for_dashboard, dashboard_movies_data
 


urlpatterns = [
	path('dashboard/usuarios/', dashboard_users_data, name='datos_de_usuarios'),
	path('dashboard/datojson/', get_data_for_dashboard, name='get_data_for_dashboard'),
	path('dashboard/movies/', dashboard_movies_data, name='datos_de_usuarios'),



]