from django.http import HttpRequest
from django.urls import reverse

from django_google_sso import conf


def is_admin_path(request: HttpRequest) -> bool:
    """Check if the request path is for the admin interface.

    This function checks if the current request path starts with the admin route
    defined in the settings. It also checks the 'next' parameter in the GET request
    and the 'sso_next_url' in the session to determine if the next destination is
    the admin interface.

    """
    admin_route = conf.SSO_ADMIN_ROUTE
    if callable(admin_route):
        admin_route = admin_route(request)
    return (
        request.path.startswith(reverse(admin_route))
        or request.GET.get("next", "").startswith(reverse(admin_route))
        or request.session.get("sso_next_url", "").startswith(reverse(admin_route))
    )


def is_page_path(request: HttpRequest) -> bool:
    return not is_admin_path(request)
