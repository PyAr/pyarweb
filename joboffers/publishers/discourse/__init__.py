import logging
import uuid

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

        uuid_suffix = str(uuid.uuid4())

        post_title = f'{title} - {uuid_suffix[:8]}'

        # If post_title is shorther than the minimum required length, complete
        # with the full uuid_suffix. Even the uuid is finite, it should be
        # long enough to complete a reasonable title length.
        if len(post_title) < MIN_LENGTH_POST_TITLE:
            post_title = f"{title} - {uuid_suffix}"

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
