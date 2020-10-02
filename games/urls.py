from django.urls import path
from .views import HomePageView, GameView


urlpatterns = [
    path("<uuid:id>/", GameView.as_view(), name="game"),
    path("", HomePageView.as_view(), name="home"),
]

