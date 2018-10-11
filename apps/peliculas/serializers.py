from rest_framework.serializers import ModelSerializer
from .models import *
from apps.comentarios.models import *
from apps.vermas_tarde.models import *
from rest_framework import serializers
from apps.series.models import Series

class peliserializer(ModelSerializer):

	class Meta:
		model = Peliculas
		fields = ('titulo', 'director', 'fecha_de_lanzamiento', 'Cover', 'id', 'slug')

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