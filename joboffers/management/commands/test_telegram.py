from joboffers.management.commands import TestPublishCommand
from joboffers.publishers.telegram import TelegramPublisher


class Command(TestPublishCommand):
    help = 'Test sending a message to telegram public group.'

    def handle(self, *args, **options):
        """Post a message to telegram."""
        self._handle_publish(options, TelegramPublisher)
