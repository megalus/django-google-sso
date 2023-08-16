# Troubleshooting Guide

### Common errors:

??? question "Admin Message: _**State Mismatched. Time expired?**_"
    This error occurs when the user is redirected to the Google login page and then returns to the Django login page but
    original state are not found. Please check if the browser has the anonymous session created by Django. This error
    can occur if you use `127.0.0.1` instead of `localhost` for your local tests.

??? question "Google show the message: _**The Solicitation from App XXX is Invalid.**_"
    Make sure you have added the correct Callback URI on Google Console. Please remember the trailing slash for this URI.

??? question "My custom css is not working"
    Make sure you have added the correct static files path on your `settings.py` file. Please check the
    [Django documentation](https://docs.djangoproject.com/en/4.2/howto/static-files/) for more details. Make sure your
    path is `static/django_google_sso/google_button.css`. You can also need to setup the `STATICFILES_DIRS` setting in
    your project. Check the Example app below for more details.

??? question "How can I log out Django user if I log out from Google first?"
    If you log out from Google, the Django user will not be logged out automatically - his user session is valid up to
    1 hour, or the time defined, in seconds, in `GOOGLE_SSO_SESSION_COOKIE_AGE`. You can use the `GOOGLE_SSO_SAVE_ACCESS_TOKEN`
    to save the access token generated during user login, and use it to check if the user status in Google (inside a
    Middleware, for example). Please check the [Example App](https://github.com/megalus/django-google-sso/tree/main/example_app)
    for more details.

### Example App

To test this library please check the `Example App` provided [here](https://github.com/megalus/django-google-sso/tree/main/example_app).

### Not working?

Don't panic. Get a towel and, please, open an [issue](https://github.com/megalus/django-google-sso/issues).
