# Autorisierte Wellen: direkte Arbeiter, Wächter nach Bedarf

Der Oberchef liest die vollständigen Eingänge und schreibt den Plan als Datei,
bevor er delegiert: ID, vollständiger Auftrag mit Originalbelegen, Abnahme,
Modell/Effort, Basiscommit, Dateibesitz, Worktree/Branch, Abhängigkeiten,
Ressourcen-/Bauzuständigkeit und Berichtspfad. Der Plan bleibt für den Nutzer
in der vereinbarten TextEdit-Gruppe lesbar. Keine zusätzlichen Aufträge erfinden.

Kleine zusammenhängende Aufgaben lokal erledigen, unabhängige Pakete bei
vorhandener Autorisierung direkt an Arbeiter vergeben. Ein Wächter ist nur
sinnvoll, wenn ein Paket zusätzliche interne Koordination benötigt. Die tatsächlichen
Host-Slots bestimmen die Parallelität; Slots für ausführende Arbeiter freihalten.
Jeder Brief bleibt kurz und selbstständig verständlich: Originalbelege, Freigabe,
Basis, Dateibesitz, Grenzen, Abnahme und Berichtspfad. Vererbten Gesamtverlauf nur
nutzen, wenn er erforderlich ist. Der Hauptagent prüft Artefakte und Gesamtergebnis.
Keine Shell-Agenten als Umgehung einer Host-Begrenzung starten.

Automatisch zugestellte Agentenmeldungen bevorzugen. Währenddessen unabhängige
Arbeit erledigen; sonst einen vom Host unterstützten ereignisbezogenen Wartevorgang
innerhalb seiner Kommunikations- und Wartegrenzen nutzen. Keine kurzen wiederholten
Statusabfragen ohne neuen Entscheidungsanlass. Fehlende Artefakte, Fehler oder
Unterbrechungen können eine gezielte Zustandsprüfung erfordern.

Modelle/Effort aus dem Auftrag verwenden und sichtbar benennen, nicht wechseln,
um Kontingent aufzubrauchen. Echte Nutzungswerte je Lauf separat erfassen.

Jeder schreibende Lauf arbeitet in einem isolierten Worktree mit geprüftem
Basiscommit und explizitem Dateibesitz. Kein Zweigwechsel im Hauptrepo, kein
ungefragtes Pull/Rebase vom freigegebenen Stand. Fremde Änderungen erhalten.
Vor Wiederholung eines fehlgeschlagenen Laufs Zustand, Bericht und Prozess-ID
prüfen; keinen zweiten Schreiber auf denselben Auftrag ansetzen.

Teure Builds/Tests nur durch die im Plan benannte Rolle, seriell hinter dem
vereinbarten gemeinsamen Projekt-Lock. Existierendes fremdes Lock nie entfernen.
Arbeiter dürfen nur ausdrücklich zugeteilte günstige Prüfungen ausführen.
Ein Dokumentationsauftrag baut keine App. Ressourcenknappheit reduziert die
Parallelität; sie rechtfertigt keine konkurrierenden Vollbuilds.

Ein Commit je Auftrag, explizite Dateipfade stagen. Integration und unabhängiges
Review nach Auftrag; passende Prüfungen am integrierten Ergebnis. Nach dem dritten
Fehlanlauf erst die belegte Diagnose, dann ein weiterer begründeter Versuch.
Push nur bei bestehendem ausdrücklichem Auftrag und durch die benannte Rolle;
Veröffentlichung erst mit geprüftem Remote-Beleg melden. Git-/Sandbox-Blockaden
mit erhaltenem Arbeitsstand berichten, keine Umgehung und keine erfundenen Hashes.

Ein Zwischenstand darf laufende Arbeiter mit beobachteter Zeit/ID/Berichtspfad
aufführen. Er ist keine Fertigmeldung. Keine Überwachung oder Fortsetzung nach
Sessionende versprechen, die der Host nicht tatsächlich unterstützt.
