from __future__ import unicode_literals

from django.db import models

class Song(models.Model):
    spotify_uri = models.CharField(max_length=22)
    name = models.CharField(max_length=100, blank=True, null=True)
    artist = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.spotify_uri


class Category(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name
