from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
import logging
from django.core.exceptions import ValidationError
from ratelimit import limits

logger = logging.getLogger(__name__)

# View for user registration
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # Define the rate limit (15 calls per 15 minutes)
    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            # Validate and save the new user data
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            # Return the user's ID, username, and email upon successful registration
            return Response({'user_id': user.id, 'user_name': user.username, 'user_email': user.email}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Log and return any validation errors
            logger.error(f"Error occurred during user registration: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # Define the rate limit (15 calls per 15 minutes)
    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        try:
            # Validate the login data
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Generate JWT tokens (refresh and access tokens)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except ValidationError as e:
            # Log and return any validation errors
            logger.error(f"Error occurred during login: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
