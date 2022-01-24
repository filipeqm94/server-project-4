import json
from tabnanny import check
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

    # @database_sync_to_async
    # def create_chat_room(self, user_one, user_two, display_name):
    #     room = ChatRoom.objects.filter(display_name=display_name)
    #     if len(room) == 0:
    #         print('i dont exist')
    #         test_user_one = CustomUser.objects.get(username=user_one)
    #         test_user_two = CustomUser.objects.get(username=user_two)
        
    #         new_chat_room = ChatRoom.objects.create(
    #         user_one=test_user_one, user_two=test_user_two, display_name=display_name)
    #         new_chat_room.save()

    @database_sync_to_async
    def create_chat_message(self, chat, sender, message):
        print(sender)
        find_sender = CustomUser.objects.filter(username = sender)[0]
        chat_room = ChatRoom.objects.filter(room_name=chat)[0]
        new_chat_message = ChatMessage.objects.create(
        chat=chat_room, sender=find_sender, message=message )
        new_chat_message.save()

    @database_sync_to_async
    def get_messages(self):
        print("Getting messages", self.room_group_name)
        chat = ChatRoom.objects.get(display_name=self.room_group_name)
        messages = ChatMessage.objects.filter(chat=chat.pk)
        print(messages)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.room_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass
        # data = json.loads(text_data)
        # # user1 is sender
        # # if data['type'] == 'open_chat':
        # #     # await self.create_chat_room()
        # #     # await self.create_chat_room(user_one, user_two, self.room_group_name)
        # #     # await self.get_messages()

        # # else:
        # user_one =  data["user_one"]
        # user_two =  data["user_two"]
        # # print('text data json', text_data_json)
        # message = data["message"]
        # print("message", message)

        # print("groupname --->", self.room_group_name)

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {"type": "chat_message", "user1": user_one, "message": message},
        # )


            
        # await self.create_chat_message(self.room_group_name, user_one, message)

    async def chat_message(self, event):
        print("from chat_message ---->")
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
