import importlib
import re

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext
from loguru import logger

register = template.Library()


@register.simple_tag
def define_sso_providers():
    provider_pattern = re.compile(r"^django_(.+)_sso$")
    providers = []
    for app in settings.INSTALLED_APPS:
        match = re.search(provider_pattern, app)
        if match:
            providers.append(match.group(1))

    sso_providers = []
    for provider in providers:
        package_name = f"django_{provider}_sso"
        try:
            package = importlib.import_module(package_name)
            conf = getattr(package, "conf")
            if getattr(conf, f"{provider.upper()}_SSO_ENABLED"):
                sso_providers.append(
                    {
                        "name": provider,
                        "logo_url": getattr(conf, f"{provider.upper()}_SSO_LOGO_URL"),
                        "text": gettext(getattr(conf, f"{provider.upper()}_SSO_TEXT")),
                        "login_url": reverse(
                            f"django_{provider}_sso:oauth_start_login"
                        ),
                        "css_url": static(
                            f"django_{provider}_sso/{provider}_button.css"
                        ),
                    }
                )
        except Exception as e:
            logger.error(f"Error importing {package_name}: {e}")
    return sso_providers
