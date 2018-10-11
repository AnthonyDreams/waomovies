from django.db import models
from apps.peliculas.models import Peliculas
from apps.series.models import Series
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
class Vermastarde(models.Model):
	fecha = models.DateTimeField(default=timezone.now)
	series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
	peliculas = models.ForeignKey(Peliculas, on_delete=models.CASCADE, null=True, blank=True, related_name="peliculas")
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, unique=False)

	def get_absolute_url(self):
		return reverse("peliculasO", kwargs={"id": self.peliculas.id})

	def get_absolute_url_serie(self):
		return reverse("series_detail", kwargs={"id": self.series.id})


	def __str__(self):
		return str(self.fecha)