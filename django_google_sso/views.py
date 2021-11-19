from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_google_sso import conf
from django_google_sso.main import GoogleAuth, UserHelper

ADMIN_URL = reverse("admin:index")


@require_http_methods(["GET"])
def start_login(request):
    google = GoogleAuth(request)
    auth_url, _ = google.flow.authorization_url(prompt="consent")
    return HttpResponseRedirect(auth_url)


@require_http_methods(["GET"])
def callback(request):
    google = GoogleAuth(request)
    code = request.GET.get("code")

    # Check if Google SSO is enabled
    if not conf.GOOGLE_SSO_ENABLED:
        messages.add_message(request, messages.ERROR, _("Google SSO not enabled."))
        return HttpResponseRedirect(ADMIN_URL)

    # First, check for authorization code
    if not code:
        messages.add_message(
            request, messages.ERROR, _("Authorization Code not received from SSO.")
        )
        return HttpResponseRedirect(ADMIN_URL)

    # Get Access Token from Google
    try:
        google.flow.fetch_token(code=code)
    except Exception as error:
        messages.add_message(request, messages.ERROR, str(error))
        return HttpResponseRedirect(ADMIN_URL)

    # Get User Info from Google
    user_helper = UserHelper(google.get_user_info(), request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid:
        messages.add_message(
            request,
            messages.ERROR,
            _(
                f"Email address not allowed: {user_helper.user_email}"
                f"\nPlease contact your administrator."
            ),
        )
        return HttpResponseRedirect(ADMIN_URL)

    # Get or Create User
    user = user_helper.get_or_create_user()

    if not user.is_active:
        return HttpResponseRedirect(ADMIN_URL)

    # Login User
    login(request, user)
    request.session.set_expiry(conf.GOOGLE_SSO_SESSION_COOKIE_AGE)

    return HttpResponseRedirect(ADMIN_URL)
