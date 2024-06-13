from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from product_service.models import Product
from order_service.models import Order, OrderItem
from decimal import Decimal
from unittest.mock import patch
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class OrderCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)  # Obtain access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')  # Set token in headers
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=Decimal('10.00'), inventory=100)

    def test_create_order(self):
        url = reverse('order-create')
        data = {
            'status': 'pending',
            'items': [
                {'product': self.product.id, 'quantity': 2, 'price': '20.00'}
            ]
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, 'pending')

        # Verify that create_payment is called with the correct token
        with patch('order_service.views.OrderCreateView.create_payment') as mock_create_payment:
            mock_create_payment.assert_called_once_with(Order.objects.get().id, Decimal('20.00'))



class OrderDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=Decimal('10.00'), inventory=100)
        self.order = Order.objects.create(customer=self.user, status='pending')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('20.00'))

    def test_retrieve_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(len(response.data['items']), 1)

    def test_update_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        data = {
            'status': 'shipped',
            'items': [
                {'product': self.product.id, 'quantity': 3, 'price': '30.00'}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'shipped')
        self.assertEqual(self.order.items.first().quantity, 3)
        self.assertEqual(self.order.items.first().price, Decimal('30.00'))

    def test_partial_update_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        data = {'status': 'delivered'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')

    def test_delete_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

class OrderListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=Decimal('10.00'), inventory=100)
        self.order = Order.objects.create(customer=self.user, status='pending')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('20.00'))


    def test_get_orders(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)