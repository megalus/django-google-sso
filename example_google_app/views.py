import httpx
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


@login_required
def secret_page(request) -> HttpResponse:
    logout_url = reverse("logout")
    return render(
        request,
        "secret_page.html",
        {"logout_url": logout_url},
    )


def single_logout_view(request):
    token = request.session.get("google_sso_access_token")
    logout(request)

    # You can revoke the Access Token here
    if token:
        httpx.post(
            "https://oauth2.googleapis.com/revoke", params={"token": token}, timeout=10
        )

    # And redirect user to Google logout page if you want
    redirect_url = reverse("admin:index")  # Or 'https://accounts.google.com/logout'
    return HttpResponseRedirect(redirect_url)
