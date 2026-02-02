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
    

class MyRankView(views.APIView):
    def get(self,request):
        username=request.query_params.get('username')
        if not username:
            return Response({"error":"Username query parameter is required."},status=status.HTTP_400_BAD_REQUEST)
        
        player=get_object_or_404(Player,username=username)
        player_scores=Score.objects.filter(player=player).aggregate(max_points=Max('points'))
        high_score = player_scores['max_points']

        if high_score is None:
            return Response({"message": "Player not found or has no scores yet"}, 
                status=status.HTTP_404_NOT_FOUND)

        better_players_count=Score.objects.values('player').annotate(max_points=Max('points')).filter(max_points__gt=high_score).count()
        rank=better_players_count+1

        return Response({"username":username,"high_score":high_score,"rank":rank},status=status.HTTP_200_OK)
