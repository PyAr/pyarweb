from joboffers.management.commands import TestPublishCommand
from joboffers.publishers.facebook import FacebookPublisher


class Command(TestPublishCommand):
    help = 'Test sending a post to facebook.'

    def handle(self, *args, **options):
        """Post a message to facebook."""
        self._handle_publish(options, FacebookPublisher)
