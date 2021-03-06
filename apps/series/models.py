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
import http.client
import json
from googletrans import Translator
from django.db.models.signals import post_save

from django.dispatch import receiver



# Create your models here.


class Temporada(models.Model):
	serie = models.ForeignKey('Series', on_delete=models.CASCADE, null=True)
	temporada_name = models.CharField(max_length=14)
	capitulos = models.ManyToManyField('Capitulos', blank=True)
	nombre_serie = models.CharField(max_length=100, blank=True)
	num_temporada = models.IntegerField(blank=True, null=True)
	slug = models.SlugField(null=True)
	on = models.ManyToManyField(Usuario, related_name="on", blank=True)
	@property
	def foo(self):
		return self.serie.titulo + " " + self.temporada_name
	
	def __str__(self):
		return self.serie.titulo + " " + self.temporada_name

class Series(models.Model):
	theid = models.IntegerField(null=True, unique=True, blank=True)
	serie_cover = models.ImageField(upload_to='static', height_field=None, width_field=None)
	portada = models.ImageField(upload_to='static', height_field=None, width_field=None, blank=True, null=True)
	pais = models.CharField(max_length=40, null=True)

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
	genero3 = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True, null=True)
	titulo = models.CharField(max_length=100, blank=True, null=True)
	titulo_original = models.CharField(max_length=100, null=True,blank=True)
	

	reparto = models.ManyToManyField('peliculas.personajes', blank=True, related_name='reparto_serie')
	sinopsis = models.TextField(blank=True, null=True)
	fecha_de_lanzamiento = models.DateField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	trailer_link = models.TextField(null=True, blank=True)
	CoverImg =models.ImageField(upload_to='', height_field=None, width_field=None, blank=True, null=True)
	tem = models.ManyToManyField('Temporada', blank=True)
	PortadaImg = models.ImageField(upload_to='', height_field=None, width_field=None, blank=True, null=True)
	puntuacion = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
	director = models.CharField(max_length=500, blank=True, null=True)
	tema = models.CharField(max_length=100, blank=True, null=True)
	palabra_clave = models.CharField(max_length=100, blank=True, null=True)
	tag1 = models.CharField(max_length=100, blank=True, null=True)
	tag2 = models.CharField(max_length=100, blank=True, null=True)
	tag3 = models.CharField(max_length=100, blank=True, null=True)
	tag4 = models.CharField(max_length=100, blank=True, null=True)
	tag5 = models.CharField(max_length=100, blank=True, null=True)
	tag6 = models.CharField(max_length=100, blank=True, null=True)
	tag7 = models.CharField(max_length=100, blank=True, null=True)
	otras_etiquetas_y_busquedas = models.ManyToManyField('Busqueda_y_etiquetas_series', blank=True, related_name="otras_etiquetas_y_busquedas")
	reportes = models.IntegerField(default=0)
	favoritos = models.ManyToManyField(Usuario, blank=True, related_name="favoritos")


	

	reportes = models.IntegerField(default=0)


	favoritos = models.ManyToManyField(Usuario, blank=True, related_name="favoritos_series")
	
	emision = models.BooleanField(default=False)
	slug = models.SlugField(max_length=200, blank=True, unique=True)

	def __str__(self):
		if self.titulo:
			return self.titulo
		else:
			return str(self.theid)
	def get_absolute_url(self):
		return reverse("series_detail", kwargs={"slug": self.slug})
	@property	
	def crear_serie_theid(self):
		if not self.director:
			conn = http.client.HTTPSConnection("api.themoviedb.org")
			payload = "{}"

			conn.request("GET", "/3/tv/"+str(self.theid)+"?language=es&api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)

			res = conn.getresponse()
			data = res.read()
			creadores = ""
			converted = json.loads(data.decode("utf-8"))
			for i in range(0,len(converted["created_by"])):
				if i != len(converted["created_by"]) - 1:
					creadores += converted["created_by"][i]["name"] + " / "
				else:
					creadores += converted["created_by"][i]["name"]

			fecha = converted["first_air_date"].split("-")
			sinopsiss = converted["overview"]
			original = converted["original_name"]
			nombre = converted["name"]
			votos = converted["vote_average"]
			emicion = converted["in_production"]
			fecha_de_lanzamientoo = datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]))

			self.fecha_de_lanzamiento = fecha_de_lanzamientoo
			self.sinopsis = sinopsiss
			self.titulo_original = original
			self.titulo = nombre
			self.puntuacion = votos
			self.emision = emicion
			self.director = creadores
			self.slug = slugify(nombre)
			conn.request("GET", "/3/tv/"+str(self.theid)+"/keywords?api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
			res = conn.getresponse()
			data = res.read()
			converted = json.loads(data.decode("utf-8"))
			maximo = 6
			key = []
			for a in range(0, len(converted["results"])):
				if a < 9:
					key.append(converted["results"][a]["name"]);
				else:
					break;


			gs = Translator()
			count = 0
			for i in key:
				count +=1
				keyp = gs.translate(i, dest="es").text
				dos = ""
				for i in keyp:
					if i == " ":
						i == "_"
					dos += i
					
				if count == 1:
					self.palabra_clave = dos
				if count == 2:
					self.tema =	dos
				if count == 3:
					self.tag1 =	dos
				if count == 4:
					self.tag2 =	dos
				if count == 5:
					self.tag3 =	dos
				if count == 6:
					self.tag4 =	dos
				if count == 7:
					self.tag5 =	dos
				if count == 8:
					self.tag6 =	dos
				if count == 9:
					self.tag7 =	dos
			self.save()

			return "Done"

@receiver(post_save, sender=Series)
def create_serie(sender, instance, created, **kwargs):
	if created:
		
		instance.crear_serie_theid


class Capitulos(models.Model):
	nombre = models.CharField(max_length=100)
	cover_capitulo = models.ImageField(upload_to='static', height_field=None, width_field=None)
	sinopsis = models.CharField(max_length=2000)
	fecha_de_lanzamiento = models.DateField(null=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
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
		return self.nombre + " - " + self.temporadaa.foo


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


class Busqueda_y_etiquetas_series(models.Model):
	tag = models.CharField(max_length=80, blank=True,null=True)
	timestamp_tag = models.DateTimeField(auto_now=False, auto_now_add=True)
	user_who_search = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
	resuelto = models.BooleanField(default=False)
	def __str__(self):
		return str(self.tag)