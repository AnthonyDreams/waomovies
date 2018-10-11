
from django.contrib import admin

# Register your models here.
from .models import *

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["content", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_editable = ["content"]
	list_filter = ["updated", "timestamp"]

	search_fields = ["content"]
	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)
admin.site.register(Answerd)
admin.site.register(Reporte)
