from rest_framework import serializers

from songs.models import Category, Song
from quiz.models import *
from accounts.serializers import PlayerSerializer


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'spotify_uri', 'name', 'artist', 'url')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'songs')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    correct_answer = SongSerializer()
    alternatives = SongSerializer(many=True)

    class Meta:
        model = Question
        fields = ('correct_answer', 'alternatives')


class RoundSerializer(serializers.HyperlinkedModelSerializer):
    whos_turn = PlayerSerializer()
    winner = PlayerSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Round
        fields = ('id', 'status', 'whos_turn', 'winner', 'category', 'questions', 'player1_score', 'player2_score')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    player1 = PlayerSerializer()
    player2 = PlayerSerializer()
    rounds = RoundSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'player1', 'player2', 'invitation_status', 'rounds')


class NewGameSerializer(serializers.Serializer):
    player2 = serializers.CharField()

    def validate(self, data):
        player2_id = data['player2']
        try:
            player2 = Player.objects.get(id=player2_id)
            if not player2:
                raise serializers.ValidationError("Invalid player id")
        except Exception, e:
            raise serializers.ValidationError("Invalid player id")

        return data


class NewRoundSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    game = serializers.IntegerField()

    def validate(self, data):
        category_id = data['category']
        game_id = data['game']
        try:
            category = Category.objects.get(id=category_id)
        except:
            raise serializers.ValidationError("Invalid category id")
        try:
            game = Game.objects.get(id=game_id)
        except:
            raise serializers.ValidationError("Invalid game id")
        return data


class UpdateRoundSerializer(serializers.Serializer):
    score = serializers.IntegerField()


class InviteSerializer(serializers.Serializer):
    game = serializers.IntegerField()
    category = serializers.IntegerField()

    def validate(self, data):
        game_id = data['game']
        category_id = data['category']
        try:
            game = Game.objects.get(id=game_id)
            category = Category.objects.get(id=category_id)
            if not game:
                raise serializers.ValidationError("Invalid game id")
            if not category:
                raise serializers.ValidationError("Invalid category id")
        except:
            raise serializers.ValidationError("Invalid request")
        return data
