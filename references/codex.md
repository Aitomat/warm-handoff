# Codex: Dokumente, Fortsetzungen und Wellen

Die verfügbaren Werkzeuge und geltenden Host-Grenzen bestimmen die Ausführung.
Native Unteragenten nur bei autorisiertem Auftrag; alternativ einen ausdrücklich
beauftragten CLI-Lauf mit dokumentierter Session-ID, Worktree und Brief verwenden.
Keine Claude-Agent-API, Kostenformel, feste Kontextgrenze oder Cache-TTL voraussetzen.
Die [AGENTS-Vorlage](../templates/AGENTS-warm-handoff.md) bleibt ein separat nutzbarer
Projekteinstieg. Der aktuelle Auftrag und Host-Rechte gehen Beispielen darin vor.

Oberchef → Wächter → Arbeiter folgt [Wellen](wave-execution.md), einschließlich
maximal vier Wächtern und dem oft niedrigeren verfügbaren Gesamtslot-Limit.
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
Gespeicherte RTF, Live-Nachträge und Chat gemeinsam abgleichen. Die alte
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
