from django.shortcuts import render
from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from .forms import *
from .models import Post, Answerd
from django.db import IntegrityError
from django.template import RequestContext
from django.http import JsonResponse
from apps.notificaciones.models import Notificaciones, Evento
from apps.usuarios.models import Usuario



def myurl(request):
    return render_to_response('template.html', {},
                               context_instance=RequestContext(request))
# Create your views here.

def post_create(request, id):
	if not request.user.is_active:
		raise Http404
	post = Post.objects.all()
	x = []
	for i in post:
		print(i.slug)
		x.append(i.slug)
	form = PostForm(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.peliculas_id = id
			if x:
				instance.slug = x[0] +1
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()

				data = {
				'message': "Successfully submitted form data."

			}
				return JsonResponse(data)
			else: 
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()

				data = {
				'message': "Successfully submitted form data."
			}

				return JsonResponse(data)


#actualizar comentario
def post_update(request, slug=None):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
				'message': "Successfully submitted form data.",
				'content':instance.content
			}
			return JsonResponse(data)




def post_delete(request, slug):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Comentario eliminado.",

			}
		return JsonResponse(data)




# serie part



def post_create_serie(request, id):
	if not request.user.is_active:
		raise Http404
	post = Post.objects.all()
	x = []
	for i in post:
		print(i.slug)
		x.append(i.slug)
		
	form = PostForm(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.series_id = id
			if x:
				instance.slug = x[0] +1
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()
				data = {
				'message': "Successfully submitted form data.",
				'content':instance.content
			}
				return JsonResponse(data)
			else: 
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()
				data = {
				'message': "Successfully submitted form data.",
				'content':instance.content
			}
				return JsonResponse(data)

		

		

	context = {
		"form": form,
	}

def like(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Vote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instances.unvote.all():
				instance.unvote.remove(request.user.id)
			instance.vote.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}

			if not instances.user == request.user:
				comentario = Notificaciones.objects.get(komentario=instances)
				evenT = Evento(event="like", mensaje=request.user.username + " Ha dado like a tu comentario", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()
		
			return JsonResponse(data)

def unlike(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Vote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.vote.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)

def dislike(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Unvote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instances.vote.all():
				instance.vote.remove(request.user.id)
			instance.unvote.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}
			return JsonResponse(data)

def outdislike(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = Unvote(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.unvote.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)




#actualizar comentario
def post_update_serie(request, slug=None):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
					'message': "Successfully submitted form data.",
					'content':instance.content
				}
			return JsonResponse(data)


def post_delete_serie(request, slug):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Comentario eliminado.",

			}
		return JsonResponse(data)







def post_create_serie_capitulo(request, id):
	if not request.user.is_active:
		raise Http404
	post = Post.objects.all()
	x = []
	for i in post:
		print(i.slug)
		x.append(i.slug)
		
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.series_id = id
		if x:
			instance.slug = x[0] +1
			instance.save()
			sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
			sendnoti.save()
			messages.success(request, "Comentario enviado")
			return HttpResponseRedirect(instance.get_absolute_url_serie())
		else: 
			instance.save()
			sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
			sendnoti.save()
			messages.success(request, "Comentario enviado")
			return HttpResponseRedirect(instance.get_absolute_url_serie())

		

		

	context = {
		"form": form,
	}

#actualizar comentario
def post_update_serie_capitulo(request, slug=None):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Comentario editado", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url_serie())

	context = {
		"title": instance.content,
		"instance": instance,
		"form":form,
	}



def post_delete_serie_capitulo(request, slug):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Comentario eliminado")
	return HttpResponseRedirect(instance.get_absolute_url_serie())

from django.utils.timesince import timesince
def responder(request, slug):
	if not request.user.is_active:
		raise Http404
	post = Answerd.objects.all()
	instances = get_object_or_404(Post, slug=slug)
	form = Answereda(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.who_id = request.user.id
			instance.comentario_id = instances.id
			instance.save()
			instances.respuestas.add(instance.id)
			data = {
				'message': "Successfully submitted form data.",
				'perfil':instance.who.profile.perfil_img.url,
				'name':instance.who.username,
				'content':instance.respuesta,
				'fecha':timesince(instance.timestamp).split(', ')[0],
				'id':instances.id,
				'idp':instance.id,
				'fechad':"fecha",
				'token':"%"

			}
			mencion = False
			posicion = 0
			posicion2 = 0
			usergetusername = ""
			for i in instance.respuesta:
				posicion += 1 
				if i == "@":
					mencion = True
					break
				else:
					pass
			if mencion:
				for i in instance.respuesta:
					posicion2 += 1
					if posicion2 >= posicion:
						if not i == " ":
							usergetusername += i
						else:
							break

			if not mencion and not instances.user == request.user:
				comentario = Notificaciones.objects.get(komentario=instances, user_a_notificar=instances.user)
				evenT = Evento(event="respuesta", mensaje=request.user.username + " Ha respondido a tu comentario", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()
			elif mencion:
				mencionado = Usuario.objects.get(username=usergetusername[1:])
				sendnoti = Notificaciones(respm=instance, user_a_notificar=mencionado)
				sendnoti.save()
				comentario = Notificaciones.objects.get(respm=instance, user_a_notificar=mencionado)
				evenT = Evento(event="mencion", mensaje=request.user.username + " Te ha mencionado en una respuesta", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()

			return JsonResponse(data)














def responder_update(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Answerd, id=id)
	form = Answereda(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
				'message': "Respuesta editada.",
				'content':instance.respuesta
			}

			return JsonResponse(data)



def delete_res(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Answerd, id=id)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Respuesta eliminada.",

			}
		return JsonResponse(data)


def post_create_capitulos(request, id):
	if not request.user.is_active:
		raise Http404
	post = Post.objects.all()
	x = []
	for i in post:
		print(i.slug)
		x.append(i.slug)
		
	form = PostForm(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.capitulos_id = id
			if x:
				instance.slug = x[0] +1
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()
				data = {
				'message': "Successfully submitted form data."
			}
				return JsonResponse(data)
			else: 
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()
				data = {
				'message': "Successfully submitted form data."
			}
				return JsonResponse(data)


#actualizar comentario
def post_update_capitulos(request, slug=None):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
				'message': "Successfully submitted form data.",
				'content':instance.content
			}
			return JsonResponse(data)




def post_delete_capitulo(request, slug):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Comentario eliminado.",

			}
		return JsonResponse(data)













def like_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Vote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instance.unvote.all():
				instance.unvote.remove(request.user.id)
			instance.vote.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}
			if not instances.user == request.user:
				comentario = Notificaciones.objects.get(komentario=instances)
				evenT = Evento(event="like", mensaje=request.user.username + " Ha dado like a tu comentario", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()
			return JsonResponse(data)

def unlike_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Vote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.vote.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)

def dislike_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	form = Unvote(request.POST or None, request.FILES or None, instance=instances)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			if request.user in instances.vote.all():
				instance.vote.remove(request.user.id)
			instance.unvote.add(request.user.id)
			instance.save()
			data = {
				'message': "+1"
			}
			return JsonResponse(data)

def outdislike_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = Unvote(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.unvote.remove(request.user.id)
			instance.save()
			data = {
				'message': "-1"
			}
			return JsonResponse(data)

def responder_serie(request, slug):
	if not request.user.is_active:
		raise Http404
	post = Answerd.objects.all()
	instances = get_object_or_404(Post, slug=slug)
	form = Answereda(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.who_id = request.user.id
			instance.comentario_id = instances.id
			instance.save()
			instances.respuestas.add(instance.id)
			data = {
				'message': "Successfully submitted form data.",
				'perfil':instance.who.profile.perfil_img.url,
				'name':instance.who.username,
				'content':instance.respuesta,
				'fecha':timesince(instance.timestamp).split(', ')[0],
				'id':instances.id,
				'idp':instance.id,
				'fechad':"fecha",
				'token':"%"

			}

			mencion = False
			posicion = 0
			posicion2 = 0
			usergetusername = ""
			for i in instance.respuesta:
				posicion += 1 
				if i == "@":
					mencion = True
					break
				else:
					pass
			if mencion:
				for i in instance.respuesta:
					posicion2 += 1
					if posicion2 >= posicion:
						if not i == " ":
							usergetusername += i
						else:
							break

			if not mencion and not instances.user == request.user:
				comentario = Notificaciones.objects.get(komentario=instances, user_a_notificar=instances.user)
				evenT = Evento(event="respuesta", mensaje=request.user.username + " Ha respondido a tu comentario", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()
			elif mencion:
				mencionado = Usuario.objects.get(username=usergetusername[1:])
				sendnoti = Notificaciones(respm=instance, user_a_notificar=mencionado)
				sendnoti.save()
				comentario = Notificaciones.objects.get(respm=instance, user_a_notificar=mencionado)
				evenT = Evento(event="mencion", mensaje=request.user.username + " Te ha mencionado en una respuesta", noti_de_evento=comentario)
				evenT.save()
				evenT.creadores.add(request.user)
				evenT.save()
				comentario.estado.add(evenT)
				comentario.save()
			return JsonResponse(data)

def responder_update_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Answerd, id=id)
	form = Answereda(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
				'message': "Respuesta editada.",
				'content':instance.respuesta
			}

			return JsonResponse(data)

from django.views.decorators.csrf import csrf_protect
@csrf_protect
def delete_res_serie(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Answerd, id=id)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Respuesta eliminada.",

			}
		return JsonResponse(data)














#test



from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .serializers import ComentSerializer


# Create your views here.
def indexa(request):
    return redirect('/inicio/')


# Create your views here.
class ComentViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = ComentSerializer

    # [ GET ] /api/image/randoms/
    @list_route(methods=['get'], url_path='randoms')
    def get_random_image(self, request):
        page = int(request.query_params.get('page'))
        start = (page - 1) * 10
        end = page * 10
        image = Post.objects.all().order_by('-id')[start:end]
        result = ComentSerializer(image, many=True)
        return Response(result.data, status=status.HTTP_200_OK)


def reportes(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Post, id=id)
	reportó = False
	report_user = Reporte.objects.filter(comentario_id=instances).filter(reportador_id=request.user.id)
	if report_user.exists():
		reportó = True

	form = REPORTAR(request.POST or None, request.FILES or None)
	if request.is_ajax() and not report_user.exists():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reportador_id = request.user.id
			instance.comentario_id = instances.id
			instance.save()
			data = {
				'message': "Comentario reportado"
			}
			return JsonResponse(data)        

def reportes_res(request, id):
	if not request.user.is_active:
		raise Http404
	instances = get_object_or_404(Answerd, id=id)
	reportó = False
	report_user = Reporte.objects.filter(respuesta_id=instances).filter(reportador_id=request.user.id)
	if report_user.exists():
		reportó = True

	form = REPORTAR(request.POST or None, request.FILES or None)
	if request.is_ajax() and not report_user.exists():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reportador_id = request.user.id
			instance.respuesta_id = instances.id
			instance.save()
			data = {
				'message': "Reporte enviado"
			}
			return JsonResponse(data)  












#comentario_articulo


def post_create_articulo(request, id):
	if not request.user.is_active:
		raise Http404
	post = Post.objects.all()
	x = []
	for i in post:
		print(i.slug)
		x.append(i.slug)
	form = PostForm(request.POST or None, request.FILES or None)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.articulo_id = id
			if x:
				instance.slug = x[0] +1
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()

				data = {
				'message': "Successfully submitted form data."

			}
				return JsonResponse(data)
			else: 
				instance.save()
				sendnoti = Notificaciones(komentario=instance, user_a_notificar=request.user)
				sendnoti.save()

				data = {
				'message': "Successfully submitted form data."
			}

				return JsonResponse(data)


#actualizar comentario
def post_update_articulo(request, slug=None):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if request.is_ajax():
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			data = {
				'message': "Successfully submitted form data.",
				'content':instance.content
			}
			return JsonResponse(data)




def post_delete_articulo(request, slug):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	if request.is_ajax():
		instance.delete()
		data = {
				'message': "Comentario eliminado.",

			}
		return JsonResponse(data)
