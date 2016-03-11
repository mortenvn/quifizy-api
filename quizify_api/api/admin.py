from django.contrib import admin
from api.models import Category, Song

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SongAdmin(admin.ModelAdmin):
    list_display = ('spotify_uri',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Song, SongAdmin)
