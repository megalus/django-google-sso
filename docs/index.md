![](images/django-google-sso.png)

# Welcome to Django Google SSO

## Motivation

This library aims to simplify the process of authenticating users with Google in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth)
and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)

## Why another library?

* This library aims for _simplicity_ and ease of use. [django-allauth](https://github.com/pennersr/django-allauth) is
  _de facto_ solution for Authentication in Django, but add lots of boilerplate, specially the html templates.
  **Django-Google-SSO** just add a fully customizable "Login with Google" button in the default login page.

    === "Light Mode"
        ![](images/django_login_with_google_light.png)

    === "Dark Mode"
        ![](images/django_login_with_google_dark.png)

* [django-admin-sso](https://github.com/matthiask/django-admin-sso/) is a good solution, but it uses a deprecated
  google `auth2client` version.

---

## Install

```shell
pip install django-google-sso
```

!!! info "Currently this project supports:"
    * Python 3.11, 3.12 and 3.13
    * Django 4.2, 5.0, 5.1 and 5.2

    Older python/django versions are not supported.
