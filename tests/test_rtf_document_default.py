"""Der Dokumentstandard ist 18 pt Gold, damit Cmd-V und Tippen richtig aussehen.

Yasin, 12.09.2026, 21:03: „wenn ich Cmd-V mache und Text eingebe, dann schaut es
so aus: kleine Schrift und ohne gelb". Ursache war ein Kopf ohne `\\fs`: hinter
jeder Absatzgruppe `{\\pard \\fs36 ...\\par}` galt wieder der RTF-Urstandard
12 pt ohne Hintergrund, und genau den erbte ein neuer Absatz.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentDefaultTests(unittest.TestCase):
    def render(self, markdown):
        directory = tempfile.TemporaryDirectory(prefix='handoff-default-')
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        source = root / 'source.md'
        source.write_text(markdown, encoding='utf-8')
        output = root / 'answer.rtf'
        result = subprocess.run([str(ROOT / 'scripts/handoff-rtf.sh'),
                                 str(source), str(output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return output

    def test_header_sets_gold_18pt_as_document_default(self):
        output = self.render('# Titel\n\nAgententext.\n\n>>>Userantwort:')
        header = output.read_text().splitlines()[0]
        self.assertIn('\\f0\\fs36\\cb1\\cbpat1\\chshdng0\\chcbpat1\\highlight1\\cf2', header)
        self.assertIn('{\\stylesheet{\\s0\\f0\\fs36\\cb1\\cbpat1\\chshdng0'
                      '\\chcbpat1\\highlight1\\cf2 Normal;}}',
                      header)

    def test_agent_paragraphs_reset_with_plain_not_cb0(self):
        # \cb0 waere in Cocoa schwarz; \plain ist der einzige saubere Reset.
        rtf = self.render('# Titel\n\nAgententext.\n\n```\ncode\n```\n').read_text()
        self.assertNotIn('\\cb0', rtf)
        self.assertIn('{\\pard\\plain\\f0\\cf2\\fs36 Agententext.\\par}', rtf)
        self.assertIn('{\\pard\\plain\\f0\\cf2\\fs48\\b Titel\\par}', rtf)
        self.assertIn('{\\pard\\plain\\f0\\cf2\\fs30 code\\par}', rtf)

    def test_cocoa_import_gives_gold_18pt_answer_and_clean_agent_text(self):
        output = self.render('# Titel\n\nAgententext.\n\n>>>Userantwort:')
        html = subprocess.check_output(
            ['textutil', '-convert', 'html', '-stdout', str(output)], text=True)
        classes = dict(re.findall(r'p\.(p\d+) \{([^}]*)\}', html))
        gold = [name for name, rule in classes.items() if 'background-color' in rule]
        self.assertEqual(len(gold), 1, html)
        self.assertIn('18.0px', classes[gold[0]])
        self.assertIn('#ffe799', classes[gold[0]].lower())
        self.assertIn('<p class="%s">&gt;&gt;&gt;Userantwort:</p>' % gold[0], html)
        agent = re.search(r'<p class="(p\d+)">Agententext\.</p>', html)
        self.assertIsNotNone(agent, html)
        self.assertNotIn('background-color', classes[agent.group(1)])
        self.assertIn('18.0px', classes[agent.group(1)])


if __name__ == '__main__':
    unittest.main()
