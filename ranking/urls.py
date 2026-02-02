from django.urls import path
from .views import SubmitScoreView,TopPlayersView

urlpatterns = [
    path('score/', SubmitScoreView.as_view(), name='submit-score'),
    path('top-players/', TopPlayersView.as_view(), name='top-players'),
]