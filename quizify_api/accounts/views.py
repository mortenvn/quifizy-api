from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from oauthlib.common import generate_token

from serializers import RegisterUserSerializer, PlayerSerializer, LoginUserSerializer
from models import Player
from oauth2_provider.models import Application, AccessToken


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    http_method_names = ('get',)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSerializer


@api_view(['POST'])
def register(request):
    qp = RegisterUserSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    username = qp['username'].value
    email = qp['email'].value
    password = qp['password'].value
    client_id = qp['client_id'].value

    app = Application.objects.get(client_id=client_id)
    user = User.objects.create_user(username, email, password)
    Player.objects.create(user=user)

    access_token = AccessToken.objects.create(user=user, application=app, token=generate_token(), expires=now() + timedelta(days=1))

    return Response({'token': access_token.token}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    qp = LoginUserSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    username = qp['username'].value
    password = qp['password'].value
    client_id = qp['client_id'].value

    app = Application.objects.get(client_id=client_id)
    user = User.objects.get(username=username)
    if not user.check_password(password):
        return Response({'error': 'access denied'}, status=status.HTTP_403_FORBIDDEN)

    access_token = AccessToken.objects.create(user=user, application=app, token=generate_token(), expires=now() + timedelta(days=1))

    return Response({'token': access_token.token}, status=status.HTTP_200_OK)
