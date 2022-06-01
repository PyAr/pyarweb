from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import gettext as _

from joboffers.constants import PENDING_MODERATION_OFFER_DAYS, TELEGRAM_PENDING_MODERATION_MESSAGE
from joboffers.models import JobOffer, OfferState
from joboffers.telegram_api import send_notification_to_moderators


def notify_pending_moderation_offers():
    """
    Notify all the moderators that there is a pending joboffer offer moderation
    """
    expiration_date = timezone.now() - timedelta(days=PENDING_MODERATION_OFFER_DAYS)
    joboffers = JobOffer.objects.filter(
      state=OfferState.MODERATION, modified_at__lte=expiration_date
    )

    for joboffer in joboffers:
        message = TELEGRAM_PENDING_MODERATION_MESSAGE.format(
          offer_url=joboffer.get_absolute_url(),
          moderation_reminder_days=PENDING_MODERATION_OFFER_DAYS
        )

        send_notification_to_moderators(message)

    return len(joboffers)


class Command(BaseCommand):
    help = '''
    Check for pending moderation offers and send a telegram notification to the moderators group
    '''

    def handle(self, *args, **options):
        offers_notifed = notify_pending_moderation_offers()

        self.stdout.write(
          self.style.SUCCESS(
            _('Se enviaron {offers_notified} recordatorios de moderación.').format(
              offers_notified=offers_notifed
            )
          )
        )
