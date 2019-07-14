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
from ww import f
from .utils import get_read_time
from apps.series.models import Series
from googletrans import Translator
from django.db.models.signals import post_save
import http.client
import json
from django.dispatch import receiver




class Peliculas(models.Model):
	theid = models.IntegerField(null=True, unique=True, blank=True)
	Cover = models.ImageField(upload_to='static', height_field=None, width_field=None)
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
	genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
	genero2 = models.CharField(max_length=20, choices=GENERO_CHOICES,blank=True, null=True)
	genero3 = models.CharField(max_length=20, choices=GENERO_CHOICES,blank=True, null=True)
	director = models.CharField(max_length=60)
	pais = models.CharField(max_length=20)
	links = models.TextField(blank=True, null=True)
	portada = models.ImageField(upload_to='static', height_field=None, width_field=None, blank=True)
	
	fecha_de_lanzamiento = models.DateField(blank=True, null=True)
	reparto = models.ManyToManyField('Personajes', blank=True)
	
	
	sinopsis = models.TextField(blank=True, null=True)
	puntuacion = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
	CoverImg =models.ImageField(upload_to='static/comprimidas', height_field=None, width_field=None, null=True, blank=True)
	
	PortadaImg = models.ImageField(upload_to='', height_field=None, width_field=None, blank=True, null=True)
	run_time = models.IntegerField(default=0, blank=True, null=True)
	titulo = models.CharField(max_length=200, blank=True, null=True)
	titulo_orinal = models.CharField(max_length=150, null=True, blank=True)

	tag_principal = models.CharField(max_length=40, blank=True)
	tema = models.CharField(max_length=40, blank=True)
	tag1 = models.CharField(max_length=40, blank=True)
	tag2 = models.CharField(max_length=40, blank=True)
	tag3 = models.CharField(max_length=40, blank=True)
	otras_etiquetas_y_busquedas = models.ManyToManyField('Busqueda_y_etiquetas', blank=True, related_name="otras_etiquetas_y_busquedas")
	reportes = models.IntegerField(default=0)
	favoritos = models.ManyToManyField(Usuario, blank=True, related_name="favoritos")
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

	slug = models.SlugField(unique=True, max_length=200,blank=True, null=True)
	class Meta:
		verbose_name_plural = "Películas"


	def __str__(self):
		if self.titulo:
			return self.titulo
		else:
			return str(self.theid)

	def get_absolute_url(self):
		return f('/{self.slug}/')


	@property
	def Coverimg(self):
		if self.CoverImg:
			return "https://d3mp3oxoqwxddf.cloudfront.net/media/static/comprimidas/compress_" + str(self.CoverImg)
		else:
			return self.Cover.url
	@property
	def Portadaimg(self):
		if self.PortadaImg:
			return "https://d3mp3oxoqwxddf.cloudfront.net/media/static/comprimidas/compress_" + str(self.PortadaImg)
		else:
			return self.portada.url
	@property
	def crear_pelicula_theid(self):
		if not self.titulo:
			conn = http.client.HTTPSConnection("api.themoviedb.org")
			payload = "{}"

			conn.request("GET", "/3/movie/"+str(self.theid)+"?language=es&api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)

			res = conn.getresponse()
			data = res.read()
			creadores = ""
			converted = json.loads(data.decode("utf-8"))

			fecha = converted["release_date"].split("-")
			sinopsiss = converted["overview"]
			original = converted["original_title"]
			nombre = converted["title"]
			votos = converted["vote_average"]
			run = converted["runtime"]
			fecha_de_lanzamientoo = datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]))

			self.fecha_de_lanzamiento = fecha_de_lanzamientoo
			self.sinopsis = sinopsiss
			self.titulo_original = original
			self.titulo = nombre
			self.puntuacion = votos
			self.run_time = run
			self.slug = slugify(nombre)
			conn.request("GET", "/3/movie/"+str(self.theid)+"/keywords?api_key=8bfa262e8f8c8848076b3494155c8c2a", payload)
			res = conn.getresponse()
			data = res.read()
			converted = json.loads(data.decode("utf-8"))
			maximo = 6
			key = []
			for a in range(0, len(converted["keywords"])):
				if a < 9:
					key.append(converted["keywords"][a]["name"]);
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

@receiver(post_save, sender=Peliculas)
def create_pelicula(sender, instance, created, **kwargs):
	if created:
		
		instance.crear_pelicula_theid

def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if instance.Cover:
        view_time_var = get_read_time(instance.Cover)
        instance.view_time = view_time_var


pre_save.connect(pre_save_post_receiver, sender=Peliculas)

class Trailers(models.Model):
	titulo = models.CharField(max_length=50)
	trailer_cover = models.ImageField(upload_to='static', height_field=None, width_field=None)
	links = models.TextField()
	fecha_de_subida = models.DateField(default=timezone.now)

	class Meta:
		verbose_name_plural = "Trailers"

	def __str__(self):
		return self.titulo

class Cast(models.Model):
	full_name = models.CharField(max_length=50) 
	personaje_fname = models.ManyToManyField('Personajes', blank=True, related_name="actor")
	def __str__(self):
		return self.full_name

class Personajes(models.Model):
	personaje= models.CharField(max_length=70, blank=True)
	

	def __str__(self):
		return self.personaje

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
	pelicula = models.ForeignKey(Peliculas, on_delete=models.CASCADE)
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	votacion = models.DecimalField(choices=PUNTOS, max_digits=5, decimal_places=1, blank=True, null=True)
	publish = models.DateField(auto_now=True, auto_now_add=False, null=True)

	def __str__(self):
		return str(self.votacion)

	def get_absolute_url(self):
		return reverse("peliculasO", kwargs={"slug": self.pelicula.slug})


class Hitcount(models.Model):
	hitcount = models.IntegerField(default=0)
	hitcount_ever = models.IntegerField(default=0)
	publish = models.DateField(auto_now=False, auto_now_add=True)
	pelicula = models.ForeignKey(Peliculas, on_delete=models.CASCADE)
	expired = models.DateTimeField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return str(self.pelicula)



class Generox(models.Model):
	accion = models.ManyToManyField(Usuario, related_name="action")
	ciencia_ficcion = models.ManyToManyField(Usuario, related_name="science_fiction")
	romance = models.ManyToManyField(Usuario, related_name="romance")
	drama = models.ManyToManyField(Usuario, related_name="drama")
	terror = models.ManyToManyField(Usuario, related_name="terror")
	crimen = models.ManyToManyField(Usuario, related_name="cryme")
	aventura = models.ManyToManyField(Usuario, related_name="adventure")
	animacion = models.ManyToManyField(Usuario, related_name="animation")
	comedia = models.ManyToManyField(Usuario, related_name="comedy")
	documental = models.ManyToManyField(Usuario, related_name="documental")
	fantasia = models.ManyToManyField(Usuario, related_name="fantasy")
	suspenso = models.ManyToManyField(Usuario, related_name="suspense")


	genero_name = models.CharField(max_length=40, null=True, unique=True)


class Busqueda_y_etiquetas(models.Model):
	tag = models.CharField(max_length=80, blank=True,null=True)
	timestamp_tag = models.DateTimeField(auto_now=False, auto_now_add=True)
	user_who_search = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
	resuelto = models.BooleanField(default=False)
	def __str__(self):
		return str(self.tag)


class solicitar(models.Model):
	solicitado = models.CharField(max_length=150, unique=True)
	solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True) 
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)