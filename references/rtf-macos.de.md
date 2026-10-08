# RTF unter macOS

<!-- rule:RT-01 -->
## Sichere Erzeugung

RTF ist ein optionaler editierbarer Zwilling eines vom Agenten geschriebenen Markdown-Handoffs. Er benötigt macOS, Python 3, Bash und `textutil`.

Erzeuge angeforderte Handoff-RTFs ausschließlich über `scripts/handoff-rtf.sh`, aus dem Repository oder installierten Skillverzeichnis mit absoluten Quell-/Zielpfaden. Baue RTF nicht von Hand nach und rufe `render_rtf.py` nicht direkt auf; `textutil` dient nur dem Lesen und Prüfen.

Cmd-S gibt gespeicherte Nutzereingaben innerhalb der bestehenden Autorisierung frei. Halte genau einen aktiven Zwischenrufe-Eingang: Handoff-Fußbereich oder vereinbarte Datei; der andere Ort verlinkt nur darauf. Archiviere beantwortete Handoffs im Archivordner des Projekts per `mv`, nie `rm`; verschiebe nicht die aktive Nutzereingabedatei.

**Lege ein neues Handoff direkt im Archivordner an.** Schreibe es nicht in den Projektstamm und verschiebe es später — jedes Verschieben ändert einen Pfad, unter dem das Dokument bereits verlinkt wurde. Also von Anfang an `<projekt>/handoff-archiv/_handoff-<projekt>-<datum>-<kennung>.md` und `.rtf` (Ordner mit `mkdir -p` anlegen, falls er fehlt); der Nutzer löscht dort selbst, was er nicht braucht. **Die Zwischenrufe-Datei bleibt im Projektstamm**, wo der Nutzer sie von Hand wegräumt.

```sh
scripts/handoff-rtf.sh /projekt/docs/handoff.md /projekt/handoff.rtf --project-root /projekt
```

Der Ausgabepfad muss neu sein. Der Renderer verweigert bestehende Dateien und Symlinks, schreibt über eine temporäre Datei, prüft Klartext und Hyperlinkfelder und veröffentlicht exklusiv. Relative Links werden gegen `--project-root`, sonst die nächste `.git`-Markierung, sonst das Markdown-Verzeichnis aufgelöst. Ausdrückliche fehlende Markdownlinks und lokale Pfade schlagen fehl, statt tote Links zu werden.

<!-- rule:RT-02 -->
## Wörtliche Eingänge und Links

Umschließe erhaltenen Nutzertext mit `<!-- user-original:start -->` und `<!-- user-original:end -->`. Sein sichtbarer Text bleibt wörtlich. Markdownlinks, unterstützte Dokumentmarker, URLs, Pfade in Inline-Code und echte absolute Pfade bleiben Linkkandidaten. Schrägstrich-Komposita wie `Root-/Arbeiterverbrauch` oder `Token-/Kosten-Telemetrie` sind Fließtext und dürfen nicht als Wurzelpfade gelesen werden.

Agententext setzt `**fett**` als Fettdruck; Markdown-Tabellen werden als beschriftete Zeilen mit umbrechenden Zellen ausgegeben. Nutzeroriginale, Antwortfelder und Code bleiben wörtlich.

<!-- rule:RT-03 -->
## Goldene Antwortfortsetzung

Zeilen, die mit `>>>` beginnen, und alle folgenden nichtleeren Fortsetzungszeilen sind goldene 18-Punkt-Antwortabsätze. Eine Leerzeile erhält ebenfalls Gold und beendet die Antwort; eine Überschrift, Codeblockgrenze oder `<!-- answer:end -->` beendet sie vor dem nächsten Absatz. Trenne Agententext immer durch eine dieser Grenzen. Für Nutzertext über Leerzeilen hinweg oder mit wörtlichem Markdown nutze einen `user-original`-Block: Jede Zeile darin ist golden. Eingabe in einem goldenen Absatz, Return, Speichern und erneutes Öffnen müssen den fortgesetzten Nutzertext golden und in 18 pt erhalten. Ein späterer Agentenabsatz darf keinen Antworthintergrund haben.

Der automatisierte AppKit-Test deckt diesen Ablauf beim Speichern und Neuladen ab. Eine manuelle TextEdit-Prüfung bleibt getrennt, weil Start oder Fokus des Editors den Desktop des Nutzers stören können.

Der **Dokumentstandard** trägt dasselbe 18 pt Gold, damit eingefügter Klartext
und getippter Text es erben und nicht auf den RTF-Urstandard 12 pt ohne
Hintergrund zurückfallen. Der Kopf setzt dafür einen `Normal`-Stylesheet-Eintrag
und denselben Zeichenzustand vor dem ersten Absatz; Agentenabsätze, Überschriften
und Codeblöcke setzen mit `\pard\plain\f0\cf2` zurück. Nutze den vollständigen
GOLD-Zustand unten für Cocoa-Zeichenschattierung; `\highlight` allein reicht nicht, und `\cb0` wird
als Schwarz gelesen statt als „kein Hintergrund"; `\plain` ist deshalb der
einzige saubere Reset. Beleg über `textutil -convert html -stdout DATEI.rtf`: die
Antwortklasse trägt 18 px Schrift und den goldenen Hintergrund, Agententext
keinen.

<!-- rule:RT-03b -->
## Schwarz auf Gold, 18 pt, für Text hinter `>>>` (Beleg W58-E1, 13.09.2026)

Tippen oder Einfügen (Cmd-V) am Ende eines goldenen Antwortabsatzes muss
schwarze Schrift auf Gold in 18 pt bleiben. Cocoa färbt nur auf Zeichenebene,
der Renderer nutzt daher alles Folgende. Dies sind Prüfkriterien für den
mitgelieferten Renderer, keine Erlaubnis für einen anderen Erzeugungsweg:

- Farbtabelle `;gold;schwarz;` — Gold ist Eintrag 1 (`\red255\green231\blue153`),
  Schwarz ist Eintrag 2;
- `GOLD = \cb1\cbpat1\chshdng0\chcbpat1\highlight1\cf2` — `\chshdng0\chcbpat1`
  ist das Einzige, was Cocoa auf Zeichenebene färbt, und `\cf2` erzwingt
  schwarze Schrift, damit Nutzertext nie Gold auf Gold wird;
- `RESET = \plain\f0\cf2` — `\cb0` wird als Schwarz gelesen statt als „kein
  Hintergrund"; `\plain` ist deshalb der einzige saubere Reset;
- Antwortabsätze werden als `RESET + \fs36 + GOLD` geschrieben; `\fs36` = 18 pt.

Beleg W58-E1: Testdatei per osascript in TextEdit geöffnet, Cursor ans
Dokumentende, `keystroke "Test 123"`, gespeichert — das RTF am Einfügepunkt
lautet `\fs36 \cf0 \cb2 >>> … Test 123`, dabei `\cb2` das Gold
`\red255\green231\blue153` und `\cf0` auto/schwarz; `textutil -convert txt`
liefert den Text vollständig.

<!-- rule:RT-04 -->
## Drei Belegbereiche

- Renderer-Roundtrip: erzeugter Text und Hyperlinkfelder.
- TextEdit-/AppKit-Fortsetzung: Eingabe und Absatzstil nach Speichern/Neuladen.
- Einfügen in Anwendung: Verhalten in der Zielanwendung.

Leite keinen Bereich aus Belegen eines anderen ab. Dateien öffnen, Tabs zusammenführen oder TextEdit-Fenster steuern ist nur mit autorisierter UI-Steuerung erlaubt. Überschreibe nie das beantwortete RTF des Nutzers.

<!-- rule:RT-05 -->
## Pfadzeile ganz oben in jedem Dokument

Jedes Dokument, das entsteht oder überarbeitet wird — Plan, Bericht, Konzept,
Roadmap, Handoff, Zwischenrufe-Datei —, beginnt mit **seinem eigenen absoluten
Pfad** als allererster Zeile, davor nichts, auch keine Überschrift. Darunter das
Stand-Datum, dann erst die Überschrift:

```markdown
/absoluter/pfad/zum/dokument.md
Stand: TT.MM.JJJJ, HH:MM

# Überschrift des Dokuments
```

Der Sinn: Der Nutzer kann die oberste Zeile kopieren und hat den Pfad gleich
mit, statt ihn zu suchen; wird ein Dokument verschoben, zieht die Zeile mit. Aus
demselben Grund stehen Pfade in Antworten immer vollständig ab der Wurzel.

<!-- rule:RT-06 -->
## Geöffnete Dokumente nach dem Ändern schließen und neu öffnen

TextEdit zeigt weiter den Stand, mit dem es die Datei geladen hat — eine
Änderung auf der Platte kommt dort nicht an. Wer eine Datei ändert, die offen
sein könnte, schließt sie darum **zuerst** und öffnet sie **danach** neu:

```sh
osascript -e 'tell application "TextEdit" to close (every document whose path contains "<dateiname>")'
open -a TextEdit "<voller pfad>"
```

Nur das eigene Dokument schließen, nie „alle Dokumente" — fremde offene Dateien
bleiben in Ruhe. Und nur schließen, was keine ungesicherten Eingaben enthält: Bei
der Zwischenrufe-Datei und beim Handoff erst lesen, was gespeichert ist, und sie
sonst offen lassen. Gilt für jedes Dokument, dessen Pfad in einer Antwort
genannt wird.

<!-- rule:RT-07 -->
## Zwischenrufe sind der Markdown-Eingang

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und in einem Editor öffnen, in den der Nutzer schreiben kann (macOS: `open -a TextEdit "<voller Pfad>"`, nie in einem reinen Lese-Viewer wie dem cmux-Markdown-Tab), nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

Zum sicheren Anhängen `scripts/zwischenrufe-antwort.sh` nutzen. Der Helfer prüft den exakten Dokumentpfad, verweigert RTF und unbekannten Editorstand und speichert niemals Nutzereingaben. Bei sicher gespeichertem Stand das eigene Dokument ohne Speichern schließen, nur anhängen und neu öffnen.
