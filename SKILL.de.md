---
name: warm-handoff
description: Zu Beginn jeder Arbeitssitzung und vor jeder längeren Pause nutzen — verfolgt das Claude-Code-Prompt-Cache-Fenster (1 Stunde gleitendes TTL auf Pro/Max), versieht jede Antwort mit einem Zeitstempel, damit der Nutzer das Fenster selbst sieht, warnt vor cache-zerstörenden Aktionen, empfiehlt ab einer Kontext-Schwelle eine frische Sitzung und schreibt ein Handoff-Dokument (mit der Testliste des Nutzers darin), damit die nächste Sitzung günstig und vollständig informiert startet. Auslöser: „cache", „handoff", „Pause", „frische Sitzung", „Welle fertig" oder beim Wiedereinstieg nach einer Lücke.
---

# warm-handoff — die Cache-Welle reiten, übergeben bevor sie bricht 🏄

**Ein Satz:** Handoff → frische Session → Handoff. Der Nutzer sammelt alles
(Testantworten, Ideen, Kritik) in EINEM Handoff-Dokument über Stunden, startet
eine frische Session, der Agent arbeitet alles durch mehrere Subagenten ab und
schreibt das nächste Handoff.
Vollständige Historie mit datierten Nutzer-Zitaten und der Begründung jeder Regel:
`references/historie.md` (lesen, wenn eine Regel hier seltsam wirkt — nicht standardmäßig laden).

**Qualität vor Kürze.** Dieser Skill darf lang sein. Er wird einmal je Sitzung geladen und
spart dafür bis zu 90 % der Anfragen einer Welle — jede Regel hier ist billiger als der
Fehler, den sie verhindert. Nichts kürzen, was eine Regel trägt: kein Zusammenstreichen von
Belegen, Zahlen oder Begründungen, weil der Text „zu lang" wirkt. Was raus darf, ist
Wiederholung; was bleibt, ist alles, wonach jemand später handelt.

## Die sparsamste Arbeitsweise in fünf Sätzen

Für den Nutzer, in einfachen Worten (gefragt am 30.08.2026, 15:06: *„was ist denn jetzt die
Moral der Geschichte?"*):

1. **Eine Session pro Welle** — Plan, Wächter, Merge, Handoff in einer; eine frische Session
   kostet ihren ~200k-Startaufbau, also erst jenseits von ~200k Kontext eine neue anfangen.
2. **Sammeln kostet nichts** — Testantworten, Einfälle und Kritik stundenlang in die
   Handoff-Datei schreiben; das sind null Anfragen, während jede Chat-Nachricht ein volles
   Kontext-Nachlesen kostet.
3. **Wächter statt Pings** — ein Wächter je Thema startet die Arbeiter, dadurch wird die
   Hauptsitzung 5–7 statt 15–20 Mal geweckt.
4. **Unter 200k Kontext bleiben** — die Hauptsitzung plant, mergt und liest Berichte;
   alles andere lebt in Agenten.
5. **Handoff mit Kostentabelle** schließt die Welle ab — gemessene Zahlen, keine Gefühle.

**Vorsatz (30.08.2026):** JEDE Sitzung messen — eine Logbuchzeile je Sitzung (Anfragen,
Äquivalent, Fertigmeldungen, Wanduhr, Aufträge) — damit dieser Skill an Belegen wächst und
nicht an Erinnerung.

## Projektstart — der Startkontext ist die erste Ersparnis

Jede Anfrage liest den ganzen Präfix neu, und der Präfix beginnt mit dem Startkontext:
System-Prompt, Werkzeug-Schemata, CLAUDE.md und Name + Beschreibung JEDES global
installierten Skills, Plugin-Skills und Agenten — ob dieses Projekt sie braucht oder nicht.
In Aitomat gemessen am 02.09.2026 (erste Anfrage zweier frischer Sitzungen): **63k Token
Startkontext, davon 46 % Skill- und Agentenbeschreibungen** (169 Skills + 67 Agenten ≈ 29k),
die meisten davon `ads-*`, `seo-*`, `firecrawl-*` — für eine Swift-Diktier-App irrelevant.
Ein eigener Projektordner hilft nicht; nur projektlokale Einstellungen helfen.

**Beim ERSTEN Handoff eines neuen Projekts** (und einmal nachträglich in jedem laufenden):

1. Entscheiden, welche Skills, Plugins und MCP-Server dieses Projekt wirklich braucht. Die
   vollständige Liste mit je einer Zweckzeile steht in `~/.claude/SKILLS-UEBERSICHT.md` (nach
   jeder Installation oder Deinstallation neu erzeugen mit `scripts/skills-uebersicht.sh`).
2. `<projekt>/.claude/settings.json` schreiben: `"enabledPlugins": {"<id>@<marktplatz>": false}`
   für nicht gebrauchte Plugins, `"skillOverrides": {"<name>": "off"}` für jeden nicht
   gebrauchten globalen Skill — ein Eintrag je Skill, es gibt KEINE Platzhalter (`~/.claude/skills`
   und das verlinkte `~/.agents/skills` eingeschlossen; Plugin-Skills nur über `enabledPlugins`).
   Globale Agenten in `~/.claude/agents/` haben keinen Projektschalter.
   Vorlage: `/Users/pro16/Code/aitomat/.claude/settings.json`.
3. Das Ergebnis im Handoff im PFLICHT-Block **`## Aktive Werkzeuge dieses Projekts`**
   dokumentieren (siehe Handoff-Struktur unten): aktive Skills, Plugins, MCP-Server, dazu die
   Zeile `Übersicht: ~/.claude/SKILLS-UEBERSICHT.md`. Wird ein Werkzeug ergänzt oder
   abgeschaltet, werden beide Stellen nachgezogen — Einstellungsdatei und dieser Block.
4. Messen, nicht glauben: die erste Anfrage der nächsten frischen Sitzung zeigt den neuen
   Startkontext (`cache_creation_input_tokens` in der Session-JSONL, oder `~/.claude/ctx.sh`).

**Warum das für API-Kunden noch mehr zählt.** Yasin, 02.09.2026, 19:10: über die API lebt der
Prompt-Cache **5 Minuten**, nicht eine Stunde — jede längere Pause ist ein vollständiger
Neuaufbau des ganzen Startkontexts zum doppelten Preis. Ein fetter Startkontext wird also
immer wieder bezahlt, ein schlanker plus alles, was in der Handoff-Datei gesammelt wurde
(null Anfragen beim Sammeln), macht jeden Neuaufbau billig. Startkontext-Diät zuerst,
Sammeln zweitens, frische Sitzung drittens — in dieser Reihenfolge bleibt die Welle auf
jedem Tarif bezahlbar.

## Die Fakten (Claude-Code-Doku, 2026-08)

- Pro/Max: **1 Stunde gleitendes Cache-TTL** — jede Anfrage setzt es zurück. Subagenten: strikt 5 Min.
- Cache-Killer unabhängig von der Uhr: `/model`- oder `/effort`-Wechsel mitten in der Sitzung,
  CLAUDE.md/Systemprompt bearbeiten, MCP-Server-Neustart. Modell + Effort beim Sitzungsstart festlegen.
- Preise relativ zu frischem Input: **Cache-Lesen ×0,1 · Cache-Schreiben ×2 (1-h-TTL) · eigene Ausgabe ×5.**
- Jede Anfrage liest den gesamten Prefix neu. Kosten = Anfragen × Kontext. Die Nachrichten
  des Nutzers sind ein Rundungsfehler; die eigenen Tool-Schritte und Berichte des Agenten sind die Rechnung.

## Jede Antwort — drei Ehrlichkeitsregeln

1. **Zeitstempel ganz am ANFANG jeder Antwort**, aus einem `date`-Aufruf IN DIESER Antwort
   (`date "+%d.%m.%Y %H:%M"`, huckepack auf einen ohnehin laufenden Befehl). Kein `date` in
   dieser Runde → kein Zeitstempel. **Auch bei Zwischenmeldungen** — „Wächter A baut, ich warte
   auf beide Meldungen" ist eine volle Anfrage, und nur der Zeitstempel vorne zeigt dem Nutzer,
   dass gerade eine Anfrage lief und den Cache warm gehalten hat (Nutzer, 30.08.2026, 15:44).
   Eine Antwort, deren erste Zeile kein Zeitstempel ist, sieht kostenlos aus — sie ist es nie.
   Nie extrapolieren, nie `~19:40`.
2. **Nie die Kontextgröße raten.** Quellen: die Statuszeile des Nutzers oder `~/.claude/ctx.sh`,
   angehängt an einen ohnehin laufenden Befehl (`date … && ~/.claude/ctx.sh`). Es liest die
   Session-JSONL (`cache_read + cache_creation` der letzten Anfrage). Keine → "nicht gemessen".
3. **Kostenzeile unter jeder inhaltlichen Antwort**, aus der LETZTEN ABGESCHLOSSENEN Anfrage, so beschriftet:
   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Bei Einzeilern weglassen. Wenn eine Runde > 2× den
   Sitzungsdurchschnitt kostet, EINMAL pro Welle freundlich sagen warum, mit dem günstigeren Weg —
   die Ursache liegt fast immer beim Agenten (ganze Dateien gelesen, Rohausgabe, lange Antworten), nicht beim Nutzer.

## Sweetspot — wann übergeben

| Was als Nächstes kommt | Übergabe bei |
|---|---|
| Große Bau-/Review-Welle (Hunderte Tool-Schritte) | ~200k |
| Gemischt | ~250k |
| Nur Gespräch / kleine Edits | ~300k |
| Alles | 400k harte Obergrenze |

Break-even für eine frische Session: `(Start-Kontext × 2) / ((alter_Kontext − Start-Kontext) × 0,1)` Schritte.
Der Startkontext wird pro Projekt GEMESSEN (82–125k gesehen), nie als "~20k" angenommen. Schritte = Tool-
Aufrufe, nicht Nutzer-Nachrichten. Reden auf fettem Kontext ist billig; Arbeiten darauf nicht.

**Was ein Subagent wirklich kostet.** Ein frischer Subagent ist NICHT gratis: sein erster
Schritt zahlt den eigenen Startkontext ×2 (Cache-Aufbau), erst jeder weitere Schritt kostet
×0,1. Eine Welle kostet also

```
Hauptkontext × 0,1 × eigene_Schritte  +  N Agenten × Startkontext × 2
                                      +  N × Startkontext × 0,1 × Agentenschritte
                                         └── die Zeile, die meist vergessen wird ──┘
```

Beispielrechnung, 220k Hauptkontext und 30k Agentkontext: ein Schritt in der Hauptsitzung
kostet 220k × 0,1 = 22k; derselbe Schritt im Agenten kostet 30k × 0,1 = 3k, aber der Agent
verbrennt einmalig 30k × 2 = 60k. Break-even: 60k ÷ (22k − 3k) ≈ **7 Schritte je Agent**.
Darunter ist Selbermachen billiger, darüber gewinnt Delegieren — und der Vorsprung wächst.
Beide Kontexte werden gemessen, nicht angenommen: bei 120k Hauptkontext liegt der Break-even
bei 60k ÷ (12k − 3k) ≈ ebenfalls 7 Schritten, bei 400k nur noch bei ≈ 2. Die Zahl nennen,
nicht "Agenten sind billig" behaupten.
Bei jedem Wellenende beiläufig sagen: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
Während die eigene Tool-Schleife des Agenten läuft, ist eine Nutzer-Nachricht fast gratis (hängt
sich an die nächste Anfrage an); während Subagenten laufen oder der Agent leerläuft, kostet sie den vollen Kontext × 0,1.

## Der eigentliche Hebel: weniger Anfragen

Gemessen: 147 Anfragen, 13 vom Nutzer; eigene Ausgabe = 23 % der Kosten. Ziele, in Reihenfolge:
**weniger Anfragen · kürzere eigene Ausgabe · kleinerer Kontext.** Techniken: alle unabhängigen
Lesevorgänge in einer Antwort bündeln · ein Skript, das zehn Dinge tut und eine Zusammenfassung
druckt · Ausgabe vorfiltern (`grep`/`tail`) · grep statt ganze Dateien lesen · keine Status-
Nachrichten pro Agent (eine Zusammenfassung, wenn die Flotte landet) · Berichte als Dateien, nicht
im Chat · Budget für eigene Ausgabe: Zwischenstand ≤ 100 Wörter, final ≤ 500, Details in Dateien.
Terminal-Tab-Vorschläge und jede Agenten-Fertigmeldung sind ebenfalls volle Anfragen.

## Wer plant was — Hauptsitzung und Wächter haben verschiedene Aufgaben

Die häufigste teure Verwechslung: ein Wächter soll sich „überlegen, was zu tun ist". Das ist
nicht seine Aufgabe. Die Arbeitsteilung ist scharf:

**Die HAUPTSITZUNG schreibt den Wellenplan** — als Datei, BEVOR ein Wächter existiert
(`docs/reviews/JJJJ-MM-TT-welleNN-plan.md`). Darin steht **jeder einzelne Auftrag** mit
seinen drei Angaben: **Was** (der ausformulierte Auftragstext samt Belegen, Screenshot-Pfaden
und Nutzerzitat mit Uhrzeit), **Abnahme** (woran man sieht, dass es fertig ist — Test,
Screenshot, grep) und **Modell** (Effort). Dazu die Strukturregeln, die für jeden Auftrag
gelten, und die Aufteilung in Tabellen — je Tabelle ein Wächter, mit hartem Dateibesitz. Nur
die Hauptsitzung hat den ganzen Kontext: das beantwortete Handoff, die Zwischenrufe-Datei,
die Screenshots, den Themenspeicher. Nur sie kann deshalb entscheiden, was diese Welle
überhaupt soll.

**Der WÄCHTER erfindet keine Aufträge.** Er bekommt eine Tabelle und tut genau fünf Dinge:
er zerlegt sie in Arbeiter, **reicht den Auftragstext weiter** (wörtlich, nicht
nacherzählt — der Plan ist die Quelle), baut seriell mit Build-Schloss, mergt per
`git merge --squash`, lässt Codex prüfen und schreibt den Bericht. Findet er unterwegs etwas
Neues, gehört das in den Bericht — nicht in einen selbst erfundenen Auftrag.

**Warum das die Modellwahl der Hauptsitzung wichtig macht.** Wenn die Hauptsitzung die
Auftragstexte schreibt, hängt die Qualität ALLER Unteragenten-Prompts an ihrem Modell. Ein
Wächter kann einen schlechten Auftrag nicht reparieren, er kann ihn nur ausführen. Ein
unscharfes „mach das Fenster schöner" kostet drei Anläufe; ein Auftrag mit Belegzitat,
Screenshot-Pfad und Abnahmekriterium kostet einen. Die Ersparnis eines billigeren
Hauptsitzungs-Modells kann also an anderer Stelle mehrfach wieder verloren gehen.

**Offener Messpunkt (Yasin, 03.09.2026, 18:38):** bisher lief die Hauptsitzung auf Opus. Die
nächste Sitzung wird **Fable/medium als Hauptsitzung** testen und über die Logbuchzeile
verglichen — Anfragen, Token, Wanduhr und vor allem: wie viele Aufträge im zweiten Anlauf
landeten. Bis diese Zeile existiert, ist die Frage offen; sie wird gemessen, nicht geraten.

## Subagenten — die Standardarbeitsweise

- **Der Wellenplan ist eine DATEI, geschrieben BEVOR die Wächter starten** (Nutzer,
  30.08.2026, 02:28: er will den Plan sehen und sich anschauen können). Vor jedem Start
  schreibt die Hauptsitzung `docs/reviews/<datum>-welleN-plan.md`: oben die Struktur-Regeln,
  die für alle Aufträge gelten (Branch-Basis, Build-Schloss, keine Rückfragen,
  Berichtsvertrag, Push vor „fertig"), darunter JE THEMA EINE TABELLE mit den Spalten
  **ID · Auftrag · Abnahmekriterium · Modell/Effort**. Sie committet die Datei, öffnet sie
  sofort (`open -a TextEdit <datei>`) und startet erst dann ALLE Wächter in EINER Nachricht,
  jeder Auftrag mit Verweis auf die Datei („dein Thema ist Tabelle B in <pfad>") statt mit
  wiederholtem Plantext. Eine Datei = eine Stelle, die der Nutzer liest, und dieselbe, die
  die Wächter lesen — kein Auseinanderdriften.
- **Der Push gehört zum Auftrag.** Jeder Wächter und jeder Skill-Agent pusht seinen Branch
  (`git push -u origin <branch>`), BEVOR er „fertig" meldet — nicht danach, nicht „macht die
  Hauptsitzung". Am 30.08.2026 um 02:36 sah der Nutzer auf GitHub keine Bewegung, weil ein
  Skill-Agent zwar committet, aber nicht gepusht hatte. Ein nur lokal existierender Branch
  ist nicht geliefert; der Bericht nennt den gepushten Hash.
- **Wächter-Agent (Guardian).** Für eine Bau-Welle bekommt EIN orchestrierender Agent (Opus,
  low/normal Effort) den ganzen Plan als Datei, startet die Arbeits-Agenten selbst, merged,
  testet, bündelt, räumt `.build` von gemergten Worktrees auf, schreibt den Bericht — die
  Hauptsitzung wird EINMAL geweckt statt einmal pro Agent (8 → 1 Meldungen ≈ 140k gespart bei 190k Kontext).
  Fragen der Arbeiter landen beim Wächter, also müssen die Aufträge vollständig sein: Pfade, Ziel,
  Grenzen, Abnahmekriterien, "keine Rückfragen — entscheiden, die Annahme dokumentieren".
- **Ein Wächter JE THEMENBEREICH, nicht einer je Welle** (30.08.2026). Ein Wächter mit 12
  Arbeitern ist Engpass und Absturzrisiko; jeder Themenbereich (Oberfläche, Audio, Tests,
  Doku …) bekommt einen eigenen Opus-Wächter mit **höchstens 4–6 Arbeitern**. Jeder Themen-
  Wächter merged in seinen eigenen Integrationsbranch. Die Hauptsitzung führt die
  Integrationsbranches zusammen und startet danach EINEN **Merge-Wächter** für den einen
  Build, die Vollsuite, das Bundle und die QA-Runde. Geweckt wird die Hauptsitzung einmal je
  Themen-Wächter, nicht einmal je Arbeiter.
- **WIE VIELE Wächter? Die Themen zählen, nicht die Arbeiter** (Nutzerfrage, 30.08.2026,
  02:24: „drei Wächter, vier Wächter, zwei Wächter — was ist am sinnvollsten?"). Die Antwort
  ist mechanisch: **ein Wächter je abgegrenztem Thema, das 4–6 eigene Aufträge trägt.** Unter
  4 Aufträgen lohnt ein Wächter nicht — er zahlt `Startkontext × 2` allein fürs Dasein (60k
  bei 30k Startkontext); solch ein Thema kommt zum Nachbar-Wächter oder in die Hauptsitzung.
  Über 6 wird der Wächter selbst zum Engpass: er merged, baut und testet seriell, die letzten
  Arbeiter warten. **Zwei** Wächter stimmen nur bei zwei wirklich getrennten Bereichen;
  **vier und mehr** sind richtig, wenn es vier unabhängige Bereiche gibt, und Verschwendung,
  wenn der vierte nur eine Scheibe des dritten ist. Drei ist meist richtig, weil eine Welle
  meist drei abgegrenzte Bereiche à 4–6 Aufträge hat — die Zahl aber aus dem Plan ableiten,
  nie aus Gewohnheit wählen.
- **Build-Schloss — nie mehr als ein Build pro Rechner.** Vor jedem Build:
  `mkdir /tmp/<projekt>-build.lock` (schlägt fehl, wenn es existiert → warten oder
  überspringen; danach `rmdir`). `mkdir` ist atomar, funktioniert also über Agenten und
  Worktrees hinweg. Das ist die mechanische Absicherung hinter "Arbeiter bauen nicht" nach
  dem Absturz vom 29.08.
- **Der Wächter startet alle Arbeiter gleichzeitig, in EINER Nachricht** (ein Batch von Agent-
  Aufrufen), nie nacheinander — ein serieller Schwanz von Arbeitern macht aus einer günstigen
  Welle eine lange. Der ERSTE Schritt jedes Arbeiters ist, den aktuellen Branch-Tip zu ziehen
  (`git pull` / `git fetch && git rebase`), bevor er irgendeine Datei anfasst, damit er nie auf
  einer veralteten Basis baut.
- **Arbeiter bauen und testen NICHT.** Sie schreiben Code + Tests, höchstens `swiftc -parse`,
  und committen früh. Nur der Wächter baut — EINMAL, seriell, im Hauptrepo — und fährt die
  Suite. 12 Arbeiter × je ein Kaltbuild = 400+ Compiler-Prozesse, Load 70, 18 GB RAM in den
  Swap, Neustart erzwungen, 90 Minuten verloren (29.08.2026). Muss doch gebaut werden: nie
  mehr als 4 gleichzeitig; `memory_pressure` vor der Vollsuite.
- **Aufträge auf eine Aufgabe und 15–25 Minuten begrenzen** (30.08.2026 — vorher ~30 Minuten,
  davor 40 Minuten / 2–3 Aufgaben; ein einziger fokussierter Auftrag landet schneller und
  lässt sich leichter zusammenführen, und erst der kurze Auftrag sorgt dafür, dass die 4–6
  Arbeiter eines Themen-Wächters gemeinsam landen). Längere Arbeit liefert in
  eine DATEI (`docs/reviews/<datum>-<thema>.md`) und berichtet nur den Pfad; das Handoff listet
  die erwarteten Dateien, und die nächste Sitzung prüft zuerst mit `ls`. Nie auf einen Nachzügler warten.
- **Jeden Arbeiter-Branch sofort bei Landung mergen**, Merges nicht für später sammeln — Konflikte
  sind einzeln billiger zu lösen, direkt solange die Arbeit frisch ist. Die VOLLE Testsuite nur
  EINMAL laufen lassen, ganz am Ende, gegen das gemergte Ergebnis; ein wackelnder/fehlschlagender
  Einzeltest wird für sich untersucht statt die ganze Suite erneut zu fahren.
- **Der Wächter schreibt nach 60 Minuten eine Zwischenstand-Datei**, falls die Welle noch läuft
  (Pfad im kommenden Handoff, z. B. `docs/wellen/<datum>-zwischenstand.md`) — damit eine Sitzung,
  die mitten in der Welle nachschaut, oder ein Handoff, das vor Fertigstellung des Wächters
  geschrieben wird, etwas Reales zum Zeigen hat. **Das Handoff startet auch ohne fertigen Wächter**:
  den Wächter und seine noch laufenden Arbeiter unter "erwartete Agenten-Ergebnisse" listen,
  die nächste Sitzung prüft sie nach.
- **Modell + Effort im sichtbaren Label — für Wächter UND für deren Arbeiter**
  (Nutzer, 30.08.2026, 02:31). Das Muster ist `Modell/Effort · ID Kurzname`, z. B.
  `Fable/low · A1 Aufnahme-Rot`, `Opus5/high · Verlauf-Tempo`. Auch ein Wächter beschriftet
  die Arbeiter, die er startet, so — der Nutzer liest die Agentenliste unten am Bildschirm
  und will dort Modell und Effort sehen, ohne zu fragen. Eine Ausnahme offen aussprechen:
  **Codex läuft als Shell-Befehl, nicht als Agent — es erscheint in dieser Liste nie**;
  das sagen, statt den Nutzer suchen zu lassen.
  Fable 5 als Subagent: **immer Effort low** — und **nur für Aufträge, die der Nutzer als
  „wichtig" markiert hat**; dort lohnt das schnellere Modell. Alles andere: Opus (low).
  **Sonnet nur für Triviales ohne Bau** (Umbenennen, Text verschieben, Dateien auflisten),
  nie für einen Bauauftrag. Für schwieriges Review/Design Opus oder eine zweite Architektur
  (Codex/GPT) nutzen. Nie die eigene Ausgabe selbst reviewen — an Codex weiterleiten.
- **Agenten testen vor dem Nutzer.** Volle Suite + ein QA-Agent, der die App startet und jeden
  Testpunkt einmal anklickt; der Nutzer sollte meist nur "funktioniert, danke" sagen. **Der QA-
  Agent schließt die Fenster/Prozesse, die er zum Testen geöffnet hat**, bevor er fertig meldet —
  der Nutzer soll keinen Haufen liegengebliebener Testinstanzen erben.
- Berichtsvertrag: ≤ 300 Wörter, Status/Entscheidungen/Belege-mit-Pfaden/Risiken/Nächstes; keine
  Chronik, keine eingefügten Logs. Subagenten-Token zählen trotzdem aufs Wochenkontingent — was sie
  sparen, ist der HAUPTkontext (jeder Schritt ≈ 1/5 der Kosten, und nichts davon bleibt in der Sitzung).
- Taktung — **innerhalb einer Welle gewinnt die Parallel-Regel** (damit ist der alte
  Widerspruch aufgelöst): Ein Wächter startet seine Arbeiter IMMER parallel, in einer
  Nachricht, egal ob der Nutzer da ist oder nicht. Die Regel „Nutzer abwesend → seriell" gilt
  nur für Arbeit AUSSERHALB eines Wächters, die die Hauptsitzung selbst erledigt (kleine
  Edits, Reviews, Prüfungen): die zeitlich strecken, damit jede Fertigmeldung den Cache warm
  hält, statt alles in einem Schwung zu verbrennen und dann leerzulaufen. Nie
  Beschäftigungstherapie erfinden.

## Belege — gemessene Wellen (Aitomat, 29./30.08.2026)

| Welle | Struktur | Anfragen | Äquivalent | Fertigmeldungen | Wanduhr |
|---|---|---|---|---|---|
| 22 | 6 Arbeiter + Merge-Agent, Hauptsitzung orchestriert | 58 | 2.075k | 8 | ~2 Std. |
| 23 | 1 Wächter, wenige große Agenten | 43 | 1.531k | 1 | 2 Std. 20 |
| 24 | 1 Wächter, 12 Arbeiter, alle bauend | 62 | 3.143k | 1 + 12 | 2 Std. 10 |
| 25 | 3 Themen-Wächter + Merge-Wächter, 15 Arbeiter | 29 | 1.192k | 5 | 64 min |
| 26 | 3 Themen-Wächter + Merge-Wächter + Skill-Agent, 17 Aufträge | 34 | 1.159k | 5 | 53 min |
| 27 | 4 Themen-Wächter + Merge + Skill-Agent, Codex-QM je Wächter, 19 Aufträge | 41 | 1.160k | 7 | 78 min |
| 28 | 2 Themen-Wächter **nach DATEIEN geschnitten** + Merge + Skill-Agent, 11 Aufträge + Skill | 33 | 1.080k | 5 | 57 min |

Vollständiger Rechenweg, Normierung je Auftrag und alle Prozentzahlen:
**[`docs/evidenz.md`](docs/evidenz.md)**. Kurzfassung: gegen Welle 22 — dieselbe App,
derselbe Nutzer, nur ohne Wächter-Struktur — sind **43–50 % der Anfragen und 43–48 % des
Hauptkontext-Äquivalents** gespart; je Auftrag gerechnet (W22 erledigte 7 Aufträge, W25–W28
je 15–19) sind es **73–79 %**. Daher „spart bis zu 70 %" — konservativ gelesen.

So liest man das: Welle 23 war die günstigste in Token unter den DAMALS bekannten Strukturen
(ein Wächter = ein Wecken; die Wellen 25–28 haben sie später unterboten), aber die
langsamste auf der Uhr — Token und Wartezeit sind zwei verschiedene Achsen. Welle 24 sieht in
jeder Spalte am schlechtesten aus, aber 90 ihrer 130 Minuten und rund 2.400k des Äquivalents
sind der Rechner-Absturz (12 parallele Kaltbuilds); **ohne den Absturz waren es ≈ 40 Minuten
und ≈ 700k** — die schnellste Welle bisher. Genau das schützen das Build-Schloss und die
Regel „4–6 Arbeiter je Wächter".
**Welle 25 (00:46–01:50, 30.08.2026, ohne Absturz) löst diesen Zielkonflikt auf: die
Themen-Wächter-Struktur war die günstigste UND die schnellste bisher** — 29 Anfragen für 15
Bauaufträge, das niedrigste Äquivalent aller abgeschlossenen Wellen und 64 Minuten gegen
2 Std.+ bei jeder früheren Struktur. **Welle 26 (02:24–03:17) ist die Kontrollmessung** und
bestätigt das: dieselbe Struktur plus ein Skill-Agent trug 17 Aufträge in 34 Anfragen,
1.159k Äquivalent, 5 Fertigmeldungen und 53 Minuten. Zweimal hintereinander ~1,2 Mio. und
unter einer Stunde ist eine Struktur, die sich wiederholt, kein Glückstreffer.
**Welle 27 (03:39–04:57) zeigt die Decke:** ein VIERTER Themen-Wächter kostete dieselben
Token wie drei (41 Anfragen, 1.160k), brauchte aber 25 Minuten mehr — Wächter B allein lief
45 min, und der Merge-Wächter musste erstmals Konflikte auflösen, weil zwei Themen dieselben
Dateien anfassten.
**Themen nach DATEIEN schneiden, nicht nach Worten.** Was dieselben Dateien ändert, gehört zu
EINEM Wächter, so verschieden die Aufträge auch heißen mögen.
**Welle 28 (15:12–16:09, 30.08.2026) ist der Beleg dafür:** zwei streng nach Dateien
geschnittene Wächter trugen 11 Aufträge plus die Skill-Welle in 33 Anfragen, 1.080k,
5 Fertigmeldungen und 57 Minuten — das niedrigste gemessene Äquivalent und **null
Merge-Konflikte**. Weniger, dateidisjunkte Wächter schlagen mehr, themendisjunkte.

## Was wir gemessen haben (Lessons)

Nur, was das Logbuch wirklich zeigt — nichts hochgerechnet:

- **Themen-Wächter halbieren Anfragen und Wanduhr** gegenüber einem Wächter mit 12 Arbeitern:
  62 Anfragen / 2 Std. 10 (W24) → 29 / 64 min (W25) → 34 / 53 min (W26).
- **Der Start-Cacheaufbau (≈ 200k, einmalig) ist der größte Einzelposten einer kurzen
  Sitzung.** Deshalb lohnt Weiterarbeiten in DERSELBEN Sitzung, solange der Kontext < 200k ist.
- **Der Kontext blieb über eine ganze Welle bei ~114k**, weil alle Arbeit in Agenten lag —
  die Hauptsitzung plante, mergte und las Berichte.
- **Fertigmeldungen sind der Kostentreiber der Hauptsitzung:** 5 statt 13 ist der Unterschied
  zwischen Welle 25/26 und Welle 24 — mehr wert als jeder Formulierungstrick.
- **Codex als Qualitätsmanager findet echte P1** — vier Stück in drei Fable-Aufträgen (W26-A7).
- **Ein vierter Wächter bringt nichts** (W27: 41 / 1.160k / 78 min gegen 34 / 1.159k / 53 min
  bei dreien) — das zusätzliche Thema überlappte in den Dateien und erzeugte die ersten
  Merge-Konflikte.
- **Jeder Wächter braucht seinen EIGENEN Worktree** (W28). Wächter A und B teilten sich das
  Hauptrepo und wechselten sich mitten in der Welle gegenseitig den Branch weg. Regel:
  `git worktree add ~/Code/<projekt>-w<N>-<thema> -b w<N>-<thema> <basis>`, Arbeiter zweigen
  vom Integrationsbranch des Wächters in eigene Worktrees ab, und **niemand wechselt je den
  Branch im Hauptrepo**. Danach `.build` gemergter Worktrees aufräumen.
- **Am Build-Schloss AKTIV warten — nie anhalten und melden.** In W28 hielt Wächter A beim
  Warten auf `/tmp/<app>-build.lock` an und musste angestoßen werden: eine vermeidbare
  Anfrage plus Leerlauf. Die Schleife lautet
  `while ! mkdir /tmp/<app>-build.lock 2>/dev/null; do sleep 30; done` … danach `rmdir`.
  „Das Schloss ist belegt" ist nie ein Grund für eine Meldung.
- **Eine Logbuchzeile je Sitzung, immer** (`~/.claude/warm-handoff-log.md`): Datum, Kontext,
  worum die Welle ging, Rebuilds, Anfragen, Äquivalent, Verschwendung, Handoff-Pfad. Sie
  kostet nichts — sie reitet auf einem ohnehin laufenden Befehl mit — und ist der einzige
  Grund, warum es die Belegtabelle oben überhaupt gibt. Eine Welle ohne Logbuchzeile ist eine
  Welle, die man nicht vergleichen kann.
- **Stray-Meldungen von Arbeitern sind normal, kein Fehler.** Ein Arbeiter, dessen Wächter
  schon fertig ist, meldet sich in der Hauptsitzung (1× in W27). Lesen, notieren, NICHT die
  Arbeit neu starten — der Merge des Wächters enthält sie bereits.
- **Ein API-Abbruch ist fortsetzbar.** Stirbt ein Agent mitten im Auftrag, KEINEN neuen
  starten: `SendMessage` an dieselbe Agenten-ID — er behält seinen Kontext und macht weiter.
- **Wenn der Nutzer „Absturz" sagt, zuerst die Crash-Reports ansehen**, im selben Aufruf wie
  alles andere: `ls -t ~/Library/Logs/DiagnosticReports/<App>-*.ips | head`, dann den obersten
  Stack lesen. In W27 nannten sechs `.ips`-Dateien dieselbe Zeile — aus einer vagen Meldung
  wurde ein Einzeiler-Fix.
- **Reine Fable-Wellen kosten ~2,5× und sind nicht schneller** (W38, 01./02.09.2026: 5 Fable-
  Wächter, 20 Aufträge → 102 Anfragen, 3.147k, 116 min gegen W37 mit 38 / 1.270k / 65 min bei
  21 Aufträgen mit Opus-Wächtern). Zwei gemessene Ursachen: Die Fable-Wächter schickten 10
  Zwischenmeldungen „warte am Build-Schloss" (jede eine volle Anfrage der Hauptsitzung), und
  der serielle Schloss-Schwanz fraß 28 min; außerdem sprang der Wochenanteil von Fable am
  Kontingent über Nacht hoch. Regel des Nutzers seit 02.09.2026, 02:58: **Wächter und Arbeiter
  sind standardmäßig Opus/low; Fable/low nur, wenn der Nutzer den Auftrag benennt oder ein
  Auftrag schon 2–3 Mal gescheitert ist.** Fable kauft Tiefe bei einem festgefahrenen Problem,
  nicht Durchsatz in einer Welle.
- **Das Handoff beantworten statt chatten** — die Sitzung vom 02.09. bekam 25 Testantworten plus
  eine Sammlung in EINER Handoff-Datei über eine Stunde (null Anfragen), und die nächste Sitzung
  machte daraus in 4 Anfragen einen Plan mit 4 Wächtern. Das ist die billigste Stunde im Logbuch.
- **Eine Pause > 60 min kostet einen Neuaufbau (≈ Kontext × 2)** — bei 114k also ≈ 230k, und
  damit immer noch weniger als eine frische Sitzung mit ~200k Startaufbau plus Neu-Briefing.

## Bezahltes Kontingent — sehen, nutzen, nach Kontogröße

- `~/.claude/codex-limit.sh [--kurz|--json]` liest Codex `rate_limits` aus dessen letzter Session-
  Datei — nur so frisch wie der letzte Codex-Lauf; `null` = unbekannt, nicht 0. Einmal pro Sitzung
  einen kleinen Ping an den ersten echten Codex-Aufruf anhängen (`codex exec --skip-git-repo-check
  "Antworte nur mit: bereit"`). Claude-Code-Kontingent: `cat ~/.claude/.claude-kontingent`
  (5h/7d %, von der Statuszeile geschrieben; die Web-UI ist die Autorität bei Abweichungen).
- Handoff-Block "Was noch im Tank ist" direkt nach dem Status: Zahlen + Alter der Messung +
  ein KONKRETER Vorschlag, wenn viel frei ist (großes Review, langer Testlauf, Zweitmeinung).
  Ungenutztes Kontingent verfällt. Gemini/OpenRouter: kein auslesbares Guthaben — so sagen, nie schätzen.
- **Kleines Codex-Konto (Plus, ~20 $)** → Codex macht NUR QA: Review, Zweitmeinung, Testläufe,
  Abnahme. Keine Bau-Aufträge, kein "mach um 23:05 weiter". Großes Konto → frei nutzen.
- **Codex als Qualitätsmanager der Welle** (Nutzer, 30.08.2026, 03:05). Wenn das
  Codex-Kontingent frisch ist, lässt JEDER Themen-Wächter seinen Integrationsbranch von Codex
  reviewen, BEVOR er den Abschlussbericht schreibt, und fixt die P1-Befunde selbst — die Welle
  endet reviewt, nicht „wird später reviewt". Befehlsform: `git diff <basis>..HEAD | codex exec
  --skip-git-repo-check "Review this. Find bugs, risks, missing tests."` Beleg, dass das keine
  Zeremonie ist: In Welle 26 ließ Auftrag A7 Codex auf drei Fable-Aufträge schauen — Codex fand
  **4 P1-Befunde**, die die bauenden Agenten übersehen hatten. Kostet einen Codex-Aufruf je
  Wächter und null Anfragen der Hauptsitzung.

## Der Wellen-Workflow und die Handoff-Datei

Das Handoff nach jeder großen Welle schreiben, ungefragt. Pfad `<projekt>/_handoff-<projekt>-JJJJ-MM-TT[-b].md`
(Projektname im Dateinamen UND im Titel). Fließtext bei ~60–70 Zeichen umbrechen; Befehle,
Pfade, URLs auf einer Zeile. Referenzieren, nicht kopieren (Pfade/URLs); Geheimnisse schwärzen;
Skills für die nächste Sitzung nennen. Struktur, von oben nach unten:

1. Titel mit Datum/Uhrzeit. Dann die Kopierzeile für die nächste Sitzung:
   `> \`Ich habe das Handoff beantwortet: /abs/pfad/_handoff-….md\``
   plus "du kannst direkt in diese Datei schreiben — Zeilen mit >>> oder Name + Zeitstempel beginnen".
2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   (`- [ ] Pfad (Agent, gestartet HH:MM)`).
3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — den Sammelbereich des
   vorigen Handoffs UNMITTELBAR vor dem Schreiben lesen (im selben Tool-Aufruf wie der
   Ungespeichert-Wächter, inklusive ungespeichertem Editor-Text) und WÖRTLICH kopieren, dann
   ein Block "Was ich daraus gemacht habe", der jeden Punkt auf gebaut / beantwortet / Roadmap
   abbildet. Auch das Handoff DAVOR auf Nachträge prüfen. Nie den Text des Nutzers umschreiben.
4. Vorige Testantworten → was daraus wurde, eine Zeile je Punkt ("deine T1-Antwort übernommen
   als: … — richtig?"). Unbeantwortete Punkte werden markiert übernommen.
5. **Testliste vN** — jeder Punkt vorbelegt mit einer leeren `>>>Userantwort:`-Zeile.
6. Banner (Markdown-Überschriften fallen in TextEdit nicht auf — Linien und Großbuchstaben schon):
   ```
   ═══════════════════════════════════════════════════════════
      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   ═══════════════════════════════════════════════════════════
   >>>Userantwort:
   ```
7. **Der rote Faden** — die nächsten 2–3 Wellen als kurze Absätze, jeweils mit
   `>>>Hast du dazu noch was anzumerken?`; danach ein kompakter Themenspeicher; dann
   **Hauptdokumente** (3–6 echte Dateien mit absolutem Pfad + einer Zeile + Aktualität).
   Danach, PFLICHT, direkt nach den Hauptdokumenten und vor der Kostentabelle, der
   Gedächtnis-Block — die Gedächtnisdatei des Projekts, im Handoff selbst (Nutzer,
   30.08.2026: er will Claudes eigene Gedächtnisdatei abschalten und das Gedächtnis
   stattdessen im Handoff führen). Überschrift `## Gedächtnis`, zwei beschriftete Listen mit
   je **4–6 Zeilen**, kurz und konkret:
   ```
   **Langzeit (gilt immer):**   → Nordstern, Arbeitsregeln, Modellpolitik,
                                   Hausregeln, die jede Welle überleben
   **Kurzzeit (diese Wochen):** → Branch + Tip + Testzahl, was offen ist,
                                   Rechner-/Plattenzustand, aktuelle Testpunkte
   ```
   Vorlage für die Form: `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-30-e.md`,
   Abschnitt `## Gedächtnis`. Die Langzeit-Liste wörtlich aus dem vorigen Handoff übernehmen,
   solange sich nichts wirklich geändert hat; die Kurzzeit-Liste jedes Mal neu schreiben.
8. **Kostentabelle** via `~/.claude/session-costs.sh --markdown` (Einheit = Spanne zwischen zwei
   Nutzer-Nachrichten; k = Tausend erklären, Kontextspalte ≠ Kosten) + ehrliche Befunde, dann die
   Schlusszeile mit GEMESSENEM Kontext und Startkontext: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit `aus: /abs/pfad` und einem leeren `>>>`.
   Der Nutzer sammelt hier, während die nächste Welle läuft — Sammeln kostet null Anfragen.

Fragen an den Nutzer gehören ins Handoff (`## Fragen an dich` mit `>>>Antwort:`), nicht in den
Chat: eine Chat-Frage blockiert eine Welle, zehn in der Datei blockieren nichts. Wellen so
zuschneiden, dass sie ohne Rückfrage durchlaufen; die wahrscheinlichere Lesart nehmen und dokumentieren.
**Eskalations-Ausnahme — sofort im Chat fragen, vor dem Handeln**, wenn die Unklarheit
Folgendes berührt: unumkehrbare oder zerstörende Aktionen (`rm`, Historie umschreiben,
Force-Push, Daten verwerfen), alles rund um Sicherheit und Zugangsdaten, alles von außen
Sichtbare (Mail versenden, veröffentlichen, ausrollen, einen Live-Shop ändern), echtes Geld
oder ein großes Kontingent ausgeben, oder Repo-Inhalte an ein externes Modell schicken.
Alles Übrige gehört ins Handoff.

## Zwischenrufe — der freie Seitenkanal, während Agenten laufen (Nutzer, 02.09.2026, 19:41–19:59)

Jede Chat-Nachricht, die der Nutzer schickt, während die Hauptsitzung auf Hintergrund-Agenten
WARTET, ist eine volle Anfrage (der ganze Kontext wird neu gelesen). Ein Skill kann Nachrichten
nicht zurückhalten. Der freie Kanal ist EINE DATEI je Sitzung:
`<projekt>/_zwischenrufe-<projekt>-JJJJ-MM-TT-<a|b|c>.md`, zu Wellenbeginn angelegt und in
TextEdit geöffnet (`open -a TextEdit`). Zwei Abschnitte: **„Zwischenrufe (für diese Session)"**
— kurze Hinweise für die laufende Welle — und **„Sammlung für das nächste Handoff"** — Ideen,
Aufträge, Kritik. Die Handoff-Datei trägt kein eigenes SAMMLUNG-Banner mehr; die Sammlung lebt hier.

Regeln: Die Hauptsitzung liest die Datei bei JEDEM Aufwachen ZUERST, angehängt an einen ohnehin
laufenden Befehl (`cat _zwischenrufe-*-<datum>-*.md`), und nimmt nur das, was NEU ist. Sie löscht
nie; nach dem Lesen hängt sie unter den letzten gelesenen Eintrag eine Markerzeile
`— übernommen bis hier, HH:MM —`, damit beide Seiten sehen, wo „neu" beginnt. **Die Antwort
gehört ebenfalls in die Datei** (Nutzer, 03.09.2026, 16:58): unter den Marker kommt
`Antwort Claude, TT.MM.JJJJ-HH:MM:` und darunter DERSELBE Text, den der Nutzer sonst im Chat
sähe — was mit jedem Zwischenruf geschehen ist, Entscheidungen, Status — dann die Zeile
`— ab hier wieder Zwischenrufe —` und ein frisches `>>>`. Der Nutzer liest die Datei, nicht das
Terminal; eine Antwort, die nur im Chat landet, ist eine Antwort, die er suchen muss.

Weil die Datei in TextEdit offen ist: nie hineinschreiben, solange sie ungespeicherte Änderungen
hat. Live-Text per `osascript` lesen, den zusammengeführten Text auf die Platte schreiben,
schließen (`saving no`) und wieder öffnen — erst wenn TextEdit `modified = false` meldet.
Beim Handoff wird alles unterhalb des letzten Markers wörtlich in den Sammlungs-Block des
Handoffs kopiert. Eine neue Sitzung beginnt eine NEUE Datei (nächstes Datum/nächster Buchstabe);
die alte bleibt offen, bis der Nutzer sie schließt, und `sammlung-pruefen.sh` prüft beide.
Kopftext der Datei (deutsch): erklärt, was Chat-Nachrichten während des Wartens kosten, dass
Terminals lange Eingaben zu „[Pasted text]" zusammenklappen, und die Marker-Regel. Das Urteil
des Nutzers beim ersten Einsatz (19:57): „geniale Lösung — so sparen wir uns jedes Mal
mindestens eine Anfrage".

## Editor-Regeln (macOS / TextEdit)

- **RTF-Zwilling — Pflicht bei jedem Handoff** (Nutzer, 03.09.2026, 21:57). Direkt nach dem
  Schreiben der `.md`: `~/.claude/skills/warm-handoff/scripts/handoff-rtf.sh <handoff.md>`.
  Der Weg ist Markdown → HTML → `textutil -convert rtf`; die gleichnamige `.rtf` liegt
  danach daneben. BEIDE öffnen (`open -a TextEdit <datei>.rtf`). Vier Eigenschaften:
  1. **18 pt** Grundschrift, Überschriften fett und größer, `>>>`-Zeilen gelb hinterlegt.
  2. **Jeder Pfad und jede URL klickbar**, auch Screenshot-Pfade mit Leerzeichen: sie werden
     zu `file://`-Links mit prozent-codierten Leerzeichen
     (`.../ScreenshotY%202026-09-03%20um%2021.10.04.jpg`). Ein roher Pfad mit Leerzeichen ist
     in TextEdit kein Link — codieren, nicht in Anführungszeichen setzen.
  3. **Die Kopf-Kopierzeile bleibt EINZEILIG** (kleinere Schrift, `white-space: nowrap`),
     damit der Pfad zum Zurückkopieren nicht zerrissen wird.
  4. **Der Nutzer antwortet IN der RTF**, unter den `>>>Userantwort:`-Markern — dafür ist der
     Zwilling da: ein Arbeitsdokument, kein Ausdruck.
  Die Antworten liest der Agent mit `textutil -convert txt -stdout <datei>.rtf` zurück (ein
  Befehl, kein Umweg über Editor oder AppleScript). Das Markdown bleibt die Quelle für das,
  was DU schreibst: Änderungen in die `.md`, danach den Zwilling neu erzeugen; die Antworten
  des Nutzers stehen in der `.rtf` und wandern von dort in die Sammlung des nächsten Handoffs.
- Jedes nutzerseitige Dokument sofort öffnen: `open -a TextEdit <datei>`. Das gilt für jedes
  neu erwähnte Dokument, nicht nur das Handoff — einen Plan, einen QA-Bericht, eine Review-
  Datei: sobald es existiert und für den Nutzer zum Lesen gedacht ist, öffnen. Einmal anbieten:
  Tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt Standardschrift
  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md`-Standardapp via `duti`.
- **Ungespeichert-Wächter vor dem Lesen:**
  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
  falls geändert, den Live-Text lesen (`… get text of (first document whose name is "…")`).
- **Nie in das offene Handoff des Nutzers schreiben, es schließen, speichern oder verschieben.**
  Ein neues Handoff ist immer eine NEUE Datei. Alte nach `handoff-archiv/` archivieren (mv, nie rm)
  erst nachdem der Nutzer sie geschlossen hat; sonst "Archivierung ausstehend" im neuen Handoff vermerken.
- Wenn Claude eine vom Nutzer geöffnete Datei bearbeitet hat und sie unverändert ist → schließen
  + neu öffnen, damit die neue Version sichtbar wird; geändert → fragen, nie schließen.
- Einmal sagen: lange Diktate gehören ins Handoff-Dokument, kurze Befehle ins Terminal (Terminals
  klappen lange Eingaben zu `[pasted text]` zusammen); TextEdit ▸ Ablage ▸ Zuletzt geöffnet findet
  verlorene Handoffs.

## Cache-Neuaufbau — erkennen, nicht raten

Trefferquote = Σ cache_creation / Σ cache_read aus der Session-JSONL; < 10 % = warm. Große
Einzel-Schreibvorgänge sind meist Anhänge, keine Neuaufbauten. Einen Neuaufbau EINMAL erwähnen,
mit Ursache, nur wenn sie ableitbar ist: Lücke > 60 Min zwischen zwei `date`-Lesungen, ein Modell-/
Effort-Wechsel, eine CLAUDE.md-Bearbeitung, ein MCP-Neustart. Unbekannte Ursache → nichts sagen.
Kosten als Arithmetik erklären ("22k, weil der Kontext 220k groß ist und Lesen ×0,1 kostet"), nie
als Behauptung; eigene frühere Fehlaussagen explizit korrigieren.

## Logbuch und Setup

Pro Handoff eine Zeile an `~/.claude/warm-handoff-log.md` anhängen:
`| 22.08.2026 14:40 | ctx 85k | 2 Wellen | Neuaufbauten: 1 (Pause 90min) | geschätzte Verschwendung ~60k |`
Muster alle ~50 Einträge zusammenfassen. Immer aktiv: "Zu Beginn jeder Sitzung den warm-handoff-
Skill aufrufen." in `~/.claude/CLAUDE.md` ergänzen. Skripte: `scripts/ctx.sh`,
`scripts/session-costs.sh` (im Repo liegt der identische deutsche Alias `session-kosten.sh`; installiert wird `session-costs.sh` — diesen Namen überall verwenden), `scripts/codex-limit.sh` → nach `~/.claude/` kopieren.
Terminal-neutral: "deine Statuszeile" sagen, nicht ein Feld eines bestimmten Hosts.
