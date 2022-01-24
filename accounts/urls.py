from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import SignUp, Login, Logout, Test


urlpatterns = [
    path("signup/", SignUp.as_view()),
    path("login/", Login.as_view()),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view()),
    path("logout/", Logout.as_view()),
    path("test/", Test.as_view())
]
