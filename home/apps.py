from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    
    def ready(self):
        # Import snippets untuk memastikan ter-register
        try:
            from .models import snippets  # noqa: F401
        except ImportError:
            pass