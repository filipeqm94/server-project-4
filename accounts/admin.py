from django.contrib import admin
from .models import CustomUser
from chatter.models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    # fields = ('username', 'chat_rooms')

class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom

class ChatMessageAdmin(admin.ModelAdmin):
    model = ChatMessage

# register custom user and admin to `admin/`
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)

