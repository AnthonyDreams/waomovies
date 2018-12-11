from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
from datetime import datetime

from apps.usuarios.models import Usuario
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Create your models here.


class Temporada(models.Model):
	serie = models.ForeignKey('Series', on_delete=models.CASCADE, null=True)
	temporada_name = models.CharField(max_length=14)
	capitulos = models.ManyToManyField('Capitulos', blank=True)
	nombre_serie = models.CharField(max_length=20, blank=True)
	num_temporada = models.IntegerField(blank=True, null=True)
	slug = models.SlugField(null=True)
	on = models.ManyToManyField(Usuario, related_name="on")
	def __str__(self):
		return self.serie.titulo + " " + self.temporada_name

class Series(models.Model):
	titulo = models.CharField(max_length=30)
	ACCION = 'ACC'
	DRAMA = 'DRA'
	CIENCIA_FICCION = 'SC'
	SUSPENSO = 'SUS'
	TERROR = 'TER'
	CRIMEN = 'CRI'
	AVENTURA = 'AVEN'
	ANIMACION = 'ANI'
	COMEDY = 'COME'
	DOCUMENTAL = 'DOCU'
	ROMANCE = 'ROM'
	FANTASIA = 'FANT'

	GENERO_CHOICES = (
		(ACCION, 'Acción'),
		(DRAMA, 'Drama'),
		(CIENCIA_FICCION, 'Ciencia_Ficción'),
		(TERROR, 'Terror'),
		(SUSPENSO, 'Suspenso'),
		(CRIMEN, 'Crimen'),
		(AVENTURA, 'Aventura'),
		(ANIMACION, 'Animación'),
		(COMEDY, 'Comedia'),
		(DOCUMENTAL, 'Documental'),
		(ROMANCE, 'Romance'),
		(FANTASIA, 'Fantasia'),

	)
	genero = models.CharField(
		max_length=20,
		choices=GENERO_CHOICES,
		default=ACCION,
	)
	genero2 = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True, null=True)

	reparto = models.ManyToManyField('peliculas.personajes', blank=True, related_name='reparto_serie')
	sinopsis = models.TextField()
	fecha_de_lanzamiento = models.DateField()
	fecha_de_publicacion = models.DateField(default=timezone.now)
	trailer_link = models.TextField(null=True, blank=True)
	serie_cover = models.ImageField(upload_to='static', height_field=None, width_field=None)
	tem = models.ManyToManyField('Temporada', blank=True)
	portada = models.ImageField(upload_to='static', height_field=None, width_field=None, blank=True, null=True)
	puntuacion = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
	palabra_clave = models.CharField(max_length=20, blank=True)
	director = models.CharField(max_length=30, blank=True)
	pais = models.CharField(max_length=40, null=True)
	tag1 = models.CharField(max_length=20, blank=True)
	tag2 = models.CharField(max_length=20, blank=True)
	tag3 = models.CharField(max_length=20, blank=True)
	reportes = models.IntegerField(default=0)
	favoritos = models.ManyToManyField(Usuario, blank=True, related_name="favoritos")


	tema = models.CharField(max_length=20, blank=True)

	reportes = models.IntegerField(default=0)


	favoritos = models.ManyToManyField(Usuario, blank=True, related_name="favoritos_series")
	
	emision = models.BooleanField(default=False)
	slug = models.SlugField(max_length=200, blank=True, unique=True)

	def __str__(self):
		return self.titulo
	def get_absolute_url(self):
		return reverse("series_detail", kwargs={"slug": self.slug})

class Capitulos(models.Model):
	nombre = models.CharField(max_length=30)
	cover_capitulo = models.ImageField(upload_to='static', height_field=None, width_field=None)
	sinopsis = models.CharField(max_length=305)
	links = models.TextField(blank=True)
	num_episodio = models.IntegerField(blank=True, null=True)
	temporadaa = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="temporada_del_capitulo", null=True)
	slug = models.SlugField(max_length=200, blank=True, unique=True)
	vote_capitulo = models.ManyToManyField(Usuario, related_name="vote_capitulo", blank=True)
	unvote_capitulo= models.ManyToManyField(Usuario, related_name="unvote_capitulo", blank=True)
	reportes = models.IntegerField(default=0, blank=True)
	rapidvideo = models.TextField(null=True, blank=True)
	vidlox = models.TextField(null=True, blank=True)
	vidoza = models.TextField(null=True, blank=True)
	openload = models.TextField(null=True, blank=True)
	streamago = models.TextField(null=True, blank=True)
	streamcloud = models.TextField(null=True, blank=True)
	servidor1 = models.TextField(null=True, blank=True)
	servidor2 = models.TextField(null=True, blank=True)
	servidor3 = models.TextField(null=True, blank=True)
	servidor4 = models.TextField(null=True, blank=True)
	def _get_unique_slug(self):
		slug = slugify(self.temporadaa.nombre_serie + "-" + self.temporadaa.num_temporada + "x" + self.num_episodio)
		unique_slug = slug
		num = 1
		while Capitulos.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug
 
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("capitulos_detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.nombre


class Votacion(models.Model):
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
	series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="series_id",null=True)
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="user_votacion_serie")
	votacion = models.DecimalField(choices=PUNTOS, max_digits=5, decimal_places=1, blank=True, null=True)
	capitulos = models.ForeignKey(Capitulos, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return str(self.votacion)

	def get_absolute_url(self):
		return reverse("series_detail", kwargs={"slug": self.series.slug})

	

class Hitcount_Series(models.Model):
	hitcount = models.IntegerField(default=0)
	hitcount_ever = models.IntegerField(default=0)
	publish = models.DateField(auto_now=False, auto_now_add=True)
	serie = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
	expired = models.DateTimeField(auto_now=False, auto_now_add=False)
	capitulo = models.ForeignKey(Capitulos, on_delete=models.CASCADE, null=True)


	def __str__(self):
		if self.serie:
			return str(self.serie)
		if self.capitulo:
			return str(self.capitulo)