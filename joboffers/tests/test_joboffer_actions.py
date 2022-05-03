
import pytest
from django.contrib.auth.models import AnonymousUser

from events.tests.factories import UserFactory
# Fixtures
from pycompanies.tests.fixtures import create_user_company_profile # noqa
#
from pycompanies.tests.factories import UserCompanyProfileFactory

from ..joboffer_actions import (
    ACTIONS, ROLE_ADMIN, ROLE_PUBLISHER,
    _get_roles, analytics, approve, create, deactivate, edit, get_history, get_valid_actions,
    reactivate, reject, request_moderation
)
from ..models import OfferState
from .factories import JobOfferCommentFactory, JobOfferFactory


EXPECTED_ACTIONS_ADMIN = {
    OfferState.ACTIVE: {analytics.code, deactivate.code, get_history.code},
    OfferState.DEACTIVATED: {analytics.code, get_history.code},
    OfferState.MODERATION: {analytics.code, get_history.code, reject.code, approve.code},
    OfferState.EXPIRED: {analytics.code, deactivate.code, reactivate.code, get_history.code},
    OfferState.NEW: set(),
    OfferState.REJECTED: {analytics.code, get_history.code}
}

EXPECTED_ACTIONS_PUBLISHER = {
    OfferState.NEW: {
        create.code
    },
    OfferState.DEACTIVATED: {
        edit.code,
        request_moderation.code,
        get_history.code,
        analytics.code
    },
    OfferState.REJECTED: {
        edit.code,
        get_history.code,
        analytics.code
    },
    OfferState.EXPIRED: {
        edit.code,
        deactivate.code,
        reactivate.code,
        get_history.code,
        analytics.code
    },
    OfferState.ACTIVE: {
        deactivate.code,
        get_history.code,
        analytics.code
    },
    OfferState.MODERATION: {
        get_history.code,
        analytics.code
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

    assert _get_roles(user, joboffer.company) == {ROLE_ADMIN}


@pytest.mark.django_db
def test_get_role_for_anonymous():
    """
    Check that _get_roles() returns empty set for a given anonymous user
    """
    user = AnonymousUser()

    assert _get_roles(user, None) == set()


@pytest.mark.django_db
def test_get_role_for_publisher_without_a_company():
    """
    Check that _get_roles() returns [ROLE_PUBLISHER] for a given publisher user
    """
    user = UserFactory.create()
    UserCompanyProfileFactory.create(user=user)

    assert _get_roles(user, None) == {ROLE_PUBLISHER}


@pytest.mark.django_db
def test_get_roles_for_publisher_for_a_different_compay_company():
    """
    Check that _get_roles() returns [] for a given publisher from another company
    """
    user = UserFactory.create()
    company_profile = UserCompanyProfileFactory.create()

    assert _get_roles(user, company_profile.company) == set()


@pytest.mark.django_db
def test_get_roles_for_publisher_with_matching_company():
    """
    Check that _get_roles() returns [ROLE_PUBLISHER] for a given publisher user
    """
    user = UserFactory.create()
    company_profile = UserCompanyProfileFactory.create(user=user)

    assert _get_roles(user, company_profile.company) == {ROLE_PUBLISHER}


@pytest.mark.django_db
def test_get_role_for_publisher_and_admin():
    """
    Check that _get_role() returns [ROLE_PUBLISHER, ROLE_ADMIN] for a given publisher and
    admin user
    """
    user = UserFactory.create(is_superuser=True)
    company_profile = UserCompanyProfileFactory.create(user=user)

    assert _get_roles(user, company_profile.company) == {ROLE_PUBLISHER, ROLE_ADMIN}


@pytest.mark.django_db
def test_get_valid_actions_for_unlogged_user():
    """
    Test get_valid_actions return no actions for unlogged user
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create()

    assert get_valid_actions(user, joboffer, set()) == set()


@pytest.mark.django_db
def test_get_valid_actions_publisher_joboffer_deactivated():
    """
    Test get_valid_actions() returns the actions for a publisher for deactivated offer.
    It mockes the role
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    expected_actions = EXPECTED_ACTIONS_PUBLISHER[OfferState.DEACTIVATED]
    actions = get_valid_actions(user, joboffer, {ROLE_PUBLISHER})

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_publisher_joboffer_active():
    """
    Test get_valid_actions() returns the actions for a publisher for active offer.
    It mockes the role
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE)

    expected_actions = EXPECTED_ACTIONS_PUBLISHER[OfferState.ACTIVE]
    actions = get_valid_actions(user, joboffer, {ROLE_PUBLISHER})

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_publisher_joboffer_rejected():
    """
    Test get_valid_actions() returns the actions for a publisher for rejected offer
    It mockes the role
    """
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.REJECTED)
    JobOfferCommentFactory.create(joboffer=joboffer)

    expected_actions = EXPECTED_ACTIONS_PUBLISHER[OfferState.REJECTED]
    actions = get_valid_actions(user, joboffer, {ROLE_PUBLISHER})

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
        user, joboffer, {ROLE_PUBLISHER, ROLE_ADMIN}
    )

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_admin_that_rejected_an_offer():
    """
    Test get_valid_actions() return reject and accept action for a moderated joboffer.
    It mockes the role.
    """
    joboffer = JobOfferFactory.create(state=OfferState.REJECTED)
    comment = JobOfferCommentFactory.create(joboffer=joboffer)
    user = comment.created_by

    expected_actions = {analytics.code, approve.code, reject.code, get_history.code}

    actions = get_valid_actions(
        user, joboffer, {ROLE_ADMIN}
    )

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_admin_that_approved_an_offer():
    """
    Test get_valid_actions() return reject and accept action for a moderated joboffer.
    It mockes the role.
    """
    user = UserFactory.create(is_superuser=True)
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE, modified_by=user)

    expected_actions = {
      analytics.code, reject.code, deactivate.code, get_history.code
    }

    actions = get_valid_actions(
        user, joboffer, {ROLE_ADMIN}
    )

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_for_admin_that_didnt_approved_the_offer():
    """
    Test get_valid_actions() doesn't have return reject/accept for an active offer accepted by a
    different user. It mockes the role.
    """
    user = UserFactory.create(is_superuser=True)
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE)

    expected_actions = {analytics.code, deactivate.code, get_history.code}

    actions = get_valid_actions(
        user, joboffer, {ROLE_ADMIN}
    )

    assert actions == expected_actions


@pytest.mark.django_db
def test_get_valid_actions_publisher_with_active_offer(user_company_profile):
    """
    Test get_valid_actions() doesn't allow to accept/reject an active offer.
    It mockes the role.
    """
    user = user_company_profile.user
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE, modified_by=user)

    expected_actions = {analytics.code, deactivate.code, get_history.code}

    actions = get_valid_actions(
        user, joboffer, {ROLE_PUBLISHER}
    )

    assert actions == expected_actions
