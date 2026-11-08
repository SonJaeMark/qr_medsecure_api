from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MedicineInventory, CommandQueue, MachineLog
from .serializers import MedicineInventorySerializer, CommandQueueSerializer, MachineLogSerializer
from .utils import require_api_key

# 1. Check Inventory (Web Side)
@api_view(['GET'])
@require_api_key
def check_inventory(request):
    items = MedicineInventory.objects.all()
    serializer = MedicineInventorySerializer(items, many=True)
    return Response(serializer.data)


# 2. Refill Medicine (Web Side / Machine Side)
@api_view(['POST'])
@require_api_key
def refill_medicine(request):
    item_id = request.data.get('medicine_inventory_id')
    quantity_added = request.data.get('quantity_added', 0)
    
    try:
        item = MedicineInventory.objects.get(id=item_id)
        item.stock_quantity += int(quantity_added)
        item.save()
        return Response({"status": "success", "new_stock": item.stock_quantity})
    except MedicineInventory.DoesNotExist:
        return Response({"error": "Medicine inventory item not found"}, status=status.HTTP_404_NOT_FOUND)


# 3. Dispensing, Motor Test (End-switch), and IR Test Triggers (Web Side)
@api_view(['POST'])
@require_api_key
def send_command(request):
    serializer = CommandQueueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(status='PENDING')
        return Response({"status": "success", "message": "Command queued for IoT machine", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4. IoT Machine Polling Endpoint (Machine Side - ESP32)
@api_view(['GET'])
@require_api_key
def iot_poll_instructions(request):
    machine_id = request.query_params.get('machine_id')
    if not machine_id:
        return Response(
            {"error": "The machine_id query parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cmd = CommandQueue.objects.filter(status='PENDING', machine_id=machine_id).first()
    if not cmd:
        return Response({"status": "no_instruction"})
    
    # Mark as PROCESSING so it doesn't duplicate instructions on repeat polls
    cmd.status = 'PROCESSING'
    cmd.save()
    
    serializer = CommandQueueSerializer(cmd)
    return Response({
        "status": "success",
        "command": serializer.data
    })


# 5. Machine Logging Endpoint (Machine Side - ESP32)
@api_view(['POST'])
@require_api_key
def machine_logging(request):
    serializer = MachineLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message": "Log recorded"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)