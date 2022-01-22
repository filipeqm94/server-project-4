from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# user chat rooms
def index(request):
  return JsonResponse({'test':'testing'})
  
# get specific chat room between user1 and user2
def room(request, chat_room_id):
  return JsonResponse({'chat_room_id': 'working'})