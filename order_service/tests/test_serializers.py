from django.test import TestCase
from django.contrib.auth import get_user_model
from product_service.models import Product
from order_service.models import Order, OrderItem
from order_service.serializers import OrderSerializer, OrderItemSerializer
from decimal import Decimal

User = get_user_model()

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=Decimal('10.00'), inventory=100)
        self.order = Order.objects.create(customer=self.user, status='pending')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('20.00'))
    
    def test_order_item_serializer(self):
        serializer = OrderItemSerializer(self.order_item)
        data = serializer.data
        self.assertEqual(data['product'], self.product.id)
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['price'], '20.00')

    def test_order_serializer(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(data['customer'], self.user.id)
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['product'], self.product.id)
        self.assertEqual(data['items'][0]['quantity'], 2)
        self.assertEqual(data['items'][0]['price'], '20.00')
    
    def test_order_serializer_create(self):
        data = {
            'status': 'pending',
            'items': [
                {'product': self.product.id, 'quantity': 2, 'price': '20.00'}
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(customer=self.user)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 2)
        self.assertEqual(order.items.first().price, Decimal('20.00'))
    
    def test_order_serializer_update(self):
        data = {
            'status': 'shipped',
            'items': [
                {'product': self.product.id, 'quantity': 3, 'price': '30.00'}
            ]
        }
        serializer = OrderSerializer(self.order, data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.status, 'shipped')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 3)
        self.assertEqual(order.items.first().price, Decimal('30.00'))
