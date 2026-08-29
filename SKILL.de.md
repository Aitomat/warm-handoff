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

## Die Fakten (Claude-Code-Doku, 2026-08)

- Pro/Max: **1 Stunde gleitendes Cache-TTL** — jede Anfrage setzt es zurück. Subagenten: strikt 5 Min.
- Cache-Killer unabhängig von der Uhr: `/model`- oder `/effort`-Wechsel mitten in der Sitzung,
  CLAUDE.md/Systemprompt bearbeiten, MCP-Server-Neustart. Modell + Effort beim Sitzungsstart festlegen.
- Preise relativ zu frischem Input: **Cache-Lesen ×0,1 · Cache-Schreiben ×2 (1-h-TTL) · eigene Ausgabe ×5.**
- Jede Anfrage liest den gesamten Prefix neu. Kosten = Anfragen × Kontext. Die Nachrichten
  des Nutzers sind ein Rundungsfehler; die eigenen Tool-Schritte und Berichte des Agenten sind die Rechnung.

## Jede Antwort — drei Ehrlichkeitsregeln

1. **Zeitstempel aus einem `date`-Aufruf IN DIESER Antwort** (`date "+%d.%m.%Y %H:%M"`,
   huckepack auf einen ohnehin laufenden Befehl). Kein `date` in dieser Runde → kein Zeitstempel.
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

## Subagenten — die Standardarbeitsweise

- **Wächter-Agent (Guardian).** Für eine Bau-Welle bekommt EIN orchestrierender Agent (Opus,
  low/normal Effort) den ganzen Plan als Datei, startet die Arbeits-Agenten selbst, merged,
  testet, bündelt, räumt `.build` von gemergten Worktrees auf, schreibt den Bericht — die
  Hauptsitzung wird EINMAL geweckt statt einmal pro Agent (8 → 1 Meldungen ≈ 140k gespart bei 190k Kontext).
  Fragen der Arbeiter landen beim Wächter, also müssen die Aufträge vollständig sein: Pfade, Ziel,
  Grenzen, Abnahmekriterien, "keine Rückfragen — entscheiden, die Annahme dokumentieren".
- **Der Wächter startet alle Arbeiter gleichzeitig, in EINER Nachricht** (ein Batch von Agent-
  Aufrufen), nie nacheinander — ein serieller Schwanz von Arbeitern macht aus einer günstigen
  Welle eine lange. Der ERSTE Schritt jedes Arbeiters ist, den aktuellen Branch-Tip zu ziehen
  (`git pull` / `git fetch && git rebase`), bevor er irgendeine Datei anfasst, damit er nie auf
  einer veralteten Basis baut.
- **Agenten auf ~30 Minuten, EINEN Auftrag kürzen** (nicht 40 Minuten / 2–3 Aufgaben — ein einziger
  fokussierter Auftrag landet schneller und lässt sich leichter mergen). Längere Arbeit liefert in
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
- **Modell + Effort im sichtbaren Label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
  Fable 5 als Subagent: **immer Effort low**; für schwieriges Review/Design Opus oder eine zweite
  Architektur (Codex/GPT) nutzen. Nie die eigene Ausgabe selbst reviewen — an Codex weiterleiten.
- **Agenten testen vor dem Nutzer.** Volle Suite + ein QA-Agent, der die App startet und jeden
  Testpunkt einmal anklickt; der Nutzer sollte meist nur "funktioniert, danke" sagen. **Der QA-
  Agent schließt die Fenster/Prozesse, die er zum Testen geöffnet hat**, bevor er fertig meldet —
  der Nutzer soll keinen Haufen liegengebliebener Testinstanzen erben.
- Berichtsvertrag: ≤ 300 Wörter, Status/Entscheidungen/Belege-mit-Pfaden/Risiken/Nächstes; keine
  Chronik, keine eingefügten Logs. Subagenten-Token zählen trotzdem aufs Wochenkontingent — was sie
  sparen, ist der HAUPTkontext (jeder Schritt ≈ 1/5 der Kosten, und nichts davon bleibt in der Sitzung).
- Taktung: Nutzer anwesend + in Eile → parallel; Nutzer abwesend → seriell (jede Fertigmeldung
  hält den Cache warm). Nie Beschäftigungstherapie erfinden.

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
8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (Einheit = Spanne zwischen zwei
   Nutzer-Nachrichten; k = Tausend erklären, Kontextspalte ≠ Kosten) + ehrliche Befunde, dann die
   Schlusszeile mit GEMESSENEM Kontext und Startkontext: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit `aus: /abs/pfad` und einem leeren `>>>`.
   Der Nutzer sammelt hier, während die nächste Welle läuft — Sammeln kostet null Anfragen.

Fragen an den Nutzer gehören ins Handoff (`## Fragen an dich` mit `>>>Antwort:`), nicht in den
Chat: eine Chat-Frage blockiert eine Welle, zehn in der Datei blockieren nichts. Wellen so
zuschneiden, dass sie ohne Rückfrage durchlaufen; die wahrscheinlichere Lesart nehmen und dokumentieren.

## Editor-Regeln (macOS / TextEdit)

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
`scripts/session-costs.sh`, `scripts/codex-limit.sh` → nach `~/.claude/` kopieren.
Terminal-neutral: "deine Statuszeile" sagen, nicht ein Feld eines bestimmten Hosts.
