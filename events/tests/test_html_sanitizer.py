from django.test import TestCase, override_settings
from events.html_sanitizer import sanitize_html
from django.conf import settings


class SanitizeHTMLTests(TestCase):
    def setUp(self):
        # Define allowed tags, attributes, and styles from settings
        self.allowed_tags = settings.ALLOWED_HTML_TAGS_INPUT
        self.allowed_attrs = settings.ALLOWED_HTML_ATTRIBUTES_INPUT
        self.allowed_styles = settings.ALLOWED_HTML_STYLES_INPUT

    def test_allowed_tags_preserved(self):
        """Ensure that allowed tags are preserved in the output."""
        input_html = "<p>This is a <strong>test</strong> paragraph.</p>"
        expected_output = "<p>This is a <strong>test</strong> paragraph.</p>"
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_disallowed_tags_removed(self):
        """Ensure that disallowed tags are removed from the output."""
        input_html = "<p>This is a <script>alert('XSS');</script> test.</p>"
        expected_output = "<p>This is a  test.</p>"
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_allowed_attributes_preserved(self):
        """Ensure that allowed attributes are preserved."""
        input_html = '<a href="https://example.com" title="Example">Link</a>'
        expected_output = '<a href="https://example.com" title="Example">Link</a>'
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_disallowed_attributes_removed(self):
        """Ensure that disallowed attributes are removed."""
        input_html = '<a href="https://example.com" onclick="alert(\'XSS\')">Link</a>'
        expected_output = '<a href="https://example.com">Link</a>'
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_allowed_styles_preserved(self):
        """Ensure that allowed CSS styles are preserved."""
        input_html = '<p style="color: red; font-weight: bold;">Styled text</p>'
        expected_output = '<p style="color: red; font-weight: bold">Styled text</p>'
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_malformed_html(self):
        """Ensure that malformed HTML is handled gracefully."""
        input_html = "<p>This is <b>bold<i> and italic</p>"
        expected_output = "<p>This is <b>bold<i> and italic</i></b></p>"
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_escape_entities(self):
        """Ensure that HTML entities are preserved."""
        input_html = "5 &lt; 10 &amp; 10 &gt; 5"
        expected_output = "5 &lt; 10 &amp; 10 &gt; 5"  # If using convert_charrefs=False
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_href_sanitization(self):
        """Ensure that href attributes do not contain 'javascript:'."""
        input_html = "<a href=\"javascript:alert('XSS')\">Bad Link</a>"
        expected_output = "<a>Bad Link</a>"  # 'href' removed due to unsafe scheme
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_style_with_malicious_content(self):
        """Ensure that style attributes do not contain malicious content."""
        input_html = (
            "<p style=\"color: red; background-image: url('javascript:alert(1)');\">Test</p>"
        )
        expected_output = '<p style="color: red">Test</p>'

        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_completely_malicious_input(self):
        """Ensure that completely malicious input is sanitized appropriately."""
        input_html = '<img src="x" onerror="alert(1)" /><script>alert("XSS")</script>'
        expected_output = '<img src="x"/>'

        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_preserve_allowed_and_remove_disallowed_mixed(self):
        """Ensure that allowed and disallowed elements are correctly handled when mixed."""
        input_html = """
            <p>This is a <strong>strong</strong> and <em>emphasized</em> text.</p>
            <script>alert('XSS');</script>
            <a href="https://example.com" onclick="stealCookies()">Example Link</a>
            <div style="color: green; font-size: 12px;">Div content</div>
        """
        expected_output = """
            <p>This is a <strong>strong</strong> and <em>emphasized</em> text.</p>

            <a href="https://example.com">Example Link</a>

            <div style="color: green; font-size: 12px">Div content</div>
        """.strip()

        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )

        # Normalize spaces:
        sanitized = " ".join(sanitized.split())
        expected_output = " ".join(expected_output.split())

        self.assertEqual(sanitized, expected_output)

    def test_allow_links_with_safe_href(self):
        """Ensure that links with safe href attributes are preserved."""
        input_html = '<a href="https://example.com" title="Example">Visit Example</a>'
        expected_output = (
            '<a href="https://example.com" title="Example">Visit Example</a>'
        )
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_allow_empty_style_attribute(self):
        """Ensure that empty style attributes are removed."""
        input_html = '<p style="">No styles</p>'
        expected_output = "<p>No styles</p>"
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    def test_preserve_text_only(self):
        """Ensure that plain text without HTML remains unchanged."""
        input_html = "Just plain text without HTML."
        expected_output = "Just plain text without HTML."
        sanitized = sanitize_html(
            input_html, self.allowed_tags, self.allowed_attrs, self.allowed_styles
        )
        self.assertEqual(sanitized, expected_output)

    @override_settings(
        ALLOWED_HTML_TAGS_INPUT=["p", "a"],
        ALLOWED_HTML_ATTRIBUTES_INPUT=["href"],
        ALLOWED_HTML_STYLES_INPUT=[],
    )
    def test_dynamic_allowed_tags(self):
        """Ensure that sanitizer uses dynamically overridden settings."""
        input_html = (
            "<p>Paragraph with"
            '<a href="https://example.com" title="Example">link</a>'
            "and <b>bold</b>.</p>"
        )
        # With settings overridden, 'a' allows 'href' only, 'b' is disallowed
        expected = '<p>Paragraph with <a href="https://example.com">link</a> and .</p>'
        sanitized = sanitize_html(
            html=input_html,
            allowed_tags=settings.ALLOWED_HTML_TAGS_INPUT,
            allowed_attrs=settings.ALLOWED_HTML_ATTRIBUTES_INPUT,
            allowed_styles=settings.ALLOWED_HTML_STYLES_INPUT,
        )
        self.assertEqual(sanitized, expected)
