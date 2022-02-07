import requests
from django.conf import settings

from .models import JobOffer
from .publisher import Publisher


def publish(message):
    """Publish a message to the configured facebook page."""
    post_url = f'https://graph.facebook.com/{settings.FACEBOOK_PAGE_ID}/feed'
    payload = {
        'message': message,
        'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
    }
    result = requests.post(post_url, data=payload)
    # TODO: Add error management
    return result


class FacebookPublisher(Publisher):
    """Facebook Publisher."""
    name = 'Facebook'
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        # TODO: Create template from offer
        message = 'This is a test message'
        publish(message)
        ...

    @classmethod
    def _render_offer(cls, job_offer: 'JobOffer'):
        raise NotImplementedError



