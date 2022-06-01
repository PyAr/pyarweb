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
from ..models import JobOffer, OfferState, Remoteness
from .utils import get_plain_messages


ADD_URL = 'joboffers:add'
EDIT_URL = 'joboffers:edit'


@pytest.mark.django_db
def test_joboffer_creation_as_publisher_with_all_fields_ok(publisher_client, user_company_profile):
    """
    Test creation of joboffer as publisher with data ok
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
    company = user_company_profile.company

    job_data = factory.build(dict, company=company, FACTORY_CLASS=JobOfferFactory)

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
        company=company,
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
    Test the validation of at least one contact info
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
    company = user_company_profile.company

    job_data = factory.build(dict, company=company, FACTORY_CLASS=JobOfferFactory)

    del job_data['contact_mail']
    del job_data['contact_phone']
    del job_data['contact_url']

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 200

    assert JobOffer.objects.count() == 0

    errors = response.context_data['form'].non_field_errors()

    assert errors == ['Debe ingresar al menos un dato de contacto.']


@pytest.mark.django_db
def test_joboffer_creation_in_office_without_location(publisher_client, user_company_profile):
    """
    Test the validation of an in office offer without location
    """
    target_url = reverse(ADD_URL)

    client = publisher_client
    company = user_company_profile.company

    job_data = factory.build(
        dict, company=company, remoteness=Remoteness.OFFICE, FACTORY_CLASS=JobOfferFactory
    )

    del job_data['location']

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 200

    assert JobOffer.objects.count() == 0

    errors = response.context_data['form'].non_field_errors()

    assert errors == ['Debe especificar un lugar para modalidad prescencial.']


@pytest.mark.django_db
def test_joboffer_edit_with_all_fields_empty(publisher_client, user_company_profile):
    """
    Test the validation of empty fields
    """
    client = publisher_client
    company = user_company_profile.company

    offer = JobOfferFactory.create(company=company)

    target_url = reverse(EDIT_URL, kwargs={'slug': offer.slug})

    assert JobOffer.objects.count() == 1

    response = client.post(target_url, {'company': company.id})

    assert response.status_code == 200

    found_errors = response.context_data['form'].errors

    MANDATORY_FIELD_ERROR = 'Este campo es obligatorio.'

    expected_mandatory_fields = [
        'title', 'experience', 'remoteness', 'hiring_type', 'salary', 'description'
    ]

    for field_name in expected_mandatory_fields:
        assert found_errors[field_name][0] == MANDATORY_FIELD_ERROR


@pytest.mark.django_db
def test_joboffer_edit_with_all_fields_ok(publisher_client, user_company_profile):
    """
    Test the validation of empty fields
    """
    client = publisher_client
    company = user_company_profile.company

    offer = JobOfferFactory.create(company=company)
    update_data = factory.build(dict, FACTORY_CLASS=JobOfferFactory)
    del update_data['company']

    assert JobOffer.objects.count() == 1

    target_url = reverse(EDIT_URL, kwargs={'slug': offer.slug})

    response = client.post(target_url, update_data)
    assert response.status_code == 302

    updated_offer = JobOffer.objects.first()

    assert update_data['title'] == updated_offer.title
    assert update_data['location'] == updated_offer.location
    assert update_data['contact_mail'] == updated_offer.contact_mail
    assert update_data['contact_phone'] == updated_offer.contact_phone
    assert updated_offer.modified_by == user_company_profile.user
