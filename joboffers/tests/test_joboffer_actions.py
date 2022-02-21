import pytest
from django.contrib.auth.models import AnonymousUser

from ..joboffer_actions import (
    ACTIONS, ROLE_ADMIN, ROLE_PUBLISHER,
    _get_roles, approve, create, deactivate, edit, get_history, get_valid_actions,
    reactivate, reject, request_moderation
)
from ..models import OfferState
from .factories import JobOfferFactory
from events.tests.factories import UserFactory
from pycompanies.tests.factories import UserCompanyProfileFactory


EXPECTED_ACTIONS_ADMIN = {
    OfferState.ACTIVE: {get_history.code},
    OfferState.DEACTIVATED: {get_history.code},
    OfferState.EXPIRED: {get_history.code},
    OfferState.MODERATION: {get_history.code, reject.code, approve.code},
    OfferState.NEW: set(),
    OfferState.REJECTED: {get_history.code}
}

EXPECTED_ACTIONS_PUBLISHER = {
    OfferState.NEW: {
        create.code
    },
    OfferState.DEACTIVATED: {
        edit.code,
        request_moderation.code,
        get_history.code
    },
    OfferState.REJECTED: {
        edit.code,
        get_history.code
    },
    OfferState.EXPIRED: {
        edit.code,
        deactivate.code,
        reactivate.code,
        get_history.code
    },
    OfferState.ACTIVE: {
        deactivate.code,
        get_history.code
    },
    OfferState.MODERATION: {
        get_history.code
    }
}


def test_joboffer_actions():
    """
    Assert the validity of actions according to previous state.
    """
    assert ACTIONS[ROLE_ADMIN] == EXPECTED_ACTIONS_ADMIN
    assert ACTIONS[ROLE_PUBLISHER] == EXPECTED_ACTIONS_PUBLISHER


@pytest.mark.django_db
def test_get_role_for_admin():
    """
    Check that _get_user_role() returns[PROFILE_ADMIN] only for a given superuser
    """
    user = UserFactory.create(is_superuser=True)
    joboffer = JobOfferFactory.create()

    assert _get_roles(joboffer.company, user) == {ROLE_ADMIN}


@pytest.mark.django_db
def test_get_role_for_anonymous():
    """
    Check that _get_user_role() returns empty set for a given anonymous user
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create()

    assert _get_roles(joboffer.company, user) == set()


@pytest.mark.django_db
def test_get_role_for_publisher_only():
    """
    Check that _get_user_role() returns [ROLE_PUBLISHER] for a given publisher user
    """
    user = UserFactory.create()
    company_profile = UserCompanyProfileFactory.create(user=user)

    assert _get_roles(company_profile.company, user) == {ROLE_PUBLISHER}


@pytest.mark.django_db
def test_get_role_for_publisher_and_admin():
    """
    Check that _get_user_role() returns [ROLE_PUBLISHER, ROLE_ADMIN] for a given publisher and
    admin user
    """
    user = UserFactory.create(is_superuser=True)
    company_profile = UserCompanyProfileFactory.create(user=user)

    assert _get_roles(company_profile.company, user) == {ROLE_PUBLISHER, ROLE_ADMIN}


@pytest.mark.django_db
def test_get_valid_actions_for_unlogged_user():
    """
    Test get_valid_actions return no actions for unlogged user
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create()

    assert get_valid_actions(user, joboffer.company, joboffer.state, set()) == set()


@pytest.mark.django_db
def test_get_valid_actions_publisher_joboffer_deactivated():
    """
    Test get_valid_actions() returns the actions for a publisher.
    It mockes the role
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    expected_actions = EXPECTED_ACTIONS_PUBLISHER[OfferState.DEACTIVATED]
    actions = get_valid_actions(user, joboffer.company, joboffer.state, {ROLE_PUBLISHER})

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_publisher_and_admin_joboffer_deactivated():
    """
    Test get_valid_actions() returns the actions for a publisher.
    It mockes the role.
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    expected_actions = EXPECTED_ACTIONS_PUBLISHER[OfferState.DEACTIVATED]
    actions = get_valid_actions(
        user, joboffer.company, joboffer.state, {ROLE_PUBLISHER, ROLE_ADMIN}
    )

    assert actions == expected_actions
