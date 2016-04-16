from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q

from permissions import PartOfGame
from serializers import CategorySerializer, SongSerializer, GameSerializer
from models import Game
from songs.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    http_method_names = ('get',)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    http_method_names = ('get', 'put', 'post',)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, PartOfGame,)
    serializer_class = GameSerializer

    def get_queryset(self):
        player = self.request.user.player
        return Game.objects.filter(Q(player1=player) | Q(player2=player))
