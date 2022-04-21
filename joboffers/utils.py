import hashlib
import unicodedata

from joboffers.models import EventType, JobOfferAccessLog

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
