"""
Tests for the community.views.HomePageView class

"""
from django.test import TestCase

from community.views import HomePageView, RECENT_ITEMS_LEN
from events.tests.factories import EventFactory
from jobs.tests.factories import JobFactory
from news.tests.factories import NewsArticleFactory


class GetContextDataRecentKeyTests(TestCase):
    def setUp(self):
        # shortcut
        self.get_context_data = HomePageView().get_context_data

    def test_a_recent_key_is_added_to_the_return_value(self):
        self.assertIn('recent', self.get_context_data())

    def test_events_are_included_in_recent(self):
        event = EventFactory()
        self.assertEqual([event], self.get_context_data()['recent'])

    def test_included_events_have_correct_fields(self):
        # Correct fields include 'category', 'created', 'title' and 'description'
        EventFactory()
        event = self.get_context_data()['recent'][0]
        self.assertEqual(event.category, 'Eventos')
        self.assertEqual(event.title, event.name)
        self.assertEqual(event.created, event.start_at)
        # Events already have a description field

    def test_jobs_are_included_in_recent(self):
        job = JobFactory()
        self.assertEqual([job], self.get_context_data()['recent'])

    def test_included_jobs_have_correct_fields(self):
        JobFactory()
        job = self.get_context_data()['recent'][0]
        self.assertEqual(job.category, 'Trabajos')
        # jobs already have 'created', 'title' and 'description' fields

    def test_news_are_included_in_recent(self):
        article = NewsArticleFactory()
        self.assertEqual([article], self.get_context_data()['recent'])

    def test_included_news_have_correct_fields(self):
        # Correct fields include 'category', 'created', 'title' and 'description'
        NewsArticleFactory()
        article = self.get_context_data()['recent'][0]
        self.assertEqual(article.category, 'Noticias')
        self.assertEqual(article.description, article.body)
        # NewsArticle already have a created and title fields

    # Independent of the Model type, all list items are sorted by their 'created' field
    def test_items_are_sorted_by_the_created_field(self):
        job = JobFactory(set_created='1985-10-26 09:00Z')  # Middle-age ;-)
        event = EventFactory(start_at='1955-11-12 06:38Z')  # Oldest
        article = NewsArticleFactory(set_created='2015-10-21 09:00Z')  # Most recent
        # Assert the models are in chronological order
        self.assertListEqual([article, job, event], self.get_context_data()['recent'])

    def test_recent_is_a_list_with_at_most_10_items(self):
        # Create more than RECENT_ITEMS_LEN models and assert that only 10 are kept as recent
        for i in range(RECENT_ITEMS_LEN):
            JobFactory()
            EventFactory()
            NewsArticleFactory()
        # The loop above creates RECENT_ITEMS_LEN * 3 items
        self.assertEqual(len(self.get_context_data()['recent']), RECENT_ITEMS_LEN)
