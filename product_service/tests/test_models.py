# product_service/tests/test_models.py
from django.test import TestCase
from product_service.models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name='Sample Product',
            description='This is a sample product.',
            price=19.99,
            inventory=100
        )
        self.assertEqual(product.name, 'Sample Product')
        self.assertEqual(product.description, 'This is a sample product.')
        self.assertEqual(product.price, 19.99)
        self.assertEqual(product.inventory, 100)

    def test_update_inventory(self):
        product = Product.objects.create(
            name='Sample Product',
            description='This is a sample product.',
            price=19.99,
            inventory=100
        )
        product.update_inventory(10)
        self.assertEqual(product.inventory, 90)

        with self.assertRaises(ValueError):
            product.update_inventory(200)
