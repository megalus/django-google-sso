from django.core.checks import Tags, register
from django.core.checks.messages import Warning

TEMPLATE_TAG_NAMES = ["show_form", "sso_tags"]


@register(Tags.templates)
def register_sso_check(app_configs, **kwargs):
    """Check for E003/W003 template warnings.

    This is a copy of the original check_for_template_tags_with_the_same_name
    but filtering out the TEMPLATE_TAG_NAMES from this library.

    Django will raise this warning if you're installed more than one SSO provider,
    like django_microsoft_sso and django_google_sso.

    To silence any E003/W003 warning, you can add the following to your settings.py:
    SILENCED_SYSTEM_CHECKS = ["templates.W003"]  # or templates.E003 for Django<=5.1

    And to run an alternate version of this check,
    you can add the following to your settings.py:
    SSO_USE_ALTERNATE_W003 = True

    You need to silence the original templates.W003 check for this to work.
    New warnings will use the id `sso.W003`

    """
    try:  # Django <=5.0 error was templates.E003
        from django.core.checks.templates import (
            check_for_template_tags_with_the_same_name,
        )

        errors = check_for_template_tags_with_the_same_name(app_configs, **kwargs)
        errors = [
            Warning(msg=error.msg, hint=error.hint, obj=error.obj, id="sso.E003")
            for error in errors
            if not any(name in error.msg for name in TEMPLATE_TAG_NAMES)
        ]
        return errors
    except ImportError:  # Django >=5.1 error is now templates.W003
        from django.apps import apps
        from django.conf import settings
        from django.template.backends.django import DjangoTemplates

        errors = []
        if app_configs is None:
            app_configs = apps.get_app_configs()

        errors = []
        for config in app_configs:
            for engine in settings.TEMPLATES:
                if (
                    engine["BACKEND"]
                    == "django.template.backends.django.DjangoTemplates"
                ):
                    engine_params = engine.copy()
                    engine_params.pop("BACKEND")
                    django_engine = DjangoTemplates(engine_params)
                    template_tag_errors = (
                        django_engine._check_for_template_tags_with_the_same_name()
                    )
                    for error in template_tag_errors:
                        if not any(name in error.msg for name in TEMPLATE_TAG_NAMES):
                            errors.append(
                                Warning(
                                    msg=error.msg,
                                    hint=error.hint,
                                    obj=error.obj,
                                    id="sso.W003",
                                )
                            )
        return errors
