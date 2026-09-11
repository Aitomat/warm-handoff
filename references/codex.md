# Codex: Dokumente, Fortsetzungen und Wellen

Die verfügbaren Werkzeuge und geltenden Host-Grenzen bestimmen die Ausführung.
Native Unteragenten nur bei autorisiertem Auftrag; alternativ einen ausdrücklich
beauftragten CLI-Lauf mit dokumentierter Session-ID, Worktree und Brief verwenden.
Keine Claude-Agent-API, Kostenformel, feste Kontextgrenze oder Cache-TTL voraussetzen.
Die [AGENTS-Vorlage](../templates/AGENTS-warm-handoff.md) bleibt ein separat nutzbarer
Projekteinstieg. Der aktuelle Auftrag und Host-Rechte gehen Beispielen darin vor.

Direkte Arbeiter und optionale Wächter folgen [Wellen](wave-execution.md),
begrenzt durch tatsächlich verfügbare Host-Slots. Kurze selbstständige Briefe
verwenden und automatische Ergebnismeldungen statt Statuspolling bevorzugen.
Bestehende Autorisierungen über Fortsetzungen bewahren. Ein Statuswunsch setzt
die Arbeit nicht außer Kraft. Eine laufende Session eindeutig identifizieren;
nicht anhand eines mehrdeutigen letzten Laufs fortsetzen.

## Vereinbarte Übergabe in TextEdit

Bei Yasins Dokumentablauf erhält jeder abgeschlossene nutzerrelevante Schritt
oder jede Welle eine neue überprüfte RTF: Änderung, Belege, offene Punkte,
laufende Arbeit und eindeutige Antwort-/Testfelder. Ein Arbeiterabschluss wird
erst nach Artefaktprüfung eingeordnet; er bedeutet nicht Gesamtabschluss.
Die Kopierzeile steht oben und zeigt auf diese neue Antwortdatei.
Alle darin genannten Lesedokumente in der aktiven TextEdit-Tabgruppe oder einer
neuen gemeinsamen Gruppe öffnen: [geprüfte Methode](rtf-macos.md).
Keine zusätzliche Rückfrage für bereits beauftragtes Öffnen; spätere
Nutzerwünsche zu Fokus/Unterbrechung beachten. Öffnen ist erst nach UI-Beleg
erledigt. Ohne verfügbares Werkzeug Pfade und offene Viewer-Prüfung nennen.

Pasted Content und lange Diktate aus Codex/cmux wie andere Originaleingänge
behandeln; Referenzen verfolgen, Platzhalter nicht als Inhalt ausgeben.
Gespeicherte RTF-Revisionen, gespeicherte Nachträge und Chat gemeinsam nach
[Handoff-Format](handoff-format.md) abgleichen; ungespeicherte Entwürfe nicht importieren. Die alte
Antwortdatei bleibt unangetastet. Fehlende Originale ausdrücklich kennzeichnen.

## Messung und Installation

Tatsächliche Host-/Session-Telemetrie mit Quelle, Zeitpunkt und Umfang erfassen.
Account-Kontingent ist kein Verbrauch dieses Auftrags; kumulierte Zähler nicht
mehrfach addieren. API-Cacheangaben sind keine Codex-Abogarantien. Ohne Messung
„nicht gemessen“, ohne Abrechnungsbeleg keine Dollarwerte aus Tokens ableiten.
Historische Helfer im Repository sind nicht automatisch für den aktuellen Host
validiert; insbesondere keine Ping-/Messanfrage zum künstlichen Warmhalten.

Eine Skill-Installation muss den ganzen Ordner mit Referenzen und Skripten
bewahren und vom konkreten Host gefunden werden. Die vorhandene sichere
Installation niemals bei einer Repository-Änderung beiläufig ersetzen.
Keine globalen Settings, Skills, Plugins, Memory, Goals oder Scheduler ändern.

## Nutzerinstanz bei nativer QA erhalten

Vor einem App-Resolver dessen Start- und Aktivierungssemantik prüfen: `getApp`
kann eine fehlende App starten. Muss die Nutzerinstanz erhalten bleiben, nur eine
verifiziert laufende isolierte Instanz/PID binden oder technisch garantierte
isolierte Startsemantik verwenden. Eine längere Fixturelaufzeit genügt nicht.
Fehlt diese Möglichkeit, native QA offenlassen; keinen normalen App-Start als
Ersatz verwenden. Unveränderte installierte Dateien und unveränderte laufende
Prozesse getrennt belegen; unerwarteten Prozesswechsel und unklaren Datenumfang melden.

## Sichtbare Fortschrittszeit

Im vereinbarten Aitomat-Profil sichtbare Fortschrittsmeldungen mit unmittelbar
zuvor gemessener Ortszeit samt Zeitzone beginnen, etwa `18:05 CEST —`.
Keine alte Uhrzeit wiederverwenden; bei fehlendem Uhrzugriff „Zeit nicht gemessen“.
Der Zeitstempel beschreibt die Meldung, keinen exakten API- oder Abrechnungsvorgang.
Keine Zusatzmeldungen nur für Zeitstempel erzeugen; Host-Kommunikationsregeln gelten.

## Yasins ausdrücklich gewähltes Chef-/Wächterprofil

Für Yasins vereinbarte komplexe Arbeitswellen gilt seit seiner Steuerung vom
11.09.2026 (20:38/20:43) das Profil Chef → Wächter/Integrator → Arbeiter.
Der Chef bewahrt Auftrag und Freigaben und überwacht die Ergebnisse. Der Wächter
koordiniert die Arbeiter, integriert und prüft ihre Artefakte und liefert dem Chef
einen konsolidierten fertigen Bericht, eine echte Blockade oder den unten
vereinbarten Lagecheck. Routinemäßige
Zwischenstände und Rückfragen gehen zwischen Arbeitern und Wächter direkt hin
und her, ohne den Chef für jede Einzelentscheidung aufzuwecken.

Automatisch zugestellte Abschluss-/Blockademeldungen verwenden; kein minütliches
Statuspolling. Ergänzung vom 11.09.2026, 21:08–21:10: Der Nutzer wünscht spätestens
25 Minuten nach der letzten gebündelten Rückmeldung einen tatsächlichen Lagecheck.
Dazu beim Wächter Fortschritt, Unterbrechungen und nötige nächste Schritte prüfen
und eine knappe gemeinsame Rückmeldung geben; dazwischen nur wichtige Ergebnisse
oder Blockaden gebündelt melden. Unterbrochene Arbeiter nur innerhalb ihres noch
gültigen Auftrags fortsetzen lassen.

Diese 25 Minuten sind eine Nutzerpräferenz innerhalb der tatsächlichen Host-
Kommunikations-, Timer- und Wartegrenzen. Ohne verfügbaren Timer oder laufende
Ausführung keine pünktliche Hintergrundmeldung versprechen. Strengere
Kommunikationspflichten des Hosts einhalten. Der gewünschte Lagecheck ist reale
Koordination; keine zusätzlichen inhaltsleeren Pings zum „Cachewarmhalten“.
Weder eine Cache-Haltedauer noch Token-/Abonnement-Einsparungen garantieren.

Modellpräferenz, präzisiert am 11.09.2026 um 21:27: grundsätzlich höchstens
Astra mit Low Effort; einfache klar begrenzte Arbeit mit Sol oder Terra bearbeiten.
Höheren Effort erst einsetzen, wenn eine Sache trotz Bearbeitung mit dieser
Vorgabe nicht funktioniert. Spark ist gewünscht, wenn tatsächlich angeboten. Vor Delegation verfügbare Modelle und erlaubte
Overrides prüfen. Spark war in der Werkzeugliste dieser Welle nicht verfügbar;
nicht durch einen unsichtbaren Wechsel oder einen anderen Modellnamen ersetzen.
Die Präferenz ist keine Behauptung über das bereits laufende Modell. Abweichende
konkrete Qualitätsaufträge und Hostbeschränkungen weiterhin beachten.

Bei vier Gesamtslots ist hier Chef + ein ausführender Wächter/Integrator + zwei
Arbeiter die passende Belegung. Zusätzliche Themen staffeln; keine wartenden
Wächter ohne Arbeiterslots und keine Umgehung durch zusätzliche CLI-Läufe.
Für andere Nutzer/Aufträge bleibt die allgemeine direkte Delegation aus
[Wellen](wave-execution.md) verfügbar.
