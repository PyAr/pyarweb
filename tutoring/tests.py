import sys
from django.test import TestCase
from tutoring import models as m
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


User = get_user_model()


class MentorDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.user2 = User.objects.create_user(
            username='jacob2', email='jacob@…', password='top_secret')
        super(MentorDetailViewTests, self).setUp()
        self.mentor = m.Mentor.objects.create(description='New Post', owner=self.user)

    def test_mentor_detail_success(self):
        response = self.client.get(reverse('display_mentor', args=(self.mentor.owner.username,)))
        self.assertEqual(response.status_code, 200)

    def test_mentor_update_success(self):
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('update_mentor', args=(self.mentor.owner.username,)))
        self.assertEqual(response.status_code, 200)

    def test_mentor_update_no_permission(self):
        self.client.login(username='jacob2', password='top_secret')
        response = self.client.get(reverse('update_mentor', args=(self.mentor.owner.username,)))
        self.assertEqual(response.status_code, 404)

    def test_mentor_detail_404(self):
        response = self.client.get(reverse('display_mentor', args=(sys.maxsize,)))
        self.assertEqual(response.status_code, 404)


class ApprenticeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.user2 = User.objects.create_user(
            username='jacob2', email='jacob@…', password='top_secret')
        super(ApprenticeDetailViewTests, self).setUp()
        self.apprentice = m.Apprentice.objects.create(description='New Post', owner=self.user)

    def test_apprentice_detail_success(self):
        response = self.client.get(
            reverse('display_apprentice', args=(self.apprentice.owner.username,)))
        self.assertEqual(response.status_code, 200)

    def test_apprentice_create_success(self):
        self.client.login(username='jacob2', password='top_secret')
        response = self.client.get(reverse('new_apprentice',))
        self.assertEqual(response.status_code, 200)

    def test_apprentice_update_success(self):
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(
            reverse('update_apprentice', args=(self.apprentice.owner.username,)))
        self.assertEqual(response.status_code, 200)

    def test_apprentice_update_no_permission(self):
        self.client.login(username='jacob2', password='top_secret')
        response = self.client.get(
            reverse('update_apprentice', args=(self.apprentice.owner.username,)))
        self.assertEqual(response.status_code, 404)

    def test_apprentice_detail_404(self):
        response = self.client.get(reverse('display_apprentice', args=(sys.maxsize,)))
        self.assertEqual(response.status_code, 404)


class MentorshipTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.user2 = User.objects.create_user(
            username='jacob2', email='jacob@…', password='top_secret')
        super(MentorshipTests, self).setUp()
        self.apprentice = m.Apprentice.objects.create(description='New Post', owner=self.user)
        self.mentor = m.Mentor.objects.create(description='New Post', owner=self.user2)
        self.mentorship = m.Mentorship.objects.create(
            owner=self.mentor, apprentice=self.apprentice)

    def test_mentorship_detail_success(self):
        response = self.client.get(reverse('display_mentorship', args=(self.mentorship.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_mentorship_update_success(self):
        self.client.login(username='jacob2', password='top_secret')
        response = self.client.get(reverse('update_mentorship', args=(self.mentorship.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_mentorship_update_no_permission(self):
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('update_apprentice', args=(self.mentorship.pk,)))
        self.assertEqual(response.status_code, 404)

    def test_mentorship_detail_404(self):
        response = self.client.get(reverse('display_mentorship', args=(sys.maxsize,)))
        self.assertEqual(response.status_code, 404)
