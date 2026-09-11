# Claude-Code-Adapter

<!-- rule:CLA-01 -->
## Anweisungen und Fähigkeiten

Lies die geltende `CLAUDE.md` und aktuelle Nutzeranweisungen. Prüfe tatsächlich vorhandene Claude-Code-Version, Werkzeuge, Rechte, Agentenfunktionen und Arbeitsbereichsgrenzen. Rufe `/warm-handoff` auf, wenn Slash-Command-Skills unterstützt werden. Behandle Hooks, Agententeams, Subagenten, Worktrees und Cache-Steuerungen als versions- und konfigurationsabhängig.

<!-- rule:CLA-02 -->
## Agenten und Rechte

Nutze Agenten nur innerhalb des autorisierten Nutzerumfangs. Weise exklusive Dateien und klare Akzeptanzkriterien zu. Fertigmeldungen von Agenten sind Eingänge der Integration und allein kein Beleg. Leite aus altem Handoff oder Projektvorlage keine Erlaubnis zum Pushen, Installieren, Öffnen von Anwendungen oder Kontaktieren anderer ab.

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
