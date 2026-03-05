import pytest
from django.test import RequestFactory
from django.urls import reverse

from django_google_sso.main import GoogleAuth
from django_google_sso.views import callback

pytestmark = pytest.mark.django_db(transaction=True)


def test_start_login_saves_code_verifier(client, mocker):
    # Arrange
    flow_mock = mocker.patch.object(GoogleAuth, "flow")
    flow_mock.authorization_url.return_value = ("https://foo/bar", "foo")
    # Mock code_verifier as a string
    type(flow_mock).code_verifier = mocker.PropertyMock(return_value="test_verifier")

    # Act
    url = reverse("django_google_sso:oauth_start_login")
    client.get(url)

    # Assert
    assert client.session["sso_code_verifier"] == "test_verifier"


def test_callback_restores_code_verifier(mocker):
    # Arrange
    rf = RequestFactory()
    url = reverse("django_google_sso:oauth_callback") + "?code=123&state=good_state"
    request = rf.get(url)
    request.session = mocker.MagicMock()
    request.session.get.side_effect = {
        "sso_state": "good_state",
        "sso_code_verifier": "saved_verifier",
    }.get

    flow_mock = mocker.patch.object(GoogleAuth, "flow")
    # Mock user info call which happens after fetch_token
    mocker.patch.object(
        GoogleAuth,
        "get_user_info",
        return_value={"email": "test@example.com", "id": "123", "verified_email": True},
    )

    # Mock other things to avoid database errors/logic
    mocker.patch("django_google_sso.views.UserHelper")
    mocker.patch("django_google_sso.views.importlib.import_module")
    mocker.patch("django_google_sso.views.login")
    mocker.patch("django_google_sso.views.send_message")

    # Act
    callback(request)

    # Assert
    # Check if code_verifier was set on the flow mock before fetch_token
    assert flow_mock.code_verifier == "saved_verifier"
    flow_mock.fetch_token.assert_called_once_with(code="123")
