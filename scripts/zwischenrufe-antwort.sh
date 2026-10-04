#!/bin/bash
# Antwort ausschließlich an den gespeicherten Markdown-Eingang anhängen.
# Bei ungespeichertem oder unbekanntem Editorzustand bleibt alles unberührt.
# Aufruf: zwischenrufe-antwort.sh <zwischenrufe.md> "<text>"|- [--keine-neuen]
set -euo pipefail
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ] || { [ "$#" -eq 3 ] && [ "$3" != '--keine-neuen' ]; }; then
  echo 'Aufruf: zwischenrufe-antwort.sh <zwischenrufe.md> "<text>"|- [--keine-neuen]' >&2
  exit 2
fi
DATEI="$1"
if [ ! -f "$DATEI" ] || [ -L "$DATEI" ] || [[ "$DATEI" != *.md ]]; then
  echo "Kein gespeicherter Markdown-Eingang: $DATEI" >&2
  exit 2
fi
DATEI="$(cd "$(dirname "$DATEI")" && pwd -P)/$(basename "$DATEI")"
if [ "$2" = '-' ]; then TEXT="$(cat)"; else TEXT="$2"; fi
NEUE='ja'
if [ "${3:-}" = '--keine-neuen' ]; then NEUE='nein'; fi

# Kein Live-Text, kein Speichern. Den eigenen Pfad als Argument übergeben,
# nicht als AppleScript-Code oder über den mehrdeutigen Dateinamen.
LAEUFT="$(osascript -e 'application "TextEdit" is running' 2>/dev/null)" || {
  echo 'Editorzustand unbekannt — nichts angehängt.' >&2; exit 3;
}
MODIFIED='nicht offen'
if [ "$LAEUFT" = 'true' ]; then
  MODIFIED="$(osascript - "$DATEI" <<'OSA'
on run argv
  set wanted to item 1 of argv
  tell application "TextEdit"
    repeat with d in documents
      if path of d is wanted then
        if modified of d then return "true"
        close d saving no
        return "false"
      end if
    end repeat
  end tell
  return "nicht offen"
end run
OSA
)" || { echo 'Editorzustand unbekannt — nichts angehängt.' >&2; exit 3; }
elif [ "$LAEUFT" != 'false' ]; then
  echo 'Editorzustand unbekannt — nichts angehängt.' >&2
  exit 3
fi
case "$MODIFIED" in
  false|'nicht offen') ;;
  *) echo 'Ungespeicherte oder unbekannte Eingaben — Antwort zurückgestellt, bitte selbst speichern.' >&2; exit 3 ;;
esac
STAMP="$(date '+%d.%m.%Y-%H:%M')"
{
  printf '\n<!-- answer:end -->\n\nZWISCHENRUFE BIS HIER BEARBEITET — %s\n' "$STAMP"
  printf 'Neue Zwischenrufe gelesen: %s (gespeicherter Stand).\n\n' "$NEUE"
  printf 'Antwort Agent, %s:\n%s\n' "$STAMP" "$TEXT"
  printf '\nAB HIER NEUE ZWISCHENRUFE\n\n>>>\n'
} >> "$DATEI"
if [ "$MODIFIED" = 'false' ]; then open -a TextEdit "$DATEI"; fi
echo "angehängt: $DATEI ($STAMP), neue Zwischenrufe: $NEUE"
