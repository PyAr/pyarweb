from django.test import TestCase

from jobs.utils import normalize_tags


class UtilTest(TestCase):
    def test_normalize_tags_with_repeated(self):
        repeated_tags = ['Django', 'DJANGO', 'djAngo']
        tags = normalize_tags(repeated_tags)
        self.assertEqual(len(tags), 1)

    def test_normalize_tags_with_repeated_and_spaces(self):
        repeated_tags = ['Django', ' DJANGO', 'djAngo ']
        tags = normalize_tags(repeated_tags)
        self.assertEqual(len(tags), 1)

    def test_normalize_tags_with_non_ascii(self):
        repeated_tags = ['DñàÈ', ]
        tags = list(normalize_tags(repeated_tags))
        self.assertEqual(len(tags), 1)
        self.assertTrue(tags[0].islower())
        self.assertTrue('dnae' == tags[0])
