# Autorisierte Arbeitswellen

<!-- rule:WV-01 -->
## Autorisierung und Plan

Eine Welle beginnt erst, nachdem der Nutzer Ziel und Nebenwirkungen autorisiert hat. Speichere vor dem Start der Arbeiter einen Plan. Halte je Paket fest: ID, Ergebnis, exklusive Pfade, Abhängigkeiten, Akzeptanzkriterien, gegebenenfalls Modell oder Effort, verbotene Aktionen und Berichtspfad.

<!-- rule:WV-02 -->
## Kapazität und Besitz

Lies die tatsächliche Agentenübersicht des Hosts und die Maschinengrenzen. Versprich nie mehr Parallelität als vorhanden. Jeder beschreibbare Pfad gehört genau einem Agenten. Teile nach Dateien und unabhängig prüfbaren Ergebnissen. Serialisiere Builds, gemeinsamen Testzustand, veränderliche Dienste, Integration und Veröffentlichung.

<!-- rule:WV-03 -->
## Direkte Arbeiter und optionaler Wächtermodus

Direkte Arbeiter eignen sich für unabhängige Pakete. Wächter eignen sich für Pakete mit Koordination, Review oder Integration. Füge keine Wächterschicht nur für Bezeichnungen hinzu.

Bezeichne jeden Agenten im Plan und im Bericht gleich: `A · Thema · Modell/Effort`.

Teure Builds und Tests laufen hinter einem gemeinsamen Projekt-Lock, gehalten von
der im Plan benannten Rolle. Ein Verzeichnis-Lock ist atomar; die PID darin macht
ein verwaistes Lock nach einem Absturz erkennbar, ohne dass jemand ein fremdes
laufendes Lock entfernt:

```sh
L=/tmp/project-build.lock
while ! mkdir $L 2>/dev/null; do
  P=$(cat $L/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $L 2>/dev/null; sleep 30
done; echo $$ > $L/pid
… build/tests …; rm -f $L/pid; rmdir $L
```

**Warten heißt warten, nie melden.** Wer am Lock hängt, schreibt keinen
Zwischenbericht „blockiert" und startet keinen zweiten Versuch daneben. Tests
laufen über das Testskript des Projekts, nicht als roher Toolchain-Aufruf;
`TMPDIR=/tmp` setzen. **Ein Build je Themen-Wächter, ganz am Ende — nicht je
Arbeiter:** der Wächter sammelt die Arbeiterergebnisse ein und baut einmal über
den integrierten Stand. Wächter beenden ihre eigenen Warteschleifen und
Hintergrundprozesse, bevor sie den Bericht schreiben; ein Bericht neben einem
noch laufenden eigenen Hintergrundlauf ist kein Bericht.

Projekte können ausdrücklich den **Wächtermodus** wählen. Dann laufen substanzielle Recherche, Analyse, Umsetzung, QA, Sichtprüfung, Berichte und Handoff-Erstellung über einen Wächter mit seinen Arbeitern. Die Hauptsession beschränkt sich auf knappe Koordination, notwendige Entscheidungen und gebündelte Abnahme; sie dupliziert keine Detailarbeit parallel. Nutze kurze eigenständige Briefe und automatische Ergebniszustellung. Frage nicht vor 25 Minuten nach Status, außer es gibt einen echten Blocker. Fehlen Plätze, nenne die Hostgrenze und stelle die Arbeit an oder verkleinere die Welle, statt Doppelarbeit zu leisten.

<!-- rule:WV-04 -->
## Zwei Bau-Slots (Regel 4 v2, 13.09.2026)

Höchstens ZWEI Builds laufen gleichzeitig (Nutzer, 13.09.2026 03:23: „Zwei Builds
gleichzeitig erlauben bitte"; 04:00: „mehr wie zwei nicht"). Das ersetzt die
frühere Regel mit einem Lock und strenger Reihenfolge. Jeder Themen-Wächter baut
einmal am Ende seines Themas, nur mit seinen gezielten Tests; die Vollsuite
gehört dem Merge-Wächter, der auf ALLE Fertig-Marken wartet. Die Reihenfolge
läuft vom größten zum kleinsten Thema. Ein Wächter nimmt einen freien Slot,
sobald höchstens EIN Vorgänger noch ohne Fertig-Marke ist:

```
TRASH=<Löschbar-Ordner des Projekts>          # nie rm; Leichen hierher verschieben
M=/tmp/<welle>-fertig; VOR="a b"              # meine Vorgänger in der Reihenfolge; A: leer, B: "a"
while [ "$(for v in $VOR; do [ -f $M-$v ] || echo x; done | wc -l)" -gt 1 ]; do sleep 30; done
L=""; while [ -z "$L" ]; do
  for s in 1 2; do C=/tmp/aitomat-build-$s.lock
    if mkdir $C 2>/dev/null; then L=$C; break; fi
    P=$(cat $C/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $C 2>/dev/null
    [ -f $C ] && mv $C "$TRASH"/lock-leiche-$s-$$   # Datei-Leiche statt Verzeichnis (W58, 01:48)
  done; [ -z "$L" ] && sleep 30
done; echo $$ > $L/pid; uptime
… Build + gezielte Tests …
rm -f $L/pid; rmdir $L; touch $M-<ich>
```

Ein Lock-Verzeichnis, dessen PID nicht mehr lebt, wird mit `rmdir` geräumt. Ein
Lock, das als DATEI statt als Verzeichnis existiert, ist eine Leiche (beobachtet
W58, 01:48): in den Löschbar-Ordner des Projekts verschieben, nie `rm`. Warten im
Vordergrund (Wartebefehl wiederholen; Host-Timeout bis 600000 ms ist in Ordnung),
nie losgelöst, und nie vor dem Ende des Builds melden. Arbeiter und Subagenten
bauen nicht (`swiftc -parse` höchstens). Vor dem Build `uptime` ins Log, und im
Bericht Load-Average und Wanduhrzeit gegen die vorige Welle stellen.

## Ausführung und Integration

Starte unabhängige Pakete nur gemeinsam, wenn der Host es unterstützt. Arbeiter müssen stoppen, bevor sie fremde Dateien anfassen. Ein Ergebnisbericht nennt geänderte Pfade, Tests, Belege, Grenzen und ungelöste Abhängigkeiten. Die Integration prüft den Diff und führt die kleinsten aussagekräftigen Kombinationsprüfungen erneut aus. Eine Startmeldung oder Arbeiterbehauptung ist kein Abnahmebeleg.

<!-- rule:WV-05 -->
## Kommunikation

Nutze die automatische Fertigmeldung des Hosts für Routineergebnisse. Melde echte Blocker, Entscheidungen mit Umfangsänderung oder wesentliche Risiken. Halte den Nutzerfaden auf Entscheidungen und belegte Ergebnisse ausgerichtet. Nutzeranweisungen haben für den jeweiligen Ablauf Vorrang vor allgemeinen Delegationsempfehlungen.

<!-- rule:WV-06 -->
## Rechte, die Bauagenten wirklich brauchen (14.09.2026)

Ein Arbeiter, der nicht bauen darf, liefert ungeprüften Code — das ist teurer als
jede gesparte Freigabe. Kläre diese vier Punkte, BEVOR die Welle startet, und
schreibe sie in den Auftrag jedes Arbeiters:

1. **Schreibrecht auf die Werkzeug-Zwischenspeicher.** Compiler und Paketmanager
   schreiben außerhalb des Arbeitsverzeichnisses (z. B. `~/.cache`). Fehlt das
   Recht, stirbt jeder Testlauf vor der Übersetzung. Beim Host ausdrücklich
   mitgeben (bei Codex: `--add-dir`), nicht hoffen.
2. **Verschachtelte Sandkästen auflösen.** Läuft der Agent schon in einer
   Sandbox, kann ein Werkzeug darin keine zweite aufspannen. Typischer Beleg:
   `sandbox_apply: Operation not permitted`. Lösung ist die Option des
   Werkzeugs, seine eigene interne Prüfung auszulassen — nicht das Abschalten
   der Host-Sandbox. Diese Option gehört wörtlich in den Auftrag, mit dem
   Zusatz: fehlgeschlagene Versuche zählen nicht gegen die Einmal-Bau-Regel.
3. **Zwischencommits vorschreiben.** Arbeiter, die erst am Ende committen,
   verlieren bei jedem Abbruch die ganze Arbeit. Nach jedem abgeschlossenen
   Punkt committen; am Ende darf zusammengefasst werden.
4. **Prozesslebensdauer klären.** Hintergrundprozesse der Hauptsession können
   mit ihr sterben. Prüfe, ob die gestarteten Arbeiter einen Abbruch der
   Hauptsession überleben, und starte lange Läufe nicht neben Abbruch-gefährdeten
   Hintergrundbefehlen.

Belegt am 14.09.2026 in Welle 62: drei Arbeiter lieferten ungeprüften Code
(Punkt 2), drei weitere verloren je eine Viertelstunde Arbeit (Punkte 3 und 4).

Siehe [Codex](codex.de.md), [Claude Code](claude-code.de.md), [Modellrouting](model-routing.de.md) und [Beleggrenzen](evidence-scope.de.md).
