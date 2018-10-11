from django.db import models

# Create your models here.

class contact(models.Model):
	subject = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	content = models.TextField()
