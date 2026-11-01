from django.db import models

class MedicineInventory(models.Model):
    medicine_name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField(default=0)
    batch_number = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommandQueue(models.Model):
    COMMAND_TYPES = [
        ('DISPENSE', 'Dispense Medicine'),
        ('REFILL', 'Refill Medicine'),
        ('TEST_MOTOR', 'Test Motor'),
        ('TEST_IR', 'Test IR Sensor'),
    ]
    command_type = models.CharField(max_length=50, choices=COMMAND_TYPES)
    motor_channel = models.IntegerField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)  # Stores JSON string (e.g., steps, direction)
    status = models.CharField(max_length=20, default='PENDING')  # PENDING, PROCESSING, COMPLETED
    created_at = models.DateTimeField(auto_now_add=True)

class MachineLog(models.Model):
    log_type = models.CharField(max_length=50)  # e.g., INFO, ERROR, SENSOR_TRIGGER
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)