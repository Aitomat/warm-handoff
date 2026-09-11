import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/handoff-inputs.py'

class InputArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'original.md'
        self.raw = 'Original ä\n>>>Antwort: vollständig\n'.encode()
        self.source.write_bytes(self.raw)
        self.snapshot = self.root / 'snapshot.json'

    def run_cli(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stderr)
        return p

    def external(self):
        self.run_cli('snapshot', '--output', self.snapshot, '--archive-dir', self.root / 'originals', self.source)
        return json.loads(self.snapshot.read_text())

    def test_external_bytes_and_text_and_saved_revision(self):
        data = self.external()
        s = data['sources'][0]
        self.assertNotIn('bytes_base64', s)
        archived = self.snapshot.parent / s['archive_path']
        self.assertEqual(archived.read_bytes(), self.raw)
        self.assertEqual(s['text'], self.raw.decode())
        self.assertEqual(s['sha256'], hashlib.sha256(self.raw).hexdigest())
        self.run_cli('verify', self.snapshot)
        self.source.write_text('Neue Revision')
        self.run_cli('verify', self.snapshot, ok=False)
        self.assertEqual(archived.read_bytes(), self.raw)

    def test_external_corruption_rejected_and_original_never_overwritten(self):
        s = self.external()['sources'][0]
        self.run_cli('snapshot', '--output', self.snapshot, '--archive-dir', self.root / 'originals', self.source, ok=False)
        self.assertEqual(self.source.read_bytes(), self.raw)
        (self.snapshot.parent / s['archive_path']).write_bytes(b'broken')
        self.run_cli('verify', self.snapshot, ok=False)

    def test_legacy_base64_verify_and_ledger_still_work(self):
        self.run_cli('snapshot', '--output', self.snapshot, self.source)
        s = json.loads(self.snapshot.read_text())['sources'][0]
        self.assertEqual(base64.b64decode(s['bytes_base64']), self.raw)
        self.check_ledger(s)

    def test_external_ledger_and_relocation(self):
        s = self.external()['sources'][0]
        self.check_ledger(s)
        moved = self.root / 'moved'
        moved.mkdir()
        self.snapshot.rename(moved / self.snapshot.name)
        (self.root / 'originals').rename(moved / 'originals')
        self.run_cli('verify', moved / self.snapshot.name)

    def test_missing_archive_and_changed_cleartext_are_rejected(self):
        data = self.external()
        data['sources'][0]['text'] += 'changed'
        self.snapshot.write_text(json.dumps(data))
        self.run_cli('verify', self.snapshot, ok=False)
        data['sources'][0]['text'] = self.raw.decode()
        self.snapshot.write_text(json.dumps(data))
        (self.snapshot.parent / data['sources'][0]['archive_path']).unlink()
        self.run_cli('verify', self.snapshot, ok=False)

    def test_existing_archive_is_never_replaced(self):
        data = self.external()
        archived = self.snapshot.parent / data['sources'][0]['archive_path']
        archived.write_bytes(b'Existing evidence')
        other = self.root / 'second.json'
        self.run_cli('snapshot', '--output', other, '--archive-dir', self.root / 'originals', self.source, ok=False)
        self.assertEqual(archived.read_bytes(), b'Existing evidence')
        self.assertFalse(other.exists())

    @unittest.skipUnless(sys.platform == 'darwin', 'RTF extraction uses macOS textutil')
    def test_rtf_archives_exact_bytes_and_extracts_readable_text(self):
        self.source = self.root / 'original.rtf'
        raw = b'{\\rtf1\\ansi Original \\b fett\\b0\\par}'
        self.source.write_bytes(raw)
        data = self.external()
        source = data['sources'][0]
        self.assertEqual((self.snapshot.parent / source['archive_path']).read_bytes(), raw)
        self.assertIn('Original fett', source['text'])
        self.run_cli('verify', self.snapshot)

    def check_ledger(self, s):
        items = self.root / 'items.json'
        items.write_text(json.dumps([dict(id='a', source=s['path'], start=0, end=len(s['text']),
            original=s['text'], status='ready', interpretation='', acceptance='', evidence='', next='')]))
        self.run_cli('ledger', self.snapshot, items)

if __name__ == '__main__':
    unittest.main()
