from django import forms
from .models import Post, Answerd, Reporte


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
      