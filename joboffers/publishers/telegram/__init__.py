import logging

from django.conf import settings

from joboffers.publishers import Publisher
from joboffers.telegram_api import send_message


ERROR_LOG_MESSAGE = 'Falló al querer publicar a telegram, url=%s data=%s: %s'


class TelegramPublisher(Publisher):
    """Telegram Publisher."""
    name = 'Telegram'

    def _push_to_api(self, message: str):
        """Publish a message to the configured chat group."""
        chat_id = settings.TELEGRAM_MODERATORS_CHAT_ID
        send_message(message, chat_id)

