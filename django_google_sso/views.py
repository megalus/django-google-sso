import importlib
from urllib.parse import urlparse

from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from loguru import logger

from django_google_sso.main import GoogleAuth, UserHelper
from django_google_sso.utils import send_message, show_credential


@require_http_methods(["GET"])
def start_login(request: HttpRequest) -> HttpResponseRedirect:
    google = GoogleAuth(request)

    # Get the next url
    next_param = request.GET.get(key="next")
    if next_param:
        clean_param = (
            next_param
            if next_param.startswith("http") or next_param.startswith("/")
            else f"//{next_param}"
        )
    else:
        next_url = google.get_sso_value("next_url")
        clean_param = reverse(next_url)
    next_path = urlparse(clean_param).path

    # Get Google Auth URL
    prompt = google.get_sso_value("authorization_prompt")
    auth_url, state = google.flow.authorization_url(prompt=prompt)

    # Save data on Session
    timeout = google.get_sso_value("timeout")
    if not request.session.session_key:
        request.session.create()
    request.session.set_expiry(timeout * 60)
    request.session["sso_state"] = state
    request.session["sso_next_url"] = next_path
    request.session.save()

    # Redirect User
    return HttpResponseRedirect(auth_url)


@require_http_methods(["GET"])
def callback(request: HttpRequest) -> HttpResponseRedirect:
    google = GoogleAuth(request)
    login_failed_url = reverse(google.get_sso_value("login_failed_url"))
    code = request.GET.get("code")
    state = request.GET.get("state")

    next_url_from_session = request.session.get("sso_next_url")
    next_url_from_conf = reverse(google.get_sso_value("next_url"))
    next_url = next_url_from_session if next_url_from_session else next_url_from_conf

    # Check if Google SSO is enabled
    enabled, message = google.check_enabled(next_url)
    if not enabled:
        send_message(request, _(message))
        return HttpResponseRedirect(login_failed_url)

    # First, check for authorization code
    if not code:
        send_message(request, _("Authorization Code not received from SSO."))
        return HttpResponseRedirect(login_failed_url)

    # Then, check state.
    request_state = request.session.get("sso_state")

    if not request_state or state != request_state:
        send_message(request, _("State Mismatch. Time expired?"))
        return HttpResponseRedirect(login_failed_url)

    # Get Access Token from Google
    try:
        google.flow.fetch_token(code=code)
    except Exception as error:
        send_message(request, _(f"Error while fetching token from SSO: {error}."))
        logger.debug(
            f"GOOGLE_SSO_CLIENT_ID: "
            f"{show_credential(google.get_sso_value('client_id'))}"
        )
        logger.debug(
            f"GOOGLE_SSO_PROJECT_ID: "
            f"{show_credential(google.get_sso_value('project_id'))}"
        )
        logger.debug(
            f"GOOGLE_SSO_CLIENT_SECRET: "
            f"{show_credential(google.get_sso_value('client_secret'))}"
        )
        return HttpResponseRedirect(login_failed_url)

    # Get User Info from Google
    google_user_data = google.get_user_info()
    user_helper = UserHelper(google_user_data, request)

    # Run Pre-Validate Callback
    pre_validate_callback = google.get_sso_value("pre_validate_callback")
    module_path = ".".join(pre_validate_callback.split(".")[:-1])
    pre_validate_fn = pre_validate_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    user_is_valid = getattr(module, pre_validate_fn)(google_user_data, request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid or not user_is_valid:
        send_message(
            request,
            _(
                f"Email address not allowed: {user_helper.user_info_email}. "
                f"Please contact your administrator."
            ),
        )
        return HttpResponseRedirect(login_failed_url)

    # Save Token in Session
    save_access_token = google.get_sso_value("save_access_token")
    if save_access_token:
        access_token = google.get_user_token()
        request.session["google_sso_access_token"] = access_token

    # Run Pre-Create Callback
    pre_create_callback = google.get_sso_value("pre_create_callback")
    module_path = ".".join(pre_create_callback.split(".")[:-1])
    pre_login_fn = pre_create_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    extra_users_args = getattr(module, pre_login_fn)(google_user_data, request)

    # Get or Create User
    auto_create_users = google.get_sso_value("auto_create_users")
    if auto_create_users:
        user = user_helper.get_or_create_user(extra_users_args)
    else:
        user = user_helper.find_user()

    if not user or not user.is_active:
        failed_login_message = f"User not found - Email: '{google_user_data['email']}'"
        if not user and not auto_create_users:
            failed_login_message += ". Auto-Create is disabled."

        if user and not user.is_active:
            failed_login_message = f"User is not active: '{google_user_data['email']}'"

        show_failed_login_message = google.get_sso_value("show_failed_login_message")
        if show_failed_login_message:
            send_message(request, _(failed_login_message), level="warning")
        else:
            logger.warning(failed_login_message)

        return HttpResponseRedirect(login_failed_url)

    request.session.save()

    # Run Pre-Login Callback
    pre_login_callback = google.get_sso_value("pre_login_callback")
    module_path = ".".join(pre_login_callback.split(".")[:-1])
    pre_login_fn = pre_login_callback.split(".")[-1]
    module = importlib.import_module(module_path)
    getattr(module, pre_login_fn)(user, request)

    # Get Authentication Backend
    # If exists, let's make a sanity check on it
    # Because Django does not raise errors if backend is wrong
    authentication_backend = google.get_sso_value("authentication_backend")
    if authentication_backend:
        module_path = ".".join(authentication_backend.split(".")[:-1])
        backend_auth_class = authentication_backend.split(".")[-1]
        try:
            module = importlib.import_module(module_path)
            getattr(module, backend_auth_class)
        except (ImportError, AttributeError) as error:
            raise ImportError(
                f"Authentication Backend invalid: {authentication_backend}"
            ) from error

    # Login User
    cookie_age = google.get_sso_value("session_cookie_age")
    login(request, user, authentication_backend)
    request.session.set_expiry(cookie_age)

    return HttpResponseRedirect(next_url)
