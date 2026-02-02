from django.urls import path
from .views import SubmitScoreView

urlpatterns = [
    path('score/', SubmitScoreView.as_view(), name='submit-score'),
]