from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication_services.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationViewTest(APITestCase):
    def test_user_registration(self):
        url = reverse('user_registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
