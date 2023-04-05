# Troubleshooting Guide

### Common errors:

??? question "Admin Message: _**State Mismatched. Time expired?**_"
    This error occurs when the user is redirected to the Google login page and then returns to the Django login page but
    original state are not found. Please check if the browser has the anonymous session created by Django.

??? question "Google show the message: _**The Solicitation from App XXX is Invalid.**_"
    Make sure you have added the correct Callback URI on Google Console. Please remember the trailing slash for this URI..

### Example App

To test this library please check the `Example App` provided [here](https://github.com/megalus/django-google-sso/tree/main/example_app).

### Not working?

Don't panic. Get a towel and, please, open an [issue](https://github.com/megalus/django-google-sso/issues).
