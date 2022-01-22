import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.chat_room_group_id = 'chat_%s' % self.chat_room_group_id

        # Join room group
        await self.channel_layer.group_add(
            self.chat_room_group_id,
            self.channel_id
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_room_group_id,
            self.channel_id
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_room_group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))