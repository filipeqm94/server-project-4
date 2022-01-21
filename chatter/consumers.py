import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.channel_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        # print('text data', text_data)
        text_data_json = json.loads(text_data)
        # print('text data json', text_data_json)
        message = text_data_json["message"]
        print("message", message)

        print("groupname --->", self.room_group_name)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        print("from chat_message ---->")
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
