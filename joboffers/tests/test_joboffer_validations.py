import factory
import pytest

from django.urls import reverse

# Fixtures
from .fixtures import ( # noqa
    create_publisher_client
)
from pyarweb.tests.fixtures import create_client, create_logged_client, create_user # noqa
from pycompanies.tests.fixtures import create_user_company_profile # noqa
#

from .factories import JobOfferFactory
from ..models import JobOffer, OfferState
from .test_views import get_plain_messages


ADD_URL = 'joboffers:add'


@pytest.mark.django_db
def test_joboffer_creation_as_publisher_with_all_fields_ok(publisher_client, user_company_profile):
    """
    Test creation of joboffer as publisher with data ok
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
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
def test_joboffer_creation_invalid_email(publisher_client, user_company_profile):
    """
    Test that the email validation is in place
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
    company = user_company_profile.company

    job_data = factory.build(
        dict,
        company=company.id,
        contact_mail="invalid_email",
        FACTORY_CLASS=JobOfferFactory
    )

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 200

    assert JobOffer.objects.count() == 0

    assert 'contact_mail' in response.context_data['form'].errors


@pytest.mark.django_db
def test_joboffer_creation_without_contact_info(publisher_client, user_company_profile):
    """
    Test that the email validation is in place
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    del job_data['location']
    del job_data['contact_mail']
    del job_data['contact_phone']
    del job_data['contact_url']

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 200

    assert JobOffer.objects.count() == 0

    errors = response.context_data['form'].non_field_errors()

    assert errors == ['Debe ingresar al menos un dato de contacto.']
