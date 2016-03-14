from django.contrib import admin
from api.models import Category, Song, Game

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SongAdmin(admin.ModelAdmin):
    list_display = ('spotify_uri',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('player1','player2','invitation_status',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Game, GameAdmin)
