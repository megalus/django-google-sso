import httpx
from django.contrib import messages
from django.contrib.auth import logout
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


def is_user_valid(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    response = httpx.get(url, headers=headers)

    # Add any check here

    return response.status_code == 200


class GoogleSLOMiddlewareExample:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.session.get("google_sso_access_token")

        if token and not is_user_valid(token):
            logout(request)

        response = self.get_response(request)
        return response
