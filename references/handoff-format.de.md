# Handoff-Format

<!-- rule:HF-01 -->
## Neue Revision, klarer Eingang

Erzeuge für jede Übergabe eine neue datierte Datei. Überschreibe nie eine beantwortete Quelle. Setze eine kopierbare erste Zeile mit dem absoluten Pfad der neuen Datei. Im RTF-Zwilling ist diese erste Zeile der eigene absolute RTF-Pfad als Link; der MD-Pfad erscheint dort nicht (`scripts/handoff-rtf.sh` tauscht ihn; Nutzer 28.09.2026, 02:52). Das MD behält seinen eigenen Pfad. Nenne Projekt, Datum und Revision im Titel.

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

1. **Erhaltene Nutzereingaben:** vollständige wörtliche Sammlung dessen, was seit der vorherigen Revision neu ist, ohne Deutung; ältere Originale nur per Verweis (HF-08).
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

**Ein neues Handoff direkt in `handoff-archiv/` anlegen**, nicht zuerst im
Projektstamm und später verschieben: Jeder Umzug bricht bereits verlinkte Pfade.
Markdown und angeforderte RTF-Zwillinge entstehen von Anfang an dort. Die
Zwischenrufe-Datei bleibt als `.md` im Projektstamm; der Nutzer räumt sie selbst weg.

<!-- rule:HF-05 -->
## Vollständig lesen, nicht gefiltert (14.09.2026)

Lies das vorherige Handoff ungefiltert von der ersten bis zur letzten Zeile, bevor du das neue schreibst. Nie lange Zeilen abschneiden, nie nur nach `>>>Userantwort:` greppen, nie „zum Token-Sparen" filtern — genau so verschwinden roter Faden, Roadmap, Messung, Hauptdokumente, Gedächtnis und Logbuch aus der Nachfolgerevision. Zu große Dateien in Blöcken lesen, aber vollständig. Und: am Wellenende nicht auf eine weitere Agentenmeldung warten; offene Meldungen gehören unter „Laufend und offen", sie halten den Abschluss nicht auf.

<!-- rule:HF-06 -->
## Vollständige Abschnittsfolge (verbindlich, 14.09.2026; Kopfzeile ergänzt 15.09.2026)

Die acht Pflichtabschnitte oben sind das Minimum. Die ausgelieferte Reihenfolge lautet:

1. **Kopf mit Kopierzeile** — Zeile 1 der eigene Pfad, Zeile 2 der Stand (HF-01),
   darunter eine einzige, vollständig markierbare Zeile, die der
   Nutzer ohne Nachbearbeitung in den Chat kopieren kann:
   `Ich habe das Handoff bearbeitet: <absoluter Pfad zur .rtf>`
   Sie ergänzt die erste Pfadzeile und ist KEINE Goldzeile — kein `>>>`
   davor (Yasin 14.09.2026 23:14: die `>>>`-Zeile im Kopf „macht keinen Sinn";
   Yasin 15.09.2026 23:04: „oben schreiben wir doch eigentlich normalerweise hin,
   ich habe das Handoff bearbeitet, und dann kommt der Handoff-Link, damit ich nur
   noch das kopieren kann"). Die erste `>>>Userantwort:` gehört unter die erste
   Frage — 2. Bearbeitungshinweis — 3. Der Stand in drei Sätzen — 4. Ziel und
   Autorisierung — 5. Verifizierter Stand — 6. Laufend und offen — 7. Sammlung des
   Nutzers, wörtlich, nach Quelle getrennt, nur neue Eingaben (HF-08) — 8. Was ich daraus gemacht habe —
   9. Entscheidungen und Fragen mit `>>>Userantwort:` — 10. Testliste mit
   `>>>Userantwort:` je Punkt — 11. Der rote Faden — 12. Kurz-Roadmap —
   13. Messung der Welle — 14. Hauptdokumente und weitere Dokumente —
   15. Gedächtnis (Langzeit/Kurzzeit) — 16. Logbuch —
   17. `SAMMLUNG FÜR DAS NÄCHSTE HANDOFF`.

Fehlt einer, ist das Handoff nicht fertig. Vor dem Rendern die Liste gegen die Datei prüfen.


<!-- rule:HF-07 -->
## Die Zwischenrufe-Datei als Markdown beantworten

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und öffnen, nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen.

Bei unveränderter Änderungszeit die Datei nicht neu öffnen oder beschreiben. Bei geändertem Stand ohne neue Nutzereingaben „nein“ vermerken. Kurzes sofort beantworten, Längeres in die nächste Welle einplanen.

<!-- rule:HF-08 -->
## Nur neue Eingaben wörtlich übernehmen, Älteres verlinken (04.10.2026)

Die wörtliche Sammlung enthält nur, was der Nutzer **nach dem vorherigen Handoff**
neu eingegeben hat: dessen Sammlungs-Fußbereich, die Zwischenrufe-Datei der Welle
und die Chatnachrichten der Welle. **Antworten, Fragen und Testantworten aus den
Antwortfeldern des Vorgängers werden NICHT wörtlich wiederholt** — weder als
Abschnitt „<Kennung> — neue Antworten“ noch in der Sammlung. Sie erscheinen nur
unter „Was ich daraus gemacht habe“, eine Zeile je Punkt mit Quelle:

`F2 → Skill gekürzt, Regel HF-08 geschärft (Quelle: _handoff-<projekt>-<datum>-CL, F2)`

Yasin, 06.10.2026, 02:42 (T34): „Ich brauch nicht, dass du die alten Handoff-Dateien
Fragen und Antworten und Tests mitnimmst“; ebenso 04.10.2026, 23:43: „keine
Wiederholungen vom alten Handoff“. `sammlung-pruefen.sh` verlangt deshalb nur den
Sammlungsfuß wörtlich, prüft für die Antwortfelder den Verweis auf den Vorgänger
und meldet wörtlich wiederholte Antworten (ab 40 Zeichen) als Befund. Originale, die der Vorgänger selbst schon aus früheren
Revisionen übernommen hatte, werden NICHT noch einmal kopiert. Sie bleiben im
archivierten Vorgänger, der nie geändert oder gelöscht wird. Eine Zeile ersetzt sie:

`Ältere Originale: <absoluter Pfad des Vorgängers>, Abschnitt „<Name>“`

Begründung in Yasins Worten (04.10.2026, 17:01): „was bringt es uns denn, wenn es
im Handoff drin ist, das haben wir doch schon im alten Handoff drin“. Gemessen am
Handoff, das die Regel ausgelöst hat: 110 kB, ein großer Teil davon zum zweiten
und dritten Mal kopierte Originale.

Drei Bedingungen halten das verlustfrei:

1. **Jeder noch offene Wunsch aus einem älteren Original bekommt eine eigene Zeile
   unter „Laufend und offen“**, mit Quelle (Handoff-Revision und Uhrzeit). Ein
   Wunsch, der nur in einem alten Original steht, ist verloren, weil die nächste
   Sitzung das neue Handoff liest und nicht die Kette dahinter.
2. **Das Lesen bleibt vollständig (HF-05).** Gespart wird im neuen Dokument, nicht
   beim Lesen des Vorgängers.
3. **Der Verweis muss auflösbar sein.** Fehlt der Vorgänger oder wurde er
   verschoben, werden seine Originale noch einmal wörtlich übernommen, statt ins
   Leere zu verweisen.

`scripts/sammlung-pruefen.sh` prüft aus demselben Grund nur den direkten Vorgänger.

<!-- rule:HF-09 -->
## Kennung, Kopf und Nachträge (02.10.2026)

Eine Revision trägt ihre Kennung überall gleich: im Dateinamen (`…-2026-10-02-r.md` und `.rtf`), im Titel, in der Kopierzeile und im Bearbeitungshinweis. Der Kopf lautet: Zeile 1 der eigene absolute Pfad, Zeile 2 `Stand:` aus `date`, dann `Ich habe das Handoff bearbeitet: <eigener .rtf-Pfad>`, dann der Titel.

- Eine neue Revision entsteht nie als Kopie der vorigen, in der nur die Pfadzeile ersetzt wird. Wer kopiert, ersetzt jeden Selbstverweis (Titel, „Antworten bitte im …“, „x ersetzt y“, Messzeile, Dokumentliste) und prüft danach. Beleg: Handoff r der Website-Session trug Titel „(q)“ und schickte die Antworten nach q.
- Ein Nachtrag nach dem Rendern kommt ins Markdown und wird eine neue Revision über `scripts/handoff-rtf.sh`. Nie direkt ins RTF schreiben: sonst laufen MD und RTF auseinander, und wer das nächste Handoff aus dem MD schreibt, verliert den Nachtrag.
- Vor dem Rendern und danach `scripts/handoff-pruefen.py <handoff.md>` laufen lassen; es prüft Pfad, Stand, Kennung, Kopierzeile, Selbstverweise im Kopf und die Abschnittsfolge. Beantwortete Vorgänger als gespeichertes RTF an `scripts/sammlung-pruefen.sh` übergeben, denn das Agenten-MD enthält die Antworten nicht.

Siehe auch [Wellen-Ausführung](wave-execution.de.md), [Beleggrenzen](evidence-scope.de.md) und [RTF unter macOS](rtf-macos.de.md).

Pfad- und Standzeilen jedes Dokuments folgen RT-05 in [RTF unter macOS](rtf-macos.de.md).

### Zeitstempel auf jede NEUE Anfrage

Die erste Zeile der ersten Antwort auf eine neue Nutzernachricht trägt
`Name, TT.MM.JJJJ-HH:MM`, nicht jede Zwischenmeldung derselben Antwortkette.
Die Zeit kommt nur aus `date "+%d.%m.%Y-%H:%M"`, niemals aus einer Schätzung.

Das gilt für **jede** neue Nutzernachricht, auch für einen Zwischenruf, den der Chef als neue
Anfrage beantwortet, und in langen Sessions genauso wie bei der ersten Antwort: Der Nutzer zählt
an diesen Stempeln seine Anfragen (08.10.2026 22:35: „Der signalisiert mir halt, wie viel Anfragen
das insgesamt waren“).

<!-- rule:HF-10 -->
## Das Archiv behält das RTF; die Sammlung bleibt (Nutzer, 08.10.2026)

- **RTF-Handoffs bleiben dauerhaft im Archivordner** als Dokumentation des Projekts. Neue
  Handoffs entstehen dort (WH-04), verschoben wird also nie.
- **Markdown-Quellen darf der Nutzer selbst löschen; der Agent löscht nie** ein Handoff, weder MD
  noch RTF.
- **Die wörtliche Sammlung bleibt in jedem Handoff** (nur neue Eingaben, HF-08). „Was ich daraus
  gemacht habe“ ist die kompakte Deutung daneben, kein Ersatz; der Nutzer will beides
  (22:53: „dann lass man das lieber so“).
