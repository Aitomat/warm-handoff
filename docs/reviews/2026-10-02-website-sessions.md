/Users/pro16/Code/warm-handoff/docs/reviews/2026-10-02-website-sessions.md
Stand: 02.10.2026, 11:54

# SKILLCHECK95 — warm-handoff in den Website-Sessions (Handoffs n–r)

Quelle: `Shop-Kopiervorlage/handoffs/` (nur gelesen). Branch `w95-skillcheck`, Commits 99f127c, 36c7993.

## Befunde (alle bewiesen)
1. **r ist Kopie von q:** MD unterscheidet sich nur in Zeile 1 und 430; Titel „(q)“ (r.md:4), „Antworten bitte im …-q.rtf“ (r.md:8), „q ersetzt p“ (r.md:11). Ursache: Renderer tauscht nur Zeile 1, nichts prüft die Kennung.
2. **r: MD und RTF auseinander:** „Nachtrag Claude 04:58“ nur im RTF (Text 115–119), RTF Cocoa-gespeichert 05:14. Regel fehlte.
3. **Kopierzeile fehlt** in n, o, p, q, r. Ursache: HF-01 (Pfad zuerst) gegen HF-06 („Kopierzeile ganz oben“); Renderer kannte nur „beantwortet“, HF-06 sagt „bearbeitet“.
4. **o:** „SAMMLUNG FÜRS …“ (Text 216) — `sammlung-pruefen.sh` meldete still OK; MD-Vorgänger enthalten Yasins Antworten nie.
5. **Geschätzte Uhrzeit:** o.md gespeichert 01:37, „Stand 01:40“; n.md 18:42 gegen 18:45.
6. **p** ohne Pfadzeile/Abschnitte, per textutil erzeugt (Faktendatei:13).
7. **Codex-Host:** Chef-Prompt „nichts öffnen“ (_codex-handoff-q.log:16) übersteuerte Yasins Regel „erwähnte Dokumente öffnen“ (Faktendatei:15).
8. **Lesbarkeit:** q 546 Zeilen/72 KB; RTF zeigt 56 Zeilen mit `**` und 52 Tabellenzeilen roh.
9. **Doppelte Wellennummer:** „Welle 9“ (o) und „Codex-Welle 9“ (q).

## Korrekturen
- `scripts/handoff-pruefen.py` (neu): Pfad, Stand (Zukunft = Schätzung), Kennung, Kopierzeile, Selbstverweise, HF-06-Folge. Findet r, o, p, q; cj/ck/cg/ch sauber.
- `render_rtf.py`: „bearbeitet“ wird verlinkt.
- `sammlung-pruefen.sh`: fehlendes Banner = Befund, „FÜRS“, RTF-Vorgänger.
- HF-08 (de/en), HF-06-Kopf, Codex-Checkliste, AGENTS.md.
- Tests: `Ran 66 tests … OK` (vorher 55; 4 neue zuerst rot).

## Braucht Yasins OK
- A: Chef-Aufträge an Codex dürfen Yasins Regeln nicht still einschränken (Befund 7).
- B: Wellennummern je Projekt einmalig.
- C: Renderer setzt `**` fett und Tabellen lesbar.
- D: `zwischenrufe-antwort.sh:64` speichert ungespeicherte Nutzereingaben — widerspricht HF-01.

## Offen
Installierte Fassung unverändert; Aitomat-AGENTS.md nennt noch „drei Skripte“.

## Für das Handbuch
Vor jedem Handoff prüft `handoff-pruefen.py`, ob Titel, Kopierzeile und Antwortdatei zur selben Revision gehören.

## Frage an Yasin
Dürfen A–D umgesetzt werden?
