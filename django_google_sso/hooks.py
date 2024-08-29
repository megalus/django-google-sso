from django.http import HttpRequest

from django_google_sso.models import User


def pre_login_user(user: User, request: HttpRequest) -> None:
    """
    Callback function called after user is created/retrieved but before logged in.
    """


def pre_create_user(google_user_info: dict, request: HttpRequest) -> dict | None:
    """
    Callback function called before user is created.

    params:
        google_user_info: dict containing user info received from Google.
        request: HttpRequest object.

    return: dict content to be passed to User.objects.create()
            as `defaults` argument.
            If not informed, username field (default: `username`)
            is always the user email.
    """
    return {}


def pre_validate_user(google_user_info: dict, request: HttpRequest) -> bool:
    """
    Callback function called before user is validated.

    Must return a boolean to indicate if user is valid to login.

    params:
        google_user_info: dict containing user info received from Google.
        request: HttpRequest object.
    """
    return True
