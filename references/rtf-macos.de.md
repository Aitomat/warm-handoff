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

Zeilen, die mit `>>>` beginnen, sind goldene 18-Punkt-Antwortabsätze. Der leere Absatz direkt nach einem Marker erhält denselben Stil. Eingabe dort, Return, Speichern und erneutes Öffnen müssen den fortgesetzten Nutzertext golden und in 18 pt erhalten. Ein späterer Agentenabsatz darf keinen Antworthintergrund haben.

Der automatisierte AppKit-Test deckt diesen Speicher- und Save/Reload-Ablauf ab. Eine manuelle TextEdit-Prüfung bleibt getrennt, weil Start oder Fokus des Editors den Desktop des Nutzers stören können.

<!-- rule:RT-04 -->
## Drei Belegbereiche

- Renderer-Roundtrip: erzeugter Text und Hyperlinkfelder.
- TextEdit-/AppKit-Fortsetzung: Eingabe und Absatzstil nach Speichern/Neuladen.
- Einfügen in Anwendung: Verhalten in der Zielanwendung.

Leite keinen Bereich aus Belegen eines anderen ab. Dateien öffnen, Tabs zusammenführen oder TextEdit-Fenster steuern ist nur mit autorisierter UI-Steuerung erlaubt. Überschreibe nie das beantwortete RTF des Nutzers.
