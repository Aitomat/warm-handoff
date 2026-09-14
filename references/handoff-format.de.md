# Handoff-Format

<!-- rule:HF-01 -->
## Neue Revision, klarer Eingang

Erzeuge für jede Übergabe eine neue datierte Datei. Überschreibe nie eine beantwortete Quelle. Setze eine kopierbare erste Zeile mit dem absoluten Pfad der neuen Datei. Nenne Projekt, Datum und Revision im Titel.

**Lies nur den gespeicherten Stand.** Das Speichern ist die Freigabe des Nutzers;
ungespeicherter Text in einem Editor ist nicht gelesen. Bitte um das Speichern
oder benenne die Lücke ausdrücklich als Lücke — speichere, schließe oder erzeuge
die Antwortdatei des Nutzers niemals neu, nur um sie einzulesen.

**Halte genau einen aktiven Sammlungseingang**, den einen Ort, an dem der Nutzer
antwortet und dazwischenruft: entweder den Sammlungsabschnitt der Antwortdatei
oder die vereinbarte Zwischenrufe-Datei. Der andere Ort verweist nur darauf. Zwei
parallele Eingänge verlieren Antworten.

<!-- rule:HF-02 -->
## Pflichtabschnitte

1. **Erhaltene Nutzereingaben:** vollständige wörtliche Sammlung aus der vorherigen Revision, ohne Deutung.
2. **Ziel und Autorisierung:** gewünschtes Ergebnis, erlaubte und verbotene Aktionen, Dateibesitz.
3. **Verifizierter Stand:** Branch/HEAD, geänderte Dateien, bestandene Prüfungen und Belegpfade.
4. **Laufend und offen:** gestartete Arbeit, Abhängigkeiten, unbekannter Stand und echte Blocker.
5. **Entscheidungen und Fragen:** nur Punkte, die Nutzerwahl brauchen; unter jeder Frage `>>>Userantwort:` plus leerer goldener Antwortabsatz.
6. **Abnahme:** kurze reproduzierbare Schritte, erwartetes Ergebnis und noch nicht belegte manuelle Prüfungen.
7. **Erinnerung:** wenige dauerhafte Regeln und sitzungsbezogene nächste Schritte, getrennt.
8. **Sammlung für das nächste Handoff:** ein eigener wörtlicher Nutzerbereich am Ende.

<!-- rule:HF-03 -->
## Original und Einordnung trennen

Nutze `<!-- user-original:start -->` und `<!-- user-original:end -->`, wenn der Renderer einen wörtlichen Block schützen soll. Ändere darin weder Rechtschreibung noch Reihenfolge. Schreibe Agentenantworten, Entscheidungen und Zusammenfassungen außerhalb. Ein Bytearchiv kann zusätzlich die unveränderte Quelle sichern; der lesbare Snapshot ersetzt es nicht.

<!-- rule:HF-04 -->
## Erledigt braucht Belege

Nenne eine Arbeit nur erledigt, wenn ein Artefakt, Commit, Status oder Test das Ergebnis belegt. „Gestartet“, „Datei vorhanden“ und Agentenmeldungen sind kein Endbeleg. Nenne für offene manuelle Prüfung den genauen offenen Schritt.

Beantwortete Handoffs nach `handoff-archiv/` des Projekts ablegen (anlegen, falls nicht vorhanden) und mit `mv` verschieben, nie mit `rm` (Yasin 13.09.2026 03:31). Ein neues Handoff ist immer eine NEUE Datei; das alte erst archivieren, wenn seine Antworten übernommen sind.

<!-- rule:HF-05 -->
## Vollständig lesen, nicht gefiltert (14.09.2026)

Lies das vorherige Handoff ungefiltert von der ersten bis zur letzten Zeile, bevor du das neue schreibst. Nie lange Zeilen abschneiden, nie nur nach `>>>Userantwort:` greppen, nie „zum Token-Sparen" filtern — genau so verschwinden roter Faden, Roadmap, Messung, Hauptdokumente, Gedächtnis und Logbuch aus der Nachfolgerevision. Zu große Dateien in Blöcken lesen, aber vollständig. Und: am Wellenende nicht auf eine weitere Agentenmeldung warten; offene Meldungen gehören unter „Laufend und offen", sie halten den Abschluss nicht auf.

<!-- rule:HF-06 -->
## Vollständige Abschnittsfolge (verbindlich, 14.09.2026)

Die acht Pflichtabschnitte oben sind das Minimum. Die ausgelieferte Reihenfolge lautet:

1. Kopierbarer absoluter Pfad — 2. Bearbeitungshinweis und `>>>Ich habe das Handoff bearbeitet:` — 3. Der Stand in drei Sätzen — 4. Ziel und Autorisierung — 5. Verifizierter Stand — 6. Laufend und offen — 7. Sammlung des Nutzers, wörtlich, nach Quelle getrennt — 8. Was ich daraus gemacht habe — 9. Entscheidungen und Fragen mit `>>>Userantwort:` — 10. Testliste mit `>>>Userantwort:` je Punkt — 11. Der rote Faden — 12. Kurz-Roadmap — 13. Messung der Welle — 14. Hauptdokumente und weitere Dokumente — 15. Gedächtnis (Langzeit/Kurzzeit) — 16. Logbuch — 17. `SAMMLUNG FÜR DAS NÄCHSTE HANDOFF`.

Fehlt einer, ist das Handoff nicht fertig. Vor dem Rendern die Liste gegen die Datei prüfen.


Siehe auch [Wellen-Ausführung](wave-execution.de.md), [Beleggrenzen](evidence-scope.de.md) und [RTF unter macOS](rtf-macos.de.md).
