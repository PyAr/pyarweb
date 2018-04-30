import unicodedata


def normalize(tag):
    """Normalize a single tag: remove non valid chars, lower case all."""

    tag_stripped = tag.strip()
    value = unicodedata.normalize("NFKD", tag_stripped.lower())
    value = value.encode('ascii', 'ignore').decode('utf-8')
    return value


def normalize_tags(tags):
    """Parse a list of tags and removed duplicated tags and non valid chars."""
    return {normalize(tag) for tag in tags}
