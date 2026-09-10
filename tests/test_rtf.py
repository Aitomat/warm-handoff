"""Isolierte Regressionen; keine Benutzerdateien und keine Editorsteuerung."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import render_rtf
from handoff_common import publish_new


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='warm-handoff-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / '.git').mkdir()
        (self.root / 'docs').mkdir()
        self.document = self.root / 'docs' / 'Grüße & Fragen.md'
        self.document.write_text('Beleg', encoding='utf-8')
        self.source = self.root / 'docs' / 'handoff.md'
        self.output = self.root / 'neu.rtf'

    def run_render(self, content, *args):
        self.source.write_text(content, encoding='utf-8')
        result = subprocess.run([str(SCRIPTS / 'handoff-rtf.sh'), str(self.source),
                                 str(self.output), *args], capture_output=True, text=True)
        return result

    def test_relative_project_link_from_nested_handoff(self):
        result = self.run_render('[Fragen](<docs/Grüße & Fragen.md>)')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.document.as_uri(), self.output.read_text())

    def test_explicit_root_without_git(self):
        (self.root / '.git').rmdir()
        result = self.run_render('[Fragen](<docs/Grüße & Fragen.md>)', '--project-root', str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_plain_relative_paths_and_screenshot_marker(self):
        second = self.root / 'docs' / 'Grüße.md'
        second.write_text('Beleg', encoding='utf-8')
        result = self.run_render('docs/Grüße.md\n⟦Screenshot: ' + str(self.document) + '⟧')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.document.as_uri(), self.output.read_text())
        self.assertIn(second.as_uri(), self.output.read_text())

    def test_slash_in_german_prose_is_not_a_root_path(self):
        original = 'Diagnose-/Altvertragskorrekturen, HTML-/RTF-Links, Geräte-/Fremd-App-Abnahme'
        result = self.run_render(original + '\n[Dokument](<' + str(self.document) + '>)', '--project-root', str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertIn(original, text)
        self.assertIn(self.document.as_uri(), self.output.read_text())

    def test_existing_output_unchanged(self):
        original = b'original >>>Userantwort: unveraendert'
        self.output.write_bytes(original)
        result = self.run_render('# Neu')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), original)

    def test_symlink_output_unchanged(self):
        self.output.symlink_to(self.root / 'does-not-exist')
        result = self.run_render('# Neu')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.output.is_symlink())
        self.assertFalse((self.root / 'does-not-exist').exists())

    def test_missing_link_does_not_publish(self):
        result = self.run_render('[Fehlt](docs/fehlt.md)')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_unsafe_scheme_does_not_publish(self):
        result = self.run_render('[Start](javascript:alert)')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_unicode_originals_copy_line_and_code_roundtrip(self):
        self.output = self.root / 'Neue Antwort Grüße.rtf'
        copy = 'Ich habe das Handoff beantwortet: ' + str(self.output)
        original = '>>>Userantwort: Grüße 👩🏽‍💻 {ja} \\ nein\n>>>Userantwort: Grüße 👩🏽‍💻 {ja} \\ nein'
        code = '```\n/path/that/is/code --argument\n```'
        result = self.run_render(copy + '\n# Titel\n' + original + '\n' + code)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertTrue(text.startswith(copy + '\n'))
        self.assertIn(original, text)
        self.assertIn('/path/that/is/code --argument', text)
        self.assertIn('\\fs36', self.output.read_text())
        self.assertIn('\\highlight1', self.output.read_text())

    def test_web_only_document_and_url_punctuation(self):
        result = self.run_render('https://example.com/path?x=1&y=2.\n>>>')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('HYPERLINK "https://example.com/path?x=1&y=2"', self.output.read_text())

    def test_percent_encoded_local_link(self):
        result = self.run_render('[Fragen](' + self.document.as_uri() + ')')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_conversion_failure_leaves_no_output(self):
        self.source.write_text('>>> Original', encoding='utf-8')
        with patch.object(render_rtf.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'textutil')):
            with self.assertRaises(subprocess.CalledProcessError):
                render_rtf.render(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_wrong_roundtrip_leaves_no_output(self):
        self.source.write_text('>>> Original', encoding='utf-8')
        with patch.object(render_rtf.subprocess, 'run', return_value=subprocess.CompletedProcess('textutil', 0, b'anderer Text')):
            with self.assertRaisesRegex(ValueError, 'roundtrip'):
                render_rtf.render(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_racing_writer_wins_without_overwrite(self):
        import handoff_common
        real_link = handoff_common.os.link
        def race(source, output):
            Path(output).write_bytes(b'Nutzerantwort beim Publizieren')
            return real_link(source, output)
        with patch.object(handoff_common.os, 'link', side_effect=race):
            with self.assertRaises(FileExistsError):
                publish_new(self.output, b'Agentenfassung')
        self.assertEqual(self.output.read_bytes(), b'Nutzerantwort beim Publizieren')
        self.assertEqual(list(self.root.glob('.handoff-*')), [])

    def test_worktree_marker_and_source_directory_fallback(self):
        (self.root / '.git').rmdir()
        (self.root / '.git').write_text('gitdir: irrelevant-for-link-resolution')
        self.assertEqual(render_rtf.project_base(self.source), self.root)
        (self.root / '.git').unlink()
        self.assertEqual(render_rtf.project_base(self.source), self.source.parent)

    def test_local_fragment_is_not_silently_discarded(self):
        result = self.run_render('[Fragen](' + self.document.as_uri() + '#antwort)')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_encoded_filename_punctuation(self):
        special = self.root / 'Antwort #1?.md'
        special.write_text('Beleg', encoding='utf-8')
        result = self.run_render('[Antwort](' + special.as_uri() + ')')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(special.as_uri(), self.output.read_text())

    def test_copy_markers_preserve_nonpath_originals(self):
        originals = '⟦Kopie: „Von Umkehrosmose und Wasser“⟧\n⟦Kopie: „Glaido“⟧\n⟦Kopie: „Eine Überschrift“⟧'
        result = self.run_render(originals)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertEqual(text.rstrip('\n'), originals)
        self.assertNotIn('HYPERLINK', self.output.read_text())

    def test_document_marker_label_and_file_target(self):
        original = '⟦Dokument: RG.pdf — ' + str(self.document) + '⟧'
        result = self.run_render(original)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.document.as_uri(), self.output.read_text())
        text = subprocess.check_output(['textutil', '-convert', 'txt', '-stdout', str(self.output)], text=True)
        self.assertEqual(text.rstrip('\n'), original)


if __name__ == '__main__':
    unittest.main()
