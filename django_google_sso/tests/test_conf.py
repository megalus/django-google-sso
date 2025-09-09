from django_google_sso import conf


def test_conf_from_settings(settings):
    # Arrange
    settings.GOOGLE_SSO_ENABLED = False

    # Assert
    assert conf.GOOGLE_SSO_ENABLED is False
