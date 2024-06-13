from django.test import TestCase
from django.contrib.auth import get_user_model
from product_service.models import Product
from order_service.models import Order, OrderItem
from decimal import Decimal

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=Decimal('10.00'), inventory=100)
        self.order = Order.objects.create(customer=self.user, status='pending')

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.customer, self.user)
        self.assertEqual(self.order.status, 'pending')

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('20.00'))
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('20.00'))
