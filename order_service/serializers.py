from rest_framework import serializers
from .models import Order, OrderItem
import logging

# Set up logging
logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual order items.
    """
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for orders, including nested order items.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'updated_at', 'items']
        read_only_fields = ['customer', 'id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Create an order along with its items.

        Args:
            validated_data (dict): Validated data for the order and items.

        Returns:
            Order: The created order instance.
        """
        items_data = validated_data.pop('items', [])  # Default to empty list if 'items' not provided
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            try:
                product = item_data.pop('product')
                quantity = item_data.pop('quantity')
                price = item_data.pop('price')
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            except Exception as e:
                logger.error(f"Error creating order item: {e}")
                raise serializers.ValidationError("Failed to create order item")

        return order

    def update(self, instance, validated_data):
        """
        Update an order and its items.

        Args:
            instance (Order): The existing order instance.
            validated_data (dict): Validated data for the order and items.

        Returns:
            Order: The updated order instance.
        """
        items_data = validated_data.pop('items', None)  # Check if 'items' exists
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if items_data is not None:
            # Update items
            for item_data in items_data:
                try:
                    product = item_data.pop('product')
                    quantity = item_data.pop('quantity')
                    price = item_data.pop('price')
                    OrderItem.objects.update_or_create(order=instance, product=product, defaults={'quantity': quantity, 'price': price})
                except Exception as e:
                    logger.error(f"Error updating order item: {e}")
                    raise serializers.ValidationError("Failed to update order item")

        return instance
