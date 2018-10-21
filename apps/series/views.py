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
from apps.vermas_tarde.models import Vermastarde
from django.core import serializers

# Create your views here.



from datetime import datetime, date, time, timedelta


def series_detail(request, slug):

	peliculasees = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase_seriesa = []

	for i in peliculasees:
		peliculase_seriesa.append(i.series)
	sacar_id = Series.objects.get(slug=slug)
	id = sacar_id.id
	
	series = Series.objects.get(id=id)
	temporada = Temporada.objects.filter(serie_id=id).order_by('num_temporada')

	relacionar = Series.objects.all()[:10]

	comentarios_list = Post.objects.filter(series_id=id)
	comentariosc = Post.objects.filter(series_id=id).count()
	seriese = Vermastarde.objects.filter(series_id=id).filter(usuario_id=request.user.id)
	seriesf = series.favoritos.filter(id=request.user.id)
	# esto es para relacionar las Series de acuerdo a las palabras clave, director,titulo, tema, ect
	relacionarr = Series.objects.filter(Q(palabra_clave__icontains=series.palabra_clave)).order_by('-puntuacion')[:10]
	relacionarcc = Series.objects.filter(Q(palabra_clave__icontains=series.palabra_clave)).count()

	relacionarpordirect = Series.objects.filter(Q(director__icontains=series.director)).order_by('-puntuacion')[:10]
	relacionarpordirectc = Series.objects.filter(Q(director__icontains=series.director)).order_by('-puntuacion').count()

	relacionarportitulo = Series.objects.filter(Q(titulo__startswith=series.titulo[:3])).order_by('-puntuacion')[:10]
	relacionarportituloc = Series.objects.filter(Q(titulo__startswith=series.titulo[:3])).order_by('-puntuacion').count()
	
	relacionarportema = Series.objects.filter(Q(tema__iexact=series.tema)|Q(tag1__iexact=series.tag1)|Q(tag2__iexact=series.tag2)|Q(tag3__iexact=series.tag3)).order_by('-puntuacion')[:10]
	relacionarportemac = Series.objects.filter(Q(tema__iexact=series.tema)).filter(Q(tema__iexact=series.tema)|Q(tag1__iexact=series.tag1)|Q(tag2__iexact=series.tag2)|Q(tag3__iexact=series.tag3)).order_by('-puntuacion')[:10].count()
	if not request.is_ajax():
		try:
			h = Hitcount_Series.objects.get(serie_id=id)
			form = count_series(request.POST or None, request.FILES or None, instance=h)
			if h.publish + timedelta(days=7) <= date.today():
				h.delete()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount = h.hitcount + 1
					instance.save()
		except ObjectDoesNotExist:
			instances = get_object_or_404(Series, id=id)
			form = count_series(request.POST or None, request.FILES or None)
			if form:
				instance = form.save(commit=False)
				instance.serie_id = id
				instance.hitcount = 1
				instance.save()
		else:
			try:
				h = Hitcount_Series.objects.get(serie_id=id)
			except ObjectDoesNotExist:
				h=0


	votacion = Votacion.objects.all()
	series_filt = True

	user_report = Reporte.objects.filter(reportador_id=request.user.id)
	report_user = []
	report_user_res = []
	for report_users in user_report:
		report_user.append(report_users.comentario)
		report_user_res.append(report_users.respuesta)

	#esto saca el promedio de la votacion lo Sum, no es la propia de python sino una que ofrece django
	votacion2 = Votacion.objects.filter(series_id=id).aggregate(total=Sum('votacion'))['total']
	#cuenta cuantas personas han votado
	votacion2c = Votacion.objects.filter(series_id=id).count()


	# esto es para saber sí el usuario ha votado, y hacer acciones de acuerdo a eso como no dejarlo votar más,
	# el objectdoesnotexist es para que sí el usuario no ha votado, no ejecuté el query
	try:
		votacion3 = Votacion.objects.filter(user_id=request.user.id).filter(series_id=id)
	except ObjectDoesNotExist:
		pass

#	try:
#		usuario = Usuario.objects.get(id=request.user.id)
#	except ObjectDoesNotExist:
#		pass


	print(votacion2)

	# aquí solo es para contar la cantidad de película en relación el menos 4 es para que en la cuatro querys 
	# elimine la película abierta... ya que también la cuenta como relacionada
	relacionarc = relacionarcc + relacionarportituloc + relacionarpordirectc  + relacionarportemac - 4
	cast = Cast.objects.all()
   # esto es para que muestre una vista específica al usuario que no está conectado
	if not request.user.is_active:

		if request.is_ajax():
			paginator = Paginator(comentarios_list, 5 + comentariosc)
		else: 
			paginator = Paginator(comentarios_list, 5)

		page = request.GET.get('page')
		try:
			comentarios = paginator.page(page)
		except PageNotAnInteger:
			comentarios = paginator.page(1)
		except EmptyPage:
			comentarios = paginator.page(paginator.num_pages)

			

		contexto = {
			'series':series,
			'relacionarr':relacionarr,
			'relacionarc':relacionarc,
	#		'a':a,
			'relacionarportitulo':relacionarportitulo,
			'relacionarpordirect':relacionarpordirect,
			'relacionarportema':relacionarportema,
			'comentarios':comentarios,
			'comentariosc':comentariosc,
			'votacion2':votacion2,
			'votacion2c':votacion2c,
			'votacion':votacion,
			'seriese':seriese,
			'seriesf':seriesf,
			'temporada':temporada,
			'series_filt':series_filt,
			'report_user':report_user,
			'report_user_res':report_user_res,
			'peliculase_seriesa':peliculase_seriesa,

#			'usuario':usuario,




			



			}

		# esto es para sacar el id del usuario de cada votacion y saber sí el usuario conectado voto
		if votacion:
			for a in votacion:
				print(a.user_id)
			contexto['a'] = a
				# recuerda que las votaciones se almacenan todas en tabla sin importar la pelicula
				# entonces lo que hago de esa tabla sacar la pelicula de acuerdo al id que se pasa en parametros
				# por la funcion
				# paso el except por si no hay votacion en la pelicula y no tire un 404
				# y como necesito tener la variable en el diccionario, porque sino tira error
				# le paso la variable pero con un false para que lo cuente como vacío
		try:
			votacion3 = Votacion.objects.filter(series_id=id)
			votacion4 = Votacion.objects.filter(user_id=request.user.id).filter(series_id=id)

			contexto['votacion3'] = votacion3
			contexto['votacion4'] = votacion4

		except ObjectDoesNotExist:
			votacion3 = False
			votacion4 = False

			contexto['votacion3'] = votacion3
			contexto['votacion4'] = votacion4

		# aquí es donde saco el promedio, el format es para que no me suelte decimales
		# de esta manera 4.44443 sino 4.4, 
		# el value error lo tira cuando el decimal es de 1 digito por lo tanto el format no funciona
		# el typeerror: es cuando no hay votaciones que promediar

		try:
			promedio = votacion2/votacion2c
			juan ="{0:.2}".format(promedio)
			contexto['promedio'] = juan
		except ValueError:
			promedio = votacion2/votacion2c
			contexto['promedio'] = promedio
			print(promedio)
		except TypeError:
			promedio = 0
			contexto['promedio'] = promedio
			print(promedio)
	
	# este codigo solo era de prueba no hace nada, but if the program it's working doesn't touch it 
	form = PostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.Series_id = id
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	# hasta aquí

	if request.is_ajax():
		paginator = Paginator(comentarios_list, 5 + comentariosc)
	else: 
		paginator = Paginator(comentarios_list, 5)
	page = request.GET.get('page')
	try:
		comentarios = paginator.page(page)
	except PageNotAnInteger:
		comentarios = paginator.page(1)
	except EmptyPage:
		comentarios = paginator.page(paginator.num_pages)
	


	contexto = {
			'series':series,
			'relacionarr':relacionarr,
			'relacionarc':relacionarc,
	#		'a':a,
			'relacionarportitulo':relacionarportitulo,
			'relacionarpordirect':relacionarpordirect,
			'relacionarportema':relacionarportema,
			'form':form,
			'comentarios':comentarios,
			'comentariosc':comentariosc,
			'votacion2':votacion2,
			'votacion2c':votacion2c,
			'votacion':votacion,
			'seriese':seriese,
			'seriesf':seriesf,
			'temporada':temporada,
			'series_filt':series_filt,
			'report_user':report_user,
			'report_user_res':report_user_res,
			'peliculase_seriesa':peliculase_seriesa,





			



			}

		# lo mismo de arriba pero para los usuarios registrados

	if votacion:
		for a in votacion:
			print(a.user_id)
		contexto['a'] = a

	try:
		votacion3 = Votacion.objects.filter(series_id=id)
		contexto['votacion3'] = votacion3
		votacion4 = Votacion.objects.filter(user_id=request.user.id).filter(series_id=id)
		contexto['votacion4'] = votacion4
	except ObjectDoesNotExist:
		votacion3 = False
		votacion4 = False

		contexto['votacion3'] = votacion3
		contexto['votacion4'] = votacion4




	try:
		promedio = votacion2/votacion2c
		juan ="{0:.2}".format(promedio)
		contexto['promedio'] = juan
	except ValueError:
		promedio = votacion2/votacion2c
		contexto['promedio'] = promedio
		print(promedio)
	except TypeError:
			promedio = 0
			contexto['promedio'] = promedio
			print(promedio)
	
	return render(request, 'seriessingle.html', contexto)





def temporada_detail(request, slug):
	temporada = Temporada.objects.get(id=slug)
	capitulo = Capitulos.objects.filter(temporadaa_id=slug)[0]
	capitulos = Capitulos.objects.filter(temporadaa_id=slug)
	series_filt = True



	contexto = {
	'temporada':temporada,
	'capitulo':capitulo,
	'series_filt':series_filt,


	}

	return render(request, 'temporada_detail.html', contexto)

def redirect(request, capitulo, temporada):
	pass
		


def capitulos_detail(request, capitulo, slug):
	

	user_report = Reporte.objects.filter(reportador_id=request.user.id)
	report_user = []
	report_user_res = []
	for report_users in user_report:
		report_user.append(report_users.comentario)
		report_user_res.append(report_users.respuesta)
	temporada = Temporada.objects.get(slug=slug)
	capitulo = Capitulos.objects.get(slug=capitulo)
	h = 0
	if not request.is_ajax():
		try:
			h = Hitcount_Series.objects.get(capitulo_id=capitulo.id)
			form = count_series(request.POST or None, request.FILES or None, instance=h)
			if h.publish + timedelta(days=7) <= date.today():
				h.delete()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount = h.hitcount + 1
					instance.update = date.today()
					instance.save()
		except ObjectDoesNotExist:
			instances = get_object_or_404(Capitulos, slug=capitulo.slug)
			form = count_series(request.POST or None, request.FILES or None)
			if form:
				instance = form.save(commit=False)
				instance.capitulo_id = instances.id
				instance.hitcount = 1
				instance.save()
	else:
		try:
			h = Hitcount_Series.objects.get(capitulo_id=capitulo.id)
		except objectdoesnotexist:
			h = 0
	siguiente = capitulo.num_episodio +1 
	anterior = capitulo.num_episodio -1
	get_siguiente=Capitulos.objects.filter(num_episodio=capitulo.num_episodio +1).filter(temporadaa_id=temporada.id)
	get_anterior=Capitulos.objects.filter(num_episodio=capitulo.num_episodio - 1).filter(temporadaa_id=temporada.id)[:1]
	
	series_filt = True
	comentarios_list = Post.objects.filter(capitulos_id=capitulo.id)
	comentariosc = Post.objects.filter(capitulos_id=capitulo.id).count()
	if request.is_ajax():
		paginator = Paginator(comentarios_list, 5 + comentariosc)
	else: 
		paginator = Paginator(comentarios_list, 5)

	page = request.GET.get('page')
	try:
		comentarios = paginator.page(page)
	except PageNotAnInteger:
		comentarios = paginator.page(1)
	except EmptyPage:
		comentarios = paginator.page(paginator.num_pages)
	contexto = {
	'temporada':temporada,
	'capitulo':capitulo,
	'series_filt':series_filt,
	'comentariosc':comentariosc,
	'comentarios':comentarios,
	'siguiente': siguiente,
	'h':h,
	'get_siguiente':get_siguiente,
	'anterior':anterior,
	'get_anterior':get_anterior,
	'report_user':report_user,
	'report_user_res':report_user_res,


	}

	return render(request, 'temporada_detail.html', contexto)


def añadirfavorito(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Series, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.favoritos.add(juan)
			instance.serie_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)

def eliminar_añadirfavorito(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Series, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.favoritos.remove(juan)
			instance.serie_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)

def reportar(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Series, id=id)
	form = reporte(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reportes = instances.reportes + 1
			instance.save()
			messages.success(request, "Gracias por reportar")
			data = {
				'message': "Gracias por reportar"
			}
			return JsonResponse(data)



# este es el formulario de votacion, simple
def votaciono(request, id):
	if not request.user.is_active:
		raise Http404
		
	form = votacion(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.series_id = id
			instance.save()
			# message success
					
			data = {
					'message': "Successfully submitted form data."
				}
			return JsonResponse(data)
def cambiar_votaciono_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Votacion, id=id)
	juan = request.user.id
	if request.is_ajax():
		instance.delete()
			# message success
				
		data = {
				'message': "Successfully submitted form data."
			}
	return JsonResponse(data)

# este es el formulario de ver mas tarde, simple

def series_list(request, filtro):
	if filtro == "orden_de_subida":
		filtro = "_id"
	seriesall = True
	series_filt = True
	juan = filtro.lstrip("_")
	filtron = filtro
	if "_" in filtro:
		series_list = Series.objects.all().order_by("-" + juan)
	else: 
		series_list = Series.objects.all().order_by(filtro)
	paginator = Paginator(series_list, 20)
	page = request.GET.get('page')
	try:
		series = paginator.page(page)
	except PageNotAnInteger:
		series = paginator.page(1)
	except EmptyPage:
		series = paginator.page(paginator.num_pages)

	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase_series = []

	for i in peliculasee:
		peliculase_series.append(i.series)

	count = Series.objects.all().count()
	contexto = {
	'series':series,
	'count':count,
	'filtro':filtron,
	'seriesall':seriesall,
	'peliculase_serie':peliculase_series,
	'series_filt':series_filt,


	}
	return render(request, 'moviegridfw.html', contexto)



def search_series(request):
	if request.method=='POST':
		peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculase = []

		for i in peliculasee:
			peliculase.append(i.series)

		srch = request.POST['src']
		juan = []
		count = -1
		index = ""
		series_filt = True
		if srch:
			juan.append(srch)


			for b in srch:
				count += 1 
				if b == " ":
					b = "_"
				index += b

		# -> NFC
		

		if srch:
			match = Series.objects.filter(Q(titulo__icontains=srch)|Q(tema__icontains=srch)|Q(tag1__icontains=index)|Q(tag2__icontains=index)|Q(tag3__icontains=index))
			matchc = Series.objects.filter(Q(titulo__icontains=srch)|Q(tema__icontains=srch)|Q(tag1__icontains=index)|Q(tag2__icontains=index)|Q(tag3__icontains=index)).count()
			paginator = Paginator(match, 20)
			page = request.GET.get('page')
			try:
				paginator = paginator.page(page)
			except PageNotAnInteger:
				paginator = paginator.page(1)
			except EmptyPage:
				paginator = paginator.page(paginator.num_pages)




			if paginator:
				contexto = {
				'peliculas':paginator,
				'count':matchc,
				'juan':srch,
				'series_filt':series_filt,
				'peliculase_serie': peliculase,


				}
				return render(request, 'movielist.html', contexto)
			elif paginator == 0:
				
				for i in srch:
					srch = correccion(i)
					print(srch)

				match = Series.objects.filter(Q(titulo__icontains=i))
				matchc = Series.objects.filter(Q(titulo__icontains=i)).count()
			
		
				contexto = {
				'sr':match,
				'count':matchc,
				'juan':srch,
				'series_filt':series_filt,
			'peliculase_serie': peliculase,

				}
				return render(request, 'movielist.html', contexto)
			else: 
				pass
		else:
			srch = "No has buscado nada"
			return HttpResponseRedirect('/series_list/orden_de_subida/')
	else:
		srch = "No has buscado nada"
		return HttpResponseRedirect('/series_list/orden_de_subida/')

			
	context = {'juan':srch, 'series_filt':series_filt, 'peliculase_serie': peliculase, }
	return render(request, 'movielist.html', context)


def filtrar(request):
	if request.method=='POST':
		peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculase = []

		for i in peliculasee:
			peliculase.append(i.series)

		letra = request.POST['letra']
		genero = request.POST['genero']
		año = request.POST['año']
		añof = request.POST['añof']
		pais = request.POST['pais']
		juan = []
		series_filt = True


		# -> NFC
		

		if  letra or genero or año or añof or pais:
			if letra and not genero and not pais and año and añof:
				match = Series.objects.filter(Q(titulo__startswith=letra)&Q(fecha_de_lanzamiento__year__range=(año, añof)))
				matchc = Series.objects.filter(Q(titulo__startswith=letra)&Q(fecha_de_lanzamiento__year__range=(año, añof))).count()

			else:
				match = Series.objects.filter(Q(titulo__startswith=letra)&Q(genero__icontains=genero)|Q(genero2__icontains=genero)&Q(fecha_de_lanzamiento__year__range=(año, añof))&Q(pais__startswith=pais.capitalize()))
				matchc = Series.objects.filter(Q(titulo__startswith=letra)&Q(genero__icontains=genero)|Q(genero2__icontains=genero)&Q(fecha_de_lanzamiento__year__range=(año, añof))&Q(pais__startswith=pais.capitalize())).count()
			paginator = Paginator(match, 20)
			page = request.GET.get('page')
			try:
				paginator = paginator.page(page)
			except PageNotAnInteger:
				paginator = paginator.page(1)
			except EmptyPage:
				paginator = paginator.page(paginator.num_pages)




			if paginator:
				contexto = {
				'peliculas':paginator,
				'count':matchc,
				'series_filt':series_filt,
				'peliculase_serie': peliculase,

				}
				return render(request, 'movielist.html', contexto)
			elif paginator == 0:
				

			
		
				contexto = {
				'count':matchc,
				'series_filt':series_filt,
				'peliculase_serie': peliculase,
				}
				return render(request, 'movielist.html', contexto)
			else: 
				messages.error(request, 'No se han encontrado resultados')
	else:
		return HttpResponseRedirect('/series_list/orden_de_subida/')
	contexto = {
			'count':matchc,
			'series_filt':series_filt,
			'peliculase_serie': peliculase,
			}
	return render(request, 'movielist.html', contexto)


def ontemporada(request, id):
	ser = Series.objects.get(id=id)
	if request.method =='POST':
		ona = request.POST['id']
		instances = get_object_or_404(Temporada, id=ona)
	form = TemporadA(request.POST or None, request.FILES or None, instance=instances)
	tempo = Temporada.objects.filter(serie_id=id)
	for i in tempo:
		if request.user in i.on.all():
			i.on.remove(request.user.id)
			i.save()
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.on.add(request.user.id)
			instance.temporada_id = instances.id
			instance.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)



def like(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Capitulos, id=id)
	form = Vote_capi(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instances.unvote_capitulo.all():
				instance.unvote_capitulo.remove(request.user.id)
			instance.vote_capitulo.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}
			return JsonResponse(data)

def unlike(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Capitulos, id=id)
	form = Vote_capi(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.vote_capitulo.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)

def dislike(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Capitulos, id=id)
	form = Unvote_capi(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instances.vote_capitulo.all():
				instance.vote_capitulo.remove(request.user.id)
			instance.unvote_capitulo.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}
			return JsonResponse(data)

def outdislike(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Capitulos, id=id)
	form = Unvote_capi(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.unvote_capitulo.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)

def reportar_cap(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Capitulos, id=id)
	form = reporte_cap(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reportes = instances.reportes + 1
			instance.save()
			messages.success(request, "Gracias por reportar")
			data = {
				'message': "Gracias por reportar"
			}
			return JsonResponse(data)