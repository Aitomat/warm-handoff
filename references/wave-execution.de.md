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
## Ausführung und Integration

Starte unabhängige Pakete nur gemeinsam, wenn der Host es unterstützt. Arbeiter müssen stoppen, bevor sie fremde Dateien anfassen. Ein Ergebnisbericht nennt geänderte Pfade, Tests, Belege, Grenzen und ungelöste Abhängigkeiten. Die Integration prüft den Diff und führt die kleinsten aussagekräftigen Kombinationsprüfungen erneut aus. Eine Startmeldung oder Arbeiterbehauptung ist kein Abnahmebeleg.

<!-- rule:WV-05 -->
## Kommunikation

Nutze die automatische Fertigmeldung des Hosts für Routineergebnisse. Melde echte Blocker, Entscheidungen mit Umfangsänderung oder wesentliche Risiken. Halte den Nutzerfaden auf Entscheidungen und belegte Ergebnisse ausgerichtet. Nutzeranweisungen haben für den jeweiligen Ablauf Vorrang vor allgemeinen Delegationsempfehlungen.

Siehe [Codex](codex.de.md), [Claude Code](claude-code.de.md), [Modellrouting](model-routing.de.md) und [Beleggrenzen](evidence-scope.de.md).
