from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

from serializers import RegisterUserSerializer, PlayerSerializer
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
    player = Player.objects.create(user=user)

    # TODO: Return auth token
    # auth_app_name = settings.AUTH_APPLICATION_NAME
    # app = Application.objects.get(name=auth_app_name)
    # token, created = AccessToken.objects.get_or_create(user=user, expires=now() + timedelta(days=1), application=app)
    # print "========"
    # print token
    # print created
    # print "========"

    return Response({'player': PlayerSerializer(player).data}, status=status.HTTP_201_CREATED)



    # serialized = UserSerializer(data=request.DATA)
    # if serialized.is_valid():
    #     User.objects.create_user(
    #         serialized.init_data['email'],
    #         serialized.init_data['username'],
    #         serialized.init_data['password']
    #     )
    #     return Response(serialized.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
