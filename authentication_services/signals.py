from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# This signal handler creates an authentication token for the user 
# whenever a new user is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create a new token for the newly created user instance
        Token.objects.create(user=instance)
