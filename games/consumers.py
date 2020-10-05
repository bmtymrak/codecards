import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Game, Card


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = f"game_{self.game_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["event_type"] == "card click":
            card = text_data_json["card"]
            event_type = "card_click"

            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": event_type, "card": card}
            )

        if text_data_json["event_type"] == "end turn":
            event_type = "end_turn"
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": event_type}
            )

        if text_data_json["event_type"] == "new game":
            game_id = text_data_json["game_id"].lstrip(("/")).rstrip("/")
            self.create_new_game(game_id)

    def card_click(self, event):
        card = event["card"]
        clicked_card = Card.objects.get(word=card["word"])
        clicked_card.clicked = True
        clicked_card.save()

        self.send(text_data=json.dumps({"event_type": "card click", "card": card}))

    def end_turn(self, event):
        self.send(text_data=json.dumps({"event_type": "end turn"}))

    def create_new_game(self, game_id):
        Game.objects.filter(id=game_id).delete()
        new_game = Game(id=game_id)
        new_game.save()

        cards = [
            {"word": card.word, "team": card.team, "clicked": card.clicked}
            for card in new_game.card_set.all()
        ]

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "new_game", "cards": cards}
        )

    def new_game(self, data):
        self.send(
            text_data=json.dumps({"event_type": data["type"], "cards": data["cards"]})
        )
