from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authentication_services.models import CustomUser
from payment_service.models import Payment
from rest_framework_simplejwt.tokens import RefreshToken

class PaymentViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        
    def test_create_payment(self):
        url = reverse('payment-create')  # Assuming you have named your URL for payment creation 'payment-create'
        data = {
            'order': 1,  # Sample order ID
            'amount': '100.00',  # Sample amount
            'status': 'pending'  # Sample status
        }
        # Set the authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data, format='json')
        print("Payment creation response:", response.data)  # Log the response data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_payment(self):
        # First, create a payment to retrieve
        payment = Payment.objects.create(order=1, amount='100.00', status='pending')
        url = reverse('payment-detail', kwargs={'pk': payment.pk})  # Assuming you have named your URL for payment retrieval 'payment-detail'
        # Set the authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        print("Payment retrieval response:", response.data)  # Log the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
