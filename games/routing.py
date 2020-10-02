from django.urls import re_path
from .consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/games/(?P<game_id>[\w-]+)/$", GameConsumer),
]
