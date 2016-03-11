from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import CategorySerializer, SongSerializer
from api.models import Category, Song

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
