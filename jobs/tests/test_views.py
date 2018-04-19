import bleach

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from jobs.models import Job
from jobs.tests.factories import JobFactory
from events.tests.factories import UserFactory


class JobsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username, password='secret')

    def test_jobs_view_list(self):
        job = JobFactory(owner=self.user)
        response = self.client.get(reverse('jobs_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(job, response.context["job_list"])

    def test_jobs_view_create(self):
        response = self.client.get(reverse('jobs_add'))
        job = {
            'title': 'Python Dev',
            'location': 'Bahia Blanca',
            'email': 'info@undominio.com',
            'tags': 'python,remoto,django',
            'description': 'Buscamos desarrollador python freelance.'
        }
        response = self.client.post(reverse('jobs_add'), job)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Job.objects.filter(title='Python Dev').count(), 1)

    def test_jobs_view_edit(self):
        job = JobFactory(
            owner=self.user, title='Python Dev',
            description='Buscamos desarrollador python freelance',
            location='Bahia Blanca', email='info@undominio')

        response = self.client.get(reverse('jobs_update', args=(job.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], job)
        job_data = {
            'title': 'Python Dev 2',
            'location': 'Azul',
            'email': 'info@undominio.com',
            'tags': 'python,remoto,django',
            'description': 'Buscamos desarrollador python freelance.'
        }
        response = self.client.post(reverse('jobs_update', args=(job.pk, )), job_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Job.objects.filter(title='Python Dev').exists())
        edit_job = Job.objects.get(pk=job.pk)
        self.assertEqual(edit_job.location, "Azul")
        self.assertEqual(edit_job.title, "Python Dev 2")

    def test_jobs_view_idelete(self):
        job = JobFactory(
            owner=self.user, title='Python/Django Dev',
            description='Buscamos desarrollador python freelance',
            location='General Pico', email='info@fdq.com')

        response = self.client.get(reverse('jobs_delete', args=(job.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], job)

        response = self.client.post(reverse('jobs_delete', args=(job.pk, )))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Job.objects.filter(title='Python/Django Dev').exists())

    def test_html_sanitizer_in_description_field(self):
        response = self.client.get(reverse('jobs_add'))
        job = {
            'title': 'Python Dev',
            'location': 'Cruz del Eje',
            'email': 'info@undominio.com',
            'tags': 'python,remoto,django',
            'description': 'an <script>evil()</script> example'
        }
        response = self.client.post(reverse('jobs_add'), job)
        self.assertEqual(response.status_code, 302)
        job = Job.objects.get(title='Python Dev')
        self.assertEqual(job.description, bleach.clean('an <script>evil()</script> example'))
