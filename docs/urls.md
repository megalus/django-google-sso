# Setup Django URLs

The base configuration for Django URLs is the same we have described as before:
```python
# urls.py

from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "google_sso/", include(
            "django_google_sso.urls",
            namespace="django_google_sso"
        )
    ),
]
```
You can change the initial Path - `google_sso/` - to whatever you want - just remember to change it in the Google Console as well.

## Overriding the Login view or Path

If you need to override the login view, or just the path, please add on the new view/class the **Django SSO Admin** login template:

```python
from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    # other urlpatterns...
    path(
        "accounts/login/",
        LoginView.as_view(
            # The modified form with Google button
            template_name="google_sso/login.html"
        ),
    ),
]
```

or

```python
from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    template_name = "google_sso/login.html"
```
