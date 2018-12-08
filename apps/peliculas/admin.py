from django.contrib import admin
from apps.peliculas.models import Peliculas, Trailers, Cast, Personajes, Votacion
# Register your models here.
class PeliculasAdmin(admin.ModelAdmin):
	search_fields = ["titulo"]
	prepopulated_fields = {'slug': ('titulo',)}



admin.site.register(Peliculas, PeliculasAdmin)
admin.site.register(Trailers)
admin.site.register(Cast)
admin.site.register(Personajes)
admin.site.register(Votacion)


