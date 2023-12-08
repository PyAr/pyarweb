import logging
import uuid

import requests
from django.conf import settings

from joboffers.publishers import Publisher

MIN_LENGTH_POST_TITLE = 20


class DiscoursePublisher(Publisher):
    """Discourse Publisher."""

    name = 'Discourse'

    def _push_to_api(self, message: str, title: str, link: str):
        """Publish a message to discourse."""
        headers = {
            'Api-Key': settings.DISCOURSE_API_KEY,
            'Api-Username': settings.DISCOURSE_USERNAME,
        }

        uuid_suffix = uuid.uuid4().hex

        # make the title unique by appending part of an uuid; however if the title
        # is too short for discourse use the whole uuid
        post_title = f'{title} - {uuid_suffix[:8]}'
        if len(post_title) < MIN_LENGTH_POST_TITLE:
            post_title = f"{title} - {uuid_suffix}"

        payload = {
            'title': post_title,
            'raw': message,
            'category': settings.DISCOURSE_CATEGORY,
        }

        url = f'{settings.DISCOURSE_BASE_URL}/posts.json'
        try:
            resp = requests.post(url, json=payload, headers=headers)
        except Exception as err:
            logging.error("Unknown error when publishing: %r", err)
            status = None
        else:
            status = resp.status_code
            if status != requests.codes.ok:
                logging.error(
                    "Bad server response when publishing: %s (%r); title=%r message=%r",
                    status, resp.text, post_title, message)

        return status
