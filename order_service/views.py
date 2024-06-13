import logging
import requests
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from ratelimit import limits

# Set up logging
logger = logging.getLogger(__name__)

class OrderCreateView(generics.CreateAPIView):
    """
    View to create a new order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def perform_create(self, serializer):
        """
        Perform the creation of an order, including inventory updates and payment creation.

        Args:
            serializer (OrderSerializer): The order serializer instance.
        """
        try:
            order = serializer.save(customer=self.request.user)
            order_total = self.calculate_order_total(serializer.validated_data)
            self.update_product_inventory(serializer.validated_data)
            self.create_payment(order.id, order_total)
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_order_total(self, order_data):
        """
        Calculate the total cost of the order.

        Args:
            order_data (dict): Data of the order.

        Returns:
            float: The total cost of the order.
        """
        items = order_data.get('items', [])
        total = 0

        for item in items:
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            total += int(quantity) * float(price)

        return total

    def update_product_inventory(self, order_data):
        """
        Update the inventory for products in the order.

        Args:
            order_data (dict): Data of the order.

        Raises:
            Exception: If the inventory update fails.
        """
        product_service_url = settings.PRODUCT_SERVICE_URL

        for item in order_data.get('items', []):
            product_id = item.get('product')
            quantity = item.get('quantity', 0)

            url = f'{product_service_url}/products/{product_id}/update_inventory/'
            payload = {'quantity': quantity}

            headers = {
                'Authorization': f'Bearer {self.request.auth.token}',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logging.info(f'Inventory updated successfully: {response.json()}')
            except requests.exceptions.HTTPError as http_err:
                logger.error(f'HTTP error occurred: {http_err}')
                raise Exception("Failed to update inventory due to HTTP error")
            except Exception as err:
                logger.error(f'Other error occurred: {err}')
                raise Exception("Failed to update inventory due to unknown error")

    def create_payment(self, order_id, amount):
        """
        Create a payment for the order.

        Args:
            order_id (int): The ID of the order.
            amount (float): The total amount of the order.

        Raises:
            Exception: If the payment creation fails.
        """
        payment_service_url = settings.PAYMENT_SERVICE_URL
        payload = {
            'order': order_id,
            'amount': amount
        }

        headers = {
            'Authorization': f'Bearer {self.request.auth.token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(f'{payment_service_url}/api/payments/', json=payload, headers=headers)
            response.raise_for_status()
            logging.info(f'Payment created successfully: {response.json()}')
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
            raise Exception("Failed to create payment due to HTTP error")
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
            raise Exception("Failed to create payment due to unknown error")

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderUpdateView(generics.UpdateAPIView):
    """
    View to update an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderListView(generics.ListAPIView):
    """
    View to list all orders for the authenticated user.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the list of orders for the authenticated user.

        Returns:
            QuerySet: A queryset of the user's orders.
        """
        user = self.request.user
        try:
            return Order.objects.filter(customer=user)
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            raise Exception("Failed to fetch orders")
