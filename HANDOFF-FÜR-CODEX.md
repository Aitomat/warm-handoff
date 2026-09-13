# HANDOFF FÜR CODEX — die Checkliste zum Abarbeiten

Yasin, 12.09.2026, 20:59: „dass der Codex, wenn der mal einen Handoff macht, das
auch richtig macht." Diese Seite ist genau dafür da. Wer einen Handoff schreibt —
Codex, Claude oder ein Wächter —, geht sie von oben nach unten durch.

Es ist eine Kurzfassung, kein Ersatz. Die verbindlichen Texte sind
[SKILL.de.md](SKILL.de.md), [Handoff-Format](references/handoff-format.de.md),
[RTF unter macOS](references/rtf-macos.de.md) und
[Wellen-Ausführung](references/wave-execution.de.md).
Englische Fassung: [HANDOFF-FOR-CODEX.md](HANDOFF-FOR-CODEX.md).

Sprache deutsch. Zeitstempel überall als `TT.MM.JJJJ, HH:MM`.

## 1. Vorher lesen — vollständig, nicht geraten

- Den **benannten** Vorgänger-Handoff, nicht den mit dem neuesten Änderungsdatum.
- Die RTF-Antworten: `textutil -convert txt -stdout DATEI.rtf`.
- Die Zwischenrufe-Datei und die Chat-Steuerung.
- **Nur der gespeicherte Stand zählt. Cmd-S ist die Freigabe.** Was in einem
  Editor ungespeichert offen liegt, ist nicht gelesen: entweder um das Speichern
  bitten oder die Lücke im Handoff ausdrücklich als Lücke benennen. Niemals die
  Antwortdatei des Nutzers zum Einlesen speichern, schließen oder neu erzeugen.
- `[Pasted text]` / `Pasted Content` ist **kein Inhalt**. Die zugehörige Datei
  öffnen; fehlt sie, den Eingang ausdrücklich offenlassen.
- Nutzeroriginale wörtlich übernehmen; Deutung und Antwort in eigene Abschnitte.

## 2. Die Pflichtblöcke — in dieser Reihenfolge

1. **Kopierzeile ganz oben**, eine ungeteilte Zeile:
   `Ich habe das Handoff beantwortet: /absoluter/Pfad/zur/neuen.rtf`
   Danach Titel, gemessene Zeit mit Zeitzone, Vorgänger, Hinweis auf `>>>`-Felder.
2. **Der Stand in drei Sätzen** — Ziel, überprüfter Stand, nächste Aktion; dazu
   Modus (Zwischenstand / fortsetzbar / abgeschlossen) und gültige Autorisierung.
3. **Was noch im Tank ist** — Messquelle, Alter, Umfang; sonst „nicht gemessen".
4. **Erwartete Agenten-Ergebnisse** — ID, Besitzer, beobachteter Status,
   Worktree/Branch/Basis, Berichtspfad, bekannte Laufzeitgrenzen.
5. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** und
   **Was ich daraus gemacht habe** — jedes Original mit Status und Beleg.
6. **Vorige Testantworten — was daraus wurde** und **Testliste vN** mit leeren
   `>>>Userantwort:`-Feldern. Kein offener Test gilt als bestanden.
7. **Fragen an dich** mit `>>>Antwort:`; optionale Fragen getrennt von den
   Entscheidungen, die den nächsten Schritt wirklich sperren.
8. **Der rote Faden**, **Hauptdokumente**, **Weitere Dokumente**, **Aktive
   Werkzeuge dieses Projekts** — echte Pfade, tatsächliche Verfügbarkeit.
9. **Gedächtnis** — je vier bis sechs konkrete Lang- und Kurzzeitpunkte.
10. **Kostentabelle** — Quelle, Alter, Haupt-/Arbeiteranteile, Messlücken.
11. Ganz zuletzt **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit Ursprungspfad und `>>>`.

**Genau EIN aktiver Sammlungs- bzw. Zwischenrufe-Abschnitt.** Entweder der
RTF-Fußbereich oder die vereinbarte Zwischenrufe-Datei; am anderen Ort steht nur
ein Link darauf. Zwei parallele Eingänge haben schon Antworten verschluckt.

## 3. Die drei Skripte

Immer benutzen, nie von Hand nachbauen.

| Skript | Wofür | Aufruf |
| --- | --- | --- |
| [`handoff-rtf.sh`](scripts/handoff-rtf.sh) | Markdown → RTF-Zwilling: klickbare Linkfelder, 18 pt, goldene Antwortabsätze | `scripts/handoff-rtf.sh docs/handoff-neu.md /projekt/handoff-neu.rtf --project-root /projekt` |
| [`handoff-inputs.py`](scripts/handoff-inputs.py) | Momentaufnahme der gespeicherten Quellen mit Hash und Zeitpunkt, bevor gelesen und geschrieben wird | `python3 scripts/handoff-inputs.py …` |
| [`sammlung-pruefen.sh`](scripts/sammlung-pruefen.sh) | **Pflichtschritt vor dem Finalisieren:** vergleicht die `>>>`-Zeilen der Vorgänger mit dem neuen Handoff und nennt, was fehlt | `scripts/sammlung-pruefen.sh docs/handoff-neu.md [vorgaenger1.md] [vorgaenger2.md]` |

Für die offene Zwischenrufe-Datei zusätzlich
[`zwischenrufe-antwort.sh`](scripts/zwischenrufe-antwort.sh): **nur anhängen**,
nie mittendrin schreiben, nie ungefragt schließen.

`sammlung-pruefen.sh` ist eine Heuristik, kein Vollständigkeitsbeweis. Antworten
außerhalb erkannter Abschnitte zusätzlich Punkt für Punkt abgleichen.

## 4. Der RTF-Zwilling

Das Markdown ist die Agentenquelle, die **RTF ist die Datei, in der Yasin
antwortet**. Vollständig in [RTF unter macOS](references/rtf-macos.de.md).

- RTF **immer** über `scripts/handoff-rtf.sh` erzeugen. Direktes `textutil` dient
  nur dem Lesen und Prüfen, nie dem Erzeugen.
- Der Renderer **verweigert jedes vorhandene Ziel**, auch Symlinks. Eine neue
  Version bekommt einen neuen Dateinamen; die beantwortete Datei bleibt unberührt.
- `--project-root` angeben, wenn die Projektwurzel bekannt ist.
- Pfade mit Leerzeichen als `[Label](<docs/Fragen an Yasin.md>)`, in Backticks
  oder als `⟦Screenshot: /absoluter/Pfad mit Leerzeichen.png⟧`.
- **Gold ist Pflicht, und zwar auch für den Dokumentstandard.** `>>>`-Absätze und
  `user-original`-Blöcke sind golden; darüber hinaus ist der Dokumentstandard
  selbst 18 pt Gold, damit **eingefügter (Cmd-V) und getippter Text** im
  Antwortfeld ebenfalls 18 pt Gold ist und nicht auf 12 pt ohne Farbe zurückfällt.
  Agententext, Überschriften und Codeblöcke setzen mit `\pard\plain\f0` zurück.
  Dieselbe Goldregel gilt für die **Zwischenrufe-RTF**, nicht nur für den Handoff.
- **Hinter `>>>` eingefügter Text ist schwarz auf Gold, 18 pt** (Beleg W58-E1,
  13.09.2026). Farbtabelle `;gold;schwarz;`; der goldene Zeichenzustand ist
  `\cb1\cbpat1\chshdng0\chcbpat1\highlight1\cf2`, der Reset `\plain\f0\cf2`,
  Antwortabsätze werden als `RESET + \fs36 + GOLD` geschrieben (`\fs36` = 18 pt).
  Nur `\chshdng0\chcbpat1` färbt in Cocoa auf Zeichenebene, `\cf2` hält
  Nutzertext schwarz, und `\cb0` würde als Schwarz gelesen — nie als Reset
  verwenden. Wer RTF selbst erzeugt statt `scripts/handoff-rtf.sh` zu rufen, muss
  genau diese Steuerworte schreiben.
- **Beantwortete Handoffs nach `handoff-archiv/`** des Projekts ablegen
  (`mv`, nie `rm`; Yasin 13.09.2026 03:31).
- Nach dem Erzeugen `grep -c "file://" DATEI.rtf`: > 0, sobald das Dokument
  lokale Verweise enthält.
- Textroundtrip und HYPERLINK-Prüfung laufen automatisch. Sie belegen **nicht**
  Lesbarkeit, Linkklicks oder das Verhalten beim Einfügen in eine fremde
  Anwendung — diese drei Beleggrenzen sauber trennen und Offenes offen nennen.
- Regressionen: `TMPDIR=/tmp python3 -m unittest discover -s tests -v`.

## 5. Vor der Übergabe

- `sammlung-pruefen.sh` gelaufen und sauber.
- Alle Quellen erneut auf Nachträge geprüft, Originale Punkt für Punkt abgeglichen.
- Lokale Links geprüft; echte Commit-/Push-Belege im Bericht, keine erfundenen Hashes.
- Nur eigene Pfade geändert.
- Bei Wellenarbeit: eigene Warteschleifen und Hintergrundprozesse beendet, teure
  Builds hinter dem gemeinsamen Projekt-Lock, ein Build je Themen-Wächter ganz am
  Ende. Siehe [Wellen-Ausführung](references/wave-execution.de.md).
- Offene Reste ausdrücklich benannt, statt sie stillschweigend als erledigt zu führen.
