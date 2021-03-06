
from django.shortcuts import (render, get_list_or_404, 
							redirect, get_object_or_404)
from itertools import chain
from datetime import datetime, date, time, timedelta
from apps.peliculas.models import *
import operator
import time
from django.http import *
from django.contrib import messages
from django.db.models import Q
import re
from unicodedata import normalize
from apps.peliculas import dic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from apps.comentarios.forms import PostForm
from apps.comentarios.models import *
from django.db.models import Sum
from .forms import *
from urllib.parse import quote_plus
from apps.usuarios.models import Usuario, Profile, UserPreference, IPS, USER_IPS
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from apps.series.models import Series, Hitcount_Series, Capitulos
from django.core import serializers
from rest_framework.views import APIView
from .serializers import Comparitapi,Friends, peliserializer, COMENTARIOS,notizerializer,pelisnoveerializer,SEGUIRYVER,serieserializer, GET_P
from apps.vermas_tarde.models import Vermastarde
from apps.notificaciones.models import Notificaciones, Evento, Compartir
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from apps.news.models import Hitcount_Articulos
from ipware import get_client_ip
import http.client
class pelis(APIView):
	serializer = peliserializer
	def get(self, request, format=None):
		lista = Peliculas.objects.all()
		response = self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data))

def search_result_ajax(request):

	if request.is_ajax():
		src = request.GET.get('term', '')
		puntuactions = '''!()[]{};:'"\,<>./?@#$%^&*'''
		srch = src
		slugsearch = ""
		srchh = ""
		juan = []
		count = -1
		index = ""
		series_filt = False
		if srch:
			juan.append(srch)
			for xy in srch:
				if xy in puntuactions:
					xy = ""
				if xy == " ":
					xy = "-"
				slugsearch += xy
			for values in srch:
				if values == " ":
					values = "_"
				srchh += values


		

		if srch:
			buscar =Busqueda_y_etiquetas.objects.filter(tag__icontains=srchh)
			idbuscar = []
			if buscar.count() > 0:
				idbuscar.append(buscar[0].id)
				if buscar.count() > 1:
					for iss in buscar:
						idbuscar.append(iss.id)


			match = Peliculas.objects.filter(Q(titulo__icontains=srch)|Q(titulo_orinal__icontains=srch)|Q(otras_etiquetas_y_busquedas__in=idbuscar)|Q(slug__icontains=slugsearch))
			matchc = Peliculas.objects.filter(Q(titulo__icontains=srchh)|Q(titulo_orinal__icontains=srch)|Q(otras_etiquetas_y_busquedas__in=idbuscar)|Q(slug__icontains=slugsearch)).count()

		results = []
		for datos in match:
			results.append(datos.titulo)

		data = json.dumps(results)
		mimetype = 'application/json'
		return HttpResponse(data, mimetype)

class Friendsitos(APIView):
	serializer = Friends
	def get(self, request, format=None):
		if request.user.is_authenticated:
			listica = Profile.objects.filter(user=request.user.id)
			for i in listica:
				amis = i.AmiGos.all()
			users_amigos = Profile.objects.filter(user__in=amis)
			if users_amigos.count() > 0:
				response = self.serializer(users_amigos, many=True)
				return HttpResponse(json.dumps(response.data))
			else:
				data = {
				'msg':'¡Debes agregar amigos para poder compartir en WaoMovies!',
				'url': '/user_ver_amigos/' + request.user.username + "/"
				}
				return JsonResponse(data)
		else:
			data = {
			'msg':'¡Tienes que registrarte/iniciar sesión si quieres compartir con amigos, sino, puedes compartir en tus redes!'
			}
			return JsonResponse(data)


class CompAPI(APIView):
	serializer = Comparitapi
	def get(self, request, format=None):
		listica = Compartir.objects.filter(users_to_share=request.user.id).order_by('-timestampc')[:20]
		response = self.serializer(listica, many=True)
		return HttpResponse(json.dumps(response.data))

class CompRead(APIView):
	serializer = Comparitapi
	def get(self, request, format=None):
		listica = Compartir.objects.filter(users_to_share=request.user.id).order_by('-timestampc').exclude(user_who_read=request.user.id)[:20]
		response = self.serializer(listica, many=True)
		anadir_read = Compartir.objects.filter(users_to_share=request.user.id).exclude(user_who_read=request.user.id)
		for a in anadir_read:
			if not request.user in a.user_who_read.all():
				a.user_who_read.add(request.user.id)
		return HttpResponse(json.dumps(response.data))

class Notifi(APIView):
	serializer = notizerializer
	def get(self, request, format=None):
		noti = Notificaciones.objects.filter(user_a_notificar=request.user.id)
		lista_noti = Evento.objects.filter(noti_de_evento__in=noti).order_by("-timestampe")[:20]
		lista_noticount = Evento.objects.filter(noti_de_evento__in=noti, status="Unread").count()
		response = self.serializer(lista_noti, many=True)
		return HttpResponse(json.dumps(response.data))

class IP_GET(APIView):
	serializer = GET_P
	def get(self, request, format=None):
		ip, is_routable = get_client_ip(request)
		if ip is None:
	   		print("No se puede obtener la ip")
		else:
			print("Normal " + ip)
			if is_routable:
				print("Publica " + ip)
			else:
				print("Privada " + ip)
		if request.user.is_authenticated:
			ipp = IPS.objects.filter(Ip=ip)
			if ipp:
				for count in ipp:
					count.hitcount += 1
					count.save()
				user_ip = USER_IPS.objects.filter(user=request.user.id)
				if user_ip:
					pass
				else:
					user = USER_IPS(user=request.user)
					user.save()
				total = 0
				false = 0
				user_ip = USER_IPS.objects.filter(user=request.user.id)
				for a in user_ip:
					for ip in a.ips.all():	
						total +=1			
						if ipp == ip: 
							pass
						else:
							false+=1
					if false == total:
						for p in ipp:
							a.ips.add(p.id)

			else:
				save_ip = IPS(Ip=ip)
				save_ip.save()
				user_ip = USER_IPS.objects.filter(user=request.user.id)
				if user_ip:
					pass
				else:
					user = USER_IPS(user=request.user)
					user.save()
				ipp = IPS.objects.filter(Ip=ip)
				user_ip = USER_IPS.objects.get(user=request.user.id)
				for p in ipp:
					user_ip.ips.add(p.id)

		else:
			ipp = IPS.objects.filter(Ip=ip)
			if ipp:
				for count in ipp:
					count.hitcount += 1
					count.save()
			else:
				save_ip = IPS(Ip=ip)
				save_ip.save()



		dataa = IPS.objects.filter(Ip=ip)
		response = self.serializer(dataa, many=True)
		return HttpResponse(json.dumps(response.data))


		

class Read(APIView):
	serializer = notizerializer
	def get(self, request, format=None):
		noti = Notificaciones.objects.filter(user_a_notificar=request.user.id)
		lista_noti = Evento.objects.filter(noti_de_evento__in=noti).order_by("-timestampe")[:20]
		lista_noticount = Evento.objects.filter(noti_de_evento__in=noti, status="Unread").count()
		response = self.serializer(lista_noti, many=True)
		Evento.objects.filter(noti_de_evento__in=noti, status="Unread").update(status="Read")
		return HttpResponse(json.dumps(response.data))

class pelis_user_nove(APIView):
	serializer = pelisnoveerializer
	def get(self, request, format=None):
		generos = []
		generoz = Generox.objects.all()
		for a in generoz:
			if request.user in a.accion.all():
				generos.append('ACC')
			if request.user in a.documental.all():
				generos.append('DOCU')
			if request.user in a.drama.all():
				generos.append('DRA')
			if request.user in a.crimen.all():
				generos.append('CRI')
			if request.user in a.ciencia_ficcion.all():
				generos.append('SC')
			if request.user in a.suspenso.all():
				generos.append('SUS')	
			if request.user in a.comedia.all():
				generos.append('COME')	
			if request.user in a.terror.all():
				generos.append('TER')	
			if request.user in a.romance.all():
				generos.append('ROM')	
			if request.user in a.aventura.all():
				generos.append('AVEN')	
			if request.user in a.fantasia.all():
				generos.append('FANT')	
			if request.user in a.animacion.all():
				generos.append('ANI')	

		lista = Peliculas.objects.filter((Q(genero__in=generos)|Q(genero2__in=generos)|Q(genero3__in=generos))).order_by("-id")[:20]
		response = self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data))

class añadiste(APIView):
	serializer = peliserializer
	def get(self, request, format=None):
		if request.user.is_authenticated:
			lista = Peliculas.objects.filter(favoritos=request.user.id)
			added_tema = []
			added_tag1 = []
			added_tag2 = []
			added_tag3 = []
			added_id = []
			for use in lista:
				added_tema.append(use.tema)
				added_tag1.append(use.tag1)
				added_tag2.append(use.tag2)
				added_tag3.append(use.tag3)
				added_id.append(use.id)

			instancess = UserPreference.objects.filter(user=request.user)
			lista2 = Peliculas.objects.filter(Q(tema__in=added_tema)|Q(tag1__in=added_tag1)|Q(tag2__in=added_tag2)|Q(tag3__in=added_tag3)).exclude(id__in=added_id)[instancess[0].endindex - 20:instancess[0].endindex]
			if instancess:
				instancess = UserPreference.objects.filter(user=request.user.id)[0]
				if  timezone.now() >= instancess.expired:
					instancess.endindex += 20
					instancess.save() 
					peliculass = instancess.week_recomendation.all()
					idsd = []
					for peli in peliculass:
						idsd.append(peli.id)
					try:
						confirm =  Peliculas.objects.filter(Q(tema__in=added_tema)|Q(tag1__in=added_tag1)|Q(tag2__in=added_tag2)|Q(tag3__in=added_tag3)).exclude(id__in=added_id)
						if instancess.endindex > confirm.count():
							instancess.endindex = 20
							instancess.save()
						mmm2 =Peliculas.objects.filter(Q(tema__in=added_tema)|Q(tag1__in=added_tag1)|Q(tag2__in=added_tag2)|Q(tag3__in=added_tag3)).exclude(id__in=list(set(idsd+added_id)))[instancess.endindex - 20:instancess.endindex]
					except IndexError:
						instancess.endindex = 20
						instancess.save()
						mmm2 =Peliculas.objects.filter(Q(tema__in=added_tema)|Q(tag1__in=added_tag1)|Q(tag2__in=added_tag2)|Q(tag3__in=added_tag3)).exclude(id__in=list(set(idsd+added_id)))[instancess.endindex - 20:instancess.endindex]

					fecha = timezone.now() + timedelta(days=7)
					instancess.expired = fecha
					instancess.week_recomendation.clear()
					instancess.save()
					instancess.week_recomendation.add(*mmm2)
				else:
					peliculass = instancess.week_recomendation.all()
					idsd = []
					for peli in peliculass:
						idsd.append(peli.id)

					mmm2 =Peliculas.objects.filter(id__in=idsd)
			else:
				if lista and not instancess:
					asunto = UserPreference(user=request.user, expired = timezone.now() + timedelta(days=7))
					asunto.save()
					mmm2 = Peliculas.objects.filter(Q(tema__in=added_tema)|Q(tag1__in=added_tag1)|Q(tag2__in=added_tag2)|Q(tag3__in=added_tag3)).exclude(id__in=added_id)[instancess.endindex - 20:instancess.endindex]
					asunto.week_recomendation.add(*mmm2)
				else:
					peliculass = instancess.week_recomendation.all()
					idsd = []
					for peli in peliculass:
						idsd.append(peli.id)
					mmm2 =Peliculas.objects.filter(id__in=idsd)
			
			

			response = self.serializer(mmm2, many=True)
			return HttpResponse(json.dumps(response.data))
		else: 
			pass

class seguirviendo(APIView):
	serializer = peliserializer
	def get(self, request, format=None):
		lista = Vermastarde.objects.filter(usuario_id=request.user.id).filter(series_id__isnull=True).order_by("fecha")
		pk_list = []
		for idd in lista:
			pk_list.append(idd.peliculas.id)
		ordering = 'FIELD(`id`, %s)' % ','.join(str(id) for id in pk_list)
		lista2 = list(Peliculas.objects.filter(id__in=pk_list))
		lista2.sort(key=lambda t: pk_list.index(t.pk))
		response = self.serializer(lista2, many=True)
		return HttpResponse(json.dumps(response.data))

class seguirviendo_series(APIView):
	serializer = serieserializer
	def get(self, request, format=None):
		lista = Vermastarde.objects.filter(usuario_id=request.user.id).filter(series_id__isnull=False).order_by("fecha")
		pk_list = []
		for idd in lista:
			pk_list.append(idd.series.id)
		ordering = 'FIELD(`id`, %s)' % ','.join(str(id) for id in pk_list)
		lista2 = list(Series.objects.filter(id__in=pk_list))
		lista2.sort(key=lambda t: pk_list.index(t.pk))
		response = self.serializer(lista2, many=True)
		return HttpResponse(json.dumps(response.data))

class answer_me(APIView):
	serializer = COMENTARIOS
	def get(self, request, format=None):
		lista = Post.objects.all()
		response = self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data))

def myview(request):
	objects = Post.objects.all()
	return render_to_response('indexx.html', { 'object':objects })


def list_moviejson(request):
	movie = serializers.serialize('json', Peliculas.objects.all())
	return HttpResponse(movie, content_type='aplication/json')
''' Esto solo hace query para mostrar las películas en el inicio, no hay algoritmos, aunque 
espero hacer uno para poner películas relacionadas según las favoritas del usuario

'''
def inicio(request):
	accion = Peliculas.objects.filter(Q(genero='ACC')|Q(genero2='ACC')|Q(genero3='ACC')).count()
	ciencia_ficcion = Peliculas.objects.filter(Q(genero='SC')|Q(genero2='SC')|Q(genero3='SC')).count()
	drama = Peliculas.objects.filter(Q(genero='DRA')|Q(genero2='DRA')|Q(genero3='DRA')).count()
	romance = Peliculas.objects.filter(Q(genero='ROM')|Q(genero2='ROM')|Q(genero3='DRA;')).count()
	crimen = Peliculas.objects.filter(Q(genero='CRI')|Q(genero2='CRI')|Q(genero3='CRI')).count()
	suspenso = Peliculas.objects.filter(Q(genero='SUS')|Q(genero2='SUS')|Q(genero3='SUS')).count()
	aventura = Peliculas.objects.filter(Q(genero='AVEN')|Q(genero2='AVEN')|Q(genero3='AVEN')).count()
	animacion = Peliculas.objects.filter(Q(genero='ANI')|Q(genero2='ANI')|Q(genero3='ANI')).count()
	comedia = Peliculas.objects.filter(Q(genero='COME')|Q(genero2='COME')|Q(genero3='COME')).count()
	terror = Peliculas.objects.filter(Q(genero='TER')|Q(genero2='TER')|Q(genero3='TER')).count()
	fantasia = Peliculas.objects.filter(Q(genero='FANT')|Q(genero2='FANT')|Q(genero3='FANT')).count()
	documental = Peliculas.objects.filter(Q(genero='DOCU')|Q(genero2='DOCU')|Q(genero3='DOCU')).count()

	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	ultimo = Capitulos.objects.all().order_by('id')[:10]
	capi = []
	temporada = []
	for n in ultimo:
		temporada.append(n.temporadaa)

	for b in temporada:
		if not b.serie in capi:
			capi.append(b.serie)
	
	peliculase = []
	peliculase_serie = []

	count = Hitcount.objects.all()
	count_series = Hitcount_Series.objects.all()

	if count:
		topsemanal = Hitcount.objects.filter(publish__day__range=(datetime.now().day - 7,datetime.now().day + 7)).exclude(hitcount=0).order_by('-hitcount')[:10]
		

	else:
		topsemanal = False
		topsemanall = False
	if request.user.is_authenticated:
		if request.user.is_admin:
			if count_series:
				topsemanal_serie = Hitcount_Series.objects.filter(capitulo_id__isnull=True).order_by('-hitcount')[:10]
				

			else:
				topsemanal_serie = False
				topsemanall_serie = False
		else:
				topsemanal_serie = False
				topsemanall_serie = False
	else:
		topsemanal_serie = False
		topsemanall_serie = False

	for i in peliculasee:
		peliculase.append(i.peliculas)
		peliculase_serie.append(i.series)

	

	peliculas = Peliculas.objects.all().order_by('-id')[:16]
	if request.user.is_authenticated:
		if request.user.is_admin:
			series = Series.objects.all().order_by('-id')[:16]
		else: 
			series= False
	else:
		series = False
	movies = Peliculas.objects.all().order_by('-id')[:10]
	trailers = Trailers.objects.all()[:10]
	

	# Order of precedence is (Public, Private, Loopback, None)

	contexto = {
	'peliculas':peliculas,
	'accion':accion,
	'ciencia_ficcion':ciencia_ficcion,
	'drama':drama,
	'romance':romance,
	'movies':movies,
	'trailers':trailers,
	'crimen':crimen,
	'terror':terror,
	'suspenso':suspenso,
	'aventura':aventura,
	'comedia':comedia,
	'animacion':animacion,
	'series':series,
	'topsemanal':topsemanal,
	'peliculase':peliculase,
	'peliculase_serie':peliculase_serie,
	'topsemanal_serie':topsemanal_serie,
	'capi':capi,
	'documental':documental,
	'fantasia':fantasia,
	'onseries': settings.SERIES,
	'inicio':True,

	}
	return render(request, 'index.html', contexto)

''' esta es la view de las peliculas en sí o object_detail

'''


def peliculasO(request, slug, *args, **kwargs):
	if not request.is_ajax():
		peliculasees = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculasa = []

		for i in peliculasees:
			peliculasa.append(i.peliculas)

	sacar_id = Peliculas.objects.get(slug=slug)
	id = sacar_id.id
	if not request.is_ajax():
		try:
			h = Hitcount.objects.get(pelicula_id=id)
			form = count(request.POST or None, request.FILES or None, instance=h)
			if timezone.now() >= h.expired:
				if form:
					instance = form.save(commit=False)
					instance.hitcount = 0
					instance.hitcount_ever = h.hitcount_ever + 1
					instance.expired = timezone.now() + timedelta(days=7)
					instance.save()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount = h.hitcount + 1
					instance.hitcount_ever = h.hitcount_ever + 1
					instance.save()
		except ObjectDoesNotExist:
			instances = get_object_or_404(Peliculas, id=id)
			form = count(request.POST or None, request.FILES or None)
			if form:
				instance = form.save(commit=False)
				instance.pelicula_id = id
				instance.hitcount = 1
				instance.hitcount_ever = 1
				instance.expired = timezone.now() + timedelta(days=7)
				instance.save()
	else:
		try:
			h = Hitcount.objects.get(pelicula_id=id)
		except ObjectDoesNotExist:
			h = 0



		

	
	peliculaa = Peliculas.objects.get(id=id)
	instance = get_object_or_404(Peliculas, id=id)


	user_report = Reporte.objects.filter(reportador_id=request.user.id)
	report_user = []
	report_user_res = []
	for report_users in user_report:
		report_user.append(report_users.comentario)
		report_user_res.append(report_users.respuesta)





	comentarios_list = Post.objects.filter(peliculas_id=id)
	comentariosc = Post.objects.filter(peliculas_id=id).count()
	if not request.is_ajax():
		peliculase = Vermastarde.objects.filter(peliculas_id=id).filter(usuario_id=request.user.id)
		peliculasf = peliculaa.favoritos.filter(id=request.user.id)
		# esto es para relacionar las peliculas de acuerdo a las palabras clave, director,titulo, tema, ect
		if peliculaa.tag_principal != "":
			relacionarr = Peliculas.objects.filter(Q(tag_principal__icontains=peliculaa.tag_principal)).order_by('-puntuacion')[:10]
			relacionarcc = Peliculas.objects.filter(Q(tag_principal__icontains=peliculaa.tag_principal)).count()
		else:
			relacionarr = Peliculas.objects.filter(Q(tag_principal__icontains="ALSJDHQWIPEQWI")).order_by('-puntuacion')[:10]
			relacionarcc = Peliculas.objects.filter(Q(tag_principal__icontains="ALSJDHQWIPEQWI")).count()
		relacionarpordirect = Peliculas.objects.filter(Q(director__icontains=peliculaa.director)).order_by('-puntuacion')[:10]
		relacionarpordirectc = Peliculas.objects.filter(Q(director__icontains=peliculaa.director)).order_by('-puntuacion').count()
		
		relacionarportitulo = Peliculas.objects.filter(Q(titulo__startswith=peliculaa.titulo[:3])).order_by('-puntuacion')[:10]
		relacionarportituloc = Peliculas.objects.filter(Q(titulo__startswith=peliculaa.titulo[:3])).order_by('-puntuacion').count()
		if peliculaa.tema == "":
			peliculaa.tema = "ALSJDHQWIPEQWI"
		if peliculaa.tag1 == "":
			peliculaa.tag1 = "ALSJDHQWIPEQWI"
		if peliculaa.tag2 == "":
			peliculaa.tag2 = "ALSJDHQWIPEQWI"
		if peliculaa.tag3 == "":
			peliculaa.tag3 = "ALSJDHQWIPEQWI"

		relacionarportema = Peliculas.objects.filter(Q(tema__iexact=peliculaa.tema)|Q(tag1__iexact=peliculaa.tag1)|Q(tag2__iexact=peliculaa.tag2)|Q(tag3__iexact=peliculaa.tag3)).order_by('-puntuacion')[:10]
		relacionarportemac = Peliculas.objects.filter(Q(tema__iexact=peliculaa.tema)|Q(tag1__iexact=peliculaa.tag1)|Q(tag2__iexact=peliculaa.tag2)|Q(tag3__iexact=peliculaa.tag3)).order_by('-puntuacion')[:10].count()

	votacion = Votacion.objects.all()
	user_id = peliculaa.favoritos.all()
	if user_id:
		for ccc in user_id:
			print(ccc.favoritos.all())
		recomendadas_despues_de_añadir_a_favoritos = ccc.favoritos.all()
	else:
		recomendadas_despues_de_añadir_a_favoritos = False





	#esto saca el promedio de la votacion lo Sum, no es la propia de python sino una que ofrece django
	votacion2 = Votacion.objects.filter(pelicula_id=id).aggregate(total=Sum('votacion'))['total']
	#cuenta cuantas personas han votado
	votacion2c = Votacion.objects.filter(pelicula_id=id).count()


	# esto es para saber sí el usuario ha votado, y hacer acciones de acuerdo a eso como no dejarlo votar más,
	# el objectdoesnotexist es para que sí el usuario no ha votado, no ejecuté el query
	try:
		votacion3 = Votacion.objects.filter(user_id=request.user.id).filter(pelicula_id=id)
	except ObjectDoesNotExist:
		pass

#	try:
#		usuario = Usuario.objects.get(id=request.user.id)
#	except ObjectDoesNotExist:
#		pass



	# aquí solo es para contar la cantidad de película en relación el menos 4 es para que en la cuatro querys 
	# elimine la película abierta... ya que también la cuenta como relacionada
	if not request.is_ajax():
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



		if not request.is_ajax():	

			contexto = {
				'peliculaa':peliculaa,
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
				'peliculase':peliculase,
				'peliculasf':peliculasf,
				'recomendadasfa':recomendadas_despues_de_añadir_a_favoritos,
				'report_user':report_user,
				'report_user_res':report_user_res,
				'peliculasa':peliculasa,
				

	#			'usuario':usuario,




				



				}
		else:
			contexto = {
			'peliculaa':peliculaa,
				'comentarios':comentarios,
				'votacion2':votacion2,
				'votacion2c':votacion2c,
				'votacion':votacion,
				'report_user':report_user,
			'report_user_res':report_user_res,
				
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
			votacion3 = Votacion.objects.filter(pelicula_id=id)
			votacion4 = Votacion.objects.filter(user_id=request.user.id).filter(pelicula_id=id)

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

	
	else:
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
		

		if not request.is_ajax():	
			contexto = {
					'peliculaa':peliculaa,
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
					'peliculase':peliculase,
					'peliculasf':peliculasf,
					'recomendadasfa':recomendadas_despues_de_añadir_a_favoritos,
					'report_user':report_user,
					'report_user_res':report_user_res,
					'peliculasa':peliculasa,
					






			



				}
		else:
			contexto = {
			'peliculaa':peliculaa,
				'comentarios':comentarios,
				'votacion2':votacion2,
				'votacion2c':votacion2c,
				'votacion':votacion,
				'report_user':report_user,
			'report_user_res':report_user_res,
				
				
			}

			# lo mismo de arriba pero para los usuarios registrados

		if votacion:
			for a in votacion:
				print(a.user_id)
			contexto['a'] = a

		try:
			votacion3 = Votacion.objects.filter(pelicula_id=id)
			contexto['votacion3'] = votacion3
			votacion4 = Votacion.objects.filter(user_id=request.user.id).filter(pelicula_id=id)
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


	return render(request, 'moviesingle.html', contexto)


	
def Generos(request):
	accion = Peliculas.objects.filter(genero='Acción').count()
	ciencia_ficcion = Peliculas.objects.filter(genero='Ciencia ficcion').count()
	drama = Peliculas.objects.filter(genero='Drama').count()
	misterio = Peliculas.objects.filter(genero='Misterio').count()

	contexto = {
	'accion':accion,
	'ciencia_ficcion':ciencia_ficcion,
	'drama':drama,
	'misterio':misterio,


	}

	return render(request, 'index.html', contexto)

def peliculas_list(request, filtro):
	seriesall = False
	juan = filtro.lstrip("_")
	filtron = filtro
	

	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.peliculas)
	if "_" in filtro[0]:
		peliculas_list = Peliculas.objects.all().order_by("-" + juan)
	else: 
		peliculas_list = Peliculas.objects.all().order_by(filtro)
	paginator = Paginator(peliculas_list, 30)
	page = request.GET.get('page')
	try:
		peliculas = paginator.page(page)
	except PageNotAnInteger:
		peliculas = paginator.page(1)
	except EmptyPage:
		peliculas = paginator.page(paginator.num_pages)

	count = Peliculas.objects.all().count()
	contexto = {
	'peliculas':peliculas,
	'count':count,
	'filtro':filtron,
	'seriesall':seriesall,
	'peliculase':peliculase,
	'select':filtro,


	}
	return render(request, 'moviegridfw.html', contexto)


def peliculas_listodo(request):
	peliculas_list = Peliculas.objects.all().order_by("-id")
	paginator = Paginator(peliculas_list, 30)


	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.peliculas)
	page = request.GET.get('page')
	try:
		peliculas = paginator.page(page)
	except PageNotAnInteger:
		peliculas = paginator.page(1)
	except EmptyPage:
		peliculas = paginator.page(paginator.num_pages)

	count = Peliculas.objects.all().count()
	contexto = {
	'peliculas':peliculas,
	'count':count,
	'peliculase':peliculase,


	}
	return render(request, 'moviegridfw.html', contexto)

''' 
esto es un diccionario que iba a implantar para el buscador


 
N = 134404155.0 # suma de todas  las frecuencias absolutas
PALABRAS = dict()

with open('C:/Users/Ant2D/Desktop/Wao/apps/peliculas/frecuencia.txt', 'r') as datafile:
	for line in datafile:
		valores = line.strip('\n').split()
		PALABRAS[valores[1]] = int(valores[2])

def P(palabra, N=sum(PALABRAS.values())): 
	"Probabilidad de `palabra`."
	return PALABRAS[palabra] / N

def correccion(palabra): 
	"Corrección más probable de una palabra."
	return max(candidatos(palabra), key=P)

def candidatos(palabra): 
	"Genera posibles correcciones para una palabra."
	return (conocidas([palabra]) or conocidas(edicion1(palabra)) or conocidas(edicion2(palabra)) or [palabra])

def conocidas(palabras): 
	"El subconjunto de `palabras` que aparecen en el diccionario de PALABRAS."
	return set(w for w in palabras if w in PALABRAS)

def edicion1(palabra):
	"Todas las ediciones que están a una edición de `palabra`."
	letras    = 'abcdefghijklmnopqrstuvwxyzáéíóúüñ'
	divisiones     = [(palabra[:i], palabra[i:])    for i in range(len(palabra) + 1)]
	omisiones    = [L + R[1:]               for L, R in divisiones if R]
	transposiciones = [L + R[1] + R[0] + R[2:] for L, R in divisiones if len(R)>1]
	remplazos   = [L + c + R[1:]           for L, R in divisiones if R for c in letras]
	inserciones    = [L + c + R               for L, R in divisiones for c in letras]
	return set(omisiones + transposiciones + remplazos + inserciones)

def edicion2(palabra): 
	"Todas las ediciones que están a dos ediciones de `palabra`."
	return (e2 for e1 in edicion1(palabra) for e2 in edicion1(e1))

'''
def search(request):
	if request.method=='POST':

		valor = request.POST['src']
		puntuactions = '''!()[]{};:'"\,<>./?@#$%^&*'''
		juan = []
		contar = -1
		contar_valor2 = -1
		index = ""

		valor2 = ""
		if valor:
			for b in valor:
				contar = contar + 1
				if b in puntuactions:
		 			b = ""
				if b == " " or b == "-" or b == "_":
					try:
						if valor[contar -1] == "-" or valor[contar + 1] =="-":
							b = ""
						elif valor[contar -1] == " " or valor[contar + 1] ==" ":
							b = ""
						else:
			 				b="_"
					except IndexError:
						b=""
					b="_"
					
				valor2 += b


		if valor2:
			for b in valor2:
				contar_valor2 = contar_valor2 + 1
				if b == "_":  
					if valor2[contar_valor2 -1] == "_":
						b = ""
				index +=b

		# -> NFC
		

		if valor and not valor == "":
			return HttpResponseRedirect('/search/search-' + index.lower())
		if valor == "":
			return HttpResponseRedirect('/ver%todo/')


	try:			
		context = {'juan':valor, 'series_filt':series_filt, 'peliculase':peliculase, }
	except UnboundLocalError:
		return HttpResponseRedirect('/ver%todo/')
	return render(request, 'movielist.html', context)


def search_result(request, src):

	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.peliculas)

	srch = src
	slugsearch = ""
	srchh = ""
	juan = []
	count = -1
	index = ""
	series_filt = False
	if srch:
		juan.append(srch)
		for xy in srch:
			if xy == "_":
				xy = "-"
			if xy in ['á','é','í','ó','ú']:
				if xy == 'á':
					xy = 'a'
				if xy == 'é':
					xy = 'e'
				if xy == 'í':
					xy = 'i'
				if xy == 'ó':
					xy = 'o'
				if xy == 'ú':
					xy = 'u'	
			slugsearch += xy

		for b in srch:
			count += 1 
			if b == "_":
				b = "_"

		for n in srch:
			if n == "_":
				n = " "
			srchh += n

	# -> NFC
	
	if srch:
		buscar =Busqueda_y_etiquetas.objects.filter(tag__icontains=srch)
		idbuscar = []
		if buscar.count() > 0:
			idbuscar.append(buscar[0].id)
			if buscar.count() > 1:
				for iss in buscar:
					idbuscar.append(iss.id)

		conn = http.client.HTTPSConnection("api.themoviedb.org")

		payload = "{}"
		conn.request("GET", "/3/search/movie?include_adult=false&page=1&query="+ slugsearch +"&language=en-US&api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)

		res = conn.getresponse()
		data = res.read()
		titulos = []
		titulos2 = []
		converted = json.loads(data.decode("utf-8"))
		for i in range(0,len(converted["results"])):
			titulos.append(json.dumps(converted["results"][i]["original_title"]))



		if int(json.dumps(converted["total_pages"])) > 1:
			for i in range(2,int(json.dumps(converted["total_pages"]))+1):
				conn.request("GET", "/3/search/movie?include_adult=false&page="+str(i)+"&query="+ slugsearch +"&language=en-US&api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
				res = conn.getresponse()
				data = res.read()
				converted = json.loads(data.decode("utf-8"))
				for i in range(0,len(converted["results"])):
					titulos.append(json.dumps(converted["results"][i]["original_title"]))
		

		for i in titulos:
			titulos2.append(i[i.find('"')+1:i.rfind('"')])

		match = Peliculas.objects.filter(Q(titulo__icontains=srchh)|Q(titulo_orinal__in=titulos)|Q(tema__icontains=srch)|Q(tag_principal=srch)|Q(tag1__icontains=srch)|Q(tag2__icontains=srch)|Q(tag3__icontains=srch)|Q(otras_etiquetas_y_busquedas__in=idbuscar)|Q(slug__icontains=slugsearch))
		matchc = Peliculas.objects.filter(Q(titulo__icontains=srchh)|Q(titulo_orinal__in=titulos)|Q(tema__icontains=srch)|Q(tag1__icontains=srch)|Q(tag_principal=srch)|Q(tag2__icontains=srch)|Q(tag3__icontains=srch)|Q(otras_etiquetas_y_busquedas__in=idbuscar)|Q(slug__icontains=slugsearch)).count()
		paginator = Paginator(match, 30)
		antes = ""
		if matchc == 0:
			
			if request.user.is_authenticated:
				guardar = Busqueda_y_etiquetas(tag=srch, user_who_search=request.user)
				guardar.save()
			else:
				guardar = Busqueda_y_etiquetas(tag=srch)
				guardar.save()
			for i in match:
				if i == " ":
					break
				else:
					antes += i
			match = Peliculas.objects.filter(titulo__startswith=antes)

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
			'juan':srchh,
			'series_filt':series_filt,
			'peliculase':peliculase,

			}
			return render(request, 'movielist.html', contexto)
		elif paginator == 0:
			
			for i in srchh:
				srchh = correccion(i)
				print(srchh)

			match = Peliculas.objects.filter(Q(titulo__icontains=i))
			
		
	
			contexto = {
			'sr':match,
			'count':matchc,
			'juan':srchh,
			'series_filt':series_filt,
			'peliculase':peliculase,

			}
			return render(request, 'movielist.html', contexto)
	

			
	context = {'juan':srchh, 'series_filt':series_filt, 'peliculase':peliculase, }
	return render(request, 'movielist.html', context)

def filtrar(request):
	if request.method=='POST':

		peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculase = []

		for i in peliculasee:
			peliculase.append(i.peliculas)

		letra = request.POST['letra']
		genero = request.POST['genero']
		año = request.POST['año']
		añof = request.POST['añof']
		pais = request.POST['pais']
		series_filt = False
		juan = []


		# -> NFC

		if  letra or genero or año or añof or pais:
			if letra and not genero and not pais and año and añof:
				match = Peliculas.objects.filter(Q(titulo__startswith=letra)&Q(fecha_de_lanzamiento__year__range=(año, añof)))
				matchc = Peliculas.objects.filter(Q(titulo__startswith=letra)&Q(fecha_de_lanzamiento__year__range=(año, añof))).count()

			else:
				match = Peliculas.objects.filter(Q(titulo__startswith=letra)&Q(genero__icontains=genero)|Q(genero2__icontains=genero)|Q(genero3__icontains=genero)&Q(fecha_de_lanzamiento__year__range=(año, añof))&Q(pais__startswith=pais.capitalize()))
				matchc = Peliculas.objects.filter(Q(titulo__startswith=letra)&Q(genero__icontains=genero)|Q(genero2__icontains=genero)|Q(genero3__icontains=genero)&Q(fecha_de_lanzamiento__year__range=(año, añof))&Q(pais__startswith=pais.capitalize())).count()
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
				'peliculase': peliculase,

				}
				return render(request, 'movielist.html', contexto)
			elif paginator == 0:
				

			
		
				contexto = {
				'count':matchc,
				'series_filt':series_filt,
				'peliculase': peliculase,
				}
				return render(request, 'movielist.html', contexto)
			else: 
				messages.error(request, 'No se han encontrado resultados')
	else:
		return HttpResponseRedirect('/ver%todo/')
	contexto = {
			'count':matchc,
			'series_filt':series_filt,
			'peliculase': peliculase,
			}
	return render(request, 'movielist.html', contexto)

def filtrar_resultado(request):
	pass


def Orden(request, generos):

	if not request.is_ajax():
		generocount = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).count()
		comedia = Generox.objects.get(genero_name="comedia")
		accion = Generox.objects.get(genero_name="accion")
		ciencia_ficcion = Generox.objects.get(genero_name="ciencia_ficcion")

		romance = Generox.objects.get(genero_name="romance")

		terror = Generox.objects.get(genero_name="terror")

		fantasia = Generox.objects.get(genero_name="fantasia")

		aventura = Generox.objects.get(genero_name="aventura")

		crimen = Generox.objects.get(genero_name="crimen")
		documental = Generox.objects.get(genero_name="documental")
		suspenso = Generox.objects.get(genero_name="suspenso")
		animacion = Generox.objects.get(genero_name="animacion")
		drama = Generox.objects.get(genero_name="drama")

		genero = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).order_by('-id')

		genero2 = Peliculas.objects.filter(genero=generos[0])
		genero3 = generos
		peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculase = []

		paginator = Paginator(genero, 30)
		page = request.GET.get('page')
		try:
			peliculas = paginator.page(page)
		except PageNotAnInteger:
			peliculas = paginator.page(1)
		except EmptyPage:
			peliculas = paginator.page(paginator.num_pages)
		for i in peliculasee:
			peliculase.append(i.peliculas)


		contexto = {
		'genero':genero,
		'generocount':generocount,
		'genero2':genero2,
		'genero3':generos,
		'peliculase':peliculase,
		'peliculas':peliculas,
		'comedia':comedia,
		'ciencia_ficcion':ciencia_ficcion,
		'terror':terror,
		'romance':romance,
		'aventura':aventura,
		'suspenso':suspenso,
		'documental':documental,
		'crimen':crimen,
		'fantasia':fantasia,
		'animacion':animacion,
		'drama':drama,
		'accion':accion,
		}

	else:
		genero2 = Peliculas.objects.filter(genero=generos[0])
		genero3 = generos
		contexto = {
		'genero2':genero2,
		'genero3':generos,

		}

		if generos == "COME":
			comedia = Generox.objects.get(genero_name="comedia")
			contexto['comedia'] = comedia
		elif generos == "ACC":
			accion = Generox.objects.get(genero_name="accion")
			contexto['accion'] = accion
		elif generos == "SC":
			ciencia_ficcion = Generox.objects.get(genero_name="ciencia_ficcion")
			contexto['ciencia_ficcion'] = ciencia_ficcion
		elif generos == "ROM":
			romance = Generox.objects.get(genero_name="romance")
			contexto['romance'] = romance
		elif generos == "TER":
			terror = Generox.objects.get(genero_name="terror")
			contexto['terror'] = terror
		elif generos == "FANT":
			fantasia = Generox.objects.get(genero_name="fantasia")
			contexto['fantasia'] = fantasia
		elif generos == "AVEN":
			aventura = Generox.objects.get(genero_name="aventura")
			contexto['aventura'] = aventura
		elif generos == "CRI":
			crimen = Generox.objects.get(genero_name="crimen")
			contexto['crimen'] = crimen
		elif generos == "DOCU":
			documental = Generox.objects.get(genero_name="documental")
			contexto['documental'] = documental
		elif generos == "SUS":
			suspenso = Generox.objects.get(genero_name="suspenso")
			contexto['suspenso'] = suspenso
		elif generos == "ANI":
			animacion = Generox.objects.get(genero_name="animacion")
			contexto['animacion'] = animacion
		elif generos == "DRA":
			drama = Generox.objects.get(genero_name="drama")
			contexto['drama'] = drama
		
		
		


	return render(request, 'generoview.html', contexto)


def genero_list(request, generos, filtro):

	if not request.is_ajax():

		generocount = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).count()
		comedia = Generox.objects.get(genero_name="comedia")
		accion = Generox.objects.get(genero_name="accion")
		ciencia_ficcion = Generox.objects.get(genero_name="ciencia_ficcion")

		romance = Generox.objects.get(genero_name="romance")

		terror = Generox.objects.get(genero_name="terror")

		fantasia = Generox.objects.get(genero_name="fantasia")

		aventura = Generox.objects.get(genero_name="aventura")

		crimen = Generox.objects.get(genero_name="crimen")
		documental = Generox.objects.get(genero_name="documental")
		suspenso = Generox.objects.get(genero_name="suspenso")
		animacion = Generox.objects.get(genero_name="animacion")
		drama = Generox.objects.get(genero_name="drama")

		genero = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).order_by('-puntuacion')

		genero2 = Peliculas.objects.filter(genero=generos[0])
		genero3 = generos
		seriesall = False
		juan = filtro.lstrip("_")
		filtron = filtro
		

		peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
		peliculase = []

		for i in peliculasee:
			peliculase.append(i.peliculas)
		if "_" in filtro[0]:
			peliculas_list = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).order_by("-" + juan)
		else: 
			peliculas_list = Peliculas.objects.filter(Q(genero=generos)|Q(genero2=generos)|Q(genero3=generos)).order_by(filtro)
		paginator = Paginator(peliculas_list, 30)
		page = request.GET.get('page')
		try:
			peliculas = paginator.page(page)
		except PageNotAnInteger:
			peliculas = paginator.page(1)
		except EmptyPage:
			peliculas = paginator.page(paginator.num_pages)

		contexto = {
		'genero':genero,
		'generocount':generocount,
		'genero2':genero2,
		'genero3':generos,
		'peliculas':peliculas,
		'filtro':filtron,
		'seriesall':seriesall,
		'peliculase':peliculase,
		'comedia':comedia,
		'ciencia_ficcion':ciencia_ficcion,
		'terror':terror,
		'romance':romance,
		'aventura':aventura,
		'suspenso':suspenso,
		'documental':documental,
		'crimen':crimen,
		'fantasia':fantasia,
		'animacion':animacion,
		'drama':drama,
		'accion':accion,
		'select':filtro,


		}
	else:
		genero2 = Peliculas.objects.filter(genero=generos[0])
		genero3 = generos
		contexto = {
		'genero2':genero2,
		'genero3':generos,

		}

		if generos == "COME":
			comedia = Generox.objects.get(genero_name="comedia")
			contexto['comedia'] = comedia
		elif generos == "ACC":
			accion = Generox.objects.get(genero_name="accion")
			contexto['accion'] = accion
		elif generos == "SC":
			ciencia_ficcion = Generox.objects.get(genero_name="ciencia_ficcion")
			contexto['ciencia_ficcion'] = ciencia_ficcion
		elif generos == "ROM":
			romance = Generox.objects.get(genero_name="romance")
			contexto['romance'] = romance
		elif generos == "TER":
			terror = Generox.objects.get(genero_name="terror")
			contexto['terror'] = terror
		elif generos == "FANT":
			fantasia = Generox.objects.get(genero_name="fantasia")
			contexto['fantasia'] = fantasia
		elif generos == "AVEN":
			aventura = Generox.objects.get(genero_name="aventura")
			contexto['aventura'] = aventura
		elif generos == "CRI":
			crimen = Generox.objects.get(genero_name="crimen")
			contexto['crimen'] = crimen
		elif generos == "DOCU":
			documental = Generox.objects.get(genero_name="documental")
			contexto['documental'] = documental
		elif generos == "SUS":
			suspenso = Generox.objects.get(genero_name="suspenso")
			contexto['suspenso'] = suspenso
		elif generos == "ANI":
			animacion = Generox.objects.get(genero_name="animacion")
			contexto['animacion'] = animacion
		elif generos == "DRA":
			drama = Generox.objects.get(genero_name="drama")
			contexto['drama'] = drama
		
		
	return render(request, 'generoview.html', contexto)

def añadirfavorito(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Peliculas, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.favoritos.add(juan)
		instance.pelicula_id = id
		instance.save()
		# message success
		messages.success(request, "Pelicula añadida a favoritos")
		return HttpResponseRedirect(instance.get_absolute_url())
			
	context = {
		"form": form,
	}
	return render(request, "login.html", context)

def eliminar_añadirfavorito(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Peliculas, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.favoritos.remove(juan)
		instance.pelicula_id = id
		instance.save()
		# message success
		messages.success(request, "Pelicula eliminada de favoritos")
		return HttpResponseRedirect(instance.get_absolute_url())
			
	context = {
		"form": form,
	}
	return render(request, "login.html", context)

def reportar(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Peliculas, id=id)
	form = reporte(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			instance.reportes = instances.reportes + 1
			messages.success(request, "Gracias por reportar")
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)




from .mixins import *
from django.views.generic import FormView
from apps.usuarios.forms import LoginForm
# este es el formulario de votacion, simple
class VotacionFormView(AjaxFormMixin, FormView):
	form_class = votacion
	template_name  = 'profile.html'


def FavoritoFormView(request, id):
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

def EliminarFavoritoFormView(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Peliculas, id=id)
	juan = request.user.id
	form = Favoritos(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.favoritos.remove(juan)
			instance.pelicula_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
		return JsonResponse(data)


def votaciono(request, id):
	if not request.user.is_active:
		raise Http404
		
	form = votacion(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.pelicula_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)

def cambiar_votaciono(request, id):
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

def test(request):

	return render(request, 'test.html')

from django.contrib.sessions.models import Session
def cookies(request):
	c = Session.objects.get(session_key='gf4793i7b48ay6tbdhsgfrnbqay879ep')

	a = request.COOKIES
	
	context = {'a':a,
				'c':c.get_decoded(),
	}

	return render(request, 'cookies.html', context)

def testing(request):

	return render(request, 'test.html')

from django.contrib.sessions.models import Session
def cookies(request):
	c = Session.objects.get(session_key='gf4793i7b48ay6tbdhsgfrnbqay879ep')

	a = request.COOKIES
	
	context = {'a':a,
				'c':c.get_decoded(),
	}

	return render(request, 'cookies.html', context)

def GeneroF(request, genre):
	if request.is_ajax():
		if genre == "drama":
			c = Generox.objects.get(genero_name="drama")
			c.drama.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "ciencia_ficcion":
			c = Generox.objects.get(genero_name="ciencia_ficcion")
			c.ciencia_ficcion.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "accion":
			c = Generox.objects.get(genero_name="accion")
			c.accion.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "aventura":
			c = Generox.objects.get(genero_name="aventura")
			c.aventura.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "crimen":
			c = Generox.objects.get(genero_name="crimen")
			c.crimen.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "terror":
			c = Generox.objects.get(genero_name="terror")
			c.terror.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "fantasia":
			c = Generox.objects.get(genero_name="fantasia")
			c.fantasia.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "romance":
			c = Generox.objects.get(genero_name="romance")
			c.romance.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "documental":
			c = Generox.objects.get(genero_name="documental")
			c.documental.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "comedia":
			c = Generox.objects.get(genero_name="comedia")
			c.comedia.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "animacion":
			c = Generox.objects.get(genero_name="animacion")
			c.animacion.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "suspenso":
			c = Generox.objects.get(genero_name="suspenso")
			c.suspenso.add(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)



def GeneroF_eliminar(request, genre):
	if request.is_ajax():
		if genre == "drama":
			c = Generox.objects.get(genero_name="drama")
			c.drama.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "ciencia_ficcion":
			c = Generox.objects.get(genero_name="ciencia_ficcion")
			c.ciencia_ficcion.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "accion":
			c = Generox.objects.get(genero_name="accion")
			c.accion.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "aventura":
			c = Generox.objects.get(genero_name="aventura")
			c.aventura.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "crimen":
			c = Generox.objects.get(genero_name="crimen")
			c.crimen.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "terror":
			c = Generox.objects.get(genero_name="terror")
			c.terror.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "fantasia":
			c = Generox.objects.get(genero_name="fantasia")
			c.fantasia.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "romance":
			c = Generox.objects.get(genero_name="romance")
			c.romance.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "documental":
			c = Generox.objects.get(genero_name="documental")
			c.documental.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "comedia":
			c = Generox.objects.get(genero_name="comedia")
			c.comedia.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "animacion":
			c = Generox.objects.get(genero_name="animacion")
			c.animacion.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)
		if genre == "suspenso":
			c = Generox.objects.get(genero_name="suspenso")
			c.suspenso.remove(request.user.id)
			c.save()
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)



def gettingembed(request, id):
	get = Peliculas.objects.get(id=id)
	if request.is_ajax():
		server = request.POST.get('server')
		if server == "rapidvideo":
			embed = get.rapidvideo
		elif server == "openload":
			embed = get.openload
		elif server == "vidoza":
			embed = get.vidoza
		elif server == "streamcloud":
			embed = get.streamcloud
		elif server == "streamago":
			embed = get.streamago
		elif server == "vidlox":
			embed = get.vidlox
		elif server == "servidor1":
			embed = get.servidor1
		elif server == "servidor2":
			embed = get.servidor2
		elif server == "servidor3":
			embed = get.servidor3
		elif server == "servidor4":
			embed = get.servidor4
		else:
			embed = None
		data= {
		'embed': embed,
		}

		return JsonResponse(data)

def actualizar_tops(request):
	if not request.is_ajax() and request.user.is_admin:
		hit = Hitcount.objects.all()
		hit_serie = Hitcount_Series.objects.all()
		hit_articulos = Hitcount_Articulos.objects.all()
		for h in hit: 
			if timezone.now() >= h.expired:
				h.hitcount = 0
				h.expired = timezone.now() + timedelta(days=7)
				h.save()	
		for h_serie in hit_serie:
			if timezone.now() >= h_serie.expired:
				h_serie.hitcount = 0
				h_serie.expired = timezone.now() + timedelta(days=7)
				h_serie.save()
		for h_articulos in hit_articulos:
			if timezone.now() >= h_articulos.expired_day:
				h_articulos.hitcount_day = 0
				h_articulos.expired_day = timezone.now() + timedelta(days=1)
				h_articulos.save()
			
			if timezone.now() >= h_articulos.expired_week:
				h_articulos.hitcount_week = 0
				h_articulos.expired_week = timezone.now() + timedelta(days=7)
				h_articulos.save()
			
			if timezone.now() >= h_articulos.expired_month:
				h_articulos.hitcount_month = 0
				h_articulos.expired_month = timezone.now() + timedelta(days=7)
				h_articulos.save()
			
	return HttpResponseRedirect('/inicio/')





def set_themvd_id(request, id):
	pelicula = Peliculas.objects.get(id=id)
	conn = http.client.HTTPSConnection("api.themoviedb.org")
	payload = "{}"
	if pelicula.theid:
		movie = pelicula.theid
		conn.request("GET", "/3/movie/" + str(movie) + "/credits?api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
		res = conn.getresponse()
		data = res.read()
		converted = json.loads(data.decode("utf-8"))
		return HttpResponse(json.dumps(converted["cast"][:8]))
	else:
		conn = http.client.HTTPSConnection("api.themoviedb.org")
		payload = "{}"
		namet = ""
		for a in pelicula.titulo_orinal:
			if a == " ":
				a = "-"
			namet += a
		conn.request("GET", "/3/search/movie?include_adult=false&page=1&query=" + namet + "&language=en&api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
		res = conn.getresponse()	
		data = res.read()
		converted = json.loads(data.decode("utf-8"))
		if converted["total_results"] >= 1:
			confirm = Peliculas.objects.get(titulo_orinal=converted["results"][0]["title"])
			confirm.theid = converted["results"][0]["id"]
			confirm.save()
			peliculaa = Peliculas.objects.get(theid=confirm.theid)
			conn.request("GET", "/3/movie/" + str(confirm.theid) + "/credits?api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
			res = conn.getresponse()
			data = res.read()
			converted = json.loads(data.decode("utf-8"))
			return HttpResponse(json.dumps(converted["cast"][:8]))


		if converted["total_results"] == 0:
			print("no results")

			




def analizis(request):
	a = Peliculas.objects.all()
	b = []
	for i in a:
		c = str(a.CoverImg)
		response = requests.get("https://d3mp3oxoqwxddf.cloudfront.net/media/static/comprimidas/compress_" + c)
	try:
		img = Image.open(BytesIO(response.content))
		return "https://d3mp3oxoqwxddf.cloudfront.net/media/static/comprimidas/compress_" + str(self.CoverImg)
	except OSError:
		return str(self.Cover.url)


def aa(request):
	a = Peliculas.objects.all()
	b = ['https://www.rapidvideo.com/e/FTBXT0V3NG', 'https://www.rapidvideo.com/e/FXPVRZ4T0P', 'https://www.rapidvideo.com/e/FWS0FNKHRB', 'https://www.rapidvideo.com/e/FUT9JN1FG8', 'https://www.rapidvideo.com/e/FT3WW1VMB4', 'https://www.rapidvideo.com/e/FX4U9VMPA0', 'https://www.rapidvideo.com/embed/FXYM8U4AFY', 'https://www.rapidvideo.com/e/FXT6NHHYIW', 'https://www3616.playercdn.net/187/3/zQr5gsV6VCRTKcV_Zw5xIg/1544417125/180106/057FN6KURV5SPX7SDKPDI.mp4', 'https://www3574.playercdn.net/187/1/uaE-rM4ySRNHHaUW9RR5qA/1544404886/171230/961FMZJ5CDS2CPMUAIIEX.mp4', 'https://www.rapidvideo.com/embed/FQIFLXAUAE', 'https://divorce.playercdn.net/187/0/xH3Gvlj8bFe1Cd0_ZJL0KQ/1545129144/181029/414FWP755MEIFFXMLL2S6.mp4', 'https://www.rapidvideo.com/embed/FVVKP8LSBG', 'https://www.rapidvideo.com/embed/FO9G3O99IJ', 'https://www.rapidvideo.com/e/FXPVZ0VBO8', 'https://www.rapidvideo.com/embed/FSJ2DUXKDC', 'https://www.rapidvideo.com/e/FTZ0H5XT3T', 'https://www.rapidvideo.com/e/FX59ROUA75', 'https://www.rapidvideo.com/e/FX55XVTZG9', 'https://www.rapidvideo.com/e/FXT78WG1TF', 'https://www.rapidvideo.com/e/FVTNIXF91P', 'https://www.rapidvideo.com/e/FSTLI3F2V6', 'https://rapidvideo.com/e/FVCD6GCPTZ', 'https://www.rapidvideo.com/e/FW5634T1H9', 'https://rapidvideo.com/e/FWU86HUWVG', 'https://www.rapidvideo.com/embed/FNJFLAWYEX', 'https://www.rapidvideo.com/e/FRVYS69WZX', 'https://rapidvideo.com/e/FW6APOIG10', 'https://rapidvideo.com/e/FWVHWYWPA9', 'https://www.rapidvideo.com/e/FT56HHOXVF', 'https://www.rapidvideo.com/e/FT13MS8U92', 'https://www.rapidvideo.com/e/FUUZBQARDW', 'https://www.rapidvideo.com/e/FTC8LZJ2J6', 'https://www.rapidvideo.com/e/FTPUPQKF5T', 'https://www.rapidvideo.com/e/FXQCXZ2QYR', 'https://www.rapidvideo.com/e/FUGJPEJ2M5', 'https://rapidvideo.com/e/FVCDCHS34E', 'https://www3798.playercdn.net/187/0/U6p_rGTr90UWoUS9-YMuRA/1545124973/180126/708FNUGBCZQ470X4I3LFK.mp4', 'https://www.rapidvideo.com/embed/FXFF5AO6U6', 'https://www.rapidvideo.com/embed/FYP5PSQKBZ', 'https://www.rapidvideo.com/e/G0OQR50F0H', 'https://www.rapidvideo.com/embed/FYTTCKTSY6', 'https://www.rapidvideo.com/embed/FSI187V34O', 'https://server.pelisplus.to/enlace/FYCOA635YI/rapidvideo', 'https://www929.playercdn.net/187/2/MRhcQS-3bIaJWEIjNjup2g/1545371363/180115/257FNH7RDVRR93MZNGUTG.mp4', 'https://www.rapidvideo.com/embed/FQGKCNAFID', 'https://www.rapidvideo.com/embed/FUPOLM8DH9', '//www.youtube.com/embed/nOGsB9dORBg', 'https://protect.playercdn.net/187/7/jTg4Ez9Jw13sXgCzWPE3eg/1545363014/181113/951FX75RTCZZWVXP9KCUO.mp4', 'https://www.rapidvideo.com/embed/FUXSR8E8DV', 'https://www.rapidvideo.com/e/FXGNI5QO1H', 'https://www.rapidvideo.com/e/FWN1E8OI5S', 'https://www.rapidvideo.com/embed/FYMQOI061F', 'https://www3801.playercdn.net/187/0/wgSH8CK9vdiT9f4otHiXtg/1545130031/181017/502FWBFCTYMSJXKARR9EM.mp4', 'https://www.rapidvideo.com/embed/FQJC1A2E4O', 'https://www.rapidvideo.com/embed/FUPOJSHRKX', 'https://www.rapidvideo.com/e/FX5AUXGI2F', 'https://www.rapidvideo.com/embed/FRWMKNFKLE', 'https://www.rapidvideo.com/embed/FV1WF91HFC', 'https://www.rapidvideo.com/e/FT8S2GXB6L', 'https://www3492.playercdn.net/187/3/5zl5SApHWBH2646qOFvShQ/1545379379/180131/540FO01F6K397ZRE3QCO5.mp4', 'https://rapidvideo.com/e/FI78AO7502', 'https://www.rapidvideo.com/e/FX54XR0QT1', 'https://www.rapidvideo.com/embed/FY59ZWCXF0', 'https://www.rapidvideo.com/e/FUP6J8UJYG', 'https://www.rapidvideo.com/embed/FXNH8GUI5I', 'https://www3963.playercdn.net/187/0/FvMv8923s0zKTmJ6iUAifg/1545126018/180915/146FVA0P76LCBVQEBW2C4.mp4', 'https://www.rapidvideo.com/e/FTD9TCTLPK', 'https://www3790.playercdn.net/187/0/SBO7Gyu675HC5iMkF2VWNQ/1545125532/180901/550FUUAU65OPOEHQXTOOY.mp4', 'https://superior.playercdn.net/187/8/dSn2SbtDnmMGhGJPi-6ZZA/1545124283/181203/059FXT922HNC8NMF5TL2U.mp4', 'https://www.rapidvideo.com/embed/FXNCUZ23TF', 'https://www3795.playercdn.net/187/0/VlKrrFP9c4CD7-gEg92Hvw/1545123179/181107/808FX023DOB3ZV3QJAXC5.mp4', 'https://www.rapidvideo.com/embedFQJLTS8NWP', 'https://rapidvideo.com/e/FX3YZCKIYE', 'https://www.rapidvideo.com/embed/FM9BS7Y42T', 'https://www.rapidvideo.com/embed/FYMQOI04UJ', 'https://www.rapidvideo.com/e/FSTLICDHX3', 'https://www3603.playercdn.net/187/0/vXIdTOqj8UErGJPsI1beXQ/1545130420/181017/492FWBEY8XAPMUMRZGERG.mp4', 'https://www.rapidvideo.com/e/FVQ38BWCZ5', 'https://www.rapidvideo.com/e/FX4TI2HFYI', 'https://www.rapidvideo.com/embed/G0NXRE44TZ', 'https://www.rapidvideo.com/e/FU8FQFW3EK', 'https://www.rapidvideo.com/e/FTZ0HPZUMA', 'https://streamango.com/embed/qsbrkdddtqaqkkke', 'https://www.rapidvideo.com/e/FX53X40XEV', 'https://www.rapidvideo.com/embed/FYLLCKSDLL', 'https://rapidvideo.com/e/FYEFZW588S', 'https://www.rapidvideo.com/e/FX4WNQRNA6', 'https://www.rapidvideo.com/e/FTX6GOI1DC', 'https://www.rapidvideo.com/embed/FY4Q6TI0NC', 'https://effect.playercdn.net/186/7/DvkRgT5ORjyLnND46U_3hg/1545363300/181117/050FXAQRIZMHAIJLK0ULM.mp4', 'https://www.rapidvideo.com/e/FY1XFBS0TW', 'https://www.rapidvideo.com/e/FXW8GAIPHO', 'https://www.rapidvideo.com/embed/FSG9S4ZJ7Q', 'https://www.rapidvideo.com/e/FUP6J73FW0', 'https://www925.playercdn.net/187/1/F0eqia7AmHSxy0ZGHhAFnQ/1545122576/180611/mL3kF8GBtKZzLCC.mp4', 'https://www.rapidvideo.com/e/FUP6JBSQF9', 'https://rapidvideo.com/e/FWUTZZ85R6', 'https://www.rapidvideo.com/embed/FXNCM4WTOL', 'https://www.rapidvideo.com/embed/FXNCDJN3PN', 'https://www.rapidvideo.com/embed/FXNC7LCFFS', 'https://www.rapidvideo.com/embed/FVPI8CDAZ2', 'https://www.rapidvideo.com/embed/FMPJS9II95', 'https://www.rapidvideo.com/embed/FY4Q1A5UGR', 'https://www.rapidvideo.com/e/FU9RL2WWSE', 'https://www.rapidvideo.com/embed/FP61X2CPN7', 'https://rapidvideo.com/e/FVKJARJVQE', 'https://www.rapidvideo.com/e/FZKKSJAC9T', 'https://www.rapidvideo.com/e/FX5BI3NLLE', 'https://www.rapidvideo.com/embed/FRSKBVSECR', 'https://www.rapidvideo.com/embed/FRKQKNIW2U', 'https://www.rapidvideo.com/embed/R5FSBTFVF', 'https://www.rapidvideo.com/embed/FX973JVL7', 'https://www.rapidvideo.com/e/FX54XR0QT1', 'https://rapidvideo.com/e/FWF6FFC7BW', 'https://www.rapidvideo.com/e/FXXQS02BU7', 'https://rapidvideo.com/e/FXQVFGX63D', 'https://www.rapidvideo.com/embed/FJVJK5IXE2', 'https://www.rapidvideo.com/embed/FYO273WL01', 'https://www.rapidvideo.com/e/FTBXT0V3NG', 'https://rapidvideo.com/e/FX43XL0F49', 'https://www3757.playercdn.net/187/0/H_BcSw8tOMnNCZdGqGZuMw/1545364135/180130/813FNZ76KLXUJ3VP1I5CO.mp4', 'https://www.rapidvideo.com/e/FWRZB148NP', 'https://rapidvideo.com/e/FWGOMJYZTV', 'https://www.rapidvideo.com/e/FSQ1RX2V3M', 'https://rapidvideo.com/e/FXOTBM20Y8', 'https://rapidvideo.com/e/FX3JCYV5HK', 'https://rapidvideo.com/e/FSSXW63NY4', 'https://www.rapidvideo.com/embed/FSX4RA97RF', 'https://www.rapidvideo.com/e/FVHUNE8BEK', 'https://www.rapidvideo.com/e/FSTLFNXJXD', 'https://www.rapidvideo.com/e/FUT9JDJBRC', 'https://rapidvideo.com/e/FWU6VIFA9M', 'https://www.rapidvideo.com/e/FUWQPYWY5G', 'https://www.rapidvideo.com/e/FVTB2C0R3N', 'https://www.rapidvideo.com/embed/FSJ8K5QKVT', 'https://www.rapidvideo.com/e/FTPVEK8BD6', 'https://www.rapidvideo.com/e/FWV532V3RQ', 'https://www.rapidvideo.com/embed/FUXRURV2XD', 'https://www.rapidvideo.com/e/FVY4YGGBKA', 'https://www.rapidvideo.com/embed/FRZM99V3E6', 'https://www.rapidvideo.com/embed/FNLG1Q0EEY', 'https://www.rapidvideo.com/e/FUWVQMIF9H']
	c = []

	for i in a:
		if i.links == "":
			c.append(i.titulo)
	print(c)
	print(len(c))

