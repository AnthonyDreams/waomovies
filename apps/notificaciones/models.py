from django.db import models
from apps.usuarios.models import *
from apps.series.models import Series
from django.conf import settings
from apps.comentarios.models import Post, Answerd
from django.utils import timesince
from apps.peliculas.models import Peliculas
from apps.series.models import Series, Capitulos
from django.db.models import Sum
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
# Create your models here.

class Notificaciones(models.Model):
	user_a_notificar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	komentario = models.OneToOneField(Post,on_delete=models.CASCADE,  blank=True, related_name="komentario", null=True)
	estado = models.ManyToManyField('Evento', blank=True)
	respm = models.OneToOneField(Answerd,on_delete=models.CASCADE,  blank=True, related_name="respm", null=True)

	def __str__(self):
		if self.komentario.peliculas:
			return self.komentario.peliculas.slug
		elif self.komentario.series:
			return self.komentario.series.slug
		elif self.komentario.capitulos:
			return self.komentario.capitulos.slug

class Evento(models.Model):
	creadores = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True, related_name="generadores")
	status = models.CharField(default="Unread", max_length=10)
	mensaje = models.CharField(max_length=200)
	event = models.CharField(max_length=15)
	noti_de_evento = models.ForeignKey(Notificaciones, on_delete=models.CASCADE)
	timestampe = models.DateTimeField(auto_now=False, auto_now_add=True)
   
	@property
	def unread(self):
		selfa = self.creadores.all()[0]
		img = Usuario.objects.get(email=selfa)
		return Evento.objects.filter(creadores=img, status="Unread").count()

	@property
	def timesince(self):
	    return timesince.timesince(self.timestampe)
	@property
	def userimg(self):
		selfa = self.creadores.all()[0]
		img = Usuario.objects.get(email=selfa)
		return img.profile.perfil_img

	@property
	def slug(self):
		if self.noti_de_evento.komentario:
			try:
				getnoti = self.noti_de_evento
				slug = getnoti.komentario.peliculas.slug
				return slug
			except AttributeError:
				getnoti = self.noti_de_evento
				if getnoti.komentario.capitulos:
					slug = getnoti.komentario.capitulos.slug
					return slug
				else:
					slug = getnoti.komentario.series.slug
					return slug

			

	@property
	def titulon(self):
		if self.noti_de_evento.komentario:
			try:
				gettitulo = self.noti_de_evento
				tituloo = gettitulo.komentario.peliculas.titulo
				return tituloo
			except AttributeError:
				gettitulo = self.noti_de_evento
				if gettitulo.komentario.capitulos:
					tituloo = gettitulo.komentario.capitulos.nombre
					return tituloo + " de " + gettitulo.komentario.capitulos.temporadaa.serie.titulo
				else:
					tituloo = gettitulo.komentario.series.titulo
					return tituloo
		elif self.noti_de_evento.respm:
			try:
				gettitulo = self.noti_de_evento
				tituloo = gettitulo.respm.comentario.peliculas.titulo
				return tituloo
			except AttributeError:
				gettitulo = self.noti_de_evento
				if gettitulo.respm.comentario.capitulos:
					tituloo = gettitulo.respm.comentario.capitulos.nombre
					return tituloo + " de " + gettitulo.respm.comentario.capitulos.temporadaa.serie.titulo
				else:
					tituloo = gettitulo.respm.comentario.series.titulo
					return tituloo
		else:
			return "WaoMovies, \"Esperamos que disfruten de su amistad\""
	@property
	def urlton(self):
		if self.noti_de_evento.komentario:
			try:
				getslugs = self.noti_de_evento
				slusg = getslugs.komentario.peliculas.slug
				return '/peliculas/' + slusg + '/'
			except AttributeError:
				getslugs = self.noti_de_evento
				if getslugs.komentario.capitulos:
					slugt = getslugs.komentario.capitulos.slug
					serie = getslugs.komentario.capitulos.temporadaa.slug
					return "/" + slugt + "/" + serie + "/"
				else:
					getslugs = self.noti_de_evento
					slusg = getslugs.komentario.series.slug
					return '/series/' + slusg + '/'
		elif self.noti_de_evento.respm:
			try:
				getslugs = self.noti_de_evento
				slusg = getslugs.respm.comentario.peliculas.slug
				return '/peliculas/' + slusg + '/'
			except AttributeError:
				getslugs = self.noti_de_evento
				if getslugs.respm.comentario.capitulos:
					slugt = getslugs.respm.comentario.capitulos.slug
					serie = getslugs.respm.comentario.capitulos.temporadaa.slug
					return "/" + slugt + "/" + serie + "/"
				else:
					getslugs = self.noti_de_evento
					slusg = getslugs.respm.comentario.series.slug
					return '/series/' + slusg + '/'
		else:
			return "#"


	def __str__(self):
	    return self.mensaje


class Compartir(models.Model):
	user_who_share = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
	users_to_share = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=False, related_name="user_to_share")
	movie_to_share = models.ForeignKey(Peliculas, null=True, blank=True, on_delete=models.CASCADE)
	serie_to_share = models.ForeignKey(Series, null=True, blank=True, on_delete=models.CASCADE)
	capitulo_to_share = models.ForeignKey(Capitulos, null=True, blank=True, on_delete=models.CASCADE)
	nota = models.CharField(max_length=150, null=True, blank=True)
	timestampc = models.DateTimeField(auto_now=False, auto_now_add=True)
	status = models.CharField(default="Unread", max_length=10)
	mensaje = models.CharField(max_length=200, null=True)
	user_who_read = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_who_read")
	event = models.CharField(max_length=15, null=True)


	@property
	def unread(self):
		selfa = self.user_who_share
		img = Usuario.objects.get(email=selfa)
		sumar = Compartir.objects.filter(users_to_share=get_current_authenticated_user()).exclude(user_who_read=get_current_authenticated_user()).count()


		return sumar


	@property
	def statu(self):
		selfa = self.user_who_read.all()
		if get_current_authenticated_user() in selfa:
			return "Read"
		else:
			return "Unread"
	@property
	def timesince(self):
		return timesince.timesince(self.timestampc)


	@property
	def titulon(self):
		if self.capitulo_to_share:
			tituloo = self.capitulo_to_share
			return tituloo.nombre + " de " + tituloo.temporadaa.serie.titulo

	@property
	def urlton(self):
		if self.movie_to_share:
			getslugs = self.movie_to_share.slug
			return '/peliculas/' + getslugs + '/'
		elif self.serie_to_share:
			getslugs = self.serie_to_share.slug
			return '/series/' + getslugs + '/'
		elif self.capitulo_to_share:
			slugt = self.capitulo_to_share.slug
			serie = self.capitulo_to_share.temporadaa.slug
			return "/" + slugt + "/" + serie + ""


	@property
	def cover(self):
		if self.movie_to_share:
			cover = self.movie_to_share.portada
			if not cover:
				cover = self.movie_to_share.Cover
			return cover
		elif self.serie_to_share:
			cover = self.serie_to_share.portada
			if not cover:
				cover = self.serie_to_share.serie_cover
			return cover
		elif self.capitulo_to_share:
			cover = self.capitulo_to_share.cover_capitulo
			return cover
	@property
	def userimg(self):
		selfa = self.user_who_share
		img = Usuario.objects.get(email=selfa)
		return img.profile.perfil_img