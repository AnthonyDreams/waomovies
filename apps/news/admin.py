from django.contrib import admin
from .models import Article, NewsTags, NewsMedia

class ArticleAdmin(admin.ModelAdmin):
	search_fields = ["titulo"]
	prepopulated_fields = {'slug_search': ('titulo',)}

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(NewsTags)
admin.site.register(NewsMedia)