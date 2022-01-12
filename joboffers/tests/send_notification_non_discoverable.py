"""
This is not a discoverable test file. Its purpose is to test the actual
notification to a telegram group. This test can only be run by hand.
"""
import pytest
import requests

from ..telegram_notifier import send_notification_to_moderators


def test_send_notification():
    """Test sending a real notification to telegram."""
    response = send_notification_to_moderators('trabajito-python')

    assert response.status_code == 200
