from django.urls import path

from django_google_sso import conf, views

app_name = "django_google_sso"

urlpatterns = []

if conf.GOOGLE_SSO_ENABLED:
    urlpatterns += [
        path("login/", views.start_login, name="oauth_start_login"),
        path("callback/", views.callback, name="oauth_callback"),
    ]
