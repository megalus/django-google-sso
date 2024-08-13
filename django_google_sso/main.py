from dataclasses import dataclass
from typing import Any, Optional

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Field, Model
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
        return conf.GOOGLE_SSO_SCOPES

    def get_client_config(self) -> Credentials:
        client_config = {
            "web": {
                "client_id": conf.GOOGLE_SSO_CLIENT_ID,
                "project_id": conf.GOOGLE_SSO_PROJECT_ID,
                "client_secret": conf.GOOGLE_SSO_CLIENT_SECRET,
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
        if conf.GOOGLE_SSO_CALLBACK_DOMAIN:
            logger.debug("Find Netloc using GOOGLE_SSO_CALLBACK_DOMAIN")
            return conf.GOOGLE_SSO_CALLBACK_DOMAIN

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


@dataclass
class UserHelper:
    user_info: dict[Any, Any]
    request: Any
    user_changed: bool = False

    @property
    def user_email(self):
        return self.user_info["email"].lower()

    @property
    def user_model(self) -> AbstractUser | Model:
        return get_user_model()

    @property
    def username_field(self) -> Field:
        return self.user_model._meta.get_field(self.user_model.USERNAME_FIELD)

    @property
    def email_is_valid(self) -> bool:
        user_email_domain = self.user_email.split("@")[-1]
        for email_domain in conf.GOOGLE_SSO_ALLOWABLE_DOMAINS:
            if user_email_domain in email_domain:
                return True
        email_verified = self.user_info.get("email_verified", None)
        if email_verified is not None and not email_verified:
            logger.debug(f"Email {self.user_email} is not verified.")
        return email_verified if email_verified is not None else False

    def get_or_create_user(self, extra_users_args: dict | None = None):
        user_defaults = extra_users_args or {}
        if self.username_field.name not in user_defaults:
            user_defaults[self.username_field.name] = self.user_email
        if "email" not in user_defaults:
            user_defaults["email"] = self.user_email
        user, created = self.user_model.objects.get_or_create(
            email__iexact=self.user_email, defaults=user_defaults
        )
        self.check_first_super_user(user)
        self.check_for_update(created, user)
        if self.user_changed:
            user.save()

        if conf.GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO:
            GoogleSSOUser.objects.update_or_create(
                user=user,
                defaults={
                    "google_id": self.user_info["id"],
                    "picture_url": self.user_info.get("picture"),
                    "locale": self.user_info.get("locale")
                    or conf.GOOGLE_SSO_DEFAULT_LOCALE,
                },
            )
        return user

    def check_for_update(self, created, user):
        if created or conf.GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA:
            self.check_for_permissions(user)
            user.first_name = self.user_info.get("given_name")
            user.last_name = self.user_info.get("family_name")
            if not getattr(user, self.username_field.name):
                setattr(user, self.username_field.name, self.user_email)
            user.set_unusable_password()
            self.user_changed = True

    def check_first_super_user(self, user):
        if conf.GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER:
            superuser_exists = self.user_model.objects.filter(
                is_superuser=True, email__icontains=f"@{self.user_email.split('@')[-1]}"
            ).exists()
            if not superuser_exists:
                message_text = _(
                    f"GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER is True. "
                    f"Adding SuperUser status to email: {self.user_email}"
                )
                messages.add_message(self.request, messages.INFO, message_text)
                logger.warning(message_text)
                user.is_superuser = True
                user.is_staff = True
                self.user_changed = True

    def check_for_permissions(self, user):
        if (
            user.email in conf.GOOGLE_SSO_STAFF_LIST
            or "*" in conf.GOOGLE_SSO_STAFF_LIST
        ):
            message_text = _(
                f"User email: {self.user_email} in GOOGLE_SSO_STAFF_LIST. "
                f"Added Staff Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_staff = True
        if user.email in conf.GOOGLE_SSO_SUPERUSER_LIST:
            message_text = _(
                f"User email: {self.user_email} in GOOGLE_SSO_SUPERUSER_LIST. "
                f"Added SuperUser Permission."
            )
            messages.add_message(self.request, messages.INFO, message_text)
            logger.debug(message_text)
            user.is_superuser = True
            user.is_staff = True

    def find_user(self):
        query = self.user_model.objects.filter(email__iexact=self.user_email)
        if query.exists():
            return query.get()
