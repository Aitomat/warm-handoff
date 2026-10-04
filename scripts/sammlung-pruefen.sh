#!/usr/bin/env bash
# HF-08: nur neue Antwortfelder und den letzten Sammlungsfuß des direkten
# Vorgängers prüfen; ältere Originale bleiben im Archiv und werden verlinkt.
# Gespeichertes RTF ausdrücklich übergeben, wenn dort geantwortet wurde.
set -euo pipefail
SKRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SKRIPT_DIR/sammlung_pruefen.py" "$@"
