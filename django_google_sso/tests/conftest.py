import importlib
from copy import deepcopy
from urllib.parse import quote, urlencode

import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from django_google_sso import conf
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
