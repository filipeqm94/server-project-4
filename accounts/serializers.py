import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

# create custom claim to send primary and learning langugages
# by importing and subclassing with the original serializer

#     origional serializer       subclass
class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(ObtainTokenPairSerializer, cls).get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["primary_language"] = user.primary_language
        token["learning_language"] = user.learning_language
        # token["user_one_chat_rooms"] = user.user_one_chat_rooms
        # token["user_two_chat_rooms"] = user.user_two_chat_rooms
        token["last_login"] = json.dumps(user.last_login, default=str)
        token["date_joined"] = json.dumps(user.date_joined, default=str)
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    # specify required fields for user creation
    email = serializers.EmailField(required=True)
    username = serializers.CharField(min_length=6, max_length=18, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    primary_language = serializers.CharField(max_length=100, required=True)
    learning_language = serializers.CharField(max_length=100, required=True)

    class Meta:
        # relate user model
        model = CustomUser
        fields = (
            "email",
            "username",
            "primary_language",
            "learning_language",
        )
        extra_kwargs = {"password": {"write_only": True}}

    # create user method
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
