from joboffers.management.commands import TestPublishCommand
from joboffers.publishers.mastodon import MastodonPublisher


class Command(TestPublishCommand):
    help = 'Test sending a post to Mastodon.'

    def handle(self, *args, **options):
        """Post a message to Mastodon."""
        self._handle_publish(options, MastodonPublisher)
