from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import Player


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return User.objects.get(id=obj.id).username

    class Meta:
        model = Player
        fields = ('id', 'username')


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    client_id = serializers.CharField()


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    client_id = serializers.CharField()