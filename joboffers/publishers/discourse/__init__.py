import datetime
import logging

import requests
from django.conf import settings

from joboffers.publishers import Publisher


DISCOURSE_POST_URL = f'http://{settings.DISCOURSE_HOST}/posts'

ERROR_LOG_MESSAGE = 'Falló al querer publicar a discourse, url=%s data=%s: %s'

MIN_LENGTH_POST_TITLE = 20


class DiscoursePublisher(Publisher):
    """Discourse Publisher."""

    name = 'Discourse'

    def _push_to_api(self, message: str, title: str):
        """Publish a message to discourse."""
        headers = {
            'Api-Key': settings.DISCOURSE_API_KEY,
            'Api-Username': settings.DISCOURSE_USERNAME,
        }

        current_date = datetime.datetime.today().strftime('%d/%m/%Y')

        # Post titles should have a minimum length of 20 characters
        # They cannot be padded with spaces to complete the minimum size
        # neither put those spaces in the middle, as discourse sanitizes
        # the data removing those extra spaces.
        post_title = f'{title} {current_date}'

        assert len(post_title) >= MIN_LENGTH_POST_TITLE

        payload = {
            'title': post_title,
            'raw': message,
            'category': settings.DISCOURSE_CATEGORY,
        }

        try:
            result = requests.post(DISCOURSE_POST_URL, json=payload, headers=headers)
        except Exception as err:
            status = None
            result_info = err
        else:
            status = result.status_code
            result_info = result.text

        if status != requests.codes.ok:
            logging.error(ERROR_LOG_MESSAGE, DISCOURSE_POST_URL, payload, result_info)
        return status
