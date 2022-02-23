## Welcome to Django Google SSO
[![PyPI](https://img.shields.io/pypi/v/django-google-sso)](https://pypi.org/project/django-google-sso/)
[![Build](https://github.com/chrismaille/django-google-sso/workflows/tests/badge.svg)](https://github.com/chrismaille/django-google-sso/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-google-sso)](https://www.python.org)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-google-sso)](https://www.djangoproject.com/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This library aims to simplify the process of authenticating users with Google in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth) and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)

### Why another library?

* This library aims for _simplicity_ and ease of use. [django-allauth](https://github.com/pennersr/django-allauth) is _de facto_ solution for Authentication in Django,
but add lots of boilerplate, specially the html templates. **Django-Google-SSO** just add the "Login with Google" button in the default login page.
* [django-admin-sso](https://github.com/matthiask/django-admin-sso/) is a good solution, but it uses a deprecated google `auth2client` version.

### Install

```shell
$ pip install django-google-sso
```

### Versions
For django 4.x use version `2.x`
For django 3.x use version `1.x`

### Configuration

1. Add the following to your `settings.py` `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # other django apps
    "django.contrib.messages",  # Need for Auth messages
    "django.contrib.sites",  # Add Sites framework
    "django_google_sso",  # Add django_google_sso
]
```

2. In [Google Console](https://console.cloud.google.com/apis/credentials) at _Api -> Credentials_, retrieve your
Project Credentials and add them in your `settings.py`:
```python
GOOGLE_SSO_CLIENT_ID = "your client id here"
GOOGLE_SSO_PROJECT_ID = "your project id here"
GOOGLE_SSO_CLIENT_SECRET = "your client secret here"
```

3. Add the default site and allowed domains to auto-create users:
```python
SITE_ID = 1  # Optional, just add if you want to use sites without request.
GOOGLE_SSO_ALLOWABLE_DOMAINS = ["example.com"]
```

4. In `urls.py` please add the **Django-Google-SSO** views:
```python
from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),
]
```
5. In [Google Console](https://console.cloud.google.com/apis/credentials) at _Api -> Credentials -> Oauth2 Client_,
please add **Django-Google-SSO** callback url, using this format: `https://your-domain.com/google_sso/callback/`,
where `your-domain.com` is the domain you defined in Django Sites Framework. For example, if you change your
Site object domain to `localhost:8000`, then your callback must be `http://localhost:8000/google_sso/callback/`.

6. Run migrations:
```shell
$ python manage.py migrate
```

### How Django-Google-SSO works

First, the user is redirected to the Django login page. If settings `GOOGLE_SSO_ENABLED` is True, the
"Login with Google" button will be added to default form.

On click, **Django-Google-SSO** will add, in current session, the `next_path` and Google Flow `state`.
This session will expire in 10 minutes. Then user will be redirected to Google login page.

On callback, **Django-Google-SSO** will check `code` and `state` received. If they are valid,
Google's UserInfo will be retrieved. If the user is already registered in Django, the user
will be logged in.

Otherwise, the user will be created and logged in, if his email domain,
matches one of the `GOOGLE_SSO_ALLOWABLE_DOMAINS`. On creation only, this user can be set the
`staff` or `superuser` status, if his email are in `GOGGLE_SSO_STAFF_LIST` or
`GOGGLE_SSO_SUPERUSER_LIST` respectively.

Please note if you add an email to one of these lists, the email domain must be added to `GOOGLE_SSO_ALLOWABLE_DOMAINS` too.

This session will expire in 1 hour, or the time defined, in seconds, in `GOOGLE_SSO_SESSION_COOKIE_AGE`.

Browser will be redirected to `next_path` if operation succeeds, or the `login` page, if operation fails.

### Further customization

Please add the following variables to your `settings.py`:

```python
GOOGLE_SSO_ENABLED = True  # default value
GOOGLE_SSO_SESSION_COOKIE_AGE = 3600  # default value

# Mark as True, to add superuser status to first user
# created with email domain in `GOOGLE_SSO_ALLOWABLE_DOMAINS`
GOGGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = True

GOGGLE_SSO_STAFF_LIST = ["email@example.com"]
GOGGLE_SSO_SUPERUSER_LIST = ["another-email@example.com"]
GOOGLE_SSO_TIMEOUT = 10  # Time before timeout Google requests. Default value: 10 seconds
GOOGLE_SSO_SCOPES = [  # Google default scope
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
```

### Running behind a Reverse Proxy
Please make sure you're passing the correct `X-Forwarded-Proto` header.

### Using the `login_required` decorator
To use the `login_required` decorator, or his Class Based View equivalent, you can redirect the `accounts/login` route
to the modified login form page, adding this to your `urls.py`:

````python
from django.conf.urls import url
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(
        r"^accounts/login/$",
        LoginView.as_view(
            template_name="admin_sso/login.html"  # The modified form with google button
        ),
    ),
]
````

### Example App
To test this library please check the `Example App` provided [here](/example_app).

### Not working?
Don't panic. Get a towel and, please, open an [issue](https://github.com/chrismaille/django-google-sso/issues).
