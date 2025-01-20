from django.core import mail
from django.urls import reverse
from django.test import TestCase, Client

from events.tests.factories import UserFactory, EventFactory


class ReportEventTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username, password='secret')
        self.event = EventFactory()

    def test_report_event_sends_email(self):
        """
        Test that reporting an event sends an email to admin and redirects the user.
        """
        report_url = reverse('events:report', kwargs={'event_id': self.event.id})

        # Simulate reporting the event
        response = self.client.post(report_url)

        # ✅ Check redirection after reporting
        self.assertEqual(response.status_code, 302)

        # ✅ Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # ✅ Verify email details
        email = mail.outbox[0]
        self.assertEqual(email.subject, f'Reporte de evento: {self.event.name}')
        self.assertIn(self.event.name, email.body)
        self.assertIn(self.event.description, email.body)
        self.assertIn('admin@python.org.ar', email.to)

    def test_anonymous_user_cannot_report_event(self):
        """
        Ensure that unauthenticated users cannot report an event.
        """
        self.client.logout()
        report_url = reverse('events:report', kwargs={'event_id': self.event.id})
        response = self.client.post(report_url)

        # 🔒 User should be redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        # 📧 No email should be sent
        self.assertEqual(len(mail.outbox), 0)
