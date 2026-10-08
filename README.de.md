# warm-handoff 🏄

**Hauptsprache: Englisch · [Vollständige englische Fassung](README.md)**

Warm Handoff erhält Nutzereingaben und belegten Projektstand über Pausen hinweg. Außerdem definiert der Skill sichere, belegorientierte Arbeitswellen für Codex und Claude Code, ohne einen Host zum Kernablauf zu machen.

Jede Änderung einer aktiven Regel wird auch in `AGENTS.md` nachgezogen. `AGENTS.md` ist die eine gemeinsame Anweisungsdatei für Codex, Claude Code und andere Agenten; aktuelle Claude-Code-Versionen lesen sie ebenfalls. Eine `CLAUDE.md` ist optional — höchstens ein einzeiliger Verweis oder ein Symlink auf `AGENTS.md`.

## Warum Zwischenrufe-Datei und Handoff

Agenten arbeiten stundenlang; der Mensch soll nicht danebensitzen und warten. Warm Handoff gibt ihm zwei schlichte Dokumente statt eines Chats, den er beobachten muss:

- **Das Handoff** ist die Brücke zwischen Sessions. Es trägt, was belegt ist, was noch läuft oder offen ist, und die Fragen, die die nächste Session beantworten muss. Der Nutzer antwortet darin in seinem Tempo; Speichern (Cmd-S) ist die Freigabe. RTF-Handoffs bleiben dauerhaft im Archiv, als Dokumentation des Projekts.
- **Die Zwischenrufe-Datei** ist der Eingang, solange eine Welle läuft. Jede Idee, Korrektur oder Frage, die einem einfällt, kommt dort hinein und wird gespeichert; der Chef holt sie beim nächsten Aufwachen ab, ohne unterbrochen zu werden.

Der Vorteil: **Der Mensch bleibt kreativ, während die Agenten arbeiten.** Er kann stundenlang weiterdenken, diktieren und ergänzen, und nichts geht verloren, denn:

1. **Fragen zuerst.** Der Chef filtert die neuen Fragen des Nutzers aus dem beantworteten Handoff heraus und beantwortet, was er kann, sofort — im Chat und als Kopie in der Zwischenrufe-Datei, parallel zum Wellenstart. Tiefere Antworten liefern danach die Fachagenten. Fragen, die erst Stunden später beantwortet werden, sind schon wieder vergessen.
2. **Späte Ideen kommen noch an.** Ein Zwischenruf zu einem noch nicht gestarteten Auftrag kommt als Nachtrag in dessen Auftragsdatei; einer zu einem laufenden Auftrag wird ein Folgeauftrag.
3. **Kleines wartet nicht.** Einer der parallelen Agentenplätze arbeitet nur kleine Aufgaben nacheinander ab, während die langen, schwierigen Themen zuerst auf den anderen starten.
4. **Jede neue Anfrage trägt einen Stempel.** Jede erste Antwort beginnt mit `Name, TT.MM.JJJJ-HH:MM` aus der Systemuhr; so sieht der Nutzer, wann die Arbeit begann, und kann seine Anfragen zählen.

<!-- section:SURFACES -->
## Oberfläche wählen

| Bedarf | Englisch | Deutsch | Installierbarer Einstieg |
|---|---|---|---|
| Routine mit wenig Kontext | [Kurzer Skill](SKILL.md) | [Installierbarer kurzer deutscher Skill](variants/compact-de/SKILL.md) | Paket `compact-en` oder `compact-de` |
| Einführung, Schulung, Audit | [Vollständiger Skill](variants/full/SKILL.md) | [Installierbarer vollständiger deutscher Skill](variants/full-de/SKILL.md) | Paket `full-en` oder `full-de` |
| Codex-Hostverhalten | [Codex-Adapter](references/codex.md) | [Codex-Adapter](references/codex.de.md) | bei Bedarf laden |
| Claude-Code-Verhalten | [Claude-Adapter](references/claude-code.md) | [Claude-Adapter](references/claude-code.de.md) | bei Bedarf laden |

Alle aktiven Dateien ohne Sprachzusatz sind Englisch. Jede aktive Anweisung hat eine semantische `.de.md`-Entsprechung in der [maschinenlesbaren Sprachmatrix](docs/language-matrix.json). Spanisch ist zurückgestellt. Audio, Video und Website-Material bleiben Zukunftsvorschläge.

<!-- section:INSTALLATION -->
## Eine Variante installieren

Prüfe ein bestehendes Ziel zuerst und bewahre es getrennt. Mische keine Dateien in ein belegtes Skillverzeichnis.

Wähle genau ein Paket aus `docs/language-matrix.json`. Kopiere dessen `entry` als `SKILL.md` in ein neues Ziel und dann nur die aufgeführten `resources` unter Erhalt ihrer relativen Pfade. Übliche Zielordner liegen unter `~/.codex/skills/` für Codex und `~/.claude/skills/` für Claude Code. Die vier Paket-IDs sind `compact-en`, `compact-de`, `full-en` und `full-de`; jedes installierte Paket hat einen eindeutigen Skillnamen.

| Paket | Als `SKILL.md` kopierter Einstieg | Skillname | Codex-Aufruf | Claude-Code-Aufruf |
|---|---|---|---|---|
| `compact-en` | `SKILL.md` | `warm-handoff` | `$warm-handoff` | `/warm-handoff` |
| `compact-de` | `variants/compact-de/SKILL.md` | `warm-handoff-de` | `$warm-handoff-de` | `/warm-handoff-de` |
| `full-en` | `variants/full/SKILL.md` | `warm-handoff-full` | `$warm-handoff-full` | `/warm-handoff-full` |
| `full-de` | `variants/full-de/SKILL.md` | `warm-handoff-full-de` | `$warm-handoff-full-de` | `/warm-handoff-full-de` |

Kopiere nicht das gesamte Repository. Historische Belege, persönliche Helfer, Reviewartefakte, Tests und Dateien wie `docs/.sol-err`, `scripts/codex-limit.sh` oder `scripts/skills-uebersicht.sh` gehören nicht in ein aktives Paket. Das Paketmanifest enthält nur den gewählten Einstieg, dessen revisionsgleiche lokale Referenzen, die Renderer-, Prüf- und Antwortskripte und die passende Projektvereinbarung. Die Installation ändert keine globalen Einstellungen oder Projektanweisungsdateien.

RTF-Unterstützung ist optional und nur für macOS. Sie benötigt Bash, Python 3 und `textutil`:

Erzeuge angeforderte Handoff-RTFs ausschließlich mit `scripts/handoff-rtf.sh`, mit absoluten Quell-/Zielpfaden und neuem Zieldateinamen. Text hinter `>>>` bleibt schwarz auf Gold in 18 pt. Siehe [RTF-Sicherheit](references/rtf-macos.de.md) für Steuerworte, Antwortgrenzen und Beleggrenzen.

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und öffnen, nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

Cmd-S gibt gespeicherte Eingaben innerhalb bestehender Autorisierung frei. Halte genau einen aktiven Zwischenrufe-Eingang (Handoff-Fußbereich oder vereinbarte Datei); der andere Ort verlinkt nur darauf. Archiviere beantwortete Handoffs im `handoff-archiv/` des Projekts mit `mv`, nie `rm`; verschiebe nicht die aktive Eingabedatei. **Neue Handoffs entstehen direkt in `handoff-archiv/` (Yasin, 16.09.2026-20:19).** Nicht im Projektstamm anlegen und später verschieben — jedes Verschieben ändert den Pfad, unter dem das Dokument schon verlinkt wurde. Also von Anfang an `<projekt>/handoff-archiv/_handoff-<projekt>-<datum>-<kennung>.md` und `.rtf` (Ordner mit `mkdir -p` anlegen, falls er fehlt). Yasin löscht dort selbst, was er nicht braucht; verschieben muss er nichts mehr. **Die Zwischenrufe-Datei bleibt dagegen im Projektstamm** — die räumt er von Hand weg. Führe die Tests unten aus dem Repository-Checkout aus; installierte Pakete enthalten keine Tests.

```sh
scripts/handoff-rtf.sh /projekt/docs/handoff.md /projekt/handoff.rtf --project-root /projekt
python3 -m unittest discover -s tests -v
```

<!-- section:CODEX-START -->
## Mit Codex starten

### Kurzes Englisch (`compact-en`)

<!-- prompt:compact-en-codex -->
```text
$warm-handoff
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Erhalte Nutzeroriginale, prüfe aktuellen Git- und Teststand und arbeite nur innerhalb der genannten Autorisierung weiter. Nutze den Codex-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Kurzes Deutsch (`compact-de`)

<!-- prompt:compact-de-codex -->
```text
$warm-handoff-de
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Arbeite auf Deutsch, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Codex-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Vollständiges Englisch (`full-en`)

<!-- prompt:full-en-codex -->
```text
$warm-handoff-full
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Nutze den vollständigen englischen Ablauf, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Codex-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Vollständiges Deutsch (`full-de`)

<!-- prompt:full-de-codex -->
```text
$warm-handoff-full-de
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Nutze den vollständigen deutschen Ablauf, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Codex-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

<!-- section:CLAUDE-START -->
## Mit Claude Code starten

### Kurzes Englisch (`compact-en`)

<!-- prompt:compact-en-claude -->
```text
/warm-handoff
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Erhalte Nutzeroriginale, prüfe aktuellen Git- und Teststand und arbeite nur innerhalb der genannten Autorisierung weiter. Nutze den Claude Code-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Kurzes Deutsch (`compact-de`)

<!-- prompt:compact-de-claude -->
```text
/warm-handoff-de
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Arbeite auf Deutsch, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Claude Code-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Vollständiges Englisch (`full-en`)

<!-- prompt:full-en-claude -->
```text
/warm-handoff-full
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Nutze den vollständigen englischen Ablauf, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Claude Code-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

### Vollständiges Deutsch (`full-de`)

<!-- prompt:full-de-claude -->
```text
/warm-handoff-full-de
Lies die geltenden AGENTS.md-Dateien und das vollständige gespeicherte Handoff unter <ABSOLUTE_HANDOFF_PATH>. Nutze den vollständigen deutschen Ablauf, erhalte Nutzeroriginale und bleibe in der genannten Autorisierung. Nutze den Claude Code-Adapter und schreibe vor Abschluss den geforderten dauerhaften Bericht.
```

<!-- section:REFERENCES -->
## Kernreferenzen

- [Handoff-Format](references/handoff-format.de.md)
- [Autorisierte Arbeitswellen](references/wave-execution.de.md)
- [RTF unter macOS](references/rtf-macos.de.md)
- [Optionaler Context Mode](references/context-mode.de.md)
- [Modellrouting](references/model-routing.de.md)
- [Beleggrenzen](references/evidence-scope.de.md)

Plattform- und Cacheaussagen sind in den Adaptern und der Modellrouting-Referenz datiert und belegt. API-Spezifikationen, wirksame Hostgrenzen und gemessene Sitzungswerte bleiben getrennt.

## Danksagung und Lizenz

Entwickelt von Yasin Akgün in der täglichen Arbeit an Aitomat. Die Handoff-Struktur baut auf [Matt Pococks `/handoff`](https://www.aihero.dev/skills-handoff) und verwandten öffentlichen Umsetzungen auf. Beiträge auf Englisch oder Deutsch sind willkommen. Siehe [LICENSE](LICENSE).
