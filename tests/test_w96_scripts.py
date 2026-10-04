"""W96: RTF-Lesbarkeit und gespeicherte Eingänge ohne echte Editoraufrufe."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class W96RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='w96-render-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def render(self, markdown):
        source, output = self.root / 'input.md', self.root / 'answer.rtf'
        source.write_text(markdown, encoding='utf-8')
        result = subprocess.run([str(ROOT / 'scripts/handoff-rtf.sh'), str(source), str(output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(output)], text=True)
        return output.read_text(), text

    def test_agenten_fettdruck_wird_gesetzt(self):
        data, text = self.render('Vorher **Wichtig** danach.\n')
        self.assertEqual(text.strip(), 'Vorher Wichtig danach.')
        self.assertIn(r'{\b Wichtig}', data)

    def test_linklabel_ist_keine_zweite_linkquelle(self):
        label = self.root / 'beleg.md'
        label.write_text('Beleg')
        data, text = self.render(f'[**{label}**](https://example.com/check)')
        self.assertIn(str(label), text)
        self.assertEqual(data.count('HYPERLINK'), 1)

    def test_fettdruck_in_linkbeschriftung_bleibt_klickbar(self):
        data, text = self.render('**[Prüfung](https://example.com/check)**\n')
        self.assertEqual(text.strip(), 'Prüfung')
        self.assertIn('HYPERLINK "https://example.com/check"', data)
        self.assertIn(r'{\b ', data)

    def test_tabellen_werden_als_beschriftete_zeilen_lesbar(self):
        data, text = self.render('| Thema | Status |\n| :--- | ---: |\n| C | **fertig** |\n| D | offen |\n')
        self.assertEqual(text.strip(), 'Thema · Status\nThema: C; Status: fertig\nThema: D; Status: offen')
        self.assertNotIn('|', text)
        self.assertNotIn('---', text)
        self.assertIn(r'{\b fertig}', data)

    def test_originale_antworten_und_code_bleiben_woertlich(self):
        original = '**Wörtlich** | kein Umbau |'
        data, text = self.render('<!-- user-original:start -->\n'+original+
                                 '\n<!-- user-original:end -->\n```\n**Code**\n```\n>>> **Antwort**\n')
        self.assertIn(original, text)
        self.assertIn('**Code**', text)
        self.assertIn('>>> **Antwort**', text)
        self.assertIn(r'\fs36\cb1\cbpat1', data)

    def test_tabellenzellen_mit_pipes_code_und_links(self):
        data, text = self.render('| Thema | Beleg |\n| --- | --- |\n'
                                 '| A \\| B | `x|y` und [Link](https://example.com/check) |\n')
        self.assertIn('Thema: A | B; Beleg: x|y und Link', text)
        self.assertIn('HYPERLINK "https://example.com/check"', data)

    def test_inline_code_und_maskierter_fettdruck_bleiben_woertlich(self):
        _, text = self.render('`**Code**` und \\**kein Fett**')
        self.assertIn('**Code**', text)
        self.assertIn('**kein Fett**', text)

    def test_tabellensyntax_in_antwortfortsetzung_bleibt_woertlich(self):
        markdown = '>>>Userantwort:\n| A | B |\n| --- | --- |\n| x | y |\n'
        _, text = self.render(markdown)
        self.assertEqual(text.rstrip('\n'), markdown.rstrip('\n'))


class W96ZwischenrufeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='w96-inbox-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.inbox = self.root / 'Zwischenrufe mit Leerzeichen.md'
        self.inbox.write_text('Gespeicherte Nutzereingabe\n', encoding='utf-8')
        self.calls = self.root / 'calls.txt'
        mock = self.root / 'osascript'
        mock.write_text('#!/bin/bash\ncat >> "$CALLS"\nprintf "%s\\n" "$*" >> "$CALLS"\n'
                        'if [[ "$*" == *"is running"* ]]; then echo true; '
                        'else echo "$EDITOR_STATE"; fi\n')
        mock.chmod(0o755)
        mock = self.root / 'open'
        mock.write_text('#!/bin/bash\nprintf "open %s\\n" "$*" >> "$CALLS"\n')
        mock.chmod(0o755)

    def run_reply(self, state, *extra):
        return subprocess.run(['bash', str(ROOT / 'scripts/zwischenrufe-antwort.sh'),
                               str(self.inbox), 'Geplant als Thema X.', *extra],
                              env={**os.environ, 'PATH': str(self.root)+':'+os.environ['PATH'],
                                   'CALLS': str(self.calls), 'EDITOR_STATE': state},
                              capture_output=True, text=True)

    def test_ungespeichertes_wird_weder_gesichert_noch_angefasst(self):
        original = self.inbox.read_bytes()
        result = self.run_reply('true')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.inbox.read_bytes(), original)
        self.assertNotIn('save (', self.calls.read_text())
        self.assertNotIn('open -a', self.calls.read_text())

    def test_unbekannter_editorzustand_blockiert_anhaengen(self):
        original = self.inbox.read_bytes()
        result = self.run_reply('unbekannt')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.inbox.read_bytes(), original)

    def test_gespeicherter_stand_bekommt_antwort_und_neuen_marker(self):
        result = self.run_reply('false')
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.inbox.read_text()
        self.assertTrue(text.startswith('Gespeicherte Nutzereingabe\n'))
        self.assertIn('ZWISCHENRUFE BIS HIER BEARBEITET', text)
        self.assertIn('Neue Zwischenrufe gelesen: ja', text)
        self.assertIn('Geplant als Thema X.', text)
        self.assertTrue(text.rstrip().endswith('AB HIER NEUE ZWISCHENRUFE\n\n>>>'))
        self.assertIn(str(self.inbox), self.calls.read_text())

    def test_keine_neuen_zwischenrufe_werden_vermerkt(self):
        result = self.run_reply('false', '--keine-neuen')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Neue Zwischenrufe gelesen: nein', self.inbox.read_text())

    def test_nicht_offenes_dokument_wird_nicht_geoeffnet(self):
        result = self.run_reply('nicht offen')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('open -a', self.calls.read_text())

    def test_symlink_wird_nicht_beschrieben(self):
        original = self.inbox.read_bytes()
        alias = self.root / 'Alias.md'
        alias.symlink_to(self.inbox)
        self.inbox = alias
        result = self.run_reply('false')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.inbox.read_bytes(), original)

    def test_rtf_ist_kein_zwischenrufe_eingang(self):
        self.inbox = self.root / 'Zwischenrufe.rtf'
        self.inbox.write_text('RTF unverändert')
        result = self.run_reply('false')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.inbox.read_text(), 'RTF unverändert')


if __name__ == '__main__':
    unittest.main()
