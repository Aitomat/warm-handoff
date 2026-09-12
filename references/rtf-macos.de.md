# RTF unter macOS

<!-- rule:RT-01 -->
## Sichere Erzeugung

RTF ist ein optionaler editierbarer Zwilling eines vom Agenten geschriebenen Markdown-Handoffs. Er benötigt macOS, Python 3, Bash und `textutil`.

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
und Codeblöcke setzen mit `\pard\plain\f0` zurück. Cocoa und TextEdit lesen
`\highlight` überhaupt nicht — dort färbt nur `\cb`/`\cbpat` —, und `\cb0` wird
als Schwarz gelesen statt als „kein Hintergrund"; `\plain` ist deshalb der
einzige saubere Reset. Beleg über `textutil -convert html -stdout DATEI.rtf`: die
Antwortklasse trägt 18 px Schrift und den goldenen Hintergrund, Agententext
keinen. Dieselbe Goldregel gilt für die Zwischenrufe-RTF, nicht nur den Handoff.

<!-- rule:RT-04 -->
## Drei Belegbereiche

- Renderer-Roundtrip: erzeugter Text und Hyperlinkfelder.
- TextEdit-/AppKit-Fortsetzung: Eingabe und Absatzstil nach Speichern/Neuladen.
- Einfügen in Anwendung: Verhalten in der Zielanwendung.

Leite keinen Bereich aus Belegen eines anderen ab. Dateien öffnen, Tabs zusammenführen oder TextEdit-Fenster steuern ist nur mit autorisierter UI-Steuerung erlaubt. Überschreibe nie das beantwortete RTF des Nutzers.
