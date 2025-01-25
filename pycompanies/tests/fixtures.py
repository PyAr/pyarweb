import pytest

from pycompanies.tests.factories import UserCompanyProfileFactory


@pytest.fixture(name='user_company_profile')
def create_user_company_profile():
    """
    Fixture with a dummy UserCompanyProfileFactory
    """
    return UserCompanyProfileFactory.create()
