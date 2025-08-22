import importlib
from copy import deepcopy
from urllib.parse import quote, urlencode

import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
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
def site_a():
    """Create a test site A with domain site.com."""
    site, _ = Site.objects.get_or_create(domain="site.com", name="Site A")
    return site


@pytest.fixture
def site_b():
    """Create a test site B with domain other-site.com."""
    site, _ = Site.objects.get_or_create(domain="other-site.com", name="Site B")
    return site


@pytest.fixture
def site_specific_settings(settings):
    """Configure site-specific settings using callables."""

    # Define site-specific auto_create_users
    def get_auto_create_users(request):
        site = request.site
        if site.domain == "site.com":
            return True  # Site A: auto-create users
        elif site.domain == "other-site.com":
            return False  # Site B: don't auto-create users
        return True  # Default

    # Define site-specific session_cookie_age
    def get_session_cookie_age(request):
        site = request.site
        if site.domain == "site.com":
            return 3600  # Site A: 1 hour
        elif site.domain == "other-site.com":
            return 86400  # Site B: 24 hours
        return 3600  # Default

    # Apply settings
    settings.GOOGLE_SSO_AUTO_CREATE_USERS = get_auto_create_users
    settings.GOOGLE_SSO_SESSION_COOKIE_AGE = get_session_cookie_age
    settings.GOOGLE_SSO_ALLOWABLE_DOMAINS = ["site.com", "other-site.com"]
    # Use the default Django authentication backend to avoid importing 'backend' module
    settings.GOOGLE_SSO_AUTHENTICATION_BACKEND = (
        "django.contrib.auth.backends.ModelBackend"
    )
    settings.AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
    return settings


@pytest.fixture
def client_with_site_a(client_with_session, site_a):
    """Client with session for site A."""
    session = client_with_session.session
    session["site_domain"] = site_a.domain
    session.save()
    return client_with_session


@pytest.fixture
def client_with_site_b(client_with_session, site_b):
    """Client with session for site B."""
    session = client_with_session.session
    session["site_domain"] = site_b.domain
    session.save()
    return client_with_session


class MockRequest:
    """Mock request object with site attribute."""


@pytest.fixture
def mock_get_sso_value(mocker, site_specific_settings):
    """
    Create a mock for GoogleAuth.get_sso_value that uses site-specific settings.

    This fixture reduces code duplication across tests by providing a common
    implementation of the mocked_get_sso_value function.
    """
    original_get_sso_value = GoogleAuth.get_sso_value

    def mocked_get_sso_value(self, key, login_failed_url=None, allowable_domains=None):
        if key == "auto_create_users" or key == "session_cookie_age":
            # Create a mock request with site attribute
            mock_request = MockRequest()
            site_domain = self.request.session.get("site_domain")
            mock_request.site = Site.objects.get(domain=site_domain)

            if key == "auto_create_users":
                return site_specific_settings.GOOGLE_SSO_AUTO_CREATE_USERS(mock_request)
            elif key == "session_cookie_age":
                return site_specific_settings.GOOGLE_SSO_SESSION_COOKIE_AGE(
                    mock_request
                )
        elif key == "login_failed_url" and login_failed_url:
            return login_failed_url
        elif key == "allowable_domains":
            # Use provided domains or default to including example.com
            return allowable_domains or ["example.com", "site.com", "other-site.com"]

        return original_get_sso_value(self, key)

    # Apply the mock
    mocker.patch.object(GoogleAuth, "get_sso_value", mocked_get_sso_value)

    return mocked_get_sso_value
