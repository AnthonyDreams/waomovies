from django import forms
from .models import *


class votacion_articulo(forms.ModelForm):
    class Meta:
        model = Votacion_Articulos
        fields = [
            "votacion",
        ]


class count_articulo(forms.ModelForm):
    class Meta:
        model = Hitcount_Articulos
        fields = [
            "hitcount_day",
			"hitcount_week",
			"hitcount_month",
			"hitcount_ever",
        ]