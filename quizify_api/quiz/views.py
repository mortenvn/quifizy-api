from rest_framework import permissions, status, viewsets
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q
from rest_framework.response import Response

from permissions import PartOfGame
from serializers import CategorySerializer, SongSerializer, GameSerializer, NewGameSerializer
from models import Game
from accounts.models import Player
from songs.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    http_method_names = ('get',)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    http_method_names = ('get', 'put', 'post',)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, PartOfGame,)
    serializer_class = GameSerializer

    def get_queryset(self):
        player = self.request.user.player
        return Game.objects.filter(Q(player1=player) | Q(player2=player))

    def create(self, request):
        qp = NewGameSerializer(data=request.data)
        if not qp.is_valid():
            return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

        player2_id = qp['player2'].value
        player2 = Player.objects.get(id=player2_id)
        if player2.id == request.user.player.id:
            return Response(data={"non_field_errors": ["Player cannot play itself"]})

        # TODO: Send notification to player2
        new_game = Game.objects.create(player1=request.user.player, player2=player2, invitation_status='sent')

        return Response(data=GameSerializer(new_game).data, status=status.HTTP_201_CREATED)
