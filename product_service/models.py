# product_service/models.py
from django.db import models, transaction

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @transaction.atomic
    def update_inventory(self, quantity):
        product = Product.objects.select_for_update().get(pk=self.pk)
        if product.inventory >= quantity:
            product.inventory -= quantity
            product.save()
        else:
            raise ValueError('Not enough inventory')
