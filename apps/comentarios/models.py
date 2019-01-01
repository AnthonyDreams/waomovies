from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from apps.peliculas.models import Peliculas
from apps.series.models import Series, Capitulos
from apps.news.models import Article
from django.utils.text import slugify
# Create your models here.
# MVC MODEL VIEW CONTROLLER


#Post.objects.all()
#Post.objects.create(user=user, title="Some time")

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		# Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	#filebase, extension = filename.split(".")
	#return "%s/%s.%s" %(instance.id, instance.id, extension)
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	peliculas = models.ForeignKey(Peliculas, on_delete=models.CASCADE, null=True)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	publish = models.DateField(auto_now=True, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	slug = models.IntegerField(unique=True, blank=False, default=0)
	series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
	capitulos = models.ForeignKey(Capitulos, on_delete=models.CASCADE, null=True, blank=True)
	articulo = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
	respuestas = models.ManyToManyField('Answerd', blank=True)
	vote = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True, related_name="vote")
	unvote = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True, related_name="unvote")
   
	
	objects = PostManager()

	def __unicode__(self):
		return self.content

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return reverse("peliculasO", kwargs={"slug": self.peliculas.slug})
	def get_absolute_url_serie(self):
		return reverse("series_detail", kwargs={"slug": self.series.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]

class Answerd(models.Model):
	comentario = models.ForeignKey(Post, on_delete=models.CASCADE)
	who = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	respuesta = models.TextField(max_length=400)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	

class Reporte(models.Model):
	reportador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	SPO = 'Spoiler'
	INA = 'Muestra odio o violencia'
	SPAM = 'Spam o Contenido comercial'
	


	Reporte = (
		(SPO, 'Spoiler'),
		(INA, 'Muestra odio o violencia'),
		(SPAM, 'Spam o Contenido comercial'),
		
	)
	reportar = models.CharField(max_length=60, choices=Reporte)
	comentario = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	respuesta = models.ForeignKey(Answerd, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.reportar