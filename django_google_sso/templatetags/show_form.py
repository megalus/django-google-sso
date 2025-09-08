from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def define_show_form(context) -> bool:
    from django_google_sso import conf

    request = context.get("request")

    # Because this tag can be called multiple times in a single request,
    # we cache the result in the request object.
    # This occurs when multiple django-*-sso providers are installed
    if request is not None and hasattr(request, "_sso_show_form_cache"):
        return request._sso_show_form_cache

    value = conf.SSO_SHOW_FORM_ON_ADMIN_PAGE
    if callable(value):
        value = value(request)

    if request is not None:
        request._sso_show_form_cache = value

    return value
