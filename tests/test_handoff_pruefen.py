"""Regressionen aus den Website-Sessions 02.10.2026 (Handoffs o–r des Shop-Projekts).

Nur temporäre Dateien; keine Benutzerdateien, keine Editorsteuerung.
"""
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import importlib.util

_spec = importlib.util.spec_from_file_location('handoff_pruefen', SCRIPTS / 'handoff-pruefen.py')
handoff_pruefen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(handoff_pruefen)

JETZT = datetime(2026, 10, 2, 5, 0)
ABSCHNITTE = ['Der Stand in drei Sätzen', 'Ziel und Autorisierung', 'Verifizierter Stand',
              'Laufend und offen', 'Sammlung des Nutzers — wörtlich', 'Was ich daraus gemacht habe',
              'Entscheidungen und Fragen', 'Testliste', 'Der rote Faden', 'Kurz-Roadmap',
              'Messung der Welle', 'Hauptdokumente und weitere Dokumente', 'Gedächtnis', 'Logbuch']


def handoff(md, kennung, titel_kennung=None, antwort_kennung=None, kopierzeile=True,
            stand='02.10.2026, 04:55', banner='## SAMMLUNG FÜR DAS NÄCHSTE HANDOFF'):
    rtf = md.with_suffix('.rtf')
    antwort = rtf.with_name(rtf.name.replace(f'-{kennung}.rtf', f'-{antwort_kennung or kennung}.rtf'))
    kopf = [str(md), f'Stand: {stand}', '']
    if kopierzeile:
        kopf += [f'Ich habe das Handoff bearbeitet: {rtf}', '']
    kopf += [f'# Handoff Shop — 02.10.2026 ({titel_kennung or kennung})', '',
             '## Bearbeitungshinweis', '', f'Antworten bitte im neuen RTF-Zwilling: {antwort}', '']
    for name in ABSCHNITTE:
        kopf += [f'## {name}', '', 'Inhalt.', '']
    kopf += [banner, '', '>>>Userantwort:', '']
    return '\n'.join(kopf)


class HandoffPruefenTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='warm-handoff-pruefen-')
        self.addCleanup(self.tmp.cleanup)
        self.ordner = Path(self.tmp.name).resolve() / 'Ordner mit Leerzeichen'
        self.ordner.mkdir()
        self.md = self.ordner / '_handoff-shop-2026-10-02-r.md'

    def befunde(self, text):
        return handoff_pruefen.pruefe_md(self.md, text, JETZT)

    def test_vollstaendiges_handoff_ist_sauber(self):
        self.assertEqual(self.befunde(handoff(self.md, 'r')), [])

    def test_kopie_der_vorrevision_mit_fremder_kennung_wird_erkannt(self):
        # Handoff r trug Titel „(q)“ und „Antworten bitte im … -q.rtf“.
        befunde = self.befunde(handoff(self.md, 'r', titel_kennung='q', antwort_kennung='q'))
        text = '\n'.join(befunde)
        self.assertIn('Titel nennt nicht die eigene Kennung „r“', text)
        self.assertIn('fremde Kennung „(q)“', text)
        self.assertIn('Revision „q“ statt „r“', text)

    def test_englische_standzeile_wird_akzeptiert(self):
        text = handoff(self.md, 'r').replace('Stand:', 'As of:')
        self.assertEqual(self.befunde(text), [])

    def test_ungueltiges_datum_ist_befund_statt_absturz(self):
        befunde = self.befunde(handoff(self.md, 'r', stand='32.10.2026, 04:55'))
        self.assertTrue(any('ungültig' in b for b in befunde), befunde)

    def test_fehlende_kopierzeile_wird_erkannt(self):
        befunde = self.befunde(handoff(self.md, 'r', kopierzeile=False))
        self.assertTrue(any(b.startswith('Kopierzeile') for b in befunde), befunde)

    def test_banner_variante_wird_benannt(self):
        # Handoff o endete mit „SAMMLUNG FÜRS NÄCHSTE HANDOFF“.
        befunde = self.befunde(handoff(self.md, 'r', banner='## SAMMLUNG FÜRS NÄCHSTE HANDOFF'))
        self.assertTrue(any('SAMMLUNG FÜRS NÄCHSTE HANDOFF' in b for b in befunde), befunde)

    def test_geschaetzter_stand_in_der_zukunft_wird_erkannt(self):
        # o.md wurde um 01:37 gespeichert, trug aber „Stand: 01:40“.
        befunde = self.befunde(handoff(self.md, 'r', stand='02.10.2026, 05:10'))
        self.assertTrue(any('in der Zukunft' in b for b in befunde), befunde)

    def test_zitierte_vorgaenger_kopierzeile_im_rumpf_ist_kein_befund(self):
        text = handoff(self.md, 'r').replace(
            '## Logbuch\n', '## Logbuch\n\nYasin: ⟦Kopie: „Ich habe das Handoff bearbeitet: '
            + str(self.md.with_name('_handoff-shop-2026-10-02-q.rtf')) + '“⟧\n')
        self.assertEqual(self.befunde(text), [])

    def test_kommandozeile_meldet_exit_eins(self):
        self.md.write_text(handoff(self.md, 'r', titel_kennung='q'), encoding='utf-8')
        result = subprocess.run([sys.executable, str(SCRIPTS / 'handoff-pruefen.py'), str(self.md),
                                 '--jetzt', '02.10.2026, 05:00'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


class SammlungPruefenTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='warm-handoff-sammlung-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_check(self, vorgaenger_text, neu_text):
        alt = self.root / '_handoff-alt.md'
        neu = self.root / '_handoff-neu.md'
        alt.write_text(vorgaenger_text, encoding='utf-8')
        neu.write_text(neu_text, encoding='utf-8')
        return subprocess.run(['bash', str(SCRIPTS / 'sammlung-pruefen.sh'), str(neu), str(alt)],
                              capture_output=True, text=True)

    def test_alte_originale_werden_nicht_erneut_verlangt(self):
        alt = ('## Sammlung des Nutzers — wörtlich\n'
               '<!-- user-original:start -->\n>>>Alte längst bearbeitete Antwort\n'
               '<!-- user-original:end -->\n'
               '## Entscheidungen und Fragen\n>>>Userantwort: Neue Entscheidung behalten\n\n'
               '## SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>Neuer Wunsch erhalten\n')
        result = self.run_check(alt, 'F1 umgesetzt (Quelle: _handoff-alt, F1)\nNeuer Wunsch erhalten\n')
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_antwortfelder_nur_verweisen_kein_fehlalarm(self):
        # W97/T34: Antworten des Vorgängers werden nicht wörtlich wiederholt.
        alt = ('## Testliste\n>>>Userantwort: Dieser neue Fehler bleibt offen und muss behoben werden\n\n'
               '## SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>\n')
        result = self.run_check(alt, '# Neu\nT1 behoben (Quelle: _handoff-alt, T1)\n')
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_antwortfelder_ohne_verweis_sind_befund(self):
        alt = ('## Testliste\n>>>Userantwort: Dieser neue Fehler bleibt offen\n\n'
               '## SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>\n')
        result = self.run_check(alt, '# Neu\n')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('VERWEIS FEHLT', result.stdout)

    def test_woertlich_wiederholte_antwort_ist_befund(self):
        antwort = 'Diese ganzen Fragen und Antworten von der letzten Session brauchen wir nicht'
        alt = (f'## Entscheidungen und Fragen\n>>>Userantwort: {antwort}\n\n'
               '## SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>\n')
        result = self.run_check(alt, f'# Neu\nCL — neue Antworten (_handoff-alt)\n{antwort}\n')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('WÖRTLICH WIEDERHOLT', result.stdout)

    def test_automatisch_nur_direkten_vorgaenger_pruefen(self):
        a = self.root / '_handoff-a.md'
        b = self.root / '_handoff-b.md'
        neu = self.root / '_handoff-neu.md'
        a.write_text('SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>Ältere erledigte Eingabe\n')
        b.write_text('SAMMLUNG FÜR DAS NÄCHSTE HANDOFF\n>>>Neue frische Eingabe\n')
        # Deterministische Reihenfolge ohne sleep oder Annahme zur Uhr.
        import os
        os.utime(a, ns=(1, 1))
        os.utime(b, ns=(2, 2))
        neu.write_text('Neue frische Eingabe\n')
        result = subprocess.run(['bash', str(SCRIPTS / 'sammlung-pruefen.sh'), str(neu)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('Ältere erledigte Eingabe', result.stdout)

    def test_fehlender_vorgaenger_ist_befund(self):
        neu = self.root / '_handoff-neu.md'
        neu.write_text('Neu')
        result = subprocess.run(['bash', str(SCRIPTS / 'sammlung-pruefen.sh'), str(neu),
                                 str(self.root / 'fehlt.md')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_englischer_sammlungsfuss(self):
        alt = '## COLLECTION FOR THE NEXT HANDOFF\n>>>Keep this new idea\n'
        result = self.run_check(alt, 'Keep this new idea\n')
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_vorgaenger_ohne_banner_ist_kein_stilles_ok(self):
        # Vorher: „0 Sammlungszeilen geprüft, 0 fehlen“ und Exit 0.
        result = self.run_check('# Alt\n\nKein Banner hier.\n>>>Wichtige Idee von Yasin\n', '# Neu\n')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('kein SAMMLUNG-Banner', result.stdout)

    def test_banner_variante_fuers_wird_gelesen(self):
        alt = '# Alt\n\nSAMMLUNG FÜRS NÄCHSTE HANDOFF\n\n>>>Wichtige Idee von Yasin\n'
        result = self.run_check(alt, '# Neu\n')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('FEHLT: >>>Wichtige Idee von Yasin', result.stdout)
        result = self.run_check(alt, '# Neu\n\nWichtige Idee von Yasin\n')
        self.assertEqual(result.returncode, 0, result.stdout)


    def test_rtf_vorgaenger_wird_als_klartext_gelesen(self):
        # Yasins Antworten stehen im gespeicherten RTF, nicht im Agenten-MD.
        alt = self.root / '_handoff-alt.rtf'
        alt.write_text('{\\rtf1\\ansi{\\fonttbl{\\f0 Helvetica;}}\\f0 '
                       '# Alt\\par SAMMLUNG F\\u220?R DAS N\\u196?CHSTE HANDOFF\\par '
                       '>>>Antwort aus dem RTF von Yasin\\par}', encoding='ascii')
        neu = self.root / '_handoff-neu.md'
        neu.write_text('# Neu\n', encoding='utf-8')
        result = subprocess.run(['bash', str(SCRIPTS / 'sammlung-pruefen.sh'), str(neu), str(alt)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('FEHLT: >>>Antwort aus dem RTF von Yasin', result.stdout)

if __name__ == '__main__':
    unittest.main()
