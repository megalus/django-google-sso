# Using Django Google SSO outside Django Admin

Django-Google-SSO aims for simplicity, that's why the primary focus is on the Admin login logic. But this package can be used
outside Django Admin, in a custom login page. To do so, you can follow the steps below.

!!! warning "This is the Tip of the Iceberg"
    In real-life projects, user customer login involves more than just a login button. You need to implement many
    features like OTP, Captcha, "Recover Password", "Remember Me", "Login with Passkey" etc. This documentation shows a simple implementation
    to demonstrate how to use Django Google SSO outside Django Admin, but for more complex UX requisites, please check
    full solutions like [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html), or incremental
    solutions like [django-otp](https://github.com/django-otp/django-otp), [django-recaptcha](https://github.com/django-recaptcha/django-recaptcha),
    [django-passkeys](https://github.com/mkalioby/django-passkeys), etc.


### Add Django Google SSO templates to your login page

Inside your login template, just add these two lines:

* `{% include 'google_sso/login_sso.html' %}` inside `<body>`
* `{% static 'django_google_sso/google_button.css' %}` inside `<head>`

### Login template example
```html
--8<-- "example_google_app/templates/login.html"
```

The `include` command will add the login button to your template for all django-sso installed in the project.

## Define per-request parameters

In the case you need different behavior for the login to Admin and login to Django pages, you can define this using callables on the Django Google SSO settings. For example:


| Setting                         | Login to Admin    | Login to Pages |
|---------------------------------|-------------------|----------------|
| `GOOGLE_SSO_ALLOWABLE_DOMAINS`  | `["example.com"]` | `["*"]`        |
| `GOOGLE_SSO_LOGIN_FAILED_URL`   | `"admin:login"`   | `"index"`      |
| `GOOGLE_SSO_NEXT_URL`           | `"admin:index"`   | `"secret"`     |
| `GOOGLE_SSO_SESSION_COOKIE_AGE` | `3600`            | `86400`        |
| `GOOGLE_SSO_STAFF_LIST`         | `[...]`           | `[]`           |
| `GOOGLE_SSO_SUPERUSER_LIST`     | `[...]`           | `[]`           |

!!! tip "You can config almost all settings per request"
    You can config different Google credentials, Scopes, Default Locale, etc. Please check the
    [Settings](settings.md) and [Sites](sites.md) docs for more details.

### Settings logic example
```python
--8<-- "example_google_app/settings.py:sso_config"
```

### Toggle Google SSO between Admin and Page logins

Finally, if you want to toggle between Admin and Page login, you can enable/disable Google SSO using the
`GOOGLE_SSO_PAGES_ENABLED` and `GOOGLE_SSO_ADMIN_ENABLED`.
For example, if you want to enable Google SSO only for Page login:

```python
# settings.py

# Enable or disable globally
GOOGLE_SSO_ENABLED = True

# Enable or Disable per request
# Always configure both Admin and Pages settings
GOOGLE_SSO_ADMIN_ENABLED = False
GOOGLE_SSO_PAGES_ENABLED = True
```
!!! question "How Package knows if the request is for Admin or Page login?"
    The package uses the `is_admin_path` and `is_page_path` helpers to check if the `request.path`
    starts with the admin path. To find the admin path, the package uses the `SSO_ADMIN_ROUTE`
    setting (default: `admin:index`).

    ```python
    # settings.py
    from django_google_sso.helpers import is_admin_path, is_page_path

    SSO_ADMIN_ROUTE = "admin:index"  # Default admin route

    GOOGLE_SSO_ENABLED = True
    GOOGLE_SSO_ADMIN_ENABLED = is_admin_path  # Same as True
    GOOGLE_SSO_PAGES_ENABLED = is_page_path  # Same as True
    ```
