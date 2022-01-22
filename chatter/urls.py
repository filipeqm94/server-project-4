from django.urls import path
from chatter import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:chat_room_id>/', views.room, name='room')
]