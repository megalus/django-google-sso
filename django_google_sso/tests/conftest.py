from copy import deepcopy
from urllib.parse import quote, urlencode

import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

from django_google_sso import conf


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
