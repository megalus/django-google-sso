import pytest
from django.contrib.sites.models import Site

from django_google_sso import conf
from django_google_sso.main import GoogleAuth

pytestmark = pytest.mark.django_db


def test_scopes(callback_request):
    # Arrange
    google = GoogleAuth(callback_request)

    # Assert
    assert google.scopes == conf.GOOGLE_SSO_SCOPES


def test_get_client_config(monkeypatch, callback_request):
    # Arrange
    monkeypatch.setattr(conf, "GOOGLE_SSO_CLIENT_ID", "client_id")
    monkeypatch.setattr(conf, "GOOGLE_SSO_PROJECT_ID", "project_id")
    monkeypatch.setattr(conf, "GOOGLE_SSO_CLIENT_SECRET", "redirect_uri")
    monkeypatch.setattr(conf, "GOOGLE_SSO_CALLBACK_DOMAIN", "localhost:8000")

    # Act
    google = GoogleAuth(callback_request)

    # Assert
    assert google.get_client_config() == {
        "web": {
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_id": "client_id",
            "client_secret": "redirect_uri",
            "project_id": "project_id",
            "redirect_uris": ["http://localhost:8000/google_sso/callback/"],
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def test_get_redirect_uri_from_http(callback_request, monkeypatch):
    # Arrange
    expected_scheme = "http"
    monkeypatch.setattr(conf, "GOOGLE_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain

    # Act
    google = GoogleAuth(callback_request)

    # Assert
    assert (
        google.get_redirect_uri()
        == f"{expected_scheme}://{current_site_domain}/google_sso/callback/"
    )


def test_get_redirect_uri_from_reverse_proxy(
    callback_request_from_reverse_proxy, monkeypatch
):
    # Arrange
    expected_scheme = "https"
    monkeypatch.setattr(conf, "GOOGLE_SSO_CALLBACK_DOMAIN", None)
    current_site_domain = Site.objects.get_current().domain

    # Act
    google = GoogleAuth(callback_request_from_reverse_proxy)

    # Assert
    assert (
        google.get_redirect_uri()
        == f"{expected_scheme}://{current_site_domain}/google_sso/callback/"
    )


def test_redirect_uri_with_custom_domain(
    callback_request_from_reverse_proxy, monkeypatch
):
    # Arrange
    monkeypatch.setattr(conf, "GOOGLE_SSO_CALLBACK_DOMAIN", "my-other-domain.com")

    # Act
    google = GoogleAuth(callback_request_from_reverse_proxy)

    # Assert
    assert (
        google.get_redirect_uri() == "https://my-other-domain.com/google_sso/callback/"
    )
