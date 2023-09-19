from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class GoogleSSOUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=255)
    picture_url = models.URLField(max_length=2000)
    locale = models.CharField(max_length=5)

    @property
    def picture(self):
        if self.picture_url:
            return mark_safe(
                '<img src = "{}" width="75" height="75">'.format(
                    self.picture_url
                )  # nosec
            )
        return None

    def __str__(self):
        return f"{self.user.email} ({self.google_id})"

    class Meta:
        db_table = "google_sso_user"
        verbose_name = _("Google SSO User")
