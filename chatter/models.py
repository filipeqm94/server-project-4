from django.utils.timezone import now
from django.db import models
from accounts.models import CustomUser

class ChatRoom(models.Model):
  user_one = models.ForeignKey(CustomUser, related_name='user_one', on_delete=models.CASCADE)
  user_two = models.ForeignKey(CustomUser, related_name='user_two', on_delete=models.CASCADE)
  display_name = models.CharField(max_length=50)

  def __str__(self):
    return self.display_name

class ChatMessage(models.Model):
  chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  message = models.TextField()
  timestamp = models.DateTimeField(default=now, editable=False)

  def __str__(self):
    return self.sender.username
  
