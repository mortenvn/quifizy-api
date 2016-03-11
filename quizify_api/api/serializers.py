from rest_framework import serializers

from api.models import Category, Song

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    songs = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'songs')

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'spotify_uri')
