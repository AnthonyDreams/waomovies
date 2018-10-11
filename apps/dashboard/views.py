from django.shortcuts import render
from apps.peliculas.models import Peliculas, Hitcount
from apps.usuarios.models import Usuario
from apps.series.models import Series
# Create your views here.

from django.shortcuts import (render, get_list_or_404, 
							redirect, get_object_or_404)
from itertools import chain
from apps.peliculas.models import *
import operator
import time
from django.http import *
from django.contrib import messages
from django.db.models import Q
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from django.http import JsonResponse
from datetime import date, timedelta

def dashboard_users_data(request):

	if request.user.is_admin:

		usuarios_totales = Usuario.objects.all().count()
		usuarios_by_year = False
		usuarios_by_month = False
		usuarios_by_week = False
		usuarios_by_day = False
		usuario = True

		context = {
		'usuarios_totales':usuarios_totales,
		'usuario':usuario,
		}
	else: 
		return HttpResponseRedirect('/waomovies/inicio/')


	return render(request, 'dashboard/usuariosdata.html', context)

def dashboard_movies_data(request):

	if request.user.is_admin:

		usuarios_totales = Usuario.objects.all().count()
		usuarios_by_year = False
		usuarios_by_month = False
		usuarios_by_week = False
		usuarios_by_day = False
		movies = True

		context = {
		'usuarios_totales':usuarios_totales,
		'movies':movies,
		}
	else: 
		return HttpResponseRedirect('/waomovies/inicio/')


	return render(request, 'dashboard/usuariosdata.html', context)

def get_data_for_movie_dashboard(self, *args, **kwargs):
	total_movies = Peliculas.objects.all()
	movie_with_report = ""
	for movie in total_movies:
		if movie.reportes >= 3:
			movie_with_report.append(movie)


def get_data_for_dashboard(self, *args, **kwargs):
	last_month = datetime.today() - timedelta(days=30)

	user_by_week = Usuario.objects.filter(create_date__range = (date.today() - timedelta(days=7), date.today() + timedelta(days=1))).count()
	danterior7 = Usuario.objects.filter(create_date__date = date.today() - timedelta(days=7)).count()
	danterior6 =Usuario.objects.filter(create_date__date = date.today() - timedelta(days=6)).count()
	danterior5 = Usuario.objects.filter(create_date__date = date.today() - timedelta(days=5)).count()
	danterior4 = Usuario.objects.filter(create_date__date = date.today() - timedelta(days=4)).count()
	danterior3= Usuario.objects.filter(create_date__date = date.today() - timedelta(days=3)).count()
	danterior2 = Usuario.objects.filter(create_date__date = date.today() - timedelta(days=2)).count()
	danterior1 = Usuario.objects.filter(create_date__date = date.today() - timedelta(days=1)).count()
	hoy = Usuario.objects.filter(create_date__date = date.today()).count()
	usersadmins = Usuario.objects.filter(admin= True).count()
	usersactive = Usuario.objects.filter(active= True).count()
	usersstaffs = Usuario.objects.filter(staff= True).count()
	noactivados = Usuario.objects.filter(active= False).count()

	datauserbyday = [hoy,danterior1,danterior2,danterior3,danterior4,danterior5,danterior6,danterior7]
	hoy = date.today()
	user_by_month = Usuario.objects.filter(create_date__gte= last_month).count()
	labels= ["hoy", "haceundia", "hacendosdia", "hacentresdia", "hacecuatrodia", "hacecincodia", "haceseisdia", "hacesietedias"]
	labelstotal= ["Admins", "Staffs", "Activados", "NoActivados"]
	usertotal = [usersadmins, usersstaffs, usersactive, noactivados]
	
	
	data = {
		'labels': labels,
		'user_by_week': user_by_week,
		'hoy': hoy,
		'datauserbyday': datauserbyday,
		'labelstotal': labelstotal,
		'usertotal': usertotal,








		'user_by_month': False
	}

	return JsonResponse(data)