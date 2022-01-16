from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

# create custom claim to send primary and learning langugages
# by importing and subclassing with the original serializer

#     origional serializer       subclass
class ObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(ObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["primary_language"] = user.primary_language
        token["learning_language"] = user.learning_language
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    # specify required fields for user creation
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        # relate user model
        model = CustomUser
        fields = ("email", "username", "password")
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
