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

Drei Stopp-Regeln, wenn du ein Handoff schreibst:

1. **Referenz zuerst öffnen.** Lies [Handoff-Format](references/handoff-format.de.md) vollständig; dort stehen der Dokumentvertrag und die verbindliche Abschnittsfolge. „Ich kenne das Format" zählt nicht.
2. **Vorgänger ungefiltert lesen,** erste bis letzte Zeile. Nie abschneiden, nie nur nach Antwortmarken greppen, nie zum Token-Sparen filtern — so gehen roter Faden, Roadmap, Messung, Gedächtnis und Logbuch verloren.
3. **Nicht warten, abschließen.** Halte eine Welle nicht für eine weitere Agentenmeldung offen; offene Meldungen kommen unter „Laufend und offen".

<!-- rule:WH-03 -->
## 3. Innerhalb der Autorisierung arbeiten

Arbeite weiter, bis das autorisierte Ergebnis vollständig ist. Teile unabhängige Arbeit nur auf, wenn Host und Auftrag es erlauben. Gib jedem Arbeiter exklusive Pfade, Akzeptanzkriterien und ausdrückliche Dateigrenzen; überschreite nie die tatsächliche Parallelkapazität. Wächter sind optionale Koordinatoren und keine Standardschicht. Serialisiere gemeinsam genutzte Ressourcen.

Builds sind die knappe Ressource, und die Grenze ist der Speicher, nicht die Zahl der Agenten: **ein Bau gleichzeitig**, mit der Sperre im Testskript des Projekts statt im Auftrag eines Arbeiters — ein Auftrag ist eine Bitte, ein Skript ist ein Tor. Ein Abschlussbau zählt nur, wenn er die Tests erreicht hat; ein Lauf, der vorher abbricht, wird wiederholt, und wer danach noch etwas ändert, baut erneut. Baue im Vordergrund, begrenze die Zahl gleichzeitiger Arbeiter und fahre einen Rauchtest, bevor der erste Arbeiter startet.

Vorflug-Listen, Slot-Sperre, Arbeiteraufträge und Wellen-Choreografie stehen in [Wellen-Ausführung](references/wave-execution.de.md). Für Modellwahl und veränderliche Plattformfakten lies [Modellrouting](references/model-routing.de.md) und [Beleggrenzen](references/evidence-scope.de.md).

<!-- rule:WH-04 -->
## 4. Dokumentsicherheit erhalten

Überschreibe nie ein beantwortetes Nutzer-Handoff. Schreibe eine neue Markdown-Quelle und auf Wunsch unter macOS einen neuen editierbaren RTF-Zwilling. Prüfe Textroundtrip und Linkfelder vor der Veröffentlichung. Die Rendererprüfung belegt weder die Fortsetzung im Editor noch das Einfügen in eine Anwendung; prüfe diese Aussagen getrennt.

Hinter `>>>` eingefügter oder getippter Text muss schwarz auf Gold in 18 pt bleiben; die genauen Steuerworte stehen in [RTF unter macOS](references/rtf-macos.de.md). Lege ein neues Handoff direkt im Archivordner des Projekts an und verschiebe es danach nie — jedes Verschieben bricht einen Pfad, unter dem das Dokument schon verlinkt war; beantwortete Handoffs wandern per `mv` dorthin, nie per `rm`. Jedes Dokument beginnt mit seinem eigenen absoluten Pfad als erster Zeile, darunter das Stand-Datum. Änderst du ein Dokument, das der Nutzer offen haben könnte, schließe und öffne es für ihn — aber fasse nie Ungespeichertes an.

Halte genau einen Eingang, zeitlich getrennt durch die Wellenuhr: Zwischen Handoff und Wellenstart ist das Handoff der einzige Eingang; die Zwischenrufe-Datei entsteht mit dem Wellenstart und ist bis zum nächsten Handoff der einzige Eingang. Kurzes beantwortest du sofort, Längeres planst du in die nächste Welle.

Lies [RTF unter macOS](references/rtf-macos.de.md), bevor du renderst oder Dokumente öffnest. Erzeuge Handoff- und Zwischenrufe-Zwillinge ausschließlich über `scripts/handoff-rtf.sh` aus dem Skillverzeichnis. Cmd-S gibt gespeicherte Eingaben innerhalb der bestehenden Autorisierung frei.

<!-- rule:WH-05 -->
## 5. Optionale Hilfen bewusst einsetzen

[Context Mode](references/context-mode.de.md) kann große Befehls- und Dateiausgaben verkleinern. Behandle Paketinstallation, MCP-Erreichbarkeit und Hook-Wirkung als getrennte Zustände. Installiere es nie ohne Erlaubnis.

<!-- rule:WH-06 -->
## 6. Mit Belegen abschließen

Lies vor dem Abschluss die benannte Feedbackquelle erneut, prüfe den Status, führe die geforderten zielgerichteten Prüfungen aus und bestätige, dass nur eigene Pfade geändert wurden. Berichte erledigte, offene und laufende Arbeit mit Belegen und nächstem Schritt. Schreibe den dauerhaften Bericht vor der kurzen Chatantwort. Nimm jeden Zeitstempel aus der Systemuhr, nie aus einer Schätzung.

Bei jedem Aufwachen der Hauptsession — Meldung eines Arbeiters, Zeitgeber, fortgesetzter Zug — vergleiche die Änderungszeit der benannten Zwischenrufe-Datei mit dem letzten Lesen. Geändert: die gespeicherten Ergänzungen lesen, bevor gehandelt oder gemeldet wird. Unverändert: geschlossen lassen. Nur gespeicherter Stand; das Speichern des Nutzers ist die Freigabe. Nie die Datei selbst überwachen: kein Monitor, kein Dateiwächter, kein Speicher-Hook darf die Session wecken, weil der Nutzer Cmd-S gedrückt hat — Speichern ist keine Anfrage und darf nichts kosten (Nutzerregel vom 23.09.2026). Nur bei einem ohnehin stattfindenden Aufwachen lesen.

Eine saubere Welle schließt du ohne Rückfrage ab: Alle Arbeiter fertig und Vollsuite grün heißt bauen, tauschen, veröffentlichen und das Handoff schreiben. Gefragt wird nur beim unsauberen Abschluss — rote Tests, ungeklärter Befund, blockiert gemeldeter Arbeiter —; dann nennst du, was fehlt, und schlägst den nächsten Schritt vor.

Die spanische Übersetzung ist zurückgestellt. Audio, Video und Website-Material gehören nicht zu diesem Skill.
