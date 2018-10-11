from django import forms
from .models import *


class votacion(forms.ModelForm):
    class Meta:
        model = Votacion
        fields = [
            "votacion",
        ]

class reporte(forms.ModelForm):
    class Meta:
        model = Series
        fields = [
            "reportes",
        ]


class Favoritos(forms.ModelForm):
    class Meta:
        model = Series
        fields = [
            "favoritos",
        ]

class count_series(forms.ModelForm):
    class Meta:
        model = Hitcount_Series
        fields = [
            "hitcount",
        ]
class TemporadA(forms.ModelForm):
    class Meta:
        model = Temporada
        fields = [
            "id",
        ]

class Vote_capi(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = [
            "vote_capitulo",
        ]

class Unvote_capi(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = [
            "unvote_capitulo",
        ]

class reporte_cap(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = [
            "reportes",
        ]