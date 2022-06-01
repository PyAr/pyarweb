from unittest.mock import patch

from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publishers.discourse import (
    ERROR_LOG_MESSAGE,
    DISCOURSE_POST_URL,
    DiscoursePublisher,
)

DUMMY_MESSAGE = 'message'
DUMMY_TITLE = 'This is a title with the right length'
DUMMY_TITLE_SHORT = 'Short'
DUMMY_LINK = 'https://example.com/'
DUMMY_CATEGORY = '1'
DUMMY_EXCEPTION_MESSAGE = 'Oops'
DUMMY_BAD_REQUEST_TEXT = 'This is bad'
DUMMY_UUID = 'aafd27ff-8baf-433b-82eb-8c7fada847da'


class DummyRequest:
    status_code = 400
    text = DUMMY_BAD_REQUEST_TEXT


def mocked_uuid():
    """Mock of uuid4 method."""
    return DUMMY_UUID


@patch('joboffers.publishers.discourse.uuid.uuid4')
def test_publish_message_ok(uuid_mock, requests_mock: Mocker, settings):
    """Test that a requests made to the facebook api is ok."""
    requests_mock.post(DISCOURSE_POST_URL, json='', status_code=200)
    uuid_mock.return_value = DUMMY_UUID
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    try:
        status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    except NoMockAddress:
        assert (
            False
        ), 'publish_offer raised an exception, wich means that the url is malformed.'

    post_title = f'{DUMMY_TITLE} - {DUMMY_UUID[:8]}'

    expected_payload = {
        'title': post_title,
        'raw': DUMMY_MESSAGE,
        'category': settings.DISCOURSE_CATEGORY,
    }

    assert expected_payload == requests_mock.request_history[0].json()
    assert status == 200


@patch('joboffers.publishers.discourse.uuid.uuid4')
def test_publish_message_insufficient_title_length(uuid_mock, requests_mock: Mocker, settings):
    """Test that a requests made to the discourse api with a short title."""
    requests_mock.post(DISCOURSE_POST_URL, json='', status_code=200)
    uuid_mock.return_value = DUMMY_UUID
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE_SHORT, DUMMY_LINK)

    post_title = f'{DUMMY_TITLE_SHORT} - {DUMMY_UUID}'

    expected_payload = {
        'title': post_title,
        'raw': DUMMY_MESSAGE,
        'category': settings.DISCOURSE_CATEGORY,
    }

    assert expected_payload == requests_mock.request_history[0].json()
    assert status == 200


@patch(
    'joboffers.publishers.discourse.requests.post',
    side_effect=Exception(DUMMY_EXCEPTION_MESSAGE),
)
@patch('joboffers.publishers.discourse.uuid.uuid4', mocked_uuid)
def test_publish_message_generic_error(post_mock, settings, caplog):
    """Test error handling of requests with a general error."""
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)

    post_title = f'{DUMMY_TITLE} - {DUMMY_UUID[:8]}'

    payload = {'title': post_title, 'raw': DUMMY_MESSAGE, 'category': DUMMY_CATEGORY}

    expected_error_message = ERROR_LOG_MESSAGE % (
        DISCOURSE_POST_URL,
        payload,
        DUMMY_EXCEPTION_MESSAGE,
    )

    assert expected_error_message in caplog.text
    assert status is None
