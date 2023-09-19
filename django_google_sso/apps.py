from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoGoogleSsoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_google_sso"
    verbose_name = _("Google SSO User")

    def ready(self):
        import django_google_sso.templatetags  # noqa
