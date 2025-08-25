# How Django Google SSO works?

## Current Flow

1. First, the user is redirected to the Django login page. If settings `GOOGLE_SSO_ENABLED` is True, the
"Login with Google" button will be added to a default form.

2. On click, **Django-Google-SSO** will add, in a anonymous request session, the `sso_next_url` and Google Flow `sso_state`.
This data will expire in 10 minutes. Then user will be redirected to Google login page.

    !!! info "Using Request Anonymous session"
        If you make any actions which change or destroy this session, like restart django, clear cookies or change
        browsers, the login will fail, and you can see the message "State Mismatched. Time expired?" in the next time
        you log in again.

3. On callback, **Django-Google-SSO** will check `code` and `state` received. If they are valid,
Google's UserInfo will be retrieved. If the user is already registered in Django, the user
will be logged in.

4. Otherwise, the user will be created and logged in, if his email domain,
matches one of the `GOOGLE_SSO_ALLOWABLE_DOMAINS`. You can disable the auto-creation setting `GOOGLE_SSO_AUTO_CREATE_USERS`
to False.

5. On creation only, this user can be set to the`staff` or `superuser` status, if his email are in `GOOGLE_SSO_STAFF_LIST` or
`GOOGLE_SSO_SUPERUSER_LIST` respectively. Please note if you add an email to one of these lists, the email domain
must be added to `GOOGLE_SSO_ALLOWABLE_DOMAINS`too.

6. This authenticated session will expire in 1 hour, or the time defined, in seconds, in `GOOGLE_SSO_SESSION_COOKIE_AGE`.

7.  If login fails, you will be redirected to route defined in `GOOGLE_SSO_LOGIN_FAILED_URL` (default: `admin:index`)
which will use Django Messaging system to show the error message.

8. If login succeeds, the user will be redirected to the `next_path` saved in the anonymous session, or to the route
defined in `GOOGLE_SSO_NEXT_URL` (default: `admin:index`) as a fallback.

## About the Google consent screen and the authorization prompt

The setting `GOOGLE_SSO_AUTHORIZATION_PROMPT` controls the `prompt` parameter sent to Google's OpenID Connect authorization URL. It changes what Google shows to the user during authentication/consent:

- `"consent"` (default): Always shows the consent screen, even if the user previously granted access to the requested scopes.
- `"select_account"`: Always shows the account chooser so the user can switch Google accounts before continuing.
- `"none"`: Never shows any screen. If the user is not already signed in to Google or has not granted consent yet, Google will return an error instead of showing screens.
- `None` (or `""`): Only show the relevant screens when they are needed. If the user is only logged in to one google account and that account has already consented, both the account and consent screens are bypassed. If consent hasn't been given, or the user is signed in to multiple google accounts, the relevant screens are shown. This is the default google prompt behavior.

Notes when testing locally:
- If you have already granted consent to the default scopes (`openid`, `userinfo.email`, `userinfo.profile`) for your app, Google may only show the account selection step. This can make it seem like the experience is always the same.
- To see the full consent screen again with `consent`, you can revoke the app permissions from your Google Account (Google Account -> Security -> Third-party access), or change the Scopes to include a new permission.
- Using `select_account` typically results in the “Choose an account” screen, which matches what you are observing locally.

Example configuration in your Django settings:

```python
# Valid values: "none", "consent", "select_account"
GOOGLE_SSO_AUTHORIZATION_PROMPT = "consent"  # default is "consent"
```

For more details about `prompt`, see Google's documentation: https://developers.google.com/identity/openid-connect/openid-connect#prompt
