# Autorisierte Wellen: Oberchef → Wächter → Arbeiter

Der Oberchef liest die vollständigen Eingänge und schreibt den Plan als Datei,
bevor er delegiert: ID, vollständiger Auftrag mit Originalbelegen, Abnahme,
Modell/Effort, Basiscommit, Dateibesitz, Worktree/Branch, Abhängigkeiten,
Ressourcen-/Bauzuständigkeit und Berichtspfad. Der Plan bleibt für den Nutzer
in der vereinbarten TextEdit-Gruppe lesbar. Keine zusätzlichen Aufträge erfinden.

Ein Wächter erhält seine abgegrenzte Tabelle und reicht vollständige Briefe an
Arbeiter weiter. Er koordiniert, integriert, prüft Belege und schreibt einen
kurzen Bericht. Neue Befunde gehören als offene Punkte in den Bericht. Der
Oberchef integriert die geprüften Ergebnisse und führt den Gesamtabgleich durch.
Kleine zusammenhängende Arbeit braucht keinen zusätzlichen Wächter.

Höchstens vier Wächter zugleich; die tatsächliche Gesamtzahl von Hauptsession,
Wächtern und Arbeitern muss in Host-Slots und Rechnerressourcen passen. Beispiel:
bei vier gesamten Slots können Oberchef + ein Wächter + zwei Arbeiter laufen;
Oberchef + drei wartende Wächter hätten keinen Arbeiterslot. Zusätzliche Themen
werden gestaffelt. Keine Shell-Agenten als Umgehung einer Host-Begrenzung starten.
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
