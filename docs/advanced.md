# Advanced Use

On this section, you will learn how to use **Django Google SSO** in more advanced scenarios. This section assumes you
have a good understanding for Django advanced techniques, like custom User models, custom authentication backends, and
so on.

## Using Custom Authentication Backend

If the users need to log in using a custom authentication backend, you can use the `GOOGLE_SSO_AUTHENTICATION_BACKEND`
setting:

```python
# settings.py

GOOGLE_SSO_AUTHENTICATION_BACKEND = "myapp.authentication.MyCustomAuthenticationBackend"
```

## Using Google as Single Source of Truth

If you want to use Google as the single source of truth for your users, you can simply set the
`GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA`. This will enforce the basic user data (first name, last name, email and picture) to be
updated at every login.

```python
# settings.py

GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA = True  # Always update user data on login
```

## Adding additional data to User model though scopes

If you need more advanced logic, you can use the `GOOGLE_SSO_PRE_LOGIN_CALLBACK` setting to import custom data from Google
(considering you have configured the right scopes and possibly a Custom User model to store these fields).

For example, you can use the following code to update the user's
name, email and birthdate at every login:

```python
# settings.py

GOOGLE_SSO_SAVE_ACCESS_TOKEN = True  # You will need this token
GOOGLE_SSO_PRE_LOGIN_CALLBACK = "hooks.pre_login_user"
GOOGLE_SSO_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/user.birthday.read",  # <- This is a custom scope
]
```

```python
# myapp/hooks.py
import datetime
import httpx
from loguru import logger


def pre_login_user(user, request):
    token = request.session.get("google_sso_access_token")
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
        }

        # Request Google User Info
        url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = httpx.get(url, headers=headers)
        user_data = response.json()
        logger.debug(f"Updating User Data with Google User Info: {user_data}")

        # Request Google People Info for the additional scopes
        url = f"https://people.googleapis.com/v1/people/me?personFields=birthdays"
        response = httpx.get(url, headers=headers)
        people_data = response.json()
        logger.debug(f"Updating User Data with Google People Info: {people_data}")
        birthdate = datetime.date(**people_data["birthdays"][0]['date'])

        user.first_name = user_data["given_name"]
        user.last_name = user_data["family_name"]
        user.email = user_data["email"]
        user.birthdate = birthdate  # You need a Custom User model to store this field
        user.save()
```
