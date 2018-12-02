from django import forms
from .models import Compartir
from django.forms.widgets import CheckboxSelectMultiple
from apps.usuarios.models import Usuario

class ShareForm(forms.ModelForm):


	class Meta:
		model = Compartir
		fields = [
			"nota",
		]

	def clean_data(self):
		notaa = self.cleaned_data.get('nota')
