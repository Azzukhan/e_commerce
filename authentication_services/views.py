#authentication_service/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
import logging
from django.core.exceptions import ValidationError
from ratelimit import limits



logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    FIFTEEN_MINUTES = 900
    @limits(calls=15, period=FIFTEEN_MINUTES)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({'user_id': user.id, 'user_name': user.username, 'user_email': user.email}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Error occurred during user registration: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except ValidationError as e:
            logger.error(f"Error occurred during login: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
