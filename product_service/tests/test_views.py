from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product_service.models import Product
from authentication_services.models import CustomUser
from decimal import Decimal

# product_service/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product_service.models import Product

class ProductListCreateViewTest(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=None)  # Ensure unauthenticated user for testing

    def test_create_product(self):
        url = reverse('product-list-create')
        data = {
            'name': 'Sample Product',
            'description': 'This is a sample product.',
            'price': 19.99,
            'inventory': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Sample Product')

    def test_update_inventory(self):
        product = Product.objects.create(
            name='Sample Product',
            description='This is a sample product.',
            price=19.99,
            inventory=100
        )
        url = reverse('update-inventory', kwargs={'pk': product.pk})
        data = {'quantity': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.inventory, 90)

        data = {'quantity': 200}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        product.refresh_from_db()
        self.assertEqual(product.inventory, 90)


class ProductRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.user.is_staff = True  # Make the user an admin
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            name='Sample Product',
            description='This is a sample product.',
            price=Decimal('19.99'),
            inventory=100
        )

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Product')

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated sample product.',
            'price': 29.99,
            'inventory': 150
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, Decimal('29.99'))  # Use Decimal for comparison

    def test_partial_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {'price': 24.99}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal('24.99'))  # Use Decimal for comparison

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
