import hashlib
import logging
import unicodedata

from smtplib import SMTPException

from django.core.mail import send_mail
from datetime import timedelta

from django.utils import timezone

from joboffers.constants import (
  EXPIRED_OFFER_MAIL_BODY,
  EXPIRED_OFFER_MAIL_SUBJECT,
  OFFER_EXPIRATION_DAYS
)
from joboffers.models import EventType, JobOffer, JobOfferAccessLog, OfferState

UNWANTED_SORROUNDING_CHARS = "@/#*"


def normalize(tag):
    """Normalize a single tag: remove non valid chars, lower case all."""
    tag_stripped = tag.strip()
    tag_stripped = tag_stripped.strip(UNWANTED_SORROUNDING_CHARS)
    value = unicodedata.normalize("NFKD", tag_stripped.lower())
    value = value.encode('ascii', 'ignore').decode('utf-8')
    return value


def normalize_tags(tags):
    """Parse a list of tags and removed duplicated tags and non valid chars."""
    return {normalize(tag) for tag in tags}


def hash_secret(credential: str):
    """Hash a secret string (so it can be logged safely.)"""
    if credential is not None:
        digest = hashlib.sha256(credential.encode('utf-8')).hexdigest()
    else:
        digest = 'None'

    return digest


def send_mail_to_publishers(joboffer, subject: str, body: str):
    """
    Send an email to the publishers of the provided joboffer
    """
    publishers_addresses = joboffer.get_publisher_mail_addresses()

    if publishers_addresses:
        try:
            send_mail(
              subject,
              body,
              None,  # Default from mail in settings
              publishers_addresses,
              fail_silently=False
            )
        except SMTPException as e:
            logging.error(e)


def get_visualization_data(joboffer):
    """
    Retrieves a plain list of the visualizations for a joboffer
    """
    data = JobOfferAccessLog \
        .objects.filter(joboffer=joboffer) \
        .values_list('created_at', 'joboffer__id', 'joboffer__title', 'event_type')

    output_data = []

    for row in data:
        new_row = (*row, EventType(row[-1]).label)
        output_data.append(new_row)

    return output_data


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
