from rest_framework import serializers
from .models import MedicineInventory, CommandQueue, MachineLog

class MedicineInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineInventory
        fields = '__all__'

class CommandQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandQueue
        fields = '__all__'

class MachineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineLog
        fields = '__all__'