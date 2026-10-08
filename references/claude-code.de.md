# Claude-Code-Adapter

<!-- rule:CLA-01 -->
## Anweisungen und Fähigkeiten

Lies die geltende `AGENTS.md` und aktuelle Nutzeranweisungen. `AGENTS.md` ist die eine gemeinsame Anweisungsdatei: aktuelle Claude-Code-Versionen laden sie als Projektanweisung, eine Datei bedient also Codex, Claude und andere Agenten. Lege keine eigene `CLAUDE.md` an; behält ein Projekt eine, ist sie nur Verweis oder Symlink auf `AGENTS.md`. Prüfe tatsächlich vorhandene Claude-Code-Version, Werkzeuge, Rechte, Agentenfunktionen und Arbeitsbereichsgrenzen. Rufe `/warm-handoff` auf, wenn Slash-Command-Skills unterstützt werden. Behandle Hooks, Agententeams, Subagenten, Worktrees und Cache-Steuerungen als versions- und konfigurationsabhängig.

<!-- rule:CLA-02 -->
## Agenten und Rechte

Nutze Agenten nur innerhalb des autorisierten Nutzerumfangs. Weise exklusive Dateien und klare Akzeptanzkriterien zu. Fertigmeldungen von Agenten sind Eingänge der Integration und allein kein Beleg. Leite aus altem Handoff oder Projektvorlage keine Erlaubnis zum Pushen, Installieren, Öffnen von Anwendungen oder Kontaktieren anderer ab.

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und öffnen, nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

<!-- rule:CLA-03 -->
## Cachefakten und Grenzen

Am 11.09.2026 anhand offizieller Anthropic-Dokumentation geprüft:

- Claude-Kontextfenster hängen vom Modell ab und können bis zu 1 Mio. Token reichen; prüfe die aktuelle Seite des gewählten Modells.
- Claude Code dokumentiert für das Hauptgespräch in Abonnements standardmäßig eine Stunde Prompt-Cache-Dauer und für andere Interaktionen wie Subagenten, Workflows und Forks fünf Minuten.
- `promptCacheTtl`, `subagentPromptCacheTtl`, zugehörige Umgebungsvariablen und `cacheTtl` für Subagenten hängen von installierter Claude-Code-Version und Konfiguration ab.
- Eine Effort-Änderung macht den Cache gewöhnlich ungültig; Anthropic dokumentiert für Fable 5.1 in bestimmten API-Key- und Abonnementfällen eine Ausnahme.

Diese Angaben sind dokumentiertes Client- oder API-Verhalten und kein Beleg für wirksamen Kontext, Cachetreffer, Kontingent oder Kosten der aktuellen Sitzung. Berichte diese nur mit aktuellem Hostbeleg. Übernimm keine historischen Preisfaktoren oder universellen Cachebruchregeln.

Quellen: [Claude-Code-Prompt-Caching](https://code.claude.com/docs/en/prompt-caching), [Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows).

<!-- rule:CLA-04 -->
## Handoff-Grenze

Schreibe vor Komprimierung, Modellwechsel oder Ende eines langen Laufs das neue Handoff und prüfe es auf dem Datenträger. Erhalte die vollständige Nutzersammlung, nenne versionsgebundene Annahmen und trenne veröffentlichte Plattformfakten von aktuellen Sitzungsmesswerten.

Claude-Sessions laufen lang und verlieren den Anfrage-Stempel leicht: Die erste Antwort auf jede neue Nutzernachricht beginnt mit `Name, TT.MM.JJJJ-HH:MM` aus `date` (HF-09), auch tief in einer Welle.
