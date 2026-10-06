#!/usr/bin/env python3
"""HF-08-Abgleich neuer gespeicherter Eingaben; eine Heuristik, kein Vollbeweis.

Seit W97 (Yasin, 06.10.2026, T34): Antworten in den Antwortfeldern des Vorgängers
werden NICHT wörtlich übernommen, nur verwiesen („was ich daraus gemacht habe“).
Wörtlich verlangt wird nur der Sammlungsfuß des Vorgängers."""
from pathlib import Path
import re
import subprocess
import sys

BANNER = re.compile(r"^(?:#{1,6}\s*)?(?:SAMMLUNG FÜR(?:S| DAS) NÄCHSTE HANDOFF|COLLECTION FOR THE NEXT HANDOFF)\s*$", re.I)
ALTE_SAMMLUNG = re.compile(r"^(?:#{1,6}\s*)?(?:Sammlung des Nutzers|Deine Sammlung|Your collection|The user's collection|Preserved user input)", re.I)
ABSCHNITT = re.compile(r"^(?:#{1,6}\s|Entscheidungen und Fragen|Decisions and questions|Testliste|Test list|Was ich daraus gemacht habe|What I made of it)", re.I)
LEERE_MARKER = re.compile(r"^>>>(?:Userantwort:|User answer:|Antwort:)?\s*$", re.I)


WOERTLICH_MIN = 40  # kürzere Antworten („Ja“, „OK“) sind kein Wiederholungsbeleg


def neue_eingaben(text):
    """Liefert (antwortfelder, fuss): beide als Liste (Originalzeile, Kern)."""
    zeilen = text.splitlines()
    banner = [i for i, z in enumerate(zeilen) if BANNER.fullmatch(z.strip())]
    if not banner:
        raise ValueError('kein SAMMLUNG-Banner gefunden — Nutzereingaben von Hand abgleichen.')
    fuss = banner[-1]
    original = alt = antwort = False
    eingaben = []
    antworten = []
    for i, zeile in enumerate(zeilen):
        z = zeile.strip()
        if z == '<!-- user-original:start -->':
            original = True
            continue
        if z == '<!-- user-original:end -->':
            original = False
            continue
        if i < fuss:
            if ALTE_SAMMLUNG.match(z):
                alt = True
                antwort = False
            elif ABSCHNITT.match(z):
                alt = False
                antwort = False
            if original or alt:
                continue
            if z.startswith('>>>'):
                antwort = True
            elif not z or z.startswith(('<!--', '```', '~~~', '#')):
                antwort = False
            if not antwort:
                continue
        elif i == fuss:
            continue
        if not z or LEERE_MARKER.fullmatch(z) or z.startswith(('aus:', 'from:', '═', '▼')):
            continue
        # Präfix ist ein Antwortfeld, der folgende Text bleibt wörtlich.
        z = re.sub(r'^>>>(?:Userantwort:|User answer:|Antwort:)?\s*', '', z, flags=re.I)
        if z:
            (eingaben if i > fuss else antworten).append((zeile.strip(), z))
    return antworten, eingaben


def klartext(pfad):
    if pfad.suffix.lower() == '.rtf':
        return subprocess.run(['textutil', '-convert', 'txt', '-stdout', str(pfad)],
                              check=True, capture_output=True, text=True).stdout
    return pfad.read_text(encoding='utf-8')


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not 1 <= len(args) <= 2:
        print('Aufruf: sammlung-pruefen.sh <neues-handoff.md> [direkter-vorgänger.md|.rtf]', file=sys.stderr)
        return 2
    neu = Path(args[0]).expanduser().resolve()
    try:
        neu_text = '\n'.join(z.strip() for z in klartext(neu).splitlines())
        if len(args) == 2:
            alt = Path(args[1]).expanduser().resolve(strict=True)
        else:
            kandidaten = [p for p in neu.parent.glob('_handoff-*.md') if p.resolve() != neu]
            if not kandidaten:
                print('Keine Vorgänger-Handoffs gefunden — nichts zu prüfen.')
                return 0
            alt = max(kandidaten, key=lambda p: p.stat().st_mtime_ns)
            if alt.with_suffix('.rtf').is_file():
                alt = alt.with_suffix('.rtf')
        print(f'── Vorgänger: {alt}')
        antworten, eingaben = neue_eingaben(klartext(alt))
        fehlt = [original for original, kern in eingaben if kern not in neu_text]
        doppelt = [original for original, kern in antworten
                   if len(kern) >= WOERTLICH_MIN and kern in neu_text]
        verweis_fehlt = bool(antworten) and alt.stem not in neu_text
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f'BEFUND: {error}')
        return 1
    for zeile in fehlt:
        print(f'   FEHLT: {zeile}')
    for zeile in doppelt:
        print(f'   WÖRTLICH WIEDERHOLT: {zeile}')
    if verweis_fehlt:
        print(f'   VERWEIS FEHLT: Antworten des Vorgängers nur mit Quelle „{alt.stem}“ verweisen.')
    print(f'   {len(eingaben)} Sammlungszeilen geprüft, {len(fehlt)} fehlen; '
          f'{len(antworten)} Antwortfelder nur als Verweis erwartet, {len(doppelt)} wörtlich wiederholt.')
    if fehlt or doppelt or verweis_fehlt:
        print('Sammlungsfuß wörtlich nachtragen; Antworten des Vorgängers nicht wiederholen, '
              'nur je Punkt „was ich daraus gemacht habe“ mit Quelle (HF-08).')
        return 1
    print('OK — Sammlungsfuß enthalten, Antworten des Vorgängers nur verwiesen (HF-08).')
    return 0

if __name__ == '__main__':
    sys.exit(main())
