from django.test import TestCase
from payment_service.models import Payment

class PaymentModelTest(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            order=1,
            amount=100.00,
            status='pending'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, 1)
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.status, 'pending')
