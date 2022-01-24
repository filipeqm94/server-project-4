import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import CustomUser
from chatter.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    @database_sync_to_async
    def get_messages_or_create_room(self):
        room = ChatRoom.objects.filter(room_name=self.room_group_name)
        print(self.room_group_name)


    @database_sync_to_async
    def create_chat_message(self, chat, sender, message):
        new_chat_message = ChatMessage.objects.create(
            chat=chat, sender=sender, message=message
        )
        new_chat_message.save()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.room_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "open_chat":
            print("room openned")
            await self.get_messages_or_create_room()
        elif data["type"] == "chat_message":
            print("message sent")
            # await self.create_chat_message()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "user1": "testing_stuff",
                    "message": "testing is going well",
                },
            )

    async def chat_message(self, event):
        print("from chat_message ---->")
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
