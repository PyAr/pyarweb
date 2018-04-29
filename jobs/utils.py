import unicodedata


def normalize_tags(tags):
    """
        Parse a list of tags and removed duplicated tags and non valid chars

    """
    results = set()
    for tag in tags:
        tag_stripped = tag.strip()
        value = unicodedata.normalize("NFKD", tag_stripped.lower())
        value = value.encode('ascii', 'ignore').decode('utf-8')
        results.add(value)
    return results
