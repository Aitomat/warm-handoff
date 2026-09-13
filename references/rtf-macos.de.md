# RTF unter macOS

<!-- rule:RT-01 -->
## Sichere Erzeugung

RTF ist ein optionaler editierbarer Zwilling eines vom Agenten geschriebenen Markdown-Handoffs. Er benötigt macOS, Python 3, Bash und `textutil`.

Erzeuge Handoff- und Zwischenrufe-RTFs ausschließlich über `scripts/handoff-rtf.sh`, aus dem Repository oder installierten Skillverzeichnis mit absoluten Quell-/Zielpfaden. Baue RTF nicht von Hand nach und rufe `render_rtf.py` nicht direkt auf; `textutil` dient nur dem Lesen und Prüfen.

Cmd-S gibt gespeicherte Nutzereingaben innerhalb der bestehenden Autorisierung frei. Halte genau einen aktiven Zwischenrufe-Eingang: Handoff-Fußbereich oder vereinbarte Datei; der andere Ort verlinkt nur darauf. Archiviere beantwortete Handoffs im `handoff-archiv/` desselben Projekts per `mv`, nie `rm`; verschiebe nicht die aktive Nutzereingabedatei.

```sh
scripts/handoff-rtf.sh /projekt/docs/handoff.md /projekt/handoff.rtf --project-root /projekt
```

Der Ausgabepfad muss neu sein. Der Renderer verweigert bestehende Dateien und Symlinks, schreibt über eine temporäre Datei, prüft Klartext und Hyperlinkfelder und veröffentlicht exklusiv. Relative Links werden gegen `--project-root`, sonst die nächste `.git`-Markierung, sonst das Markdown-Verzeichnis aufgelöst. Ausdrückliche fehlende Markdownlinks und lokale Pfade schlagen fehl, statt tote Links zu werden.

<!-- rule:RT-02 -->
## Wörtliche Eingänge und Links

Umschließe erhaltenen Nutzertext mit `<!-- user-original:start -->` und `<!-- user-original:end -->`. Sein sichtbarer Text bleibt wörtlich. Markdownlinks, unterstützte Dokumentmarker, URLs, Pfade in Inline-Code und echte absolute Pfade bleiben Linkkandidaten. Schrägstrich-Komposita wie `Root-/Arbeiterverbrauch` oder `Token-/Kosten-Telemetrie` sind Fließtext und dürfen nicht als Wurzelpfade gelesen werden.

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
keinen. Dieselbe Goldregel gilt für die Zwischenrufe-RTF, nicht nur den Handoff.

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
