import uuid
from unittest.mock import patch

from ..publishers.discourse import DiscoursePublisher


DUMMY_MESSAGE = "message"
DUMMY_TITLE = "This is a title with the right length"
DUMMY_LINK = "https://example.com/"
DUMMY_CATEGORY = "1"
DUMMY_UUID = uuid.UUID("ce322dce-ef12-4393-bebc-1ad56e4007fd")


@patch("joboffers.publishers.discourse.uuid.uuid4", return_value=DUMMY_UUID)
def test_publish_message_ok(uuid_mock, requests_mock, settings):
    """Request made to the Discourse API is ok."""
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    settings.DISCOURSE_BASE_URL = "https://localhost:9876"
    requests_mock.post("https://localhost:9876/posts.json", json="", status_code=200)

    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)

    expected_payload = {
        "title": f"{DUMMY_TITLE} - {DUMMY_UUID.hex[:8]}",
        "raw": DUMMY_MESSAGE,
        "category": settings.DISCOURSE_CATEGORY,
    }
    assert expected_payload == requests_mock.request_history[0].json()
    assert status == 200


@patch("joboffers.publishers.discourse.uuid.uuid4", return_value=DUMMY_UUID)
def test_publish_message_insufficient_title_length(uuid_mock, requests_mock, settings):
    """Fix the title being too short."""
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    settings.DISCOURSE_BASE_URL = "https://localhost:9876"
    requests_mock.post("https://localhost:9876/posts.json", json="", status_code=200)

    very_short_title = "A job!"
    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, very_short_title, DUMMY_LINK)

    expected_payload = {
        "title": f"{very_short_title} - {DUMMY_UUID.hex}",
        "raw": DUMMY_MESSAGE,
        "category": settings.DISCOURSE_CATEGORY,
    }
    assert expected_payload == requests_mock.request_history[0].json()
    assert status == 200


@patch("joboffers.publishers.discourse.requests.post", side_effect=ValueError("Oops"))
def test_publish_message_request_crash(post_mock, settings, caplog):
    """The request call ended really bad."""
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    settings.DISCOURSE_BASE_URL = "https://localhost:9876"

    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status is None

    expected_error_message = "Unknown error when publishing: ValueError('Oops')"
    assert expected_error_message in caplog.text


@patch("joboffers.publishers.discourse.uuid.uuid4", return_value=DUMMY_UUID)
def test_publish_message_request_failure(uuid_mock, requests_mock, settings, caplog):
    """The server didn"t return OK."""
    settings.DISCOURSE_CATEGORY = DUMMY_CATEGORY
    settings.DISCOURSE_BASE_URL = "https://localhost:9876"
    requests_mock.post("https://localhost:9876/posts.json", text="Problem!", status_code=500)

    status = DiscoursePublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status == 500

    real_title = f"{DUMMY_TITLE} - {DUMMY_UUID.hex[:8]}"
    expected_error_message = (
        f"Bad server response when publishing: 500 ('Problem!'); "
        f"title={real_title!r} message={DUMMY_MESSAGE!r}"
    )
    assert expected_error_message in caplog.text
