# W55-R6: Goldhintergrund über Cocoa-Speichern erhalten

Befund: Eine mit `\cbpat1\highlight1` erzeugte künstliche Antwort verliert beim
Cocoa-Roundtrip (`textutil`, RTF → RTF) ihre Hintergrundfarbe. `\cb1` erhält sie.
Der bisherige reine TXT-Roundtrip konnte diesen Verlust nicht erkennen.

Der öffentliche Renderer ergänzt `\cb1`, verwendet das vereinbarte Gold
RGB 255/231/153 und unterstützt explizite mehrzeilige Nutzeroriginalblöcke.
Darin bleiben Markdown und Pfadtext wörtlich. Agentenantworten erhalten keinen
Goldhintergrund. Fehlende, zusätzliche oder verschachtelte Blockmarker verhindern
eine Veröffentlichung; Markerbeispiele in Codeblöcken bleiben normaler Text.

TDD: Zuerst vier neue Regressionen, davon drei erwartungsgemäß fehlgeschlagen
(Hintergrundverlust, fehlende Literalblöcke, ungeschütztes Blockende).
Nach schmalem Patch bestehen alle 23 Renderer-Tests. Neue Prüfungen reimportieren
RTF über Cocoa, exportieren HTML und prüfen Hintergrundfarbe, Schriftgröße,
Folgeabsätze sowie Abgrenzung zur Agentenantwort. Bestehende Schutzprüfungen für
Originaldateien und atomare Veröffentlichung bleiben grün.

Keine persönlichen Skills installiert, keine Nutzerdateien geändert, keine App
geöffnet. Die nächste neue AW-Datei muss mit diesem Renderer erzeugt werden.
Native TextEdit-Eingabe/Paste und die Darstellung im geöffneten Dokument bleiben
bis zur tatsächlichen Prüfung offen. Veröffentlichung übernimmt Root nach Review.
