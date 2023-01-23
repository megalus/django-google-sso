from django.conf import settings

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
GOOGLE_SSO_AUTO_CREATE_USERS = getattr(settings, "GOOGLE_SSO_AUTO_CREATE_USERS", True)

GOOGLE_SSO_AUTHENTICATION_BACKEND = getattr(
    settings, "GOOGLE_SSO_AUTHENTICATION_BACKEND", None
)

GOOGLE_SSO_PRE_LOGIN_CALLBACK = getattr(
    settings,
    "GOOGLE_SSO_PRE_LOGIN_CALLBACK",
    "django_google_sso.hooks.pre_login_user",
)
