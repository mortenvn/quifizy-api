from __future__ import unicode_literals

from django.db import models

from accounts.models import Player

class Song(models.Model):
    spotify_uri = models.CharField(max_length=22)

    def __unicode__(self):
        return self.spotify_uri

class Category(models.Model):
    """
    Super nice documentation
    """
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

class Game(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1')
    player2 = models.ForeignKey(Player, related_name='player2')

    INVITATION_STATUS_TYPES = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )

    invitation_status = models.CharField(max_length=20, choices=INVITATION_STATUS_TYPES)


class Round(models.Model):
    category = models.ForeignKey(Category)

    STATUS_TYPES = (
        ('active', 'active'),
        ('completed', 'completed'),
    )

    status = models.CharField(max_length=20, choices=STATUS_TYPES)
    whos_turn = models.ForeignKey(Player, related_name='whos_turn')
    winner = models.ForeignKey(Player, related_name='winner')

class Score(models.Model):
    player = models.ForeignKey(Player)
    answer_time = models.DurationField()
    answered_correctly = models.BooleanField()

class Question(models.Model):
    round = models.ForeignKey(Round)
    correct_answer = models.ForeignKey(Song, related_name='correct_answer')
    alternatives = models.ManyToManyField(Song, related_name='alternatives')
    score_player1 = models.ForeignKey(Score, related_name='score_player1')
    score_player2 = models.ForeignKey(Score, related_name='score_player2')
