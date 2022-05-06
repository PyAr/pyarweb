from django.core.management.base import BaseCommand

from joboffers.tests.utils import create_analytics_sample_data


class Command(BaseCommand):
    help = 'Creates a sample joboffer with fake visualization data used for testing purposes'

    def handle(self, *args, **options):
        create_analytics_sample_data(
          test_username='publisher',
          test_offer_title='Oferta Prueba (Analítica)'
        )
