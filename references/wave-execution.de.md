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
L=/tmp/<projekt>-build.lock
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
## Ein einziger Bau-Slot

Es läuft genau EIN Build gleichzeitig. Die Grenze ist der Speicher, nicht die
Zahl der Agenten: einmal gemessen auf einem speichergebundenen Laptop, machten
zwei gleichzeitige Builds eines kompilierten Projekts die Maschine für Stunden
unbenutzbar, während zehn denkende Agenten kaum auffielen. Frühere Fassungen
dieses Skills erlaubten zwei Slots; ein Slot ersetzt sie.

- **Die Sperre gehört in das Testskript des Projekts, nicht in den Auftrag des
  Arbeiters.** Ein Auftrag ist eine Bitte — in einer gemessenen Welle bauten
  trotzdem sechs von vierzehn Arbeitsverzeichnissen gleichzeitig. Ein Skript ist
  ein Tor, durch das jeder Arbeiter muss.
- **Ein Abschlussbau zählt nur, wenn er die Tests erreicht hat.** Ein Lauf, der
  vor dem ersten Test abbricht (Werkzeug, Zwischenspeicher, Umgebung), ist kein
  Abschlussbau und wird wiederholt; wer nach seinem Lauf noch etwas ändert, fährt
  einen zweiten. Beide Läufe gehören in den Bericht. Die Regel spart Last; sie
  darf nie Belege unterdrücken.
- **Ein Build je Themenverantwortlichem, ganz am Ende** — nicht je Arbeiter. Der
  Verantwortliche sammelt die Arbeiterergebnisse ein und baut einmal über den
  integrierten Stand. Arbeiter und Subagenten bauen nicht, höchstens eine
  Syntax- oder Parse-Prüfung.
- **Zahl gleichzeitiger Arbeiter begrenzen** (vier ist auf einem einzelnen Laptop
  eine sinnvolle Obergrenze). Mehr ist nicht schneller, wenn ohnehin alle hinter
  einem Slot warten.
- Ein pausierter Build behält seinen Speicher; Pausieren hilft der CPU, nicht dem
  RAM. Die Antwort ist, den zweiten Build gar nicht erst zu starten.

Der Slot selbst, genommen, sobald höchstens ein Vorgänger noch offen ist:

```sh
TRASH=<Löschbar-Ordner des Projekts>          # nie rm; Leichen hierher verschieben
M=/tmp/<welle>-fertig; VOR="a b"              # meine Vorgänger in der Baureihenfolge
while [ "$(for v in $VOR; do [ -f $M-$v ] || echo x; done | wc -l)" -gt 1 ]; do sleep 30; done
L=""; while [ -z "$L" ]; do
  for s in 1; do C=/tmp/<projekt>-build-$s.lock
    if mkdir $C 2>/dev/null; then L=$C; break; fi
    P=$(cat $C/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $C 2>/dev/null
    [ -f $C ] && mv $C "$TRASH"/lock-leiche-$s-$$   # Datei-Leiche statt Verzeichnis
  done; [ -z "$L" ] && sleep 30
done; echo $$ > $L/pid; uptime
… Build + gezielte Tests …
rm -f $L/pid; rmdir $L; touch $M-<ich>
```

Ein Lock-Verzeichnis, dessen PID nicht mehr lebt, wird mit `rmdir` geräumt. Ein
Lock, das als DATEI statt als Verzeichnis existiert, ist eine Leiche: in den
Löschbar-Ordner des Projekts verschieben, nie `rm`. Warten im Vordergrund
(Wartebefehl wiederholen; Host-Timeout bis 600000 ms ist in Ordnung), nie
losgelöst, und nie vor dem Ende des Builds melden. Vor dem Build `uptime` ins
Log, und im Bericht Load-Average und Wanduhrzeit gegen die vorige Welle stellen.

## Ausführung und Integration

Starte unabhängige Pakete nur gemeinsam, wenn der Host es unterstützt. Arbeiter müssen stoppen, bevor sie fremde Dateien anfassen. Ein Ergebnisbericht nennt geänderte Pfade, Tests, Belege, Grenzen und ungelöste Abhängigkeiten. Die Integration prüft den Diff und führt die kleinsten aussagekräftigen Kombinationsprüfungen erneut aus. Eine Startmeldung oder Arbeiterbehauptung ist kein Abnahmebeleg.

<!-- rule:WV-05 -->
## Kommunikation

Nutze die automatische Fertigmeldung des Hosts für Routineergebnisse. Melde echte Blocker, Entscheidungen mit Umfangsänderung oder wesentliche Risiken. Halte den Nutzerfaden auf Entscheidungen und belegte Ergebnisse ausgerichtet. Nutzeranweisungen haben für den jeweiligen Ablauf Vorrang vor allgemeinen Delegationsempfehlungen. Prüfe bei jedem Aufwachen der Hauptsession die Änderungszeit der Zwischenrufe-Datei und lies sie, wenn sie sich geändert hat, bevor du handelst oder meldest.

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

<!-- rule:WV-07 -->
## Last begrenzen und messen (14.09.2026)

Bau-Slots begrenzen die Zahl der Builds, nicht die Zahl der Prozesse. Ein
einziger Build startet so viele Compilerprozesse, wie die Maschine Kerne hat —
zwei gleichzeitige Builds legen den Rechner des Nutzers lahm. Belegt am
14.09.2026 in Welle 62: zwei Bau-Slots auf zwölf Kernen ergaben sechzehn
Compilerprozesse und einen Load-Average von 104; der Nutzer konnte kaum noch
arbeiten.

Deshalb gilt zusätzlich zu den Slots:

1. **Jobzahl je Build begrenzen.** Höchstens ein Viertel der Kerne pro Build
   (bei zwölf Kernen `-j 3`), damit zwei Builds zusammen die Hälfte der Maschine
   frei lassen. Die Option gehört in den Auftrag jedes Arbeiters.
2. **Freundlich bauen.** Build und Tests mit niedriger Priorität starten
   (`nice -n 10`), damit die Oberfläche des Nutzers Vorrang behält.
3. **Vorher und nachher messen.** Load-Average vor dem Wellenstart und am Ende
   notieren und in die Messung der Welle schreiben. Steigt der Load über die
   Kernzahl, war die Welle zu breit — die nächste läuft mit weniger
   gleichzeitigen Arbeitern.
4. **Der Rechner gehört dem Nutzer.** Wird er spürbar langsam, ist das ein
   Blocker, kein Schönheitsfehler: laufende Builds herabstufen (`renice +15`)
   statt sie abzubrechen, und die Breite der Welle sofort reduzieren.

<!-- rule:WV-08 -->
## Ein Rauchtest vor der Welle (14.09.2026)

Bevor die Welle startet, lässt du EINEN Arbeiter den kleinsten echten Bau- und
Testlauf machen — nicht die Hauptsession, sondern einen Arbeiter unter genau den
Rechten, die alle bekommen werden. Erst wenn dessen Lauf kompiliert, starten die
übrigen.

Belegt am 14.09.2026: Ohne Rauchtest liefen vier Wächter los, alle vier
scheiterten an derselben Sandbox-Hürde, und die Ursache fiel erst nach einer
Stunde auf. Ein einzelner Rauchtest hätte sie in drei Minuten gezeigt. Dieselbe
Panne war schon in der Welle davor aufgetreten — in anderer Form, mit derselben
Wirkung: ungeprüfter Code.

Prüfe im Rauchtest drei Dinge und halte sie im Wellenplan fest: der Arbeiter
kann schreiben, wo das Werkzeug schreiben muss; er kann bauen und testen; sein
Prozess überlebt einen Abbruch der Hauptsession. Wiederhole den Rauchtest,
sobald sich Host, Modell oder Rechtevergabe ändern.

Zweite Lehre desselben Tages: Die Breite der Welle ist nicht das Problem, die
Last ist es. Mit begrenzter Jobzahl je Build (WV-07) laufen mehr Arbeiter
gleichzeitig, ohne den Rechner zu lähmen — zwölf Themen in drei Staffeln kosten
mehr Wanduhrzeit als zwölf in zwei.

<!-- rule:WV-09 -->
## Vorflug-Liste, bevor der erste Arbeiter startet

Diese Liste läuft einmal, bevor irgendein Arbeiter gestartet wird. Jeder Punkt
hat eine gemessene Welle Stunden gekostet, als er übersprungen wurde:

1. **Werkzeug-Zwischenspeicher vorbereiten.** Vorgebaute native Module, die die
   Agenten-CLI braucht, gehören vor der Welle in ihren Plugin-Zwischenspeicher;
   sonst stößt jeder Arbeiter seine eigene Paketinstallation an (einmal gemessen:
   rund 1500 Prozesse und ein Load-Average von 148). Dasselbe gilt für
   Compiler-Zwischenspeicher: überholte vorher umbenennen oder räumen, nicht
   mittendrin.
2. **Rauchtest in einem Verzeichnis, das kein Arbeiter benutzt.** Ändert ein
   Arbeiter die Datei, die der Rauchtest gerade übersetzt, ist der Rauchtest
   wertlos. Siehe WV-08.
3. **Die Toolchain-Umgebung ausdrücklich setzen**, vor dem Aufruf des Testskripts
   in zusätzlichen Arbeitsverzeichnissen, wo ein nackter Aufruf die falsche
   Toolchain erwischen kann.
4. **Die vier Rechtepunkte aus WV-06 klären** und in jeden Auftrag schreiben.
5. **Eine Regeldatei für die Arbeiter schreiben und versionieren** — die
   Wellennummer anhängen, die Datei nie kopieren. Eine kopierte Datei bringt
   Sätze zurück, die der Nutzer längst verboten hat. Arbeiter lassen fremde
   Restdateien liegen und committen immer mit ausdrücklicher Dateiliste, nie mit
   einem Sammel-Add.

<!-- rule:WV-10 -->
## Choreografie: je Thema starten, früh mergen, spät bauen

Warten kostet die Welle, nicht das Bauen. Gemessen mit einem Bau-Slot und zehn
Themen:

- **Jeden Arbeiter starten, sobald SEINE Vorarbeit fertig ist** (die
  Datei:Zeile-Liste seines Themas), nicht erst, wenn die ganze Welle geplant ist.
  Die Staffelung ergibt sich dann von selbst, und der erste Bau läuft nach
  wenigen Minuten.
- **Arbeiter bauen im Vordergrund und pollen nie im Hintergrund.** Die
  Bauwarteschlange ist stumm; ein Arbeiter, der Warteschleifen in den Hintergrund
  legt, weckt sich und seine Nachbarn immer wieder: Ein beobachteter Arbeiter
  erzeugte alle sechs Sekunden eine Schleife und trieb den Load über 40, ein
  fertiger Arbeiter wurde jedes Mal mit großem Kontext neu geweckt. Das Verbot
  gehört wörtlich in jeden Auftrag. Schleift ein Arbeiter trotzdem: anhalten,
  seine Schleifen beenden, seinen Abschlusstest selbst fahren — seine Commits
  sind sicher.
- **Gebaute Verzeichnisse wiederverwenden statt frischer Arbeitsverzeichnisse.**
  Ein kopiertes Bauverzeichnis wird an einem neuen Pfad nicht wiederverwendet
  (absolute Pfade darin), der erste Bau dort ist also ein Komplettbau — mit einem
  Slot sind fünf frische Arbeitsverzeichnisse Stunden Warteschlange. Ist ein
  Arbeiter fertig, das nächste Thema in SEINEM Verzeichnis abzweigen und
  inkrementell bauen. Ein Thema auf den Branch eines Vorgängers stapeln, wenn
  beide dieselbe Datei anfassen, und die Restprozesse des fertigen Arbeiters
  beenden, bevor sein Verzeichnis weitergenutzt wird (nach Shells suchen, deren
  Kommando seine Logdatei nennt, nicht nur nach dem Ordner).
- **Früh mergen, spät bauen.** Jedes fertige Thema sofort in den Wellen-Branch
  mergen, nur Merge, kein Bau; Konflikte zeigen sich dann einzeln. Merge-Nachricht
  ausdrücklich mitgeben: Die Standardnachricht verliert Pflicht-Trailer
  stillschweigend.
- **Dateigrenzen in jedem Auftrag nennen** („NICHT anfassen: …"). Sechs parallele
  Themen mit klaren Grenzen ergaben null Konflikte.
- **Nie Quellen in einem Verzeichnis ändern, in dem gerade ein Bau läuft.** Eine
  späte Korrektur kommt in ein freies gebautes Verzeichnis auf eigenem Branch und
  wird nach der Suite gemergt.

<!-- rule:WV-11 -->
## Die erste Vollsuite grün bekommen

Eine Welle ist nur so schnell wie ihre erste Vollsuite; in einer gemessenen Welle
waren sechs Themen in einer halben Stunde gebaut und gemergt und brauchten danach
vier Vollsuiten bis Grün. Die Hebel:

- **Vor dem Bau nach überholten Verträgen suchen.** Wer sichtbare Texte,
  Menütitel, Meldungen, Layout-Reihenfolgen, Asset-Maße oder die ANZAHL
  eingebauter Dinge ändert, durchsucht VOR dem Bau den Testbaum nach der alten
  Zeichenkette oder Bezeichnung, nimmt jeden Treffer in seinen Testfilter und
  stellt ihn auf den neuen, gleich scharfen Vertrag um. Der Chef wiederholt die
  Suche über alle Arbeiterberichte vor der ersten Vollsuite. Überholte Verträge in
  alten Tests sind die häufigste Ursache zusätzlicher Suiten.
- **Ein Test, der zweimal fällt, ist kein „Wackler unter Last", bis es bewiesen
  ist.** Ein wiederholt fallender Test entpuppte sich als echte Kollision in einem
  kurzen Zufallssuffix. Nie auf einer roten Vollsuite installieren, wie plausibel
  die Ausrede auch klingt.
- **Ein Themenfilter deckt ältere Tests nicht ab, die ein Arbeiter außerhalb
  davon geändert hat.** Sie gehören in die Merge-Notizen; die Vollsuite ist ihr
  erster echter Lauf.
- **Jedes „nicht gefunden" eines Agenten mit einer eigenen Suche gegenprüfen**,
  bevor darauf gehandelt wird.
- **Beweis vor Auftrag.** Bei Absturz oder Hänger zuerst den Absturzbericht und
  das Diagnoseprotokoll der Anwendung lesen; der Auftrag nennt die Ursache dann
  als bewiesen, wahrscheinlich oder vermutet. Themen, die auf Vermutungen liefen,
  kosteten ganze Wellen; ein bewiesener Backtrace war in Minuten behoben.

<!-- rule:WV-12 -->
## Eine Welle abschließen

Alle Arbeiter fertig **und** Vollsuite grün heißt: ohne Rückfrage abschließen —
bauen, selbst testen, tauschen, veröffentlichen und das Handoff schreiben.
Gefragt wird nur beim unsauberen Abschluss — rote Tests, ungeklärter Befund, ein
blockiert gemeldeter Arbeiter —; dann kein Artefakt, sondern die Frage, mit dem,
was fehlt, und einem Vorschlag.

Den Selbsttest am fertigen Artefakt selbst fahren, nicht am Arbeitsstand, bevor
es installiert wird, und den Exit-Code direkt aus dem Lauf abgreifen statt aus
einer Zusammenfassungszeile, die abgeschnitten oder umgeschrieben sein kann.

Der Eingang folgt derselben Uhr wie die Welle: Zwischen Handoff und Wellenstart
ist das Handoff der einzige Eingang; die Zwischenrufe-Datei entsteht mit dem
Wellenstart und ist bis zum nächsten Handoff der einzige Eingang.

Siehe [Codex](codex.de.md), [Claude Code](claude-code.de.md), [Modellrouting](model-routing.de.md) und [Beleggrenzen](evidence-scope.de.md).
