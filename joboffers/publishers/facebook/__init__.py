import logging

import requests
from django.conf import settings

from joboffers.models import JobOffer
from joboffers.publishers import Publisher


def publish(message):
    """Publish a message to the configured facebook page."""
    post_url = f'https://graph.facebook.com/{settings.FACEBOOK_PAGE_ID}/feed'
    payload = {
        'message': message,
        'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
    }
    status = None

    try:
        result = requests.post(post_url, data=payload)
    except Exception as err:
        status = requests.codes.server_error
        logging.error(f'Falló al querer publicar a facebook url={post_url} data={payload}: {err}')
    else:
        status = result.status_code

    if status != requests.codes.ok:
        logging.error(f'Falló al querer publicar a facebook url={post_url} data={payload}:'
                      f'{result.text}')
    return status


class FacebookPublisher(Publisher):
    """Facebook Publisher."""
    name = 'Facebook'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        message = cls._render_offer(job_offer)
        status = publish(message)
        if status == requests.codes.ok:
            return cls.RESULT_OK
        else:
            return cls.RESULT_BAD
