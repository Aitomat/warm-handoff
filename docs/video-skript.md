# warm-handoff — Video-Skript (Gerüst)

Stand: 30.08.2026, 00:53. Zielzeit ~6–8 Minuten, deutsch, Bildschirmaufnahme
mit Terminal und TextEdit. Je Szene: Bild → Text.

## Szene 1 — Das Problem (Kaltstart)

Bild: eine frische Sitzung, die minutenlang Dateien einliest.
Jede Anfrage liest den ganzen bisherigen Verlauf neu. Wer das nicht sieht,
zahlt es trotzdem — nur eben ohne es zu merken.

## Szene 2 — Das Problem (Fettkontext)

Bild: Statuszeile mit 400k Kontext, ein winziger Edit läuft.
Bei 400k kostet jeder einzelne Tool-Schritt so viel wie früher eine ganze
Welle. Der Nutzer hat nichts falsch gemacht — die Sitzung ist einfach alt.

## Szene 3 — Die Cache-Fakten

Bild: die drei Zahlen groß im Bild.
Lesen aus dem Cache ×0,1 · Schreiben in den Cache ×2 · eigene Ausgabe ×5.
Auf Pro/Max hält das Fenster eine Stunde, gleitend: jede Anfrage setzt es zurück.

## Szene 4 — Die Cache-Killer

Bild: `/model`-Wechsel mitten in der Sitzung, danach ein 200k-Cache-Write.
Modell wechseln, Effort wechseln, CLAUDE.md bearbeiten, MCP neu starten:
alles vier zerstört den Cache sofort, egal wie warm die Uhr noch ist.
Deshalb: Modell und Effort ganz am Anfang festlegen.

## Szene 5 — Sichtbar machen

Bild: eine Antwort mit Zeitstempel und Kostenzeile darunter.
Jede Antwort trägt eine gemessene Uhrzeit und eine gemessene Kostenzeile.
Nicht geschätzt, nicht extrapoliert — kein `date`-Aufruf, kein Zeitstempel.
Erst wenn man es sieht, kann man es steuern.

## Szene 6 — Der Sweetspot

Bild: die Übergabe-Tabelle, Cursor auf „~200k".
Vor einer großen Bau-Welle wird bei 200k übergeben, bei reinem Gespräch
erst bei 300k. 400k ist die harte Grenze. Der Break-even wird gerechnet,
nicht gefühlt.

## Szene 7 — Die Handoff-Datei

Bild: das Handoff in TextEdit, Scroll durch Stand → Testliste → Sammelfeld.
Das ist das Herzstück: ein Dokument, in das der Nutzer stundenlang alles
hineinsammelt — Testantworten, Ideen, Kritik. Sammeln kostet null Anfragen.

## Szene 8 — Fragen gehören in die Datei

Bild: `>>>Userantwort:` im Handoff, daneben ein leerer Chat.
Eine Rückfrage im Chat blockiert eine ganze Welle. Zehn Fragen in der Datei
blockieren nichts. Ausnahme: alles Unumkehrbare, Sicherheitsrelevante oder
nach außen Sichtbare — da wird sofort gefragt.

## Szene 9 — Der Wächter

Bild: ein Wächter-Agent startet fünf Arbeiter in einer Nachricht.
Statt acht Fertigmeldungen in der Hauptsitzung — acht volle Anfragen bei
vollem Kontext — weckt ein Wächter die Sitzung genau einmal.
Das allein sparte gemessen rund 140k.

## Szene 10 — Ein Wächter je Thema

Bild: drei Wächter nebeneinander, je 4–6 Arbeiter, darunter der Merge-Wächter.
Ein Wächter mit zwölf Arbeitern ist ein Engpass — und, wie am 29.08.,
ein Absturzrisiko: zwölf Kaltbuilds legten den Rechner 90 Minuten lahm.
Heute: ein Wächter je Themenbereich, Aufträge 15–25 Minuten, ein Build-Schloss.

## Szene 11 — Die Bilanz

Bild: die Wellen-Tabelle 22/23/24 mit Anfragen, Äquivalent, Wanduhr.
Welle 23 war die billigste und zugleich die langsamste. Welle 24 ohne den
Absturz: 40 Minuten und 700k. Token und Wartezeit sind zwei Achsen —
wer nur eine misst, optimiert die falsche.

## Szene 12 — Der Kreis schließt sich

Bild: Handoff wird geschrieben, Sitzung beendet, neue Sitzung startet daraus.
Handoff → frische Sitzung → Handoff. Die neue Sitzung beginnt günstig und
vollständig informiert — und der Nutzer hat inzwischen längst weitergesammelt.
