#!/bin/bash
# zwischenrufe-antwort.sh — Antwort ans ENDE der Zwischenrufe-Datei anhängen
#
#   zwischenrufe-antwort.sh <zwischenrufe.md> "<text>"
#   zwischenrufe-antwort.sh <zwischenrufe.md> -        # Text von stdin
#
# Hintergrund (Yasin, 03.09.2026, 22:57/23:09/23:12): Die Datei ist in TextEdit
# offen. Wer mittendrin hineinschreibt oder die Datei ungefragt schliesst,
# zerstoert ungespeicherte Eingaben des Nutzers. Darum:
#   * NUR anhaengen (>>), nie mittendrin ersetzen,
#   * vorher den LIVE-Text aus TextEdit lesen (auch ungespeichert) und, falls
#     die Datei ungespeicherte Aenderungen hat, diese zuerst sichern,
#   * Marker + Zeitstempel schreiben,
#   * schliessen/oeffnen nur, wenn TextEdit `modified = false` meldet.
#
# Geschrieben wird der Block:
#   — übernommen bis hier, HH:MM —
#   Antwort Claude, TT.MM.JJJJ-HH:MM:
#   <text>
#   — ab hier wieder Zwischenrufe —
#   >>>

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Aufruf: $(basename "$0") <zwischenrufe.md> \"<text>\" | -" >&2
  exit 2
fi

DATEI="$1"
if [ ! -f "$DATEI" ]; then
  echo "Datei nicht gefunden: $DATEI" >&2
  exit 1
fi
DATEI="$(cd "$(dirname "$DATEI")" && pwd)/$(basename "$DATEI")"
NAME="$(basename "$DATEI")"

if [ "$2" = "-" ]; then
  TEXT="$(cat)"
else
  TEXT="$2"
fi

STAMP_LANG="$(date '+%d.%m.%Y-%H:%M')"
STAMP_KURZ="$(date '+%H:%M')"

# --- 1. Live-Stand aus TextEdit ------------------------------------------------
MODIFIED="unbekannt"
if osascript -e 'application "TextEdit" is running' 2>/dev/null | grep -q true; then
  MODIFIED="$(osascript 2>/dev/null <<OSA || true
tell application "TextEdit"
  repeat with d in documents
    if name of d is "$NAME" then return (modified of d) as text
  end repeat
end tell
return "nicht offen"
OSA
)"
  MODIFIED="${MODIFIED:-nicht offen}"
  if [ "$MODIFIED" = "true" ]; then
    # Ungespeicherte Nutzereingaben zuerst sichern — NIE verwerfen.
    osascript >/dev/null 2>&1 <<OSA || true
tell application "TextEdit"
  save (first document whose name is "$NAME")
end tell
OSA
    MODIFIED="gesichert"
  fi
fi

# --- 2. Anhaengen, ausschliesslich ans Dateiende --------------------------------
{
  printf '\n— übernommen bis hier, %s —\n\n' "$STAMP_KURZ"
  printf 'Antwort Claude, %s:\n' "$STAMP_LANG"
  printf '%s\n' "$TEXT"
  printf '\n— ab hier wieder Zwischenrufe —\n\n>>>\n'
} >> "$DATEI"

# --- 3. Nur bei modified = false neu laden --------------------------------------
NEUGELADEN="nein"
if osascript -e 'application "TextEdit" is running' 2>/dev/null | grep -q true; then
  JETZT="$(osascript 2>/dev/null <<OSA || true
tell application "TextEdit"
  repeat with d in documents
    if name of d is "$NAME" then return (modified of d) as text
  end repeat
end tell
return "nicht offen"
OSA
)"
  if [ "$JETZT" = "false" ]; then
    osascript >/dev/null 2>&1 <<OSA || true
tell application "TextEdit"
  close (first document whose name is "$NAME") saving no
end tell
OSA
    open -a TextEdit "$DATEI"
    NEUGELADEN="ja"
  fi
fi

echo "angehängt: $DATEI (${STAMP_LANG}), vorher modified=$MODIFIED, neu geladen=$NEUGELADEN"
