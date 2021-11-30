import pytest

from ..joboffer_actions import (ACTIONS, CODE_APPROVE, CODE_COMMENT,
                                CODE_DEACTIVATE, CODE_EDIT, CODE_REACTIVATE,
                                CODE_REJECT, CODE_REQUEST_MODERATION,
                                PROFILE_ADMIN, PROFILE_PUBLISHER, approve,
                                comment, deactivate, edit, reactivate, reject,
                                request_moderation)
from ..models import OfferState


#@pytest.mark.django_db
def test_valid_actions():
    """
    Assert that the validity of actions according to previous state.
    """

    expected_actions_map = {
        PROFILE_ADMIN: {

        },
        PROFILE_PUBLISHER: {

        }
    }
    ...

