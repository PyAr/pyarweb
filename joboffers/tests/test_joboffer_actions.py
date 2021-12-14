import pytest

from django.contrib.auth.models import AnonymousUser

from events.tests.factories import UserFactory

from .factories import JobOfferFactory
from ..joboffer_actions import (
    ACTIONS, ROLE_ADMIN, ROLE_GUEST, ROLE_PUBLISHER, approve, deactivate, edit, get_history,
    reactivate, reject, request_moderation, get_valid_actions, _get_roles
)
from ..models import OfferState


# TODO: Reactivate this test
def test_joboffer_actions():
    """
    Assert the validity of actions according to previous state.
    """
    expected_actions_admin = {
            OfferState.MODERATION: {
                approve.code: approve,
                reject.code: reject,
            },
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

    assert ACTIONS[ROLE_ADMIN] == expected_actions_admin
    assert ACTIONS[ROLE_PUBLISHER] == expected_actions_publisher


@pytest.mark.django_db
def teeeeest_get_valid_actions_for_anonymous_user():
    """
    Test that there are no actions for unlogged users
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create()
    actions = get_valid_actions(joboffer, user)

    assert [] == actions


@pytest.mark.django_db
def test_get_user_role_for_admin():
    """
    Check that _get_user_role() returns PROFILE_ADMIN for a given superuser
    """
    user = UserFactory.create(is_superuser=True)
    joboffer = JobOfferFactory.create()

    assert [ROLE_ADMIN] == _get_roles(joboffer, user)


@pytest.mark.django_db
def test_get_user_role_for_anonymous():
    """
    Check that _get_user_role() returns ROLE_GUEST for a given anonymous user
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create()

    assert [ROLE_GUEST] == _get_roles(joboffer, user)


@pytest.mark.django_db
def test_get_valid_actions_user_invalid_owner():
    """Assert that when a user tries to get actions for an offer of a company they is not part of,
    raises ValueError."""
    # TODO: assert this after the programming of the relationship between company and
    # user is completed.
    ...
