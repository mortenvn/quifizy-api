from rest_framework import permissions


class PartOfGame(permissions.BasePermission):
    """
    Custom permission for checking that user is part of Game
    """

    def has_object_permission(self, request, view, obj=None):
        game = obj
        user = request.user

        return obj is None or game.player1 == user.player or game.player2 == user.player


class PartOfRound(permissions.BasePermission):
    """
    Custom permission for checking that user is part of Game
    """

    def has_object_permission(self, request, view, obj=None):
        round = obj
        user = request.user
        try:
            game = Game.objects.get(round.game)
        except:
            return False

        return obj is None or game.player1 == user.player or game.player2 == user.player
