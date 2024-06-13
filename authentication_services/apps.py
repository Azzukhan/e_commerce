from django.apps import AppConfig


class AuthenticationServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication_services'

    def ready(self):
        import authentication_services.signals
