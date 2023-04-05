# Using Django Admin

**Django Google SSO** integrates with Django Admin, adding an Inline Model Admin to the User model. This way, you can
access the Google SSO data for each user.

## Using Custom User model

If you are using a custom user model, you may need to add the `GoogleSSOInlineAdmin` inline model admin to your custom user model admin, like this:

```python
# admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django_google_sso.admin import GoogleSSOInlineAdmin

CustomUser = get_user_model()

if admin.site.is_registered(CustomUser):
    admin.site.unregister(CustomUser)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    inlines = [GoogleSSOInlineAdmin]
```
