from django import forms
from .models import Post, Answerd, Reporte
from apps.notificaciones.models import Evento

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"content",
		]

class Answereda(forms.ModelForm):
	class Meta:
		model = Answerd
		fields = ["respuesta"]


class Vote(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"vote",
		]

class Unvote(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"unvote",
  


	  ]

class REPORTAR(forms.ModelForm):
	



	class Meta:
	        model = Reporte
	        fields = [
	            "reportar",
	        ]
      


class Noti(forms.ModelForm):
	class Meta:
		model = Evento
		fields = [
			"status",
			"event",
			"mensaje",
  


	  ]
