from joboffers.management.commands import TestPublishCommand
from joboffers.publishers.discourse import DiscoursePublisher


class Command(TestPublishCommand):
    help = 'Test sending a post to discourse.'

    def handle(self, *args, **options):
        """Post a message to discourse."""
        self._handle_publish(options, DiscoursePublisher)
