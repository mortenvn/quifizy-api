from django.contrib import admin
from api.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SongAdmin(admin.ModelAdmin):
    list_display = ('spotify_uri',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('player1','player2','invitation_status',)

class RoundAdmin(admin.ModelAdmin):
    list_display = ('category', 'status', 'whos_turn', 'whos_turn', 'winner',)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'answer_time', 'answered_correctly',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('round', 'correct_answer', 'score_player1', 'score_player2',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Question, QuestionAdmin)
