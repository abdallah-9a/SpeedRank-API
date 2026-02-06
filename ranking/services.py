import redis
from django.conf import settings


r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])

LEADERBOARD_KEY = "game_leaderboard"

class RedisLeaderboardService:
    
    @staticmethod
    def add_score(username, score):
        # Only update if new score is higher
        resuilt = r.zadd(LEADERBOARD_KEY, {username: score},gt=True) # gt used to update if new score is greater, and prevent race condition 
        return resuilt > 0

    @staticmethod
    def get_top_players(limit=10):
        """
        Get top N players
        """
        results = r.zrevrange(LEADERBOARD_KEY, 0, limit - 1, withscores=True)
    
        cleaned_results = []
        for rank, (username, score) in enumerate(results, start=1):
            cleaned_results.append({
                "rank": rank,
                "username": username.decode('utf-8'),
                "points": int(score)
            })
        return cleaned_results

    @staticmethod
    def get_user_rank(username):
    
        rank = r.zrevrank(LEADERBOARD_KEY, username)
        
        if rank is None:
            return None
            
    
        score = r.zscore(LEADERBOARD_KEY, username)

        return {
            "username": username,
            "rank": rank + 1,  
            "points": int(score)
        }