import logging

import requests
from django.conf import settings

from joboffers.publishers import Publisher


FACEBOOK_POST_URL = f'https://graph.facebook.com/{settings.FACEBOOK_PAGE_ID}/feed'

ERROR_LOG_MESSAGE = 'Falló al querer publicar a facebook, url=%s data=%s: %s'


class FacebookPublisher(Publisher):
    """Facebook Publisher."""
    name = 'Facebook'

    def _push_to_api(self, message: str, title: str):
        """Publish a message to the configured facebook page."""
        payload = {
            'message': message,
            'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
        }

        try:
            result = requests.post(FACEBOOK_POST_URL, data=payload)
        except Exception as err:
            status = None
            result_info = err
        else:
            status = result.status_code
            result_info = result.text

        if status != requests.codes.ok:
            logging.error(ERROR_LOG_MESSAGE, FACEBOOK_POST_URL, payload, result_info)
        return status
