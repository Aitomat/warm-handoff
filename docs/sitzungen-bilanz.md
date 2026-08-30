# Sitzungsbilanz seit Skill-Start (22.08.–30.08.2026)

Stand: 30.08.2026, 00:52.

**Quellen und was woher kommt — bitte beim Lesen mitdenken:**

- **Alle Zeilen der Tabelle** stammen aus `~/.claude/warm-handoff-log.md`
  (Logbuch, eine Zeile je Handoff/Wellenende, von Hand beim Schreiben des
  Handoffs angehängt). Kontextwerte dort mit `~` sind Schätzungen aus der
  Statuszeile, Werte ohne `~` gemessen über `ctx.sh`.
- **`~/.claude/session-kosten.sh --markdown`** liest die JSONL der jeweils
  laufenden Sitzung. Es ist damit **nur für die aktuelle Sitzung
  aussagekräftig** — für vergangene Sitzungen liegen die Zahlen nicht mehr
  vor. Messung zum Zeitpunkt dieser Datei (Sitzung, in der Welle 25 lief):
  1 Abschnitt, **19 Anfragen, Kontext 107k, 1.359k gelesen, 302k
  geschrieben, 55k Ausgabe, Äquivalent 1.016k**. Diese Zahl steht in der
  Tabelle NICHT in einer Wellenzeile, weil sie nicht einer Welle zuzuordnen
  ist.
- Alles, was das Logbuch nicht festhält, steht als **„nicht gemessen"**.
  Es wird nichts hochgerechnet und nichts erfunden.

## Tabelle

| Datum/Zeit | Projekt / Welle | Kontext Start→Ende | Agenten / Struktur | Neuaufbauten | geschätzte Verschwendung | Handoff-Datei |
|---|---|---|---|---|---|---|
| 22.08. 14:45 | Aitomat, Welle 2 (läuft) | nicht gemessen → ~95k | nicht gemessen | 0 (warm seit Start) | 0 | nicht gemessen |
| 22.08. 17:10 | Aitomat, Welle 2 fertig (Escape, Menüs, Dock, Freeze-Fix) | nicht gemessen → ~150k | nicht gemessen | 0 | nicht gemessen | Handoff B |
| 22.08. 16:58 | Aitomat, Wellen 3+4 (Regressionen, Chat, Orb, Ton-Deckel) | nicht gemessen → ~190k | nicht gemessen | 0 | nicht gemessen | Handoff C, Testliste v54 |
| 22.08. 17:55 | Aitomat, Welle 5 läuft (Audio-Gate, Orb R3, KI-Ton, Design-Review) | nicht gemessen → 400k (Schwelle) | 471 Anfragen | 0 seit 12:10 | nicht gemessen | Empfehlung: Handoff D + frische Sitzung |
| 22.08. 18:58 | Aitomat, Welle 5 fertig | nicht gemessen → 457k | 541 Anfragen seit 12:10 | 0 | nicht gemessen | Handoff D FINAL, Testliste v55 |
| 23.08. 15:10 | Aitomat, Welle 6 | nicht gemessen → ~65k | 5 Agenten + Codex R30/R31, Ox (429) | 0 | nicht gemessen | Build 9, beide Branches gepusht |
| 23.08. 17:10 | Mail v2.7 + SEO/Ads/YT-Lagecheck | nicht gemessen → ~85k | nicht gemessen | 1 (Pause 12 Tage) | nicht gemessen | Handoff 23.08. |
| 23.08. 17:54 | Aitomat, Wellen 6+7 | nicht gemessen → ~240k | 13 Agenten, Codex R30–R33, Vorlesen W1 | 0 | nicht gemessen | Build 10, Sweetspot-Regel neu |
| 23.08. 18:06 | Abend-Welle autonom (Ads, GSC-Cluster, Konkurrenz, F8) | nicht gemessen → ~160k | nicht gemessen | 0 | 0 (Cache bewusst warm gehalten) | nicht gemessen |
| 23.08. 19:26 | Weckruf verspätet (19:26 statt 18:50, Mac im Schlaf) | nicht gemessen → ~165k | nicht gemessen | 1 (Fenster 18:06→19:06 abgelaufen) | **~165k** Cache-Write | nicht gemessen |
| 24.08. 21:35 | Analyse + Mail v2.8 + YouTube + PrefSources | nicht gemessen → ~90k | 1 Welle | 0 | nicht gemessen | Handoff geschrieben |
| 24.08. 22:04 | Welle 8 | nicht gemessen → ~60k | 6 Agenten parallel, 5 Branches gemergt | 0 | nicht gemessen (4× Stopp beim Test-Warten, Nudges nötig) | nicht gemessen |
| 24.08. 22:56 | 2 Wellen (Tonalität, Tissen-Schutz, PrefSources) | nicht gemessen → ~140k | nicht gemessen | 0 | nicht gemessen | nicht gemessen |
| 24.08. 23:15 | Welle 9 | nicht gemessen → ~80k | 5 Agenten, alle gemergt, Bundle 12 | 0 | nicht gemessen (2× Wartefalle trotz Verbot) | nicht gemessen |
| 24.08. 23:51 | 3 Wellen (Garantie-Prinzip live) | nicht gemessen → ~175k | nicht gemessen | 0 | nicht gemessen | nicht gemessen |
| 25.08. 15:07 | Welle 14 (8 Punkte) | nicht gemessen → 260k | 6 Agenten | 0 | nicht gemessen (API-Gegenwert ~94 $) | nicht gemessen |
| 25.08. 17:23 | Welle 14 + Testrunde | 82k → ~310k | 8 Agenten, 205 Anfragen (15 vom Nutzer) | 0 | nicht gemessen | Cache-Write-Faktor korrigiert (×2) |
| 25.08. 20:11 | Wellen 14 + 14b + 14c | nicht gemessen → >400k | 11 Agenten, 269 Anfragen (15 vom Nutzer) | 0 | nicht gemessen | CPU-Runaway als Absturzursache gefunden |
| 28.08. 16:45 | Welle 19 | nicht gemessen → 205k | 7 Agenten (Fable/low), 4705 Tests grün | 0 | nicht gemessen | Fable-Filter-Fehlalarm → Opus 4.8 |
| 28.08. 19:43 | Welle 20 | ~110k → 160k | 6 Agenten + Merge-Agent | 0 | **~80k** (4 Zwischenrufe) | Codex-5h-Limit 18:38, Auto-Start 23:05 |
| 29.08. 14:56 | Aitomat, Welle 21 | 125k → 175k | 8 Agenten (7 Opus5 + Merge) | 0 | **~50k** vermeidbar (Dump + geblockter Befehl); ~110k Fertigmeldungen unvermeidbar | `_handoff-aitomat-2026-08-29.md` |
| 29.08. 18:08 | Aitomat, Welle 22 | 125k → 192k | 6 Opus + Merge + 2 Codex-Analysen + Codex-QS, 4906 Tests | 0 | ~145k (8 Fertigmeldungen); Platte voll → 27 `.build`-Caches gelöscht | nicht gemessen |
| 29.08. 21:10 | Aitomat, Welle 23 | nicht gemessen → 178k | 1 Wächter (1 Meldung statt 8), Skill 172 Z. | 0 | nicht gemessen (Kosten niedrig, aber 2 Std. 20 Wanduhr) | Handoff C |
| 30.08. 00:10 | Aitomat, 1 Welle + Skill A2 | nicht gemessen → 139k | nicht gemessen | 1 (Rechner-Absturz 22:00) | **~700k** | Handoff D |
| 30.08. 00:44–01:51 | Aitomat, Welle 25 (Themen-Wächter) | ~107k → 120k (gemessen 01:51) | 3 Themen-Wächter + 1 Merge-Wächter, 15 Arbeiter, 29 Anfragen, 2.495k gelesen / 319k geschrieben / 61k Ausgabe, Äquivalent **1.192k**, 5 Fertigmeldungen, 64 min (00:46–01:50) | 0 (kein Absturz) | 0 — die 319k „geschrieben" sind der Start-Cacheaufbau (~107k ×2) plus Handoff-/Plan-Anhänge, kein Neuaufbau | `_handoff-aitomat-2026-08-30-e.md` (Handoff E) |

## Muster — was sich seit 22.08. verbessert hat, was nicht

1. **Der Kontext ist beherrscht.** Am 22.08. lief eine Sitzung bis 457k und
   541 Anfragen; seit dem 28.08. enden Sitzungen zwischen 139k und 205k.
   Die Sweetspot-Tabelle und das Handoff-Ritual wirken — das ist die
   deutlichste Verbesserung der Woche.
2. **Cache-Neuaufbauten sind fast verschwunden.** 24 Logzeilen, drei
   Neuaufbauten: eine 12-Tage-Pause (unvermeidbar), ein verschlafener
   Weckruf (~165k) und ein Rechner-Absturz (~700k). Keiner davon ging auf
   ein Modell-/Effort-Umschalten oder eine CLAUDE.md-Bearbeitung zurück —
   die Regel „Modell und Effort beim Start festlegen" hält.
3. **Die Fertigmeldungen waren der teuerste bekannte Posten** und sind
   gelöst: 8 Meldungen ≈ 145k am 29.08. mittags, eine einzige Meldung am
   Abend über den Wächter. Diese eine Regel hat mehr gespart als alle
   Formulierungs-Tricks zusammen.
4. **Die Wanduhr blieb dabei auf der Strecke.** Welle 23 war die
   günstigste und zugleich die langsamste (2 Std. 20). Token-Sparen und
   Warten-Sparen sind zwei Achsen; das Logbuch misst bisher nur die erste.
   **Welle 25 hat diesen Zielkonflikt aufgelöst.** Mit 3 Themen-Wächtern +
   1 Merge-Wächter über 15 Arbeiter war sie die **günstigste UND die
   schnellste Welle bisher**: 29 Anfragen und 1.192k Äquivalent gegen
   43/1.531k (W23), 58/2.075k (W22) und 62/3.143k (W24) — und 64 Minuten
   gegen 2 Std. 20 (W23), ~2 Std. (W22), 2 Std. 10 (W24). Der Grund ist
   strukturell, nicht glücklich: die Themen-Wächter starten ihre 4–6
   Arbeiter parallel, und der Merge-Wächter zieht den seriellen Schwanz
   (Build, volle Suite, Bundle, QA) auf einen einzigen Durchlauf zusammen.
   Zugleich blieben es 5 Fertigmeldungen statt 13 wie in Welle 24.
5. **Der Rechner ist der neue Engpass, nicht das Kontingent.** Innerhalb
   von 24 Stunden: Platte voll (27 `.build`-Caches), dann Absturz durch 12
   gleichzeitige Kaltbuilds (~700k Verschwendung). Beide Vorfälle sind
   Ressourcen-, keine Token-Probleme. Daher das Build-Schloss ab Welle 25.
6. **Wiederkehrend ungelöst: Agenten warten auf Tests.** Am 24.08. zweimal
   an einem Abend „Wartefalle trotz Verbot" — die Regel steht im Skill,
   greift aber nicht zuverlässig. Offener Punkt.
7. **Die Messdisziplin selbst ist lückenhaft.** In der Mehrzahl der Zeilen
   fehlt der Startkontext, und „geschätzte Verschwendung" ist nur sechsmal
   beziffert. Ohne Startkontext lässt sich der Break-even nicht nachrechnen
   — das Logbuch sollte künftig Start UND Ende, Agentenzahl und Struktur
   verpflichtend führen.
8. **Rückwirkend messen geht nicht.** `session-kosten.sh` sieht nur die
   laufende Sitzung; alles, was nicht beim Wellenende ins Logbuch kam, ist
   dauerhaft verloren. Deshalb: die Zeile schreiben, bevor die Sitzung endet.
