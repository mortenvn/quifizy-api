from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Super nice documentation
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    spotify_uri = models.CharField(max_length=22)
    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.spotify_uri
