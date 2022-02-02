from datetime import datetime

import factory
import pytest
from django.contrib.messages import get_messages as contrib_get_messages
from django.urls import reverse

from pyarweb.tests.fixtures import create_client, create_logged_client, create_user # noqa
from pycompanies.tests.factories import UserCompanyProfileFactory
from pycompanies.tests.fixtures import create_user_company_profile # noqa
from ..models import JobOffer, OfferState
from ..views import STATE_LABEL_CLASSES
from .factories import JobOfferCommentFactory, JobOfferFactory
from .fixtures import create_publisher_client # noqa


ADD_URL = 'joboffers:add'
ADMIN_URL = 'joboffers:admin'
VIEW_URL = 'joboffers:view'
APPROVE_URL = 'joboffers:approve'
REJECT_URL = 'joboffers:reject'
REQUEST_MODERATION_URL = 'joboffers:request_moderation'

JOBOFFER_TITLE1 = 'title1'
JOBOFFER_TITLE2 = 'title2'
JOBOFFER_TITLE3 = 'title3'

JOBOFFER_TAG_1 = 'tag1'
JOBOFFER_TAG_2 = 'tag2'


def get_plain_messages(request):
    """
    Gets a plain text message from a given request/response object. Useful for testing messages
    """
    messages = contrib_get_messages(request.wsgi_request)
    return [m.message for m in messages]


@pytest.mark.django_db
def test_joboffer_creation_redirects_unlogged(client):
    target_url = reverse(ADD_URL)
    response = client.get(target_url)

    assert 302 == response.status_code
    assert f'/accounts/login/?next={target_url}' == response.url


@pytest.mark.django_db
def test_joboffer_create_form_render_should_redirect_for_an_user_without_company(
        logged_client
):
    """
    Test that the get request to the joboffer's create view redirects for an user without company
    """

    client = logged_client
    target_url = reverse(ADD_URL)

    response = client.get(target_url)
    message = ("No estas relacionade a ninguna empresa. Asociate a una para poder "
               "crear una oferta de trabajo.")

    assert message == get_plain_messages(response)[0]
    assert response.status_code == 302


@pytest.mark.django_db
def test_joboffer_create_form_render_should_not_redirect_for_an_user_with_company(
        logged_client, user
):
    """
    Test that the get request to the joboffer's create view doesn't redirect for
    an user with company
    """

    client = logged_client
    target_url = reverse(ADD_URL)

    UserCompanyProfileFactory.create(user=user)

    response = client.get(target_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_creation_should_fail_for_an_user_from_a_different_company(
        logged_client, user_company_profile
):
    """
    Test that the post request to the joboffer's create view fails for not allowed user
    """
    client = logged_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 403
    assert JobOffer.objects.count() == 0


@pytest.mark.django_db
def test_joboffer_creation_as_admin_should_fail(admin_client, user_company_profile):
    """
    Test joboffer creation is not allowed as admin user
    """
    client = admin_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    del job_data['company']

    assert 0 == JobOffer.objects.count()

    response = client.post(target_url, job_data)

    assert JobOffer.objects.count() == 0
    # Asserts redirection to the joboffer status page
    assert response.status_code == 403


@pytest.mark.django_db
def test_joboffer_request_moderation_ok(publisher_client, user_company_profile):
    """
    Test request for moderation for a publisher user
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company)

    target_url = reverse(REQUEST_MODERATION_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.DEACTIVATED == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta enviada a moderación")

    joboffer = JobOffer.objects.first()
    assert OfferState.MODERATION == joboffer.state


@pytest.fixture(name="joboffers_list")
def create_joboffers_list(user_company_profile):
    company = user_company_profile.company

    return [
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE1,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 20)
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE2,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 21)
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE3,
            tags=[JOBOFFER_TAG_2],
            created_at=datetime(2021, 12, 22)
        )
    ]


@pytest.mark.django_db
def test_joboffer_admin_works_with_random_query_search(logged_client, joboffers_list):
    """
    Test that an empty queryset is returned for random search
    """
    client = logged_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': 'unexistant thing Ç '})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    assert list(actual_joboffers) == []


@pytest.mark.django_db
def test_joboffer_admin_works_with_empty_query_search(logged_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = logged_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': ''})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_admin_works_without_query(logged_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = logged_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url)

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_approve_without_permission(publisher_client, user_company_profile):
    """
    Test approval of a joboffer with a publisher should fail and keep the same state in the offer
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company, state=OfferState.MODERATION)

    target_url = reverse(APPROVE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 403 == response.status_code
    joboffer = JobOffer.objects.first()
    assert joboffer.state == OfferState.MODERATION


@pytest.mark.django_db
def test_joboffer_approve_ok(admin_client):
    """
    Test approval of a joboffer with an admin user
    """
    client = admin_client
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)

    target_url = reverse(APPROVE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta aceptada y activada.")

    joboffer = JobOffer.objects.first()
    assert OfferState.ACTIVE == joboffer.state


@pytest.mark.django_db
def test_joboffer_reject_ok(admin_client):
    """
    Test rejection of the joboffer by the admin user
    """
    client = admin_client
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)

    target_url = reverse(REJECT_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state

    # TODO: Test for deactivated state
    # end preconditions check

    comment_data = factory.build(dict, joboffer=joboffer.id, FACTORY_CLASS=JobOfferCommentFactory)

    response = client.post(target_url, data=comment_data)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta rechazada.")

    joboffer = JobOffer.objects.first()
    assert OfferState.DEACTIVATED == joboffer.state


@pytest.mark.django_db
def test_joboffer_form_with_initial_user_company(user, publisher_client, user_company_profile):
    """
    Assert that the form inits with the associated user company
    """
    client = publisher_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company
    factory.build(dict, user=user.id, company=company.id, FACTORY_CLASS=JobOfferFactory)

    response = client.get(target_url)

    assert company == response.context['form'].initial['company']


@pytest.mark.django_db
def test_joboffer_view_as_anonymous(client):
    """
    Test that the joboffer detail view renders without error as anonymous user
    """
    joboffer = JobOfferFactory.create()

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 200
    assert response.context_data['action_buttons'] == []


@pytest.mark.django_db
def test_joboffer_create_view_as_publisher(publisher_client):
    """
    Test that the joboffer detail view renders without error as a publisher
    """
    client = publisher_client

    target_url = reverse(ADD_URL)

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_admin_filters_by_company_name(logged_client, joboffers_list):
    """
    Test that searching by title2 retrieves only title2 joboffer
    """
    client = logged_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': JOBOFFER_TITLE2})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2]


@pytest.mark.django_db
def test_joboffer_admin_filters_by_exactly_by_tagname(logged_client, joboffers_list):
    """
    Test that searching by tag retrieves only the offers that match exactly with the tag name
    """
    client = logged_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': 'tag1'})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2, JOBOFFER_TITLE1]


@pytest.mark.django_db
def test_joboffer_create_view_as_publusher(publisher_client):
    """
    Test that the joboffer create view renders without error as anonymous user
    """
    client = publisher_client

    target_url = reverse(ADD_URL)

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_active_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with active label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    label_class = STATE_LABEL_CLASSES[OfferState.ACTIVE]

    assert response.context_data['state_label_class'] == label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_deactivated_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with deactivated label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.DEACTIVATED]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_expired_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with expired label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.EXPIRED)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.EXPIRED]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_moderation_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with moderation label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.MODERATION]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_new_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with new label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.NEW)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.NEW]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_rejected_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with rejected label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.REJECTED)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.REJECTED]

    assert response.context_data['state_label_class'] == state_label_class
