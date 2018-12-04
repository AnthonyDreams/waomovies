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
from apps.usuarios.models import Usuario, Profile

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





	if request.is_ajax():
		form = ShareForm(request.POST or None, request.FILES or None)
		notta = request.POST.get('nota')
		amigos_to = request.POST.get('users_to_share')
		amigos_no = request.POST.get('oculto')
		amigo_no = amigos_no.split(",")
		amigo_to = amigos_to.split(",")
		to_share = []
		for am in amigo_to:
			if am in amigo_no:
				continue
			else:
				to_share.append(am)

		if "todos" in to_share:
			listica = Profile.objects.filter(user=request.user.id)
			for i in listica:
				amis = i.AmiGos.all()
			users_amigos = Profile.objects.filter(user__in=amis)
			ide  = Usuario.objects.filter(profile__in=users_amigos)
			contar = Usuario.objects.filter(profile__in=users_amigos).count()
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
				data = {
				'message': "Se ha compartido con exito"
			}
				return JsonResponse(data)
			
		else:
			ide = Usuario.objects.filter(username__in=to_share)
			contar = Usuario.objects.filter(username__in=to_share).count()
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
		
				data = {
				'message': "Se ha compartido con exito"
			}
				return JsonResponse(data)
# Create your views here.

