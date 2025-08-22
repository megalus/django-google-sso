import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.mark.parametrize(
    "client_fixture, should_create_user, login_failed_url, "
    "expected_status, expected_redirect",
    [
        # Site A: auto-creates users, login succeeds
        ("client_with_site_a", True, None, 200, None),
        # Site B: doesn't auto-create users, redirects to login failed URL
        ("client_with_site_b", False, "admin:index", None, "/admin/"),
    ],
    ids=["site_a_auto_create", "site_b_no_auto_create"],
)
def test_site_auto_create_user(
    request,
    callback_url,
    mock_get_sso_value,
    client_fixture,
    should_create_user,
    login_failed_url,
    expected_status,
    expected_redirect,
):
    """Test user auto-creation behavior based on site settings."""

    # Arrange
    User.objects.filter(email="foo@example.com").delete()
    client = request.getfixturevalue(client_fixture)

    if login_failed_url:
        # Configure the mock to return custom login_failed_url if provided
        mock_get_sso_value.__defaults__ = (
            login_failed_url,
            ["example.com", "site.com", "other-site.com"],
        )

    # Act
    response = client.get(callback_url, follow=True)

    # Assert
    if should_create_user:
        assert User.objects.filter(
            email="foo@example.com"
        ).exists(), f"User should be auto-created on {client_fixture}"
        assert client.session.get_expiry_age() > 0, "Session should have an expiry age"
        assert response.status_code == expected_status, "Login should be successful"
    else:
        assert not User.objects.filter(
            email="foo@example.com"
        ).exists(), f"User should not be auto-created on {client_fixture}"
        assert response.redirect_chain[-1][0].startswith(
            expected_redirect
        ), "Should redirect to login failed URL"


def test_existing_user_site_b_session_age(
    client_with_site_b, callback_url, mock_get_sso_value
):
    """Test that existing users on site B get a 24-hour session."""

    # Arrange
    user = User.objects.create_user(
        username="foo@example.com",
        email="foo@example.com",
        password="password",  # nosec B106
        is_active=True,
    )

    # Act
    response = client_with_site_b.get(callback_url, follow=True)

    # Assert
    assert response.status_code == 200, "Login should be successful for existing user"
    assert (
        client_with_site_b.session.get_expiry_age() > 0
    ), "Session should have an expiry age"

    # Clean up
    user.delete()
