"""
Tests for the events.EventParticipation Model

"""
from django.test import TestCase
from events.tests.factories import EventParticipationFactory, UserFactory


class IsVerifiedTests(TestCase):

    # Only registered users (can login) are set in the user field.
    # Registered users are considered verified by default because we have email
    def test_user_is_not_none_then_return_true(self):
        participation = EventParticipationFactory(user=UserFactory())
        self.assertTrue(participation.is_verified)
