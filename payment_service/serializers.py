from rest_framework import serializers
from .models import Payment
import logging

logger = logging.getLogger(__name__)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            payment = Payment.objects.create(**validated_data)
            return payment
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise serializers.ValidationError("Failed to create payment")

    def update(self, instance, validated_data):
        try:
            instance.amount = validated_data.get('amount', instance.amount)
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance
        except Exception as e:
            logger.error(f"Error updating payment: {e}")
            raise serializers.ValidationError("Failed to update payment")
