from joboffers.management.commands import TestPublishCommand
from joboffers.publishers.twitter import TwitterPublisher


class Command(TestPublishCommand):
    help = 'Test sending a post to twitter.'

    def handle(self, *args, **options):
        """Post a message to twitter."""
        self._handle_publish(options, TwitterPublisher)
