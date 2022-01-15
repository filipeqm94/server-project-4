from django.urls import path
from . import views

urlpatterns = [
    path("objects/", views.ObjectsList.as_view(), name="objects_list")
]