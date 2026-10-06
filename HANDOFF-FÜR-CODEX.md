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

## 0. Harte Regeln — jedes Kästchen abhaken

Genau diese Punkte hat ein Codex-Chef schon übersprungen. Die Checkliste steht im
[Codex-Adapter](references/codex.de.md) (Regel CDX-05); kurz:

- [ ] Zeitstempel aus `date`, nie geschätzt.
- [ ] Erste Zeile = absoluter Pfad des Dokuments, zweite Zeile = Stand.
- [ ] Neues Handoff direkt im Archivordner; nie verschieben, nie ein beantwortetes überschreiben.
- [ ] Ein Eingang: bis Wellenstart der Handoff-Fuß, danach die Zwischenrufe-Datei.
- [ ] Zuerst das [Handoff-Format](references/handoff-format.de.md) vollständig öffnen.
- [ ] Den Vorgänger ungefiltert lesen, erste bis letzte Zeile.
- [ ] Bündel am Wellenende: bauen, installieren, pushen, Handoff — in einem Durchgang.

## 1. Vorher lesen — vollständig, nicht geraten

- Den **benannten** Vorgänger-Handoff, nicht den mit dem neuesten Änderungsdatum.
- Die RTF-Antworten: `textutil -convert txt -stdout DATEI.rtf`.
- Die Zwischenrufe-Datei und die Chat-Steuerung.
- **Nur der gespeicherte Stand zählt. Cmd-S ist die Freigabe innerhalb bestehender Autorisierung.** Was in einem
  Editor ungespeichert offen liegt, ist nicht gelesen: entweder um das Speichern
  bitten oder die Lücke im Handoff ausdrücklich als Lücke benennen. Niemals die
  Antwortdatei des Nutzers zum Einlesen speichern, schließen oder neu erzeugen.
- `[Pasted text]` / `Pasted Content` ist **kein Inhalt**. Die zugehörige Datei
  öffnen; fehlt sie, den Eingang ausdrücklich offenlassen.
- Nutzeroriginale wörtlich übernehmen; Deutung und Antwort in eigene Abschnitte.
- **Ungefiltert lesen (14.09.2026).** Den Vorgänger-Handoff von der ersten bis
  zur letzten Zeile lesen. Nie lange Zeilen abschneiden, nie nur nach
  `>>>Userantwort:` greppen, nie „zum Token-Sparen" filtern — genau so sind
  roter Faden, Roadmap, Messung, Hauptdokumente, Gedächtnis und Logbuch schon
  einmal aus der Nachfolgerevision verschwunden. Zu große Dateien in Blöcken
  lesen, aber vollständig.
- **Die Referenz öffnen**, bevor geschrieben wird: `references/handoff-format.de.md`
  im Skill-Repo (Regeln HF-05 und HF-06). „Ich kenne das Format" zählt nicht.

## 2. Die Pflichtblöcke — in dieser Reihenfolge

1. **Kopf:** Zeile 1 der eigene absolute Pfad, Zeile 2 `Stand:` aus `date`,
   danach die **Kopierzeile** als eine ungeteilte Zeile:
   `Ich habe das Handoff bearbeitet: /absoluter/Pfad/zur/neuen.rtf`
   Danach Titel **mit der eigenen Kennung** (Dateiname `…-r.md` → Titel nennt `r`), gemessene Zeit mit Zeitzone, Vorgänger, Hinweis auf `>>>`-Felder.
2. **Der Stand in drei Sätzen** — Ziel, überprüfter Stand, nächste Aktion; dazu
   Modus (Zwischenstand / fortsetzbar / abgeschlossen) und gültige Autorisierung.
3. **Was noch im Tank ist** — Messquelle, Alter, Umfang; sonst „nicht gemessen".
4. **Erwartete Agenten-Ergebnisse** — ID, Besitzer, beobachteter Status,
   Worktree/Branch/Basis, Berichtspfad, bekannte Laufzeitgrenzen.
5. **Neue Nutzereingaben seit dem Vorgänger (wörtlich, HF-08)** und
   **Was ich daraus gemacht habe** — jedes neue Original mit Status und Beleg. Ältere Originale bleiben per Verweis im archivierten Vorgänger; jeder noch offene ältere Wunsch steht mit Quelle unter „Laufend und offen“.
6. **Vorige Testantworten — was daraus wurde** und **Testliste vN** mit leeren
   `>>>Userantwort:`-Feldern. Kein offener Test gilt als bestanden.
7. **Fragen an dich** mit `>>>Antwort:`; optionale Fragen getrennt von den
   Entscheidungen, die den nächsten Schritt wirklich sperren.
8. **Der rote Faden**, **Kurz-Roadmap**, **Messung der Welle** (Zahlen, was
   schiefging, was es gekostet hat, Lehren), **Hauptdokumente**, **Weitere
   Dokumente**, **Aktive Werkzeuge dieses Projekts** — echte Pfade, tatsächliche
   Verfügbarkeit.
9. **Gedächtnis** — je vier bis sechs konkrete Lang- und Kurzzeitpunkte.
10. **Kostentabelle** — Quelle, Alter, Haupt-/Arbeiteranteile, Messlücken.
10b. **Logbuch** — was in dieser Welle tatsächlich passiert ist, mit Zeitstempeln.
11. Ganz zuletzt **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit Ursprungspfad und `>>>`.

**Genau EIN aktiver Sammlungs- bzw. Zwischenrufe-Abschnitt**, und er wechselt
mit dem Wellentakt (Yasin 14.09.2026): Zwischen Handoff und Wellenstart ist der
RTF-Fußbereich `SAMMLUNG FÜR DAS NÄCHSTE HANDOFF` der einzige Eingang — die
Zwischenrufe-Datei wird **nicht** zusammen mit dem Handoff angelegt. Erst beim
Wellenstart entsteht sie und ist dann bis zum nächsten Handoff der einzige
Eingang. Zwei parallele Eingänge haben schon Antworten verschluckt.

**Nicht warten, abschließen.** Am Wellenende nicht auf eine weitere
Agentenmeldung warten: Handoff schreiben, öffnen, pushen, melden. Offene
Meldungen stehen unter „Laufend und offen"; sie halten den Abschluss nicht auf.

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und öffnen, nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

## 3. Die vier Skripte

Immer benutzen, nie von Hand nachbauen.

| Skript | Wofür | Aufruf |
| --- | --- | --- |
| [`handoff-rtf.sh`](scripts/handoff-rtf.sh) | Markdown → RTF-Zwilling: klickbare Linkfelder, 18 pt, goldene Antwortabsätze | `scripts/handoff-rtf.sh docs/handoff-neu.md /projekt/handoff-neu.rtf --project-root /projekt` |
| [`handoff-inputs.py`](scripts/handoff-inputs.py) | Momentaufnahme der gespeicherten Quellen mit Hash und Zeitpunkt, bevor gelesen und geschrieben wird | `python3 scripts/handoff-inputs.py …` |
| [`handoff-pruefen.py`](scripts/handoff-pruefen.py) | **Pflichtschritt vor und nach dem Rendern:** Pfad- und Standzeile, Kennung im Titel, Kopierzeile, Selbstverweise im Kopf, Abschnittsfolge HF-06; mit RTF-Zwilling auch dessen Kopf | `python3 scripts/handoff-pruefen.py docs/handoff-neu.md` |
| [`sammlung-pruefen.sh`](scripts/sammlung-pruefen.sh) | **Pflichtschritt vor dem Finalisieren:** verlangt den letzten Sammlungsfuß des direkten Vorgängers wörtlich, prüft den Verweis auf dessen Antwortfelder und meldet wörtlich wiederholte Antworten (HF-08) | `scripts/sammlung-pruefen.sh docs/handoff-neu.md [vorgaenger.rtf]` — beantwortete Vorgänger als gespeichertes RTF übergeben |

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
- Hinter `>>>` bleibt eingefügter und getippter Text schwarz auf Gold in 18 pt, einschließlich Fortsetzung und Dokumentstandard. Agententext setzt den Hintergrund zurück; die exakten Steuerworte und Beleggrenzen stehen in RT-03/RT-03b der oben verlinkten RTF-Referenz. Zwischenrufe bleiben `.md`.
- **Beantwortete Handoffs nach `handoff-archiv/`** des Projekts ablegen
  (`mv`, nie `rm`; Yasin 13.09.2026 03:31).
- Nach dem Erzeugen `grep -c "file://" DATEI.rtf`: > 0, sobald das Dokument
  lokale Verweise enthält.
- Textroundtrip und HYPERLINK-Prüfung laufen automatisch. Sie belegen **nicht**
  Lesbarkeit, Linkklicks oder das Verhalten beim Einfügen in eine fremde
  Anwendung — diese drei Beleggrenzen sauber trennen und Offenes offen nennen.
- Regressionen: `TMPDIR=/tmp python3 -m unittest discover -s tests -v`.

## 5. Vor der Übergabe

- `handoff-pruefen.py` und `sammlung-pruefen.sh` gelaufen und sauber.
- Alle Quellen erneut auf Nachträge geprüft, Originale Punkt für Punkt abgeglichen.
- Lokale Links geprüft; echte Commit-/Push-Belege im Bericht, keine erfundenen Hashes.
- Nur eigene Pfade geändert.
- Bei Wellenarbeit: eigene Warteschleifen und Hintergrundprozesse beendet, teure
  Builds hinter dem gemeinsamen Projekt-Lock, ein Build je Themen-Wächter ganz am
  Ende. Siehe [Wellen-Ausführung](references/wave-execution.de.md).
- Offene Reste ausdrücklich benannt, statt sie stillschweigend als erledigt zu führen.
