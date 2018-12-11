from rest_framework.serializers import ModelSerializer
from .models import *
from apps.comentarios.models import *
from apps.vermas_tarde.models import *
from rest_framework import serializers
from apps.series.models import Series
from apps.notificaciones.models import Notificaciones, Evento, Compartir
from apps.usuarios.models import Profile

class peliserializer(ModelSerializer):

	class Meta:
		model = Peliculas
		fields = ('titulo', 'director', 'fecha_de_lanzamiento', 'Cover', 'id', 'slug', 'puntuacion')

class notizerializer(ModelSerializer):
	unread = serializers.IntegerField()
	timesince = serializers.DateTimeField()
	userimg = serializers.ImageField()
	slug = serializers.CharField()
	titulon = serializers.CharField()
	urlton = serializers.CharField()

	class Meta:
		model = Evento
		fields = ('status', 'mensaje', 'event', 'timestampe', 'id', 'unread', 'timesince', 'userimg', 'slug', 'titulon', 'urlton')

class Friends(ModelSerializer):
	superamigos = serializers.CharField()

	class Meta:
		model = Profile
		fields = ('superamigos', 'perfil_img',)

class Comparitapi(ModelSerializer):
	unread = serializers.IntegerField()
	timesince = serializers.DateTimeField()
	titulon = serializers.CharField()
	urlton = serializers.CharField()
	userimg = serializers.ImageField()
	cover = serializers.ImageField()
	statu = serializers.CharField()




	class Meta:
		model = Compartir
		fields = ('titulon', 'nota', 'timesince', 'urlton', 'mensaje', 'unread', 'userimg', 'statu', 'cover')

class serieserializer(ModelSerializer):

	class Meta:
		model = Series
		fields = ('titulo', 'director', 'fecha_de_lanzamiento', 'serie_cover', 'id', 'slug')

class pelisnoveerializer(ModelSerializer):

	class Meta:
		model = Peliculas
		fields = ('titulo', 'director', 'fecha_de_lanzamiento', 'Cover', 'id','slug')


class COMENTARIOS(ModelSerializer):

	class Meta:
		model = Post
		fields = ('content',)
class SEGUIRYVER(serializers.ModelSerializer):
	peliculas = serializers.StringRelatedField(many=True)

	class Meta:
		model = Vermastarde
		fields = ('series', 'peliculas')