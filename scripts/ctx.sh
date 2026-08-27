#!/usr/bin/env bash
# ctx.sh — was seit der letzten Nachricht des Nutzers verbraucht wurde, und WOFÜR.
#
# Warum (Yasin, 26.08.2026, 18:20): "Dass du immer angibst, was wofür gerade
# verbraucht worden ist seit der letzten Nachricht — so ein Feedback. Ah, ich habe
# dir jetzt geantwortet, und das Ganze hatte so und so viele Tokens gekostet, weil
# dies und das und mal zehn Prozent."
#
# Also nicht nur eine Zahl, sondern eine Aufschlüsselung: wie viele Anfragen, was
# in ihnen passiert ist (Agentenberichte, Dateizugriffe, Befehle, eigene Antworten)
# und wie sich die Kosten auf Lesen / Schreiben / Ausgabe verteilen.
#
# Der Trick, damit die Messung nichts kostet: NIE allein aufrufen, sondern an einen
# Befehl anhängen, der ohnehin läuft — meist an dasselbe `date` für den Zeitstempel:
#   date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh
#
# Preisfaktoren (auf frische Eingabe normiert): lesen ×0,1 · schreiben ×2 · Ausgabe ×5.

set -uo pipefail
ziel="${1:-}"
if [ -z "$ziel" ]; then
  proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"
  ziel=$(ls -t "$proj"/*.jsonl 2>/dev/null | head -1)
fi
[ -f "$ziel" ] || exit 0

SESS="$ziel" python3 <<'PY'
import json, os
from collections import Counter

# Zeilen vom Typ "user", die NICHT vom Menschen stammen (siehe session-kosten.sh).
MASCHINE = ("<task-notification>", "<system-reminder>", "Caveat:",
            "Base directory for this skill:", "<local-command-",
            "[Request interrupted", "API Error")

zeilen = open(os.environ["SESS"], "rb").read().decode("utf-8", "ignore").splitlines()

# Rückwärts bis zur letzten ECHTEN Nutzernachricht laufen.
start = 0
for i in range(len(zeilen) - 1, -1, -1):
    try:
        d = json.loads(zeilen[i])
    except Exception:
        continue
    if d.get("type") != "user":
        continue
    c = (d.get("message") or {}).get("content")
    echt = isinstance(c, str) or (
        isinstance(c, list)
        and not any(isinstance(p, dict) and p.get("type") == "tool_result" for p in c))
    if not echt:
        continue
    roh = c if isinstance(c, str) else " ".join(
        p.get("text", "") for p in c if isinstance(p, dict))
    if " ".join(roh.split()).startswith(MASCHINE):
        continue
    start = i
    break

lesen = schreiben = ausgabe = eingabe = anfragen = 0
werkzeuge = Counter()
g_lesen = g_schreiben = g_ausgabe = g_eingabe = g_anfragen = 0

for i, z in enumerate(zeilen):
    if '"usage"' not in z and '"tool_use"' not in z:
        continue
    try:
        d = json.loads(z)
    except Exception:
        continue
    m = d.get("message") or {}
    u = m.get("usage")
    if u:
        g_anfragen += 1
        g_lesen += u.get("cache_read_input_tokens", 0)
        g_schreiben += u.get("cache_creation_input_tokens", 0)
        g_ausgabe += u.get("output_tokens", 0)
        g_eingabe += u.get("input_tokens", 0)
        if i >= start:
            anfragen += 1
            lesen += u.get("cache_read_input_tokens", 0)
            schreiben += u.get("cache_creation_input_tokens", 0)
            ausgabe += u.get("output_tokens", 0)
            eingabe += u.get("input_tokens", 0)
    if i >= start:
        c = m.get("content")
        if isinstance(c, list):
            for teil in c:
                if isinstance(teil, dict) and teil.get("type") == "tool_use":
                    werkzeuge[teil.get("name", "?")] += 1

if anfragen == 0:
    raise SystemExit(0)

def k(n):
    return f"{n/1000:.1f}k" if n < 10000 else f"{n/1000:.0f}k"

aeq = lesen * 0.1 + schreiben * 2 + ausgabe * 5 + eingabe
g_aeq = g_lesen * 0.1 + g_schreiben * 2 + g_ausgabe * 5 + g_eingabe

# Werkzeuge in Klartext, damit die Zeile ohne Vorwissen lesbar ist.
NAMEN = {"Bash": "Befehle", "Read": "Dateien gelesen", "Edit": "Dateien geändert",
         "Write": "Dateien geschrieben", "Grep": "Suchläufe", "Glob": "Dateisuchen",
         "Agent": "Agenten gestartet", "SendMessage": "Nachrichten an Agenten",
         "Task": "Aufgaben", "WebFetch": "Web-Abrufe", "TodoWrite": "Merkliste"}
teile = [f"{n}× {NAMEN.get(w, w)}" for w, n in werkzeuge.most_common(5)]
womit = " · ".join(teile) if teile else "nur Antworten"

print(f"SEIT DEINER LETZTEN NACHRICHT ≈ {k(aeq)} in {anfragen} Anfragen ({womit})")
print(f"  davon: Gespräch {anfragen}× neu gelesen ({k(lesen)} ×0,1 = {k(lesen*0.1)})"
      f" · Neues gespeichert ({k(schreiben)} ×2 = {k(schreiben*2)})"
      f" · meine Antworten ({k(ausgabe)} ×5 = {k(ausgabe*5)})")
print(f"  Sitzung gesamt: {g_anfragen} Anfragen, {k(g_aeq)}")
PY
