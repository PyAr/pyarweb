import pytest

from datetime import timedelta

from django.utils import timezone

from joboffers.constants import PENDING_MODERATION_OFFER_DAYS, TELEGRAM_PENDING_MODERATION_MESSAGE
from joboffers.models import JobOffer, OfferState
from joboffers.management.commands.notify_pending_moderation_offers import (
  notify_pending_moderation_offers
)
from .factories import JobOfferFactory
from .fixtures import create_telegram_dummy # noqa


@pytest.mark.django_db
def test_remind_offers_in_moderation(telegram_dummy):
    """
    Test expiration of old joboffers command
    """
    today = timezone.now()
    two_hundred_days_ago = today - timedelta(days=200)
    JobOfferFactory.create()
    offer2 = JobOfferFactory.create(state=OfferState.MODERATION)
    JobOfferFactory.create(state=OfferState.MODERATION)
    JobOfferFactory.create(state=OfferState.ACTIVE)

    JobOffer.objects.filter(id=offer2.id).update(modified_at=two_hundred_days_ago)

    offers_notified = notify_pending_moderation_offers()

    telegram_history = telegram_dummy.call_history
    sent_message = telegram_history[0]['text'][0]

    assert offers_notified == 1
    assert len(telegram_history) == 1
    assert sent_message.endswith(TELEGRAM_PENDING_MODERATION_MESSAGE.format(
      offer_url=offer2.get_absolute_url(),
      moderation_reminder_days=PENDING_MODERATION_OFFER_DAYS
    ))
