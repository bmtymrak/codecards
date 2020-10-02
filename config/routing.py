from channels.routing import ProtocolTypeRouter, URLRouter
import games.routing

application = ProtocolTypeRouter(
    {"websocket": URLRouter(games.routing.websocket_urlpatterns)}
)

