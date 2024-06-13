from django.test import TestCase
from authentication_services.serializers import UserSerializer, LoginSerializer
from authentication_services.models import CustomUser

class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123'))

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_login_serializer(self):
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
