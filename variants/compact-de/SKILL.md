---
name: warm-handoff-de
description: Handoff, Welle, Zwischenrufe und sichere Wiederaufnahme. Nutzen beim Sessionstart, wenn der Nutzer „Handoff", „Welle", „Zwischenrufe", „weiter", „Sessionstart" sagt, ein gespeichertes Handoff (.md/.rtf) übergibt oder vor einer Pause; erhält Nutzereingaben wörtlich, führt ausdrücklich autorisierte Arbeitswellen mit Dateibesitz und providerneutralen Belegen aus und schreibt das nächste Handoff.
---

# Warm Handoff

Kurzer Einstieg für Routinearbeit: Lies nur die Referenz, die der aktuelle Schritt braucht. Nutze die getrennt installierte Variante `warm-handoff-full-de`, wenn du den gesamten Ablauf erklärst, einführst oder prüfst.

## Dauerregeln (jeder Zug, nicht einmalig)

1. Die erste Antwort auf jede neue Nutzernachricht beginnt mit `Name, TT.MM.JJJJ-HH:MM` aus `date "+%d.%m.%Y-%H:%M"` — nie geschätzt, auch nach Zwischenrufen (HF-09). Ein `UserPromptSubmit`-Hook kann die Uhrzeit liefern.
2. Nur gespeicherten Stand lesen; Cmd-S des Nutzers gibt gespeicherte Eingaben innerhalb der bestehenden Autorisierung frei. Nie Ungespeichertes im Editor speichern, schließen oder anfassen.
3. Nie ein beantwortetes Handoff überschreiben; nie `rm` — per `mv` archivieren.
4. Jedes Dokument beginnt mit seinem eigenen absoluten Pfad als erster Zeile, darunter das Stand-Datum.
5. Ein Handoff dokumentiert Absicht; es erteilt keine Rechte, die der Nutzer nicht gegeben hat.

<!-- rule:WH-01 -->
## 1. Umfang feststellen

Lies zuerst die Projektregeln (`AGENTS.md`, die eine gemeinsame Anweisungsdatei für alle Agenten, Claude Code eingeschlossen), dann behandle das jüngste gespeicherte Handoff und spätere Nachrichten als einen geordneten Eingangsstrom. Bestimme die benannten Quell- und Feedbackdateien; halte autorisierten Umfang, verbotene Aktionen, Dateibesitz und erforderliche Belege fest. Wähle genau einen Host-Adapter: [Codex](references/codex.de.md) oder [Claude Code](references/claude-code.de.md); halte die Kernregeln providerneutral.

<!-- rule:WH-02 -->
## 2. Verlustfrei fortsetzen

Lies die vollständige gespeicherte Quelle einschließlich eingebetteter oder angehängter Nutzertexte. Erhalte Nutzeroriginale wörtlich; Deutungen und Antworten kommen in getrennte Abschnitte. Gleiche späte Ergänzungen vor dem Handeln ab. Prüfe Repository-Stand und Erledigt-Aussagen anhand von Dateien, Git, Tests oder anderen direkten Belegen; kennzeichne den Rest als unbekannt.

Drei Stopp-Regeln, wenn du ein Handoff schreibst:

1. **Referenz zuerst öffnen.** Lies [Handoff-Format](references/handoff-format.de.md) vollständig (Dokumentvertrag, verbindliche Abschnittsfolge). „Ich kenne das Format" zählt nicht.
2. **Vorgänger ungefiltert lesen,** erste bis letzte Zeile. Nie abschneiden, nie nur nach Antwortmarken greppen, nie zum Token-Sparen filtern.
3. **Nicht warten, abschließen.** Halte eine Welle nie für eine weitere Agentenmeldung offen; offene Meldungen kommen unter „Laufend und offen".

<!-- rule:WH-03 -->
## 3. Innerhalb der Autorisierung arbeiten

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

Arbeite weiter, bis das autorisierte Ergebnis vollständig ist; teile unabhängige Arbeit nur auf, wenn Host und Auftrag es erlauben. In der Welle neue Nutzerfragen, die du selbst beantworten kannst, sofort beantworten (Chat plus Zwischenrufe-Datei), späte Zwischenrufe als Nachtrag oder Folgeauftrag einordnen und einen Platz als Kleine-Aufgaben-Spur führen (WV-13). Gib jedem Arbeiter exklusive Pfade, Akzeptanzkriterien und ausdrückliche Dateigrenzen; überschreite nie die tatsächliche Parallelkapazität. Wächter sind optional, keine Standardschicht. Serialisiere gemeinsam genutzte Ressourcen.

Ein Bau gleichzeitig, mit Sperre im Projekt-Testskript, im Vordergrund; vor dem ersten Arbeiter ein Rauchtest. Nur ein bis zu den Tests gelangter Abschlussbau zählt; nach späteren Änderungen erneut prüfen.

Vorflug-Listen, Slot-Sperre, Arbeiteraufträge, Choreografie: [Wellen-Ausführung](references/wave-execution.de.md). Modellwahl und veränderliche Plattformfakten: [Modellrouting](references/model-routing.de.md), [Beleggrenzen](references/evidence-scope.de.md).

<!-- rule:WH-04 -->
## 4. Dokumentsicherheit erhalten

Schreibe eine neue Markdown-Quelle und auf Wunsch unter macOS einen neuen editierbaren RTF-Zwilling — ausschließlich über `scripts/handoff-rtf.sh` aus dem Skillverzeichnis; lies [RTF unter macOS](references/rtf-macos.de.md), bevor du renderst oder Dokumente öffnest. Prüfe Textroundtrip und Linkfelder vor der Veröffentlichung. Text hinter `>>>` bleibt schwarz auf Gold in 18 pt.

Lege ein neues Handoff direkt im Archivordner des Projekts an und verschiebe es danach nie — jedes Verschieben bricht einen Pfad, unter dem es schon verlinkt war. RTFs bleiben dort dauerhaft (HF-10). Änderst du ein Dokument, das der Nutzer offen haben könnte, schließe und öffne es für ihn — nur ohne ungespeicherte Eingaben.

Bis zum Wellenstart ist der Handoff-Fuß der einzige Eingang. Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und in einem Editor öffnen, in den der Nutzer schreiben kann (macOS: `open -a TextEdit "<voller Pfad>"`, nie in einem reinen Lese-Viewer wie dem cmux-Markdown-Tab), nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Antworten in dieselbe Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen. Nach HF-07.

<!-- rule:WH-05 -->
## 5. Optionale Hilfen bewusst einsetzen

[Context Mode](references/context-mode.de.md) kann große Befehls- und Dateiausgaben verkleinern. Installiere es nie ohne Erlaubnis.

<!-- rule:WH-06 -->
## 6. Mit Belegen abschließen

Lies vor dem Abschluss die benannte Feedbackquelle erneut, prüfe den Status, führe die geforderten zielgerichteten Prüfungen aus und bestätige, dass nur eigene Pfade geändert wurden. Berichte erledigte, offene und laufende Arbeit mit Belegen und nächstem Schritt. Schreibe den dauerhaften Bericht vor der kurzen Chatantwort; jeden Zeitstempel aus `date`.

Bei jedem Aufwachen der Hauptsession — Meldung eines Arbeiters, Zeitgeber, fortgesetzter Zug — vergleiche die Änderungszeit der Zwischenrufe-Datei mit dem letzten Lesen. Geändert: die gespeicherten Ergänzungen lesen, bevor gehandelt oder gemeldet wird. Unverändert: geschlossen lassen. Nie die Datei überwachen: kein Monitor, kein Dateiwächter, kein Speicher-Hook — Speichern ist keine Anfrage und darf nichts wecken (Nutzerregel vom 23.09.2026).

Eine saubere Welle schließt du ohne Rückfrage ab: Alle Arbeiter fertig und Vollsuite grün heißt bauen, tauschen, veröffentlichen und das Handoff schreiben. Gefragt wird nur beim unsauberen Abschluss — rote Tests, ungeklärter Befund, blockiert gemeldeter Arbeiter —; dann nennst du, was fehlt, und schlägst den nächsten Schritt vor.
