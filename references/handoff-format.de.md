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

Siehe auch [Wellen-Ausführung](wave-execution.de.md), [Beleggrenzen](evidence-scope.de.md) und [RTF unter macOS](rtf-macos.de.md).
