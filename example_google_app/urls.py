"""example_google_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

from example_google_app.settings import INSTALLED_APPS
from example_google_app.views import secret_page, single_logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("secret/", secret_page),
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="google_sso/login.html"
        ),  # The modified form with google button
    ),
    path("accounts/logout/", single_logout_view, name="logout"),
]

if "grappelli" in INSTALLED_APPS:
    urlpatterns += [path("grappelli/", include("grappelli.urls"))]

if "jet" in INSTALLED_APPS:
    urlpatterns += [
        path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
        path("jet/", include("jet.urls", "jet")),
    ]

urlpatterns += [
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
