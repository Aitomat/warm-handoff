# warm-handoff 🏄

> **Hauptsprache des Repos ist Englisch: [README.md](README.md). Dies ist die deutsche Fassung.**

**Ein Claude-Code-Skill, der die Sitzung um das Prompt-Cache-Fenster herum taktet: Er
misst, wo man steht, hält die Zahl der Anfragen klein und schreibt im richtigen Moment
ein Übergabedokument.**

Autor: **Yasin Akgün** ([github.com/Aitomat](https://github.com/Aitomat)). Entstanden beim
täglichen Bauen von [Aitomat](https://aitomat.ai) mit Claude Code — jede Regel im Skill war
zuerst eine Sitzung, die schiefging, oder eine Rechnung, die seltsam aussah.

---

## Inhalt

1. [Das Problem in drei Minuten](#1-das-problem-in-drei-minuten)
2. [Die Kosten-Arithmetik mit echten Zahlen](#2-die-kosten-arithmetik-mit-echten-zahlen)
3. [Der Wellen-Workflow](#3-der-wellen-workflow)
4. [Subagenten-Ökonomie](#4-subagenten-ökonomie)
5. [Was der Skill sichtbar macht: Kostenzeile, Kostentabelle, Kontingent](#5-was-der-skill-sichtbar-macht)
6. [Installation](#6-installation)
7. [Die Skripte](#7-die-skripte)
8. [Ehrliche Grenzen](#8-ehrliche-grenzen)
9. [Die Fakten, auf denen alles steht](#9-die-fakten-auf-denen-alles-steht)
10. [Danksagung, Vorarbeiten, Lizenz](#10-danksagung-vorarbeiten-lizenz)

---

## 1. Das Problem in drei Minuten

Wer Claude Code benutzt, sieht eine Chat-Oberfläche. Was er nicht sieht:

- **Jede Nachricht ist nicht eine Anfrage, sondern viele.** Claude liest eine Datei, sucht,
  ändert, führt einen Befehl aus, liest das Ergebnis — jeder dieser Schritte ist eine
  eigene Anfrage an das Modell, und **jede** dieser Anfragen schickt den gesamten bisherigen
  Gesprächsverlauf mit. Eine harmlose Bitte wie „bau das bitte ein und teste es" kann 30
  bis 150 Anfragen auslösen.
- **Der Verlauf wächst und wird jedes Mal mitgeschickt.** Nach zwei Stunden Arbeit ist das
  Gespräch 200.000–500.000 Token groß. Jeder der 150 Schritte trägt diesen Rucksack.
- **Es gibt einen Cache, der das erträglich macht — aber nur im Zeitfenster.** Claude Code
  legt den Gesprächsanfang (Prefix) in einen Prompt-Cache. Lesen aus dem Cache kostet ein
  Zehntel. Auf Pro/Max hält dieser Cache **eine Stunde, gleitend** — jede Anfrage setzt die
  Uhr zurück. Wer eine Stunde Pause macht, das Modell wechselt, den Effort verstellt oder
  die CLAUDE.md editiert, baut den Cache neu auf: der gesamte Verlauf wird einmal zum
  **doppelten** Preis geschrieben.
- **Nichts davon steht irgendwo.** Kein Zähler zeigt die Kontextgröße, keiner die Zahl der
  Anfragen, keiner, ob die letzte Runde teuer oder billig war. Also optimieren die Leute das
  Falsche — sie tippen kürzere Nachrichten — während die eigentlichen Kosten in einer
  Arbeitsschleife aus Dateizugriffen stecken, die sie nie sehen.

Die Messung, die diesen Skill ausgelöst hat: Ein Abschnitt einer echten Sitzung — „Handoff
beantwortet, bitte umsetzen" — kostete **147 Anfragen** bei 223k Kontext, umgerechnet
**4.380k Token-Äquivalente**. Derselbe Arbeitsumfang, in Subagenten delegiert und gebündelt,
braucht im Hauptkontext **14 Anfragen**. Das ist der Hebel, um den es hier geht: nicht
kürzer schreiben, sondern **weniger Anfragen im fetten Kontext**.

## 2. Die Kosten-Arithmetik mit echten Zahlen

Alle Zahlen in diesem Skill sind auf „frische Eingabe = 1" normiert (Anthropic-Listenpreise,
Opus-Verhältnis). Auf einem Abo zahlt niemand diese Summe in Dollar — sie misst, **was das
Kontingent belastet**, und das ist auf Pro/Max die Währung, die knapp wird.

| Posten | Faktor | Was das praktisch heißt |
|---|---:|---|
| Cache **lesen** | **×0,1** | Der warme Verlauf wird bei jeder Anfrage zum Zehntelpreis mitgelesen |
| Cache **schreiben** (1-h-TTL) | **×2** | Neuer Text kommt einmal zum doppelten Preis in den Cache; ein Neuaufbau schreibt ALLES neu |
| Eigene **Ausgabe** | **×5** | Jedes Wort, das Claude tippt, kostet fünffach — Erklärungen im Chat sind der teuerste Posten, den Claude allein zu verantworten hat |
| Frische Eingabe | ×1 | Die Bezugsgröße |

### Warum die Anzahl der Anfragen alles dominiert

Eine Anfrage bei 220k Kontext kostet **220k × 0,1 = 22.000 Äquivalente** — nur fürs Lesen,
bevor irgendetwas passiert. Bei 30k Kontext (ein frischer Subagent) sind es **3.000**.

```
Alles im Hauptkontext:   147 Schritte × 151k × 0,1              = 2.217k
Delegiert:                14 Hauptanfragen × 345k × 0,1  =  483k
                         147 Agentenschritte ×  30k × 0,1 =  441k
                                                    Summe =  924k
```

**2,4× billiger für exakt dieselbe Arbeit** — nur weil jeder Schritt gegen den kleinen
Kontext des Agenten rechnet statt gegen den fetten der Sitzung. Rechnet man die anderen
Techniken dazu (Fertigmeldungen deckeln, nicht erzählen, was man gerade tut, Erklärungen
ins Handoff statt in den Chat), lag der gemessene Abschnitt statt bei 4.380k bei
**1.350–2.050k — rund 55–70 % Ersparnis**.

### Timing, nicht Kürze: wann eine Nachricht fast nichts kostet

Die Frage, die jeder stellt: „Kostet meine Zwischenfrage jetzt auch?" Die Antwort hängt
nicht von der Länge ab, sondern **vom Zeitpunkt**:

| Lage | Was mit der Nachricht passiert | Kosten |
|---|---|---|
| Claudes eigener Werkzeug-Ablauf läuft (Datei lesen, Befehl, Agent starten) | wird an die nächste ohnehin fällige Anfrage angehängt | **fast null** (~140 Äquivalente für 50 Wörter) |
| Subagenten rechnen, Claude selbst wartet | löst eine neue Anfrage aus | **volle 10 %** des Kontexts (22k bei 220k) |
| Ruhezustand nach der Antwort | löst eine neue Anfrage aus | **volle 10 %** |

Der Haken: Die Frage ist billig, **die Antwort nicht** — 300 Wörter Antwort sind ~2.000
Äquivalente (×5). Deshalb hält der Skill Antworten auf Zwischenfragen kurz und schiebt
Details ins Handoff, wo sie einfach statt fünffach kosten.

### Was ein Neuaufbau kostet — und woran man ihn erkennt

Eine Sitzung mit 287k Kontext, Start war 82k: Ein Modell- oder Effort-Wechsel mitten drin
schreibt ~287k × 2 neu, **~574k Äquivalente** — für nichts. Deshalb warnt der Skill vor
`/model`, `/effort`, CLAUDE.md-Änderungen und MCP-Neustarts, und er meldet einen Neuaufbau
nur, wenn er die Ursache benennen kann (>1 h Pause, Wechsel, Prefix-Änderung) — sonst
schweigt er, statt zu raten.

Wichtiges Missverständnis, das der Skill aktiv ausräumt: **„147 Anfragen ≠ 147
Neuaufbauten."** Innerhalb des Fensters laufen alle 147 gegen den warmen Cache. Die
gemessene Cache-Trefferquote in den Sitzungen lag bei 1,6–3,3 % geschrieben — durchgehend
warm.

## 3. Der Wellen-Workflow

Die Arithmetik belohnt einen bestimmten Rhythmus. Der Skill nennt ihn **Wellen**:

```
┌──────────────────────────────────────────────────────────────────────┐
│  1. Nutzer schickt EINE gebündelte Nachricht (oder ein beantwortetes │
│     Handoff): alles für die nächste Arbeitsstrecke                   │
│                                                                      │
│  2. Claude arbeitet die Welle ab — Subagenten für alles mit mehr     │
│     als einer Handvoll Schritten; Zwischenfragen sind erlaubt        │
│     und billig, solange Claude selbst gerade rattert                 │
│                                                                      │
│  3. Am Ende schreibt Claude ein HANDOFF-DOKUMENT statt im Chat       │
│     auszulaufen: Geliefertes, offene Punkte, Fahrplan, Kostentabelle,│
│     Kontingent-Stand, Fragen — und die Testliste mit Antwortzeilen   │
│                                                                      │
│  4. Nutzer öffnet das Handoff im Texteditor, beantwortet die Tests,  │
│     sammelt neue Ideen im Sammelbereich — in seinem Tempo, auch      │
│     über eine lange Pause hinweg. Kostet exakt null Anfragen.        │
│                                                                      │
│  5. Nächste Session startet NUR mit dem Handoff: kleiner Kontext,    │
│     Cache einmal minimal aufgebaut, voll gebrieft                    │
└──────────────────────────────────────────────────────────────────────┘
```

### Warum ein Editor und nicht das Chatfenster

Das Terminal klappt lange Eingaben zu `[pasted text]` zusammen — man verliert den
Überblick. Im Editor (TextEdit, VS Code, egal) sieht man das ganze Dokument, kann zwischen
Testpunkten springen, Notizen ergänzen, das Dokument zwei Tage liegen lassen. Und es
kostet **keine Anfrage**, solange man sammelt. Regel: **⌘S, bevor man Claude bittet, die
Datei zu lesen** — ungespeicherte Änderungen sind auf der Platte unsichtbar.

### Wie ein Handoff aussieht

```markdown
> **Für die nächste Session — diese Zeile kopieren und einfügen:**
> `Ich habe das Handoff beantwortet: /Users/…/projekt/_handoff-projekt-2026-08-27-b.md`

# Handoff Projekt — 27.08.2026, 18:21

## Kontingent
Claude Code: 5-h-Fenster 34 % · Woche 61 % (reset Mo 09:00) · Codex: 10 %/7d (Messung 2 h alt)

## Geliefert in dieser Welle
- …

## Erwartete Agenten-Ergebnisse
- [ ] docs/reviews/2026-08-27-tageszeit-und-kontingente.md (Recherche-Agent, 17:02)

## Offene Punkte / Fahrplan
- Welle 19: …

## Fragen an dich
1. Soll der Papierkorb-Weg auch für Ordner gelten?
>>>Antwort:

## Testliste v70
## T1 — Tagfilter ohne Beachball
Filter auf „Rechnung" setzen, 2.000 Einträge, darf nicht hängen.
>>>Antwort:

## T2 — Hyperlink-Editor
…
>>>Antwort:

# Die Kostentabelle dieser Sitzung
| # | Zeit | Worum es ging | Anfr. | Kontext | gelesen | geschr. | Ausgabe | Äquiv. |
…

## Sammlung für das nächste Handoff
>>>
```

Die Einzelheiten — Pfad ganz oben zum Kopieren, Projektname im Dateinamen, vorbereitete
Antwortzeilen, was ins Handoff gehört und was nicht (Regeln übernommen von Matt Pococks
`/handoff`) — stehen in `SKILL.md`, Abschnitt „The wave workflow".

### Der Nutzer ist der Engpass

Die neueste Regel im Skill (28.08.2026): Der Mensch kann nicht dauernd am Terminal sitzen.
Jede Rückfrage, die eine Welle anhält, kostet Stunden Echtzeit. Deshalb werden Wellen so
geschnitten, dass sie **ohne Rückfrage durchlaufen**: Vertretbare Annahmen werden getroffen
und im Handoff markiert, Fragen **gesammelt** ins Handoff geschrieben statt einzeln in den
Chat, Agenten bekommen **mehrere Aufgaben gebündelt** und melden sich erst, wenn alles
fertig ist. Agenten, die länger als eine Stunde brauchen, schreiben ihr Ergebnis in eine
Datei (`docs/reviews/<datum>-<thema>.md`); das Handoff nennt die erwartete Datei, und die
**nächste** Session prüft beim Lesen des Handoffs, ob sie da ist — das Fertigwerden kostet
so keine eigene Anfrage und keinen Neuaufbau nach der Nachtpause.

## 4. Subagenten-Ökonomie

Subagenten sind im Skill **der Standardweg, nicht die Ausnahme** — alles mit mehr als einer
Handvoll Schritten geht in einen Agenten. Die Gründe, in Zahlen:

| | Hauptkontext (220k) | Subagent (~30k) |
|---|---:|---:|
| Kosten je Arbeitsschritt (×0,1) | 22.000 | 3.000 |
| Cache-TTL | 1 h gleitend | 5 min (immer, auch auf Max) |
| Startkosten | — | 1–3 Anfragen + Auftragstext |
| Bericht zurück in den Hauptkontext | — | wird zum ×2-Cache-Schreiben — **deckeln!** |

Drei Dinge, die man dabei wissen muss:

1. **Subagenten-Tokens sind nicht gratis.** Sie belasten dasselbe Wochenkontingent. Was sie
   NICHT belasten, ist der Hauptkontext — der bleibt klein, schnell und antwortfähig.
2. **Die Ersparnis lässt sich reinvestieren.** Ein Agent arbeitet gründlicher, als man es
   nebenbei täte: aus 147 Schritten werden 600. Dann ist die Rechnung wieder ausgeglichen —
   aber es ist **viermal so viel erledigt**. Das ist „Token-Maximierung": mehr Arbeit fürs
   gleiche Kontingent, nicht weniger Ausgabe.
3. **Der Bericht ist die versteckte Kostenstelle.** Jeder Agentenbericht wird in den
   Hauptkontext geschrieben (×2) und danach bei jeder Anfrage mitgelesen (×0,1). Deshalb
   bekommt jeder Agent eine Berichtsgrenze („≤ 250 Wörter, keine Diffs") und lange
   Ergebnisse gehen in Dateien.

Modellwahl (aus der Tabelle im Skill): Dateien finden, Umbenennen, Log-Sichtung, Tests nach
Muster → **schnell/billig, Effort low** (bei Fable 5 als Agent: immer low). Design-
entscheidungen, Sicherheits-Review → starkes Modell, hoher Effort, oder ein anderes Modell
(Codex/GPT) als Zweitmeinung. Modell und Effort stehen sichtbar in der Agentenbeschreibung
(`"Fable/low · Testdateien umbenennen"`), damit der Nutzer im Terminal sieht, wer arbeitet.

Parallel vs. sequenziell: **parallel für Tempo, sequenziell für Wärme** — Agenten cachen
separat mit 5 Minuten; wer fünf Agenten gleichzeitig startet, hat fünf kalte Caches.

## 5. Was der Skill sichtbar macht

### Der Zeitstempel

Unter jeder Antwort steht Datum und Uhrzeit — frisch aus `date`, nie aus einer früheren
Antwort hochgerechnet. So sieht der Nutzer selbst, wie lange die letzte Anfrage her ist
und ob das Fenster noch offen ist.

### Die Kostenzeile

Unter substanziellen Antworten (`ctx.sh`, ans ohnehin laufende `date` angehängt, damit die
Messung selbst keine Anfrage kostet):

```
Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5) ≈ 52k ·
Sitzung bisher: 265 Anfragen, 9.520k
```

Und ein Hinweis, wenn etwas teuer war: „Das waren 12 Anfragen, weil ich drei Agenten
gestartet und ihre Berichte gelesen habe — 4.600k."

### Die Kostentabelle je Sitzung

Am Ende jeder Welle im Handoff (`session-costs.sh --markdown`). Die Zeile ist bewusst der
**Abschnitt zwischen zwei Nutzernachrichten** — die Einheit, die ein Mensch erlebt („ich
habe was gesagt, dann ist etwas passiert"), nicht die einzelne Modellanfrage.

| # | Zeit | Worum es ging | Anfr. | Kontext | gelesen | geschr. | Ausgabe | Äquiv. |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 17:00 | Handoff gelesen, neun Agenten gestartet | 36 | 148k | 4130k | 282k | 110k | 1529k |
| 2 | 17:35 | *(gebündelt)* | 0 | — | 0 | 0 | 0 | **0** |
| 3 | 17:35 | Deine Kostenfragen | 6 | 156k | 906k | 11k | 19k | 208k |
| 4 | 17:38 | `/context all` ausgewertet | 10 | 180k | 1706k | 43k | 8k | 298k |
| 5 | 17:48 | Timing und Bündeln erklärt | 5 | 188k | 907k | 11k | 9k | 159k |
| 6 | 18:15 | *(gebündelt — sechs Fragen)* | 0 | — | 0 | 0 | 0 | **0** |
| 7 | 18:21 | Restarbeit, Bauen, Handoff | 20 | 220k | 4080k | 59k | 41k | 729k |
| **Σ** | | **7 Abschnitte** | **82** | **220k** | **12671k** | **416k** | **200k** | **3102k** |

Wie man sie liest:

- **Äquiv.** = gelesen × 0,1 + geschrieben × 2 + Ausgabe × 5 — alle drei Posten auf einen
  Preis gebracht und addiert. Zeile 1: 4130 × 0,1 + 282 × 2 + 110 × 5 = 413 + 564 + 550 ≈ 1529k.
- **Kontext addiert sich NICHT.** „180k" in Zeile 4 heißt: So dick war das Gespräch am Ende
  dieses Abschnitts — nicht, dass der Abschnitt 180k gekostet hätte.
- **Zwei Zeilen stehen bei null.** Das ist kein Rundungsfehler: Die Nachrichten kamen an,
  während Claude arbeitete, und wurden in die laufende Runde gebündelt.
- **Ausgabe 200k × 5 = 1.000k — ein Drittel der Gesamtkosten.** Der einzige Posten, den
  Claude allein zu verantworten hat. Lehre: weniger reden, mehr ins Dokument schreiben.
- **82 Anfragen im Hauptkontext für neun Arbeitspakete** — die über 500 Arbeitsschritte
  liefen in den Agenten. Im Hauptkontext hätten sie ~7.500k statt 3.102k gekostet.

### Der Kontingent-Block

Ganz oben im Handoff steht, was vom bezahlten Kontingent noch da ist — Claude Codes
eigenes 5-Stunden- und Wochenfenster (aus der Statuszeile in eine Datei geparkt, weil
Claude seine Prozentzahlen sonst nicht sehen kann) und Codex/GPT (`codex-limit.sh`,
aus dem `rate_limits`-Block der letzten Codex-Session, mit Alter der Messung). Der Sinn:
Wer monatlich bezahlt, sollte das Kontingent **ausnutzen** — der Skill schlägt vor, was
man mit dem Rest noch machen könnte („Woche zu 61 %, Reset Montag: reicht für die
Codex-Zweitmeinung zu Welle 19"). Mehr dazu in `SKILL.md`, „Was noch im Tank ist".

Nebenbefund aus einem Review vom 27.08.2026 (`docs/reviews` im Aitomat-Projekt): Die
frühere „Peak-Hours"-Kürzung des Kontingents bei Claude Code Pro/Max wurde am 06.05.2026
abgeschafft; Tageszeit spielt für Preis und Kontingent heute keine Rolle mehr — nur für
529-Überlastfehler. Und die Skill-Liste selbst ist auf ~2.000 Token gedeckelt; ein
405k-Sitzungsstart kommt nicht von 89 installierten Skills, sondern aus etwas anderem
(`/context all` verrät, woraus).

## 6. Installation

```bash
mkdir -p ~/.claude/skills/warm-handoff
curl -fsSL https://raw.githubusercontent.com/Aitomat/warm-handoff/main/SKILL.md \
  -o ~/.claude/skills/warm-handoff/SKILL.md

for f in ctx.sh codex-limit.sh session-costs.sh; do
  curl -fsSL "https://raw.githubusercontent.com/Aitomat/warm-handoff/main/scripts/$f" \
    -o ~/.claude/"$f"
  chmod +x ~/.claude/"$f"
done
```

Oder das Repo klonen: `SKILL.md` nach `~/.claude/skills/warm-handoff/SKILL.md`, alles aus
`scripts/` nach `~/.claude/`, Dateinamen beibehalten.

**Damit der Skill in jeder Session ohne Zutun anspringt**, eine Zeile in die globale
`~/.claude/CLAUDE.md`:

```
Zu Beginn jeder Session den Skill `warm-handoff` aufrufen. Uhrzeit in jede Antwort schreiben.
```

Manuell: `/warm-handoff` oder einfach „Cache", „Handoff", „Welle fertig", „frische
Session" sagen.

Voraussetzungen: macOS oder Linux, `bash`, `python3` (für die Kostenskripte), `jq`
optional. Die Skripte lesen nur die lokalen Session-Dateien unter `~/.claude/projects/`
und `~/.codex/sessions/` — nichts geht nach außen.

## 7. Die Skripte

| Skript | Was es tut | Aufruf |
|---|---|---|
| `scripts/ctx.sh` | Was seit der letzten Nutzernachricht verbraucht wurde und **wofür**: Anzahl Anfragen, was darin passiert ist (Agentenberichte, Dateizugriffe, Befehle, eigene Antworten), Verteilung auf Lesen/Schreiben/Ausgabe. Liefert die Kostenzeile. | `date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh` — immer an einen ohnehin laufenden Befehl anhängen, damit die Messung nichts kostet |
| `scripts/session-costs.sh` | Die Kostentabelle je Sitzung, Welle für Welle, aus der `.jsonl` der Session. Nennt teuersten Abschnitt und Cache-Trefferquote. | `session-costs.sh` (aktuelles Projekt, neueste Sitzung) · `session-costs.sh <sitzung.jsonl>` · `session-costs.sh --markdown` (fertig fürs Handoff) |
| `scripts/codex-limit.sh` | Wie viel vom Codex/GPT-Kontingent verbraucht ist. Die Codex-CLI hat keinen Usage-Befehl; das Skript liest den `rate_limits`-Block aus der letzten Session-Datei und druckt das Alter der Messung dazu. | `codex-limit.sh` · `--kurz` (Statuszeile: `codex 10%/7d`) · `--json` |

Dazu im Skill beschrieben: ein kleines Statuszeilen-Skript, das die Claude-Code-Prozente
aus dem stdin-JSON in eine Datei parkt, damit der Skill sie im Handoff zitieren kann, und
ein „Aufwach-Ping" für die Codex-Anzeige (ein Mini-Aufruf, damit die Messung frisch ist).

## 8. Ehrliche Grenzen

- Die Messungen stammen aus echten Sitzungen eines Entwicklers auf einem Abo mit
  1-Stunden-Cache, in einem Projekt (Swift/macOS). Andere Projekte, andere Verhältnisse —
  deshalb liegen die Skripte bei, nicht nur die Ergebnisse.
- Die Ersparnis je Technik ist eine Schätzung, die ein zweites Modell (Codex/GPT) über
  dieselben Sitzungsdaten gerechnet hat. Die Posten überlappen und dürfen nicht addiert
  werden.
- Die „Äquivalente" sind Listenpreis-Verhältnisse. Auf Pro/Max zahlt niemand diese Summe;
  sie misst die Belastung des Kontingents, und die Umrechnung des Kontingents in Tokens ist
  von Anthropic nicht dokumentiert.
- Ein Neuaufbau wird nur gemeldet, wenn eine Ursache herleitbar ist. Ohne Ursache sagt der
  Skill lieber nichts.
- Der Skill schult ausdrücklich: „Erst die Zahl, dann die Regel." Wenn eine frühere
  Erklärung im Skill falsch war (das kam vor — „fast die Hälfte gespart" waren nachgerechnet
  ein Drittel), wird sie korrigiert und die Korrektur bleibt lesbar.

## 9. Die Fakten, auf denen alles steht

| Regel | Wert |
|---|---|
| Pro/Max Cache-TTL | 1 Stunde, **gleitend** — jede Anfrage setzt sie zurück |
| Über Plan-Limit (bezahlte Credits) | fällt automatisch auf 5 Minuten |
| Subagenten | immer 5 Minuten, auch auf Max |
| Cache lesen / schreiben / eigene Ausgabe | ×0,1 / ×2 (1-h-TTL) / ×5 |
| Umgebungsvariablen | `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1` |
| Skill-Liste im Kontext | gedeckelt (`skillListingBudgetFraction`, ~2.000 Token) |

Quellen: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching),
[Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices),
[Extend Claude with skills](https://docs.claude.com/en/docs/claude-code/skills). Stand 27.08.2026.

## 10. Danksagung, Vorarbeiten, Lizenz

- [Matt Pococks /handoff-Skill](https://www.aihero.dev/skills-handoff)
  ([mattpocock/skills](https://github.com/mattpocock/skills)) — das klarste Denken darüber,
  *wie* man ein Handoff schreibt. Übernommen: auf abgeschlossene Dokumente verweisen statt
  sie zu kopieren, Geheimnisse schwärzen, Skills für den nächsten Agenten vorschlagen.
  Bewusst anders: Unsere Handoffs leben *im Projekt* als datierte, vom Nutzer annotierte
  Arbeitsdokumente, und jenseits der Kontextschwelle ziehen wir Handoff + frische Session
  dem `/compact` vor.
- Weitere Handoff-Implementierungen: [392fyc](https://github.com/392fyc/claude-handoff),
  [REMvisual](https://github.com/REMvisual/claude-handoff),
  [willseltzer](https://github.com/willseltzer/claude-handoff),
  [ykdojo](https://github.com/ykdojo/claude-code-tips/blob/main/skills/handoff/SKILL.md).
- Zweitmeinungen zu den Rechnungen: Codex/GPT-5.6 und Ox Alpha (OpenRouter).

Issues, Messungen aus eigenen Sitzungen und Pull Requests sind willkommen — auf Deutsch
oder Englisch.

Lizenz: MIT.
