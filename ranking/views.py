from django.shortcuts import render,get_object_or_404
from .serializers import SubmitScoreSerializer,TopPlayersSerializer
from django.db.models import Max
from rest_framework import generics,views,status
from rest_framework.response import Response
from .models import Score, Player
from .services import RedisLeaderboardService
# Create your views here.

class SubmitScoreSQLView(generics.CreateAPIView):
    queryset = Score.objects.all()
    serializer_class = SubmitScoreSerializer


class TopPlayersSQLView(generics.ListAPIView):
    serializer_class = TopPlayersSerializer

    def get_queryset(self):
        return Score.objects.select_related('player').order_by('-points')[:10]
    

class MyRankSQLView(views.APIView):
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
    

class SubmitScoreRedisView(views.APIView):
    def post(self, request):
        serializer = SubmitScoreSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            points = serializer.validated_data['points']
            
            # 1. Save to database (persistence)
            player, _ = Player.objects.get_or_create(username=username)
            Score.objects.create(player=player, points=points)
            
            # 2. Update Redis (fast queries)
            RedisLeaderboardService.add_score(username, points)
            
            return Response({"message": "Score submitted"}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                       status=status.HTTP_400_BAD_REQUEST)
    

class TopPlayersRedisView(views.APIView):
    def get(self,request):
        top_players=RedisLeaderboardService.get_top_10()
        return Response(top_players,status=status.HTTP_200_OK)


class MyRankRedisView(views.APIView):
    def get(self,request):
        username=request.query_params.get('username')
        if not username:
            return Response({"error":"Username query parameter is required."},status=status.HTTP_400_BAD_REQUEST)
        
        user_rank=RedisLeaderboardService.get_user_rank(username)
        if user_rank is None:
            return Response({"message": "Player not found in leaderboard."}, 
                status=status.HTTP_404_NOT_FOUND)
        
        return Response(user_rank,status=status.HTTP_200_OK)
