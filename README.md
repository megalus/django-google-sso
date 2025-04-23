<p align="center">
  <img src="docs/images/django-google-sso.png" alt="Django Google SSO"/>
</p>
<p align="center">
<em>Easily integrate Google Authentication into your Django projects</em>
</p>

<p align="center">
<a href="https://pypi.org/project/django-google-sso/" target="_blank">
<img alt="PyPI" src="https://img.shields.io/pypi/v/django-google-sso"/></a>
<a href="https://github.com/megalus/django-google-sso/actions" target="_blank">
<img alt="Build" src="https://github.com/megalus/django-google-sso/workflows/tests/badge.svg"/>
</a>
<a href="https://www.python.org" target="_blank">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/django-google-sso"/>
</a>
<a href="https://www.djangoproject.com/" target="_blank">
<img alt="PyPI - Django Version" src="https://img.shields.io/pypi/djversions/django-google-sso"/>
</a>
<a href="https://github.com/megalus/django-google-sso/blob/main/LICENSE" target="_blank">
<img alt="License" src="https://img.shields.io/github/license/megalus/django-google-sso"/>
</a>
</p>

## Welcome to Django Google SSO

This library simplifies the process of authenticating users with Google in Django projects. It adds a customizable "Login with Google" button to your Django Admin login page with minimal configuration.

### Why use Django Google SSO?

- **Simplicity**: Adds Google authentication with minimal setup and no template modifications
- **Admin Integration**: Seamlessly integrates with the Django Admin interface
- **Customizable**: Works with popular Django Admin skins like Grappelli, Jazzmin, and more
- **Modern**: Uses the latest Google authentication libraries
- **Secure**: Follows OAuth 2.0 best practices for authentication

---

## Quick Start

### Installation

```shell
$ pip install django-google-sso
```

> **Compatibility**
> - Python 3.11, 3.12, 3.13
> - Django 4.2, 5.0, 5.1
> - For Python 3.10, use version 4.x
> - For Python 3.9, use version 3.x
> - For Python 3.8, use version 2.x

### Configuration

1. Add to your `settings.py`:

```python
# settings.py

INSTALLED_APPS = [
    # other django apps
    "django.contrib.messages",  # Required for auth messages
    "django_google_sso",  # Add django_google_sso
]

# Google OAuth2 credentials
GOOGLE_SSO_CLIENT_ID = "your client id here"
GOOGLE_SSO_PROJECT_ID = "your project id here"
GOOGLE_SSO_CLIENT_SECRET = "your client secret here"

# Auto-create users from these domains
GOOGLE_SSO_ALLOWABLE_DOMAINS = ["example.com"]
```

2. Add the callback URL in [Google Console](https://console.cloud.google.com/apis/credentials) under "Authorized Redirect URIs":
   - For local development: `http://localhost:8000/google_sso/callback/`
   - For production: `https://your-domain.com/google_sso/callback/`

3. Add to your `urls.py`:

```python
# urls.py

from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),
]
```

4. Run migrations:

```shell
$ python manage.py migrate
```

That's it! Start Django and visit `http://localhost:8000/admin/login` to see the Google SSO button:

<p align="center">
   <img src="docs/images/django_login_with_google_light.png"/>
</p>

## Admin Skin Compatibility

Django Google SSO works with popular Django Admin skins including:
- Django Admin (default)
- [Grappelli](https://github.com/sehmaschine/django-grappelli)
- [Django Jazzmin](https://github.com/farridav/django-jazzmin)
- [Django Admin Interface](https://github.com/fabiocaccamo/django-admin-interface)
- [Django Jet Reboot](https://github.com/assem-ch/django-jet-reboot)
- [Django Unfold](https://github.com/unfoldadmin/django-unfold)

## Documentation

For detailed documentation, visit:
- [Full Documentation](https://megalus.github.io/django-google-sso/)
- [Quick Setup](https://megalus.github.io/django-google-sso/quick_setup/)
- [Google Credentials Setup](https://megalus.github.io/django-google-sso/credentials/)
- [User Management](https://megalus.github.io/django-google-sso/users/)
- [Customization](https://megalus.github.io/django-google-sso/customize/)
- [Troubleshooting](https://megalus.github.io/django-google-sso/troubleshooting/)

## License
This project is licensed under the terms of the MIT license.
