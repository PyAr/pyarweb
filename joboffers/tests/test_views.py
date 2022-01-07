import factory
import pytest
from ..models import JobOffer, OfferState
from .factories import JobOfferCommentFactory, JobOfferFactory
# Fixtures
from .fixtures import ( # noqa
    create_publisher_client
)
from pyarweb.tests.fixtures import create_client, create_logged_client, create_user # noqa
from pycompanies.tests.fixtures import create_user_company_profile # noqa
#
from django.contrib.messages import get_messages as contrib_get_messages
from django.urls import reverse


ADD_URL = 'joboffers:add'
ADMIN_URL = 'joboffers:admin'
VIEW_URL = 'joboffers:view'
APPROVE_URL = 'joboffers:approve'
REJECT_URL = 'joboffers:reject'
REQUEST_MODERATION_URL = 'joboffers:request_moderation'


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
def test_joboffer_create_form_render_should_fail_for_an_user_from_a_different_company(
        logged_client
):
    """
    Test that the get request to the joboffer's create view fails for not allowed user
    """

    client = logged_client
    target_url = reverse(ADD_URL)

    assert JobOffer.objects.count() == 0

    response = client.get(target_url)

    assert response.status_code == 403


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
def test_joboffer_creation_as_publisher_with_all_fields_ok(publisher_client, user_company_profile):
    """
    Test creation of joboffer as publisher with data ok
    """
    client = publisher_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert JobOffer.objects.count() == 1

    joboffer = JobOffer.objects.first()

    # Asserts redirection to the joboffer status page
    assert response.status_code == 302
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    # Deactivated should be the first state
    assert OfferState.DEACTIVATED == joboffer.state

    obtained_messages = get_plain_messages(response)
    assert obtained_messages[0].startswith('Oferta creada correctamente.')


@pytest.mark.django_db
def test_joboffer_creation_as_admin_should_fail(admin_client, user_company_profile):
    """
    Test joboffer creation is not allowed as admin user
    """
    client = admin_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

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
def test_joboffer_create_view_as_publusher(publisher_client):
    """
    Test that the joboffer detail view renders without error as anonymous user
    """
    client = publisher_client

    target_url = reverse(ADD_URL)

    response = client.get(target_url)

    assert response.status_code == 200
