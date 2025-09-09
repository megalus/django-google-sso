import importlib
import re
from typing import Callable

from django import template
from django.conf import settings
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse
from loguru import logger

from django_google_sso.helpers import is_admin_path, is_page_path

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

    # Because this tag can be called multiple times in a single request,
    # we cache the result in the request object.
    # This occurs when multiple django-*-sso providers are installed
    if request is not None and hasattr(request, "_sso_providers_cache"):
        return request._sso_providers_cache

    for provider in providers:
        package_name = f"django_{provider}_sso"
        try:
            package = importlib.import_module(package_name)
            conf = getattr(package, "conf")
            sso_enabled_conf = f"{provider.upper()}_SSO_ENABLED"
            sso_enabled: bool = getattr(conf, sso_enabled_conf)
            sso_pages_enabled_conf = f"{provider.upper()}_SSO_PAGES_ENABLED"
            sso_pages_enabled: bool | Callable[[HttpRequest], bool] | None = getattr(
                conf, sso_pages_enabled_conf, None
            )
            sso_admin_enabled_conf = f"{provider.upper()}_SSO_ADMIN_ENABLED"
            sso_admin_enabled: bool | Callable[[HttpRequest], bool] | None = getattr(
                conf, sso_admin_enabled_conf, None
            )

            provider_name = provider.title()
            if not sso_enabled:
                logger.debug(
                    f"{provider_name} SSO is Disabled from config: {sso_enabled_conf}"
                )
                continue

            can_add = True

            # Check for admin and pages only if they are defined (not None)
            if request and (
                sso_admin_enabled is not None or sso_pages_enabled is not None
            ):
                # If callable, call it with the request
                if callable(sso_admin_enabled):
                    sso_admin_enabled = sso_admin_enabled(request)
                # If is True, check if is admin path
                elif sso_admin_enabled is True:
                    sso_admin_enabled = is_admin_path(request)
                else:
                    sso_admin_enabled = False

                if callable(sso_pages_enabled):
                    sso_pages_enabled = sso_pages_enabled(request)
                elif sso_pages_enabled is True:
                    sso_pages_enabled = is_page_path(request)
                else:
                    sso_pages_enabled = False

                if is_admin_path(request):
                    can_add = sso_admin_enabled
                    log_text = (
                        f"{provider_name} SSO is "
                        f"{'Enabled' if can_add else 'Disabled'} "
                        f"for ADMIN, from config: "
                        f"{sso_admin_enabled_conf}="
                        f"{sso_admin_enabled} and path: {request.path}"
                    )
                else:
                    can_add = sso_pages_enabled
                    log_text = (
                        f"{provider_name} SSO is "
                        f"{'Enabled' if can_add else 'Disabled'} for "
                        f"PAGES, from config: "
                        f"{sso_pages_enabled_conf}="
                        f"{sso_pages_enabled} and path: {request.path}"
                    )
                logger.debug(log_text)

            if can_add:
                logo_conf = f"{provider.upper()}_SSO_LOGO_URL"
                text_conf = f"{provider.upper()}_SSO_TEXT"
                logo_conf = getattr(conf, logo_conf)
                if callable(logo_conf):
                    logo_conf = logo_conf(request)
                text_conf = getattr(conf, text_conf)
                if callable(text_conf):
                    text_conf = text_conf(request)
                sso_providers.append(
                    {
                        "name": provider,
                        "logo_url": logo_conf,
                        "text": text_conf,
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

    if request is not None:
        setattr(request, "_sso_providers_cache", sso_providers)

    return sso_providers
