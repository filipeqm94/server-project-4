from django.utils.timezone import now
from django.db import models
from accounts.models import CustomUser

class ChatRoom(models.Model):
  user_one = models.ForeignKey(CustomUser, related_name='user_one_chat_rooms', on_delete=models.CASCADE)
  user_two = models.ForeignKey(CustomUser, related_name='user_two_chat_rooms', on_delete=models.CASCADE)
  room_name = models.TextField(unique=True, null=False, blank=False)

  def __str__(self):
    return self.room_name

class ChatMessage(models.Model):
  chat = models.ForeignKey(ChatRoom, related_name='chats', on_delete=models.CASCADE)
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  message = models.TextField()
  timestamp = models.DateTimeField(default=now, editable=False)

  def __str__(self):
    return "Message by: " + self.chat.room_name
