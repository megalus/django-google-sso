from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse


@login_required
def secret_page(request):
    logout_url = reverse("logout")
    body = f"<h2>You're looking at the secret page.</h2><a href={logout_url}>Logout</a>"
    return HttpResponse(body)
