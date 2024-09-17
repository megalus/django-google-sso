from django.conf import settings
from loguru import logger

GOOGLE_SSO_CLIENT_ID = getattr(settings, "GOOGLE_SSO_CLIENT_ID", None)

GOOGLE_SSO_PROJECT_ID = getattr(settings, "GOOGLE_SSO_PROJECT_ID", None)
GOOGLE_SSO_CLIENT_SECRET = getattr(settings, "GOOGLE_SSO_CLIENT_SECRET", None)
GOOGLE_SSO_SCOPES = getattr(
    settings,
    "GOOGLE_SSO_SCOPES",
    [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)
GOOGLE_SSO_TIMEOUT = getattr(settings, "GOOGLE_SSO_TIMEOUT", 10)

GOOGLE_SSO_ALLOWABLE_DOMAINS = getattr(settings, "GOOGLE_SSO_ALLOWABLE_DOMAINS", [])
GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = getattr(
    settings, "GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER", False
)
GOOGLE_SSO_SESSION_COOKIE_AGE = getattr(settings, "GOOGLE_SSO_SESSION_COOKIE_AGE", 3600)
GOOGLE_SSO_ENABLED = getattr(settings, "GOOGLE_SSO_ENABLED", True)
GOOGLE_SSO_SUPERUSER_LIST = getattr(settings, "GOOGLE_SSO_SUPERUSER_LIST", [])
GOOGLE_SSO_STAFF_LIST = getattr(settings, "GOOGLE_SSO_STAFF_LIST", [])
GOOGLE_SSO_CALLBACK_DOMAIN = getattr(settings, "GOOGLE_SSO_CALLBACK_DOMAIN", None)
GOOGLE_SSO_LOGIN_FAILED_URL = getattr(
    settings, "GOOGLE_SSO_LOGIN_FAILED_URL", "admin:index"
)
GOOGLE_SSO_NEXT_URL = getattr(settings, "GOOGLE_SSO_NEXT_URL", "admin:index")
GOOGLE_SSO_AUTO_CREATE_USERS = getattr(settings, "GOOGLE_SSO_AUTO_CREATE_USERS", True)

GOOGLE_SSO_AUTHENTICATION_BACKEND = getattr(
    settings, "GOOGLE_SSO_AUTHENTICATION_BACKEND", None
)
GOOGLE_SSO_PRE_VALIDATE_CALLBACK = getattr(
    settings,
    "GOOGLE_SSO_PRE_VALIDATE_CALLBACK",
    "django_google_sso.hooks.pre_validate_user",
)
GOOGLE_SSO_PRE_CREATE_CALLBACK = getattr(
    settings,
    "GOOGLE_SSO_PRE_CREATE_CALLBACK",
    "django_google_sso.hooks.pre_create_user",
)
GOOGLE_SSO_PRE_LOGIN_CALLBACK = getattr(
    settings,
    "GOOGLE_SSO_PRE_LOGIN_CALLBACK",
    "django_google_sso.hooks.pre_login_user",
)

GOOGLE_SSO_LOGO_URL = getattr(
    settings,
    "GOOGLE_SSO_LOGO_URL",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/"
    "Google_%22G%22_logo.svg/1280px-Google_%22G%22_logo.svg.png",
)

GOOGLE_SSO_TEXT = getattr(settings, "GOOGLE_SSO_TEXT", "Sign in with Google")
GOOGLE_SSO_SAVE_ACCESS_TOKEN = getattr(settings, "GOOGLE_SSO_SAVE_ACCESS_TOKEN", False)
GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA = getattr(
    settings, "GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA", False
)
GOOGLE_SSO_DEFAULT_LOCALE = getattr(settings, "GOOGLE_SSO_DEFAULT_LOCALE", "en")
SSO_USE_ALTERNATE_W003 = getattr(settings, "SSO_USE_ALTERNATE_W003", False)

if SSO_USE_ALTERNATE_W003:
    from django_google_sso.checks.warnings import register_sso_check  # noqa

GOOGLE_SSO_ENABLE_LOGS = getattr(settings, "GOOGLE_SSO_ENABLE_LOGS", True)
GOOGLE_SSO_ENABLE_MESSAGES = getattr(settings, "GOOGLE_SSO_ENABLE_MESSAGES", True)
GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO = getattr(
    settings, "GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO", True
)
GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE = getattr(
    settings, "GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE", False
)

if GOOGLE_SSO_ENABLE_LOGS:
    logger.enable("django_google_sso")
else:
    logger.disable("django_google_sso")
