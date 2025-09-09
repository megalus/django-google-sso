from dataclasses import dataclass
from typing import Any, Optional

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Field
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from loguru import logger

from django_google_sso import conf
from django_google_sso.models import GoogleSSOUser


@dataclass
class GoogleAuth:
    request: Any
    _flow: Optional[Flow] = None

    @property
    def scopes(self) -> list[str]:
        return self.get_sso_value("scopes")

    def get_sso_value(self, key: str) -> Any:
        """Get SSO value from request or settings.

        Both configurations are valid:
        GOOGLE_SSO_CLIENT_ID = "your-client-id" # string value
        GOOGLE_SSO_CLIENT_ID = get_client_id # callable function

        When the value is a callable,
        it will be called with the request as an argument:

        def get_client_id(request):
            client_ids = {
                "example.com": "your-client-id",
                "other.com": "your-other-client-id",
            }
            return client_ids.get(request.site.domain, None)

        GOOGLE_SSO_CLIENT_ID = get_client_id

        :param key: The key to retrieve from the settings.
        :return: The value associated with the key.
        :raises ValueError: If the key is not found in the settings.
        """
        google_sso_conf = f"GOOGLE_SSO_{key.upper()}"
        if hasattr(conf, google_sso_conf):
            value = getattr(conf, google_sso_conf)
            if callable(value):
                logger.debug(
                    f"Value from conf {google_sso_conf} is a callable. Calling it."
                )
                return value(self.request)
            return value
        raise ValueError(
            f"SSO Configuration '{google_sso_conf}' not found in settings."
        )

    def get_client_config(self) -> Credentials:
        client_config = {
            "web": {
                "client_id": self.get_sso_value("client_id"),
                "project_id": self.get_sso_value("project_id"),
                "client_secret": self.get_sso_value("client_secret"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_provider_x509_cert_url": (
                    "https://www.googleapis.com/oauth2/v1/certs"
                ),
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [self.get_redirect_uri()],
            }
        }
        return client_config

    def get_netloc(self):
        callback_domain = self.get_sso_value("callback_domain")
        if callback_domain:
            logger.debug("Find Netloc using GOOGLE_SSO_CALLBACK_DOMAIN")
            return callback_domain

        site = get_current_site(self.request)
        logger.debug("Find Netloc using Site domain")
        return site.domain

    def get_redirect_uri(self) -> str:
        if "HTTP_X_FORWARDED_PROTO" in self.request.META:
            scheme = self.request.META["HTTP_X_FORWARDED_PROTO"]
        else:
            scheme = self.request.scheme
        netloc = self.get_netloc()
        path = reverse("django_google_sso:oauth_callback")
        callback_uri = f"{scheme}://{netloc}{path}"
        logger.debug(f"Callback URI: {callback_uri}")
        return callback_uri

    @property
    def flow(self) -> Flow:
        if not self._flow:
            self._flow = Flow.from_client_config(
                self.get_client_config(),
                scopes=self.scopes,
                redirect_uri=self.get_redirect_uri(),
            )
        return self._flow

    def get_user_info(self):
        session = self.flow.authorized_session()
        user_info = session.get("https://www.googleapis.com/oauth2/v2/userinfo").json()
        return user_info

    def get_user_token(self):
        return self.flow.credentials.token

    def check_enabled(self, next_url: str) -> tuple[bool, str]:
        response = True, ""
        if not conf.GOOGLE_SSO_ENABLED:
            response = False, "Google SSO not enabled."
        else:
            admin_route = conf.SSO_ADMIN_ROUTE
            if callable(admin_route):
                admin_route = admin_route(self.request)

            admin_enabled = self.get_sso_value("admin_enabled")
            if admin_enabled is False and next_url.startswith(reverse(admin_route)):
                response = False, "Google SSO not enabled for Admin."

            pages_enabled = self.get_sso_value("pages_enabled")
            if pages_enabled is False and not next_url.startswith(reverse(admin_route)):
                response = False, "Google SSO not enabled for Pages."

        if response[1]:
            logger.debug(f"SSO Enable Check failed: {response[1]}")

        return response


@dataclass
class UserHelper:
    user_info: dict[Any, Any]
    request: Any
    user_changed: bool = False

    @property
    def user_info_email(self):
        return self.user_info["email"].lower()

    @property
    def user_model(self) -> type[User]:
        return get_user_model()

    @property
    def username_field(self) -> Field:
        return self.user_model._meta.get_field(self.user_model.USERNAME_FIELD)

    @property
    def email_field_name(self) -> str:
        return self.user_model.get_email_field_name()

    @property
    def email_is_valid(self) -> bool:
        google = GoogleAuth(self.request)
        user_email_domain = self.user_info_email.split("@")[-1]
        allowable_domains = google.get_sso_value("allowable_domains")
        if "*" in allowable_domains or user_email_domain in allowable_domains:
            return True
        email_verified = self.user_info.get("email_verified", None)
        if email_verified is not None and not email_verified:
            logger.debug(f"Email {self.user_info_email} is not verified.")
        return email_verified if email_verified is not None else False

    def get_or_create_user(self, extra_users_args: dict | None = None):
        user_defaults = extra_users_args or {}
        if self.username_field.name not in user_defaults:
            user_defaults[self.username_field.name] = self.user_info_email
        if self.email_field_name not in user_defaults:
            user_defaults[self.email_field_name] = self.user_info_email
        user, created = self.user_model.objects.get_or_create(
            **{f"{self.email_field_name}__iexact": self.user_info_email},
            defaults=user_defaults,
        )
        self.check_first_super_user(user)
        self.check_for_update(created, user)
        if self.user_changed:
            user.save()

        google = GoogleAuth(self.request)
        save_basic_info = google.get_sso_value("save_basic_google_info")
        if save_basic_info:
            default_locale = google.get_sso_value("default_locale")
            GoogleSSOUser.objects.update_or_create(
                user=user,
                defaults={
                    "google_id": self.user_info["id"],
                    "picture_url": self.user_info.get("picture"),
                    "locale": self.user_info.get("locale") or default_locale,
                },
            )
        return user

    def check_for_update(self, created, user):
        google = GoogleAuth(self.request)
        always_update = google.get_sso_value("always_update_user_data")
        if created or always_update:
            self.check_for_permissions(user)
            user.first_name = self.user_info.get("given_name")
            user.last_name = self.user_info.get("family_name")
            if not getattr(user, self.username_field.name):
                setattr(user, self.username_field.name, self.user_info_email)
            user.set_unusable_password()
            self.user_changed = True

    def check_first_super_user(self, user):
        google = GoogleAuth(self.request)
        auto_create = google.get_sso_value("auto_create_first_superuser")
        if auto_create:
            superuser_exists = self.user_model.objects.filter(
                is_superuser=True,
                **{
                    f"{self.email_field_name}__icontains": (
                        f"@{self.user_info_email.split('@')[-1]}"
                    )
                },
            ).exists()
            if not superuser_exists:
                message_text = _(
                    f"GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER is True. "
                    f"Adding SuperUser status to email: {self.user_info_email}"
                )
                messages.add_message(self.request, messages.INFO, message_text)
                logger.warning(message_text)
                user.is_superuser = True
                user.is_staff = True
                self.user_changed = True

    def check_for_permissions(self, user):
        user_email = getattr(user, self.email_field_name)
        google = GoogleAuth(self.request)
        staff_list = google.get_sso_value("staff_list")
        if user_email in staff_list or "*" in staff_list:
            message_text = _(
                f"User email: {user_email} in GOOGLE_SSO_STAFF_LIST. "
                f"Added Staff Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_staff = True
        superuser_list = google.get_sso_value("superuser_list")
        if user_email in superuser_list:
            message_text = _(
                f"User email: {user_email} in GOOGLE_SSO_SUPERUSER_LIST. "
                f"Added SuperUser Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_superuser = True
            user.is_staff = True

    def find_user(self):
        query = self.user_model.objects.filter(
            **{f"{self.email_field_name}__iexact": self.user_info_email}
        )
        return query.get() if query.exists() else None
