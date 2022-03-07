import hashlib

from ..utils import normalize_tags


def test_normalize_tags_with_repeated():
    """
    Test that uppercase/lowercase combinations be unified
    """
    repeated_tags = ['Django', 'DJANGO', 'djAngo']
    tags = normalize_tags(repeated_tags)
    assert len(tags) == 1


def test_normalize_tags_sorrunding_with_symbols_and_spaces():
    """
    Test that unwanted leading and trailing symbols be unified as one tag
    """
    repeated_tags = ['  Django', '@django ', '//DJANGO', '#django#']
    tags = normalize_tags(repeated_tags)
    assert len(tags) == 1


def test_normalize_tags_with_non_ascii():
    """
    Test normalizing non assci chars
    """
    repeated_tags = ['DñàÈ', ]
    tags = list(normalize_tags(repeated_tags))
    assert len(tags) == 1
    assert tags[0].islower()
    assert 'dnae' == tags[0]


def test_hash_secret():
    """
    Test hash_secret method. It should receive a string and return a sha256 hexdigest.
    """
    dummy_secret = 'kl^324523²#¹¹}##'
    expected_result = '787de9491332e7f258aadf90983101d0dfa63973a9ac935deb37cdea76bac1f3'
    result = hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest()
    assert result == expected_result
