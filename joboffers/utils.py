import hashlib
import unicodedata

from django.core.mail import send_mail

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
    publishers_addresses = joboffer.get_publisher_mail_addresses()

    if publishers_addresses:
        send_mail(
          subject,
          body,
          None,  # Default from mail in settings
          publishers_addresses,
          fail_silently=False
        )
