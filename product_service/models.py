from django.db import models, transaction

class Product(models.Model):
    """
    Model representing a product in the e-commerce system.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()

    def __str__(self):
        """
        String representation of the product, returning its name.
        """
        return self.name

    @transaction.atomic
    def update_inventory(self, quantity):
        """
        Update the inventory of the product.

        Args:
            quantity (int): The quantity to reduce from inventory.

        Raises:
            ValueError: If the inventory is insufficient to cover the quantity.
        """
        # Use select_for_update to lock the row until the end of the transaction
        product = Product.objects.select_for_update().get(pk=self.pk)
        
        # Check if there is enough inventory
        if product.inventory >= quantity:
            product.inventory -= quantity
            product.save()  # Save changes to the database
        else:
            # Raise an error if not enough inventory
            raise ValueError('Not enough inventory')
