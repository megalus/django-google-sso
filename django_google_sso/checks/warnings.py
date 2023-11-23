import glob
import os

from django.core.checks import Tags, register
from django.core.checks.messages import Warning
from django.core.checks.templates import check_for_template_tags_with_the_same_name


def get_template_tag_names():
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(os.path.dirname(dir_path), "templatetags")
    python_files = glob.glob(os.path.join(template_path, "*.py"))
    names = [
        os.path.basename(file).replace(".py", "")
        for file in python_files
        if not file.endswith("__init__.py")
    ]
    return names


TEMPLATE_TAG_NAMES = get_template_tag_names()


@register(Tags.templates)
def register_sso_check(app_configs, **kwargs):
    """Check for E003/W003 template warnings.

    This is a copy of the original check_for_template_tags_with_the_same_name
    but filtering out the TEMPLATE_TAG_NAMES from this library.

    Django will raise this warning if you're installed more than one SSO provider,
    like django_microsoft_sso and django_google_sso.

    To silence any E003/W003 warning, you can add the following to your settings.py:
    SILENCED_SYSTEM_CHECKS = ["templates.E003"]

    And to run an alternate version of this check,
    you can add the following to your settings.py:
    SSO_USE_ALTERNATE_W003 = True

    You need to silence the original templates.E003 check for this to work.
    New warnings will use the id `sso.E003`

    """
    errors = check_for_template_tags_with_the_same_name(app_configs, **kwargs)
    errors = [
        Warning(msg=error.msg, hint=error.hint, obj=error.obj, id="sso.E003")
        for error in errors
        if not any(name in error.msg for name in TEMPLATE_TAG_NAMES)
    ]
    return errors
