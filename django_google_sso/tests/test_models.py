import pytest

from django_google_sso.main import UserHelper

pytestmark = pytest.mark.django_db


def test_google_sso_model(google_response, callback_request, settings):
    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.googlessouser.google_id == google_response["id"]
    assert user.googlessouser.picture_url == google_response["picture"]
    assert user.googlessouser.locale == google_response["locale"]
