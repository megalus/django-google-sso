from django import template

register = template.Library()


@register.simple_tag
def define_show_form() -> bool:
    from django.conf import settings

    return getattr(settings, "SSO_SHOW_FORM_ON_ADMIN_PAGE", True)
