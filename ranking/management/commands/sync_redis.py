from django.core.management.base import BaseCommand
from django.db.models import Max
from ranking.models import Score 
from ranking.services import RedisLeaderboardService

class Command(BaseCommand):
    help = 'Synchronize data from SQL Database to Redis Leaderboard'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("⏳ Starting migration from SQL to Redis..."))

        players_data = Score.objects.values('player__username').annotate(max_score=Max('points'))

        total_players = len(players_data)
        self.stdout.write(f"📊 Found {total_players} unique players in SQL.")

        count = 0
        for entry in players_data:
            username = entry['player__username']
            score = entry['max_score']

            RedisLeaderboardService.add_score(username, score)
            
            count += 1
            if count % 1000 == 0:
                self.stdout.write(f"   -> Synced {count}/{total_players}...")

        self.stdout.write(self.style.SUCCESS(f"✅ DONE! Successfully synced {count} players to Redis."))