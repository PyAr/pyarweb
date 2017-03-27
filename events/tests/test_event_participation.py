"""
Tests for the events.EventParticipation Model

"""
from django.test import TestCase, mock
from email_confirm_la.models import EmailConfirmation
from events.tests.factories import EventParticipationFactory, UserFactory


class IsVerifiedTests(TestCase):

    # Only registered users (can login) are set in the user field. 
    # Registered users are considered verified by default because we have email
    def test_user_is_not_none_then_return_true(self):
        participation = EventParticipationFactory(user = UserFactory())
        self.assertTrue(participation.is_verified)

    def test_anonymous_user_confirmed_his_email_then_return_true(self):
        participation = EventParticipationFactory()
        # not email_confirmations.exists means the user confirmed his email
        participation.email_confirmations.all().delete()
        assert participation.user is None  # Make sure no user is set
        self.assertTrue(participation.is_verified)

    def test_anonymous_user_with_pending_email_confirmation_return_false(self):
        participation = EventParticipationFactory()
        assert participation.user is None  # Make sure no user is set
        assert participation.email_confirmations.exists()
        # email_confirmations.exists means the user didn't confirm his email
        self.assertFalse(participation.is_verified)
