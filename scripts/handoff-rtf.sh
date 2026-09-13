#!/usr/bin/env bash
set -euo pipefail
# Sole generation entry point for handoff and Zwischenrufe RTFs.
# Einziger Erzeugungseinstieg für Handoff- und Zwischenrufe-RTFs.
# render_rtf.py owns the black-on-gold 18 pt state and output verification.
exec python3 "$(dirname "$0")/render_rtf.py" "$@"
