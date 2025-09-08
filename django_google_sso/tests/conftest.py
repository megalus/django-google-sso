import importlib
from copy import deepcopy
from typing import Generator
from urllib.parse import quote, urlencode

import pytest
from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import connection, models
from django.urls import reverse

from django_google_sso import conf
from django_google_sso import conf as conf_module
from django_google_sso.main import GoogleAuth

SECRET_PATH = "/secret/"


@pytest.fixture
def query_string():
    return urlencode(
        {
            "code": "12345",
            "state": "foo",
            "scope": " ".join(conf.GOOGLE_SSO_SCOPES),
            "hd": "example.com",
            "prompt": "consent",
        },
        quote_via=quote,
    )


@pytest.fixture
def google_response():
    return {
        "id": "12345",
        "email": "foo@example.com",
        "verified_email": True,
        "name": "Bruce Wayne",
        "given_name": "Bruce",
        "family_name": "Wayne",
        "picture": "https://lh3.googleusercontent.com/a-/12345",
        "locale": "en-US",
        "hd": "example.com",
    }


@pytest.fixture
def google_response_update():
    return {
        "id": "12345",
        "email": "foo@example.com",
        "verified_email": True,
        "name": "Clark Kent",
        "given_name": "Clark",
        "family_name": "Kent",
        "picture": "https://lh3.googleusercontent.com/a-/12345",
        "locale": "en-US",
        "hd": "example.com",
    }


@pytest.fixture
def callback_request(rf, query_string):
    request = rf.get(f"/google_sso/callback/?{query_string}")
    middleware = SessionMiddleware(get_response=lambda req: None)
    middleware.process_request(request)
    request.session.save()
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.fixture
def callback_request_from_reverse_proxy(rf, query_string):
    request = rf.get(
        f"/google_sso/callback/?{query_string}", HTTP_X_FORWARDED_PROTO="https"
    )
    middleware = SessionMiddleware(get_response=lambda req: None)
    middleware.process_request(request)
    request.session.save()
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.fixture
def callback_request_with_state(callback_request):
    request = deepcopy(callback_request)
    request.session["sso_state"] = "foo"
    request.session["sso_next_url"] = "/secret/"
    return request


@pytest.fixture
def client_with_session(client, settings, mocker, google_response):
    settings.GOOGLE_SSO_ALLOWABLE_DOMAINS = ["example.com"]
    settings.GOOGLE_SSO_PRE_LOGIN_CALLBACK = "django_google_sso.hooks.pre_login_user"
    settings.GOOGLE_SSO_PRE_CREATE_CALLBACK = "django_google_sso.hooks.pre_create_user"
    settings.GOOGLE_SSO_PRE_VALIDATE_CALLBACK = (
        "django_google_sso.hooks.pre_validate_user"
    )
    importlib.reload(conf)
    session = client.session
    session.update({"sso_state": "foo", "sso_next_url": SECRET_PATH})
    session.save()
    mocker.patch.object(GoogleAuth, "flow")
    mocker.patch.object(GoogleAuth, "get_user_info", return_value=google_response)
    mocker.patch.object(GoogleAuth, "get_user_token", return_value="12345")
    yield client


@pytest.fixture
def callback_url(query_string):
    return f"{reverse('django_google_sso:oauth_callback')}?{query_string}"


@pytest.fixture
def custom_user_model(settings) -> Generator[type, None, None]:
    """
    Create a temporary custom user model, point AUTH_USER_MODEL to it,
    recreate GoogleSSOUser table to reference the new model, yield the
    custom user class and then fully restore the previous state.
    """
    # Capture previous state
    old_auth = settings.AUTH_USER_MODEL
    import django_google_sso.models as gg_models

    old_googlessouser = gg_models.GoogleSSOUser

    class CustomNamesUser(AbstractBaseUser):
        user_name = models.CharField(max_length=150, unique=True)
        mail = models.EmailField(unique=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        USERNAME_FIELD = "user_name"
        EMAIL_FIELD = "mail"
        REQUIRED_FIELDS = ["mail"]

        class Meta:
            app_label = "django_google_sso"

        def __str__(self) -> str:
            return self.user_name

    # Register dynamic model and create its table
    apps.register_model("django_google_sso", CustomNamesUser)
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(CustomNamesUser)

    # Point to the new user model and reload conf + models so relations are rebuilt
    settings.AUTH_USER_MODEL = "django_google_sso.CustomNamesUser"
    importlib.reload(conf_module)
    gg_models = importlib.reload(gg_models)

    # Replace GoogleSSOUser DB table so its FK points to the new user model
    new_googlessouser = gg_models.GoogleSSOUser
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(old_googlessouser)
        schema_editor.create_model(new_googlessouser)

    try:
        yield CustomNamesUser
    finally:
        # Teardown: remove new tables and restore original model/table
        gg_models = importlib.reload(gg_models)
        new_googlessouser = gg_models.GoogleSSOUser

        with connection.schema_editor() as schema_editor:
            # delete the GoogleSSOUser table that references the dynamic user
            schema_editor.delete_model(new_googlessouser)
            # delete the dynamic user table
            schema_editor.delete_model(CustomNamesUser)

        # restore AUTH_USER_MODEL and reload modules
        settings.AUTH_USER_MODEL = old_auth
        importlib.reload(conf_module)
        importlib.reload(gg_models)

        # recreate the original GoogleSSOUser table created by migrations
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(old_googlessouser)

        # unregister the dynamic model from the apps registry and clear caches
        app_models = apps.all_models.get("django_google_sso", {})
        app_models.pop("customnamesuser", None)
        apps.clear_cache()

        importlib.reload(importlib.import_module("django_google_sso.main"))
