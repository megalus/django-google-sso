import importlib

import pytest

from django_google_sso import conf
from django_google_sso.main import UserHelper

pytestmark = pytest.mark.django_db


def test_user_email(google_response, callback_request):
    # Act
    helper = UserHelper(google_response, callback_request)

    # Assert
    assert helper.user_email == "foo@example.com"


@pytest.mark.parametrize(
    "allowable_domains, expected_result", [(["example.com"], True), ([], False)]
)
def test_email_is_valid(
    google_response, callback_request, allowable_domains, expected_result, settings
):
    # Arrange
    settings.GOOGLE_SSO_ALLOWABLE_DOMAINS = allowable_domains
    importlib.reload(conf)

    # Act
    helper = UserHelper(google_response, callback_request)

    # Assert
    assert helper.email_is_valid == expected_result


@pytest.mark.parametrize("auto_create_super_user", [True, False])
def test_get_or_create_user(
    auto_create_super_user, google_response, callback_request, settings
):
    # Arrange
    settings.GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = auto_create_super_user
    importlib.reload(conf)

    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.first_name == google_response["given_name"]
    assert user.last_name == google_response["family_name"]
    assert user.username == google_response["email"]
    assert user.email == google_response["email"]
    assert user.is_active is True
    assert user.is_staff == auto_create_super_user
    assert user.is_superuser == auto_create_super_user


@pytest.mark.parametrize(
    "always_update_user_data, expected_is_equal", [(True, True), (False, False)]
)
def test_update_existing_user_record(
    always_update_user_data,
    google_response,
    google_response_update,
    callback_request,
    expected_is_equal,
    settings,
):
    # Arrange
    settings.GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA = always_update_user_data
    importlib.reload(conf)
    helper = UserHelper(google_response, callback_request)
    helper.get_or_create_user()

    # Act
    helper = UserHelper(google_response_update, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert (
        user.first_name == google_response_update["given_name"]
    ) == expected_is_equal
    assert (
        user.last_name == google_response_update["family_name"]
    ) == expected_is_equal
    assert user.username == google_response_update["email"]
    assert user.email == google_response_update["email"]


def test_create_staff_from_list(google_response, callback_request, settings):
    # Arrange
    settings.GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    settings.GOOGLE_SSO_STAFF_LIST = [google_response["email"]]
    importlib.reload(conf)

    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is False


def test_create_super_user_from_list(google_response, callback_request, settings):
    # Arrange
    settings.GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    settings.GOOGLE_SSO_SUPERUSER_LIST = [google_response["email"]]
    importlib.reload(conf)

    # Act
    helper = UserHelper(google_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True
