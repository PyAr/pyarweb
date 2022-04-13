from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.contrib.sessions.backends.db import SessionStore
from django.utils.timezone import now

from events.tests.factories import UserFactory
from joboffers.tests.factories import JobOfferFactory
from joboffers.models import EventType, JobOfferAccessLog, OfferState


class Command(BaseCommand):
    help = 'Creates a sample joboffer with fake visualization data used for testing purposes'

    def handle(self, *args, **options):
        publisher = UserFactory.create(username='publisher')
        joboffer = JobOfferFactory(
          created_at=publisher,
          modified_at=publisher,
          state=OfferState.ACTIVE, title="Oferta de Prueba - Analítica"
        )

        today = now().replace(hour=0, minute=0, second=0, microsecond=0)

        event_types = [event_type.value for event_type in EventType]

        for i in range(10):
            visualization_date = today - timedelta(days=i)

            month_year = visualization_date.month * 10000 + visualization_date.year

            for event_type in event_types:
                views_amount = randint(20, 100)
                for _ in range(views_amount):
                    session = SessionStore()
                    session.create()

                    JobOfferAccessLog.objects.get_or_create(
                      created_at=visualization_date,
                      month_and_year=month_year,
                      event_type=event_type,
                      session=session.session_key,
                      joboffer=joboffer
                    )
