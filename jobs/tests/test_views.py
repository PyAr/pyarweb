import bleach

from django.test import TestCase, Client
from django.urls import reverse

from jobs.models import Job
from jobs.tests.factories import JobFactory
from events.tests.factories import UserFactory
from pycompanies.tests.factories import CompanyFactory


class JobsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username, password='secret')

    def test_jobs_view_list(self):
        job = JobFactory(owner=self.user)
        company = CompanyFactory(owner=self.user, rank=3)
        sponsored_job = JobFactory(owner=self.user, company=company)
        sponsored_job2 = JobFactory(owner=self.user, company=company)

        response = self.client.get(reverse('jobs_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(job, response.context["job_list"])
        self.assertEqual(len(response.context["job_list"]), 1)
        self.assertIn(sponsored_job, response.context["sponsored_jobs"])
        self.assertIn(sponsored_job2, response.context["sponsored_jobs"])
        self.assertEqual(len(response.context["sponsored_jobs"]), 2)

    def test_jobs_view_list_with_tags(self):
        job = JobFactory(owner=self.user)
        job_2 = JobFactory(owner=self.user)

        job.tags.add('tag1')
        job_2.tags.add('tag2')

        response = self.client.get(reverse('jobs_list_all'), {'tag_tag1': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(job, response.context["job_list"])
        self.assertEqual(len(response.context["job_list"]), 1)

    def test_jobs_view_list_regular_and_sponsored(self):
        sponsored_company = CompanyFactory(name='Name', owner=self.user, rank=3)
        sponsored_job = JobFactory(owner=self.user, company=sponsored_company)
        sponsored_job_2 = JobFactory(owner=self.user, company=sponsored_company)

        company = CompanyFactory(name='Other name', owner=self.user, rank=0)
        job = JobFactory(owner=self.user, company=company)
        job_2 = JobFactory(owner=self.user, company=company)

        response = self.client.get(reverse('jobs_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(job, response.context["job_list"])
        self.assertIn(job_2, response.context["job_list"])
        self.assertEqual(len(response.context["job_list"]), 2)
        self.assertIn(sponsored_job, response.context["sponsored_jobs"])
        self.assertIn(sponsored_job_2, response.context["sponsored_jobs"])
        self.assertEqual(len(response.context["sponsored_jobs"]), 2)

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

    def test_jobs_view_create_avoiding_repeated_tags(self):
        response = self.client.get(reverse('jobs_add'))
        job = {
            'title': 'Python Dev',
            'location': 'Bahia Blanca',
            'email': 'info@undominio.com',
            'tags': 'python,remoto,DJANGO,django',
            'description': 'Buscamos desarrollador python freelance.'
        }
        response = self.client.post(reverse('jobs_add'), job)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Job.objects.filter(title='Python Dev').count(), 1)
        self.assertEqual(Job.objects.all()[0].tags.all().count(), 3)

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
