from typing import Optional, Type

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser

from django_google_sso import conf
from django_google_sso.models import GoogleSSOUser

if conf.GOOGLE_SSO_ENABLED:
    admin.site.login_template = "google_sso/login.html"


def get_current_user_and_admin() -> (
    tuple[AbstractUser, Optional[UserAdmin], Type[UserAdmin]]
):
    """Get the current user model and last admin class.

    For user model, we use the get_user_model() function.
    For the last admin class registered, we use the
    admin.site._registry.get(user_model) function or default `UserAdmin`

    """

    user_model = get_user_model()
    existing_user_admin = admin.site._registry.get(user_model)
    user_admin_model = (
        UserAdmin if existing_user_admin is None else existing_user_admin.__class__
    )
    return user_model, existing_user_admin, user_admin_model


CurrentUserModel, last_admin, LastUserAdmin = get_current_user_and_admin()


if admin.site.is_registered(CurrentUserModel):
    admin.site.unregister(CurrentUserModel)


class GoogleSSOInlineAdmin(admin.StackedInline):
    model = GoogleSSOUser
    readonly_fields = ("google_id",)
    extra = 0

    def has_add_permission(self, request, obj):
        return False


@admin.register(GoogleSSOUser)
class GoogleSSOAdmin(admin.ModelAdmin):
    list_display = ("user", "google_id")
    readonly_fields = ("google_id", "picture")

    def has_add_permission(self, request):
        return False


@admin.register(CurrentUserModel)
class GoogleSSOUserAdmin(LastUserAdmin):
    model = CurrentUserModel
    inlines = (
        tuple(set(list(last_admin.inlines) + [GoogleSSOInlineAdmin]))
        if last_admin
        else (GoogleSSOInlineAdmin,)
    )
