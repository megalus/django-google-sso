import pytest

from django_google_sso.templatetags.sso_tags import define_sso_providers
from django_google_sso.utils import adefine_sso_providers

pytestmark = pytest.mark.django_db


def test_tags(client_with_session, settings, callback_request):

    # Arrange
    def custom_view(request):
        from django.shortcuts import render

        sso_providers = define_sso_providers({"request": request})
        sso_providers[0]["text"] = "SignWith2"

        context = {
            "sso_providers": sso_providers,
        }

        return render(request, "login.html", context)

    settings.GOOGLE_SSO_ENABLED = True
    settings.GOOGLE_SSO_PAGES_ENABLED = True

    # Act
    response = custom_view(callback_request)
    response_text = (
        response.text if hasattr(response, "text") else response.content.decode()
    )

    # Assert
    assert "SignWith2" in response_text


async def test_async_view(aclient_with_session, callback_request):

    # Arrange
    async def custom_view(request):
        from django.shortcuts import render

        sso_providers = await adefine_sso_providers(request)
        sso_providers[0]["text"] = "SignWith2"

        context = {"sso_providers": sso_providers}

        return render(request, "login.html", context)

    # Act
    response = await custom_view(callback_request)
    response_text = (
        response.text if hasattr(response, "text") else response.content.decode()
    )

    # Assert
    assert "SignWith2" in response_text
