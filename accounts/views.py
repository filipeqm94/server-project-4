from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

from .serializers import ObtainTokenPairSerializer, CustomUserSerializer
from .models import CustomUser
from chatter.models import ChatMessage, ChatRoom

# login view
class Login(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer


# signup view
class SignUp(APIView):
    # allow anyone to create a new signup
    permission_classes = (permissions.AllowAny,)
    # remove auth classes
    # so users dont need to be logged in to create an account
    authentication_classes = ()

    def post(self, request, format="json"):
        username = CustomUser.objects.filter(username=request.data["username"]).exists()
        email = CustomUser.objects.filter(email=request.data["email"]).exists()

        if username:
            return Response(
                {"detail": "Username is already taken"},
                status=status.HTTP_409_CONFLICT,
            )
        elif email:
            return Response(
                {"detail": "Email is already taken"}, status=status.HTTP_409_CONFLICT
            )
        else:
            # check the request data against the serializer
            serializer = CustomUserSerializer(data=request.data)
            # if the data received is valid
            if serializer.is_valid():
                # create the new user
                user = serializer.save()
                # if the creation was successfull
                if user:
                    # send back the created user with the 200 response
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
            # send back 400 if missing information or bad request
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# logout view
class Logout(APIView):
    # allow anyone to logout
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            # get refresh token
            refresh_token = request.data["refresh_token"]
            # create a refresh token object for access to the blacklist class method
            token = RefreshToken(refresh_token)
            # blacklist token
            token.blacklist()
            # send 200
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # send 400
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUsers(APIView):
    def get(self, request):
        # variable name = request.GET.get("the value of key that was passed in the request", or "empty string")
        primary_language = request.GET.get("primary_language", "")
        learning_language = request.GET.get("learning_language", "")
        # filter the database to get the matching users
        users = CustomUser.objects.filter(
            primary_language=learning_language, learning_language=primary_language
        ).values("username")
        return JsonResponse(list(users), safe=False)


class GetMessages(APIView):
    def get(self, request, room_name):
        room = ChatRoom.objects.filter(room_name=room_name)
        chat_messages = (
            ChatMessage.objects.filter(chat=room[0].pk)
            .order_by("-timestamp")
            .values("message", "sender")
        )
        return JsonResponse(list(chat_messages), safe=False)


class GetChatRooms(APIView):
    def get(self, request):
        username = CustomUser.objects.get(username=request.GET.get("username", ""))
        rooms_one = list(ChatRoom.objects.filter(user_one=username).values("user_two"))
        rooms_two = list(ChatRoom.objects.filter(user_two=username).values("user_one"))
        chat_rooms = rooms_one + rooms_two
        users_list = []

        for pk in chat_rooms:
            if "user_one" in pk:
                users_list.append(
                    CustomUser.objects.filter(pk=pk["user_one"]).values("username")[0][
                        "username"
                    ]
                )
            else:
                users_list.append(
                    CustomUser.objects.filter(pk=pk["user_two"]).values("username")[0][
                        "username"
                    ]
                )

        return JsonResponse(users_list, safe=False)
