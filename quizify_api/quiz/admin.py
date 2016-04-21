from django.contrib import admin
from quiz.models import *


class GameAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'invitation_status',)


class RoundAdmin(admin.ModelAdmin):
    list_display = ('category', 'status', 'whos_turn', 'winner',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('round', 'correct_answer',)

admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Question, QuestionAdmin)
