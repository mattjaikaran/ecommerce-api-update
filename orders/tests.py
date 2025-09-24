# orders/tests.py
from django.test import TestCase

from .models import Orders


class OrdersTests(TestCase):
    def setUp(self):
        self.orders = Orders.objects.create(
            name="Test Orders", description="This is a test description"
        )

    def test_str(self):
        self.assertEqual(str(self.orders), "Test Orders")

    def test_model_fields(self):
        self.assertTrue(isinstance(self.orders.name, str))
        self.assertTrue(isinstance(self.orders.description, str))

    def test_api_list(self):
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_detail(self):
        response = self.client.get(f"/orders/{self.orders.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Orders")
