"""Cocoa-Roundtrip für Antwortfarben; keine Editor- oder Nutzerdateizugriffe."""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


class BackgroundTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='handoff-background-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source.md'
        self.output = self.root / 'answer.rtf'

    def render(self, text):
        self.source.write_text(text)
        return subprocess.run([str(SCRIPTS / 'handoff-rtf.sh'), str(self.source), str(self.output)],
                              capture_output=True, text=True)

    def cocoa_html(self):
        # RTF erneut einlesen und speichern: ein bloßer TXT-Roundtrip verliert Formatbelege.
        saved = subprocess.check_output(['textutil', '-convert', 'rtf', '-format', 'rtf',
                                          '-stdout', str(self.output)])
        return subprocess.check_output(['textutil', '-convert', 'html', '-format', 'rtf',
                                         '-stdin', '-stdout'], input=saved).decode()

    def paragraph_style(self, html, text):
        paragraph = re.search(r'<p class="([^"]+)">' + re.escape(text) + r'</p>', html)
        self.assertIsNotNone(paragraph, html)
        style = re.search(r'p\.' + re.escape(paragraph.group(1)) + r'\s*\{([^}]+)\}', html)
        self.assertIsNotNone(style, html)
        return style.group(1)

    def test_answer_background_survives_cocoa_save_without_coloring_agent_reply(self):
        result = self.render('>>>Userantwort: Antwort\n<!-- answer:end -->\nAgentenantwort')
        self.assertEqual(result.returncode, 0, result.stderr)
        html = self.cocoa_html()
        answer = self.paragraph_style(html, '&gt;&gt;&gt;Userantwort: Antwort')
        self.assertIn('background-color: #ffe799', answer)
        self.assertIn('18.0px', answer)
        self.assertNotIn('background-color', self.paragraph_style(html, 'Agentenantwort'))

    def test_multiline_original_preserves_literal_text_and_background(self):
        original = 'Antwort eins\n# Originalüberschrift\n[kein Link](nicht-vorhanden.md)'
        result = self.render('<!-- user-original:start -->\n' + original
                             + '\n<!-- user-original:end -->\nAgentenantwort')
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertEqual(text, original + '\nAgentenantwort\n')
        html = self.cocoa_html()
        for line in original.splitlines():
            self.assertIn('background-color: #ffe799', self.paragraph_style(html, line))
        self.assertNotIn('background-color', self.paragraph_style(html, 'Agentenantwort'))

    def test_unclosed_original_does_not_publish(self):
        result = self.render('<!-- user-original:start -->\nAntwort')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_markers_inside_code_are_literal(self):
        result = self.render('```\n<!-- user-original:start -->\n```')
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertEqual(text, '<!-- user-original:start -->\n')


if __name__ == '__main__':
    unittest.main()
