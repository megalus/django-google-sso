import importlib


def test_conf_from_settings(settings):
    # Arrange
    settings.GOOGLE_SSO_ENABLED = False

    # Act
    from django_google_sso import conf

    importlib.reload(conf)

    # Assert
    assert conf.GOOGLE_SSO_ENABLED is False
