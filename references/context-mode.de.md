# Optionaler Context Mode

<!-- rule:CM-01 -->
## Zweck

Context Mode kann große Dateien, Logs, Befehlsausgaben und strukturierte Daten verarbeiten und ein gezieltes Ergebnis zurückgeben. Nutze ihn, wenn die Rohdaten wesentlichen Kontext verbrauchen würden. Kleine feste Ausgaben und Dateiänderungen gehören weiter in die normalen Hostwerkzeuge.

<!-- rule:CM-02 -->
## Drei unabhängige Zustände

Prüfe und berichte getrennt:

1. **Paket installiert:** Dateien sind in der konfigurierten Umgebung vorhanden.
2. **MCP erreichbar:** Ein Context-Mode-Werkzeug ist in dieser Sitzung aufrufbar.
3. **Hooks wirksam:** Erwartete Erfassungs- oder Indexierungs-Hooks sind registriert und arbeiten.

Kein Zustand belegt einen anderen. Nutze das Diagnosewerkzeug des Plugins, wenn vorhanden; kennzeichne sonst ungeprüfte Zustände als unbekannt.

<!-- rule:CM-03 -->
## Berechtigungsgrenze

Installiere, aktualisiere oder aktiviere Hooks und ändere globale Einstellungen nur mit ausdrücklicher Erlaubnis. Ein Projekt kann Context Mode empfehlen, doch der Warm-Handoff-Skill muss ohne ihn funktionieren. Gib keine Geheimnisse preis und umgehe keine Dateiregeln des Hosts durch ein Verarbeitungswerkzeug.

<!-- rule:CM-04 -->
## Wo es sich in langen Wellen lohnt

Lange Wellen erzeugen genau die Ausgaben, die einen Kontext fluten: Testsuiten, Bauprotokolle, Agentenberichte, Git-Verlauf, Webseiten. Mit Context Mode bleibt die Rohausgabe in einer Sandbox und wird indiziert; die Sitzung bekommt nur die gezielte Antwort oder Suchtreffer, und Folgefragen durchsuchen den Index, statt die Datei neu zu lesen. So bleibt eine lange Sitzung länger kompaktierbar.

- Für Auswertungen nutzen, nicht für die Datei, die du gleich bearbeitest; Bearbeitungen brauchen weiter das gewöhnliche Lesen des Hosts.
- Parallele Agentenstarts können jeweils gleichzeitig die Ersteinrichtung des Plugins auslösen; richte es einmal vor der Welle ein, mit Erlaubnis, statt jeden Arbeiter installieren zu lassen.
- Die Ersparnis in eigenen Läufen ist ungemessen, bis du sie misst; zitiere keine Prozentzahl aus fremden Läufen.

Quelle: [context-mode](https://github.com/mksglu/context-mode).
