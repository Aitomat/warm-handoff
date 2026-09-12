"""Check gold on each expected paragraph, including multiline originals."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GoldLineTests(unittest.TestCase):
    def test_each_user_line_is_gold_and_boundaries_reset(self):
        with tempfile.TemporaryDirectory(prefix='f3-gold-') as directory:
            output = Path(directory) / 'gold.rtf'
            subprocess.run([str(ROOT / 'scripts/handoff-rtf.sh'),
                            str(ROOT / 'tests/fixtures/f3-gold.md'), str(output)],
                           check=True, capture_output=True)
            lines = output.read_text().splitlines()
            expected = ['>>>Answer: First answer line', 'Second answer line',
                        'Third answer line', '>>>Answer: Before heading',
                        '>>>Answer: Before explicit end', '>>>Answer: Before code',
                        'Old user message', '# Old literal heading', 'Old user wish']
            for text in expected:
                with self.subTest(text=text):
                    paragraphs = [line for line in lines if text in line]
                    self.assertEqual(len(paragraphs), 1)
                    count = subprocess.run(['grep', '-c', 'cbpat1'],
                                           input='\n'.join(paragraphs), text=True,
                                           capture_output=True)
                    self.assertGreater(int(count.stdout), 0, text)
            for line in lines:
                if 'Agent' in line:
                    self.assertNotIn('cbpat1', line)
            self.assertEqual(sum('cbpat1' in line for line in lines), 11)


if __name__ == '__main__':
    unittest.main()
