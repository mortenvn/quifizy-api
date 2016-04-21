from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from oauthlib.common import generate_token
from django.shortcuts import get_object_or_404

from serializers import RegisterUserSerializer, PlayerSerializer, LoginUserSerializer, SearchUsernameSerializer
from models import Player
from oauth2_provider.models import Application, AccessToken


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    http_method_names = ('get',)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSerializer


@api_view(['POST'])
def search_by_username(request):
    qp = SearchUsernameSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=qp['username'].value)
    player = get_object_or_404(Player, user=user)
    return Response(data=PlayerSerializer(player).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    qp = RegisterUserSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    username = qp['username'].value
    email = qp['email'].value
    password = qp['password'].value
    client_id = qp['client_id'].value

    try:
        app = Application.objects.get(client_id=client_id)
        user = User.objects.create_user(username, email, password)
        if not app:
            return Response({'error': 'Invalid client id'}, status=status.HTTP_403_FORBIDDEN)
        Player.objects.create(user=user)
        access_token = AccessToken.objects.create(user=user, application=app, token=generate_token(), expires=now() + timedelta(days=1))
    except:
        return Response({'error': 'Invalid client id'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'token': access_token.token}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    qp = LoginUserSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    username = qp['username'].value
    password = qp['password'].value
    client_id = qp['client_id'].value

    try:
        app = Application.objects.get(client_id=client_id)
        user = User.objects.get(username=username)
        if not user:
            return Response({'error': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
        if not user.check_password(password):
            return Response({'error': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
        if not app:
            return Response({'error': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({'error': 'access denied'}, status=status.HTTP_403_FORBIDDEN)

    access_token = AccessToken.objects.create(user=user, application=app, token=generate_token(), expires=now() + timedelta(days=1))

    return Response({'token': access_token.token}, status=status.HTTP_200_OK)
