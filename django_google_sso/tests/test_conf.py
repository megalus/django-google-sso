def test_conf_from_settings(settings):
    # Arrange
    settings.GOOGLE_SSO_ENABLED = False

    # Act
    from django_google_sso.conf import GOOGLE_SSO_ENABLED

    # Assert
    assert GOOGLE_SSO_ENABLED is False
