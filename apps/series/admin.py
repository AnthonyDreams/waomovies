from django.contrib import admin
from apps.series.models import Temporada, Series, Capitulos
# Register your models here.

class CapitulosAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre', 'num_episodio')}

class TemporadasAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre_serie', 'num_temporada')}

class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Temporada, TemporadasAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Capitulos, CapitulosAdmin)