# warm-handoff — Historie (vollständige Fassung bis 29.08.2026, mit allen datierten Nutzer-Zitaten)
> Nachschlagewerk zum Kern-Skill in ../SKILL.md. Nicht standardmäßig laden.

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

Claude Code caches your conversation prefix. Working *inside* that cache is fast and cheap;
rebuilding it is slow and expensive. This skill makes the cache window visible, keeps you
inside it, and — when leaving it is the better deal — writes the handoff that lets a fresh
session continue seamlessly.
> Primary language: English. Dated German passages record the sessions each rule came from — sie bleiben bewusst erhalten. Deutsche README: README.de.md im Repo.


## Table of contents by topic (Thematischer Wegweiser)

This file grew session by session — dated headings mark when a rule was added and why.
To find things by TOPIC rather than by date, use this map:

| Topic | Sections |
|---|---|
| Facts & mechanics | The facts · What a cache rebuild looks like · When does the hour actually start · Einen Cache-Neuaufbau ERKENNEN |
| What Claude does each turn | What Claude does when this skill is active · The window as a friendly coach · Honesty rules |
| Measuring instead of guessing | Die Schritte ZÄHLEN · Die Startkosten MITRECHNEN · Den Sweetspot AUSRECHNEN · Was wird eigentlich GESCHRIEBEN |
| Fewer requests (the real lever) | Der eigentliche Hebel · Die Technik-Liste · Wie wenige Anfragen sind realistisch · Nachrichten WÄHREND der Arbeit · Die Ausgabe ist teuer |
| Subagents | Pacing · Choosing WHICH subagent · Sequential vs. parallel · Make the work visible · Die ehrlichste Zahl · Subagenten sind der Standardweg · Lange Agentenläufe / Nutzer als Engpass / Fable low |
| Cost visibility | Die Kostenzeile · Die Kostentabelle · Wie man diese Tabelle liest · Dieser Skill soll SCHULEN |
| Paid quota | Bezahltes Kontingent sichtbar machen · Was noch im Tank ist · Aufwach-Ping · Codex, Gemini und OpenRouter · Codex nach Kontogröße (29.08.) |
| Sammlung & Ende-Feld | Vier Regeln vom 29.08.: Sammlung wörtlich kopieren · Ende-Feld als Banner · Agenten-Anzeige |
| The handoff document | The wave workflow · Writing the handoff well · When to stay vs. hand off · The economics, honestly · Diktieren ins Terminal |
| Setup | The logbook · Make it always-on |

## The facts (verified against Claude Code docs, 2026-08)

- **Pro/Max subscription: 1-hour cache TTL, sliding.** Every message and every cache hit
  resets the 1-hour timer. Stay under one hour between exchanges and the cache lives forever.
- **Fallback:** if you exceed plan limits and draw on paid usage credits, Claude Code drops
  to a 5-minute TTL automatically.
- **Subagents always use a strict 5-minute TTL**, even on Max.
- Env overrides: `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1`.
- **What kills the cache instantly, regardless of the clock:** switching model or reasoning
  effort mid-session, editing the system prompt / CLAUDE.md mid-session, an MCP server that
  crashes and restarts (stdio servers with "Connection Failed" are prime suspects), and
  anything else that changes the cached prefix. Set model and effort at the START, never
  mid-session — before the first message it costs nothing.

## What Claude does when this skill is active

1. **Timestamp every reply** (e.g. `(22.08.2026, 12:50)`) — and **only from a `date` call
   made in THAT SAME reply. Hard rule: no `date` run in this turn → write NO timestamp at
   all.** An LLM has no sense of elapsed time; the classic failure is extrapolating from a
   `date` read a few turns earlier ("it was 16:28, two agents finished, so ~16:47") — that
   produced stamps 15+ minutes wrong in practice. Extrapolated ≠ read. Piggyback the read
   onto any tool call the reply makes anyway (`… && date "+%H:%M"`), or run `date` alone;
   a missing stamp is honest, a guessed one actively misleads the user who relies on it
   to judge the cache window. This is the cheapest cache monitor that exists.
   **Always stamp DATE + time together** (`date "+%d.%m.%Y %H:%M"`), even when the day
   obviously hasn't changed — handoffs and logs get read days later, and a bare "16:47"
   is ambiguous by then. The read costs nothing: append it to any command the reply
   already runs.
   **The #1 trap: replies to background-agent notifications.** When a subagent
   finishes and Claude writes a short status update, that reply usually makes NO
   tool call — so there is nothing to piggyback on, and the temptation is to
   extrapolate ("last read 18:34, three agents done, so ~19:40"). A tilde does
   NOT make a guess honest — `~19:40` is still a fabricated stamp (real time was
   20:02 in practice, 24.08.2026). Rule: agent-status replies either run `date`
   as their one tool call, or carry NO time at all. Never `~`-stamps.
2. **State the window when asked** ("am I still cached?"): last exchange + 60 minutes,
   sliding. Answering the question itself resets the timer.
3. **Warn before cache-destroying actions** — a mid-session `/model` or `/effort` change, a
   flaky MCP server in the config — *before* the user pays for it.
4. **Measure the context size at every wave end — don't wait to be asked.** The skill has
   no background process; the threshold rule only works if Claude actually checks. So:
   at every handoff/wave end (and whenever finishing a large batch of subagent work,
   which grows context fast), read the current context size from the status line or a
   monitor and state it in the reply. A threshold that nobody measures is decoration —
   this exact failure happened once: the user crossed 400k unnoticed while Claude was
   busy orchestrating, and had to point it out himself.

   **NEVER guess the context number — same rule as the clock (Yasin 25.08.2026).**
   Claude cannot feel how full its context is. A sentence like "Cache frisch (~20k)"
   written without looking is a fabrication, and it is worse than saying nothing:
   the user reads it as a measurement and plans the wave around it. The real number
   at that moment was ~80k. Only two sources count:
   - the **status line** the user's terminal renders (`ctx 15% used (85% left) | ctx 148k`)
     — if the user pastes or screenshots it, use exactly that number;
   - a monitor/tool call made in THIS turn that reports it.

   **Dritte Quelle — und sie ist die beste: SELBST MESSEN (Yasin 25.08.2026).** Sein
   Einwand: „Dass du bei dieser Session die Gesamtkontextgröße nicht siehst, das ist doch
   komisch, das muss doch irgendwie gehen." Er hatte recht. Claude Code schreibt jede
   Anfrage samt `usage`-Block in die Session-Datei unter
   `~/.claude/projects/<pfad-mit-bindestrichen>/<session-id>.jsonl`. Die letzte Zeile mit
   `usage` trägt `cache_read_input_tokens + cache_creation_input_tokens` — das IST die
   aktuelle Kontextgröße. Ein Bash-Aufruf genügt:

   ```bash
   proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"
   sess=$(ls -t "$proj"/*.jsonl | head -1)
   SESS="$sess" python3 -c '
   import json, os
   zeilen = open(os.environ["SESS"], "rb").read().decode("utf-8","ignore").splitlines()
   ein=aus=cw=cr=0
   for z in zeilen:
       try: u=(json.loads(z).get("message") or {}).get("usage")
       except Exception: continue
       if not u: continue
       ein+=u.get("input_tokens",0); aus+=u.get("output_tokens",0)
       cw+=u.get("cache_creation_input_tokens",0); cr+=u.get("cache_read_input_tokens",0)
   for z in reversed(zeilen):
       try: u=(json.loads(z).get("message") or {}).get("usage")
       except Exception: continue
       if u:
           print(f"Kontext: {(u.get(\"cache_read_input_tokens\",0)+u.get(\"cache_creation_input_tokens\",0))/1000:.0f}k"); break
   print(f"API-Gegenwert: ${(ein*15+aus*75+cw*18.75+cr*1.5)/1_000_000:.2f}")'
   ```

   Damit ist die Sweetspot-Ansage (s. unten) jederzeit belastbar — auch ohne dass der
   Nutzer seine Statuszeile abtippt. Am Wellenende gehört diese Messung dazu.

   Zwei ehrliche Einschränkungen: Die Datei wird pro Anfrage fortgeschrieben, die Zahl ist
   also der Stand der LETZTEN Anfrage, nicht der Sekunde. Und der Dollarbetrag ist der
   API-GEGENWERT zu Listenpreisen — auf einem Pro-/Max-Abo zahlt niemand diese Summe; sie
   misst, was das Kontingent belastet.

   Keine dieser drei Quellen verfügbar → „Kontext: nicht gemessen" (oder weglassen). Für
   die Schlusszeile des Handoffs gilt dasselbe: ein erfundenes „~60k" dort ist derselbe
   Fehler, nur archiviert.

   **What the status-line fields mean** (users ask, and the numbers look contradictory):
   - `ctx N% used` / `ctx 148k` — how full THIS conversation's context window is.
     Nothing to do with billing or quota; it resets to zero in a fresh session.
   - `5h:3%` — the rolling 5-hour usage window. Matches "Aktuelle Sitzung" in the
     web UI under Einstellungen ▸ Nutzung.
   - `7d:0%` — the weekly window as Claude Code sees it. This can differ sharply from
     the web UI's "Alle Modelle 59%", because the web number aggregates EVERYTHING
     (chats, other models, Fable) while the terminal field tracks the Claude-Code
     slice — and it updates in steps, not live. When they disagree, the web UI is
     the authority; say so instead of explaining the gap away.
   - The web UI also lists per-model bars (e.g. "Fable 90%") with their own reset
     time. A red bar there is the real constraint even when the terminal shows 0%.
5. **Recommend a fresh session at the sweetspot.** The threshold is not one number —
   it depends on what the NEXT stretch of work looks like (Yasin asked exactly this on
   25.08.2026, and his instinct was right):

   | What comes next | Hand off at |
   |---|---|
   | A big build/review wave (hundreds of tool-steps) | **~200k** |
   | Mixed: some building, mostly discussion | ~250k |
   | Only conversation, answers, small edits | **~300k** |
   | Anything | **400k = hard ceiling**, never ride past it |

   The reason the number moves: cost scales with *tool-steps × context*, and the user's
   own messages are a rounding error. 300 work-steps on a 300k context is ~9M token
   equivalents; the same wave from a fresh 30k session is ~0.9M. Ten quiet exchanges on
   300k cost ~0.3M — nothing. So a fat context is cheap to TALK on and expensive to
   WORK on. Below ~150k, none of this matters; chat freely. Rationale: every further work-step
   re-reads the whole prefix at 1/10, so a big wave on a fat context costs multiples of
   the same wave in a fresh ~30k session, and past ~500–600k answer quality degrades from
   sheer information load even while the cache is warm. Under ~150k, staying is fine.
5. **Write the handoff automatically after every big work wave** — do not wait to be asked.

## What a cache rebuild looks like (and doesn't)

- **You cannot see a rebuild in the context counter.** Context size is the same before and
  after — it's the same content, just frozen again. The counter measures size, not cost.
- **Where you DO see it: your 5-hour and weekly usage quota.** A rebuild re-writes the whole
  prefix at cache-write rates, so the quota drops noticeably faster. A lost cache doesn't
  make your context bigger — it makes it more expensive.
- **A short message costs ~1/10 of the WHOLE context — cheap when small, real when fat.**
  At 30k context, chat freely (near-free, and it resets the 1-hour timer). At 200k+, each
  exchange is ~20k full-price equivalents and ten quick back-and-forths equal one full
  context read: batch conversation too — ideally ONE long structured message per wave,
  handoff to handoff, answers collected under the test items; short questions only when
  they can't wait.

## When does the hour actually start? (users always ask this)

The 1-hour timer resets on **every request in the session** — not just the user's
messages. That includes each of Claude's own tool-steps, and each status message Claude
emits when a background subagent finishes. Consequences worth telling the user:

- The hour counts from **Claude's last output**, whichever side produced the last
  activity. "Agent Y finished, here's the handoff" at 16:30 → the user has until ~17:30
  to answer warmly. Reading costs the user nothing; only their reply is a new request.
- While Claude waits on subagents, its own "agent X done" interim reports keep the cache
  warm automatically — no dedicated keep-alive needed during active waves.
- Work through subagents by default for heavy lifting: they run in their own small
  contexts (5-min TTL, cached separately), so the main context stays lean while the
  completion notifications double as free cache refreshes.
- **Und die andere Hälfte der Wahrheit: JEDE ANTWORT kostet ebenfalls.** Eine Anfrage ist
  eine Anfrage, egal wer sie auslöst — auch Claudes eigene Antwort liest den ganzen
  Kontext zu 10 % neu (bei 220k also ~22k Äquivalente) und bezahlt obendrauf ihre eigenen
  Ausgabe-Token zum **fünffachen** Preis. Eine 300-Wörter-Antwort sind ~2.000 Äquivalente
  extra. Die Uhr kostenlos warm zu halten geht deshalb nicht: Jeder Timer-Reset ist eine
  bezahlte Anfrage. Das ist kein Argument gegen das Antworten, sondern gegen das
  Ausschweifen — und der Grund, warum leere Zwischenmeldungen gestrichen wurden.

## Pacing: parallel for speed, sequential for warmth

Subagents are not just a context-saver — their SCHEDULING is a cache instrument. Two modes,
chosen by what the user needs right now (ask, or react to cues like "Zeitdruck" /
"ich gehe ins Bett"):

- **User is present and wants speed** → run subagents IN PARALLEL. Everything lands fast;
  the user answers between waves and the timer never gets close to expiring.
- **User steps away (lunch, evening, night)** → run subagents SEQUENTIALLY. Each completion
  wakes Claude, produces a report — a new request that resets the 1-hour timer. The user
  returns hours later to a still-warm cache and a finished handoff, having typed nothing.
  Claude's goal while the user is away: always produce SOME output within each hour, work
  chained through the queue, handoff at the end.
- Honest limit: sequential mode keeps the cache warm only while real work remains. For an
  8-hour absence, first build a work queue big enough to span it (backlog items, review
  rounds, doc sweeps) — plan it WITH the user before they leave. Never invent busywork
  just to touch the cache; if the queue runs dry, write the handoff and let the cache go.
- Model economics: the orchestrator holds the big cached context — subagents don't. Run
  subagents on a strong model with LOW reasoning effort for mechanical work and reserve
  high effort for hard review/design steps; set the session's model+effort once at start
  (mid-session switches kill the cache).

### Choosing WHICH subagent — cheap/fast vs. strong/slow (Yasin 25.08.2026)

Picking the tier is part of the plan, not an afterthought. State the choice out loud
in one clause ("drei Leser auf dem schnellen Modell, die Review auf dem starken"), so
the user can veto before the tokens are spent.

| Work | Tier | Why |
|---|---|---|
| Finding files, listing call sites, mechanical renames, log sifting | fast/cheap, low effort | Answer is verifiable at a glance; a strong model adds nothing |
| Writing tests to an existing pattern, doc sweeps, format fixes | fast/cheap, low effort | The pattern is already decided |
| Design decisions, security/correctness review, "why is this wrong" | strong, high effort | Errors here are expensive and hard to spot later |
| Anything the user will ship without re-reading | strong | Treat it as production |

Cross-checking your OWN output is a separate job — a second opinion from a different
model (Codex/GPT, a second reviewer) catches what a same-architecture re-read cannot.

### Sequential vs. parallel — decide it, then say it

- **"Ich hab's eilig"** → make a short plan first, then fan out in parallel. Say how many
  agents and what each one owns.
- **User is away / the steps depend on each other** → chain them one after another (also
  the cache-warm mode above).
- **Mixed** is normal: fan out the independent reads, then run the dependent build/review
  steps in sequence.

### Make the work visible in the user's terminal

The user watches a status line and a task list, not Claude's reasoning. So:

- **Keep a live to-do list** for any task with more than ~3 steps, and update it as
  steps finish — that list IS the progress bar. Never let it go stale; a finished step
  still marked "in Arbeit" is worse than no list.
- **Announce the whole fleet ONCE when it starts** — one block, what each agent owns.
  Danach Funkstille bis zum Ende.
- **Name the running total** at wave end: how many agents ran, what came back, what is
  still open.

**WIDERRUFEN am 26.08.2026, 16:48 — keine Einzelmeldung je Agent mehr.** Hier stand
früher „announce each subagent when it starts AND when it lands, those lines double as
cache-refreshing requests". Das war teuer und überflüssig. Yasins Einwand, wörtlich:
„Du musst mir kein Feedback geben, wenn einer gestoppt hat. Dann hat er gestoppt — bis
dann alle fertig sind oder bis fast eine Stunde rum ist, damit du den Cache warm hältst.
Unten in meinem cmux-Fenster sehe ich ja doch, wenn Unteragenten arbeiten."

Er hat in beiden Punkten recht:

1. **Der Host zeigt laufende Agenten ohnehin an.** Eine Zeile „Agent 3 ist fertig" ist
   Information, die der Nutzer schon vor Augen hat — bezahlt mit einer vollen Anfrage.
2. **Als Cache-Wärmer sind diese Meldungen unnötig,** weil die eigenen Tool-Schritte den
   Timer sowieso bei jedem Schritt zurücksetzen. Die Meldung wärmt nichts, was nicht
   schon warm wäre.

Die Regel lautet jetzt:

- **Während einer Welle wird NICHT je Agent gemeldet.** Landen fünf Agenten, entsteht
  EINE Zusammenfassung, wenn der letzte durch ist.
- **Gemeldet wird nur bei drei Anlässen:** eine Entscheidung, die der Nutzer treffen
  muss · eine Blockade, die ohne ihn nicht weitergeht · ein abgeschlossener Meilenstein.
- **Die Ausnahme ist der Uhrzeiger:** Ist der Nutzer anwesend und die Welle läuft schon
  fast eine Stunde ohne Lebenszeichen, kommt EINE gebündelte Zwischenmeldung — damit
  das Cache-Fenster nicht abläuft und er nicht im Dunkeln sitzt.
- **Bei einem einzelnen langen Agenten** (kein Bündel) gilt dasselbe: Ergebnis abwarten,
  nicht kommentieren, dass er gestartet ist.

Rechenbeispiel aus der gemessenen Session: fünf Einzelmeldungen bei ~220k Kontext sind
rund 110k Token-Äquivalente — für Text, den der Nutzer bereits sieht.

### Terminal- und Werkzeug-neutral halten

Some users run cmux, others plain Terminal/iTerm/Ghostty, VS Code, or Codex instead of
Claude Code. Everything in this skill must survive that:

- Never assume a specific terminal's UI. Say "deine Statuszeile", not "das cmux-Feld".
  If a feature only exists in one host (cmux panes/surfaces, a custom status line),
  mark it as such in one clause and give the generic fallback.
- The handoff document is the portable artifact: a plain Markdown file any agent in any
  tool can read. Never encode state in a terminal-specific place instead.
- When another agent (Codex/GPT, Gemini) does the work, the SAME rules apply — timestamp,
  measured context, handoff, archive. Hand it the handoff file, not a chat summary.

## Den Sweetspot AUSRECHNEN und ansagen (Yasin 25.08.2026)

Sein Wunsch im Wortlaut: „Könnten wir den Sweetspot berechnen und dann sagen: hey, jetzt
ist dein Sweetspot erreicht, deswegen habe ich ein Handoff gemacht, die Welle ist auch
gerade fertig, starte lieber eine neue Session — das wäre am elegantesten."

Das geht, und zwar ohne Magie. Zwei Zahlen genügen, beide ablesbar:

```
verbleibende Schritte im Fenster ≈ (Ziel-Kontext − aktueller Kontext) / Zuwachs pro Schritt
```

- **Aktueller Kontext**: aus der Statuszeile (`ctx 148k`) — nie geschätzt.
- **Zuwachs pro Schritt**: aus dieser Sitzung selbst. Zwei Messpunkte reichen: Kontext beim
  letzten Handoff, Kontext jetzt, geteilt durch die Anzahl Wellen/Schritte dazwischen. In
  der Praxis: eine Bau-Welle mit Tests kostet grob 40–80k, eine Gesprächsrunde 2–5k.
- **Ziel-Kontext**: 200k / 250k / 300k je nachdem, was als Nächstes ansteht (Tabelle oben).

Daraus wird eine Ansage, die der Nutzer wirklich brauchen kann — nicht „dein Kontext ist
groß", sondern **wie viel noch reinpasst**:

> „Kontext 148k, Ziel 200k vor der nächsten Bau-Welle — das reicht noch für etwa eine
> Welle oder ein Dutzend Fragen. Danach mache ich das Handoff."

**Wann diese Ansage kommt (ungefragt):**
- am Ende jeder Welle, zusammen mit der gemessenen Kontextzahl;
- sobald das Restbudget unter EINE weitere Welle fällt — dann klar: „Das hier war die
  letzte Welle in dieser Sitzung, das Handoff ist geschrieben, starte morgen frisch."
- wenn der Nutzer nach dem Stand fragt.

**Ton (sein ausdrücklicher Wunsch):** kurz, beiläufig, motivierend — nie mahnend.
„Noch Platz für ~2 Wellen" ist ein Streak-Zähler, keine Rechnung. Und wenn das Budget
knapp wird, ruhig auch der praktische Hinweis: „Ab hier lieber längere Nachrichten
sammeln statt vieler kurzer" — das ist derselbe Gedanke, nur aus seiner Perspektive.

Ehrliche Grenze: Der Zuwachs pro Schritt schwankt stark (ein Screenshot kostet mehr als
eine Textantwort). Die Schätzung ist eine Größenordnung, kein Versprechen — so soll sie
auch formuliert sein („etwa", „grob"), und die gemessene Kontextzahl steht immer daneben.

### Die Startkosten einer frischen Session MITRECHNEN (Yasin 25.08.2026)

Sein Einwand, wörtlich: „Du beachtest nicht, dass bei einer neuen Session ja ich mit
70.000 Tokens starte und das mal zwei gerechnet wird, weil der Cache neu aufgebaut wird.
Deswegen ist in unserem Skill eine Rechnung noch nicht perfekt."

Er hat recht, und der Beleg stand in derselben Sitzung: die MESSUNG direkt nach dem
Sessionstart, vor der ersten Zeile Arbeit, ergab **82k** — nicht die „~20k", mit denen
dieser Skill an mehreren Stellen rechnet. Skills, Werkzeug-Schemata, Systemvorgaben und
Projektregeln sind schon da, bevor der Nutzer irgendetwas tut. Die 20k-Zahl war zu
optimistisch und muss projektspezifisch GEMESSEN statt geraten werden.

Die vollständige Rechnung hat drei Posten statt zwei. **Der Cache-Write-Faktor hängt an
der TTL, und das ist eine klassische Verwechslung:** 1,25× gilt für die 5-MINUTEN-
Speicherung, **2× für die 1-STUNDEN-Speicherung** — und die ist auf Pro/Max der Normalfall
(s. „The facts" ganz oben). Wer 1,25 einsetzt, rechnet den Neuaufbau um 60 % zu billig.
Yasin hat genau diesen Fehler am 25.08.2026 gefunden („das müsste doch mal zwei sein,
dachte ich") — er hatte recht. Cache-Read bleibt 0,1×.

```
Neuaufbau EINMALIG       = Startkontext × 2      (1-h-TTL; nur bei 5-min-TTL × 1,25)
Schritt in neuer Session = Startkontext × 0,1
Schritt in alter Session = aktueller Kontext × 0,1
Break-even (Schritte)    = (Startkontext × 2) / ((alt − neu) × 0,1)
```

Beispiel aus der Sitzung: Start 82k, aktuell 287k →
Neuaufbau ~164k, Ersparnis 20,5k je Schritt → **Break-even bei ~8 Schritten.**

**Der Satz, der dabei am häufigsten falsch verstanden wird:** „Schritte" sind NICHT die
Nachrichten des Nutzers, sondern ganz überwiegend die eigenen Tool-Aufrufe. Daraus folgt
die Regel, die tatsächlich trägt:

- **Nur noch reden / Testliste durchgehen / ein paar kleine Korrekturen** (< ~6 Schritte)
  → BLEIBEN, auch bei 260k+. Der Neuaufbau wäre teurer als das, was er spart.
- **Eine Bau-Welle, ein Review, eine Migration** (Hunderte Schritte) → WECHSELN, sobald
  der Kontext deutlich über dem Startkontext liegt. Der Break-even fällt schon nach dem
  sechsten Schritt, alles danach ist reiner Gewinn.

Deshalb gehört in die Sweetspot-Ansage IMMER der gemessene Startkontext dieser Session
und die Frage „was kommt als Nächstes?" — ohne beides ist die Empfehlung geraten.

### Die Schritte ZÄHLEN, nicht schätzen (Yasins Auftrag, 25.08.2026)

Sein Satz: „Da müssen wir dann schauen, wie viele Schritte das wirklich sind — das muss
der Skill schon berechnen, wissen und auch dem User anzeigen."

Geht, und zwar exakt: Jede Anfrage ans Modell steht als Zeile mit `usage` in der
Session-Datei. Startkontext, aktueller Kontext, Anzahl Anfragen und der Anteil, den der
Nutzer selbst ausgelöst hat, sind daraus direkt ablesbar. Dieser eine Aufruf liefert die
komplette Sweetspot-Rechnung:

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
z = open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines()
u_alle=[]; echte_user=0
for l in z:
    try: d=json.loads(l)
    except Exception: continue
    m=d.get('message') or {}
    if m.get('usage'): u_alle.append(m['usage'])
    if d.get('type')=='user':
        c=m.get('content')
        if isinstance(c,str): echte_user+=1
        elif isinstance(c,list) and not any(isinstance(p,dict) and p.get('type')=='tool_result' for p in c): echte_user+=1
k=lambda u:(u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0))/1000
start,jetzt,n = k(u_alle[0]), k(u_alle[-1]), len(u_alle)
spar=(jetzt-start)*0.1
neu=start*2   # 1-h-TTL (Pro/Max). Bei nachweislich 5-min-TTL: start*1.25
print('Start %.0fk - jetzt %.0fk - %d Anfragen, davon %d vom Nutzer (%.1f Schritte je Nachricht)'
      % (start,jetzt,n,echte_user,n/max(1,echte_user)))
print('Neue Session kostet einmalig ~%.0fk; spart %.1fk je Schritt; Break-even nach %.0f Schritten'
      % (neu, spar, neu/spar) if spar>0 else 'Kontext noch auf Startniveau - bleiben')
"
```

Was die Zahlen bedeuten und wie daraus eine Ansage wird:

- **„Anfragen" ist die Zahl, die zählt — nicht die Nachrichten des Nutzers.** In einer
  echten Bau-Welle standen 205 Anfragen 15 Nutzernachrichten gegenüber: rund 14 Schritte
  je Nachricht im Schnitt, in der Welle selbst weit über 100, in Gesprächsrunden genau 1.
  Genau deshalb ist ein fetter Kontext zum REDEN billig und zum ARBEITEN teuer.
- **Break-even in Schritten** sagt, ab wann sich der Wechsel lohnt. Liegt die erwartete
  Schrittzahl der nächsten Aufgabe darunter → bleiben. Darüber → wechseln.
- Die Ansage an den Nutzer nennt beide Zahlen und die Empfehlung in einem Satz, z. B.:
  „287k, Start war 82k — ein Wechsel kostet einmalig ~102k und lohnt ab ~5 Schritten.
  Testliste durchgehen: bleiben. Nächste Bau-Welle: wechseln."

Diese Messung gehört an jedes Wellenende und in jede Antwort auf „soll ich neu starten?".

## Diktieren ins Terminal: kurz halten, lang gehört ins Dokument

Wichtig für jeden, der seine Nachrichten spricht statt tippt (Yasin 25.08.2026):

**Terminals kürzen lange Eingaben zu einem Platzhalter.** In cmux erscheint ab einer
gewissen Länge nur noch `[pasted text]` (Ghostty und andere verhalten sich ähnlich) —
der Nutzer sieht dann NICHT mehr, was er eigentlich gesagt hat, kann es nicht überfliegen,
nicht korrigieren, nicht wiederfinden. Ein langes Diktat ist damit im Terminal
faktisch blind abgeschickt.

Daraus folgt die Arbeitsteilung, die dieser Skill ohnehin empfiehlt — jetzt mit dem
konkreten Grund dahinter:

- **Ins Terminal gehören kurze Nachrichten**: eine Frage, ein Auftrag, eine Korrektur.
  Kurz genug, dass sie als sichtbarer Text stehen bleibt.
- **Alles Lange gehört ins Handoff-Dokument im Texteditor**: Testantworten, Ideen,
  Braindumps, Kritik. Dort sieht der Nutzer jedes Wort, kann tagelang weiterarbeiten,
  ergänzen und umstellen — und der Agent liest am Ende das ganze Dokument auf einmal.
- Das ist kein Kompromiss, sondern der bessere Weg: Ein Handoff darf wochenlang
  wachsen, bis es voll ist. Dann eine frische Session, Dokument rein, weiter geht's.

Claude sagt das dem Nutzer EINMAL pro Setup — nicht bei jeder langen Nachricht.

## The window as a friendly coach (frame it this way)

Present the 1-hour window, the handoff ritual and the test list as POSITIVE motivators,
never as pressure or cost-anxiety. The sliding hour is a natural work rhythm: "answer
within the hour and the wave keeps riding" is the same gentle pull as a streak — it
nudges the user to test the delivered items now, dictate answers now, fire the next wave
now, while everything is fresh. The pre-seeded test questions make re-entry effortless
(no blank page — just put the cursor after the marker and speak). Claude should
occasionally voice this framing ("window's still warm — perfect moment for the test
list"), and celebrate kept streaks in the logbook rather than only counting waste.

## Der eigentliche Hebel: WENIGER ANFRAGEN (Yasin 26.08.2026, 16:48)

Dieser Skill hat sich lange auf die Kontextgröße konzentriert. Die Messung vom
26.08.2026 zeigt, dass das nur ein Drittel der Wahrheit war. Die Zahlen einer echten
Arbeitssitzung:

| Posten | Token | Faktor | Äquivalent |
|---|---|---|---|
| Cache gelesen | 22.171k | ×0,1 | 2.217k |
| Cache geschrieben | 562k | ×2 | 1.125k |
| **Eigene Ausgabe** | 208k | **×5** | **1.038k** |

**147 Anfragen — davon 13 durch Nutzernachrichten ausgelöst.** Die anderen 134 waren
eigene Tool-Schritte und Zwischenmeldungen. Und die eigene AUSGABE machte fast ein
Viertel der Gesamtkosten aus — der Posten, den dieser Skill vorher gar nicht erwähnt hat.

Daraus folgen drei Ziele, in dieser Reihenfolge: **weniger Anfragen · kürzere eigene
Ausgabe · kleinerer Kontext.** Die Übergabe (der ursprüngliche Zweck dieses Skills) ist
der SCHWÄCHSTE der drei Hebel.

### Die Technik-Liste (mit Codex gegengerechnet)

Ein zweites Modell (GPT-5.6 via Codex) hat dieselben Zahlen bekommen und geschätzt, was
jede Technik in genau dieser Sitzung gebracht hätte. Zielbild: **35–55 statt 147
Anfragen im Hauptkontext**, Gesamtkosten von 4.380k auf 1.350–2.050k.

| Technik | Wie | Effekt |
|---|---|---|
| **Werkzeuge bündeln** | Alle unabhängigen Lese-/Such-/Prüfschritte in EINER Antwort parallel anfordern, erst danach auswerten | −25 bis −45 Anfragen |
| **Skript statt Einzelbefehle** | Ein Aufruf, der zehn Dinge tut und EINE Zusammenfassung druckt, statt zehn Aufrufe | −20 bis −35 Anfragen |
| **Agenten nach Arbeitspaket schneiden** | EIN Agent macht „Ursache finden + Fix bauen + Tests prüfen", nicht drei Agenten je einen Teil | −30 bis −60 Anfragen |
| **Chef-Kontext schlank halten** | Der Agent bekommt Pfade, Ziel, Grenzen, Abnahmekriterien — nie die Chat-Historie | −0,2 bis −0,5 Mio. Lesen |
| **Berichte als Datei** | Details schreibt der Agent in eine Datei; zurück kommen nur Ergebnis, Risiken, Pfad | −0,3 bis −0,7 Mio. |
| **Berichtslänge begrenzen** | Dem Agenten im Auftrag vorgeben: höchstens 300 Wörter, keine Arbeitschronik, keine kopierten Protokolle | −0,2 bis −0,4 Mio. Ausgabe |
| **Zwischenmeldungen bündeln** | Siehe eigene Regel oben | −15 bis −30 Anfragen |
| **Ausgabe vorfiltern** | `grep`/`jq`/`tail` vor der Ausgabe; Erfolg einzeilig, bei Fehler nur die relevanten Zeilen | −0,1 bis −0,3 Mio. |
| **Eigenes Ausgabebudget** | Zwischenstände ≤100 Wörter, Abschluss ≤500 Wörter, Details in Dateien statt in den Chat | 208k → 50–80k Ausgabe |
| **Früher übergeben** | Bei 100–120k statt bei 223k | −0,3 bis −0,7 Mio. Lesen |

(Die Effekte überlappen und dürfen nicht addiert werden.)

### Wie wenige Anfragen sind realistisch? (die ehrliche Antwort)

Yasins naheliegende Nachfrage: „Versuchen wir, die 147 Anfragen zum Beispiel auf 14 zu
reduzieren — kann man das so sagen?"

Für den HAUPTKONTEXT: ja, die Größenordnung stimmt. Für die Arbeit selbst: nein — die
verschwindet nicht, sie WANDERT in die Subagenten. Genau darin liegt der Trick:

- 100 Arbeitsschritte im Hauptkontext bei 220k → 100 × 22k = **2.200k Äquivalente**.
- Dieselben 100 Schritte in einem Subagenten mit ~30k → 100 × 3k = **300k**.
- **Faktor ~7** — und keiner dieser 100 Schritte taucht in der Hauptsitzung als Anfrage auf.

Die realistische Untergrenze einer reinen Orchestrierungs-Welle, Posten für Posten:

| Anfragen | Wofür |
|---|---|
| 1 | Handoff lesen |
| 1–2 | die ganze Flotte in EINER gebündelten Antwort starten |
| je 1 pro Agent | sein Abschlussbericht — unvermeidbar, so kommt das Ergebnis an |
| 2–3 | Bauen, Testen, Committen, je über EIN Skript |
| 1 | Handoff schreiben |
| 1 | Abschlussmeldung |

Das landet bei grob **13–20 statt 147 Anfragen** für dieselbe gelieferte Arbeit.
Zwischengespräche mit dem Nutzer kommen obendrauf — und die sind gewollt, kein Verschnitt.
Wegzukürzen ist das Geplapper der Maschine, nie das Denken des Nutzers.

### Nachrichten WÄHREND der Arbeit sind fast gratis (Yasin 26.08.2026, 17:26)

Seine Frage, dreimal gestellt, weil die Antwort alles ändert: „Kostet diese Nachricht
jetzt auch nichts, weil du gerade arbeitest? Oder meinst du, weil es kurze Nachrichten
sind?"

Nicht die Kürze ist der Grund, sondern der **Zeitpunkt**. Und der Unterschied ist groß:

- **Der Agent arbeitet gerade** (Werkzeuge laufen, Subagenten rechnen). Die Nachricht wird
  in den laufenden Ablauf eingehängt und fährt bei der nächsten Anfrage mit, die ohnehin
  stattgefunden hätte. Es entsteht **keine zusätzliche Anfrage**. Bezahlt wird nur der
  Nachrichtentext selbst, einmal in den Cache geschrieben: 50 Wörter ≈ 70 Token × 2 ≈
  **140 Äquivalente**.
- **Der Agent wartet** (Ruhezustand nach seiner Antwort). Jetzt LÖST die Nachricht eine
  Anfrage aus, die sonst nicht stattgefunden hätte: **der volle Kontext × 0,1**. Bei 220k
  sind das **22.000 Äquivalente** — das 150-Fache.

Dasselbe in einem Satz: Während der Arbeit kostet eine Zwischenfrage rund ein halbes
Prozent dessen, was sie im Ruhezustand kostet.

**Der Haken, der dabei gern übersehen wird:** Die Frage ist billig — die ANTWORT nicht.
Ausgabe kostet Faktor 5; eine 300-Wörter-Antwort sind ~2.000 Äquivalente, also das
Vierzehnfache der Frage. Deshalb gilt für Antworten auf Zwischenfragen während einer
laufenden Welle: **kurz halten, Details später im Handoff.** Nicht die Frage bremsen,
sondern die eigene Ausschweifung.

**PRÄZISIERUNG, weil „während etwas läuft" zwei verschiedene Dinge heißt (Yasin fragte
sofort nach, 26.08.2026, 17:37 — zu Recht).** Entscheidend ist nicht, ob IRGENDWO etwas
rechnet, sondern ob der eigene Werkzeug-Ablauf gerade läuft:

| Lage | Nachricht des Nutzers | Kosten |
|---|---|---|
| Der eigene Tool-Loop läuft (Datei lesen, Befehl, Agent starten) | wird angehängt, fährt mit | **fast null** |
| **Subagenten rechnen, man selbst wartet** | löst eine neue Anfrage aus | **volle 10 %** |
| Nach der eigenen Antwort, Ruhezustand | löst eine neue Anfrage aus | **volle 10 %** |

Der mittlere Fall ist der überraschende und muss dem Nutzer ausdrücklich gesagt werden:
Während Subagenten arbeiten, ARBEITET DER HAUPTAGENT NICHT — er wartet auf ihre
Meldungen. Eine Nachricht in dieser Zeit ist so teuer wie jede andere im Ruhezustand.

Ein Trost, der auch stimmt: **Mehrere Nachrichten kurz hintereinander werden zu EINER
Anfrage gebündelt**, wenn sie eintreffen, bevor die Antwort beginnt. Zwei Gedanken direkt
nacheinander kosten also einmal, nicht zweimal.

Was der Nutzer daraus praktisch mitnimmt — und das gehört ihm EINMAL gesagt:

> Solange du siehst, dass ich selbst rattere, schreib ruhig sofort. Wenn nur die
> Unteragenten laufen oder ich auf dich warte, sammle lieber und schick es gebündelt —
> am besten in den Sammelbereich des Handoffs, dort kostet es gar nichts.

Und genau deshalb ist der Sammelbereich im Handoff so wertvoll: Dort kostet Sammeln
exakt null, weil gar keine Anfrage entsteht.

### Was wird eigentlich GESCHRIEBEN? (die meistunterschätzte Spalte)

Yasin nahm am 26.08.2026 um 18:04 an, die 1.125k Schreibkosten kämen von seinen eigenen
Nachrichten: „Egal ob ich gesammelt oder einzeln schreibe — das Schreiben ist nicht zu
vernachlässigen." Der Schluss ist verständlich und trotzdem falsch, und die Korrektur
ändert, wo man ansetzt.

Geschrieben wird alles, was NEU in den Verlauf kommt. Nach Größe sortiert:

1. **Werkzeug-Ergebnisse** — Dateiinhalte, Befehlsausgaben, Suchtreffer, Bilder. Eine
   gelesene 500-Zeilen-Datei sind ~7k Token, die einmal zum doppelten Preis in den Cache
   wandern. Das ist mit Abstand der größte Posten.
2. **Subagenten-Berichte** — ein 800-Wörter-Bericht sind ~1k Token × 2. Bei zehn Agenten
   summiert sich das; deshalb steht die 300-Wörter-Grenze im Subagenten-Vertrag.
3. **Die eigenen Antworten** — sie zahlen doppelt: erst als Ausgabe (×5), dann beim
   nächsten Schritt als Cache-Schreibung (×2).
4. **Die Nachrichten des Nutzers** — der kleinste Posten von allen. 100 Wörter ≈ 140 Token
   × 2 = 280 Äquivalente. Bei 1.125k Gesamtschreibung ist das ein Promille.

**Daraus folgt die Handlungsanweisung, und sie zielt NICHT auf den Nutzer:** Nicht ganze
Dateien lesen, wenn ein `grep` reicht. Befehlsausgaben vorfiltern statt roh hereinlassen.
Berichte begrenzen. Bilder nur ansehen, wenn sie wirklich gebraucht werden. Der Nutzer
soll ruhig schreiben, so viel er will — er ist nicht das Problem.

### Die ehrlichste Zahl im ganzen Skill: was Subagenten wirklich sparen

Das gehört sauber ausgerechnet, weil hier vorher zwei verschiedene Dinge in EINER Rechnung
standen — links 147 Schritte, rechts 600 — und daraus der falsche Schluss gezogen wurde,
Subagenten senkten die Rechnung nicht. Der Vergleich war unfair: Er setzte auf beiden
Seiten unterschiedlich viel Arbeit an. Es sind zwei Aussagen, und die erste ist die
wichtigere.

**Erstens: gleiche Arbeit, nur delegiert — hier wird es wirklich billiger.**

```
Alles im Hauptkontext:  147 Schritte × 151k × 0,1              = 2.217k
Delegiert:               14 Hauptanfragen × 345k × 0,1  =  483k
                        147 Agentenschritte ×  30k × 0,1 =  441k
                                                   Summe =  924k
```

**2,4× weniger für exakt dieselbe Arbeit.** Mehr steckt nicht dahinter: Jeder Schritt
rechnet gegen den kleinen Kontext des Agenten statt gegen den fetten der Sitzung — je
Arbeitsschritt rund **ein Fünftel**.

**Zweitens, und das ist ein SEPARATER Gedanke:** Wer die Ersparnis nicht einsteckt, sondern
reinvestiert, bekommt fürs gleiche Kontingent ein Vielfaches an Arbeit. Ein Agent arbeitet
gründlicher, als man es nebenbei täte — aus 147 Schritten werden schnell 600:

```
14 Hauptanfragen × 345k × 0,1 =   483k
600 Agentenschritte × 30k × 0,1 = 1.800k
                          Summe = 2.283k
```

Dann ist die Rechnung wieder ungefähr ausgeglichen — aber es ist **viermal so viel
erledigt**. Genau das meint die „Token-Maximierung", die der Nutzer will: mehr Arbeit fürs
gleiche Kontingent, nicht weniger Ausgabe.

> **Subagenten machen beides: dieselbe Arbeit deutlich billiger (Faktor ~2,4) — und, wenn
> man das Gesparte wieder ausgibt, ein Vielfaches an Arbeit zum selben Preis.**

Und die Ehrlichkeit, die dazugehört: **Subagenten-Tokens sind nicht gratis.** Sie
belasten dasselbe Wochenkontingent. Was sie nicht belasten, ist der HAUPTKONTEXT — die
Sitzung bleibt klein, schnell und antwortfähig, und genau das ist ihr Wert. Wer glaubt,
Agenten liefen „nebenbei", wundert sich später über sein Kontingent.

### Subagenten sind der Standardweg, nicht die Ausnahme

Yasins Formulierung, und sie trifft es: „Ziel ist, dass ich mit einem guten Modell
arbeite, das als Chef die Unteragenten rauslässt, wenig Tokens verbraucht, gebündelt
alles sagt und wenig Anfragen macht."

**Warum die STARTKOSTEN den Unterschied machen.** Yasin hat den Mechanismus besser
formuliert als jede Dokumentation (26.08.2026): „Wenn du einen Unteragenten losschickst,
startet der nicht wie eine neue Session bei 80.000 Tokens mal zwei, sondern zum Beispiel
bei 10.000 mal zwei. Er verbrät dann intern viel, teilweise günstig, teilweise teuer —
aber er gibt WENIG zurück, weil er nur das Ergebnis zurückgibt. Und somit bleibt die
aktuelle Session klein und günstig."

Dasselbe, Posten für Posten:

1. **Startkontext.** Eine frische Session lag in einem echten Projekt bei **82k**, bevor
   eine einzige Zeile Arbeit passiert war — Skills, Werkzeugschemata und Projektregeln
   sind vorher da —, und der Neuaufbau kostet das mal zwei. Ein Subagent startet mit
   seinem Auftrag plus eigenen Werkzeugschemata, also grob **10–20k**; mal zwei sind das
   einmalig ~20–40k.
2. **Was intern passiert.** Der Agent liest, sucht, ändert, testet — Dutzende Schritte,
   von denen jeder nur SEINEN kleinen Kontext zu ×0,1 neu liest. Manche Schritte sind
   billig, manche (lange Dateien, Testausgaben) nicht — aber jeder rechnet gegen ~15k
   statt gegen deine 220k. Deshalb kosten 100 Schritte dort ~300k und hier ~2.200k.
3. **Was in den Hauptkontext zurückfließt.** Genau zwei Dinge: der Auftrag, den du
   geschrieben hast, und der Bericht, den du auf 300 Wörter begrenzt hast. Arbeitschronik,
   Protokolle und Sackgassen bleiben im Kontext des Agenten und sterben mit ihm.

Teure Arbeit, billige Quittung — diese Asymmetrie ist der größte Einzelhebel in diesem
ganzen Skill. In der gemessenen Sitzung haben sechs Agenten zusammen über eine Million
Token verbraucht; im Hauptkontext landeten davon nur Aufträge und Berichte.

**Wann ein Subagent sich NICHT lohnt** (auch das gehört zur Ehrlichkeit): unter etwa
3–5 Werkzeugschritten, bei streng sequenzieller Arbeit, oder wenn erst viel gemeinsamer
Kontext übertragen werden müsste. Seine Startkosten sind grob 1–3 Anfragen plus
Briefing plus Bericht.

**Modell und Denktiefe gehören in den ANGEZEIGTEN Namen (Yasin 26.08.2026, 17:35).**
Sein Einwand: „Wenn du Unteragenten losschickst — kannst du unten anzeigen, welche Art
gerade arbeitet? GPT-5.6 hoch, extra hoch, oder Opus 5? Den Effort stellst du doch auch
ein. Aktuell sehe ich nie, welcher Agent das ist."

Er hat recht, und die Lösung ist trivial: Der Host zeigt die KURZBESCHREIBUNG des Agenten
an — also gehört das Modell da hinein, nicht nur die Aufgabe.

```
schlecht:  "History-Tempo Runde 2"
gut:       "Opus5/high · History-Tempo"
gut:       "Fable/low · Testdateien umbenennen"
gut:       "GPT5.6 · Zeitmessende Tests"     (Codex-Lauf)
```

Damit sieht der Nutzer im Terminal auf einen Blick, ob gerade ein teures oder ein billiges
Modell läuft — und kann eingreifen, bevor die Tokens weg sind. Wird kein Modell gesetzt,
erbt der Agent das Sitzungsmodell; auch das gehört dann so benannt („geerbt"), statt es zu
verschweigen. Dieselbe Regel gilt für die Ansage im Chat: Wenn eine Flotte startet, steht
in der EINEN Startmeldung, wer auf welchem Modell mit welcher Denktiefe läuft.

**Der Subagenten-Vertrag**, der in jeden Auftrag gehört:

> Arbeite bis zum Ergebnis oder bis zu einer echten Blockade. Melde nur: Status,
> Entscheidungen, Belege mit Pfaden, Risiken, nächster Schritt. Höchstens 300 Wörter,
> keine Arbeitschronik, keine kopierten Protokolle oder Diffs — Details in eine Datei.

### Die Ausgabe ist teuer — schreib kürzer

Ausgabe kostet den **fünffachen** Preis von frischer Eingabe und das Fünfzigfache eines
Cache-Lesers. Praktisch heißt das:

- **Kein Nacherzählen der eigenen Arbeit.** Was der Nutzer im Terminal sieht, muss nicht
  in Prosa wiederholt werden.
- **Lange Inhalte gehören in Dateien**, nicht in den Chat — das Handoff ist genau
  deshalb eine Datei und keine Chat-Nachricht.
- **Keine Fassung „zur Sicherheit noch mal komplett".** Ein Verweis auf die Datei genügt.
- Das Handoff selbst bleibt ausführlich: Es ersetzt einen ganzen Kontext und ist damit
  die beste Investition auf der Liste. Ausführlich ≠ geschwätzig.

### Dieser Skill soll SCHULEN, nicht nur takten

Yasins ausdrücklicher Auftrag (16:53): „Der Skill soll auch schulen. Die Leute sollen
verstehen, wie das genau funktioniert. So wie es mir geht, geht es vielen Leuten."

Deshalb gilt für jede Kostenaussage gegenüber dem Nutzer:

1. **Erst die Zahl, dann die Regel.** Nicht „das ist teuer", sondern „das sind 22k
   Äquivalente, weil der Kontext 220k groß ist und Lesen ein Zehntel kostet".
2. **Missverständnisse aktiv ausräumen.** Das häufigste: „X Anfragen = X Cache-
   Neuaufbauten". Falsch — siehe die Messung im Abschnitt „Einen Cache-Neuaufbau
   ERKENNEN".
3. **Eigene Fehler benennen.** Wenn eine frühere Erklärung schief war (hier: „fast die
   Hälfte gespart" — nachgerechnet waren es eher ein Drittel), wird das korrigiert, nicht
   stillschweigend überschrieben.

## Die Kostenzeile unter JEDER Antwort (Yasin 26.08.2026, 18:06)

Sein Wunsch: „Kannst du bei jeder Nachricht, die du ausgibst, sagen, was wie viel
gekostet hat — zehn Prozent, zweihundert Prozent? Diese Tokenangabe einfach zusätzlich
bei deinen Antworten." Und die Gegenfrage gleich hinterher: „Oder sprengt das den Skill?"

Es sprengt ihn nicht — es ist sein Kern: Kosten sichtbar machen, statt über sie zu reden.
Aber es hat eine Falle, die man beim Bauen sofort trifft.

**Die Falle:** Eine Messung braucht einen Werkzeugaufruf, und ein Werkzeugaufruf IST eine
Anfrage — bei 350k Kontext also 35k Äquivalente. Wer die Kostenanzeige naiv baut, zahlt
für das Messen mehr, als die Anzeige je einspart. Das wäre ein Thermometer, das den Raum
heizt.

**Die Lösung:** `~/.claude/ctx.sh` wird NIE allein aufgerufen, sondern an einen Befehl
angehängt, der ohnehin läuft — meist an dasselbe `date`, das den Zeitstempel liefert:

```bash
date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh
```

Ausgabe (echte Zeile):

```
KOSTEN | Kontext 366k · letzte Anfrage: 366k gelesen ×0,1 + 0.4k geschrieben ×2
        + 2.9k Ausgabe ×5 = 52k | Sitzung: 265 Anfragen, 9520k
```

Daraus wird unter der Antwort eine Zeile in Klartext:

> *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe
> (×5) ≈ 52k · Sitzung bisher: 265 Anfragen, 9.520k*

**Die zwei Ehrlichkeitsregeln dazu** — dieselben wie bei Uhrzeit und Kontextgröße:

1. **Alle drei Zahlen stammen aus der LETZTEN ABGESCHLOSSENEN Anfrage** — nicht aus der
   Antwort, unter der die Zeile steht. Die Kosten der laufenden Antwort stehen erst fest,
   wenn sie fertig ist; niemand kann sie währenddessen kennen. Yasin hat am 26.08.2026
   genau richtig nachgefragt: „Diese 2.600 Ausgabe-Token — sind das wirklich die dieser
   Antwort gewesen?" Nein. Beim Lesen und Schreiben fällt das kaum auf, weil der Kontext
   je Schritt nur um Prozente wächst. Bei der AUSGABE dagegen sehr wohl: Eine kurze Antwort
   steht dann unter der Ausgabezahl einer langen — und umgekehrt. Deshalb heißt die Zeile
   **„Letzte gemessene Anfrage"** und nicht mehr „Diese Runde".
   Die Alternative: Man KÖNNTE die Ausgabe der laufenden Antwort aus ihrer Wortzahl
   schätzen (Wörter × ~1,4). Erlaubt — aber das wäre eine Schätzung neben zwei Messwerten,
   und wer sie hinschreibt, markiert sie als Schätzung („≈2,6k geschätzt").
2. **Ohne Messung in dieser Runde keine Zahl** — oder eine ausdrücklich mit `~` markierte
   Fortschreibung des letzten Standes. Nie eine erfundene.

**Der zweite Zweck der Zeile: sich melden, wenn eine Runde auffällig teuer war**
(Yasin 26.08.2026, 18:17). Sein Wunsch im Wortlaut: „Das ist ja das Genialste, dass du am
Ende genau das sagst, was ich sehen wollte — dann sieht der User, was er gerade verbraucht
hat. Und wenn er ganz viel verbraucht hat, kannst du ja noch hinweisen: hallo, das war blöd
von dir. In irgendeiner Form, ganz nett."

- **Wann überhaupt:** nur, wenn eine Runde deutlich über dem eigenen Schnitt DIESER Sitzung
  liegt — grob: mehr als das Doppelte der bisherigen Durchschnittskosten je Anfrage. Keine
  feste Grenze; der Schnitt steht in der Sitzungsdatei und ist damit gemessen, nicht geraten.
- **Der Ton ist das Entscheidende, und er ist ausdrücklich NICHT tadelnd** — der Nutzer hat
  selbst „ganz nett" gesagt. Nie „das war blöd", sondern Ursache benennen und einen
  konkreten billigeren Weg anbieten:

  > „Die Runde war teuer (≈120k), weil ich drei große Dateien komplett gelesen habe — beim
  > nächsten Mal reicht ein gezielter Suchlauf."

  > „Diese fünf kurzen Nachrichten haben zusammen ≈180k gekostet, weil der Kontext
  > inzwischen 350k groß ist. Gesammelt in einer wären es ≈37k gewesen."
- **Die Verantwortung liegt fast immer beim AGENTEN, nicht beim Nutzer.** Das gehört
  ausdrücklich hierher, sonst wird aus der Funktion Nutzer-Erziehung. Die häufigsten
  Ursachen teurer Runden sind: ganze Dateien lesen statt greppen, ungefilterte
  Befehlsausgaben, zu lange eigene Antworten, Einzelmeldungen je Subagent — alles Dinge,
  die der Agent abstellt, nicht der Nutzer.
- **Höchstens EINMAL je Welle**, nicht bei jeder teuren Runde erneut. Sonst wird aus dem
  Hinweis Gemecker.
- **Die Gegenrichtung gehört dazu.** War eine Runde ungewöhnlich günstig oder eine Welle gut
  gelaufen, wird das genauso benannt: „Die ganze Welle lief über Subagenten — 40k im
  Hauptkontext für sechs Arbeitspakete." Der Skill soll motivieren, nicht mahnen.

**Wann die Zeile weggelassen wird:** in reinen Zwischenrufen und Einzeilern. Eine
Kostenzeile unter einem Dreiwortsatz ist Lärm. Sinnvoll ist sie am Ende jeder inhaltlichen
Antwort, am Wellenende und im Handoff.

## Die Kostentabelle je Sitzung (Yasin 26.08.2026, 17:51)

Sein Wunsch: „Kannst du nicht einfach so eine Tabelle machen, wo wir alles übersichtlich
haben je Session — damit man eine Übersicht hat, was wann wie viel Tokens gekostet hat?
Das wäre doch genial."

Gebaut als `~/.claude/session-kosten.sh`. Die Einheit der Tabelle ist bewusst der
**Abschnitt zwischen zwei Nutzernachrichten** — das ist, was ein Mensch erlebt („ich habe
etwas gesagt, dann ist etwas passiert"), nicht die einzelne Modellanfrage, die niemand
sieht.

```bash
~/.claude/session-kosten.sh              # aktuelles Projekt, neueste Sitzung
~/.claude/session-kosten.sh --markdown   # nur die Tabelle, fertig fürs Handoff
```

Beispielausgabe (echte Sitzung):

```
| # | Zeit | Worum es ging | Anfr. | Kontext | gelesen | geschr. | Ausgabe | Äquiv. |
| 1 | 14:05 | Handoff beantwortet …          | 147 | 223k | 22171k | 562k | 208k | 4380k |
| 6 | 17:22 | Also ich habe ja jetzt vorhin … |  25 | 319k |  7346k | 108k |  69k | 1297k |
| Σ |       | 10 Abschnitte                  | 246 | 345k | 49906k | 811k | 396k | 8594k |

Teuerster Abschnitt:  #1 um 14:05 (4380k Äquivalente, 147 Anfragen)
Anfragen je Nachricht: 24,6 im Schnitt
Anteil eigene Ausgabe: 23 % der Gesamtkosten
Cache-Trefferquote:    1,6 % geschrieben (unter 10 % = warm)
```

### Wie man diese Tabelle liest (Yasin verstand sie beim ersten Anblick nicht — zu Recht)

Seine Fragen im Wortlaut: „22.171k — sind das 22 Millionen Token gelesen? Was wurde da
gelesen? Warum steht in Zeile 2 als Kontext 241k? Ich kapiere die ganze Tabelle nicht."
Vollkommen berechtigt: Ohne das folgende Bild ergibt keine einzige Zahl darin Sinn. Diese
Erklärung gehört deshalb dazu, wann immer die Tabelle jemandem gezeigt wird.

**Zuerst das Banale, weil genau daran das Verständnis hängenbleibt: „k" heißt Tausend.**
22.171k sind also 22.171.000 Token — ja, zweiundzwanzig Millionen, in einer einzigen Sitzung.

**Und nun das Bild, mit dem alles klickt: Der Gesprächsverlauf ist ein Buch.** Das Modell hat
zwischen zwei Anfragen KEIN Gedächtnis. Vor jeder einzelnen Antwort liest es das GANZE Buch
noch einmal von vorne — jede frühere Nachricht, jede gelesene Datei, jedes Werkzeugergebnis.
Bei 147 Anfragen und einem Buch, das im Schnitt rund 151.000 Token („Seiten") dick war, sind
das 147 × 151k = **22.171k gelesene Seiten**. Deshalb steht in der Lese-Spalte eine Zahl, die
ein Vielfaches der Kontext-Spalte ist. Das ist kein Fehler in der Tabelle — das IST die
Funktionsweise.

**Die Rechnung geht exakt auf**, und genau deshalb überzeugt sie:

```
147 Anfragen × ~151k Durchschnittskontext = 22.171k gelesen   × 0,1  = 2.217k
                                               562k geschrieben × 2   = 1.125k
                                               208k eigene Ausgabe × 5 = 1.038k
                                                                 Summe = 4.380k
```

4.380k — genau die Zahl, die in der Äquivalent-Spalte steht.

**Was jede Spalte bedeutet:**

| Spalte | Bedeutung |
|---|---|
| **#** | Nummer des Abschnitts (ein Abschnitt = von einer Nutzernachricht bis zur nächsten) |
| **Zeit** | wann der Abschnitt begann, in deiner Ortszeit |
| **Worum es ging** | die ersten Wörter deiner Nachricht, damit du die Zeile wiedererkennst |
| **Anfr.** | wie viele Anfragen ans Modell dieser eine Satz von dir ausgelöst hat |
| **Kontext** | wie dick das Buch am ENDE des Abschnitts war — **keine Kostenspalte** |
| **gelesen** | Anfragen × Buchdicke; der größte Posten, Preis ×0,1 |
| **geschr.** | was neu in den Cache geschrieben wurde, Preis ×2 |
| **Ausgabe** | was Claude selbst geschrieben hat, Preis ×5 |
| **Äquiv.** | die drei Posten auf einen Preis umgerechnet und addiert |

**Der wichtigste Satz zur Kontext-Spalte: Sie addiert sich NICHT.** „241k" in Zeile 2 heißt
nicht, dass dieser Abschnitt 241k gekostet hätte — es heißt, dass das Buch am Ende dieses
Abschnitts 241.000 Token dick war. Sie steht da, um die Lese-Spalte zu ERKLÄREN: je dicker
das Buch, desto teurer jede weitere Anfrage. Deshalb wächst sie über die Sitzung stetig,
während die Kostenspalten je Abschnitt schwanken.

**Und eine Zeile mit 0 Anfragen ist kein Fehler.** Sie bedeutet: Diese Nachricht traf ein,
während die Arbeit schon lief, wurde an den laufenden Ablauf angehängt und hat keine eigene
Anfrage ausgelöst — genau der Fall aus der Tabelle „Nachrichten WÄHREND der Arbeit sind fast
gratis". Eine Null dort ist die billigste Zeile, die es gibt.

Die vier Zeilen unter der Tabelle sind der eigentliche Ertrag — sie beantworten je eine
Frage, die sonst offen bleibt: *Welche Welle war teuer? Wie viele Schritte löst eine
Nachricht aus? Wie viel kostet mein eigenes Geschwätz? War der Cache überhaupt warm?*

**Regel: Diese Tabelle gehört in JEDES Handoff**, direkt vor die Schlusszeile mit dem
Kontextstand. Sie ersetzt die bisherige Einzelzahl („Kontext dieser Session: 220k") nicht,
sondern erklärt sie. Und sie ist ehrlicher als jede Erinnerung: Sie zeigt auch die
Abschnitte, in denen viel Geld für wenig Ergebnis verbrannt wurde.

**Zwei Dinge, die das Skript bewusst so macht — und die man beim Nachbauen leicht falsch
macht:** Die Sitzungsdatei speichert UTC, der Nutzer denkt in seiner Ortszeit (umrechnen,
sonst stimmt die ganze Tabelle scheinbar nicht). Und nicht jede Zeile vom Typ „user" ist
eine Nachricht des Menschen — Werkzeug-Ergebnisse, Agenten-Fertigmeldungen und
Skill-Ladungen tragen denselben Typ. Ohne Filter zerfällt die Tabelle in Systemzeilen und
wird unlesbar.

## Bezahltes Kontingent sichtbar machen — und ausnutzen (Yasin 26.08.2026, 14:03)

Sein Wunsch im Wortlaut: „Siehst du bei Codex überhaupt, ob ich noch genug Limit habe?
Könnte man das sichtbar machen — und dass du mich ab und an darauf hinweist? Wenn ich
einen Account habe, wo ich monatlich bezahle, dann sollte man die Tokens ausnutzen, wenn
da noch welche frei sind. Der Skill könnte sagen: hey, wir hätten jetzt Zeit, wir haben
noch ganz viele Tokens übrig in Codex oder in deinem Wochenkontingent — mach dir mal
Gedanken, was wir da machen könnten. Und das gehört ganz oben ins Handoff, als
Hauptinformation."

Beides ist auslesbar, keins davon sieht Claude von allein:

**Codex/GPT** — die Codex-CLI hat keinen Usage-Befehl, aber der Server schickt bei jeder
Antwort einen `rate_limits`-Block, den die CLI in ihre Session-Datei schreibt
(`~/.codex/sessions/JJJJ/MM/TT/rollout-*.jsonl`). Fertig ausgewertet:

```bash
~/.claude/codex-limit.sh          # "Codex (plus): 10 % vom 7d-Fenster verbraucht, Reset in 5d 2h  [… vor 24 h]"
~/.claude/codex-limit.sh --kurz   # "codex 10%/7d"  (steht so in der Statuszeile)
~/.claude/codex-limit.sh --json
```

Ehrliche Grenze, die IMMER mitgesagt wird: Die Zahl ist so frisch wie der letzte
Codex-Lauf. Wer seit Tagen kein Codex benutzt hat, sieht einen alten Stand — und der ist
eher zu hoch als zu niedrig, weil das Fenster inzwischen weitergelaufen ist. Das Skript
nennt das Alter der Messung selbst; dieses Alter gehört mit ins Handoff.

**Claude Code** — die eigenen 5-Stunden- und Wochen-Prozente stehen NUR im stdin-JSON der
Statuszeile, nicht im Modellkontext. Die Statuszeile legt sie deshalb bei jedem Render ab:

```bash
cat ~/.claude/.claude-kontingent   # {"stand":"…","fuenf_stunden_prozent":3,"sieben_tage_prozent":0}
```

Auch hier: Der `stand`-Zeitstempel gehört dazu, und bei Abweichungen zur Web-Oberfläche
(Einstellungen ▸ Nutzung) ist die Web-Oberfläche die Autorität — sie zählt alles, das
Terminalfeld nur den Claude-Code-Anteil und in Stufen.

**Was daraus im Handoff wird:** ein kurzer Block **ganz oben**, direkt nach „Der Stand in
drei Sätzen", nie am Ende. Drei Zeilen genügen — zwei Zahlen und ein Vorschlag:

```
## Was noch im Tank ist

- **Codex/GPT:** 10 % vom Wochenfenster verbraucht, Reset in 5 Tagen
  (gemessen beim letzten Codex-Lauf, vor 24 h) → 90 % frei.
- **Claude Code:** 5h 3 % · Woche 0 % (Stand 14:12).
- **Vorschlag:** Codex hat viel Luft — die Startzeit-Analyse und der
  9-Stunden-Langzeittest wären genau die Sorte Arbeit dafür.
```

Ton: beiläufig und einladend, nie mahnend — es ist bezahltes Kontingent, kein Budget, das
man schonen muss. Der Vorschlag ist der eigentliche Punkt: Wenn viel frei ist, benennt
Claude KONKRET, welche offenen Posten aus dem roten Faden sich damit erledigen ließen
(große Analysen, Langzeittests, Zweitmeinungen, Migrationen) — nicht „du könntest mehr
nutzen", sondern „damit könnten wir X und Y machen".

**Ist viel frei, wird GROSSES VORGESCHLAGEN — dafür ist dieser Block da.** Ungenutztes
Kontingent verfällt. Es wandert nicht in die nächste Woche, es ist einfach weg; der Verlust
ist das ablaufende Fenster, nie das Ausgeben. Wann immer das 5-Stunden- oder das
Wochenfenster noch echte Luft hat, sagt Claude das UND nennt etwas, das sich damit lohnt.
Yasins eigenes Bild: „Schau mal, check mal alles durch, ob das gut ist." Gute Kandidaten,
gerade weil sie teuer und nie dringend sind:

- ein Durchlauf über das ganze Projekt mit HOHER Denktiefe („ultrathink") — Architektur,
  toter Code, Widersprüche; die Dinge, die niemand einplant;
- ein Qualitäts-Check eines ganzen Bereichs gegen seine Abnahmekriterien, nicht nur gegen
  den letzten Diff;
- eine große Zweitmeinungs-Analyse auf einem anderen Modell (Codex/GPT) — eine andere
  Architektur sieht andere Fehler als ein erneutes Lesen durch dieselbe;
- ein langer Testlauf, den sich niemand freiwillig hinsetzt: Startzeiten, Langzeittests,
  eine volle Matrix.

Formuliert als Einladung mit Zahl daneben: „90 % der Woche sind noch frei — das ist der
Moment für den großen Review, billiger als auf schon bezahltem Kontingent wird er nie."
Nie: „du solltest dein Kontingent mehr ausnutzen."

Und: Ist ein Kontingent fast leer (> ~85 %), gehört das genauso in denselben Block, mit
der Reset-Zeit daneben — dann ist die Botschaft „bis morgen früh lieber die kleinen
Sachen", was dieselbe Information von der anderen Seite ist.

### Aufwach-Ping für die Codex-Anzeige (Yasin 27.08.2026)

Sein Wunsch, nachdem `codex-limit.sh` an einem Tag nur
`{"primary": null, "secondary": null, "plan": "plus",
"alter_minuten": 107}` lieferte, also gar keine Zahl: „Ja gerne
einbauen bitte. Auch in dem Skill einbauen. Auch in GitHub
warm-handoff."

**Das Problem:** `codex-limit.sh` liest die Kontingente nicht
live, sondern aus der LETZTEN Codex-Sitzungsdatei. Die Zahl ist
also nur so frisch wie der letzte Codex-Lauf — lag der Stunden
zurück, zeigt das Skript einen veralteten Stand oder, wie oben,
gar keinen. **`null` heißt dabei nicht „0 % verbraucht"**,
sondern „seit dem letzten Lauf kam kein neuer `rate_limits`-
Block an, der Wert ist unbekannt" — eine Null wäre hier eine
Fabrikation, dieselbe Falle wie bei Uhrzeit und Kontextgröße.

**Die Lösung:** einmal je Sitzung einen winzigen Codex-Aufruf
absetzen, damit der Server einen frischen `rate_limits`-Block
schickt:

```bash
codex exec --skip-git-repo-check "Antworte nur mit: bereit"
```

- **Wann:** einmal pro Sitzung, zu Beginn — angehängt an einen
  Befehl, der ohnehin läuft (z. B. den ersten echten
  Codex-Auftrag der Sitzung), NIE als eigener, sonst
  zusätzlicher Aufruf nur fürs Messen.
- **Kosten ehrlich benannt:** Das kostet ein paar Codex-Token —
  vernachlässigbar gegen ein bezahltes Wochenkontingent, aber
  nicht null. Deshalb an einen ohnehin fälligen Aufruf hängen,
  nicht extra dafür starten.
- **Ist Codex nicht installiert oder nicht eingeloggt:** still
  weitergehen, keinen Fehler melden — der Ping ist ein Bonus
  für die Anzeige, kein Pflichtschritt der Sitzung.
- Danach zeigt `codex-limit.sh` den frischen Stand, und das
  „vor X h" im Handoff-Block oben stimmt wieder mit der
  Realität überein.

### Codex, Gemini und OpenRouter zusammendenken (Yasin 27.08.2026)

Sein Auftrag, nachdem der Aufwach-Ping stand: „Nee, das ist
super, macht es." Gemeint: alle DREI Kontingente als EIN Bild
sehen, nicht nur Codex.

**Der gemeinsame Kern: bei allen dreien verfällt, was nicht
genutzt wird.** Codex im bezahlten Abo läuft in einem
Wochenfenster ab, egal ob benutzt oder nicht. Gemini stellt
kostenfreie Anfragen bereit, die ebenfalls mit dem Fenster
verfallen. OpenRouter bietet kostenfreie Modelle (Yasin nutzt
dort u. a. „Ox Alpha" als Zweitreviewer) — auch dort ist eine
ungenutzte Anfrage kein Guthaben fürs nächste Mal, sondern
schlicht weg. Dieselbe Haltung wie beim Claude-Kontingent oben:
nicht schonen, AUSNUTZEN, solange das Fenster läuft.

**Zuordnung — welche Arbeit zu wem passt:**

| Arbeit | Anbieter | Warum |
|---|---|---|
| Große Lese-/Analyse-/Review-Läufe, ganzes Projekt durchsehen | Codex oder OpenRouter | Andere Architektur sieht andere Fehler; teuer und selten dringend — genau wofür verfallendes Kontingent da ist |
| Zweitmeinung zu eigenem Code/eigener Antwort | Codex oder OpenRouter (z. B. Ox Alpha) | No-Self-Review-Regel — Claude darf sich nicht selbst gegenlesen |
| Umbauten IM Code | Claude | Bleibt im Fahrersitz, kennt Verlauf und Entscheidungen |
| Recherche, sehr lange Kontexte | Gemini | Großes Kontextfenster, genau dafür gebaut |

**Wie man den Stand sieht — und wo ehrlich nichts gemessen wird:**

- **Codex:** `~/.claude/codex-limit.sh` (s. oben), nach dem
  Aufwach-Ping frisch. Zeigt Prozent vom 7-Tage-Fenster plus
  Reset-Zeit.
- **Gemini und OpenRouter:** Hier gibt es kein Skript und keine
  verlässliche Messung — kein Kontostand wird erfunden. Ehrlich
  sagen: „Bei Gemini/OpenRouter kann ich den Kontingentstand
  nicht auslesen, nur den Nutzungshinweis in der jeweiligen
  Oberfläche zeigen." Ein `~` oder ein geschätzter Prozentwert
  wäre hier dieselbe Fabrikation wie bei Uhrzeit oder
  Kontextgröße oben — deshalb bewusst weggelassen statt geraten.

**Ton:** einladend, mit Zahl daneben, nie mahnend — wie beim
Codex-Block oben. Ist bei Codex viel frei, wird das benannt UND
gleich ein passender Kandidat vorgeschlagen („90 % der Woche
noch frei — das wäre der Moment für den großen Zweitmeinungs-
Lauf mit Ox Alpha oder Codex"). Bei Gemini/OpenRouter bleibt es
bei der Einladung ohne Zahl: „Wenn dort noch Kontingent offen
ist, wäre jetzt der Moment für die Recherche/den Zweitreviewer"
— ohne zu behaupten, wie viel das genau ist.

## The wave workflow (the heart of this skill)

The economics reward a specific rhythm:

- **The user batches work into waves**: one big message with many tasks. Claude works through
  it (subagents welcome — they cache separately at 5 min, so batch their jobs too). During
  the wave the cache stays warm by itself; short back-and-forth messages in between are cheap
  — small side-topics are *encouraged* while the main work runs.
- **After each wave, Claude writes a handoff document**: a dated Markdown file
  (`_handoff-<projekt>-YYYY-MM-DD[-b].md`) containing what was delivered, running state, open items,
  project constraints — **and the current test checklist at the bottom**. **Pre-seed every
  test item with an answer line**, ready to dictate into:

  ```
  ## T3 — Dark/light toggle inverted
  <test description>

  >>>Answer:
  ```

  (Use the user's language for the marker — e.g. `>>>Userantwort:` for a German user.)

  The user just places the cursor after the marker and speaks. An item whose answer line
  stays empty simply wasn't tested yet — that's information too, not an error.- **The user works in the handoff file with a plain text editor** (TextEdit or similar), not
  in the chat box: they answer each test point directly beneath it, and collect new ideas and
  findings in the same file — even across a long pause. Why an editor and not the terminal:
  chat inputs collapse long pastes into `[pasted text]`, so the user loses overview; in the
  editor they see the whole document. **Rule: save (⌘S) before telling Claude to read it** —
  unsaved editor changes are invisible on disk.
- **Next session starts with only the handoff** — a fresh, small context instead of 500k+,
  fully briefed, cache rebuilt once at minimum size. **Do not promise „~20k": measure it.**
  Skills, tool schemas and project rules are loaded before the user does anything — in one
  real project that floor was 82k. See „Die Startkosten einer frischen Session MITRECHNEN". Claude reads the annotated test answers
  and new ideas from the file and starts the next wave.

**Der PFAD des Handoffs steht GANZ OBEN im Dokument — als Erstes, vor allem
anderen.** Der Nutzer öffnet das Handoff im Editor; der Dateipfad ist dort
nirgends sichtbar, und für die nächste Session muss er ihn angeben. Ohne diese
Zeile sucht er ihn im Finder zusammen oder tippt ihn ab. Deshalb beginnt jedes
Handoff mit einem fertigen Übergabe-Satz zum Kopieren — eine Zeile, per
Doppelklick markierbar und direkt in die frische Session einfügbar:

```
> **Für die nächste Session — diese Zeile kopieren und einfügen:**
> `Ich habe das Handoff beantwortet: /Users/…/projekt/_handoff-projekt-2026-08-25.md`
```

Absoluter Pfad, keine Tilde-Kurzform (die muss der Agent erst auflösen), und in
Backticks, damit ein Doppelklick das Ganze fasst.

**Der Projektname gehört IN den Dateinamen — nicht nur das Datum.** Users work in
several projects/sessions in parallel, and parallel sessions produce handoffs on the
SAME day. `_handoff-2026-08-24-b.md` is then ambiguous: which project is it from?
Rule: every handoff file name carries the project name, e.g.
`_handoff-aitomat-2026-08-24-b.md`. Same for the `# Titel` line inside the file
(`# Handoff Aitomat — 24.08.2026, 23:40 (Welle 9 B)`) and for the logbook entry, so
a file that has drifted out of its folder is still identifiable. The suffix
`-b`, `-c` … stays for the second/third handoff of one day within the same project.

**Two fixed blocks at the very bottom of EVERY handoff** — after the last test item,
in this order:

1. **Freies Feld für den User.** A short closing sentence marks the end of the
   Q&A/test part and invites everything that came up outside the list — new
   instructions, ideas, tips, tasks, gripes. Example (user's language):

   ```
   ---
   ## Hiermit sind Fragen, Antworten und Tests zu Ende.

   Feld für alles Weitere — neue Anweisungen, Ideen, Tipps, Aufgaben,
   die dir eingefallen sind:

   >>>Userantwort:
   ```

   Without this field, everything not covered by a test question has no home
   and gets lost between waves.

2. **Kontext-Stand + „nächste Welle startet frisch"** as the last line of the
   document. Name the measured context size of the ending session and state
   explicitly that the next wave starts in a fresh session — this is the
   reassurance that a fat context is not a problem the user has to worry about:

   ```
   *Kontext dieser Session: ~285k. Die nächste Welle startet frisch (~20k)
   aus genau diesem Handoff — nichts geht verloren.*
   ```

   Use the actually measured number (see rule 4 above); no measurement → write
   no number, not a guessed one.

3. **Sammelbereich für die laufende Session (Yasin 25.08.2026).** Ganz zuletzt, nach
   allem anderen, eine dritte Überschrift — der Platz, an dem der Nutzer sammelt,
   WÄHREND Claude an der nächsten Welle arbeitet:

   ```
   ---
   ## Sammlung für das nächste Handoff

   Alles, was dir während der laufenden Welle einfällt, hier hinein.
   Ich rühre diesen Abschnitt nicht an — ich lese ihn nur, wenn ich das
   nächste Handoff schreibe.

   >>>
   ```

   Sein Grund, wörtlich: „Wenn ich dir ein Handoff übergeben habe, fallen mir während
   du arbeitest neue Sachen ein, die will ich sammeln … sonst muss ich ein neues
   TextEdit-Dokument öffnen, dort sammeln, und dann Copy-Paste machen."

   **Die Regel dazu ist hart: Claude schreibt NIE in ein Handoff, das der Nutzer
   gerade beschreibt.** Ein neues Handoff ist immer eine NEUE Datei; das alte bleibt
   Wort für Wort so liegen, wie er es hinterlassen hat. Genau daran hing sein zweiter
   Ärger („dann sagt das Dokument ungesicherte Änderungen, und plötzlich ist meine
   Sammlung weg"): Bearbeitet Claude eine Datei, die im Editor offen ist, kollidieren
   die Fassungen. Wird nie in die aktive Datei geschrieben, kann das nicht passieren.

   Beim Schreiben des nächsten Handoffs wird der Sammelbereich mitgelesen wie die
   Testantworten — jeder Punkt daraus wird beantwortet oder in den roten Faden
   übernommen, damit sichtbar ist, dass nichts untergegangen ist.

   **Und das VORLETZTE Handoff nochmal aufschlagen (Yasin 25.08.2026, 14:14).** Sein
   Wunsch im Wortlaut: „Vor dem neuen Handoff schauen, ob im alten Handoff was dazu
   gekommen ist, und nur diese Änderungen dann im neuen Handoff erwähnen." Der Grund ist
   praktisch: Er sammelt weiter, NACHDEM er das Handoff übergeben hat — diese Zeilen
   entstehen also erst, während Claude schon an der Welle arbeitet, und stünden sonst
   nirgends. Ablauf beim Schreiben eines neuen Handoffs:

   1. Das gerade beantwortete Handoff lesen (wie immer).
   2. **Zusätzlich das davor** — nur den Abschnitt „Sammlung für das nächste Handoff".
      Steht dort etwas, das im aktuellen Handoff nicht vorkommt, ist es neu.
   3. Diese Punkte kommen **ganz oben** ins neue Handoff, unter einer eigenen Überschrift
      wie „Aus deiner Sammlung übernommen" — je Punkt eine Zeile, was damit passiert
      (beantwortet / eingebaut / im roten Faden gelandet). Damit sieht er sofort, dass
      seine Zwischenrufe angekommen sind, ohne selbst Copy-Paste zu machen.
   4. Erst dann wandert das alte Handoff ins Archiv.

**Keep lines narrow.** Users often park the editor beside their terminal on a split
screen and bump the font size (⌘+) — long lines then wrap unpredictably or run off
screen. Hard-wrap prose at roughly **60–70 characters** per line; narrower is better.
The ONE exception: commands, paths and URLs stay on a single line however long, so a
triple-click copies them whole. After the first document, ask the user once whether
the width suits them (narrower? wider?) and remember the preference.

**Open the handoff for the user automatically.** Right after writing it, open the file in a
plain text editor so the user *sees* that the wave is done and the annotated test list is
ready — on macOS: `open -a TextEdit <file>` (always name the editor explicitly; the system
default for `.md` is often an IDE or preview app the user doesn't want). On Windows:
`notepad <file>`; on Linux: `xdg-open <file>`.

**Open as a tab, not a new window.** Users who live in this workflow accumulate many open
documents; each new floating window adds clutter. macOS controls this globally: offer once
to run `defaults write -g AppleWindowTabbingMode always` so new documents open as tabs in
the existing TextEdit window (reversible with `defaults delete -g AppleWindowTabbingMode`,
or per System Settings ▸ Desktop & Dock ▸ "Prefer tabs"). Mention that this is a
system-wide setting — if the user dislikes it, they say so and Claude reverts it.

Caveat: tabbing only joins windows on the SAME Space/desktop — if the user's main TextEdit
window lives on another Space, macOS opens a separate window anyway. Fallback after
opening: merge windows into tabs via the menu (needs Automation permission; try the
localized title first):

```bash
osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Alle Fenster zusammenführen" of menu "Fenster" of menu bar 1' \
|| osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Merge All Windows" of menu "Window" of menu bar 1'
```

If the user mentions that double-clicking `.md` files opens the wrong app, offer to fix the
default (macOS, via [duti](https://github.com/moretension/duti): `brew install duti && duti
-s com.apple.TextEdit .md all`) — many users have fought and lost this battle manually.

**Every user-facing document, not just handoffs.** Whenever Claude creates a document the
user is meant to read or react to (a plan, a report, a checklist, a draft), open it in the
text editor immediately — users rarely dig through folders for a path printed in the chat,
and an editor window is the visible signal "this is ready for you". Put a short header at
the top of each such document:

```
> You can comment directly in this file — start the line with >>> or with your
> name + timestamp, e.g. "J. Doe, 2026-08-22 14:40:".
```

(Write the header in the user's language.) The marker is a convention, not a syntax:
`>>>` is only the default. A name + timestamp prefix is even better — it says *who* answered *when*,
which matters once several annotation rounds pile up in one document. **Claude infers the
user's marker from the document itself**: whatever consistent prefix appears on the
answer lines is treated as the user's voice; don't force a format.

Tip Claude should offer once (macOS): the system has no built-in dynamic timestamp —
System Settings ▸ Keyboard ▸ Text Replacements can only insert static text. For a live
`name + date + time` snippet the user needs a text-expansion tool (any snippet app; if the
user dictates with a tool that supports snippets, that's the natural place for it).

When Claude later re-reads any of these documents, it treats the marked lines as the
user's comments/answers and runs the unsaved-changes guard below first.

**Unsaved-changes guard (macOS).** Claude reads files from disk, so unsaved editor changes
are invisible — but on macOS, Claude can check for them. Before reading an annotated
handoff, ask TextEdit whether the document is open with unsaved changes:

```bash
osascript -e 'tell application "TextEdit" to get {name, modified} of documents'
```

If the handoff shows `modified: true`, tell the user: *"Your handoff has unsaved changes —
shall I take them over?"* and on confirmation either save it for them
(`osascript -e 'tell application "TextEdit" to save (first document whose name is "<file>")'`)
or read the live window text directly
(`… to get text of (first document whose name is "<file>")`). Requires macOS automation
permission for TextEdit (one-time prompt). This turns the ⌘S rule from a hard requirement
into a safety net — but still teach ⌘S as the habit, since the guard only sees documents
that are open in TextEdit.

**Open documents LARGE — fix the font default, not the zoom.** Users bump every freshly
opened document with ⌘+ because TextEdit opens plain text tiny (default 11 pt) — and
TextEdit's per-window zoom is NOT scriptable, so Claude cannot read or restore it when
reopening a document. The durable lever is TextEdit's default plain-text font size:

```bash
defaults read com.apple.TextEdit NSFontSize          # unset = 11 pt
defaults write com.apple.TextEdit NSFontSize 18
defaults write com.apple.TextEdit NSFixedPitchFontSize 18
```

Offer this once (pick ~18 pt, adjust on feedback; reversible with `defaults delete`).
Documents opened AFTER the change come up large natively — no zooming. Already-open
windows keep their old size until the user quits and reopens TextEdit (never quit it
for them). This pairs with the narrow-line rule: big font + ~60–70-char lines is exactly
the split-screen setup the wave workflow assumes. When closing + reopening a document to
reload it from disk (TextEdit does not live-reload), warn the user once that per-window
zoom is lost — the font default is what makes that painless.

**Reload edited documents in the editor — every time, unprompted.** TextEdit does not
live-reload files changed on disk. Whenever Claude (or a subagent) edits a document the
user has open, run the unsaved-changes guard on exactly those files, then: unmodified →
close and reopen it so the user sees the new version; modified → do NOT close — tell the
user which of their unsaved edits collide, offer to merge them into the new version, and
only reload after they confirm. Skipping this leaves the user reading a stale document
while believing it is current — worse than any extra window shuffle.

**Tip for lost handoffs** (tell the user once): if they closed the document and can't find
the file, TextEdit ▸ **File ▸ Open Recent** brings back any
recently closed handoff without hunting through Finder.

**Carry the old test list forward.** When writing a NEW handoff while an older one exists:
read the old handoff first and check its answer lines. Answered items get incorporated —
and the new handoff says so explicitly per item ("Your T1 answer from the previous list is
taken into account: <one-line summary> — correct?"), so the user can veto a misreading.
Unanswered items and items whose fix needs a re-test move into the new list unchanged
(marked as carried over). The old handoff stays untouched as the record; only the newest
one is the active working document.

**Das alte Handoff schließen — nur nach einer Prüfung IM SELBEN Aufruf (Yasin
25.08.2026, 14:21 — ein echter Datenverlust).** Sein Satz: „Vorhin habe ich in der alten
Handoff-Liste, die du automatisch geschlossen hast, schon was Neues reingeschrieben
gehabt … aber das ist jetzt verloren gegangen, weil du es ja geschlossen hast." Genau so
war es: Der Ungespeichert-Wächter war Minuten vorher gelaufen, das Schließen kam später,
und dazwischen hatte er weitergeschrieben. Eine Prüfung, die nicht unmittelbar vor der
Aktion steht, ist wertlos.

**NACHGESCHÄRFT am 26.08.2026, 14:07 — Claude schließt das alte Handoff GAR NICHT
mehr.** Yasins Begründung im Wortlaut: „Wenn ich unten was reinschreibe und das noch
nicht gespeichert habe, und du schließt dann das alte Handoff, nachdem du gearbeitet
hast — dann kannst du es ja gar nicht schließen, wenn ich da noch ungesicherte
Änderungen drin habe. Deswegen würde ich fast sagen: das alte Handoff gar nicht
schließen, sondern offen lassen, dass der User das schließt."

Er hat recht, und der Grund ist grundsätzlicher als der Datenverlust vom 25.08.: Der
Sammelbereich ist ausdrücklich dafür da, dass er WÄHREND der laufenden Welle
weiterschreibt. Genau in dem Moment, in dem Claude fertig wird und aufräumen möchte,
ist die Wahrscheinlichkeit am höchsten, dass dort ungespeicherter Text steht. Ein
Aufräumschritt, der ausgerechnet dann zuschlägt, kann nur verlieren.

Die Regel ist deshalb jetzt:

1. **Das alte Handoff bleibt offen. Punkt.** Claude schließt es nicht, speichert es
   nicht, rührt es nicht an. Der Nutzer schließt es selbst, wenn er fertig ist.
2. **Vor dem Schreiben des neuen Handoffs wird sein Inhalt trotzdem gelesen** — inklusive
   Sammelbereich, und zwar über den Ungespeichert-Wächter, damit auch ungespeicherte
   Zeilen ankommen (`get text of (first document whose name is "…")`). Lesen ist
   gefahrlos; nur Schließen und Schreiben sind es nicht.
3. **Das neue Handoff ist IMMER eine neue Datei** mit neuem Namen. Damit gibt es
   niemals eine Kollision zwischen Claudes Fassung und dem, was im Editor offen liegt.
4. **Archiviert (`mv`) wird erst, wenn der Nutzer das Dokument geschlossen hat** — oder
   gar nicht in dieser Welle. Ein Handoff, das noch offen im Editor liegt, wird nicht
   verschoben; das neue Handoff notiert stattdessen in einer Zeile, dass die
   Archivierung noch aussteht.
5. **Schließen + neu öffnen bleibt genau EINE Ausnahme:** wenn Claude selbst die Datei
   verändert hat, die der Nutzer offen hat (sonst liest er eine veraltete Fassung).
   Auch dann gilt die Prüfung im SELBEN Aufruf, und bei `modified: true` wird NICHT
   geschlossen, sondern gefragt.

Im Zweifel gilt immer: **lieber ein Fenster zu viel offen als eine Zeile des Nutzers weg.**

When Claude finishes a handoff it should say so and explain the loop to the user once:
*"Handoff written, your test list is at the bottom. Answer under the test points, add new
ideas, ⌘S — and give the file to a fresh session (or to me, if you're still in the window)."*

## The economics, honestly (teach this to the user once)

- Every request inside a warm cache re-reads the WHOLE prefix at ~1/10 price. At 220k
  context a short question costs ~22k full-price token equivalents; ten such exchanges
  ≈ one full context read. The user's instinct "batch my messages" is directionally right —
- — BUT the user's messages are a rounding error. Claude's own tool loop dominates:
  every file read, every command is a request that re-reads the prefix. A working day
  can be 500+ requests, of which the user sent ~20. The lever is therefore NOT fewer
  user messages; it is a SMALL context while the many work-steps run. (This is also why
  subagents pay off: the heavy lifting happens in their separate small contexts.)
- Concrete arithmetic for the sweetspot: a 300-step wave at 220k context ≈ 300 × 22k
  ≈ 6.6M equivalents; the same wave in a fresh ~30k session ≈ 0.9M. A fresh session's
  rebuild is cheap because the new prefix is small — the expensive thing is never the
  handoff, it is running a big wave on top of a fat context.
- Rule of thumb that follows: hand off BEFORE each big new wave once context has grown
  past ~150–250k — not at a fixed percentage, and not after every wave regardless of
  size. **Sweetspot: hand off around ~200k, hard ceiling well before 400k.** Below ~50k,
  short questions are near-free — chat freely; past ~150k, batch conversation too
  (one structured message per wave). Every message resets the 1-hour timer either way.

## When to stay vs. when to hand off

| Situation | Recommendation |
|---|---|
| Pause < 1 h ahead, context < 150k | Just continue; optionally keep warm on request (max ~3 cycles) |
| Pause < 1 h, context 150–400k | Continue, but write the handoff now as insurance |
| Big build wave ahead, context > ~200k | Hand off FIRST, then start the wave fresh |
| Only talk/small edits ahead, context < ~300k | Stay — talking on a fat context is cheap |
| Context > 400k | Handoff + fresh session — say so proactively |
| Pause > 1 h (cache gone anyway) | Never rebuild the giant context: handoff + fresh session |
| Mid-session model/effort change wanted | Warn: full cache rebuild; suggest doing it at the next fresh session instead |

## Writing the handoff well (rules adopted from Matt Pocock's /handoff)

- **Reference, don't copy.** Specs, plans, commits, diffs and issues that are already written
  down get linked by path or URL — never pasted into the handoff. Keeps the file small and
  the settled detail in ONE place instead of two that drift.
- **Redact secrets** (keys, tokens, passwords) before writing the file.
- **Name suggested skills** for the next session — what the fresh agent should reach for.
- **Landkarte statt nur Restliste (Yasin 25.08.2026).** Der „Offen (nächste Wellen)"-Block
  am Ende ist gut, aber er sagt nur, was NOCH kommt — nicht, wo das Projektwissen liegt.
  Jedes Handoff bekommt deshalb direkt davor einen kurzen Block **„Hauptdokumente"**:
  die 3–6 Dateien, die den Stand wirklich tragen (Roadmap, Projekt-Status, Übersicht
  offener Themen, aktuelle Konzeptpapiere), je mit absolutem Pfad und EINER Zeile, was
  drinsteht und wie frisch es ist. Beispiel:

  ```
  ## Hauptdokumente (wo was steht)

  - `/Users/…/projekt/ROADMAP-MASTER.md` — Fahrplan aller Wellen (Stand 23.08.)
  - `/Users/…/projekt/PROJEKT-STATUS.md` — was fertig/in Arbeit ist (Stand 25.08.)
  - `/Users/…/projekt/UEBERSICHT-OFFENE-THEMEN.md` — Themenspeicher, gröber als
    die Restliste unten
  ```

  Regeln: nur Dokumente aufführen, die WIRKLICH existieren (vorher prüfen), veraltete
  ausdrücklich als veraltet markieren statt still mitzuschleppen, und nie den Inhalt
  hineinkopieren — der Pfad ist der Sinn der Sache („Reference, don't copy").
- **Der untere Teil ist ein roter Faden, keine Stichwortliste (Yasin 25.08.2026).**
  Sein Wunsch: „dass man da unten nicht nur die Fragen und Tests hat, sondern einen roten
  Faden sieht, roadmapartig — was als nächste Welle kommt, was die übernächste, kurz, mit
  ein paar Details, damit man sich erinnert und motiviert ist, noch was dazuzuschreiben."

  Also: Die Restliste `Offen (nächste Wellen)` wird zu einem kurzen **Fahrplan mit
  Antwortfeldern**. Für die nächsten zwei bis drei Wellen je ein Absatz — was drankommt,
  warum, und ein oder zwei Details, die den Gedanken wieder wachrufen. Danach dieselbe
  Einladung wie bei den Tests:

  ```
  ## Der rote Faden — was als Nächstes drankommt

  ### Nächste Welle: Live-Transkript unterm HUD
  Der Text soll schon während der Aufnahme mitlaufen, alle 5 Minuten
  ein Zwischenstand. Hängt an deinem 5-Stunden-Video-Plan; die
  Audio-Seite ist seit Welle 10 gesichert, es fehlt nur der Text.

  >>>Hast du dazu noch was anzumerken?

  ### Übernächste Welle: Vorlesen Welle 2
  Rechtsklick-Dienst, Vorlese-Zustand im HUD, Tempo, weitere Stimmen laden.

  >>>Hast du dazu noch was anzumerken?
  ```

  Der Rest (die lange Aufzählung aller offenen Punkte) bleibt darunter als
  Themenspeicher stehen — komprimiert, ohne Antwortfelder. Der Fahrplan ist die
  Einladung zum Mitdenken, die Liste ist das Gedächtnis.
- **Alte Handoffs archivieren, nie löschen (Yasin 25.08.2026).** Wenn ein neues Handoff
  geschrieben ist und seine Antworten eingearbeitet sind, wandert das VORHERIGE in einen
  Unterordner `handoff-archiv/` desselben Projekts (anlegen, falls er fehlt):

  ```bash
  mkdir -p "<projekt>/handoff-archiv"
  mv "<projekt>/_handoff-projekt-2026-08-24-b.md" "<projekt>/handoff-archiv/"
  ```

  Verschieben, nicht löschen — der Nutzer räumt selbst auf, wenn er will. Im Projektordner
  liegt damit immer nur EIN aktives Handoff, und die Frage „welches ist das richtige?"
  stellt sich nicht mehr. Das neue Handoff nennt den Archivordner in einer Zeile, damit
  der Weg zurück sichtbar bleibt. Nur archivieren, wenn das alte Dokument keine unbearbeiteten
  Antworten mehr enthält (sonst bleibt es liegen, mit Begründung im neuen Handoff).
- One deliberate difference: Pocock writes handoffs to the temp directory (transit document)
  and recommends `/compact` for same-directory continuation. This skill writes them **into
  the project** (dated, part of the working rhythm, the user annotates them) and prefers
  handoff + fresh session over `/compact` past the context threshold — on subscription
  plans, `/compact` keeps the huge expensive prefix alive; a fresh ~20k session does not.

## Einen Cache-Neuaufbau ERKENNEN und ansagen (Yasin 25.08.2026)

Sein Wunsch: „Wenn sich so ein Cache neu aufbaut, bekommst du das mit und kannst du das
dem User dann sagen — dass der Cache gerade neu aufgebaut hat, weil er eben zu spät war
oder was auch immer der Grund war."

**KORREKTUR vom 26.08.2026 — es GIBT ein Signal, und zwar ein hartes.** Hier stand
früher „es gibt kein Signal, das einen Cache-Miss meldet". Das war falsch: Jede Zeile der
Session-Datei trägt `cache_creation_input_tokens` (zum 2×-Preis geschrieben) neben
`cache_read_input_tokens` (zum 0,1×-Preis gelesen). **Das Verhältnis der beiden Summen
IST die Trefferquote.**

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
u=[(json.loads(l).get('message') or {}).get('usage') for l in open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines() if '\"usage\"' in l]
u=[x for x in u if x]
cr=sum(x.get('cache_read_input_tokens',0) for x in u); cw=sum(x.get('cache_creation_input_tokens',0) for x in u)
gross=[x.get('cache_creation_input_tokens',0) for x in u if x.get('cache_creation_input_tokens',0)>20000]
print(f'{len(u)} Anfragen · gelesen {cr/1000:.0f}k · geschrieben {cw/1000:.0f}k ({cw/max(1,cr)*100:.1f} %) · Grossschriften: {len(gross)}')"
```

Deutung: **unter ~10 % geschrieben/gelesen = der Cache war warm.** Einzelne Zeilen mit
großer Neuschrift sind fast immer NACHTRÄGE (der Verlauf wächst, der neue Teil wird
einmal geschrieben), nicht Neuaufbauten. Ein echter Neuaufbau sieht anders aus: viel
Schrift bei fast keinem Lesen.

**Warum das wichtig ist — es räumt das häufigste Missverständnis ab.** Yasin fragte am
25.08. und nochmal am 26.08.: „269 Anfragen — heißt das, du hast 269-mal den Cache neu
aufgebaut?" Nein. Und ohne diese Messung war die Antwort eine bloße Behauptung. Mit ihr
ist sie ein Beleg: in der gemessenen Session 22.171k gelesen gegen 562k geschrieben —
**2,5 %**, bei 147 Anfragen nur 6 mit nennenswerter Neuschrift.

**Was weiterhin NICHT geht:** die URSACHE eines Misses aus den Daten ablesen. Ob die
Pause zu lang war, ein Modellwechsel dazwischenkam oder serverseitig geräumt wurde, sagt
die Datei nicht. Dafür gilt die Ableitung unten — und ohne feststehende Ursache wird
nichts behauptet.

**Die drei Kostenposten, die in jede Erklärung gehören** (der dritte wurde lange
unterschlagen): Cache-Lesen ×0,1 · Cache-Schreiben ×2 · **eigene Ausgabe ×5**. In der
gemessenen Session machte die Ausgabe fast ein Viertel der Gesamtkosten aus. Lange
Antworten und ausführliche Handoffs sind ihr Geld wert, aber sie sind nicht gratis — wer
nur über Kontextgröße redet, erklärt dem Nutzer nur zwei Drittel der Rechnung.

**Und eine Regel für Claude selbst:** Jede Zwischenmeldung („Agent X ist fertig") ist eine
VOLLE Anfrage und kostet so viel wie eine Nutzernachricht — bei 200k Kontext rund 20k
Äquivalente. Landen mehrere Agenten kurz hintereinander, werden ihre Meldungen
zusammengefasst statt einzeln abgesetzt.

**Was geht — und zwar sicher:** die Lücke messen. Ein Cache-Miss durch Zeitablauf ist die
mit Abstand häufigste Ursache, und er ist aus zwei `date`-Lesungen ableitbar:

1. Bei jeder Antwort ohnehin `date` lesen (Regel 1 oben). Die letzte gelesene Zeit ist
   damit bekannt — sie steht im eigenen vorherigen Text.
2. Beim nächsten Turn erneut lesen. Differenz > 60 Minuten (bzw. > 5 Minuten, wenn die
   Session nachweislich im 5-Minuten-Modus läuft) ⇒ der Cache war weg, der aktuelle
   Turn hat ihn neu aufgebaut.

Dann EINMAL, beiläufig, mit Grund und Zahl:

> „Nebenbei: zwischen deiner letzten Nachricht und dieser lagen 1 h 40 — der Cache ist
> in der Zeit abgelaufen und mit diesem Turn neu aufgebaut worden. Kein Beinbruch, nur
> damit du weißt, warum die Antwort etwas teurer war als sonst."

Weitere Ursachen, die Claude ebenfalls SICHER weiß, weil es die eigene Handlung war oder
im Verlauf steht — auch die dürfen benannt werden:
- ein Modell- oder Effort-Wechsel mitten in der Session,
- eine Änderung an CLAUDE.md / am System-Prompt während der Sitzung,
- ein MCP-Server, der neu gestartet ist (sichtbar an einer Fehlermeldung im Verlauf).

Ursachen, die Claude NICHT sehen kann (Plan-Limit erreicht → 5-Minuten-TTL, serverseitige
Räumung), werden nicht geraten. Steht keine dieser Ursachen fest, gilt: nichts sagen.

Zwei Regeln zum Ton: **einmal pro Ereignis, nicht als Dauerwarnung**, und nie als
Vorwurf — der Nutzer hat eine Pause gemacht, das ist sein gutes Recht. Der Satz dient der
Erklärung („warum ging da gerade Kontingent weg"), nicht der Erziehung. In den Logbuch-
Eintrag gehört derselbe Befund als Zeile mit Ursache und geschätzter Verschwendung.

## Long agent runs, the user as bottleneck, Fable low (Yasin 28.08.2026)

Drei Regeln, die aus der Welle vom 27./28.08.2026 stammen. Alle drei haben
denselben Kern: **Die teuerste Ressource ist nicht das Modell, sondern der
Mensch, der auf es wartet — und jede Anfrage, die nur stattfindet, weil jemand
„fertig" melden will.**

### a) Agents running longer than an hour deliver into a FILE

Ein Subagent, dessen Arbeit voraussichtlich **länger als eine Stunde** dauert
(Recherche, Review mit vielen Quellen, große Umbauten), meldet sein Ergebnis
nicht in den Chat, sondern **schreibt es in eine Datei** — Konvention:
`docs/reviews/<JJJJ-MM-TT>-<thema>.md` (oder der im Projekt übliche Ort).

Warum: Wenn der Agent nach 90 Minuten fertig wird, ist die Hauptsitzung
entweder längst in der Pause (Cache kalt, Fertigmeldung löst einen
Neuaufbau aus) oder sie wartet aktiv und verbrennt dabei Anfragen. Beides
ist teurer als eine Datei, die einfach da liegt.

Ablauf:

1. **Beim Start** sagt der Orchestrator dem Agenten den Zielpfad und den
   Auftrag: „Schreib das Ergebnis nach `docs/reviews/2026-08-28-x.md`.
   Melde dich erst, wenn die Datei vollständig ist; die Meldung darf nur
   den Pfad und zwei Sätze enthalten."
2. **Im Handoff** trägt der Orchestrator eine Zeile ein, welche Datei von
   welchem Agenten **erwartet** wird:

   ```
   ## Erwartete Agenten-Ergebnisse
   - [ ] docs/reviews/2026-08-28-tageszeit-und-kontingente.md (Recherche-Agent, gestartet 17:02)
   - [ ] docs/reviews/2026-08-28-skills-mcp-ballast.md (Analyse-Agent, gestartet 17:05)
   ```

3. **Die NÄCHSTE Session** prüft beim Lesen des Handoffs als Erstes, ob die
   erwarteten Dateien existieren (`ls docs/reviews/`), hakt sie ab und liest
   sie im Zuge der Handoff-Lektüre — **in derselben ersten Anfrage**. So kostet
   das Fertigwerden des Agenten keine eigene Anfrage, keinen Neuaufbau und
   keine Wartezeit.
4. Fehlt eine erwartete Datei, steht das im ersten Statusblock der neuen
   Session („Review-Datei X fehlt — Agent abgebrochen?"), statt dass es
   stillschweigend untergeht.

Ergebnis in Zahlen: Zwei Reviews à 200–600 Zeilen kamen so am 27.08. in
die Folgesitzung — als Teil der ersten Anfrage statt als zwei zusätzliche
Fertigmeldungen in eine 220k-Session (2 × 22k Äquivalente gespart, plus
kein Neuaufbau nach der Nachtpause).

### b) The user is the bottleneck — cut waves so they run through

Yasin, 28.08.2026: Der Mensch kann nicht dauernd am Terminal sitzen; jede
Rückfrage, die eine Welle anhält, kostet Stunden Echtzeit, nicht Sekunden.
Deshalb:

- **Wellen so zuschneiden, dass möglichst viel OHNE Rückfrage läuft.**
  Wenn ein Auftrag zwei Auslegungen hat, die beide vertretbar sind: die
  wahrscheinlichere nehmen, im Handoff kennzeichnen („angenommen: X; falls
  Y gemeint war, ist die Änderung in Datei Z rückgängig zu machen"), und
  weiterarbeiten. Anhalten nur, wenn eine falsche Annahme Daten zerstört,
  Geld kostet oder nach außen wirkt (Push, Mail, Bestellung).
- **Fragen werden GESAMMELT ins Handoff geschrieben**, nicht einzeln in
  den Chat. Ein Abschnitt `## Fragen an dich` mit vorbereiteten
  Antwortzeilen (`>>>Antwort:`), die der Nutzer im Editor beantwortet, wann
  er will. Eine Frage im Chat blockiert; zehn Fragen im Handoff blockieren
  nichts.
- **Agenten bekommen mehrere Aufgaben gebündelt** und melden sich erst,
  wenn ALLES fertig ist — nicht nach jeder Teilaufgabe. Drei Aufträge an
  einen Agenten sind eine Fertigmeldung; drei Agenten mit je einem Auftrag
  sind drei Anfragen im Hauptkontext. Bündeln, solange die Aufgaben sich
  nicht gegenseitig blockieren oder die Laufzeit über eine Stunde treibt
  (dann greift Regel a).
- **Der Auftrag an den Agenten enthält den Vertrag:** was das Ergebnis
  ist, wohin es geht, wie lang der Bericht sein darf, und ausdrücklich
  „keine Rückfragen — entscheide selbst und dokumentiere die Annahme".

### c) Fable 5 as agent model: ALWAYS effort low

Nutzerregel (Yasin): Wird Fable 5 als Subagenten-Modell eingesetzt, dann
**ausschließlich mit Effort low**. Grund: Fable low ist schnell und billig
genug für Mechanik, Recherche und Textarbeit; der höhere Effort frisst
Zeit und Kontingent, ohne dass die Ergebnisse in diesen Aufgaben besser
werden. Für Aufgaben, die wirklich hohen Effort brauchen (Design-
entscheidungen, Sicherheits-Review), ein anderes Modell wählen (Opus 5,
oder Codex/GPT-5.6 als Zweitmeinung) — nicht Fable hochdrehen.

Beim Start eines Agenten steht Modell und Effort sichtbar in der
Beschreibung, damit der Nutzer es im Terminal sieht:

```
gut:  "Fable/low · Kostentabelle aus Session-JSONL bauen"
```

## Honesty rules

- There is no background timer: Claude only acts when a request arrives. That is exactly why
  the handoff is written *proactively at the end of a wave*, not "when the hour is nearly up".
- Cost claims should be shown as arithmetic when it matters (cache-write vs. re-read pricing),
  not asserted.
- Ein Cache-Neuaufbau wird gemeldet, wenn er ABLEITBAR ist (s. Abschnitt oben) — nie geraten.

## The logbook (self-observation, optional but recommended)

Keep a running log at `~/.claude/warm-handoff-log.md`. **Append one line at every handoff**
(and whenever a cache-relevant event happens), format:

```
| 22.08.2026 14:40 | ctx 85k | 2 waves | rebuilds: 1 (pause 90min, no handoff) | est. waste ~60k tokens |
```

Log-worthy events: session start/end context size, waves completed, every cache rebuild
**with its cause** (pause > 1h, mid-session model/effort switch, MCP restart, prefix change),
warnings the user overrode, and a rough token-waste estimate for each avoidable rebuild.

**Every ~50 entries:** write a short summary block at the top — recurring patterns and
concrete recommendations ("6 of 8 sessions lost the cache to a >1h pause without a handoff,
costing roughly X — schedule the handoff before breaks"; "effort was switched mid-session
3 times despite warnings"). Then continue logging below it.

Honest limits: there is no background telemetry — the log only covers sessions where this
skill is active, and waste numbers are estimates, clearly labeled as such. That is enough
for pattern-spotting, which is the point.

## Make it always-on (recommended setup)

Add one line to your global `~/.claude/CLAUDE.md` (or the project's `CLAUDE.md`):

```
At the start of every session, invoke the warm-handoff skill.
```

Then you never need to type `/warm-handoff` — the session opens with the timestamp habit,
the thresholds, and the wave workflow already active.

## Vier Regeln aus dem Handoff-Test vom 29.08.2026 (Yasin)

### a) Die Sammlung wird WÖRTLICH kopiert — und im selben Aufruf gelesen

Was passiert ist: Die Session vom 28.08. las die „Sammlung für das
nächste Handoff" um ~16:45, arbeitete dann 3 Stunden, und schrieb um
19:45 das neue Handoff — **ohne die Sammlung erneut zu lesen.** Alles,
was Yasin zwischen 18:53 und 19:42 dort eingetragen hatte (acht
Punkte: Mikro-Warnung, Systemaudio-Qualität, HUD-Transparenz,
Schlafmodus-Optik, Filter-Reset …), fehlte im neuen Handoff. Er
musste es am nächsten Tag selbst hineinkopieren und fragte zu Recht:
„Hast du das mitgenommen? Ich bin mir unsicher."

Zwei Regeln, beide hart:

1. **Die Sammlung wird UNMITTELBAR vor dem Schreiben des neuen
   Handoffs gelesen** — im selben Werkzeugaufruf wie der
   Ungespeichert-Wächter, nicht Stunden vorher. Eine Lesung, die
   nicht direkt vor dem Schreiben steht, ist wertlos (derselbe
   Grundsatz wie beim Schließen alter Handoffs, 25.08.).
2. **Sie wird EINS ZU EINS kopiert, nicht umgeschrieben.** Yasin,
   wörtlich (29.08., 13:22): „Wenn du das wieder umschreibst, dann
   weiß ich nicht mehr, ob es die letzte Sammlung ist." Ganz oben
   im neuen Handoff steht deshalb ein Block:

   ```
   # Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)

   > Kopiert aus `_handoff-…-28-b.md`, Abschnitt „Sammlung", am
   > 29.08.2026 13:40 — inklusive ungespeicherter Zeilen aus dem
   > offenen TextEdit-Fenster. Unverändert; meine Antworten dazu
   > stehen direkt darunter.

   [Sammlung wörtlich, Zeile für Zeile]

   ## Was ich daraus gemacht habe
   - 19:29 Transparenz statt Farbintensität → gebaut (T4)
   - …
   ```

   Erst die Kopie (damit der Nutzer den Abgleich SEHEN kann), dann
   die Zuordnung. Zusammenfassen ist erlaubt — aber nur ZUSÄTZLICH
   zur wörtlichen Kopie, nie statt ihrer.

### b) Codex nach Kontogröße einsetzen — kleines Konto = nur Qualitätssicherung

Yasin, 28.08. 20:08, nachdem Codex im 5-Stunden-Limit hing und der
Vorschlag lautete, ihm ab 23:05 die Hauptarbeit zu geben: „Nein,
ich bin mit dem Vorschlag nicht einverstanden. Wenn Codex so knapp
ist, dann sollten wir Codex nur für wichtige Qualitätsmanagement-
Sachen nutzen — der soll dann nur prüfen — und nicht, dass wir zwei,
drei Stunden warten, bis der wieder Kontingent hat. Ich habe nur
einen Zwanzig-Dollar-Account bei Codex. Nicht versuchen, jedes
letzte Tröpfchen Token auszusaugen."

Der Abschnitt „Bezahltes Kontingent ausnutzen" oben bleibt richtig —
aber er gilt für das Kontingent, das man HAT. Die Regel wird damit
kontoabhängig:

| Codex-Konto | Einsatz |
|---|---|
| Klein (Plus, ~20 $/Monat: enges 5h-Fenster) | **Nur Prüfarbeit:** Code-Review, Zweitmeinung, Testläufe, Abnahme. Keine Bau-Aufträge, keine Nachtschichten, kein „ab 23:05 weitermachen". Reicht das Fenster nicht, macht Claude (oder ein Opus-Subagent) die Arbeit — nicht warten. |
| Groß (Pro/Team, weites Fenster) | Wie bisher: großzügig einsetzen, auch für Umbauten und lange Analysen. |

Warum das nicht im Widerspruch zu „Kontingent ausnutzen" steht:
Beim kleinen Konto ist das 5-Stunden-Fenster der Engpass, nicht die
Woche. Ein Bau-Auftrag frisst es in einer Stunde, und dann fehlt
Codex genau dort, wo er den größten Wert hat — als ANDERE Architektur,
die Claudes Fehler sieht. Prüfarbeit ist kurz, gezielt und wertvoll;
Hauptarbeit kann Claude selbst. Wer das Konto vergrößert, wechselt
die Zeile — der Skill fragt beim Setup einmal, welches Konto
vorliegt, und merkt es sich.

### c) Das Ende-Feld muss auffallen — Markdown hilft im Editor nicht

Yasin, 28.08. 20:00: „Kann man denn nicht Buchstaben größer machen?
Bei MD geht das nicht, gell. Das ‚Hiermit sind Fragen … zu Ende'
müsste eigentlich auffälliger sein."

Richtig: In TextEdit ist eine `##`-Überschrift nur zwei Rauten vor
normalem Text. Was im Klartext auffällt, sind **Linien und Leerraum**,
nicht Markup. Die beiden Schluss-Blöcke (Ende-Feld, Sammelbereich)
bekommen deshalb eine Bannerzeile:

```
═══════════════════════════════════════════════════════════
   ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
   Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
═══════════════════════════════════════════════════════════

>>>Userantwort:
```

Großbuchstaben, Doppellinie, drei Leerzeilen davor. Das funktioniert
in jedem Editor ohne Rendering.

### d) „Welche Agenten arbeiten gerade?" — was der Host zeigt und was nicht

Yasins Frage (28.08. 18:53, Screenshot der Statuszeile): ob unten
stehen kann, WELCHE Agenten arbeiten. Ehrliche Antwort:

- **Was sichtbar ist:** Claude Code listet laufende Hintergrund-
  Agenten mit ihrer Kurzbeschreibung unter der Eingabezeile („← for
  agents"). Deshalb gehört Modell + Denktiefe in diese Beschreibung
  (Regel vom 26.08.: „Opus5/high · Thema") — dann steht dort alles.
- **Was NICHT geht:** Die eigene Statuszeile (`ctx 17% | 7d:10%`)
  bekommt vom Host keine Agentenliste übergeben; sie kann sie nicht
  anzeigen. Wer sie dort will, muss die Agenten-Anzeige des Hosts
  aufklappen.
- **Die eine Ansage im Chat beim Start der Flotte** bleibt der
  vollständige Überblick: wie viele Agenten, welches Modell, welches
  Arbeitspaket. Danach Funkstille.

## Leitsatz — der ganze Skill in einem Satz (Yasin 29.08.2026, 14:01)

> **Handoff → frische Session → Handoff.** Der Nutzer sammelt über
> Stunden alles in EIN Handoff (Antworten, Ideen, Kritik), startet
> eine neue Session, der Agent arbeitet alles durch und schreibt das
> nächste Handoff — und dazwischen immer eine frische Session.

Warum das der sparsamste Rhythmus ist: Die Kosten sitzen in den
Anfragen (jede liest den ganzen Verlauf), nicht in den Nachrichten
des Nutzers. Also: Hauptkontext klein halten (frische Session je
Welle), Arbeit in wenige Subagenten mit MEHREREN Aufgaben (wenige
Berichte = wenige Anfragen), und das Handoff ausführlich — mit
Kostentabelle, Testliste, rotem Faden und der wörtlichen Sammlung —,
weil es einen ganzen Kontext ersetzt. Ein dünnes Handoff spart
nichts; es verschiebt die Kosten in Rückfragen.

Drei Details, die dazugehören (alle vom 29.08.2026):

- **Tab-Vorschläge des Terminals sind Anfragen.** Claude Code blendet
  graue Vorschlagszeilen ein; wer sie mit Tab übernimmt und abschickt,
  löst eine volle Anfrage aus (Kontext × 0,1). Die Zeile lässt sich
  nicht beschriften — sie kommt vom Programm. Nur nutzen, wenn man
  den Vorschlag wirklich will.
- **Agenten-Fertigmeldungen sind Anfragen des Programms, nicht des
  Agenten.** Jede „Agent X finished"-Meldung weckt den Hauptagenten —
  das ist eine Anfrage, auch wenn er schweigt. Sein Einzeiler dazu
  („zwei von sieben durch") kostet nur ~50 Token Ausgabe extra. Was
  Anfragen SPART, ist nicht Schweigen, sondern weniger, größere
  Agenten (drei Aufgaben in einem = eine Fertigmeldung).
- **Der Sammelbereich trägt den Pfad seines Handoffs** in der
  Bannerzeile („aus: /Users/…/_handoff-projekt-2026-08-29.md"), damit
  bei mehreren offenen Handoffs klar ist, welche Sammlung das ist —
  und der Pfad zum Kopieren bereitsteht.

## Welle 23 — günstig in Token, aber 2 Std. 20 durch seriellen Schwanz (29.08.2026)

Welle 23 (Aitomat, Merge-Bericht siehe Commit `1f308c86`) lief mit
wenigen, größeren Agenten nach der alten Regel oben („drei Aufgaben in
einem = eine Fertigmeldung"). Ergebnis: **günstig gemessen** (wenig
Hauptkontext verbraucht, wenige Fertigmeldungen), aber **2 Stunden 20
Minuten Wanduhrzeit**, weil die Agenten nicht wirklich gleichzeitig
liefen — mehrere Aufgaben in einem Agenten heißt, der Agent arbeitet
sie INTERN nacheinander ab, und wenn ein zweiter Wächter-Agent auf das
Ergebnis des ersten wartet, bevor er seine eigenen Arbeiter startet,
entsteht ein serieller Schwanz aus Wartezeiten, den keine Kostenzeile
zeigt. Yasin wartete dabei ~3 Stunden auf ein Ergebnis, das inhaltlich
in Bruchteilen der Zeit fertig hätte sein können.

Die Lehre: **Tokenkosten und Wanduhrzeit sind zwei verschiedene
Achsen.** Weniger/größere Agenten sparen Anfragen (Achse 1), aber
bündeln Arbeit seriell in der Wanduhrzeit (Achse 2) — genau dann teuer,
wenn der Nutzer wartet statt nebenher zu arbeiten. Die Regel wird
deshalb geschärft, ohne die alte Erkenntnis zu verwerfen:

- **Ein Arbeits-Agent = EIN Auftrag, ~30 Minuten** (statt ~40 Minuten /
  2–3 Aufgaben). Ein einziger fokussierter Auftrag lässt sich schneller
  abschließen UND schneller mergen, ohne dass die interne Abarbeitung
  mehrerer Aufgaben im selben Agenten eine unsichtbare Warteschlange
  erzeugt.
- **Der Wächter startet ALLE Arbeiter in einer einzigen Nachricht**
  gleichzeitig, nie nacheinander — das serielle Anstoßen war die
  eigentliche Ursache des Schwanzes in Welle 23, nicht die Anzahl der
  Agenten selbst.
- **Jeder Arbeiter zieht zuerst den aktuellen Branch-Tip**, bevor er
  etwas anfasst — bei paralleler statt serieller Ausführung ist eine
  veraltete Basis sonst wahrscheinlicher, weil mehrere Arbeiter
  gleichzeitig vom selben Stand abzweigen.
- **Merges sofort bei Landung, nicht gesammelt** — wer auf den
  letzten Arbeiter wartet, um alle Merges auf einmal zu machen, baut
  den seriellen Schwanz am Ende wieder ein.
- **Volle Testsuite nur einmal, ganz am Ende**, gegen das gemergte
  Ergebnis — nicht nach jedem einzelnen Merge, sonst multipliziert sich
  die Laufzeit der Suite mit der Zahl der Arbeiter.
- **Der Wächter schreibt nach 60 Minuten einen Zwischenstand**, falls
  die Welle noch läuft, und **das Handoff startet auch ohne fertigen
  Wächter** — in Welle 23 hätte ein Zwischenstand nach einer Stunde dem
  Nutzer gezeigt, dass er nicht auf ein hängendes System wartet.

Kurz: schnell UND günstig braucht beides — kleine Aufträge UND
echte Gleichzeitigkeit beim Start. Eines allein reicht nicht.

## 29.08.2026, 23:35 — Der Rechner-Absturz

Welle 24: Der Wächter startete 12 Arbeiter gleichzeitig, jeder in eigenem
Worktree mit eigenem Kaltbuild. 400+ swift-frontend-Prozesse, Load ~70 auf
12 Kernen, 18 GB RAM → Swap → Rechner stand, Yasin musste neu starten; die
Session brach ab, 90 Minuten verloren. Yasin: „Sowas sollte nicht mehr
passieren." Regel: Arbeiter bauen nicht; nur der Wächter baut, einmal, seriell.

## Welle 25 — ein Wächter je Themenbereich (30.08.2026)

Yasin, 30.08.2026, sinngemäß: „Je Themenbereich ein Opus-Wächter, der
auf 3–5 Arbeiter aufpasst, Aufträge 15–25 Minuten."

Nach Welle 23 (billig, aber 2 Std. 20 durch seriellen Schwanz) und
Welle 24 (schnell gedacht, aber Rechner-Absturz durch 12 gleichzeitige
Kaltbuilds) war klar: EIN Wächter je Welle ist die falsche Größe. Er ist
Engpass, wenn er zu viele Arbeiter führt, und er kann den Bauzugriff nicht
mehr ordnen. Daraus die Regeln der Welle 25:

- **Ein Wächter JE THEMENBEREICH** (Oberfläche, Audio, Tests, Doku …),
  jeder mit **höchstens 4–6 Arbeitern** (Yasins Zahl war 3–5; 4–6 ist die
  im Skill festgehaltene Obergrenze). Jeder Themen-Wächter merged in seinen
  eigenen Integrationsbranch. Die **Hauptsitzung** führt die Integrations-
  branches zusammen und startet dann **einen Merge-Wächter** für den einen
  Build, die Vollsuite, das Bundle und die QA-Runde. Damit wird die
  Hauptsitzung einmal je Thema geweckt statt einmal je Arbeiter — und
  bleibt trotzdem die Instanz, die den Gesamtstand kennt.
- **Aufträge 15–25 Minuten** statt ~30. Kürzere Aufträge landen dichter
  beieinander; ein Wächter mit fünf Arbeitern wartet sonst auf den
  langsamsten und baut den seriellen Schwanz im Kleinen wieder ein.
- **Build-Schloss:** `mkdir /tmp/<projekt>-build.lock` vor jedem Build,
  `rmdir` danach. `mkdir` ist atomar, also wirkt das Schloss über Agenten,
  Worktrees und Sitzungen hinweg. Nie mehr als ein Build pro Rechner — die
  mechanische Fassung der Lehre vom 29.08.
- **Modellwahl:** Fable 5 als Arbeiter nur für Aufträge, die der Nutzer
  als „wichtig" markiert hat (dort lohnt das schnellere Modell); alles
  andere Opus/low. **Sonnet nur für Triviales ohne Bau.**

Ebenfalls am 30.08. präzisiert (aus dem Codex-Review vom 29.08.):

- **Parallel schlägt seriell innerhalb einer Welle.** Der alte Widerspruch
  („Wächter startet alle gleichzeitig" vs. „Nutzer abwesend → seriell")
  wird so aufgelöst: Ein Wächter startet seine Arbeiter IMMER parallel.
  Die Taktungsregel gilt nur für Nicht-Wächter-Arbeit der Hauptsitzung.
- **Eskalations-Ausnahme:** Rückfragen gehören ins Handoff — außer bei
  unumkehrbaren/zerstörenden Aktionen, Sicherheit/Zugangsdaten, von außen
  Sichtbarem, echtem Geldeinsatz oder Repo-Inhalten an externe Modelle.
  Dort sofort im Chat fragen, vor dem Handeln.
- **Kostenrechnung für Subagenten korrigiert:** Der erste Schritt eines
  frischen Subagenten zahlt seinen Startkontext ×2, erst danach ×0,1.
  Break-even bei 220k Haupt- und 30k Agentkontext: 60k ÷ (22k − 3k) ≈
  7 Schritte je Agent. Kürzere Aufträge macht man selbst.
