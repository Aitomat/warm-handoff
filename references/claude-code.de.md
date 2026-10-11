# Claude-Code-Adapter

<!-- rule:CLA-01 -->
## Anweisungen und Fähigkeiten

Lies die geltende `AGENTS.md` und aktuelle Nutzeranweisungen. `AGENTS.md` ist die eine gemeinsame Anweisungsdatei: aktuelle Claude-Code-Versionen laden sie als Projektanweisung, eine Datei bedient also Codex, Claude und andere Agenten. Lege keine eigene `CLAUDE.md` an; behält ein Projekt eine, ist sie nur Verweis oder Symlink auf `AGENTS.md`. Prüfe tatsächlich vorhandene Claude-Code-Version, Werkzeuge, Rechte, Agentenfunktionen und Arbeitsbereichsgrenzen. Rufe `/warm-handoff` auf, wenn Slash-Command-Skills unterstützt werden. Behandle Hooks, Agententeams, Subagenten, Worktrees und Cache-Steuerungen als versions- und konfigurationsabhängig.

<!-- rule:CLA-02 -->
## Agenten und Rechte

Nutze Agenten nur innerhalb des autorisierten Nutzerumfangs. Weise exklusive Dateien und klare Akzeptanzkriterien zu. Fertigmeldungen von Agenten sind Eingänge der Integration und allein kein Beleg. Leite aus altem Handoff oder Projektvorlage keine Erlaubnis zum Pushen, Installieren, Öffnen von Anwendungen oder Kontaktieren anderer ab.

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und in einem Editor öffnen, in den der Nutzer schreiben kann (macOS: `open -a TextEdit "<voller Pfad>"`, nie in einem reinen Lese-Viewer wie dem cmux-Markdown-Tab), nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

<!-- rule:CLA-03 -->
## Cachefakten und Grenzen

Am 11.09.2026 anhand offizieller Anthropic-Dokumentation geprüft:

- Claude-Kontextfenster hängen vom Modell ab und können bis zu 1 Mio. Token reichen; prüfe die aktuelle Seite des gewählten Modells.
- Claude Code dokumentiert für das Hauptgespräch in Abonnements standardmäßig eine Stunde Prompt-Cache-Dauer und für andere Interaktionen wie Subagenten, Workflows und Forks fünf Minuten.
- `promptCacheTtl`, `subagentPromptCacheTtl`, zugehörige Umgebungsvariablen und `cacheTtl` für Subagenten hängen von installierter Claude-Code-Version und Konfiguration ab.
- Eine Effort-Änderung macht den Cache gewöhnlich ungültig; Anthropic dokumentiert für Fable 5.1 in bestimmten API-Key- und Abonnementfällen eine Ausnahme. Am 11.10.2026 erneut geprüft: Claude Code dokumentiert inzwischen, dass ein Effort-Wechsel bei Opus 5.5, Sonnet 5.5, Haiku 5.5 und Fable 5.1 über API-Schlüssel oder Claude-Abo den Cache erhält; Anbieter, Version und Konfiguration können das ausschließen. In direkten API-Aufrufen macht ein geänderter requestweiter Effort- oder Thinking-Wert mindestens den Nachrichten-Cache ungültig.
- Ein Modellwechsel in einer Sitzung verarbeitet die ganze Historie neu, ohne Treffer aus dem Cache des alten Modells: Der Neuaufbau wird als Cache-Schreiben berechnet (1,25-fache Basiseingabe für fünf Minuten, 2-fach für eine Stunde), während ein Cache-Lesen normalerweise 10 % der Basiseingabe kostet, bei manchen neueren Modellen weniger. Vor dem Nennen einer Zahl die aktuelle Preisseite prüfen.

Diese Angaben sind dokumentiertes Client- oder API-Verhalten und kein Beleg für wirksamen Kontext, Cachetreffer, Kontingent oder Kosten der aktuellen Sitzung. Berichte diese nur mit aktuellem Hostbeleg. Übernimm keine historischen Preisfaktoren oder universellen Cachebruchregeln.

Quellen: [Claude-Code-Prompt-Caching](https://code.claude.com/docs/en/prompt-caching), [Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows), [API-Prompt-Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

<!-- rule:CLA-04 -->
## Handoff-Grenze

Schreibe vor Komprimierung, Modellwechsel oder Ende eines langen Laufs das neue Handoff und prüfe es auf dem Datenträger. Erhalte die vollständige Nutzersammlung, nenne versionsgebundene Annahmen und trenne veröffentlichte Plattformfakten von aktuellen Sitzungsmesswerten.

Claude-Sessions laufen lang und verlieren den Anfrage-Stempel leicht: Die erste Antwort auf jede neue Nutzernachricht beginnt mit `Name, TT.MM.JJJJ-HH:MM` aus `date` (HF-09), auch tief in einer Welle.

<!-- rule:CLA-05 -->
## Richtig kompaktieren: eine Sitzung statt vieler

Ein langes Projekt braucht nicht für jeden Schritt eine neue Sitzung. Lass eine Sitzung weiterlaufen und setze `/compact` an einem guten Moment: zwischen zwei Schritten, wenn der Stand in Dateien steht.

1. **Vorher fragen, was man danach eingibt.** Frag den Agenten vor dem Kompaktieren: „Was soll ich nach `/compact` eingeben?“ Er schreibt einen Fortsetzungsblock in eine Datei (Stand, was läuft, nächster Schritt, welche Dateien zu lesen sind) und gibt dir einen Satz zum Einfügen.
2. **Kompaktieren, dann einfügen.** Nach `/compact` genügt Kopieren und Einfügen dieses Satzes; der Agent liest die Datei neu, statt sich auf die Zusammenfassung zu verlassen.
3. **Warum:** Eine neue Sitzung baut den ganzen Cache neu auf und verliert den Arbeitsrhythmus; eine kompaktierte Sitzung behält Regeln und Gedächtnisdateien und lässt nur den Rohverlauf fallen.

Beobachtung, kein dokumentiertes Verhalten: In neueren Claude-Code-Versionen wurde eine Sitzung nach etwa einer Stunde Inaktivität automatisch kompaktiert, sodass der große Kontext nicht vollständig neu aufgebaut werden musste. Verlass dich nicht darauf; schreib den Fortsetzungsblock vor jeder langen Pause.

Gemessenes Beispiel: Eine Hauptsitzung lief über 57 Stunden mit fünf Kompaktierungen und trug mehrere vollständige Arbeitswellen, darunter eine mit 57 Aufträgen.

<!-- rule:CLA-06 -->
## Cron-Wecker: ein Lagebericht, der den Cache warm hält

Plane während einer langen Welle einen **einmaligen** Wecker (in Claude Code mit `CronCreate`) etwa 50 Minuten voraus und gib ihm echte Arbeit: einen kurzen Lagebericht für den Nutzer. Nach dem Bericht den nächsten einmaligen Wecker setzen, falls die Welle noch läuft. Nie einen wiederkehrenden Auftrag anlegen.

- **Cache:** Beim Stunden-Cache der Hauptsitzung liegt ein Wecker nach etwa 50 Minuten im Zeitfenster, sofern er rechtzeitig ausgeführt wird. Er ist kein garantierter spätester Lesezeitpunkt: Ist der Agent beschäftigt, wartet der Wecker bis zum Ende des laufenden Schritts, und die Sitzung muss geöffnet sein.
- **Der Nutzer weiß, wann der Agent wieder liest.** Zwischenrufe kann er bis zum nächsten Bericht sammeln und speichern, statt sie einzeln zu schicken; Dringendes gehört weiter in den Chat.
- **Grenzen:** Dass ein Wecker die automatische Kompaktierung generell verhindert, ist nicht belegt; ein voller Kontext kann sie weiterhin auslösen. Ein Wecker kostet eine Anfrage; verbinde ihn mit einem nützlichen Bericht statt mit einem leeren Ping. Das Laden dieses Skills legt nie selbst einen Wecker an (WV-14).

Quelle: [Claude-Code-Termine](https://code.claude.com/docs/en/scheduled-tasks).

<!-- rule:CLA-07 -->
## Statuszeile als Cockpit

Leg die Zahlen, von denen ein langer Lauf abhängt, in die Fußzeile oder Statuszeile des Terminals, statt nach ihnen zu fragen: etwa Kontextgröße, Fünf-Stunden- und Wochenverbrauch, das Restlimit des zweiten Anbieters und die Sitzungskosten. In einem Multiplexer wie cmux bleibt die Fußzeile über alle Bereiche sichtbar, sodass der Nutzer auf einen Blick sieht, wann er kompaktieren, bremsen oder auf einen Reset warten sollte. Die Statuszeile ist eine Anzeige; ein Agent berichtet weiterhin nur gemessene Werte und nennt den Rest unbekannt (MR-02).
