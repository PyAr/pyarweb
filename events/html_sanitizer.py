from bs4 import BeautifulSoup

from urllib.parse import urlparse

from django.conf import settings


def is_safe_url(url: str, attr: str) -> bool:
    """
    Check if the URL uses an allowed scheme for the given attribute.

    Args:
        url (str): The URL to validate.
        attr (str): The attribute name (e.g., 'href', 'src').

    Returns:
        bool: True if the URL is safe, False otherwise.
    """
    parsed = urlparse(url)
    if parsed.scheme == "":
        # URLs without a scheme are considered safe (relative URLs)
        return True
    allowed_schemes = settings.ALLOWED_URL_SCHEMES.get(attr, [])
    return parsed.scheme.lower() in allowed_schemes


def remove_disallowed_tags(soup: BeautifulSoup, allowed_tags: list[str]) -> None:
    """
    Remove any tags that are not present in allowed_tags.
    """
    for tag in soup.find_all():
        if tag.name not in allowed_tags:
            tag.decompose()


def filter_style_attribute(style_value: str, allowed_styles: list[str]) -> str:
    """
    Take a CSS style string (e.g. "color: red; font-weight: bold;") and
    return a sanitized version containing only the allowed properties.
    Returns an empty string if no allowed properties remain.
    """
    filtered_style_pairs = []
    for prop_pair in style_value.split(";"):
        prop_pair = prop_pair.strip()
        if not prop_pair:
            continue
        if ":" not in prop_pair:
            continue

        prop_name, prop_value = prop_pair.split(":", 1)
        prop_name = prop_name.strip().lower()
        prop_value = prop_value.strip()

        if prop_name in allowed_styles:
            filtered_style_pairs.append(f"{prop_name}: {prop_value}")

    return "; ".join(filtered_style_pairs)


def filter_attributes(
    soup: BeautifulSoup, allowed_attrs: list[str], allowed_styles: list[str]
) -> None:
    """
    For each remaining (allowed) tag in the soup, remove any attribute
    not in allowed_attrs. If the attribute is 'style', filter out
    disallowed CSS properties.
    """
    for tag in soup.find_all():
        for attr_name in list(tag.attrs):
            # If attribute name is not allowed, remove it
            if attr_name not in allowed_attrs:
                del tag.attrs[attr_name]
            # If it's a style attribute, apply style filtering
            elif attr_name == "style":
                style_value = tag.attrs["style"]
                safe_style = filter_style_attribute(style_value, allowed_styles)
                if safe_style:
                    tag.attrs["style"] = safe_style
                else:
                    # If no allowed properties remain, remove the style attribute
                    del tag.attrs["style"]
            elif attr_name in settings.ALLOWED_URL_SCHEMES:
                # Validate URL schemes for attributes like 'href' and 'src'
                url = tag.attrs[attr_name]
                if not is_safe_url(url, attr_name):
                    del tag.attrs[attr_name]


def sanitize_html(
    html: str,
    allowed_tags: list[str],
    allowed_attrs: list[str],
    allowed_styles: list[str],
) -> str:
    """
    Main function that orchestrates the sanitization process.
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove disallowed tags entirely
    remove_disallowed_tags(soup, allowed_tags)

    # 2. Filter attributes (including style) on the remaining tags
    filter_attributes(soup, allowed_attrs, allowed_styles)

    # Return the resulting sanitized HTML
    return str(soup)
