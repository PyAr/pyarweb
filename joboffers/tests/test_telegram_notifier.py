from unittest.mock import patch

from django.urls import reverse

from ..telegram_notifier import (MODERATION_MESSAGE,
                                 _get_absolute_joboffer_url,
                                 send_notification_to_moderators)


def test_get_absolute_joboffer_url(settings):
    """Test that the url being crafted has the correct BASE_URL and the right format."""
    dummy_url = 'http://example.com'
    dummy_job_slug = 'python-job'
    settings.BASE_URL = dummy_url
    joboffer_url = reverse('joboffers:view', kwargs={'slug': dummy_job_slug})
    expected_url = "".join((dummy_url, joboffer_url))
    result = _get_absolute_joboffer_url(dummy_job_slug)
    assert expected_url == result


def test_send_notification_to_moderators(settings):
    """Test that message has been crafted correctly."""
    dummy_job_slug = 'python-job'
    dummy_url = 'http://example.com'
    dummy_job_slug = 'python-job'
    dummy_chat_id = 1

    settings.BASE_URL = dummy_url
    settings.TELEGRAM_MODERATORS_CHAT_ID = dummy_chat_id

    joboffer_url = reverse('joboffers:view', kwargs={'slug': dummy_job_slug})
    expected_url = "".join((dummy_url, joboffer_url))
    expected_message = MODERATION_MESSAGE.format(offer_url=expected_url)

    with patch('joboffers.telegram_notifier.send_message') as mock_send_message:
        send_notification_to_moderators(dummy_job_slug)
        assert mock_send_message.called_args(expected_message, dummy_chat_id)
