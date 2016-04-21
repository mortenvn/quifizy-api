from rest_framework import permissions, status, viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from permissions import PartOfGame, PartOfRound
from serializers import CategorySerializer, RoundSerializer, GameSerializer, NewGameSerializer, \
    InviteSerializer, NewRoundSerializer, UpdateRoundSerializer
from models import Game, Round
from accounts.models import Player
from songs.models import Category
from generate_round import generate_round


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    http_method_names = ('put', 'post',)
    permission_classes = (permissions.IsAuthenticated, PartOfRound)
    serializer_class = RoundSerializer

    def create(self, request):
        qp = NewRoundSerializer(data=request.data)
        if not qp.is_valid():
            return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check that old rounds are completed
        active_rounds = Round.objects.filter(game=qp['game'].value, status='active')
        if active_rounds:
            return Response(data={"error": "Previous round not completed"}, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.get(id=qp['game'].value)
        category = Category.objects.get(id=qp['category'].value)
        round = generate_round(game, category, request.user.player)
        # TODO: Notification
        return Response(data=GameSerializer(game, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        qp = UpdateRoundSerializer(data=request.data)
        if not qp.is_valid():
            return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            round = Round.objects.get(id=pk)
            game = Game.objects.get(id=round.game.id)
            # Update score and whos_turn
            if request.user.player.id == game.player1.id:
                round.player1_score = qp['score'].value
                round.whos_turn = game.player2
            else:
                round.player2_score = qp['score'].value
                round.whos_turn = game.player1

            # If turn complete, update status and remove whos turn attribute
            if round.player1_score and round.player2_score:
                round.status = 'completed'
                round.whos_turn = None
            round.save()
        except Exception, e:
            print e
            return Response(data={"error": "Round not found"}, status=status.HTTP_404_NOT_FOUND)

        # TODO: Notification
        return Response(data=RoundSerializer(round, context={'request': request}).data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    http_method_names = ('get', 'put', 'post',)
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
            return Response(data={"non_field_errors": ["Player cannot play itself"]}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Send notification to player2
        new_game = Game.objects.create(player1=request.user.player, player2=player2, invitation_status='sent')

        return Response(data=GameSerializer(new_game).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def accept_invite(request):
    qp = InviteSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    game_id = qp['game'].value
    category_id = qp['category'].value

    game = Game.objects.get(id=game_id)
    if not game.player2.id == request.user.player.id:
        return Response(data={"non_field_errors": ["Not permitted"]}, status=status.HTTP_403_FORBIDDEN)

    game.invitation_status = 'accepted'
    game.save()

    category = Category.objects.get(id=category_id)
    new_round = generate_round(game, category, request.user.player)
    # TODO: Send notification to player1
    test = GameSerializer(game, context={'request': request}).data

    return Response(data=test, status=status.HTTP_201_CREATED)
