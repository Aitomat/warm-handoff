"""RTF-Kopf: erste Zeile ist der eigene RTF-Pfad, nicht der MD-Pfad (Yasin, 28.09.2026)."""
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


class PathHeaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='warm-handoff-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / '.git').mkdir()
        self.source = self.root / '_handoff-x.md'
        self.output = self.root / '_handoff-x.rtf'

    def render(self, content):
        self.source.write_text(content, encoding='utf-8')
        result = subprocess.run([str(SCRIPTS / 'handoff-rtf.sh'), str(self.source), str(self.output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        return text.splitlines(), self.output.read_text()

    def test_first_line_is_own_rtf_path_as_link(self):
        lines, raw = self.render(f'{self.source}\nStand: 28.09.2026, 03:00\n\nText\n')
        self.assertEqual(lines[0], str(self.output))
        self.assertEqual(lines[1], 'Stand: 28.09.2026, 03:00')
        self.assertNotIn(str(self.source), '\n'.join(lines))
        self.assertNotIn(self.source.as_uri(), raw)
        self.assertIn('HYPERLINK "' + self.output.as_uri() + '"', raw)

    def test_other_first_line_stays(self):
        lines, _ = self.render('Überschrift\nText\n')
        self.assertEqual(lines[0], 'Überschrift')


if __name__ == '__main__':
    unittest.main()
