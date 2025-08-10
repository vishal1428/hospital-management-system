from django.test import TestCase
from .models import Service

class ServiceModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Cardiology",
            description="Heart care services",
            cost=2500.00
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Cardiology")
        self.assertEqual(self.service.cost, 2500.00)

    def test_service_str_method(self):
        self.assertEqual(str(self.service), "Cardiology - 2500.00") 