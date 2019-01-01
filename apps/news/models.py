from django.db import models
from apps.peliculas.models import Peliculas
from apps.series.models import Series
from apps.usuarios.models import Usuario
from .utils import rand_slug
from django.db.models.signals import pre_save
# Create your models here.


class Article(models.Model):
	titulo = models.CharField(max_length=50)
	cover = models.ImageField(upload_to='static', height_field=None, width_field=None, max_length=100)
	detail = models.CharField(max_length=140, null=True)
	contenido = models.TextField()
	tags = models.ManyToManyField('NewsTags', related_name="tags", blank=True)
	media = models.ManyToManyField('NewsMedia', related_name='media', blank=True)
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
	pelicula = models.ForeignKey(Peliculas, on_delete=models.CASCADE, null=True, blank=True)
	serie = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
	slug = models.CharField(max_length=8, unique=True, null=True, blank=True)
	publish = models.DateField(auto_now=True, auto_now_add=False)
	slug_search = models.SlugField(null=True)
	NOT = 'Noticias'
	REV = 'Critica'
	GLOB = 'Global'
	CATEGORIES_CHOICES = (
		(NOT, 'Noticias'),
		(REV, 'Crítica'),
		(GLOB, 'Global'),
	)		

	categoria = models.CharField(max_length=20, choices=CATEGORIES_CHOICES, null=True)
	def __str__(self):
		return self.titulo


def slug_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = rand_slug(instance)

pre_save.connect(slug_save, sender=Article)

class NewsTags(models.Model):
	tag = models.CharField(max_length=50)

	def __str__(self):
		return self.tag

class NewsMedia(models.Model):
	titulo = models.CharField(max_length=50)
	video = models.FileField(upload_to='videos/', null=True, verbose_name="", blank=True)
	img = models.ImageField(upload_to='static', height_field=None, width_field=None, max_length=100, null=True, blank=True)
	embed = models.TextField(null=True, blank=True)
	detail = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.titulo


class Votacion_Articulos(models.Model):
	uno = 1
	uno_y_medio = 1.5
	dos = 2
	dos_y_medio = 2.5
	tres = 3
	tres_y_medio = 3.5
	cuatro = 4
	cuatro_y_medio = 4.5
	cinco = 5

	PUNTOS = (
		(uno, 'uno'),
		(uno_y_medio, 'uno_y_medio'),
		(dos, 'dos'),
		(dos_y_medio, 'dos_y_medio'),
		(tres, 'tres'),
		(tres_y_medio, 'tres_y_medio'),
		(cuatro, 'cuatro'),
		(cuatro_y_medio, 'cuatro_y_medio'),
		(cinco, 'cinco'),

	)
	articulo = models.ForeignKey(Article, on_delete=models.CASCADE)
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	votacion = models.DecimalField(choices=PUNTOS, max_digits=5, decimal_places=1, blank=True, null=True, default=1)
	publish = models.DateField(auto_now=True, auto_now_add=False, null=True)

	def __str__(self):
		return str(self.votacion)

	def get_absolute_url(self):
		return reverse("peliculasO", kwargs={"slug": self.articulo.slug})


class Hitcount_Articulos(models.Model):
	hitcount_day = models.IntegerField(default=0)
	hitcount_week = models.IntegerField(default=0)
	hitcount_month = models.IntegerField(default=0)
	hitcount_ever = models.IntegerField(default=0)
	publish = models.DateField(auto_now=False, auto_now_add=True)
	articulo = models.ForeignKey(Article, on_delete=models.CASCADE)
	expired_day = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
	expired_month = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
	expired_week = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
