import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import CustomUser
from chatter.models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name
        self.username = await self.get_name()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.create_chat_room()
        await self.create_chat_message()

        await self.accept()

    @database_sync_to_async
    def create_chat_room(self, user_one, user_two, display_name):
        new_chat_room = ChatRoom.objects.create(user_one=user_one, user_two=user_two, display_name=display_name)
        new_chat_room.save()
        return new_chat_room

    @database_sync_to_async
    def create_chat_message(self, chat, user, message ):
        new_chat_message = ChatMessage.objects.create(chat=chat, user=user, message=message)
        new_chat_message.save()
        return new_chat_message

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.room_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # user1 is sender
        user_one = text_data_json['user_one']
        user_two = text_data_json['user_two']
        # print('text data json', text_data_json)
        message = text_data_json["message"]
        print("message", message)

        print("groupname --->", self.room_group_name)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
            "user1": user_one, "message": message}
        )
        
    async def chat_message(self, event):
        print("from chat_message ---->")
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
