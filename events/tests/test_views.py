import bleach

from django.test import TestCase, Client
from django.utils.timezone import now, timedelta
from django.urls import reverse

from events.models import Event
from events.tests.factories import UserFactory, EventFactory, FutureEventFactory


class EventsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username, password='secret')

    def test_events_view_list(self):
        event = EventFactory()
        response = self.client.get(reverse('events:events_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(event, response.context["eventos_pasados"])

    def test_events_feed_view_list(self):
        event = FutureEventFactory(name="PyDay San Rafael")
        response = self.client.get(reverse('events:events_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, event.name)

    def test_events_view_create(self):
        response = self.client.get(reverse('events:add'))
        event = {
            'name': "PyDay San Rafael",
            'description': "Charlas y talleres",
            'place': 'UTN Regional, San Rafael',
            'address': 'Gral. Paz 1432',
            'url': 'pydaysanrafael.tk',
            'start_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 08:00:00'),
            'end_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 18:00:00'),
            'registration_enabled': 1,
            'has_sponsors': 1
        }
        response = self.client.post(reverse('events:add'), event)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.filter(name='PyDay San Rafael').count(), 1)

    def test_events_view_edit(self):
        event = EventFactory(owner=self.user)

        response = self.client.get(reverse('events:edit', args=(event.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], event)
        event_data = {
            'name': "PyDay Rio IV",
            'description': event.description,
            'place': event.place,
            'address': event.address,
            'url': "http://rioiv.python.org.ar",
            'start_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 08:00:00'),
            'end_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 18:00:00'),
            'registration_enabled': 1,
            'has_sponsors': 1
        }
        response = self.client.post(reverse('events:edit', args=(event.pk, )), event_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(name=event.name).exists())
        edit_event = Event.objects.get(pk=event.pk)
        self.assertEqual(edit_event.name, "PyDay Rio IV")
        self.assertEqual(edit_event.url, "http://rioiv.python.org.ar")

    def test_html_sanitizer_in_description_field(self):
        response = self.client.get(reverse('events:add'))
        event = {
            'name': "PyDay San Rafael",
            'description': 'an <script>evil()</script> example',
            'place': 'UTN Regional, San Rafael',
            'address': 'Gral. Paz 1432',
            'url': 'pydaysanrafael.tk',
            'start_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 08:00:00'),
            'end_at': (now() + timedelta(days=1)).strftime('%d/%m/%Y 18:00:00'),
            'registration_enabled': 1,
            'has_sponsors': 1
        }
        response = self.client.post(reverse('events:add'), event)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.filter(name='PyDay San Rafael').count(), 1)
        event = Event.objects.filter(name='PyDay San Rafael').get()
        self.assertEqual(event.description, bleach.clean('an <script>evil()</script> example'))

    def test_events_view_delete(self):
        event = EventFactory(owner=self.user)

        response = self.client.get(reverse('events:delete', args=(event.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], event)
        response = self.client.post(reverse('events:delete', args=(event.pk, )))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(name=event.name).exists())

    def test_events_view_slug(self):
        event = EventFactory()
        response_por_slug = self.client.get('/eventos/{}/'.format(event.slug))
        self.assertEqual(response_por_slug.context['event'].id, event.id)
