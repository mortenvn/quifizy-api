from django.contrib import admin

from songs.models import Song, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SongAdmin(admin.ModelAdmin):
    list_display = ('spotify_uri', 'name', 'artist',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Song, SongAdmin)
