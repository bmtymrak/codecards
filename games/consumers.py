import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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

    def card_click(self, event):
        card = event["card"]

        self.send(text_data=json.dumps({"event_type": "card click", "card": card}))

    def end_turn(self, event):
        self.send(text_data=json.dumps({"event_type": "end turn"}))

