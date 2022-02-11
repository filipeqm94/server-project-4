from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from .views import GetChatRooms, SignUp, Login, Logout, GetMessages, GetUsers


urlpatterns = [
    path("signup/", SignUp.as_view()),
    path("login/", Login.as_view()),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view()),
    path("logout/", Logout.as_view()),
    path("getusers/", GetUsers.as_view()),
    path("getmessages/<str:room_name>/", GetMessages.as_view()),
    path("getchatrooms/", GetChatRooms.as_view()),
]
