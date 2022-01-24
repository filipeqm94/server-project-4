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
    def create_room_if_it_does_not_exist(self, user_one, user_two):
        first_user = CustomUser.objects.get(username=user_one)
        second_user = CustomUser.objects.get(username=user_two)
        room = ChatRoom.objects.filter(room_name=self.room_group_name)
        if len(room) == 0:
            new_room = ChatRoom.objects.create(
                user_one=first_user,
                user_two=second_user,
                room_name=self.room_group_name,
            )
            new_room.save()

    @database_sync_to_async
    def create_chat_message(self, sender, message):
        user = CustomUser.objects.get(username=sender)
        chat = ChatRoom.objects.get(room_name=self.room_group_name)
        new_chat_message = ChatMessage.objects.create(
            chat=chat, sender=user, message=message
        )
        new_chat_message.save()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.room_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "open_chat":
            await self.create_room_if_it_does_not_exist(
                data["user_one"], data["user_two"]
            )

        elif data["type"] == "chat_message":
            await self.create_chat_message(data["sender"], data["message"])

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "sender": data["sender"],
                    "message": data["message"],
                },
            )

    async def chat_message(self, event):
        sender = event["sender"]
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "message": message,
                }
            )
        )