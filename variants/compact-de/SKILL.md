---
name: warm-handoff-de
description: Erhält Nutzereingaben und belegten Arbeitsstand über Pausen hinweg, setzt sicher fort und führt ausdrücklich autorisierte Arbeitswellen mit providerneutralen Belegen und Dateibesitz aus.
---

# Warm Handoff

Nutze diesen kurzen Einstieg für Routinearbeit. Lies nur die Referenz, die für den aktuellen Schritt nötig ist. Nutze die getrennt installierte Variante `warm-handoff-full-de`, wenn du den gesamten Ablauf erklärst, einführst oder prüfst.

<!-- rule:WH-01 -->
## 1. Umfang feststellen

Behandle das jüngste gespeicherte Handoff und spätere Nachrichten des Nutzers als einen geordneten Eingangsstrom. Lies zuerst die Projektregeln, bestimme die benannten Quellen und Feedbackdateien und halte den autorisierten Umfang, verbotene Aktionen, Dateibesitz und erforderliche Belege fest. Ein Handoff dokumentiert Absicht; es erteilt keine Rechte, die der Nutzer nicht gegeben hat.

Wähle genau einen Host-Adapter: [Codex](references/codex.de.md) oder [Claude Code](references/claude-code.de.md). Halte die Kernregeln providerneutral.

<!-- rule:WH-02 -->
## 2. Verlustfrei fortsetzen

Lies die vollständige gespeicherte Quelle einschließlich eingebetteter oder angehängter Nutzertexte. Erhalte Nutzeroriginale wörtlich und schreibe Deutungen oder Antworten in getrennte Abschnitte. Gleiche späte Ergänzungen vor dem Handeln ab. Prüfe Repository-Stand und Erledigt-Aussagen anhand von Dateien, Git-Stand, Tests oder anderen direkten Belegen; kennzeichne alles andere als unbekannt.

Für Dokumentvertrag und Pflichtabschnitte lies [Handoff-Format](references/handoff-format.de.md).

### Handoff schreiben: drei Stopp-Regeln (14.09.2026)

1. **Referenz zuerst öffnen.** `references/handoff-format.de.md` vollständig lesen, bevor du schreibst — dort steht die verbindliche 17-teilige Abschnittsfolge (HF-06). „Ich kenne das Format" zählt nicht.
2. **Vorgänger ungefiltert lesen.** Erste bis letzte Zeile. Nie Zeilen abschneiden, nie nur nach `>>>Userantwort:` greppen, nie „zum Token-Sparen" filtern — so gehen roter Faden, Roadmap, Messung, Gedächtnis und Logbuch verloren.
3. **Nicht warten, abschließen.** Am Wellenende nicht auf eine weitere Agentenmeldung warten; offene Meldungen kommen unter „Laufend und offen".


<!-- rule:WH-03 -->
## 3. Innerhalb der Autorisierung arbeiten

Arbeite weiter, bis das autorisierte Ergebnis vollständig ist. Teile unabhängige Arbeit nur auf, wenn Host und Auftrag es erlauben. Gib jedem Arbeiter exklusive Pfade und Akzeptanzkriterien; überschreite nie die tatsächliche Parallelkapazität. Wächter sind optionale Koordinatoren und keine Standardschicht. Serialisiere gemeinsam genutzte Ressourcen und begrenze Builds auf die zwei Slots von Regel 4 v2.

### Regel 4 v2 — höchstens ZWEI Builds gleichzeitig (13.09.2026)

Jeder Themen-Wächter baut EINMAL am Ende seines Themas mit gezielten Tests; die
Vollsuite gehört dem Merge-Wächter. Zwei Slot-Locks, größtes Thema zuerst, warten
im Vordergrund, Arbeiter bauen nicht. Details und Slot-Lock-Block stehen in
[Wellen-Ausführung](references/wave-execution.de.md).

Für die Ausführung lies [Wellen-Ausführung](references/wave-execution.de.md). Für Modellwahl und veränderliche Plattformfakten lies [Modellrouting](references/model-routing.de.md) und [Beleggrenzen](references/evidence-scope.de.md).

<!-- rule:WH-04 -->
## 4. Dokumentsicherheit erhalten

Überschreibe nie ein beantwortetes Nutzer-Handoff. Schreibe eine neue Markdown-Quelle und auf Wunsch unter macOS einen neuen editierbaren RTF-Zwilling. Prüfe Textroundtrip und Linkfelder vor der Veröffentlichung. Die Rendererprüfung belegt weder die Fortsetzung in TextEdit noch das Einfügen in eine Anwendung; prüfe diese Aussagen getrennt.

Hinter `>>>` eingefügter oder getippter Text muss schwarz auf Gold in 18 pt bleiben: Farbtabelle `;gold;schwarz;`, Goldzustand `\cb1\cbpat1\chshdng0\chcbpat1\highlight1\cf2`, Reset `\plain\f0\cf2`, Antwortabsätze `RESET + \fs36 + GOLD` (`\fs36` = 18 pt; Beleg W58-E1, 13.09.2026). Beantwortete Handoffs nach `handoff-archiv/` des Projekts ablegen (`mv`, nie `rm`; Yasin 13.09.2026 03:31).

### Ein einziger Eingang, zeitlich getrennt (14.09.2026)

Zwischen Handoff und Wellenstart ist das Handoff der einzige Eingang (`SAMMLUNG FÜR DAS NÄCHSTE HANDOFF` plus die `>>>Userantwort:`-Zeilen); die Zwischenrufe-Datei existiert dann **nicht** und wird nicht zusammen mit dem Handoff angelegt (Yasin 14.09.2026). Erst mit dem Wellenstart legst du sie an, öffnest sie in TextEdit, und sie ist bis zum nächsten Handoff der einzige Eingang. Dieselbe Goldregel gilt dort für jede Nutzerzeile. Kurzes beantwortest du sofort, Längeres planst du mit Notiz in die nächste Welle.

Lies [RTF unter macOS](references/rtf-macos.de.md), bevor du renderst oder Dokumente öffnest.

Erzeuge Handoff- und Zwischenrufe-RTFs ausschließlich über `scripts/handoff-rtf.sh` aus dem Skillverzeichnis. Halte genau einen aktiven Zwischenrufe-Eingang: Handoff-Fußbereich oder vereinbarte Datei; der andere Ort verlinkt nur darauf. Cmd-S gibt gespeicherte Eingaben innerhalb der bestehenden Autorisierung frei.

<!-- rule:WH-05 -->
## 5. Optionale Hilfen bewusst einsetzen

[Context Mode](references/context-mode.de.md) kann große Befehls- und Dateiausgaben verkleinern. Behandle Paketinstallation, MCP-Erreichbarkeit und Hook-Wirkung als getrennte Zustände. Installiere es nie ohne Erlaubnis.

<!-- rule:WH-06 -->
## 6. Mit Belegen abschließen

Lies vor dem Abschluss die benannte Feedbackquelle erneut, prüfe den Status, führe die geforderten zielgerichteten Prüfungen aus und bestätige, dass nur eigene Pfade geändert wurden. Berichte erledigte, offene und laufende Arbeit mit Belegen und nächstem Schritt. Schreibe den geforderten dauerhaften Bericht vor einer kurzen Chatantwort.

### Zwischenrufe-Datei bei jedem Aufwachen prüfen (13.09.2026)

Regel des Nutzers vom 13.09.2026 (05:17): Bei jedem Aufwachen der Hauptsession — Meldung eines Arbeiters oder Wächters, Zeitgeber, fortgesetzter Zug — die Änderungszeit der benannten Zwischenrufe-Datei mit dem Zeitpunkt des letzten Lesens vergleichen. Geändert: die gespeicherten Ergänzungen lesen, bevor gehandelt oder gemeldet wird. Unverändert: nicht öffnen. Nur gespeicherter Stand; Cmd-S des Nutzers ist die Freigabe.

Die spanische Übersetzung ist zurückgestellt. Audio, Video und Website-Material gehören nicht zu diesem Skill.
