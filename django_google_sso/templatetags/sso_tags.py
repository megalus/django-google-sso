import importlib
import re

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext
from loguru import logger

register = template.Library()


@register.simple_tag(takes_context=True)
def define_sso_providers(context):
    provider_pattern = re.compile(r"^django_(.+)_sso$")
    providers = []
    for app in settings.INSTALLED_APPS:
        match = re.search(provider_pattern, app)
        if match:
            providers.append(match.group(1))

    sso_providers = []
    request = context.get("request")
    for provider in providers:
        package_name = f"django_{provider}_sso"
        try:
            package = importlib.import_module(package_name)
            conf = getattr(package, "conf")
            sso_enabled_conf = f"{provider.upper()}_SSO_ENABLED"
            sso_enabled = getattr(conf, f"{provider.upper()}_SSO_ENABLED")
            sso_pages_enabled_conf = f"{provider.upper()}_SSO_PAGES_ENABLED"
            sso_pages_enabled = getattr(conf, f"{provider.upper()}_SSO_PAGES_ENABLED")
            sso_admin_enabled_conf = f"{provider.upper()}_SSO_ADMIN_ENABLED"
            sso_admin_enabled = getattr(conf, f"{provider.upper()}_SSO_ADMIN_ENABLED")

            provider_name = provider.title()
            if callable(sso_admin_enabled):
                sso_admin_enabled = sso_admin_enabled(request)
            if callable(sso_pages_enabled):
                sso_pages_enabled = sso_pages_enabled(request)

            # If pages and admin are None, use original configuration
            if sso_pages_enabled is None and sso_admin_enabled is None:
                can_add = sso_enabled
                log_text = (
                    f"SSO Provider: {provider_name} is "
                    f"{'Enabled' if can_add else 'Disabled'}"
                    f" from config {sso_enabled_conf}"
                )
            else:
                if request.path.startswith(reverse("admin:index")):
                    can_add = sso_admin_enabled
                    log_text = (
                        f"SSO Provider: {provider_name} is "
                        f"{'Enabled' if can_add else 'Disabled'} "
                        f"for Admin, from config: "
                        f"{sso_admin_enabled_conf}="
                        f"{sso_admin_enabled} and path: {request.path}"
                    )
                else:
                    can_add = sso_pages_enabled
                    log_text = (
                        f"SSO Provider: {provider_name} is "
                        f"{'Enabled' if can_add else 'Disabled'} for "
                        f"Pages, from config: "
                        f"{sso_pages_enabled_conf}="
                        f"{sso_pages_enabled} and path: {request.path}"
                    )

            logger.debug(log_text)
            if can_add:
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
