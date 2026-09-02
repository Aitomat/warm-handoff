#!/usr/bin/env bash
# sammlung-pruefen.sh — mechanischer Schutz gegen verlorene Sammlungen.
#
# Warum es das gibt (Yasin, 02.09.2026): am 02.09. ist es ZWEIMAL passiert,
# dass die Sammlung des vorherigen Handoffs beim Schreiben des neuen nicht
# wörtlich übernommen wurde. Ein Mensch merkt das erst Stunden später.
# Dieses Skript vergleicht die `>>>`-Zeilen NACH dem SAMMLUNG-Banner der
# beiden Vorgänger-Handoffs mit dem neuen Handoff und gibt aus, was fehlt.
#
# Aufruf:
#   sammlung-pruefen.sh <neues-handoff.md> [vorgaenger1.md] [vorgaenger2.md]
#
# Ohne Vorgänger-Argumente werden die beiden Handoffs genommen, die im selben
# Verzeichnis nach Änderungszeit direkt vor dem neuen liegen
# (Muster `_handoff-*.md`, das neue selbst ausgenommen).
#
# Rückgabe: 0 = alles übernommen · 1 = Zeilen fehlen · 2 = Aufrufproblem.
# PFLICHTSCHRITT: vor dem Finalisieren jedes Handoffs laufen lassen.

set -u

neu="${1:-}"
if [ -z "$neu" ] || [ ! -f "$neu" ]; then
  echo "Aufruf: sammlung-pruefen.sh <neues-handoff.md> [vorgaenger1] [vorgaenger2]" >&2
  exit 2
fi

verz="$(cd "$(dirname "$neu")" && pwd)"
neu_abs="$verz/$(basename "$neu")"

if [ "$#" -ge 2 ]; then
  shift
  vorgaenger=("$@")
else
  vorgaenger=()
  while IFS= read -r f; do
    [ "$f" = "$neu_abs" ] && continue
    vorgaenger+=("$f")
    [ "${#vorgaenger[@]}" -ge 2 ] && break
  done < <(ls -t "$verz"/_handoff-*.md 2>/dev/null)
fi

if [ "${#vorgaenger[@]}" -eq 0 ]; then
  echo "Keine Vorgänger-Handoffs in $verz gefunden — nichts zu prüfen."
  exit 0
fi

# Sammlung = alle Zeilen ab dem SAMMLUNG-Banner bis Dateiende, die mit >>> beginnen
# oder Freitext des Nutzers sind. Wir vergleichen nur die inhaltlichen Zeilen.
# Wichtig: das Banner steht oft ZWEIMAL in der Datei — einmal im zitierten
# Block „Deine Sammlung aus dem letzten Handoff" und einmal am Ende als echte
# Sammlung. Es zählt IMMER das LETZTE Vorkommen.
sammlung() {
  awk '
    { zeile[NR]=$0; if ($0 ~ /SAMMLUNG FÜR DAS NÄCHSTE HANDOFF/) start=NR }
    END { if (start) for (i=start+1; i<=NR; i++) print zeile[i] }
  ' "$1" \
  | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' \
  | grep -v '^$' \
  | grep -v '^═\+$' \
  | grep -v '^▼\+' \
  | grep -v '^aus:' \
  | grep -v '^>>>Userantwort:$' \
  | grep -v '^>>>$'
}

# Der neue Handoff als Ganzes ist der Suchraum (die Sammlung kann in
# „wörtlich kopiert" ODER in „Was ich daraus gemacht habe" gelandet sein).
neu_text="$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' "$neu_abs")"

fehlt_gesamt=0
for v in "${vorgaenger[@]}"; do
  [ -f "$v" ] || { echo "übersprungen (nicht gefunden): $v"; continue; }
  echo "── Vorgänger: $v"
  anz=0; fehlt=0
  while IFS= read -r zeile; do
    [ ${#zeile} -lt 8 ] && continue        # zu kurz, um aussagekräftig zu sein
    anz=$((anz+1))
    kern="${zeile#>>>}"
    kern="$(printf '%s' "$kern" | sed -e 's/^[[:space:]]*//')"
    if ! printf '%s' "$neu_text" | grep -Fq -- "$kern"; then
      fehlt=$((fehlt+1))
      echo "   FEHLT: $zeile"
    fi
  done < <(sammlung "$v")
  echo "   $anz Sammlungszeilen geprüft, $fehlt fehlen."
  fehlt_gesamt=$((fehlt_gesamt+fehlt))
done

echo
if [ "$fehlt_gesamt" -eq 0 ]; then
  echo "OK — die Sammlungen beider Vorgänger sind im neuen Handoff enthalten."
  exit 0
fi
echo "ACHTUNG: $fehlt_gesamt Zeile(n) fehlen im neuen Handoff."
echo "Wörtlich nachtragen, NICHT umformulieren, dann erneut prüfen."
exit 1
