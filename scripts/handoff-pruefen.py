#!/usr/bin/env python3
"""handoff-pruefen.py — mechanische Kopf-, Kennungs- und Abschnittsprüfung eines Handoffs.

Warum es das gibt (Website-Sessions 02.10.2026): Handoff r war eine Kopie von q,
in der nur Zeile 1 und eine Tabellenzeile ersetzt wurden. Titel „(q)“, der
Bearbeitungshinweis „Antworten bitte im … -q.rtf“ und „q ersetzt p“ blieben
stehen; Yasin hätte seine Antworten in die falsche Datei geschrieben. Der
Renderer tauscht nur die Pfadzeile und prüft den Rest nicht. Außerdem fehlte in
o, p, q und r die Kopierzeile, und o trug „SAMMLUNG FÜRS …“ statt des Banners,
das sammlung-pruefen.sh sucht.

Aufruf:
  handoff-pruefen.py <handoff.md> [--rtf <zwilling.rtf>] [--jetzt "TT.MM.JJJJ, HH:MM"]

Ohne --rtf wird der gleichnamige .rtf-Zwilling geprüft, falls er existiert.
Rückgabe: 0 = alles in Ordnung · 1 = Befunde · 2 = Aufrufproblem.
Vor dem Rendern (MD) und nach dem Rendern (MD + RTF) laufen lassen.
"""
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re
import subprocess
import sys

BUCHSTABE = 'A-Za-z0-9ÄÖÜäöüß'
STAND = re.compile(r'^Stand:\s*(\d{2})\.(\d{2})\.(\d{4}),?\s+(\d{2}):(\d{2})')
KOPIERZEILE = re.compile(r'^(?:>\s*)?Ich habe das Handoff (?:bearbeitet|beantwortet):\s*`?(.+?)`?\s*$')
BANNER = 'SAMMLUNG FÜR DAS NÄCHSTE HANDOFF'
BANNER_EN = 'COLLECTION FOR THE NEXT HANDOFF'

# Pflichtabschnitte nach HF-06 in ihrer Reihenfolge; je Abschnitt zulässige
# Stichworte (deutsch/englisch und die in Projekten gebräuchlichen Varianten).
ABSCHNITTE = [
    ('Bearbeitungshinweis', ('bearbeitungshinweis', 'editing note')),
    ('Der Stand in drei Sätzen', ('stand in drei sätzen', 'state in three sentences')),
    ('Ziel und Autorisierung', ('ziel und autorisierung', 'objective and authorization')),
    ('Verifizierter Stand', ('verifizierter stand', 'verified state')),
    ('Laufend und offen', ('laufend und offen', 'running and pending')),
    ('Sammlung des Nutzers', ('sammlung', 'collection')),
    ('Was ich daraus gemacht habe', ('was ich daraus gemacht habe', 'what i made of it')),
    ('Entscheidungen und Fragen', ('entscheidungen und fragen', 'fragen an dich', 'decisions and questions')),
    ('Testliste', ('testliste', 'test list')),
    ('Der rote Faden', ('rote faden', 'through-line')),
    ('Kurz-Roadmap', ('roadmap',)),
    ('Messung der Welle', ('messung', 'measurement')),
    ('Hauptdokumente', ('hauptdokumente', 'main documents')),
    ('Gedächtnis', ('gedächtnis', 'memory')),
    ('Logbuch', ('logbuch', 'logbook')),
]


def kennung_aus_name(pfad):
    """`_handoff-aitomat-shop-2026-10-02-r.md` → `r`; `…-2026-10-01-ck` → `ck`."""
    treffer = re.search(r'\d{4}-\d{2}-\d{2}-([' + BUCHSTABE + r']+)$', pfad.stem)
    return treffer.group(1) if treffer else None


def als_token(text, kennung):
    return re.search(r'(?<![' + BUCHSTABE + r'])' + re.escape(kennung) + r'(?![' + BUCHSTABE + r'])',
                     text, re.IGNORECASE) is not None


def geschwister(zeile, md):
    """Pfade auf andere Revisionen derselben Reihe (gleicher Präfix, andere Kennung)."""
    eigen = kennung_aus_name(md)
    praefix = md.stem[:len(md.stem) - len(eigen)] if eigen else None
    if not praefix:
        return []
    funde = re.findall(re.escape(praefix) + r'([' + BUCHSTABE + r']+)\.(?:rtf|md)', zeile)
    return [k for k in funde if k.lower() != eigen.lower()]


def pruefe_md(md, text, jetzt):
    befunde = []
    zeilen = text.splitlines()
    rtf = md.with_suffix('.rtf')
    eigene = {str(md), str(rtf)}
    if not zeilen or zeilen[0].strip().strip('`') not in eigene:
        befunde.append(f'Pfadzeile: Zeile 1 muss der eigene absolute Pfad sein ({md} oder {rtf}).')
    stand = STAND.match(zeilen[1].strip()) if len(zeilen) > 1 else None
    if not stand:
        befunde.append('Standzeile: Zeile 2 muss „Stand: TT.MM.JJJJ, HH:MM“ aus `date` sein.')
    else:
        tag, monat, jahr, stunde, minute = map(int, stand.groups())
        zeitpunkt = datetime(jahr, monat, tag, stunde, minute)
        if zeitpunkt > jetzt + timedelta(minutes=2):
            befunde.append(f'Standzeile: {zeitpunkt:%d.%m.%Y, %H:%M} liegt in der Zukunft — geschätzt statt aus `date`.')

    kennung = kennung_aus_name(md)
    titel = next((z for z in zeilen if z.startswith('# ')), None)
    if kennung is None:
        befunde.append('Kennung: Dateiname endet nicht auf JJJJ-MM-TT-<Kennung>.')
    elif titel is None:
        befunde.append('Titel: keine Überschrift „# …“ gefunden.')
    else:
        if not als_token(titel, kennung):
            befunde.append(f'Kennung: Titel nennt nicht die eigene Kennung „{kennung}“: {titel.strip()}')
        for fremd in re.findall(r'\(([' + BUCHSTABE + r']{1,3})\)', titel):
            if fremd.lower() != kennung.lower():
                befunde.append(f'Kennung: Titel trägt fremde Kennung „({fremd})“, Datei ist „{kennung}“.')

    kopf = zeilen[:15]
    kopier = [KOPIERZEILE.match(z.strip()) for z in kopf]
    kopier = [k for k in kopier if k]
    if not kopier:
        befunde.append('Kopierzeile: „Ich habe das Handoff bearbeitet: <eigener .rtf-Pfad>“ fehlt im Kopf.')
    elif kopier[0].group(1).strip() != str(rtf):
        befunde.append(f'Kopierzeile: zeigt auf {kopier[0].group(1).strip()}, erwartet {rtf}.')

    # Selbstverweise nur im Kopf prüfen (bis zum ersten Abschnitt nach dem
    # Bearbeitungshinweis): weiter unten zitieren Nutzeroriginale zu Recht die
    # Kopierzeile des Vorgängers.
    abschnitte = [n for n, z in enumerate(zeilen) if re.match(r'^##\s', z)]
    if abschnitte and 'bearbeitungshinweis' in zeilen[abschnitte[0]].lower():
        abschnitte = abschnitte[1:]
    kopfende = abschnitte[0] if abschnitte else len(zeilen)
    for nummer, zeile in enumerate(zeilen[:kopfende], 1):
        if re.search(r'Antworten bitte|RTF-Zwilling|Ich habe das Handoff|answer in|RTF twin', zeile, re.IGNORECASE):
            for fremd in geschwister(zeile, md):
                befunde.append(f'Selbstverweis Zeile {nummer}: verweist zum Antworten auf Revision „{fremd}“ statt „{kennung}“.')

    ueberschriften = [(n, z.lstrip('#').strip()) for n, z in enumerate(zeilen) if re.match(r'^##\s', z)]
    letzte = -1
    for name, stichworte in ABSCHNITTE:
        treffer = [n for n, u in ueberschriften
                   if any(s in u.lower() for s in stichworte)
                   and BANNER not in u and BANNER_EN not in u.upper()]
        if not treffer:
            befunde.append(f'Abschnitt fehlt: „{name}“ (HF-06).')
            continue
        passend = [n for n in treffer if n > letzte]
        if not passend:
            befunde.append(f'Reihenfolge: „{name}“ steht vor einem früheren Pflichtabschnitt (HF-06).')
            continue
        letzte = passend[0]
    banner = [n for n, u in ueberschriften if u.upper() in (BANNER, BANNER_EN)]
    if not banner:
        varianten = [u for _, u in ueberschriften if 'SAMMLUNG' in u.upper() and 'NÄCHSTE' in u.upper()]
        hinweis = f' (gefunden: „{varianten[0]}“ — sammlung-pruefen.sh erkennt nur das genaue Banner)' if varianten else ''
        befunde.append(f'Abschnitt fehlt: „## {BANNER}“ als letzter Abschnitt{hinweis}.')
    elif banner[-1] != ueberschriften[-1][0]:
        befunde.append(f'Reihenfolge: „{BANNER}“ muss der letzte Abschnitt sein.')
    elif not any(z.strip().startswith('>>>') for z in zeilen[banner[-1]:]):
        befunde.append(f'Eingang: unter „{BANNER}“ fehlt eine leere `>>>`-Zeile.')
    return befunde


def rtf_text(pfad):
    return subprocess.run(['textutil', '-convert', 'txt', '-stdout', str(pfad)],
                          check=True, capture_output=True).stdout.decode('utf-8')


def pruefe_rtf(md, rtf, text):
    befunde = []
    zeilen = text.splitlines()
    if not zeilen or zeilen[0].strip() != str(rtf):
        befunde.append(f'RTF-Pfadzeile: Zeile 1 des RTF muss {rtf} sein (nicht der MD-Pfad).')
    kennung = kennung_aus_name(rtf)
    titel = next((z for z in zeilen[2:12] if z.strip().startswith('Handoff')), '')
    if kennung and titel and not als_token(titel, kennung):
        befunde.append(f'RTF-Kennung: Titel im RTF nennt nicht „{kennung}“: {titel.strip()}')
    for nummer, zeile in enumerate(zeilen[:20], 1):  # nur der Kopf, siehe pruefe_md
        if re.search(r'Antworten bitte|RTF-Zwilling|Ich habe das Handoff', zeile, re.IGNORECASE):
            for fremd in geschwister(zeile, md):
                befunde.append(f'RTF-Selbstverweis Zeile {nummer}: verweist auf Revision „{fremd}“.')
    return befunde


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('handoff')
    parser.add_argument('--rtf')
    parser.add_argument('--jetzt', help='Vergleichszeit „TT.MM.JJJJ, HH:MM“ (Standard: Systemzeit)')
    args = parser.parse_args(argv)
    md = Path(args.handoff).expanduser().absolute()
    if not md.is_file() or md.suffix != '.md':
        print(f'Aufruf: handoff-pruefen.py <handoff.md> — keine Markdown-Datei: {md}', file=sys.stderr)
        return 2
    jetzt = datetime.strptime(args.jetzt, '%d.%m.%Y, %H:%M') if args.jetzt else datetime.now()
    befunde = pruefe_md(md, md.read_text(encoding='utf-8'), jetzt)
    rtf = Path(args.rtf).expanduser().absolute() if args.rtf else md.with_suffix('.rtf')
    if rtf.is_file():
        befunde += pruefe_rtf(md, rtf, rtf_text(rtf))
    elif args.rtf:
        print(f'RTF nicht gefunden: {rtf}', file=sys.stderr)
        return 2
    for befund in befunde:
        print(f'FEHLT/FALSCH: {befund}')
    if befunde:
        print(f'{len(befunde)} Befund(e) in {md.name} — vor dem Übergeben beheben (neue Revision, nie die beantwortete Datei).')
        return 1
    print(f'OK — {md.name}: Pfad, Stand, Kennung, Kopierzeile, Selbstverweise und Abschnittsfolge stimmen.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
