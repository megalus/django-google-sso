from django.contrib import messages
from loguru import logger

from django_google_sso import conf


def send_message(request, message, level: str = "error"):
    getattr(logger, level.lower())(message)
    enable_messages = getattr(conf, "GOOGLE_SSO_ENABLE_MESSAGES", False)
    if callable(enable_messages):
        enable_messages = enable_messages(request)
    if enable_messages:
        messages.add_message(request, getattr(messages, level.upper()), message)


def show_credential(credential):
    credential = str(credential)
    return f"{credential[:5]}...{credential[-5:]}"
