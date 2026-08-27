#!/usr/bin/env bash
# session-kosten.sh — Kostenübersicht einer Claude-Code-Sitzung, Welle für Welle.
#
# Warum es das gibt (Yasin, 26.08.2026, 17:51): "Kannst du nicht einfach so eine
# Tabelle machen, wo wir alles übersichtlich haben je Session — damit man eine
# Übersicht hat, was wann wie viel Tokens gekostet hat? Das wäre doch genial."
#
# Die Einheit der Tabelle ist bewusst der ABSCHNITT ZWISCHEN ZWEI NUTZER-
# NACHRICHTEN. Das ist die Einheit, die ein Mensch erlebt ("ich habe was gesagt,
# dann ist etwas passiert") — nicht die einzelne Modellanfrage, die niemand sieht.
#
# Preisfaktoren (Anthropic-Listenpreise, Opus-Verhältnis):
#   Cache lesen   ×0,1   Cache schreiben (1-h-TTL) ×2   Ausgabe ×5   frische Eingabe ×1
# Die "Äquivalente" sind auf frische Eingabe normiert. Auf einem Abo zahlt niemand
# diese Summe — sie misst, was das Kontingent belastet.
#
# Aufruf:
#   session-kosten.sh                  # aktuelles Projekt, neueste Sitzung
#   session-kosten.sh <sitzung.jsonl>  # bestimmte Sitzung
#   session-kosten.sh --markdown       # fertige Tabelle fürs Handoff

set -uo pipefail

ziel="${1:-}"
markdown=0
[ "$ziel" = "--markdown" ] && { markdown=1; ziel=""; }

if [ -z "$ziel" ]; then
  proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"
  ziel=$(ls -t "$proj"/*.jsonl 2>/dev/null | head -1)
fi

if [ ! -f "$ziel" ]; then
  echo "Keine Sitzungsdatei gefunden. Aufruf: session-kosten.sh [datei.jsonl|--markdown]"
  exit 1
fi

SESS="$ziel" MD="$markdown" python3 <<'PY'
import json, os, datetime

pfad = os.environ["SESS"]

def ortszeit(stempel):
    """Die Sitzungsdatei speichert UTC. Der Nutzer denkt in seiner Uhr."""
    if not stempel:
        return "--:--"
    try:
        t = datetime.datetime.fromisoformat(stempel.replace("Z", "+00:00"))
        return t.astimezone().strftime("%H:%M")
    except Exception:
        return stempel[11:16]

# Nicht jede Zeile vom Typ "user" ist eine Nachricht des Menschen. Werkzeug-
# Ergebnisse, Agenten-Fertigmeldungen, Skill-Ladungen und System-Erinnerungen
# tragen denselben Typ — sie gehören zum LAUFENDEN Abschnitt, nicht in einen neuen.
# Ohne diesen Filter zerfällt die Tabelle in lauter Systemzeilen.
MASCHINE = ("<task-notification>", "<system-reminder>", "Caveat:",
            "Base directory for this skill:", "<local-command-",
            "[Request interrupted", "API Error")
md = os.environ.get("MD") == "1"

# Preisfaktoren, normiert auf frische Eingabe
F_LESEN, F_SCHREIBEN, F_AUSGABE, F_EINGABE = 0.1, 2.0, 5.0, 1.0

wellen = []          # je Abschnitt: {start, text, anfragen, ...}
aktuell = None

def neue_welle(zeit, text):
    return {"zeit": zeit, "text": text, "anfragen": 0,
            "lesen": 0, "schreiben": 0, "ausgabe": 0, "eingabe": 0, "kontext": 0}

for zeile in open(pfad, "rb").read().decode("utf-8", "ignore").splitlines():
    try:
        d = json.loads(zeile)
    except Exception:
        continue
    m = d.get("message") or {}
    zeit = ortszeit(d.get("timestamp"))

    # Eine ECHTE Nutzernachricht startet einen neuen Abschnitt. Werkzeug-Ergebnisse
    # sind technisch auch "user", zählen hier aber nicht — sie sind Teil der Arbeit.
    if d.get("type") == "user":
        c = m.get("content")
        echt = isinstance(c, str) or (
            isinstance(c, list)
            and not any(isinstance(p, dict) and p.get("type") == "tool_result" for p in c)
        )
        if echt:
            roh = c if isinstance(c, str) else " ".join(
                p.get("text", "") for p in c if isinstance(p, dict))
            sauber = " ".join(roh.split())
            if sauber.startswith(MASCHINE):     # Systemzeile → kein neuer Abschnitt
                continue
            # Der eigene Zeitstempel des Nutzers sagt mehr als der Anfang seines Satzes.
            kurz = sauber[:56] or "(leer)"
            if aktuell:
                wellen.append(aktuell)
            aktuell = neue_welle(zeit, kurz)
            continue

    u = m.get("usage")
    if not u:
        continue
    if aktuell is None:                       # Anfragen vor der ersten Nachricht
        aktuell = neue_welle(zeit, "(Sitzungsstart)")
    aktuell["anfragen"] += 1
    aktuell["lesen"] += u.get("cache_read_input_tokens", 0)
    aktuell["schreiben"] += u.get("cache_creation_input_tokens", 0)
    aktuell["ausgabe"] += u.get("output_tokens", 0)
    aktuell["eingabe"] += u.get("input_tokens", 0)
    stand = (u.get("cache_read_input_tokens", 0)
             + u.get("cache_creation_input_tokens", 0))
    if stand:                       # Zeilen ohne Cache-Werte den Stand nicht auf 0 reissen
        aktuell["kontext"] = stand

if aktuell:
    wellen.append(aktuell)

def aequivalent(w):
    return (w["lesen"] * F_LESEN + w["schreiben"] * F_SCHREIBEN
            + w["ausgabe"] * F_AUSGABE + w["eingabe"] * F_EINGABE)

def k(n):
    return f"{n/1000:.0f}k" if n >= 1000 else str(int(n))

kopf = ("| # | Zeit | Worum es ging | Anfr. | Kontext | gelesen | geschr. | Ausgabe | Äquiv. |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|")
print(kopf[0]); print(kopf[1])

for i, w in enumerate(wellen, 1):
    print(f"| {i} | {w['zeit']} | {w['text']} | {w['anfragen']} | {k(w['kontext'])} | "
          f"{k(w['lesen'])} | {k(w['schreiben'])} | {k(w['ausgabe'])} | {k(aequivalent(w))} |")

g = {s: sum(w[s] for w in wellen) for s in ("anfragen", "lesen", "schreiben", "ausgabe", "eingabe")}
g_aeq = sum(aequivalent(w) for w in wellen)
print(f"| **Σ** | | **{len(wellen)} Abschnitte** | **{g['anfragen']}** | "
      f"**{k(wellen[-1]['kontext'])}** | **{k(g['lesen'])}** | **{k(g['schreiben'])}** | "
      f"**{k(g['ausgabe'])}** | **{k(g_aeq)}** |")

if not md:
    print()
    teuerste = max(wellen, key=aequivalent)
    anteil_ausgabe = g["ausgabe"] * F_AUSGABE / max(1, g_aeq) * 100
    trefferquote = g["schreiben"] / max(1, g["lesen"]) * 100
    print(f"Teuerster Abschnitt:  #{wellen.index(teuerste)+1} um {teuerste['zeit']} "
          f"({k(aequivalent(teuerste))} Äquivalente, {teuerste['anfragen']} Anfragen)")
    print(f"Anfragen je Nachricht: {g['anfragen']/max(1,len(wellen)):.1f} im Schnitt")
    print(f"Anteil eigene Ausgabe: {anteil_ausgabe:.0f} % der Gesamtkosten")
    print(f"Cache-Trefferquote:    {trefferquote:.1f} % geschrieben (unter 10 % = warm)")
PY
