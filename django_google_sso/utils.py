import asyncio
from typing import Any, Callable, Coroutine

from asgiref.sync import sync_to_async
from django.contrib import messages
from loguru import logger

from django_google_sso import conf
from django_google_sso.templatetags.show_form import define_show_form
from django_google_sso.templatetags.sso_tags import define_sso_providers


def send_message(request, message, level: str = "error"):
    getattr(logger, level.lower())(message)
    enable_messages = conf.GOOGLE_SSO_ENABLE_MESSAGES
    if callable(enable_messages):
        enable_messages = enable_messages(request)
    if enable_messages:
        messages.add_message(request, getattr(messages, level.upper()), message)


def show_credential(credential):
    credential = str(credential)
    return f"{credential[:5]}...{credential[-5:]}"


def async_(
    func: Callable,
) -> Callable[..., Any] | Callable[[Any, Any], Coroutine[Any, Any, Any]]:
    """Returns a coroutine function."""
    return func if asyncio.iscoroutinefunction(func) else sync_to_async(func)


async def adefine_sso_providers(request):
    context = {"request": request}
    return await async_(define_sso_providers)(context)


async def adefine_show_form(request):
    context = {"request": request}
    return await async_(define_show_form)(context)
