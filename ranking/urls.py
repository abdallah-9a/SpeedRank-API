from django.urls import path
from .views import MyRankRedisView, SubmitScoreRedisView, TopPlayersRedisView

urlpatterns = [
    path('score/', SubmitScoreRedisView.as_view(), name='submit-score'),
    path('top-players/', TopPlayersRedisView.as_view(), name='top-players'),
    path('my-rank/', MyRankRedisView.as_view(), name='my-rank'),
]