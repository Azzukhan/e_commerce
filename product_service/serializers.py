from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model with validation for price and inventory.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory']

    def validate_price(self, value):
        # Ensure that the price is greater than zero
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_inventory(self, value):
        # Ensure that the inventory is not negative
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative.")
        return value
