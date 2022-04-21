from django.core.management.base import BaseCommand

from joboffers.models import JobOffer


class TestPublishCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--offer-id", type=int, required=False)

    def _handle_publish(self, options, publisher_class):
        """Command handler for any publisher."""
        offer_id = options.get('offer_id')
        status = None
        raw_status = None
        publisher = publisher_class()

        if offer_id is not None:
            job_offer = JobOffer.objects.get(id=offer_id)
            self.stdout.write(self.style.SUCCESS(f'Publicando oferta #{offer_id}.'))
            status = publisher.publish(job_offer)
        else:
            self.stdout.write(self.style.SUCCESS('Publicando una prueba.'))
            raw_status = publisher._push_to_api(
                'Esto es una prueba de post.', 'Título de prueba'
            )

        if raw_status == 200 or status == publisher.RESULT_OK:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Oferta publicada con éxito en: {publisher.name}.'
                )
            )
        else:
            self.stderr.write(
                self.style.ERROR(
                    f'Hubo un error al querer publicar la oferta en: {publisher.name}.'
                )
            )
