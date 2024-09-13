# tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import SensorData
from django.utils import timezone
import json
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

class SensorDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sensor-data')

    def test_create_sensor_data(self):
        data = {
            "equipmentId": "test_equipment",
            "timestamp": "2023-02-15T01:30:00.000-05:00",
            "value": 42.5
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorData.objects.count(), 1)

    def test_create_sensor_data_invalid_json(self):
        response = self.client.post(self.url, data="invalid json", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_sensor_data_with_missing_fields(self):
        data = {
            "timestamp": "2023-02-15T01:30:00.000-05:00",
            "value": 42.5
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SensorDataCSVUploadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sensor-data-csv-upload')

    def test_upload_csv(self):
        csv_content = "equipmentId,timestamp,value\ntest_eq,2023-05-01T12:00:00Z,42.5"
        csv_file = SimpleUploadedFile("data.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post(self.url, {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorData.objects.count(), 1)

    def test_upload_non_csv_file(self):
        file = SimpleUploadedFile("data.txt", b"hello world", content_type="text/plain")
        response = self.client.post(self.url, {'file': file})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AggregatedDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('aggregated-data')
        SensorData.objects.create(equipment_id="eq1", timestamp=timezone.now(), value=10)
        SensorData.objects.create(equipment_id="eq1", timestamp=timezone.now() - timedelta(hours=1), value=20)

    def test_get_aggregated_data(self):
        response = self.client.get(self.url, {'period': '24h'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['equipment_id'], 'eq1')
        self.assertEqual(response.data[0]['avg_value'], 15)
    
    def test_get_aggregated_data_invalid_period(self):
        response = self.client.get(self.url, {'period': '72h'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_user(self):
        data = {
            "username": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_data(self):
        data = {
            "username": "testuser@example.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
