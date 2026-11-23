from django.template import Context, Engine
from django.test import SimpleTestCase
from django.utils.safestring import SafeData

from APP.templatetags.repofilterek import markdown


class MarkdownFilterTests(SimpleTestCase):
    def test_removes_active_html_and_unsafe_urls(self):
        examples = [
            '<img src="x" onerror="alert(1)">',
            '<a href="javascript:alert(1)" onclick="alert(1)">link</a>',
            '<a href="jav&#x61;script:alert(1)">link</a>',
            '[link](javascript:alert(1))',
            '<img src="data:image/svg+xml,<svg onload=alert(1)>">',
            '<script>alert(1)</script>',
            '<svg><a onload="alert(1)">x</a></svg>',
            '<iframe src="https://example.com"></iframe>',
            '<div style="background:url(javascript:alert(1))">text</div>',
        ]
        for value in examples:
            with self.subTest(value=value):
                result = markdown(value).lower()
                for forbidden in ('onerror', 'onclick', 'onload', 'javascript:',
                                  'data:image', '<script', '<svg', '<iframe', 'style='):
                    self.assertNotIn(forbidden, result)

    def test_preserves_markdown_and_syntax_highlighting(self):
        value = (
            '# Heading\n\n**bold** and [link](https://example.com)\n\n'
            '![image](https://example.com/image.png)\n\n'
            '| A | B |\n|---|---|\n| 1 | 2 |\n\n'
            '```python\nprint("hello")\n```'
        )
        result = markdown(value)
        for expected in ('<h1>Heading</h1>', '<strong>bold</strong>',
                         'href="https://example.com"', 'src="https://example.com/image.png"',
                         '<table>', '<td>1</td>', 'class="codehilite"', '<span class='):
            self.assertIn(expected, result)
        self.assertIsInstance(result, SafeData)

    def test_template_output_is_sanitized_without_double_escaping(self):
        engine = Engine(libraries={'repofilterek': 'APP.templatetags.repofilterek'})
        template = engine.from_string('{% load repofilterek %}{{ value|markdown }}')
        result = template.render(Context({'value': '**OK** <img src=x onerror=alert(1)>'}))
        self.assertIn('<strong>OK</strong>', result)
        self.assertIn('<img src="x">', result)
        self.assertNotIn('onerror', result)
