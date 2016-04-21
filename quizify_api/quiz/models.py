from __future__ import unicode_literals
from django.db import models

from accounts.models import Player
from songs.models import Song, Category


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
    game = models.ForeignKey(Game, related_name='rounds')

    STATUS_TYPES = (
        ('active', 'active'),
        ('completed', 'completed'),
    )

    status = models.CharField(max_length=20, choices=STATUS_TYPES)
    whos_turn = models.ForeignKey(Player, related_name='whos_turn', blank=True, null=True)
    winner = models.ForeignKey(Player, related_name='winner', blank=True, null=True)
    player1_score = models.IntegerField(blank=True, null=True)
    player2_score = models.IntegerField(blank=True, null=True)


class Question(models.Model):
    round = models.ForeignKey(Round, related_name='questions')
    correct_answer = models.ForeignKey(Song, related_name='correct_answer')
    alternatives = models.ManyToManyField(Song, related_name='alternatives')
