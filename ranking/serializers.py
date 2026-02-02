from rest_framework import serializers
from .models import Player, Score

class SubmitScoreSerializer(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    player = serializers.CharField(source='player.username', read_only=True)

    class Meta:
        model = Score
        fields = ['username', 'player','points','achieved_at']
    
    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("Points cannot be negative")
        if value > 1000000:  # Max points limit
            raise serializers.ValidationError("Points exceed maximum allowed")
        return value
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        player, _ = Player.objects.get_or_create(username=username)
        score = Score.objects.create(player=player, **validated_data)
        return score

class TopPlayersSerializer(serializers.ModelSerializer):
    player_username = serializers.CharField(source='player.username')

    class Meta:
        model = Score
        fields = ['player_username', 'points']