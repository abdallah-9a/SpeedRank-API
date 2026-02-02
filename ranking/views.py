from django.shortcuts import render,get_object_or_404
from .serializers import SubmitScoreSerializer,TopPlayersSerializer
from django.db.models import Max
from rest_framework import generics,views,status
from rest_framework.response import Response
from .models import Score, Player
# Create your views here.

class SubmitScoreView(generics.CreateAPIView):
    queryset = Score.objects.all()
    serializer_class = SubmitScoreSerializer


class TopPlayersView(generics.ListAPIView):
    serializer_class = TopPlayersSerializer

    def get_queryset(self):
        return Score.objects.select_related('player').order_by('-points')[:10]
    
