from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from .models import Compartir
from .forms import ShareForm
from apps.peliculas.models import Peliculas
from apps.series.models import Series, Capitulos
from apps.usuarios.models import Usuario

def compartiR(request, to, toslug):
	if not request.user.is_active:
		raise Http404
	pelicula = Peliculas.objects.filter(id=to, slug=toslug)
	serie = Series.objects.filter(id=to, slug=toslug)
	capitulo = Capitulos.objects.filter(id=to, slug=toslug)
	if pelicula:
		pelicula = Peliculas.objects.filter(id=to, slug=toslug)[0]
	if serie:
		serie = Series.objects.filter(id=to, slug=toslug)[0]
	if capitulo:
		capitulo = Capitulos.objects.filter(id=to, slug=toslug)[0]





	if request.method == "POST":
		form = ShareForm(request.POST or None, request.FILES or None)
		notta = request.POST['nota']
		amigos_to = request.POST['oculto']
		amigo_to = amigos_to.split(",")
		ide = Usuario.objects.filter(username__in=amigo_to)
		contar = Usuario.objects.filter(username__in=amigo_to).count()
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_who_share = request.user
			if pelicula:
				instance.movie_to_share = pelicula
			if serie:
				instance.serie_to_share = serie
			if capitulo:
				instance.capitulo_to_share = capitulo
			instance.nota = notta
			instance.event = "Share"
			if pelicula:
				if contar > 1:
					instance.mensaje = request.user.username + " Ha compartido " + pelicula.titulo + " contigo y con " +  str(contar - 1) + " amigos más" 
				if contar == 1:
					instance.mensaje = request.user.username + " Ha compartido " + pelicula.titulo 
			elif serie:
				if contar > 1:
					instance.mensaje = request.user.username + " Ha compartido " + serie.titulo + " contigo y con " +  str(contar - 1) + " amigos más" 
				if contar == 1:
					instance.mensaje = request.user.username + " Ha compartido " + serie.titulo
			elif capitulo:
				if contar > 1:
					instance.mensaje = request.user.username + " Ha compartido " + capitulo.nombre + " contigo y con " +  str(contar - 1) + " amigos más" 
				if contar == 1:
					instance.mensaje = request.user.username + " Ha compartido " + capitulo.nombre + " en " + capitulo.temporadaa.serie.titulo

			instance.save()
			amigos_share = []
			for i in ide:
				amigos_share.append(i.id)
			instance.users_to_share.add(*amigos_share)
		
			return HttpResponseRedirect('/user_ver_amigos/' + request.user.username + "/sada")
		return HttpResponseRedirect('/user_ver_amigos/' + request.user.username + "/")
# Create your views here.

