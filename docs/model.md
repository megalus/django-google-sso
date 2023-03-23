# Getting Google info

## The User model

**Django Google SSO** saves in the database the following information from Google, using current `User` model:

* `email`: The email address of the user.
* `first_name`: The first name of the user.
* `last_name`: The last name of the user.
* `username`: The email address of the user.
* `password`: An unusable password, generated using `get_unusable_password()` from Django.

Getting data on code is straightforward:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    })
```

## The GoogleSSOUser model

Also, on the `GoogleSSOUser` model, it saves the following information:

* `picture_url`: The URL of the user's profile picture.
* `google_id`: The Google ID of the user.
* `locale`: The preferred locale of the user.

This is a one-to-one relationship with the `User` model, so you can access this data using the `googlessouser` reverse
relation attribute:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

@login_required
def retrieve_user_data(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "picture": user.googlessouser.picture_url,
        "google_id": user.googlessouser.google_id,
        "locale": user.googlessouser.locale,
    })
```

You can also import the model directly, like this:

```python
from django_google_sso.models import GoogleSSOUser

google_info = GoogleSSOUser.objects.get(user=user)
```

## About Google Scopes

To retrieve this data **Django Google SSO** uses the following scopes for [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2):

```python
GOOGLE_SSO_SCOPES = [  # Google default scope
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
```

You can change this scopes overriding the `GOOGLE_SSO_SCOPES` setting in your `settings.py` file. But if you ask the user
to authorize more scopes, this additional data will not be saved in the database by this plugin. You will need to implement
your own logic to save this data, calling google again.

!!! info "The main goal here is simplicity"
    The main goal of this plugin is to be simple to use as possible. But it is important to ask the user **_once_** for the scopes.
    That's why this plugin permits you to change the scopes, but will not save the additional data from it.
