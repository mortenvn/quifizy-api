from django.contrib import admin
from api.models import Category, Song

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SongAdmin(admin.ModelAdmin):
    list_display = ('uri',)
