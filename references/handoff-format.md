# Handoff erstellen und fortsetzen

Deutsch ist das vereinbarte Profil; eine ausdrückliche andere Sprachwahl geht vor.
Die erste nutzbare Zeile lautet ohne manuellen Zeilenumbruch:
`Ich habe das Handoff beantwortet: /absoluter/Pfad/zum/neuen-handoff.rtf`.
Titel, gemessene Zeit samt Zeitzone und Vorgänger folgen. Ein optischer Umbruch
bei schmalem Fenster darf die kopierte Zeile nicht verändern.

## Eingänge verlustsicher übernehmen

Explizit den bezeichneten Handoff, beide Vorgänger soweit vorhanden, RTF-Antworten,
Zwischenrufe, Chat-Steuerung und referenzierten Pasted Content lesen. Keine Quelle
anhand des neuesten Änderungsdatums erraten. Quelle, gelesene Revision/Hash und
Zeitpunkt festhalten. Originale unverändert in eine neue Datei übernehmen;
Interpretation, Antwort und Umsetzung separat zuordnen. Wiederholungen und
Widersprüche bleiben erkennbar. Jede frühere Testantwort einzeln verfolgen.

Vor Dateizugriffen vorhandene Editorinformationen berücksichtigen: gespeichertes
RTF mit `textutil -convert txt -stdout DATEI.rtf` lesen; bekannte ungesicherte
Änderungen sind damit nicht gelesen. Falls zugänglich Live-Text lesend erfassen,
sonst die Eingabelücke markieren und unabhängige Arbeit fortsetzen. Niemals die
Antwortdatei zum Einlesen automatisch speichern, schließen oder neu erzeugen.
Zwischenrufe vor Ergänzungen, nach neuen Nachrichten, bei natürlichen Wartephasen
und spätestens nach zehn Minuten aktiver Arbeit erneut lesen. Quittungen separat
neu anlegen; keine konkurrierenden Schreibzugriffe auf den aktiven Eingang.

`[Pasted text]` oder `Pasted Content` in Claude, Codex oder cmux ist kein Ersatz
für den tatsächlichen Text. Zugehörige Datei/Anlage öffnen und Originale übernehmen.
Fehlt sie, den betreffenden Eingang ausdrücklich offenlassen. Lange Diktate gehören
in die vereinbarte Sammlung; kurze Steuerung darf im Chat bleiben.

## Gliederung für die nächste neue Version

Den Vorgänger aktualisieren; für den ersten Einstieg dienen diese Pflichtblöcke:

1. Kopierzeile oben, Titel/Zeit/Vorgänger, Hinweise auf `>>>Userantwort:`.
2. **Der Stand in drei Sätzen**: Ziel, überprüfter Stand, nächste Aktion;
   Modus Zwischenstand / fortsetzbar / abgeschlossen und gültige Autorisierung.
3. **Was noch im Tank ist**: Messquelle/-alter/-umfang oder „nicht gemessen“.
4. **Erwartete Agenten-Ergebnisse**: IDs, Besitzer, beobachteter Status,
   Worktree/Branch/Basis, Berichtspfad und bekannte Laufzeitgrenzen.
5. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** und
   **Was ich daraus gemacht habe**: Zuordnung jedes Originals zu Status/Beleg.
6. **Vorige Testantworten — was daraus wurde** und **Testliste vN**:
   durchgeführt / fehlgeschlagen / manuell offen, Schritte und Erwartung,
   leere `>>>Userantwort:`-Felder. Kein offener Test gilt als bestanden.
7. **Fragen an dich** mit `>>>Antwort:` und klarer Trennung von optionalen
   Fragen und Entscheidungen, die den nächsten Schritt tatsächlich sperren.
8. **Der rote Faden**, **Hauptdokumente**, **Weitere Dokumente**, **Aktive
   Werkzeuge dieses Projekts**: echte Pfade und tatsächliche Verfügbarkeit.
9. **Gedächtnis**: je vier bis sechs konkrete Langzeit- und Kurzzeitpunkte.
10. **Kostentabelle**: Quelle, Alter, Haupt-/Arbeiteranteile und Messlücken;
    eine Zeile im vereinbarten Projektlogbuch, keine globale Datei ungefragt ändern.
11. Ganz zuletzt **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF**, Ursprungspfad und `>>>`.

Genau einen aktiven Sammlungseingang benennen: RTF-Fußbereich oder vereinbarte
Zwischenrufe-Datei. Am anderen Ort darauf verlinken. Vor Übergabe alle Quellen
auf Nachträge prüfen, Originale Punkt für Punkt abgleichen und lokale Links
prüfen. Vorhandene `sammlung-pruefen.sh`-Heuristik ist kein Vollständigkeitsbeweis;
auch Antworten außerhalb erkannter Abschnitte direkt abgleichen.
Berichte mit echten Commit-/Push-Belegen und offenen Resten übergeben.
RTF-Erstellung und Öffnen folgen [RTF/TextEdit](rtf-macos.md).

## Zukunftsfaden bei dokumentengeführter Zusammenarbeit

Wenn der Nutzer kommende Wellen im Handoff verfolgt, den „roten Faden“ aus den
beiden Vorgängern und den referenzierten Plänen ausdrücklich abgleichen. Offene
Zukunftspunkte nicht durch eine pauschale Roadmap-Verweisung ersetzen. Für die
nächsten drei bis vier sinnvollen Arbeitspakete Ziel, konkrete Restpunkte,
Abhängigkeiten und Status nennen: freigegeben, vorgeschlagen, Entscheidung offen
oder erledigt mit Beleg. Frühere Wellennummern sind historische Planung; eine
Umordnung samt Grund sichtbar erklären. Keine zusätzlichen Wellen erfinden, wenn
nur weniger belegt sind. Entfernte oder vertagte Themen mit Grund erhalten.

Den detaillierten Ausblick nahe dem Dokumentende vor der abschließenden Sammlung
platzieren; je künftigem Paket ein optionales Antwortfeld für Ergänzungen und
Prioritäten anbieten. Offene Produktentscheidungen einzeln weiterführen. Alte
Freigaben, Modelle oder Wächterzahlen nicht aus der Zukunftsliste ableiten.
Eine neue Idee bleibt Vorschlag, bis ihr Umfang zur Umsetzung freigegeben ist.
