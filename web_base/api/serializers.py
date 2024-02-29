from rest_framework.serializers import ModelSerializer

from .models import Device, Robot

class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class RobotSerializer(ModelSerializer):
    class Meta:
        model = Robot
        fields = '__all__'