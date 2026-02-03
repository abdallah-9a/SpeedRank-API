import random
from locust import HttpUser, task, between

class LeaderboardUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.username = f"loadtest_user_{random.randint(1, 100000)}"

    @task(3) 
    def view_top_10(self):
        """Get top 10 players - most frequent operation"""
        with self.client.get("/api/top-players/", name="GET Top Players", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")

    @task(1) 
    def submit_new_score(self):
        """Submit a new score - less frequent"""
        points = random.randint(1, 100000)
        with self.client.post(
            "/api/score/", 
            json={"username": self.username, "points": points},
            name="POST Submit Score",
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}: {response.text}")

    @task(2) 
    def check_my_rank(self):
        """Check user's rank - medium frequency"""
        with self.client.get(
            f"/api/my-rank/?username={self.username}",
            name="GET My Rank",
            catch_response=True
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")