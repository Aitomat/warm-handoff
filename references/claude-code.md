# Claude Code — aktiver Arbeitsablauf

Dieser Adapter erhält den gelebten Claude-Ablauf: Antworten sammeln → vollständigen
Wellenplan schreiben → autorisierte Wächter/Arbeiter ausführen → Ergebnisse prüfen
und integrieren → neues Handoff in TextEdit. Er ist eine aktive Anleitung, kein
Verweis auf einen stillgelegten Workflow. Gemeinsame Details stehen in
[Handoff-Format](handoff-format.md), [Wellen](wave-execution.md) und
[RTF/TextEdit](rtf-macos.md); diese aktuellen Regeln gelten vor alten Beispielen.

## Einstieg und Durchführung

Beim Aufruf oder Sessionstart im entsprechend vereinbarten Projekt zuerst den
bezeichneten neuesten Handoff, vorhandene Vorgänger, RTF-Antworten, Zwischenrufe
und Nachträge lesen. Deutsche Nutzeroriginale erhalten; frühere Testantworten
wörtlich übernehmen und jede Umsetzung/Zurückstellung belegen. Kurze Steuerung
im Chat berücksichtigen, ohne die autorisierte Welle zu vergessen.

Der Oberchef plant die vollständigen Arbeitspakete. Unabhängige Pakete gehen
direkt an Arbeiter; ein Wächter koordiniert nur bei
zusätzlichem internem Bedarf. Kurze selbstständige Briefe und tatsächliche
Host-Slots/Rechnerressourcen bestimmen die Ausführung. Alle schreibenden
Rollen bekommen isolierte Worktrees und Dateibesitz. Modell/Effort aus Yasins
aktuellem Profil in Brief und sichtbarer Rollenbezeichnung festhalten. Vorliegende
Claude-Agent- und Fortsetzungsfunktionen verwenden, keine versionsfremde API
voraussetzen. Zusätzliche Codex-Zweitmeinung nur mit verfügbarer, autorisierter
Brücke; unabhängiges Review braucht nicht zwingend einen anderen Anbieter.

Wächter reichen vollständige Aufträge weiter, prüfen Rückgaben, integrieren nach
Plan und liefern einen Bericht. Teure Builds/Tests seriell im gemeinsamen Lock
durch die dafür benannte Rolle. Das Hauptrepo wechselt keinen Branch. Ein Commit
je Auftrag; nur die beauftragte Rolle veröffentlicht bei bestehender Erlaubnis.
Langläufer mit ID und Berichtspfad im Zwischenstand erhalten, nicht vergessen.

Gespeicherte Zwischenrufe an natürlichen Kontrollpunkten und vor Handoff erneut lesen.
Speichern ist das Übergabesignal; ungespeicherte Entwürfe gemäß
[Handoff-Format](handoff-format.md) standardmäßig nicht lesen oder importieren.
Rückmeldungen gehen in eine
neue Antwort-/Quittungsdatei mit Quellenrevision und Zeitpunkt und anschließend
in den nächsten Handoff. Der alte `zwischenrufe-antwort.sh` ist ein Legacy-Helfer,
der offene Dokumente speichern/schließen kann: im aktuellen sicheren Ablauf nicht
verwenden. Stattdessen Originale lesend erfassen, neue Antwortdatei schreiben.
Kein Reload, Speichern oder Schließen offener Nutzerdateien durch den Agenten.

## Übergabe und TextEdit

Der Handoff enthält alle Blöcke aus [Handoff-Format](handoff-format.md), darunter
Tank, ursprüngliche Sammlung, Verarbeitung, alte Tests, neue Testliste, Fragen,
roter Faden, Haupt-/weitere Dokumente, Werkzeuge, Gedächtnis und Kostentabelle.
Die Kopierzeile steht ganz oben. Nutzer antworten im RTF unter `>>>Userantwort:`.
Das RTF ist eine neue editierbare Antwortfassung, keine ersetzbare Druckansicht.
Der Konverter bewahrt Unicode und prüft Text sowie tatsächliche Hyperlink-Felder.

Alle erwähnten Lesedokumente in der aktiven TextEdit-Tabgruppe oder einer neuen
gemeinsamen Gruppe öffnen. Keine fremden Gruppen vereinigen, keine globalen
Tab-Einstellungen ändern, eigene leere Hilfstabs entfernen. Die Originaldateien
bleiben erhalten. Lange Diktate und Pasted Content aus Claude, Codex oder cmux
vollständig importieren; ein zusammengeklappter Terminalmarker ist kein Text.

## Kontext, Kosten und Belege

Zeitstempel nur aus frischer Uhrabfrage; Kontext/Kontingent nur mit Messquelle
und Alter. Claude-Session- und Agentenverbrauch getrennt erfassen. Das Repository
enthält historische Messskripte; deren Voraussetzungen und Sessionzuordnung vor
Nutzung prüfen. Keine Kosten oder TTL allein aus dem damaligen Pro/Max-Profil
ableiten, keine zusätzlichen Aufträge nur zum Kontingentverbrauch starten.
Cache als Optimierung behandeln, gespeicherten Zwischenstand als Gedächtnis.

Bei drohendem Kontextverlust oder längerer Pause den überprüften Stand sichern
und bei Bedarf einen frischen Lauf fortsetzen lassen. Keine universellen
200k/400k-Grenzen, Keepalive-Pings oder automatischen Modell-/Settingswechsel.
Die ursprünglichen ausführlichen [englischen](claude-workflow-history.md) und
[deutschen](claude-workflow-history.de.md) Fassungen mit historischen Begründungen
bleiben vollständig lesbar. Zahlen darin sind historische Beobachtungen, keine
aktuellen Preis-, Rechte- oder Installationsanweisungen.
