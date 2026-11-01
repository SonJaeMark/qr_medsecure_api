from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.check_inventory, name='check-inventory'),
    path('refill/', views.refill_medicine, name='refill-medicine'),
    path('commands/send/', views.send_command, name='send-command'),
    path('iot/poll/', views.iot_poll_instructions, name='iot-poll'),
    path('logs/machine/', views.machine_logging, name='machine-logs'),
]