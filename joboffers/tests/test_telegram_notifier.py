from unittest.mock import patch

from django.urls import reverse

# from ..telegram_notifier import (MODERATION_MESSAGE,
#                                  _get_absolute_joboffer_url,
#                                  send_notification_to_moderators)


# def test_get_absolute_joboffer_url(settings):
#     """Test that the url being crafted has the correct BASE_URL and the right format."""
#     dummy_url = 'http://example.com'
#     dummy_job_slug = 'python-job'
#     settings.BASE_URL = dummy_url
#     joboffer_url = reverse('joboffers:view', kwargs={'slug': dummy_job_slug})
#     expected_url = "".join((dummy_url, joboffer_url))
#     result = _get_absolute_joboffer_url(dummy_job_slug)
#     assert expected_url == result
