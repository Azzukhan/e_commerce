from django.test import TestCase
from payment_service.serializers import PaymentSerializer

class PaymentSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'order': 1,
            'amount': 100.00,
            'status': 'pending'
        }
        self.serializer = PaymentSerializer(data=self.valid_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data(self):
        invalid_data = {
            'order': 1,
            'amount': 'invalid',
            'status': 'pending'
        }
        serializer = PaymentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_create_method(self):
        self.serializer.is_valid(raise_exception=True)
        payment = self.serializer.save()
        self.assertEqual(payment.order, 1)
        self.assertEqual(payment.amount, 100.00)
        self.assertEqual(payment.status, 'pending')
