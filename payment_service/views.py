from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer
import requests
from e_commerce_app import settings
import logging
from rest_framework.response import Response
from rest_framework import status
from ratelimit import limits

# Set up logging
logger = logging.getLogger(__name__)

class PaymentCreateView(generics.CreateAPIView):
    """
    View to create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def perform_create(self, serializer):
        """
        Perform the creation of a payment and update the corresponding order status.

        Args:
            serializer (PaymentSerializer): The payment serializer instance.
        """
        try:
            payment = serializer.save()
            self.update_order_status(payment.order)
        except Exception as e:
            logger.error(f'Failed to create payment: {e}')
            raise

    def update_order_status(self, order_id):
        """
        Update the status of an order to 'paid'.

        Args:
            order_id (int): The ID of the order to update.

        Raises:
            Exception: If the order status update fails.
        """
        order_service_url = settings.ORDER_SERVICE_URL
        payload = {
            'status': 'paid'
        }

        # Ensure the token is in string format
        byte_token = self.request.auth.token
        token = byte_token.decode('utf-8') if isinstance(byte_token, bytes) else byte_token

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.patch(f'{order_service_url}/api/orders/{order_id}/', json=payload, headers=headers)

        if response.status_code != 200:
            logger.error(f'Order service responded with status code {response.status_code}: {response.text}')
            raise Exception('Order status update failed')

        logger.info(f'Successfully updated order status for order {order_id}')

class PaymentDetailView(generics.RetrieveAPIView):
    """
    View to retrieve details of a specific payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific payment by its ID.

        Args:
            request (Request): The request instance.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing payment details or an error message.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Payment.DoesNotExist:
            logger.error(f'Payment with id {kwargs["pk"]} does not exist.')
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Failed to retrieve payment: {e}')
            return Response({'error': 'Failed to retrieve payment.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
