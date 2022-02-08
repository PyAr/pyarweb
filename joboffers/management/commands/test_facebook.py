from django.core.management.base import BaseCommand

from joboffers.publisher.facebook import publish


class Command(BaseCommand):
    help = 'Test sending a post to facebook.'

    def handle(self, *args, **options):
        """Test that the offer is send to the facebook publishers."""
        publish('Esto es una prueba.')
        self.stdout.write(self.style.SUCCESS('POST de prueba enviado'))
