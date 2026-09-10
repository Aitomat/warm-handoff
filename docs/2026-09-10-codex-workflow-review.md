# W53 — Warm-Handoff für Codex, Claude und TextEdit

Stand: 10.09.2026, 18:40:50 CEST (Uhrabfrage).
Arbeitsort: `/tmp/warm-handoff-codex-w53`, Branch `codex-w53-workflow`,
Basis `ad5cd4959990ce4c151ec97267b98544b8ee5541`.

## Ergebnis

Gemeinsamer [Skill-Einstieg](../SKILL.md), aktive Adapter für
[Codex](../references/codex.md) und [Claude](../references/claude-code.md).
Der gelebte Claude-Dokumentzyklus bleibt aktiv; vollständige frühere Fassungen
bleiben als Herkunft erhalten. README und eigenständige AGENTS-Vorlage sind
angeglichen: deutsch, Originalantworten, Kopierzeile oben, Pasted Content auch
Codex/cmux, Oberchef → Wächter → Arbeiter, maximal vier Wächter innerhalb
tatsächlicher Host-/Rechnerkapazität und isolierter Dateiverantwortung.

[RTF-/Tab-Anleitung](../references/rtf-macos.md) enthält die von der Hauptsession
per CUA geprüfte gezielte TextEdit-Methode: aktive oder neue gemeinsame Gruppe,
keine fremden Fenster vereinen, eigenen leeren Hilfstab entfernen.

Der neue [Renderer](../scripts/render_rtf.py) ersetzt temporäres HTML durch
deterministische RTF-Linkfelder. Relative Links nutzen die explizite Projektwurzel
oder nächste Git-Wurzel; ohne Git das Markdown-Verzeichnis. Bestehende Ziele
einschließlich Symlinks werden auch bei Konkurrenz atomar geschützt.

## Belege

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`:
  **18/18 bestanden**, einschließlich Projektlinks, Leerzeichen, Unicode/Emoji,
  Kopierzeile, Kopie-Zitaten, Dokument-/Screenshot-Markern und Dateischutz.
- Vier anfängliche und zwei beim Review ergänzte rote Regressionen behoben.
- `quick_validate.py .`: gültiger Skill; `bash -n scripts/handoff-rtf.sh`: bestanden.
- 23 interne Links aktiver Skill-Anleitungen geprüft; `git diff --check` sauber.

## Grenzen / Übergabe

Keine App-Dateien, App-Builds, globale Installation oder UI verändert.
TextEdit-Klick-/Speicherabnahme des neuen Renderers bleibt bei root offen.
Komplexes Markdown kann sichtbare Syntax bleiben; lokale Anker werden ausdrücklich
abgewiesen, keine still abgeschnittenen Ziele. Veröffentlichung übernimmt root.

Automatische dcg-Prüfung blockierte das rekursive Entfernen eigener Python-Caches.
Keine Umgehung; ungestagte `__pycache__`-Artefakte bleiben zur späteren Bereinigung.

Git-Staging scheiterte an `index.lock: Operation not permitted` im externen
Worktree-Gitverzeichnis. Kein Commit/Push; root muss explizit stagen und committen.

README-Nachreview: Historische Hauptabschnitte lokal gekennzeichnet; aktuelle
Installation, Skripttabelle und Credits korrigiert. Claude-Ursprung und tatsächliche
Codex-W53-Mitwirkung sichtbar. Nur Dokumentation geändert; 18 Tests nicht wiederholt.
