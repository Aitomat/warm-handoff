#!/usr/bin/env bash
# HF-08: den letzten Sammlungsfuß des direkten Vorgängers wörtlich verlangen;
# Antwortfelder des Vorgängers nur verweisen, nie wörtlich wiederholen (W97).
# Gespeichertes RTF ausdrücklich übergeben, wenn dort geantwortet wurde.
set -euo pipefail
SKRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SKRIPT_DIR/sammlung_pruefen.py" "$@"
