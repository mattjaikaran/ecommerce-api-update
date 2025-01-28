# products/tests.py
from django.test import TestCase
from .models import Products

class ProductsTests(TestCase):
    def setUp(self):
        self.products = Products.objects.create(
            name='Test Products',
            description='This is a test description'
        )

    def test_str(self):
        self.assertEqual(str(self.products), 'Test Products')

    def test_model_fields(self):
        self.assertTrue(isinstance(self.products.name, str))
        self.assertTrue(isinstance(self.products.description, str))

    def test_api_list(self):
        response = self.client.get(f'/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_detail(self):
        response = self.client.get(f'/products/{self.products.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Products')
