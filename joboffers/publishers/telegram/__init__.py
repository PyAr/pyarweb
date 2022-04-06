from django.conf import settings

from joboffers.publishers import Publisher
from joboffers.telegram_api import send_message


class TelegramPublisher(Publisher):
    """Telegram Publisher."""
    name = 'Telegram'

    def _push_to_api(self, message: str):
        """Publish a message to the configured chat group."""
        chat_id = settings.TELEGRAM_PUBLIC_CHAT_ID
        return send_message(message, chat_id)
