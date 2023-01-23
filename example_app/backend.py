from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from loguru import logger


class MyBackend(ModelBackend):
    """Simple test for custom authentication backend"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, username, password, **kwargs)


def pre_login_callback(user, request):
    """Callback function called after user is logged in."""
    messages.info(request, f"Running Pre-Login callback for user: {user}.")
    if not user.is_superuser or not user.is_staff:
        logger.info(f"Adding SuperUser status to email: {user.email}")
        user.is_superuser = True
        user.is_staff = True
        user.save()
