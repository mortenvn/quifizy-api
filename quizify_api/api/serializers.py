from rest_framework import serializers

from api.models import Category, Song


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'spotify_uri')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # songs = serializers.StringRelatedField(many=True)
    songs = SongSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'songs')
