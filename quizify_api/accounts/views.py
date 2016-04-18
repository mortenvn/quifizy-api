from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from oauthlib.common import generate_token

from serializers import RegisterUserSerializer
from models import Player
from oauth2_provider.models import Application, AccessToken

@api_view(['POST'])
def register(request):
    qp = RegisterUserSerializer(data=request.data)
    if not qp.is_valid():
        return Response(data=qp.errors, status=status.HTTP_400_BAD_REQUEST)

    username = qp['username'].value
    email = qp['email'].value
    password = qp['password'].value

    user = User.objects.create_user(username, email, password)
    Player.objects.create(user=user)

    auth_app_name = settings.AUTH_APPLICATION_NAME
    app = Application.objects.get(name=auth_app_name)
    access_token = AccessToken.objects.create(user=user, application=app, token=generate_token(), expires=now() + timedelta(days=1))

    return Response({'token': access_token.token}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def debug(request):
    print request.data
    return Response({'token': 'hoi'})
