from django.contrib import admin
from accounts.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Player, PlayerAdmin)
