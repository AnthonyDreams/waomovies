from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from datetime import datetime, date, time, timedelta
from django.utils import timezone
from django.db.models import Q
from .models import Article, NewsTags
import itertools 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from apps.comentarios.models import Post

# Create your views here.
def NewsList(request):
	articulos_list = Article.objects.all().order_by('-id')
	noticias_count = Article.objects.filter(categoria="Noticias").count()
	critica_count = Article.objects.filter(categoria="Critica").count()
	global_count = Article.objects.filter(categoria="Global").count()

	paginator = Paginator(articulos_list, 30)
	mas_vistas = Hitcount_Articulos.objects.all().order_by('-hitcount_week')[:4]
	page = request.GET.get('page')
	try:
		articulos = paginator.page(page)
	except PageNotAnInteger:
		articulos = paginator.page(1)
	except EmptyPage:
		articulos = paginator.page(paginator.num_pages)
	context = {
		'articulos':articulos,
		'mas_vistas': mas_vistas,
		'noticias_count':noticias_count,
		'critica_count':critica_count,
		'global_count':global_count,

	}
	return render(request, 'bloggrid.html', context)



def Categories(request, categorie):
	noticias_count = Article.objects.filter(categoria="Noticias").count()
	critica_count = Article.objects.filter(categoria="Critica").count()
	global_count = Article.objects.filter(categoria="Global").count()
	if categorie.capitalize() == "Noticias" :
		articulos_list = Article.objects.filter(categoria="Noticias").order_by('-id')
		Noticias = True
		Critica = False
		Global = False
	elif categorie.capitalize() == "Critica":
		articulos_list = Article.objects.filter(categoria="Critica").order_by('-id')
		Noticias = False
		Critica = True
		Global = False
	elif categorie.capitalize() == "Global":
		articulos_list = Article.objects.filter(categoria="Global").order_by('-id')
		Noticias = False
		Critica = False
		Global = True
	else:
		raise 404
	paginator = Paginator(articulos_list, 30)
	mas_vistas = Hitcount_Articulos.objects.all().order_by('-hitcount_week')[:4]
	page = request.GET.get('page')
	try:
		articulos = paginator.page(page)
	except PageNotAnInteger:
		articulos = paginator.page(1)
	except EmptyPage:
		articulos = paginator.page(paginator.num_pages)
	context = {
		'articulos':articulos,
		'mas_vistas': mas_vistas,
		'noticias_count':noticias_count,
		'critica_count':critica_count,
		'global_count':global_count,
		'noticias':Noticias,
		'critica':Critica,
		'global':Global,


	}
	

	return render(request, 'bloggrid.html', context)





def BlogDetail(request, categorie,slug):
	blog_detail = Article.objects.get(slug=slug, categoria=categorie.capitalize())
	noticias_count = Article.objects.filter(categoria="Noticias").count()
	critica_count = Article.objects.filter(categoria="Critica").count()
	global_count = Article.objects.filter(categoria="Global").count()
	comentarios = Post.objects.filter(articulo_id=blog_detail.id)


	mas_vistas = Hitcount_Articulos.objects.all().order_by('-hitcount_week')[:4]
	try:
		userario = Votacion_Articulos.objects.filter(user=request.user, articulo_id=blog_detail.id)[0]
	except IndexError:
		userario = Votacion_Articulos.objects.filter(user=request.user, articulo_id=blog_detail.id)


	parrafo = blog_detail.contenido
	content = parrafo.split("</p>")
	parrafoo = []
	for parrafos in content:
		parrafoo.append(parrafos)

	

	if not request.is_ajax():
		try:
			h = Hitcount_Articulos.objects.get(articulo_id=blog_detail.id)
			form = count_articulo(request.POST or None, request.FILES or None, instance=h)
			if form:
				instance = form.save(commit=False)
				instance.hitcount_ever = h.hitcount_ever + 1
			if timezone.now() >= h.expired_day:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_day = 0
					instance.hitcount_week = h.hitcount_week + 1
					instance.hitcount_month = h.hitcount_month + 1
					instance.expired_day = timezone.now() + timedelta(days=7)
					instance.save()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_day = h.hitcount_day + 1	
					instance.save()
			if timezone.now() >= h.expired_week:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_week = 0
					instance.expired_week = timezone.now() + timedelta(days=7)
					instance.save()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_week = h.hitcount_week + 1
					instance.save()
			if timezone.now() >= h.expired_month:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_month = 0
					instance.expired_month = timezone.now() + timedelta(days=7)
					instance.save()
			else:
				if form:
					instance = form.save(commit=False)
					instance.hitcount_month = h.hitcount_month + 1
					instance.save()
		except ObjectDoesNotExist:
			instances = get_object_or_404(Article, slug=slug)
			form = count_articulo(request.POST or None, request.FILES or None)
			if form:
				instance = form.save(commit=False)
				instance.articulo_id = blog_detail.id
				instance.hitcount_day = 1
				instance.hitcount_week = 1
				instance.hitcount_month = 1
				instance.hitcount_ever = 1
				instance.expired_day = timezone.now() + timedelta(days=1)
				instance.expired_week = timezone.now() + timedelta(days=7)
				instance.expired_month = timezone.now() + timedelta(days=30)
				instance.save()
	else:
		try:
			h = Hitcount_Articulos.objects.get(articulo_id=blog_detail.id)
		except ObjectDoesNotExist:
			h = 0
	
	context = {
	'blog':blog_detail,
	'mas_vistas': mas_vistas,
		'noticias_count':noticias_count,
		'critica_count':critica_count,
		'global_count':global_count,
		'content':content,
		'parrafo':parrafoo,
		'userario':userario,
		'comentarios':comentarios,

	}

	return render(request, 'blogdetail.html', context)


def SearchRedirect(request):
	if request.method=='POST':

		srch = request.POST['src']
		slugsearch = ""
		index = ""
		series_filt = False
		if srch:
			for xy in srch:
				if xy == " ":
					xy = "-"
				slugsearch += xy

			for b in srch:
				if b == " ":
					b = "_"
				if b == "-":
					b = "_"
				index += b

		# -> NFC
		

		if srch and not srch == "":
			return HttpResponseRedirect('/blog_search/search/s=' + index)
		if srch == "":
			return HttpResponseRedirect('/ver%todo/')

def BlogSearch(request, searched):
	noticias_count = Article.objects.filter(categoria="Noticias").count()
	critica_count = Article.objects.filter(categoria="Critica").count()
	global_count = Article.objects.filter(categoria="Global").count()
	mas_vistas = Hitcount_Articulos.objects.all().order_by('-hitcount_week')[:4]
	src = searched
	srch = src
	slugsearch = ""
	srchh = ""
	juan = []
	count = -1
	index = ""
	series_filt = False
	if srch:
		buscar = NewsTags.objects.filter(tag__icontains=srch)
		idbuscar = []
		if buscar.count() > 0:
			idbuscar.append(buscar[0].id)
			if buscar.count() > 1:
				for iss in buscar:
					idbuscar.append(iss.id)
		juan.append(srch)
		for xy in srch:
			if xy == "_":
				xy = "-"
			slugsearch += xy

		for b in srch:
			count += 1 
			if b == "_":
				b = "_"

		for n in srch:
			if n == "_":
				n = " "
			srchh += n
	if srch:
		match = Article.objects.filter(Q(titulo__icontains=srchh)|Q(categoria__icontains=srch)|Q(tags__in=idbuscar)|Q(slug_search=slugsearch))
		matchc = Article.objects.filter(Q(titulo__icontains=srchh)|Q(categoria__icontains=srch)|Q(tags__in=idbuscar)|Q(slug_search=slugsearch)).count()
		paginator = Paginator(match, 20)
		page = request.GET.get('page')
		try:
			articulos = paginator.page(page)
		except PageNotAnInteger:
			articulos = paginator.page(1)
		except EmptyPage:
			articulos = paginator.page(paginator.num_pages)

	context = {
	'articulos':articulos,
	'matchc':matchc,
	'src':srchh,
	'mas_vistas': mas_vistas,
		'noticias_count':noticias_count,
		'critica_count':critica_count,
		'global_count':global_count,
	}
	return render(request, 'bloglist.html', context)


def votaciono_art(request, id):
	if not request.user.is_active:
		raise Http404
	userario = Votacion_Articulos.objects.filter(user=request.user, articulo_id=id)
	if userario.exists():
		raise Http404
	form = votacion_articulo(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.articulo_id = id
			instance.save()
			# message success
				
			data = {
				'message': "Successfully submitted form data."
			}
			return JsonResponse(data)


def cambiar_votaciono_articulo(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Votacion_Articulos, id=id)
	if request.is_ajax():
		instance.delete()
			# message success
				
		data = {
				'message': "Successfully submitted form data."
			}
	return JsonResponse(data)