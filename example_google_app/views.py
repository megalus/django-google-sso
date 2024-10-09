import httpx
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


@login_required
def secret_page(request):
    logout_url = reverse("logout")
    body = f"<h2>You're looking at the secret page.</h2><a href={logout_url}>Logout</a>"
    return HttpResponse(body)


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
