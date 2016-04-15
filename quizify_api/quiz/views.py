from django.shortcuts import render
from rest_framework import viewsets
from serializers import CategorySerializer, SongSerializer, GameSerializer
from songs.models import Category, Song
from quiz.models import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
