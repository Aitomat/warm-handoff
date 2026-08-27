#!/usr/bin/env bash
# codex-limit.sh — zeigt, wie viel vom Codex-/GPT-Kontingent verbraucht ist.
#
# Warum es das gibt (Yasin, 26.08.2026, 14:03): "Siehst du bei Codex ueberhaupt,
# ob ich noch genug Limit habe? Koennte man das sichtbar machen? Wenn ich einen
# Account monatlich bezahle, sollte man die Tokens ausnutzen."
#
# Woher die Zahl kommt: Die Codex-CLI hat KEINEN Usage-Befehl. Aber der Server
# schickt bei jeder Antwort einen `rate_limits`-Block mit, und die CLI schreibt
# ihn in die Session-Datei unter ~/.codex/sessions/JJJJ/MM/TT/rollout-*.jsonl.
# Der letzte dieser Bloecke ist der aktuelle Stand.
#
# EHRLICHE GRENZE: Die Zahl ist so frisch wie der letzte Codex-Lauf. Wer seit
# drei Tagen kein Codex benutzt hat, sieht den Stand von vor drei Tagen (und der
# ist dann eher zu hoch als zu niedrig — das Fenster laeuft ja weiter). Deshalb
# steht das Alter der Messung immer dabei.
#
# Aufruf:
#   codex-limit.sh          -> eine Zeile fuer Menschen
#   codex-limit.sh --kurz   -> kompakt fuer die Statuszeile ("codex 10%/7d")
#   codex-limit.sh --json   -> Rohwerte

set -uo pipefail
modus="${1:-}"
cache="$HOME/.claude/.codex-limit-cache${modus:+${modus//-/}}"

# Statuszeile rendert oft — Ergebnis 5 Minuten cachen.
if [ "$modus" = "--kurz" ] && [ -f "$cache" ]; then
  alter=$(( $(date +%s) - $(stat -f %m "$cache" 2>/dev/null || echo 0) ))
  if [ "$alter" -lt 300 ]; then
    cat "$cache"
    exit 0
  fi
fi

# Neueste Session-Datei finden: die letzten Tagesordner absuchen statt den
# ganzen Baum (das waere bei jedem Render zu teuer).
# `tac` gibt es auf macOS nicht — `tail -r` ist das Gegenstueck. Und die neueste
# Datei muss nicht die mit dem Limit-Block sein (abgebrochene Laeufe), deshalb
# wird bis zum ersten Treffer weitergesucht.
sess=""
for kandidat in $(ls -t "$HOME"/.codex/sessions/*/*/*/*.jsonl 2>/dev/null | head -40); do
  if grep -ql '"rate_limits"' "$kandidat" 2>/dev/null || grep -q '"rate_limits"' "$kandidat" 2>/dev/null; then
    sess="$kandidat"; break
  fi
done

if [ -z "$sess" ]; then
  [ "$modus" = "--kurz" ] || echo "Codex: keine Sitzungsdaten gefunden"
  exit 0
fi

SESS="$sess" MODUS="$modus" python3 <<'PY' > "$cache.tmp" 2>/dev/null
import json, os, time

pfad = os.environ["SESS"]
modus = os.environ.get("MODUS", "")
letzte = None
with open(pfad, "rb") as f:
    for zeile in f.read().decode("utf-8", "ignore").splitlines():
        if '"rate_limits"' not in zeile:
            continue
        try:
            d = json.loads(zeile)
        except Exception:
            continue
        # Der Block steckt verschachtelt in einem token_count-Event.
        stapel = [d]
        while stapel:
            k = stapel.pop()
            if isinstance(k, dict):
                if "rate_limits" in k and isinstance(k["rate_limits"], dict):
                    letzte = k["rate_limits"]
                stapel.extend(k.values())
            elif isinstance(k, list):
                stapel.extend(k)

if not letzte:
    raise SystemExit(0)

gemessen = os.path.getmtime(pfad)
alter_min = (time.time() - gemessen) / 60

def fenster(b):
    if not b:
        return None
    p = b.get("used_percent")
    wm = b.get("window_minutes") or 0
    name = "7d" if wm >= 9000 else ("5h" if wm >= 250 else f"{wm}m")
    rest = ""
    ra = b.get("resets_at")
    if ra:
        s = ra - time.time()
        if s > 0:
            rest = f", Reset in {int(s//86400)}d {int((s%86400)//3600)}h" if s > 86400 else f", Reset in {int(s//3600)}h"
    return {"prozent": p, "name": name, "rest": rest}

p1 = fenster(letzte.get("primary"))
p2 = fenster(letzte.get("secondary"))
plan = letzte.get("plan_type") or "?"

if modus == "--json":
    print(json.dumps({"primary": p1, "secondary": p2, "plan": plan,
                      "alter_minuten": round(alter_min)}, ensure_ascii=False))
elif modus == "--kurz":
    teile = [f"codex {x['prozent']:.0f}%/{x['name']}" for x in (p1, p2) if x and x["prozent"] is not None]
    if teile:
        print(" ".join(teile))
else:
    alter = f"{alter_min/60:.0f} h" if alter_min >= 90 else f"{alter_min:.0f} min"
    if alter_min >= 2880:
        alter = f"{alter_min/1440:.0f} Tage"
    print(f"Codex ({plan}): " + " · ".join(
        f"{x['prozent']:.0f} % vom {x['name']}-Fenster verbraucht{x['rest']}"
        for x in (p1, p2) if x and x["prozent"] is not None
    ) + f"  [gemessen beim letzten Codex-Lauf, vor {alter}]")
PY

if [ -s "$cache.tmp" ]; then
  mv "$cache.tmp" "$cache"
  cat "$cache"
else
  rm -f "$cache.tmp"
fi
