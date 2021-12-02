import pytest

from ..joboffer_actions import (ACTIONS, CODE_APPROVE, CODE_COMMENT,
                                CODE_DEACTIVATE, CODE_EDIT, CODE_REACTIVATE,
                                CODE_REJECT, CODE_REQUEST_MODERATION,
                                PROFILE_ADMIN, PROFILE_PUBLISHER, approve,
                                comment, deactivate, edit, get_history,
                                get_valid_actions, reactivate, reject,
                                request_moderation)
from ..models import OfferState
from .factories import JobOfferFactory


def test_joboffer_actions():
    """
    Assert the validity of actions according to previous state.
    """
    expected_actions_admin = {
            OfferState.MODERATION:{
                approve.code: approve,
                comment.code: comment,
                reject.code: reject,
            }
        }

    expected_actions_publisher = {
            OfferState.DEACTIVATED: {
                edit.code: edit,
                request_moderation.code: request_moderation,
                get_history.code: get_history
            },
            OfferState.REJECTED: {
                edit.code: edit,
                get_history.code: get_history
            },
            OfferState.EXPIRED: {
                edit.code: edit,
                deactivate.code: deactivate,
                reactivate.code: reactivate,
                get_history.code: get_history
            },
            OfferState.ACTIVE: {
                deactivate.code: deactivate,
                get_history.code: get_history
            },
        }

    assert ACTIONS[PROFILE_ADMIN] == expected_actions_admin
    assert ACTIONS[PROFILE_PUBLISHER] == expected_actions_publisher


@pytest.mark.django_db
def test_get_valid_actions_user_invalid_owner():
    """Assert that when a user tries to get actions for an offer of a company they is not part of,
    raises ValueError."""
    # TODO: assert this after the programming of the relationship between company and
    # user is completed.
    ...
