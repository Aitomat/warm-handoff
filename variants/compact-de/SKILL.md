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

<!-- rule:WH-03 -->
## 3. Innerhalb der Autorisierung arbeiten

Arbeite weiter, bis das autorisierte Ergebnis vollständig ist. Teile unabhängige Arbeit nur auf, wenn Host und Auftrag es erlauben. Gib jedem Arbeiter exklusive Pfade und Akzeptanzkriterien; überschreite nie die tatsächliche Parallelkapazität. Wächter sind optionale Koordinatoren und keine Standardschicht. Serialisiere Builds und gemeinsam genutzte Ressourcen.

Für die Ausführung lies [Wellen-Ausführung](references/wave-execution.de.md). Für Modellwahl und veränderliche Plattformfakten lies [Modellrouting](references/model-routing.de.md) und [Beleggrenzen](references/evidence-scope.de.md).

<!-- rule:WH-04 -->
## 4. Dokumentsicherheit erhalten

Überschreibe nie ein beantwortetes Nutzer-Handoff. Schreibe eine neue Markdown-Quelle und auf Wunsch unter macOS einen neuen editierbaren RTF-Zwilling. Prüfe Textroundtrip und Linkfelder vor der Veröffentlichung. Die Rendererprüfung belegt weder die Fortsetzung in TextEdit noch das Einfügen in eine Anwendung; prüfe diese Aussagen getrennt.

Lies [RTF unter macOS](references/rtf-macos.de.md), bevor du renderst oder Dokumente öffnest.

<!-- rule:WH-05 -->
## 5. Optionale Hilfen bewusst einsetzen

[Context Mode](references/context-mode.de.md) kann große Befehls- und Dateiausgaben verkleinern. Behandle Paketinstallation, MCP-Erreichbarkeit und Hook-Wirkung als getrennte Zustände. Installiere es nie ohne Erlaubnis.

<!-- rule:WH-06 -->
## 6. Mit Belegen abschließen

Lies vor dem Abschluss die benannte Feedbackquelle erneut, prüfe den Status, führe die geforderten zielgerichteten Prüfungen aus und bestätige, dass nur eigene Pfade geändert wurden. Berichte erledigte, offene und laufende Arbeit mit Belegen und nächstem Schritt. Schreibe den geforderten dauerhaften Bericht vor einer kurzen Chatantwort.

Die spanische Übersetzung ist zurückgestellt. Audio, Video und Website-Material gehören nicht zu diesem Skill.
