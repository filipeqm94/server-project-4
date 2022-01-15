from rest_framework import generics
from .serializers import ObjectsSerializer
from .models import Objects

# Create your views here.
class ObjectsList(generics.ListCreateAPIView):
    queryset = Objects.objects.all()
    serializer_class = ObjectsSerializer