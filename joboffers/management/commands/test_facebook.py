from django.core.management.base import BaseCommand

from joboffers.models import JobOffer
from joboffers.publishers.facebook import FacebookPublisher


class Command(BaseCommand):
    help = 'Test sending a post to facebook.'

    def add_arguments(self, parser):
        parser.add_argument("--offer-id", type=int, required=False)

    def handle(self, *args, **options):
        """Post a message to facebook."""
        offer_id = options.get('offer_id')
        status = None
        raw_status = None

        if offer_id is not None:
            job_offer = JobOffer.objects.get(id=offer_id)
            self.stdout.write(self.style.SUCCESS(f'Publicando oferta #{offer_id}.'))
            status = FacebookPublisher().publish(job_offer)
        else:
            self.stdout.write(self.style.SUCCESS('Publicando una prueba.'))
            raw_status = FacebookPublisher()._push_to_api('Esto es una prueba.')

        if raw_status == 200 or status == FacebookPublisher.RESULT_OK:
            self.stdout.write(self.style.SUCCESS('Oferta publicada con éxito.'))
        else:
            self.stderr.write(self.style.ERROR('Hubo un error al querer publicar la oferta.'))
