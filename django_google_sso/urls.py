from django.urls import path

from django_google_sso import views

app_name = "django_google_sso"

urlpatterns = [
    path("oauth2/login", views.start_login, name="oauth_start_login"),
    path("oauth2/callback", views.callback, name="oauth_callback"),
]
