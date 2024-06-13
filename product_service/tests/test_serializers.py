from django.test import TestCase
from product_service.serializers import ProductSerializer
from product_service.models import Product

class ProductSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            'name': 'Sample Product',
            'description': 'This is a sample product.',
            'price': 19.99,
            'inventory': 100
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_price(self):
        data = {
            'name': 'Sample Product',
            'description': 'This is a sample product.',
            'price': -1,
            'inventory': 100
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['price']))

    def test_invalid_inventory(self):
        data = {
            'name': 'Sample Product',
            'description': 'This is a sample product.',
            'price': 19.99,
            'inventory': -5
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['inventory']))
