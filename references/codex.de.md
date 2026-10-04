# Codex-Adapter

<!-- rule:CDX-01 -->
## Anweisungen und Werkzeuge feststellen

Lies vor dem Handeln die geltenden `AGENTS.md`-Dateien und aktuellen Nutzeranweisungen. Prüfe Werkzeuge, Skills, Apps, Dateirechte, Freigaberegeln und Agentenplätze, die diese Sitzung tatsächlich anbietet. Leite Shell, Browser, Subagentenzahl, beschreibbare Pfade, Netzwerkzugriff oder Freigabestand nie von einem anderen Codex-Host ab.

Rufe diesen Skill als `$warm-handoff` auf, wenn der Host benannte Skills unterstützt. Der kurze Skill bleibt providerneutral; diese Datei bildet ihn auf Codex ab.

<!-- rule:CDX-02 -->
## Rechte und dauerhafte Arbeit

Nutze das engste verfügbare Werkzeug, das die Aktion erledigt. Reine Leseprüfung und reversible Arbeit laufen normalerweise innerhalb des autorisierten Auftrags weiter. Beachte ausdrücklichen Dateibesitz. Frage nach Freigabe oder nutze sie nur, wenn der Host sie für eine autorisierte notwendige Aktion verlangt. Behandle ein Handoff nie als Erlaubnis zur Veröffentlichung, globalen Installation, UI-Steuerung, Kontaktaufnahme oder destruktiven Arbeit.

Schreibe geforderte Pläne und Berichte, bevor du Abschluss meldest. Lies oder hashe gespeicherte Dateien erneut, wenn Installation oder exakte Erhaltung entscheidend ist.

Rufe für jedes RTF-Handoff `scripts/handoff-rtf.sh QUELLE NEUE_AUSGABE` aus dem Skill-Verzeichnis auf; beachte [RTF-Sicherheit](rtf-macos.de.md). Erzeuge das endgültige RTF nie direkt mit `textutil`: Es dient in diesem Ablauf nur zum Lesen und Prüfen.

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und öffnen, nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

<!-- rule:CDX-03 -->
## Agenten und Wächtermodus

Delegiere nur, wenn Nutzer, Projektregeln oder aktiver Ablauf Agenten verlangen. Prüfe zuerst die echten freien Plätze. Gib jedem Arbeiter einen kurzen eigenständigen Brief, exklusive Pfade, Akzeptanzkriterien und Lieferpfad. Nutze die automatische Fertigmeldung für Routineergebnisse.

Wenn ein Projekt den Wächtermodus wählt, leite substanzielle Recherche, Analyse, Umsetzung, QA, Sichtprüfung, Berichte und Handoff-Erstellung über Wächter und Arbeiter. Die Hauptsession übernimmt knappe Koordination, notwendige Entscheidungen und gebündelte Abnahme ohne parallele Detaildoppelarbeit. Frage nicht vor 25 Minuten nach Status, außer bei einem Blocker. Ist kein Platz frei, melde oder plane die Arbeit; erledige nicht still eine zweite Kopie in der Hauptsession.

<!-- rule:CDX-04 -->
## Modelle, Kontext und Telemetrie

Behandle Modellverfügbarkeit, Kontextkapazität, Reasoning-Steuerung, Caching, Kontingente und Kostenanzeigen als veränderliche Hostfakten. Nutze [Modellrouting](model-routing.de.md). Ein veröffentlichtes OpenAI-API-Kontextfenster belegt nicht die wirksame Grenze des aktuellen Codex-Clients. Zeigt der Host keine wirksame Grenze oder Sitzungstelemetrie, nenne sie unbekannt; setze keine erinnerten Zahlen ein.

Am 11.09.2026 anhand offizieller OpenAI-Dokumentation geprüft: Die öffentlichen API-Modellseiten nennen für GPT-6 Astra und GPT-5.6 Sol Kontextfenster von 1.050.000 Token. Das ist nur API-Spezifikation. OpenAIs Prompt-Caching-Leitfaden beschreibt API-Caching und ist keine Garantie für eine Codex-Abonnementsitzung.

Quellen: [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [Prompt-Caching](https://developers.openai.com/api/docs/guides/prompt-caching).

<!-- rule:CDX-05 -->
## Harte Regeln für einen Codex-Chef

Eine Codex-Chefsitzung überspringt genau diese Punkte gern. Jeder ist eine Schranke, kein Rat; ein Handoff, dem einer fehlt, ist nicht fertig.

- [ ] Jeder Zeitstempel kommt beim Schreiben aus `date`, nie aus einer Schätzung.
- [ ] Erste Zeile jedes Handoffs, Berichts und jeder Zwischenrufe-Datei: der eigene absolute Pfad; zweite Zeile: der Stand aus `date`.
- [ ] Das neue Handoff entsteht direkt im Archivordner des Projekts und wird nie verschoben; ein beantwortetes Handoff wird nie überschrieben.
- [ ] Genau ein Eingang: bis zum Wellenstart der Handoff-Fuß, danach die Zwischenrufe-Datei als `.md` bis zum nächsten Handoff.
- [ ] Vor dem Schreiben das [Handoff-Format](handoff-format.de.md) vollständig öffnen; „Ich kenne das Format" zählt nicht.
- [ ] Den Vorgänger ungefiltert lesen, erste bis letzte Zeile — nichts abschneiden, nicht nur nach Antwortmarkern greppen.
- [ ] Bündel am Wellenende: bauen, installieren, im Rahmen der Freigabe committen und pushen, Handoff schreiben und öffnen — in einem Durchgang; ausstehende Berichte kommen unter „Laufend und ausstehend".
- [ ] RTF nur über `scripts/handoff-rtf.sh`.
