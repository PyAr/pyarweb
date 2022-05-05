from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from joboffers.constants import (
  EXPIRED_OFFER_MAIL_BODY,
  EXPIRED_OFFER_MAIL_SUBJECT,
  OFFER_EXPIRATION_DAYS
)
from joboffers.models import EventType, JobOffer, OfferState
from joboffers.utils import send_mail_to_publishers


def expire_old_offers():
    """
    Mark old job offers as EXPIRED and send a mail to the publishers
    """
    expiration_date = timezone.now() - timedelta(days=OFFER_EXPIRATION_DAYS)
    joboffers = JobOffer.objects.filter(
      state=OfferState.ACTIVE, modified_at__lte=expiration_date
    )

    for joboffer in joboffers:
        subject = EXPIRED_OFFER_MAIL_SUBJECT % {'title': joboffer.title}
        body = EXPIRED_OFFER_MAIL_BODY % {
          'title': joboffer.title,
          'offer_url': joboffer.get_absolute_url(),
          'listing_views': joboffer.get_visualizations_amount(EventType.LISTING_VIEW),
          'detail_views': joboffer.get_visualizations_amount(EventType.DETAIL_VIEW),
          'contact_info_views': joboffer.get_visualizations_amount(EventType.CONTACT_INFO_VIEW),
          'expiration_days': OFFER_EXPIRATION_DAYS
        }
        joboffer.state = OfferState.EXPIRED
        joboffer.save()

        send_mail_to_publishers(joboffer, subject, body)


class Command(BaseCommand):
    help = 'Queries the database for expired offers and send the mails to the publishers'

    def handle(self, *args, **options):
        expire_old_offers()
