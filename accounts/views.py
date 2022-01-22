from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ObtainTokenPairSerializer, CustomUserSerializer

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
