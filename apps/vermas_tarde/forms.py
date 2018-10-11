from django import forms
from .models import *


class Fechas(forms.ModelForm):
    class Meta:
        model = Vermastarde
        fields = [
            "id",
        ]