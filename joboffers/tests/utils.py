from datetime import timedelta
from random import randint

from django.contrib.messages import get_messages as contrib_get_messages
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from events.tests.factories import UserFactory
from joboffers.tests.factories import JobOfferFactory
from joboffers.models import OfferState, EventType, JobOfferAccessLog


def create_analytics_sample_data(
    test_username: str, test_offer_title: str, test_company=None, max_views_amount=100
):
    """
    Create a sample joboffer with random ammounts views (JobOfferAccessLog) for testing purposes.
    It creates an offer with the given title if it does not exist or adds views to the same offer
    if there is already an offer with the same title.
    """
    DAYS_BEFORE = 10  # Amount of days from where to start adding views

    try:
        User = get_user_model()
        publisher = User.objects.get(username=test_username)
    except User.DoesNotExist:
        publisher = UserFactory.create(username=test_username)

    if test_company:
        joboffer = JobOfferFactory(
          company=test_company,
          created_at=publisher,
          modified_at=publisher,
          state=OfferState.ACTIVE,
          title=test_offer_title
        )
    else:
        joboffer = JobOfferFactory(
          created_at=publisher,
          modified_at=publisher,
          state=OfferState.ACTIVE,
          title=test_offer_title
        )

    today = now().replace(hour=0, minute=0, second=0, microsecond=0)

    event_types = [event_type.value for event_type in EventType]

    total_views = 0

    for i in range(DAYS_BEFORE):
        visualization_date = today - timedelta(days=i)

        month_year = visualization_date.month * 10000 + visualization_date.year

        for event_type in event_types:
            views_amount = randint(5, max_views_amount)
            for __ in range(views_amount):
                session = SessionStore()
                session.create()

                created_at = visualization_date.replace(
                  hour=randint(0, 23), minute=randint(0, 59), second=randint(0, 59)
                )

                JobOfferAccessLog.objects.get_or_create(
                  created_at=created_at,
                  month_and_year=month_year,
                  event_type=event_type,
                  session=session.session_key,
                  joboffer=joboffer
                )

                total_views += 1

    return joboffer, total_views


def get_plain_messages(request):
    """
    Gets a plain text message from a given request/response object. Useful for testing messages
    """
    messages = contrib_get_messages(request.wsgi_request)
    return [m.message for m in messages]
