import asyncio
import json
from channels.consumer import AsyncConsumer

class ChatConsumer(AsyncConsumer):
  async def websocket_connect(self,event):
    print('connected', event)
    chat_room = "chatroom"
    self.chat_room = chat_room
    await self.channel_layer.group_add(
      chat_room,
      self.channel_name
    )
    await self.send({
      "type": "websocket.accept"
    })

    async def websocket_receive(self, event):
      drawing_data = event.get('text', None)
      await self.channel_layer.group_send(
        self.chat_room,
        {
          "type": "chat_message",
          "text": drawing_data
        }
      )
    
    async def chat_message(self, event):
      await self.send({
        "type": 'websocket.send',
        "text": event['text']
      })
    
    async def websocket_disconnect(self, event):
      print('disconnected', event)