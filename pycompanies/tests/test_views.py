import pytest

from django.contrib.messages import get_messages as contrib_get_messages
from django.urls import reverse

from pycompanies.views import get_user_display_name
from pycompanies.tests.factories import CompanyFactory, UserCompanyProfileFactory, UserFactory
from joboffers.tests.fixtures import create_admin_client, create_publisher_client  # noqa
from pyarweb.tests.fixtures import create_client, create_logged_client, create_user  # noqa
from pycompanies.tests.fixtures import create_user_company_profile  # noqa
from joboffers.tests.utils import create_analytics_sample_data


ERROR_USER_DOES_NOT_EXIST = 'Le usuarie que ingresaste no existe.'
USER_ASSOCIATED_CORRECTLY = 'Le usuarie fue asociade correctamente.'

ADMIN_URL = reverse('companies:admin')


def get_plain_messages(request):
    """
    Get a plain text message from a given request/response object. Useful for testing messages
    """
    messages = contrib_get_messages(request.wsgi_request)
    return [m.message for m in messages]


@pytest.mark.django_db
def test_associate_nonexistent_user(logged_client):
    """
    Should fail to associate an nonexistent user
    """
    company = CompanyFactory.create()
    ASSOCIATE_URL = reverse('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': 'pepito'})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert ERROR_USER_DOES_NOT_EXIST == message


@pytest.mark.django_db
def test_associate_user_in_company(logged_client, user):
    """
    Should redirect and send a success message after associating the user
    """
    company = CompanyFactory.create()

    ASSOCIATE_URL = reverse('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert USER_ASSOCIATED_CORRECTLY == message


@pytest.mark.django_db
def test_associate_user_already_in_company(logged_client, user):
    """
    Should fail, redirect and send a warning message if the user is already in the company
    """
    company = CompanyFactory.create()
    user_company = UserCompanyProfileFactory.create(company=company, user=user)

    ERROR_USER_ALREADY_IN_COMPANY = ('Le usuarie que desea vincular ya '
                                     f'pertenece a {user_company.company}')

    ASSOCIATE_URL = reverse('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert ERROR_USER_ALREADY_IN_COMPANY == message


@pytest.mark.django_db
def test_associate_user_in_other_company(logged_client, user):
    """
    Should fail, redirect and send a warning message if the user is associated in other company
    """
    company = CompanyFactory.create(name='company_1')
    other_company = CompanyFactory.create(name='company_2')
    UserCompanyProfileFactory.create(company=other_company, user=user)

    ERROR_USER_IN_OTHER_COMPANY = f'Le usuarie que ingresó esta vinculade a {other_company}.'

    ASSOCIATE_URL = reverse('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert message == ERROR_USER_IN_OTHER_COMPANY


@pytest.mark.django_db
def test_company_admin_with_no_logged_user_should_redirect(client):
    """
    Should redirect if the user is not logged
    """
    response = client.get(ADMIN_URL)

    assert 302 == response.status_code


@pytest.mark.django_db
def test_company_admin_with_no_company_logged_user_should_redirect(logged_client):
    """
    Should redirect if the user is logged but not associated to a company
    """
    response = logged_client.get(ADMIN_URL)

    assert 302 == response.status_code


@pytest.mark.django_db
def test_company_admin_with_company_logged_user_should_not_redirect(logged_client, user):
    """
    Should not redirect if the user is logged and associated to a company
    """
    company = CompanyFactory.create(name='company')
    UserCompanyProfileFactory.create(company=company, user=user)

    response = logged_client.get(ADMIN_URL)

    assert 200 == response.status_code


@pytest.mark.django_db
def test_company_admin_should_have_two_companies_in_context(logged_client):
    """
    Context should have two companies if the search matches with both company names
    """
    company_1 = CompanyFactory.create(name='company_1')
    company_2 = CompanyFactory.create(name='company_2')

    FIRST_NAME_1 = 'firstname1'
    LAST_NAME_1 = 'lastname1'

    profile_1 = UserCompanyProfileFactory.create(
      company=company_1, user__first_name=FIRST_NAME_1, user__last_name=LAST_NAME_1
    )
    profile_2 = UserCompanyProfileFactory.create(company=company_2)
    profile_3 = UserCompanyProfileFactory.create(company=company_2)

    COMPANY_LIST_URL = reverse('companies:association_list')

    response = logged_client.get(COMPANY_LIST_URL, data={'empresa': 'company'})

    expected_name_1 = f"{profile_1.user.first_name} {profile_1.user.last_name}"
    expected_name_2 = profile_2.user.username
    expected_name_3 = profile_3.user.username

    companies_and_owners = list(response.context_data['companies_and_owners'])

    assert 200 == response.status_code
    assert 2 == len(companies_and_owners)
    assert company_1 == companies_and_owners[0][0]
    assert company_2 == companies_and_owners[1][0]
    assert [expected_name_1] == companies_and_owners[0][1]
    assert [expected_name_2, expected_name_3] == companies_and_owners[1][1]


@pytest.mark.django_db
def test_company_admin_should_have_no_matching_company_in_context(logged_client):
    """
    Context should have an empty companies if the search doesn't match any company name
    """
    CompanyFactory.create(name='company_1')
    COMPANY_LIST_URL = reverse('companies:association_list')

    response = logged_client.get(COMPANY_LIST_URL, data={'empresa': 'not_matching_search'})

    assert 200 == response.status_code
    assert 0 == len(response.context['companies'])


@pytest.mark.django_db
def test_company_disassociate_last_user_from_company(logged_client, user):
    """
    Message in context should notice if is the last user associated to the company
    """
    DISASSOCIATE_MESSAGE = ('Esta es la última persona vinculada a esta empresa '
                            '¿Estás seguro que deseas desvincularla?')

    company_1 = CompanyFactory.create(name='company_1')
    user_company_profile = UserCompanyProfileFactory.create(company=company_1, user=user)

    COMPANY_DISSASOCIATE_URL = reverse('companies:disassociate',
                                       kwargs={'pk': user_company_profile.id})

    response = logged_client.get(COMPANY_DISSASOCIATE_URL, data={'empresa': company_1})

    assert 200 == response.status_code
    assert DISASSOCIATE_MESSAGE == response.context_data['message']


@pytest.mark.django_db
def test_company_disassociate_one_user_from_company(logged_client, user):
    """
    Message in context should show the user and company if it's not the last user associated
    """
    user_2 = UserFactory.create()
    company = CompanyFactory.create(name='company_1')
    user_company_profile = UserCompanyProfileFactory.create(company=company, user=user)
    UserCompanyProfileFactory.create(company=company, user=user_2)

    DISASSOCIATE_MESSAGE = f'¿Estás seguro que deseas desvincular a {user} de {company.name}?'

    COMPANY_DISSASOCIATE_URL = reverse('companies:disassociate',
                                       kwargs={'pk': user_company_profile.id})

    response = logged_client.get(COMPANY_DISSASOCIATE_URL, data={'empresa': company})

    assert 200 == response.status_code
    assert DISASSOCIATE_MESSAGE == response.context_data['message']


@pytest.mark.django_db
def test_company_detail_doesnt_show_analytics_button_for_normal_user(logged_client):
    """
    Test that the company page doesn't show the analytics button for authenticated users that
    doesn't belong to the current company
    """
    client = logged_client
    company = CompanyFactory.create(name='company_1')

    target_url = reverse('companies:detail', kwargs={'pk': company.id})

    response = client.get(target_url)

    assert response.context_data['can_view_analytics'] is False


@pytest.mark.django_db
def test_company_detail_show_analytics_button_for_admin_user(admin_client):
    """
    Test that the company page show the analytics button for an admin user
    """
    client = admin_client
    company = CompanyFactory.create(name='company_1')

    target_url = reverse('companies:detail', kwargs={'pk': company.id})

    response = client.get(target_url)

    assert response.context_data['can_view_analytics'] is True


@pytest.mark.django_db
def test_company_detail_show_analytics_button_for_publisher_user(
    publisher_client, user_company_profile
):
    """
    Test that the company page show the analytics button for a publisher that belongs to the
    company
    """
    client = publisher_client
    company = user_company_profile.company

    target_url = reverse('companies:detail', kwargs={'pk': company.id})

    response = client.get(target_url)

    assert response.context_data['can_view_analytics'] is True


@pytest.mark.django_db
def test_company_analytics_access_denied_for_external_user(logged_client):
    """
    Test that the rendering of JobOfferAccessLog data for a company doesn't fail.
    """
    client = logged_client
    company = CompanyFactory.create(name='company_1')

    target_url = reverse('companies:analytics', kwargs={'pk': company.id})

    response = client.get(target_url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_render_company_analytics_ok(publisher_client, user_company_profile):
    """
    Test that the rendering of JobOfferAccessLog data for a company doesn't fail.
    """
    client = publisher_client
    company = user_company_profile.company
    user = user_company_profile.user

    target_url = reverse('companies:analytics', kwargs={'pk': company.id})

    create_analytics_sample_data(
      test_username=user.username,
      test_offer_title='Testing Offer 1',
      test_company=company,
      max_views_amount=10
    )

    create_analytics_sample_data(
      test_username=user.username,
      test_offer_title='Testing Offer 2',
      test_company=company,
      max_views_amount=10
    )

    response = client.get(target_url)
    assert response.status_code == 200


def test_get_user_display_name_without_first_name_and_last_name():
    """
    Test return for an user without first_name and last_name
    """
    user = UserFactory.build(first_name='', last_name='')
    actual_name = get_user_display_name(user)

    assert actual_name == user.username


def test_get_user_display_name_with_first_name():
    """
    Test return for an user with only first_name
    """
    user = UserFactory.build(first_name='firstname', last_name='')
    actual_name = get_user_display_name(user)

    assert actual_name == f"{user.first_name} "


def test_get_user_display_name_with_last_name():
    """
    Test return for an user with only last_name
    """
    user = UserFactory.build(first_name='', last_name='lastname')
    actual_name = get_user_display_name(user)

    assert actual_name == f" {user.last_name}"


def test_get_user_display_name_with_first_name_and_last_name():
    """
    Test return for an user with first_name and last_name
    """
    user = UserFactory.build(first_name='firstname', last_name='lastname')
    actual_name = get_user_display_name(user)

    assert actual_name == f"{user.first_name} {user.last_name}"
