from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import DeviceSerializer
from .models import Device
# Create your views here.

class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.all()
