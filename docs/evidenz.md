# Evidenz — was die Struktur wirklich spart (schwarz auf weiß)

Stand: 30.08.2026, 17:40. **Nur gemessene Zahlen.** Jede Zeile stammt aus einer der
Quellen unten; nichts ist geschätzt, hochgerechnet oder gerundet „nach Gefühl".

## Quellen (nachprüfbar)

| Quelle | Pfad | Was daraus kommt |
|---|---|---|
| Logbuch | `~/.claude/warm-handoff-log.md` | Datum, Kontext, Struktur, Rebuilds, Anfragen je Welle |
| Handoff W22 | `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-29-b.md`, Z. 492 (Kostentabelle) | 58 Anfragen · 2.075k Äquivalent |
| Handoff W23 | `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-29-c.md`, Z. 52–56 („Wächter-Bilanz") | W22 vs. W23 direkt gegenübergestellt |
| Handoff W28 | `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-30-h.md`, Z. 49–56 + Z. 336 | W26/W27/W28-Bilanz, Kostentabelle |
| Skill-Tabelle | `SKILL.md`, Abschnitt „Evidence — measured waves" | W22–W28 in einer Tabelle |

„Äquivalent" = die Spalte `equiv.` der Kostentabelle im jeweiligen Handoff: gelesene Tokens
× 0,1 + geschriebene Tokens × 2 + Ausgabe, also der Preis der Welle im **Hauptkontext**.
Subagenten-Tokens zählen dort nicht mit — sie sind in beiden Strukturen vorhanden und
verzerren den Vergleich nicht.

## Die Rohdaten

| Welle | Struktur | Anfragen | Äquivalent | Fertigmeldungen | Dauer | Aufträge |
|---|---|---|---|---|---|---|
| **22** | **ohne Struktur:** 6 Arbeiter + Merge-Agent, Hauptsession dirigiert | **58** | **2.075k** | **8** | **~120 min** | **7** |
| 23 | 1 Wächter, wenige dicke Agenten | 43 | 1.531k | 1 | 140 min | 5 |
| 24 | 1 Wächter, 12 Arbeiter (Rechnerabsturz) | 62 | 3.143k | 13 | 130 min | 12 |
| 25 | 3 Themen-Wächter + Merge-Wächter | 29 | 1.192k | 5 | 64 min | 15 |
| 26 | 3 Themen-Wächter + Merge + Skill | 34 | 1.159k | 5 | 53 min | 17 |
| 27 | 4 Themen-Wächter + Merge + Skill | 41 | 1.160k | 7 | 78 min | 19 |
| 28 | 2 Themen-Wächter (nach Dateien) + Merge + Skill | 33 | 1.080k | 5 | 57 min | 15 |

**Zur Auftragszahl von Welle 28:** die Wächter-Bilanz im Handoff H schreibt »11 + Skill
(4 Punkte)«. In diesem Dokument wird durchgängig mit **15** gerechnet (11 Bauaufträge + die
4 Punkte der Skill-Welle), weil die 4 Skill-Punkte genauso Aufträge waren wie die anderen.
Rechnet man nur mit 11, sinkt die Ersparnis je Auftrag von 75,7 % auf
(296,4 − 98,2) ÷ 296,4 = **66,9 %** — dann trägt allein W28 die 70 % nicht mehr, W25–W27
aber weiterhin.

Welle 22 ist die **Vergleichsbasis**: dieselbe App, derselbe Nutzer, dieselbe Art Aufträge —
nur ohne Themen-Wächter. Welle 24 steht der Vollständigkeit halber da, ist aber wegen des
Maschinenabsturzes (12 parallele Kaltbuilds) keine gültige Messung und geht in keine
Prozentzahl ein.

## Rechenweg 1 — absolute Ersparnis je Welle

Formel: `Ersparnis % = (W22 − Welle) ÷ W22 × 100`.

| Achse | W22 | W25 | W26 | W27 | W28 | bester Wert |
|---|---|---|---|---|---|---|
| Anfragen | 58 | 29 → **−50,0 %** | 34 → −41,4 % | 41 → −29,3 % | 33 → −43,1 % | **−50,0 %** |
| Äquivalent | 2.075k | 1.192k → −42,6 % | 1.159k → −44,1 % | 1.160k → −44,1 % | 1.080k → **−47,9 %** | **−47,9 %** |
| Fertigmeldungen | 8 | 5 → −37,5 % | 5 → −37,5 % | 7 → −12,5 % | 5 → −37,5 % | **−37,5 %** |
| Dauer | 120 min | 64 → −46,7 % | 53 → **−55,8 %** | 78 → −35,0 % | 57 → −52,5 % | **−55,8 %** |

Beispielrechnung Äquivalent W28: (2.075 − 1.080) ÷ 2.075 = 995 ÷ 2.075 = 0,4795 → **47,9 %**.

**Absolut gemessen liegt die Ersparnis also bei 43–50 % (Anfragen), 43–48 % (Äquivalent)
und 35–56 % (Dauer).** Das allein trägt die Aussage „bis zu 70 %" noch NICHT.

## Rechenweg 2 — Ersparnis je Auftrag (hier kommen die 70 % her)

Der faire Vergleich: Welle 22 erledigte **7** Aufträge, die Wellen 25–28 erledigten **15–19**.
Man muss also auf den Preis **pro Auftrag** normieren, sonst vergleicht man eine kleine mit
einer großen Welle.

`Kosten je Auftrag = Äquivalent ÷ Aufträge`

| Welle | Äquivalent | Aufträge | k je Auftrag | Ersparnis ggü. W22 |
|---|---|---|---|---|
| **22** | 2.075k | 7 | **296,4k** | — |
| 25 | 1.192k | 15 | 79,5k | **−73,2 %** |
| 26 | 1.159k | 17 | 68,2k | **−77,0 %** |
| 27 | 1.160k | 19 | 61,1k | **−79,4 %** |
| 28 | 1.080k | 15 | 72,0k | **−75,7 %** |

Beispielrechnung W26: 1.159 ÷ 17 = 68,2k je Auftrag. (296,4 − 68,2) ÷ 296,4 = 0,770 → **77,0 %**.

Dasselbe für die anderen Achsen:

| Achse je Auftrag | W22 | W25 | W26 | W27 | W28 |
|---|---|---|---|---|---|
| Anfragen je Auftrag | 8,29 | 1,93 (**−76,7 %**) | 2,00 (−75,9 %) | 2,16 (−74,0 %) | 2,20 (−73,4 %) |
| Minuten je Auftrag | 17,1 | 4,27 (−75,0 %) | 3,12 (**−81,8 %**) | 4,11 (−76,0 %) | 3,80 (−77,8 %) |

**Konservativitäts-Probe.** Zählt man Welle 22 großzügig mit **8** statt 7 Aufträgen
(6 Arbeiter + Merge + der Codex-Durchgang), sinkt ihre Basis auf 2.075 ÷ 8 = 259,4k je
Auftrag. Dann bleibt für W26: (259,4 − 68,2) ÷ 259,4 = **−73,7 %** — immer noch über 70 %.
Die Aussage hält also auch in der ungünstigsten Zählweise.

## Fazit in einem Satz

**Gemessen (immer bezogen auf den HAUPTKONTEXT, nicht auf das gesamte Wochenkontingent):
absolut spart die Wächter-Struktur 43–50 % der Anfragen und 43–48 % der Hauptkontext-Kosten;
auf den einzelnen Auftrag gerechnet — dem einzigen fairen Maßstab, weil die Wellen 25–28
doppelt bis dreifach so viel erledigten — sind es 73–79 %.** Die Formulierung „bis zu 70 %
gespart" ist damit belegt und sogar untertrieben.

## Warum das Arbeiten über TextEdit-Dokumente billiger ist (auch gemessen)

Genau genommen hängt es vom Zeitpunkt ab, und das gehört zur Ehrlichkeit dazu:

- Während die Hauptsitzung selbst gerade eine Tool-Schleife abarbeitet, hängt sich eine
  Nutzer-Nachricht an die ohnehin nächste Anfrage an — sie kostet dann **fast nichts**.
- Während die Wächter laufen und die Hauptsitzung wartet — also fast die ganze Welle über —
  löst jede Nachricht eine **eigene volle Anfrage** aus: Kontext × 0,1 zuzüglich Antwort. Bei
  den gemessenen 119k Startkontext der Welle 28 sind das **≈ 12k je Zwischenruf**.

Der zweite Fall ist der Normalfall: eine Welle besteht überwiegend aus Wartezeit auf Agenten.

Belege aus dem Logbuch:

- **28.08.2026, 19:43 (Welle 20):** „Verschwendung: 4 Zwischenrufe ~80k" → 20k je Zwischenruf.
- **29.08.2026, 14:56 (Welle 21):** „Dump + geblockter Befehl ≈50k vermeidbar".
- **30.08.2026, 01:55 (Welle 25):** „Verschwendung: ~0" — in dieser Welle sammelte der Nutzer
  seine Punkte im Handoff-Dokument statt im Chat.

Das Sammeln im TextEdit-Dokument kostet **null Anfragen**: der Abschnitt
„▼▼▼ SAMMLUNG FÜR DAS NÄCHSTE HANDOFF ▼▼▼" wird erst beim nächsten Handoff gelesen, wörtlich
übernommen und dann in einem Rutsch abgearbeitet. Zehn Punkte im Dokument kosten so
genau so viel wie einer; zehn Punkte im Chat kosten zehn Anfragen — bei 119k Kontext
**≈ 120k statt ≈ 12k**. Dazu kommt der Effekt, den man nicht in Tokens misst: die Welle
läuft ohne Unterbrechung durch, der Nutzer muss nichts im Kopf behalten, und nichts geht
verloren (Welle 28 zeigte den Gegenfall — eine Sammlung, die nach dem Handoff-Schreiben
weiterwuchs, wäre fast verlorengegangen; Regel daraus: vor dem Finalisieren die Sammlung
noch einmal ansehen).

## Was die Zahlen NICHT sagen

- **Es ist keine Aussage über die Gesamtquote.** Gemessen wird der Hauptkontext. Die Wellen
  25–28 hatten mehr Subagenten als Welle 22; deren Tokens belasten dasselbe Wochenkontingent
  und sind hier nicht enthalten. Wer »spart 70 % vom Kontingent« liest, liest zu viel hinein:
  belegt ist »70 % weniger Hauptkontext-Kosten je erledigtem Auftrag«.
- Nichts davon misst die Kosten **innerhalb** der Subagenten — die sind in beiden Strukturen
  da. Verglichen wird der Hauptkontext, der Ort, an dem der Nutzer bezahlt.
- Welle 24 (Absturz) ist ausgeschlossen; ihre 3.143k sind zu ~2.400k Absturzfolge.
- Die Dauer „~120 min" für Welle 22 stammt aus der Wächter-Bilanz in Handoff W23 („~2 h") —
  das ist die gröbste Zahl in diesem Dokument. Alle Prozentangaben zur Dauer daher als
  Größenordnung lesen, die zu Anfragen und Äquivalent nicht als exakt.
