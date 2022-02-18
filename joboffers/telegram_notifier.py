from django.conf import settings
from django.urls import reverse

from joboffers.telegram_api import send_message

MODERATION_MESSAGE = 'La oferta {offer_url} necesita ser moderada.'


def _get_absolute_joboffer_url(job_slug: str):
    """Get the complete offer URL including the domain."""
    job_url = reverse('joboffers:view', kwargs={'slug': job_slug})
    complete_url = "".join((settings.BASE_URL, job_url))
    return complete_url


def send_notification_to_moderators(job_slug: str):
    """Send a notification of a slug thats needs to be moderated to moderator's group."""
    complete_offer_slug_url = _get_absolute_joboffer_url(job_slug)
    moderation_message = MODERATION_MESSAGE.format(offer_url=complete_offer_slug_url)
    status = send_message(moderation_message, settings.TELEGRAM_MODERATORS_CHAT_ID)
    return status
