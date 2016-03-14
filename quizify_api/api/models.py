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


#class Round(models.Model):
