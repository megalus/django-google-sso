import importlib

import pytest

from django_google_sso.main import UserHelper

pytestmark = pytest.mark.django_db(transaction=True)


def test_google_sso_model(google_response, callback_request, settings):
    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.googlessouser.google_id == google_response["id"]
    assert user.googlessouser.picture_url == google_response["picture"]
    assert user.googlessouser.locale == google_response["locale"]


def test_very_long_picture_url(google_response, callback_request, settings):
    # Arrange
    google_response["picture"] += "a" * 1900

    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert len(user.googlessouser.picture_url) == len(google_response["picture"])


def test_user_with_custom_field_names(
    custom_user_model, google_response, callback_request
):
    # Arrange
    importlib.reload(importlib.import_module("django_google_sso.main"))
    from django_google_sso.main import UserHelper

    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.user_name == "foo@example.com"
    assert user.mail == "foo@example.com"
