"""
Module for telegram notifications.

Apart from unittests, there is a manual test, to assert the actual send of a message to Telegram.
It can be called from cli using pytest in the root folder of the project.

pytest -s --disable-pytest-warnings joboffers/tests/send_notification_non_discoverable.py

The test file specified above, will not run automatically.

"""
import urllib.parse

import requests
from django.conf import settings
from django.urls import reverse

TELEGRAM_API_URL = 'https://api.telegram.org/bot'
MODERATION_MESSAGE = 'La oferta {offer_url} necesita ser moderada.'


def _compose_message(message: str):
    """Santitize, escape and add environment prefix to message."""
    message_with_prefix = " ".join((settings.TELEGRAM_MESSAGE_PREFIX, message))
    safe_message = urllib.parse.quote_plus(message_with_prefix)
    return safe_message


def _get_request_url(message: str, chat_id: int):
    """Compose url for telegram."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f'{TELEGRAM_API_URL}{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    return url


def _send_message(message: str, chat_id: int):
    """Send a message to a chat using a bot."""
    safe_message = _compose_message(message)
    url = _get_request_url(safe_message, chat_id)
    status = requests.get(url)
    return status


def _get_absolute_joboffer_url(job_slug: str):
    """Get the complete offer URL including the domain."""
    job_url = reverse('joboffers:view', kwargs={'slug': job_slug})
    complete_url = "".join((settings.BASE_URL, job_url))
    return complete_url


def send_notification_to_moderators(job_slug: str):
    """Send a notification of a slug thats needs to be moderated to moderator's group."""
    complete_offer_slug_url = _get_absolute_joboffer_url(job_slug)
    moderation_message = MODERATION_MESSAGE.format(offer_url=complete_offer_slug_url)
    status = _send_message(moderation_message, settings.TELEGRAM_MODERATORS_CHAT_ID)
    return status
