from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Peliculas

class StaticViewSitemap(Sitemap):
	def items(self):
		return ['inicio']

	def location(self, item):
		return reverse(item)





class SnippetsSitemap(Sitemap):

	def items(self):
		return Peliculas.objects.all()