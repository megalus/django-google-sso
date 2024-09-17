import importlib
from urllib.parse import urlparse

from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from loguru import logger

from django_google_sso import conf
from django_google_sso.main import GoogleAuth, UserHelper
from django_google_sso.utils import send_message, show_credential


@require_http_methods(["GET"])
def start_login(request: HttpRequest) -> HttpResponseRedirect:
    # Get the next url
    next_param = request.GET.get(key="next")
    if next_param:
        clean_param = (
            next_param
            if next_param.startswith("http") or next_param.startswith("/")
            else f"//{next_param}"
        )
    else:
        clean_param = reverse(conf.GOOGLE_SSO_NEXT_URL)
    next_path = urlparse(clean_param).path

    # Get Google Auth URL
    google = GoogleAuth(request)
    auth_url, state = google.flow.authorization_url(prompt="consent")

    # Save data on Session
    if not request.session.session_key:
        request.session.create()
    request.session.set_expiry(conf.GOOGLE_SSO_TIMEOUT * 60)
    request.session["sso_state"] = state
    request.session["sso_next_url"] = next_path
    request.session.save()

    # Redirect User
    return HttpResponseRedirect(auth_url)


@require_http_methods(["GET"])
def callback(request: HttpRequest) -> HttpResponseRedirect:
    login_failed_url = reverse(conf.GOOGLE_SSO_LOGIN_FAILED_URL)
    google = GoogleAuth(request)
    code = request.GET.get("code")
    state = request.GET.get("state")

    # Check if Google SSO is enabled
    if not conf.GOOGLE_SSO_ENABLED:
        send_message(request, _("Google SSO not enabled."))
        return HttpResponseRedirect(login_failed_url)

    # First, check for authorization code
    if not code:
        send_message(request, _("Authorization Code not received from SSO."))
        return HttpResponseRedirect(login_failed_url)

    # Then, check state.
    request_state = request.session.get("sso_state")
    next_url = request.session.get("sso_next_url")

    if not request_state or state != request_state:
        send_message(request, _("State Mismatch. Time expired?"))
        return HttpResponseRedirect(login_failed_url)

    # Get Access Token from Google
    try:
        google.flow.fetch_token(code=code)
    except Exception as error:
        send_message(request, _(f"Error while fetching token from SSO: {error}."))
        logger.debug(
            f"GOOGLE_SSO_CLIENT_ID: {show_credential(conf.GOOGLE_SSO_CLIENT_ID)}"
        )
        logger.debug(
            f"GOOGLE_SSO_PROJECT_ID: {show_credential(conf.GOOGLE_SSO_PROJECT_ID)}"
        )
        logger.debug(
            f"GOOGLE_SSO_CLIENT_SECRET: "
            f"{show_credential(conf.GOOGLE_SSO_CLIENT_SECRET)}"
        )
        return HttpResponseRedirect(login_failed_url)

    # Get User Info from Google
    google_user_data = google.get_user_info()
    user_helper = UserHelper(google_user_data, request)

    # Run Pre-Validate Callback
    module_path = ".".join(conf.GOOGLE_SSO_PRE_VALIDATE_CALLBACK.split(".")[:-1])
    pre_validate_fn = conf.GOOGLE_SSO_PRE_VALIDATE_CALLBACK.split(".")[-1]
    module = importlib.import_module(module_path)
    user_is_valid = getattr(module, pre_validate_fn)(google_user_data, request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid or not user_is_valid:
        send_message(
            request,
            _(
                f"Email address not allowed: {user_helper.user_email}. "
                f"Please contact your administrator."
            ),
        )
        return HttpResponseRedirect(login_failed_url)

    # Save Token in Session
    if conf.GOOGLE_SSO_SAVE_ACCESS_TOKEN:
        access_token = google.get_user_token()
        request.session["google_sso_access_token"] = access_token

    # Run Pre-Create Callback
    module_path = ".".join(conf.GOOGLE_SSO_PRE_CREATE_CALLBACK.split(".")[:-1])
    pre_login_fn = conf.GOOGLE_SSO_PRE_CREATE_CALLBACK.split(".")[-1]
    module = importlib.import_module(module_path)
    extra_users_args = getattr(module, pre_login_fn)(google_user_data, request)

    # Get or Create User
    if conf.GOOGLE_SSO_AUTO_CREATE_USERS:
        user = user_helper.get_or_create_user(extra_users_args)
    else:
        user = user_helper.find_user()

    if not user or not user.is_active:
        failed_login_message = f"User not found - Email: '{google_user_data['email']}'"
        if not user and not conf.GOOGLE_SSO_AUTO_CREATE_USERS:
            failed_login_message += ". Auto-Create is disabled."

        if user and not user.is_active:
            failed_login_message = f"User is not active: '{google_user_data['email']}'"

        if conf.GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE:
            send_message(request, _(failed_login_message), level="warning")
        else:
            logger.warning(failed_login_message)

        return HttpResponseRedirect(login_failed_url)

    request.session.save()

    # Run Pre-Login Callback
    module_path = ".".join(conf.GOOGLE_SSO_PRE_LOGIN_CALLBACK.split(".")[:-1])
    pre_login_fn = conf.GOOGLE_SSO_PRE_LOGIN_CALLBACK.split(".")[-1]
    module = importlib.import_module(module_path)
    getattr(module, pre_login_fn)(user, request)

    # Login User
    login(request, user, conf.GOOGLE_SSO_AUTHENTICATION_BACKEND)
    request.session.set_expiry(conf.GOOGLE_SSO_SESSION_COOKIE_AGE)

    return HttpResponseRedirect(next_url or reverse(conf.GOOGLE_SSO_NEXT_URL))
