from django.test import SimpleTestCase

from APP.templatetags.repofilterek import markdown


class MarkdownFilterSecurityTests(SimpleTestCase):
    def test_removes_onerror_attribute(self):
        rendered = str(markdown('<img src="x" onerror="alert(1)">'))

        self.assertNotIn('onerror', rendered.lower())
        self.assertIn('<img', rendered.lower())

    def test_removes_script_elements(self):
        rendered = str(markdown('<script>alert(1)</script>'))

        self.assertNotIn('<script', rendered.lower())
        self.assertNotIn('alert(1)', rendered)

    def test_removes_javascript_link_protocol(self):
        rendered = str(markdown('[Kattints](javascript:alert(1))'))

        self.assertNotIn('javascript:', rendered.lower())

    def test_preserves_safe_markdown(self):
        rendered = str(markdown('**Kiemelt** és [link](https://example.com)'))

        self.assertIn('<strong>Kiemelt</strong>', rendered)
        self.assertIn('href="https://example.com"', rendered)
