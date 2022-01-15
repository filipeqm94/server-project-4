from rest_framework import serializers
from .models import Objects


class ObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objects
        fields = ("id", "name", "dob")
