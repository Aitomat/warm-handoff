# RTF und TextEdit — Antwortdateien erhalten, Tabgruppe gezielt nutzen

## Neue RTF sicher erzeugen

RTF ist die editierbare Nutzerquelle. Speichern ist das Übergabesignal; vor der
nächsten Version die gesamte gespeicherte Revision nach [Handoff-Format](handoff-format.md)
abgleichen und Originale wörtlich erhalten. Ungespeicherte Entwürfe bleiben ohne
ausdrücklich gewählten Live-Modus außerhalb des Eingangs; keinen Editor-Live-Read ausführen.
Niemals offene oder andere bestehende Nutzerdateien überschreiben, speichern,
schließen oder verschieben. Der Renderer verweigert jedes vorhandene Ziel,
einschließlich Symlinks. Er steuert keinen Editor und ändert keine Einstellungen.

```sh
scripts/handoff-rtf.sh /projekt/docs/handoff-neu.md /projekt/handoff-neu.rtf --project-root /projekt
```

Python 3 und macOS `textutil` sind nötig; kein pandoc, HTML oder Netzwerkzugriff.
Die Projektwurzel explizit angeben, wenn bekannt. Ohne Option gilt die nächste
übergeordnete `.git`-Markierung (Verzeichnis oder Worktree-Datei), ansonsten das
Markdown-Verzeichnis. Relative **explizite Links und nackte Dokumentpfade** werden
gegen diese Basis absolut aufgelöst, nie gegen einen temporären Konverterordner.
Bei quellrelativen Links ausdrücklich `--project-root` auf das Quellverzeichnis
setzen. Mehrdeutige Basen nicht erraten. Lokale explizite Linkziele müssen existieren;
die exakt gerade erzeugte neue RTF darf sich in der Kopierzeile selbst verlinken.

Pfade mit Leerzeichen als `[Label](<docs/Fragen an Yasin.md>)`, in Backticks oder
als `⟦Screenshot: /absoluter/Pfad mit Leerzeichen.png⟧` schreiben. Prozentkodierte
`file:///`-URIs funktionieren. Web-Links bleiben Web-Links; andere Schemes und
entfernte file-Hosts werden abgewiesen. Nicht existierende nackte relative Namen
bleiben Text; für beabsichtigte Dokumentverweise explizite Links verwenden.
`⟦Kopie: „beliebiger zitierter Text“⟧` bleibt wortgetreu; nur ein gültiges Webziel
oder tatsächlich vorhandenes Dateiziel wird verlinkt. Dokumentmarker wie
`⟦Dokument: RG.pdf — ~/Downloads/RG.pdf⟧` verlinken den Pfad nach dem Trenner,
während der vollständige Marker sichtbar unverändert bleibt.

Der konservative Markdown-Umfang umfasst Überschriften, Listen-/Tabellenzeilen,
Codeblöcke, Inline-Code, Links und Antwortmarker. Zeilen und Unicode bleiben
lesbar; komplexe Markdown-Formatierung kann als sichtbare Syntax stehen bleiben.
Codeblöcke werden nicht als Dateiverweise interpretiert. 18 pt Grundschrift,
größere fette Überschriften, goldener Hintergrund der `>>>`-Antwortabsätze. Die Kopierzeile ist eine logische
Zeile; ihre optische Breite hängt vom Fenster ab. Originalquellen bleiben erhalten.

Erst nach erfolgreichem `textutil`-Textroundtrip und Prüfung aller erzeugten
HYPERLINK-Felder wird die vollständige Datei atomar veröffentlicht. Ein Fehler
hinterlässt kein neues Ziel. Tests: `python3 -m unittest discover -s tests -v`.
Diese Checks beweisen noch keine UI-Bedienbarkeit: Lesbarkeit, Linkklicks,
Kopierzeile und Antwortspeicherung im Viewer zusätzlich prüfen oder offen nennen.
Ein Dokument ohne lokale Links ist zulässig; `grep -c file://` ist keine Abnahme.

## Alle Lesedokumente in einer passenden Tabgruppe öffnen

Im vereinbarten Dokumentablauf alle im Bericht/Handoff erwähnten nutzerseitigen
Lesedokumente öffnen, nicht nur den Handoff. Nicht-textuelle Belege bei Bedarf
im passenden Viewer; keine Binärdateien als Text öffnen. Existierende Dokumente
anhand voller Pfade und sichtbarem Zustand zuordnen, nie nur nach Dateinamen.

1. Vorhandene TextEdit-Fenster/-Tabs und aktive Gruppe lesend erfassen. Die aktive
   Gruppe des Auftrags nutzen. Falls keine passende Gruppe existiert, eine neue
   gemeinsame Gruppe für die Auftragsdokumente herstellen. Fremde Gruppen erhalten.
2. Vorhandene verlässliche Tab-Öffnungsfunktion des aktuellen Hosts bevorzugen;
   sichtbare UI nach jedem abhängigen Schritt abwarten. Nicht voraussetzen, dass
   mehrere `open`-Aufrufe automatisch derselben Gruppe beitreten.
3. **Am 10.09.2026 durch die Hauptsession per CUA geprüft:** Im Ziel-Einzelfenster
   `Darstellung → Tableiste einblenden`, sichtbares `+` / „Neuer Tab“ anklicken.
   Dies erzeugt einen eigenen leeren Hilfstab in dieser Gruppe. Von dort `⌘O`,
   `⇧⌘G`; auf das sichtbare Pfadfeld warten und dessen Wert vollständig setzen
   (`setValue` des beobachteten Feldes). Return, auf aktualisierten Öffnen-Dialog
   warten, „Öffnen“ anklicken. Die Datei erschien als dritter Tab neben Plan und
   Hilfstab in derselben Gruppe. Für weitere Dokumente Zustand neu prüfen.
4. Den eindeutig selbst erzeugten Hilfstab **zuerst auswählen**, seine leere
   Textansicht prüfen und erst dann `⌘W` drücken. Ein Klick auf den Schließen-Knopf
   ohne Auswahl entfernte ihn im Versuch nicht zuverlässig. Die Hauptsession
   bestätigte danach fünf echte Dokumente gemeinsam, ohne leeren Rest.
   Keine Nutzerfenster oder unsicheren/ungesicherten Dokumente schließen.
   Falls ein eigener leerer Fensterrest entstanden ist, nur diesen nach eindeutiger
   Zuordnung entfernen. Kein neuer leerer Tab/Fensterrest darf unbemerkt bleiben.
5. Erfolg am tatsächlichen Zustand prüfen: erwartete Dokumentpfade/-tabs gemeinsam,
   fremde Gruppen unverändert, kein eigener leerer Rest. Aktuellen Host-Tools folgen;
   die Schritte sind ein geprüfter Fallback, keine Garantie jeder TextEdit-Version.

**Nie „Alle Fenster zusammenführen“ / `mergeAllWindows` verwenden.** Dies würde
fremde Gruppen einsammeln. Kein blindes `⌘⌥N`: im beobachteten Fall entstand ein
leeres Fenster. Direktes `typeText` nach `⇧⌘G` verlor im Versuch den Pfadpräfix;
deshalb sichtbares Feld abwarten und gezielt vollständig befüllen. Keine globalen
`defaults write`-Änderungen. Ist Gruppierung oder UI-Steuerung nicht verfügbar,
Dateien liefern und exakt die offene Gruppierung/Viewer-Prüfung dokumentieren.

## Goldene Antwortflächen

Im vereinbarten Aitomat-Profil bezeichnet Gold den Absatzhintergrund von
Nutzerantworten, nicht die Schriftfarbe. Normal große, lesbare Schrift erhalten.
Mehrzeilige Originale vollständig hervorheben, Agentenantworten getrennt lassen.
Vor Rendereränderungen vorhandene Formatierung prüfen; diese Regel ist kein
Beleg, dass jede bestehende Vorlage bereits alle Folgeabsätze korrekt hervorhebt.
Rendererformatierung und interaktives Einfügen in TextEdit separat an einer neuen
Datei oder wegwerfbaren Probe prüfen. Bloße RTF-Steuercodes beweisen keine behobene
Viewer-Störung. Keine bestehende Antwortdatei pauschal umfärben oder überschreiben.
