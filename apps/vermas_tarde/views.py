from apps.series.models import *
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.http import *
from django.contrib import messages
from django.db.models import Q
import re
from unicodedata import normalize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from apps.comentarios.forms import PostForm
from apps.comentarios.models import *
from django.db.models import Sum
from .forms import *
from urllib.parse import quote_plus
from apps.usuarios.models import Usuario
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from apps.peliculas.models import Cast, Personajes
from .models import *
from django.core import serializers
# Create your views here.



def VerFormView(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Peliculas, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.favoritos.add(juan)
			instance.pelicula_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)

def EliminarVerFormView(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Vermastarde, peliculas_id=id)
	juan = request.user.id
	form = Fechas(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.peliculas_id.remove(id)
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)


# este es el formulario de ver mas tarde, simple
def vermastarde(request, id):
	if not request.user.is_active:
		raise Http404
	juan = request.user.id
	ver = Vermastarde.objects.all()
	filtrar = Vermastarde.objects.filter(usuario_id=request.user.id).filter(peliculas_id=id)
	if filtrar:
		data = {
			'message': "Ya está añadida."
		}
		return JsonResponse(data)
	form = Fechas(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.usuario_id= juan
			instance.peliculas_id = id
			instance.save()
				# message success	
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)
# este es el formulario de eliminar...., simple
def eliminar_vermastarde(request, id):
	if not request.user.is_active:
		raise Http404
	if request.is_ajax():
		instance = get_object_or_404(Vermastarde, peliculas_id=id, usuario_id=request.user.id)
		instance.delete()
		data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)

def vermastarde_series(request, id):
	if not request.user.is_active:
		raise Http404
	juan = request.user.id
	ver = Vermastarde.objects.all()
	filtrar = Vermastarde.objects.filter(usuario_id=request.user.id).filter(series_id=id)
	if filtrar:
		data = {
			'message': "Ya está añadida."
		}
		return JsonResponse(data)
	form = Fechas(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.usuario_id= juan
			instance.series_id = id
			instance.save()
				# message success	
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)
# este es el formulario de eliminar...., simple
def eliminar_vermastarde_series(request, id):
	if not request.user.is_active:
		raise Http404
	if request.is_ajax():
		instance = get_object_or_404(Vermastarde, series_id=id, usuario_id=request.user.id)
		instance.delete()
		data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)