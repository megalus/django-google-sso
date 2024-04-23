from django.contrib import messages
from loguru import logger

from django_google_sso import conf


def send_message(request, message, level: str = "error"):
    getattr(logger, level.lower())(message)
    if conf.GOOGLE_SSO_ENABLE_MESSAGES:
        messages.add_message(request, getattr(messages, level.upper()), message)


def show_credential(credential):
    credential = str(credential)
    return f"{credential[:5]}...{credential[-5:]}"
