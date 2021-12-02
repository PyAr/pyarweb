import pytest

from ..joboffer_actions import (ACTIONS, CODE_APPROVE, CODE_COMMENT,
                                CODE_DEACTIVATE, CODE_EDIT, CODE_REACTIVATE,
                                CODE_REJECT, CODE_REQUEST_MODERATION,
                                PROFILE_ADMIN, PROFILE_PUBLISHER, approve,
                                comment, deactivate, edit, get_valid_actions,
                                reactivate, reject, request_moderation)
from ..models import OfferState
from .factories import JobOfferFactory


def test_joboffer_actions():
    """
    Assert the validity of actions according to previous state.
    """
    expected_actions_map = {
        PROFILE_ADMIN: {},
        PROFILE_PUBLISHER: {
            OfferState.DEACTIVATED: {
                edit.code: edit,
                request_moderation.code: request_moderation,
            },
            OfferState.REJECTED: {
                edit.code: edit,
            },
            OfferState.EXPIRED: {
                edit.code: edit,
                deactivate.code: deactivate,
            },
            OfferState.ACTIVE: {
                deactivate.code: deactivate,
            },
        },
    }
    assert ACTIONS == expected_actions_map


@pytest.mark.django_db
def test_get_valid_actions_user_invalid_owner():
    """Assert that when a user tries to get actions for an offer of a company they is not part of,
    raises ValueError."""
    # TODO: assert this after the programming of the relationship between company and
    # user is completed.
    ...
