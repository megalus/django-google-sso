from typing import Any, Callable, List

from django.conf import settings
from django.http import HttpRequest
from loguru import logger


class GoogleSSOSettings:
    """
    Settings class for Django Google SSO.

    This class implements the PEP 562 approach to avoid accessing Django settings
    at import time, which can cause issues if the module is imported before
    Django has fully initialized its settings.
    """

    def _get_setting(
        self, name: str, default: Any = None, accept_callable: bool = True
    ) -> Any:
        """Get a setting from Django settings."""
        value = getattr(settings, name, default)
        if not accept_callable and callable(value):
            raise TypeError(f"The setting {name} cannot be a callable.")
        return value

    # Configurations without callable
    @property
    def GOOGLE_SSO_ENABLED(self) -> bool:
        return self._get_setting("GOOGLE_SSO_ENABLED", True, accept_callable=False)

    @property
    def GOOGLE_SSO_ENABLE_LOGS(self) -> bool:
        value = self._get_setting("GOOGLE_SSO_ENABLE_LOGS", True, accept_callable=False)
        if value:
            logger.enable("django_google_sso")
        else:
            logger.disable("django_google_sso")
        return value

    @property
    def SSO_USE_ALTERNATE_W003(self) -> bool:
        return self._get_setting("SSO_USE_ALTERNATE_W003", False, accept_callable=False)

    # Configurations with optional callable

    @property
    def GOOGLE_SSO_LOGO_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "GOOGLE_SSO_LOGO_URL",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/"
            "Google_%22G%22_logo.svg/1280px-Google_%22G%22_logo.svg.png",
        )

    @property
    def GOOGLE_SSO_TEXT(self) -> bool | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_TEXT", "Sign in with Google")

    @property
    def GOOGLE_SSO_ADMIN_ENABLED(self) -> bool | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_ADMIN_ENABLED", None)

    @property
    def GOOGLE_SSO_PAGES_ENABLED(self) -> bool | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_PAGES_ENABLED", None)

    @property
    def GOOGLE_SSO_CLIENT_ID(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_CLIENT_ID", None)

    @property
    def GOOGLE_SSO_PROJECT_ID(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_PROJECT_ID", None)

    @property
    def GOOGLE_SSO_CLIENT_SECRET(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_CLIENT_SECRET", None)

    @property
    def GOOGLE_SSO_SCOPES(self) -> List[str] | Callable[[HttpRequest], List[str]]:
        return self._get_setting(
            "GOOGLE_SSO_SCOPES",
            [
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        )

    @property
    def GOOGLE_SSO_TIMEOUT(self) -> int | Callable[[HttpRequest], int]:
        return self._get_setting("GOOGLE_SSO_TIMEOUT", 10)

    @property
    def GOOGLE_SSO_ALLOWABLE_DOMAINS(
        self,
    ) -> List[str] | Callable[[HttpRequest], List[str]]:
        return self._get_setting("GOOGLE_SSO_ALLOWABLE_DOMAINS", [])

    @property
    def GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER", False)

    @property
    def GOOGLE_SSO_SESSION_COOKIE_AGE(self) -> int | Callable[[HttpRequest], int]:
        return self._get_setting("GOOGLE_SSO_SESSION_COOKIE_AGE", 3600)

    @property
    def GOOGLE_SSO_SUPERUSER_LIST(
        self,
    ) -> List[str] | Callable[[HttpRequest], List[str]]:
        return self._get_setting("GOOGLE_SSO_SUPERUSER_LIST", [])

    @property
    def GOOGLE_SSO_STAFF_LIST(self) -> List[str] | Callable[[HttpRequest], List[str]]:
        return self._get_setting("GOOGLE_SSO_STAFF_LIST", [])

    @property
    def GOOGLE_SSO_CALLBACK_DOMAIN(self) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_CALLBACK_DOMAIN", None)

    @property
    def GOOGLE_SSO_LOGIN_FAILED_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("GOOGLE_SSO_LOGIN_FAILED_URL", "admin:index")

    @property
    def GOOGLE_SSO_NEXT_URL(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("GOOGLE_SSO_NEXT_URL", "admin:index")

    @property
    def GOOGLE_SSO_AUTO_CREATE_USERS(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_AUTO_CREATE_USERS", True)

    @property
    def GOOGLE_SSO_AUTHENTICATION_BACKEND(
        self,
    ) -> str | Callable[[HttpRequest], str] | None:
        return self._get_setting("GOOGLE_SSO_AUTHENTICATION_BACKEND", None)

    @property
    def GOOGLE_SSO_PRE_VALIDATE_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "GOOGLE_SSO_PRE_VALIDATE_CALLBACK",
            "django_google_sso.hooks.pre_validate_user",
        )

    @property
    def GOOGLE_SSO_PRE_CREATE_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "GOOGLE_SSO_PRE_CREATE_CALLBACK",
            "django_google_sso.hooks.pre_create_user",
        )

    @property
    def GOOGLE_SSO_PRE_LOGIN_CALLBACK(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting(
            "GOOGLE_SSO_PRE_LOGIN_CALLBACK",
            "django_google_sso.hooks.pre_login_user",
        )

    @property
    def GOOGLE_SSO_SAVE_ACCESS_TOKEN(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_SAVE_ACCESS_TOKEN", False)

    @property
    def GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA", False)

    @property
    def GOOGLE_SSO_DEFAULT_LOCALE(self) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("GOOGLE_SSO_DEFAULT_LOCALE", "en")

    @property
    def GOOGLE_SSO_ENABLE_MESSAGES(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_ENABLE_MESSAGES", True)

    @property
    def GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO(self) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO", True)

    @property
    def GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE", False)

    @property
    def GOOGLE_SSO_AUTHORIZATION_PROMPT(
        self,
    ) -> str | None | Callable[[HttpRequest], str]:
        return self._get_setting("GOOGLE_SSO_AUTHORIZATION_PROMPT", "consent")

    @property
    def SSO_ADMIN_ROUTE(
        self,
    ) -> str | Callable[[HttpRequest], str]:
        return self._get_setting("SSO_ADMIN_ROUTE", "admin:index")

    @property
    def SSO_SHOW_FORM_ON_ADMIN_PAGE(
        self,
    ) -> bool | Callable[[HttpRequest], bool]:
        return self._get_setting("SSO_SHOW_FORM_ON_ADMIN_PAGE", True)


# Create a single instance of the settings class
_google_sso_settings = GoogleSSOSettings()


def __getattr__(name: str) -> Any:
    """
    Implement PEP 562 __getattr__ to lazily load settings.

    This function is called when an attribute is not found in the module's
    global namespace. It delegates to the _google_sso_settings instance.
    """
    return getattr(_google_sso_settings, name)


if _google_sso_settings.SSO_USE_ALTERNATE_W003:
    from django_google_sso.checks.warnings import register_sso_check  # noqa

if _google_sso_settings.GOOGLE_SSO_ENABLE_LOGS:
    logger.enable("django_google_sso")
else:
    logger.disable("django_google_sso")
