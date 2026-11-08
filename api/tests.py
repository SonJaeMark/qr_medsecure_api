from django.test import TestCase
from rest_framework.test import APIClient

from .models import CommandQueue


class CommandMachineRoutingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY='qr-medsecure-super-secret-key-123')

    def test_send_command_requires_machine_id_and_returns_it(self):
        response = self.client.post(
            '/api/v1/commands/send/',
            {
                'machine_id': 'MSv1M-001',
                'command_type': 'DISPENSE',
                'motor_channel': 2,
                'parameters': '{"steps": 120}',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['machine_id'], 'MSv1M-001')

    def test_iot_poll_only_returns_commands_for_requesting_machine(self):
        CommandQueue.objects.create(machine_id='MSv1M-001', command_type='DISPENSE')
        CommandQueue.objects.create(machine_id='MSv1M-002', command_type='CALIBRATE')

        response = self.client.get('/api/v1/iot/poll/?machine_id=MSv1M-002')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['command']['machine_id'], 'MSv1M-002')
        self.assertEqual(response.data['command']['command_type'], 'CALIBRATE')

    def test_iot_poll_requires_machine_id(self):
        response = self.client.get('/api/v1/iot/poll/')

        self.assertEqual(response.status_code, 400)
