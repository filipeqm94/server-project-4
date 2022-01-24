from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
# @login_required
class Test(APIView):
    def get(self, request):
        return JsonResponse({"test": "a quick one too"})


# user chat rooms
def index(request):
    return JsonResponse({"test": "testing"})


# get specific chat room between user1 and user2
def room(request, chat_room_id):
    return JsonResponse({"chat_room_id": "working"})
