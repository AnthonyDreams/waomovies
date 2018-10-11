from django import forms
from .models import *


class votacion(forms.ModelForm):
    class Meta:
        model = Votacion
        fields = [
            "votacion",
            "pelicula"
        ]

class reporte(forms.ModelForm):
    class Meta:
        model = Peliculas
        fields = [
            "reportes",
        ]



class Favoritos(forms.ModelForm):
    class Meta:
        model = Peliculas
        fields = [
            "favoritos",
        ]

class count(forms.ModelForm):
    class Meta:
        model = Hitcount
        fields = [
            "hitcount",
        ]