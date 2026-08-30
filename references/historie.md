# warm-handoff — History (complete version up to 29.08.2026, with all dated user quotes)
> Reference work for the core skill in ../SKILL.md. Do not load by default.

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

Claude Code caches your conversation prefix. Working *inside* that cache is fast and cheap;
rebuilding it is slow and expensive. This skill makes the cache window visible, keeps you
inside it, and — when leaving it is the better deal — writes the handoff that lets a fresh
session continue seamlessly.
> Primary language: English. Dated German passages record the sessions each rule came from — sie bleiben bewusst erhalten. German README: README.de.md in the repo.


## Table of contents by topic (Thematischer Wegweiser)

This file grew session by session — dated headings mark when a rule was added and why.
To find things by TOPIC rather than by date, use this map:

| Topic | Sections |
|---|---|
| Facts & mechanics | The facts · What a cache rebuild looks like · When does the hour actually start · RECOGNIZING a cache rebuild |
| What Claude does each turn | What Claude does when this skill is active · The window as a friendly coach · Honesty rules |
| Measuring instead of guessing | COUNTING the steps · FACTORING IN the start-up cost · CALCULATING the Sweetspot (sweet spot) · What actually gets WRITTEN |
| Fewer requests (the real lever) | The real lever · The techniques list · How few requests are realistic · Messages DURING the work · Output is expensive |
| Subagents | Pacing · Choosing WHICH subagent · Sequential vs. parallel · Make the work visible · The most honest number · Subagents are the default path · Long agent runs / the user as bottleneck / Fable low |
| Cost visibility | The Kostenzeile (cost line) · The cost table · How to read this table · This skill is meant to TEACH |
| Paid quota | Making the paid quota visible · What's still in the tank · Wake-up ping · Codex, Gemini and OpenRouter · Codex by account size (29.08.) |
| Sammlung & end field | Four rules from 29.08.: copy the Sammlung (collection) verbatim · End field as a banner · Agent display |
| The handoff document | The wave workflow · Writing the handoff well · When to stay vs. hand off · The economics, honestly · Dictating into the terminal |
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

   **Third source — and it is the best one: MEASURE IT YOURSELF (Yasin 25.08.2026).** His
   objection: „Dass du bei dieser Session die Gesamtkontextgröße nicht siehst, das ist doch
   komisch, das muss doch irgendwie gehen." (the user's German original; roughly: "It's odd
   that you can't see this session's total context size — there must be a way.") He was
   right. Claude Code writes every request together with its `usage` block into the session
   file under `~/.claude/projects/<pfad-mit-bindestrichen>/<session-id>.jsonl`. The last
   line carrying `usage` holds `cache_read_input_tokens + cache_creation_input_tokens` —
   that IS the current context size. One Bash call is enough:

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

   With this, the Sweetspot announcement (see below) is defensible at any time — even
   without the user typing out his status line. At the end of a Welle (wave) this
   measurement is part of the routine.

   Two honest limitations: the file is appended per request, so the number is the state of
   the LAST request, not of this second. And the dollar amount is the API EQUIVALENT at
   list prices — on a Pro/Max subscription nobody pays that sum; it measures what is
   charged against the quota.

   If none of these three sources is available → „Kontext: nicht gemessen" (or leave it
   out). The same applies to the closing line of the handoff: a made-up „~60k" there is the
   same mistake, only archived.

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
- **And the other half of the truth: EVERY REPLY COSTS as well.** A request is a request,
  no matter who triggers it — Claude's own reply also re-reads the whole context at 10%
  (at 220k that is ~22k equivalents) and pays on top for its own output tokens at
  **five times** the price. A 300-word reply is ~2,000 extra equivalents. So keeping the
  clock warm for free is impossible: every timer reset is a paid request. That is not an
  argument against replying, but against rambling — and the reason empty interim
  notifications were struck out.

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
  Then radio silence until the end.
- **Name the running total** at wave end: how many agents ran, what came back, what is
  still open.

**REVOKED on 26.08.2026, 16:48 — no more individual per-agent notifications.** This spot
used to say "announce each subagent when it starts AND when it lands, those lines double
as cache-refreshing requests". That was expensive and unnecessary. Yasin's objection,
verbatim:
„Du musst mir kein Feedback geben, wenn einer gestoppt hat. Dann hat er gestoppt — bis
dann alle fertig sind oder bis fast eine Stunde rum ist, damit du den Cache warm hältst.
Unten in meinem cmux-Fenster sehe ich ja doch, wenn Unteragenten arbeiten."

He is right on both counts:

1. **The host displays running agents anyway.** A line "Agent 3 is done" is information
   the user already has in front of him — paid for with a full request.
2. **As a cache warmer these messages are unnecessary,** because Claude's own tool-steps
   reset the timer at every step anyway. The message warms nothing that would not already
   be warm.

The rule is now:

- **During a wave there is NO per-agent reporting.** If five agents land, ONE summary is
  produced once the last one is through.
- **Reporting happens on three occasions only:** a decision the user has to make · a
  blockage that cannot move on without him · a completed milestone.
- **The exception is the clock:** if the user is present and the wave has already been
  running for nearly an hour without a sign of life, ONE bundled interim message goes out —
  so the cache window does not expire and he is not left in the dark.
- **For a single long-running agent** (no bundle) the same applies: wait for the result,
  do not comment that it has started.

Worked example from the measured session: five individual notifications at ~220k context
are roughly 110k token equivalents — for text the user can already see.

### Keep it terminal- and tool-neutral

Some users run cmux, others plain Terminal/iTerm/Ghostty, VS Code, or Codex instead of
Claude Code. Everything in this skill must survive that:

- Never assume a specific terminal's UI. Say "deine Statuszeile", not "das cmux-Feld".
  If a feature only exists in one host (cmux panes/surfaces, a custom status line),
  mark it as such in one clause and give the generic fallback.
- The handoff document is the portable artifact: a plain Markdown file any agent in any
  tool can read. Never encode state in a terminal-specific place instead.
- When another agent (Codex/GPT, Gemini) does the work, the SAME rules apply — timestamp,
  measured context, handoff, archive. Hand it the handoff file, not a chat summary.

## CALCULATING the Sweetspot and announcing it (Yasin 25.08.2026)

His wish, in his own words: „Könnten wir den Sweetspot berechnen und dann sagen: hey, jetzt
ist dein Sweetspot erreicht, deswegen habe ich ein Handoff gemacht, die Welle ist auch
gerade fertig, starte lieber eine neue Session — das wäre am elegantesten."

That works, and without magic. Two numbers are enough, both readable:

```
verbleibende Schritte im Fenster ≈ (Ziel-Kontext − aktueller Kontext) / Zuwachs pro Schritt
```

- **Current context**: from the status line (`ctx 148k`) — never estimated.
- **Growth per step**: from this session itself. Two measuring points suffice: context at
  the last handoff, context now, divided by the number of waves/steps in between. In
  practice: a build wave with tests costs roughly 40–80k, a round of conversation 2–5k.
- **Target context**: 200k / 250k / 300k depending on what comes next (table above).

Out of that comes an announcement the user can actually use — not "your context is large",
but **how much still fits**:

> „Kontext 148k, Ziel 200k vor der nächsten Bau-Welle — das reicht noch für etwa eine
> Welle oder ein Dutzend Fragen. Danach mache ich das Handoff."

**When this announcement comes (unprompted):**
- at the end of every wave, together with the measured context number;
- as soon as the remaining budget falls below ONE further wave — then say it plainly:
  „Das hier war die letzte Welle in dieser Sitzung, das Handoff ist geschrieben, starte
  morgen frisch."
- when the user asks for the status.

**Tone (his explicit wish):** short, casual, motivating — never admonishing.
„Noch Platz für ~2 Wellen" is a streak counter, not an invoice. And when the budget gets
tight, the practical hint is fine too: „Ab hier lieber längere Nachrichten sammeln statt
vieler kurzer" — that is the same thought, just from his perspective.

Honest limit: growth per step varies a lot (a screenshot costs more than a text reply).
The estimate is an order of magnitude, not a promise — it should be phrased that way too
(„etwa", „grob"), and the measured context number always stands next to it.

### FACTORING IN the start-up cost of a fresh session (Yasin 25.08.2026)

His objection, verbatim: „Du beachtest nicht, dass bei einer neuen Session ja ich mit
70.000 Tokens starte und das mal zwei gerechnet wird, weil der Cache neu aufgebaut wird.
Deswegen ist in unserem Skill eine Rechnung noch nicht perfekt."

He is right, and the proof was in the same session: the MEASUREMENT taken right after the
session start, before the first line of work, came to **82k** — not the "~20k" this skill
assumes in several places. Skills, tool schemas, system prompts and project rules are
already there before the user does anything. The 20k figure was too optimistic and must be
MEASURED per project instead of guessed.

The full calculation has three items instead of two. **The cache-write factor depends on
the TTL, and this is a classic mix-up:** 1.25× applies to the 5-MINUTE storage, **2× to
the 1-HOUR storage** — and on Pro/Max that is the normal case (see "The facts" at the very
top). Anyone plugging in 1.25 prices the rebuild 60% too cheap. Yasin found exactly this
mistake on 25.08.2026 („das müsste doch mal zwei sein, dachte ich") — he was right.
Cache read stays 0.1×.

```
Neuaufbau EINMALIG       = Startkontext × 2      (1-h-TTL; nur bei 5-min-TTL × 1,25)
Schritt in neuer Session = Startkontext × 0,1
Schritt in alter Session = aktueller Kontext × 0,1
Break-even (Schritte)    = (Startkontext × 2) / ((alt − neu) × 0,1)
```

Example from the session: start 82k, currently 287k →
rebuild ~164k, saving 20.5k per step → **break-even at ~8 steps.**

**The sentence most often misunderstood here:** "steps" are NOT the user's messages, but
overwhelmingly Claude's own tool calls. From that follows the rule that actually holds:

- **Only talking / going through the Testliste (test list) / a few small corrections**
  (< ~6 steps) → STAY, even at 260k+. The rebuild would cost more than it saves.
- **A build wave, a review, a migration** (hundreds of steps) → SWITCH, as soon as the
  context is clearly above the start context. Break-even already falls after the sixth
  step, everything after that is pure gain.

That is why the Sweetspot announcement must ALWAYS include this session's measured start
context and the question "what comes next?" — without both, the recommendation is guessed.

### COUNTING the steps, not estimating them (Yasin's assignment, 25.08.2026)

His sentence: „Da müssen wir dann schauen, wie viele Schritte das wirklich sind — das muss
der Skill schon berechnen, wissen und auch dem User anzeigen."

Doable, and exactly: every request to the model appears as a line with `usage` in the
session file. Start context, current context, number of requests and the share the user
triggered himself can be read off directly. This single call delivers the complete
Sweetspot calculation:

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

What the numbers mean and how they turn into an announcement:

- **"Requests" is the number that counts — not the user's messages.** In a real build wave
  there were 205 requests against 15 user messages: roughly 14 steps per message on
  average, well over 100 within the wave itself, exactly 1 in rounds of conversation.
  That is precisely why a fat context is cheap to TALK on and expensive to WORK on.
- **Break-even in steps** says from when the switch pays off. If the expected step count of
  the next task is below it → stay. Above it → switch.
- The announcement to the user names both numbers and the recommendation in one sentence,
  e.g.: „287k, Start war 82k — ein Wechsel kostet einmalig ~102k und lohnt ab ~5 Schritten.
  Testliste durchgehen: bleiben. Nächste Bau-Welle: wechseln."

This measurement belongs at every wave end and in every answer to „soll ich neu starten?".

## Dictating into the terminal: keep it short, long stuff belongs in the document

Important for anyone who speaks their messages instead of typing them
(Yasin 25.08.2026):

**Terminals shorten long inputs to a placeholder.** In cmux, beyond a certain
length only `[pasted text]` appears (Ghostty and others behave similarly) —
the user then can NO LONGER see what he actually said, cannot skim it,
cannot correct it, cannot find it again. A long dictation is therefore
effectively sent blind in the terminal.

From this follows the division of labour that this skill recommends anyway —
now with the concrete reason behind it:

- **Short messages belong in the terminal**: a question, a task, a correction.
  Short enough that it stays there as visible text.
- **Everything long belongs in the Handoff (session handover) document in the
  text editor**: test answers, ideas, braindumps, criticism. There the user
  sees every word, can keep working for days, add to it and rearrange it —
  and in the end the agent reads the whole document in one go.
- This is not a compromise but the better way: a Handoff may grow for weeks
  until it is full. Then a fresh session, document in, and on we go.

Claude says this to the user ONCE per setup — not with every long message.

## The window as a friendly coach (frame it this way)

Present the 1-hour window, the handoff ritual and the test list as POSITIVE motivators,
never as pressure or cost-anxiety. The sliding hour is a natural work rhythm: "answer
within the hour and the wave keeps riding" is the same gentle pull as a streak — it
nudges the user to test the delivered items now, dictate answers now, fire the next wave
now, while everything is fresh. The pre-seeded test questions make re-entry effortless
(no blank page — just put the cursor after the marker and speak). Claude should
occasionally voice this framing ("window's still warm — perfect moment for the test
list"), and celebrate kept streaks in the logbook rather than only counting waste.

## The real lever: FEWER REQUESTS (Yasin 26.08.2026, 16:48)

This skill focused on context size for a long time. The measurement from
26.08.2026 shows that this was only a third of the truth. The numbers from a
real working session:

| Item | Tokens | Factor | Equivalent |
|---|---|---|---|
| Cache read | 22.171k | ×0,1 | 2.217k |
| Cache written | 562k | ×2 | 1.125k |
| **Own output** | 208k | **×5** | **1.038k** |

**147 requests — of which 13 were triggered by user messages.** The other 134
were the agent's own tool steps and interim reports. And its own OUTPUT made up
almost a quarter of total costs — the item this skill previously did not even mention.

From this follow three goals, in this order: **fewer requests · shorter own
output · smaller context.** The handover (the original purpose of this skill) is
the WEAKEST of the three levers.

### The technique list (cross-checked with Codex)

A second model (GPT-5.6 via Codex) was given the same numbers and estimated what
each technique would have saved in exactly this session. Target picture: **35–55
instead of 147 requests in the main context**, total cost from 4.380k down to
1.350–2.050k.

| Technique | How | Effect |
|---|---|---|
| **Bundle tools** | Request all independent read/search/check steps in parallel in ONE reply, only evaluate afterwards | −25 to −45 requests |
| **Script instead of single commands** | One call that does ten things and prints ONE summary, instead of ten calls | −20 to −35 requests |
| **Cut agents along work packages** | ONE agent does "find cause + build fix + check tests", not three agents doing one part each | −30 to −60 requests |
| **Keep the boss context lean** | The agent gets paths, goal, boundaries, acceptance criteria — never the chat history | −0,2 to −0,5 million read |
| **Reports as a file** | The agent writes details into a file; only result, risks and path come back | −0,3 to −0,7 million |
| **Cap report length** | Specify in the agent's brief: at most 300 words, no work chronicle, no copied logs | −0,2 to −0,4 million output |
| **Bundle interim reports** | See own rule above | −15 to −30 requests |
| **Pre-filter output** | `grep`/`jq`/`tail` before printing; success in one line, on failure only the relevant lines | −0,1 to −0,3 million |
| **Own output budget** | Interim updates ≤100 words, closing ≤500 words, details in files instead of in the chat | 208k → 50–80k output |
| **Hand over earlier** | At 100–120k instead of at 223k | −0,3 to −0,7 million read |

(The effects overlap and must not be added up.)

### How few requests are realistic? (the honest answer)

Yasin's obvious follow-up question: „Versuchen wir, die 147 Anfragen zum Beispiel
auf 14 zu reduzieren — kann man das so sagen?" (roughly: can we say we reduce the
147 requests to, say, 14?)

For the MAIN CONTEXT: yes, the order of magnitude is right. For the work itself:
no — it does not disappear, it MIGRATES into the subagents. That is precisely
the trick:

- 100 work steps in the main context at 220k → 100 × 22k = **2.200k equivalents**.
- The same 100 steps in a subagent at ~30k → 100 × 3k = **300k**.
- **Factor ~7** — and none of these 100 steps shows up in the main session as a request.

The realistic lower bound of a pure orchestration Welle (wave), item by item:

| Requests | What for |
|---|---|
| 1 | read the Handoff |
| 1–2 | start the whole fleet in ONE bundled reply |
| 1 each per agent | its closing report — unavoidable, that is how the result arrives |
| 2–3 | building, testing, committing, each via ONE script |
| 1 | write the Handoff |
| 1 | closing message |

That lands at roughly **13–20 instead of 147 requests** for the same delivered work.
Conversations with the user in between come on top — and those are wanted, not waste.
What is to be trimmed away is the machine's chatter, never the user's thinking.

### Messages DURING the work are almost free (Yasin 26.08.2026, 17:26)

His question, asked three times because the answer changes everything: „Kostet
diese Nachricht jetzt auch nichts, weil du gerade arbeitest? Oder meinst du, weil
es kurze Nachrichten sind?" (roughly: does this message cost nothing because you
are working right now — or did you mean because they are short messages?)

It is not the brevity that is the reason but the **timing**. And the difference is
large:

- **The agent is working right now** (tools are running, subagents are computing).
  The message is hooked into the running flow and rides along with the next request
  that would have happened anyway. **No additional request** arises. Only the message
  text itself is paid for, written into the cache once: 50 words ≈ 70 tokens × 2 ≈
  **140 equivalents**.
- **The agent is waiting** (idle state after its reply). Now the message TRIGGERS a
  request that would otherwise not have happened: **the full context × 0,1**. At 220k
  that is **22.000 equivalents** — 150 times as much.

The same in one sentence: during the work an interim question costs about half a
percent of what it costs in the idle state.

**The catch that is easily overlooked here:** the question is cheap — the ANSWER is
not. Output costs a factor of 5; a 300-word answer is ~2.000 equivalents, i.e.
fourteen times the question. Therefore, for answers to interim questions during a
running wave: **keep it short, details later in the Handoff.** Do not slow down the
question, but your own rambling.

**CLARIFICATION, because "while something is running" means two different things
(Yasin asked immediately, 26.08.2026, 17:37 — rightly so).** What matters is not
whether SOMETHING is computing somewhere, but whether one's own tool flow is
currently running:

| Situation | User's message | Cost |
|---|---|---|
| One's own tool loop is running (reading a file, a command, starting an agent) | is appended, rides along | **almost zero** |
| **Subagents are computing, one is waiting oneself** | triggers a new request | **the full 10 %** |
| After one's own reply, idle state | triggers a new request | **the full 10 %** |

The middle case is the surprising one and must be stated explicitly to the user:
while subagents are working, THE MAIN AGENT IS NOT WORKING — it is waiting for
their reports. A message during that time is as expensive as any other in the
idle state.

One consolation that is also true: **several messages in quick succession are
bundled into ONE request** if they arrive before the answer begins. Two thoughts
right after one another therefore cost once, not twice.

What the user takes away from this in practice — and this should be said to him
ONCE (output template, stays German):

> Solange du siehst, dass ich selbst rattere, schreib ruhig sofort. Wenn nur die
> Unteragenten laufen oder ich auf dich warte, sammle lieber und schick es gebündelt —
> am besten in den Sammelbereich des Handoffs, dort kostet es gar nichts.

And that is exactly why the collection area (Sammlung — collection) in the Handoff
is so valuable: collecting there costs exactly zero, because no request arises at all.

### What actually gets WRITTEN? (the most underestimated column)

On 26.08.2026 at 18:04 Yasin assumed the 1.125k write costs came from his own
messages: „Egal ob ich gesammelt oder einzeln schreibe — das Schreiben ist nicht zu
vernachlässigen." (roughly: whether I write in batches or one by one — the writing
is not negligible.) The conclusion is understandable and nevertheless wrong, and
the correction changes where you apply the lever.

Everything that comes NEW into the transcript is written. Sorted by size:

1. **Tool results** — file contents, command outputs, search hits, images. A 500-line
   file that has been read is ~7k tokens which migrate into the cache once at double
   price. This is by far the largest item.
2. **Subagent reports** — an 800-word report is ~1k tokens × 2. With ten agents that
   adds up; that is why the 300-word limit is in the subagent contract.
3. **One's own replies** — they pay twice: first as output (×5), then at the next step
   as a cache write (×2).
4. **The user's messages** — the smallest item of all. 100 words ≈ 140 tokens × 2 =
   280 equivalents. Against 1.125k total writing that is one per mille.

**From this follows the instruction for action, and it does NOT target the user:**
do not read whole files when a `grep` is enough. Pre-filter command output instead of
letting it in raw. Cap reports. Only look at images when they are really needed. The
user should feel free to write as much as he wants — he is not the problem.

### The most honest number in the whole skill: what subagents really save

This needs to be calculated cleanly, because two different things previously stood in
ONE calculation — 147 steps on the left, 600 on the right — and from that the wrong
conclusion was drawn that subagents do not lower the bill. The comparison was unfair:
it assumed different amounts of work on the two sides. There are two statements, and
the first is the more important one.

**First: the same work, merely delegated — here it really does get cheaper.**

```
Alles im Hauptkontext:  147 Schritte × 151k × 0,1              = 2.217k
Delegiert:               14 Hauptanfragen × 345k × 0,1  =  483k
                        147 Agentenschritte ×  30k × 0,1 =  441k
                                                   Summe =  924k
```

**2,4× less for exactly the same work.** There is nothing more behind it: every step
counts against the agent's small context instead of the session's fat one — roughly
**one fifth** per work step.

**Second, and this is a SEPARATE thought:** whoever does not pocket the saving but
reinvests it gets a multiple of the work for the same allowance. An agent works more
thoroughly than one would do on the side — 147 steps quickly become 600:

```
14 Hauptanfragen × 345k × 0,1 =   483k
600 Agentenschritte × 30k × 0,1 = 1.800k
                          Summe = 2.283k
```

Then the bill is roughly balanced again — but **four times as much has been done**.
That is exactly what the "token maximisation" the user wants means: more work for the
same allowance, not less output.

> **Subagenten machen beides: dieselbe Arbeit deutlich billiger (Faktor ~2,4) — und, wenn
> man das Gesparte wieder ausgibt, ein Vielfaches an Arbeit zum selben Preis.**

And the honesty that goes with it: **subagent tokens are not free.** They draw on the
same weekly allowance. What they do not burden is the MAIN CONTEXT — the session stays
small, fast and responsive, and that is precisely their value. Whoever believes agents
run "on the side" will later be surprised by their allowance.

### Subagents are the standard route, not the exception

Yasin's formulation, and it hits the mark: „Ziel ist, dass ich mit einem guten Modell
arbeite, das als Chef die Unteragenten rauslässt, wenig Tokens verbraucht, gebündelt
alles sagt und wenig Anfragen macht."

**Why the STARTUP COSTS make the difference.** Yasin phrased the mechanism better than
any documentation (26.08.2026): „Wenn du einen Unteragenten losschickst, startet der
nicht wie eine neue Session bei 80.000 Tokens mal zwei, sondern zum Beispiel bei 10.000
mal zwei. Er verbrät dann intern viel, teilweise günstig, teilweise teuer — aber er gibt
WENIG zurück, weil er nur das Ergebnis zurückgibt. Und somit bleibt die aktuelle Session
klein und günstig."

The same, item by item:

1. **Starting context.** A fresh session was at **82k** in a real project before a single
   line of work had happened — skills, tool schemas and project rules are there beforehand —
   and rebuilding it costs that times two. A subagent starts with its brief plus its own
   tool schemas, so roughly **10–20k**; times two that is a one-off ~20–40k.
2. **What happens internally.** The agent reads, searches, changes, tests — dozens of steps,
   each of which re-reads only ITS small context at ×0,1. Some steps are cheap, some (long
   files, test output) are not — but each counts against ~15k instead of against your 220k.
   That is why 100 steps cost ~300k there and ~2.200k here.
3. **What flows back into the main context.** Exactly two things: the brief you wrote and the
   report you limited to 300 words. Work chronicle, logs and dead ends stay in the agent's
   context and die with it.

Expensive work, cheap receipt — this asymmetry is the biggest single lever in this whole
skill. In the measured session six agents together consumed over a million tokens; only
briefs and reports ended up in the main context.

**When a subagent is NOT worth it** (this too belongs to the honesty): below about
3–5 tool steps, with strictly sequential work, or when a lot of shared context would have
to be transferred first. Its startup cost is roughly 1–3 requests plus briefing plus report.

**Model and thinking depth belong in the DISPLAYED name (Yasin 26.08.2026, 17:35).**
His objection: „Wenn du Unteragenten losschickst — kannst du unten anzeigen, welche Art
gerade arbeitet? GPT-5.6 hoch, extra hoch, oder Opus 5? Den Effort stellst du doch auch
ein. Aktuell sehe ich nie, welcher Agent das ist."

He is right, and the solution is trivial: the host displays the agent's SHORT DESCRIPTION —
so the model belongs in there, not just the task.

```
schlecht:  "History-Tempo Runde 2"
gut:       "Opus5/high · History-Tempo"
gut:       "Fable/low · Testdateien umbenennen"
gut:       "GPT5.6 · Zeitmessende Tests"     (Codex-Lauf)
```

This way the user sees at a glance in the terminal whether an expensive or a cheap model is
running — and can intervene before the tokens are gone. If no model is set, the agent inherits
the session model; that too should then be named as such ("geerbt" / inherited) instead of
concealing it. The same rule applies to the announcement in the chat: when a fleet starts, the
ONE start message states who runs on which model with which thinking depth.

**The subagent contract**, which belongs in every brief (output template, stays German):

> Arbeite bis zum Ergebnis oder bis zu einer echten Blockade. Melde nur: Status,
> Entscheidungen, Belege mit Pfaden, Risiken, nächster Schritt. Höchstens 300 Wörter,
> keine Arbeitschronik, keine kopierten Protokolle oder Diffs — Details in eine Datei.

### Output is expensive — write shorter

Output costs **five times** the price of fresh input and fifty times that of a cache read.
In practice this means:

- **No retelling of one's own work.** What the user sees in the terminal does not have to be
  repeated in prose.
- **Long content belongs in files**, not in the chat — that is exactly why the Handoff is a
  file and not a chat message.
- **No version "just to be safe, in full once more".** A pointer to the file is enough.
- The Handoff itself stays detailed: it replaces an entire context and is therefore the best
  investment on the list. Detailed ≠ chatty.

### This skill should EDUCATE, not just keep time

Yasin's explicit instruction (16:53): „Der Skill soll auch schulen. Die Leute sollen
verstehen, wie das genau funktioniert. So wie es mir geht, geht es vielen Leuten."

Therefore the following applies to every cost statement made to the user:

1. **First the number, then the rule.** Not "that is expensive", but "that is 22k equivalents,
   because the context is 220k in size and reading costs a tenth".
2. **Actively clear up misunderstandings.** The most common one: "X requests = X cache
   rebuilds". Wrong — see the measurement in the section „Einen Cache-Neuaufbau ERKENNEN"
   (recognising a cache rebuild).
3. **Name one's own mistakes.** If an earlier explanation was off (here: "saved almost half" —
   recalculated it was more like a third), it gets corrected, not silently overwritten.

## The Kostenzeile (cost line) under EVERY answer (Yasin 26.08.2026, 18:06)

His wish: „Kannst du bei jeder Nachricht, die du ausgibst, sagen, was wie viel gekostet hat —
zehn Prozent, zweihundert Prozent? Diese Tokenangabe einfach zusätzlich bei deinen Antworten."
And the counter-question right after it: „Oder sprengt das den Skill?"

It does not blow up the skill — it is its core: making costs visible instead of talking about
them. But it has a trap that you hit immediately when building it.

**The trap:** a measurement needs a tool call, and a tool call IS a request — at 350k context
that is 35k equivalents. Whoever builds the cost display naively pays more for measuring than
the display will ever save. That would be a thermometer that heats the room.

**The solution:** `~/.claude/ctx.sh` is NEVER called on its own, but appended to a command that
runs anyway — usually to the same `date` that supplies the timestamp:

```bash
date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh
```

Output (a real line):

```
KOSTEN | Kontext 366k · letzte Anfrage: 366k gelesen ×0,1 + 0.4k geschrieben ×2
        + 2.9k Ausgabe ×5 = 52k | Sitzung: 265 Anfragen, 9520k
```

From this a plain-text line under the answer is produced (output template, stays German):

> *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe
> (×5) ≈ 52k · Sitzung bisher: 265 Anfragen, 9.520k*

**The two honesty rules that go with it** — the same as for time of day and context size:

1. **All three numbers come from the LAST COMPLETED request** — not from the answer under which
   the line stands. The cost of the running answer is only fixed once it is finished; nobody can
   know it in the meantime. On 26.08.2026 Yasin asked exactly the right question: „Diese 2.600
   Ausgabe-Token — sind das wirklich die dieser Antwort gewesen?" No. With reading and writing
   this is barely noticeable, because the context only grows by percentages per step. With the
   OUTPUT, however, very much so: a short answer then stands under the output figure of a long
   one — and vice versa. That is why the line is called **„Letzte gemessene Anfrage"** and no
   longer "Diese Runde".
   The alternative: one COULD estimate the output of the running answer from its word count
   (words × ~1,4). Permitted — but that would be an estimate next to two measured values, and
   whoever writes it down marks it as an estimate („≈2,6k geschätzt").
2. **No number without a measurement in this round** — or an extrapolation of the last state
   explicitly marked with `~`. Never an invented one.

**The line's second purpose: to speak up when a round was conspicuously expensive**
(Yasin 26.08.2026, 18:17). His wish verbatim: „Das ist ja das Genialste, dass du am Ende genau
das sagst, was ich sehen wollte — dann sieht der User, was er gerade verbraucht hat. Und wenn
er ganz viel verbraucht hat, kannst du ja noch hinweisen: hallo, das war blöd von dir. In
irgendeiner Form, ganz nett."

- **When at all:** only when a round is clearly above one's own average for THIS session —
  roughly: more than twice the average cost per request so far. No fixed limit; the average is
  in the session file and is therefore measured, not guessed.
- **The tone is the decisive thing, and it is explicitly NOT reproachful** — the user himself
  said „ganz nett" (quite nicely). Never "that was silly", but name the cause and offer a
  concrete cheaper route (output templates, stay German):

  > „Die Runde war teuer (≈120k), weil ich drei große Dateien komplett gelesen habe — beim
  > nächsten Mal reicht ein gezielter Suchlauf."

  > „Diese fünf kurzen Nachrichten haben zusammen ≈180k gekostet, weil der Kontext
  > inzwischen 350k groß ist. Gesammelt in einer wären es ≈37k gewesen."
- **The responsibility lies almost always with the AGENT, not with the user.** This belongs
  here explicitly, otherwise the feature turns into user education. The most common causes of
  expensive rounds are: reading whole files instead of grepping, unfiltered command output,
  overly long replies of one's own, individual reports per subagent — all things the agent
  stops doing, not the user.
- **At most ONCE per Welle**, not again with every expensive round. Otherwise the hint turns
  into nagging.
- **The opposite direction belongs to it too.** If a round was unusually cheap or a wave went
  well, that gets named just as much: „Die ganze Welle lief über Subagenten — 40k im
  Hauptkontext für sechs Arbeitspakete." The skill should motivate, not admonish.

**When the line is omitted:** in pure interjections and one-liners. A cost line under a
three-word sentence is noise. It makes sense at the end of every substantive answer, at the end
of a wave and in the Handoff.

## The cost table per session (Yasin 26.08.2026, 17:51)

His wish: „Kannst du nicht einfach so eine Tabelle machen, wo wir alles übersichtlich haben je
Session — damit man eine Übersicht hat, was wann wie viel Tokens gekostet hat? Das wäre doch
genial."

Built as `~/.claude/session-kosten.sh`. The table's unit is deliberately the **stretch between
two user messages** — that is what a human experiences ("I said something, then something
happened"), not the individual model request that nobody sees.

```bash
~/.claude/session-kosten.sh              # aktuelles Projekt, neueste Sitzung
~/.claude/session-kosten.sh --markdown   # nur die Tabelle, fertig fürs Handoff
```

Example output (a real session):

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

### How to read this table (Yasin did not understand it at first sight — rightly so)

His questions verbatim: „22.171k — sind das 22 Millionen Token gelesen? Was wurde da
gelesen? Warum steht in Zeile 2 als Kontext 241k? Ich kapiere die ganze Tabelle nicht."
Entirely justified: without the following picture not a single number in it makes sense. This
explanation therefore belongs with it whenever the table is shown to somebody.

**First the banal part, because that is exactly where understanding gets stuck: "k" means
thousand.** So 22.171k is 22.171.000 tokens — yes, twenty-two million, in a single session.

**And now the picture that makes everything click: the conversation transcript is a book.** The
model has NO memory between two requests. Before every single answer it reads the WHOLE book
again from the beginning — every earlier message, every file read, every tool result. With 147
requests and a book that was on average around 151.000 tokens ("pages") thick, that is
147 × 151k = **22.171k pages read**. That is why the read column contains a number that is a
multiple of the context column. That is not an error in the table — that IS how it works.

**The calculation adds up exactly**, and that is precisely why it convinces:

```
147 Anfragen × ~151k Durchschnittskontext = 22.171k gelesen   × 0,1  = 2.217k
                                               562k geschrieben × 2   = 1.125k
                                               208k eigene Ausgabe × 5 = 1.038k
                                                                 Summe = 4.380k
```

4.380k — exactly the number that stands in the equivalent column.

**What each column means:**

| Column | Meaning |
|---|---|
| **#** | number of the stretch (one stretch = from one user message to the next) |
| **Zeit** | when the stretch began, in your local time |
| **Worum es ging** | the first words of your message, so you recognise the row again |
| **Anfr.** | how many requests to the model this one sentence of yours triggered |
| **Kontext** | how thick the book was at the END of the stretch — **not a cost column** |
| **gelesen** | requests × book thickness; the largest item, price ×0,1 |
| **geschr.** | what was newly written into the cache, price ×2 |
| **Ausgabe** | what Claude itself wrote, price ×5 |
| **Äquiv.** | the three items converted to one price and added up |

**The most important sentence about the context column: it does NOT add up.** "241k" in row 2
does not mean that this stretch cost 241k — it means that the book was 241.000 tokens thick at
the end of this stretch. It is there to EXPLAIN the read column: the thicker the book, the more
expensive every further request. That is why it grows steadily over the session, while the cost
columns fluctuate per stretch.

**And a row with 0 requests is not an error.** It means: this message arrived while the work
was already running, was appended to the running flow and did not trigger a request of its own —
exactly the case from the table „Nachrichten WÄHREND der Arbeit sind fast gratis". A zero there
is the cheapest row there is.

The four lines under the table are the real yield — they each answer a question that otherwise
stays open: *Which wave was expensive? How many steps does one message trigger? How much does my
own chatter cost? Was the cache warm at all?*

**Rule: this table belongs in EVERY Handoff**, directly before the closing line with the context
level. It does not replace the previous single number ("Kontext dieser Session: 220k") but
explains it. And it is more honest than any memory: it also shows the stretches in which a lot
of money was burned for little result.

**Two things the script deliberately does this way — and which are easy to get wrong when
rebuilding it:** the session file stores UTC, the user thinks in his local time (convert, or the
whole table will seem wrong). And not every line of type "user" is a message from the human —
tool results, agent completion notices and skill loads carry the same type. Without a filter the
table disintegrates into system rows and becomes unreadable.

## Making the paid allowance visible — and using it up (Yasin 26.08.2026, 14:03)

His wish verbatim: „Siehst du bei Codex überhaupt, ob ich noch genug Limit habe?
Könnte man das sichtbar machen — und dass du mich ab und an darauf hinweist? Wenn ich
einen Account habe, wo ich monatlich bezahle, dann sollte man die Tokens ausnutzen, wenn
da noch welche frei sind. Der Skill könnte sagen: hey, wir hätten jetzt Zeit, wir haben
noch ganz viele Tokens übrig in Codex oder in deinem Wochenkontingent — mach dir mal
Gedanken, was wir da machen könnten. Und das gehört ganz oben ins Handoff, als
Hauptinformation."

Both can be read out, neither is something Claude sees on its own:

**Codex/GPT** — the Codex CLI has no usage command, but the server sends a `rate_limits` block
with every answer, which the CLI writes into its session file
(`~/.codex/sessions/JJJJ/MM/TT/rollout-*.jsonl`). Fully evaluated:

```bash
~/.claude/codex-limit.sh          # "Codex (plus): 10 % vom 7d-Fenster verbraucht, Reset in 5d 2h  [… vor 24 h]"
~/.claude/codex-limit.sh --kurz   # "codex 10%/7d"  (steht so in der Statuszeile)
~/.claude/codex-limit.sh --json
```

An honest limitation that is ALWAYS stated along with it: the number is only as fresh as the
last Codex run. Whoever has not used Codex for days sees an old state — and that one is more
likely too high than too low, because the window has moved on in the meantime. The script names
the age of the measurement itself; this age belongs in the Handoff too.

**Claude Code** — one's own 5-hour and weekly percentages are ONLY in the status line's stdin
JSON, not in the model context. The status line therefore stores them at every render:

```bash
cat ~/.claude/.claude-kontingent   # {"stand":"…","fuenf_stunden_prozent":3,"sieben_tage_prozent":0}
```

Here too: the `stand` timestamp belongs with it, and in case of deviations from the web interface
(Settings ▸ Usage) the web interface is the authority — it counts everything, the terminal field
only the Claude Code share and in steps.

**What this becomes in the Handoff:** a short block **right at the top**, directly after „Der
Stand in drei Sätzen", never at the end. Three lines are enough — two numbers and a suggestion
(output template, stays German):

```

## Was noch im Tank ist

- **Codex/GPT:** 10 % vom Wochenfenster verbraucht, Reset in 5 Tagen
  (gemessen beim letzten Codex-Lauf, vor 24 h) → 90 % frei.
- **Claude Code:** 5h 3 % · Woche 0 % (Stand 14:12).
- **Vorschlag:** Codex hat viel Luft — die Startzeit-Analyse und der
  9-Stunden-Langzeittest wären genau die Sorte Arbeit dafür.
```

Tone: casual and inviting, never admonishing — it is a paid allowance, not a budget that has to
be conserved. The suggestion is the actual point: when a lot is free, Claude names CONCRETELY
which open items from „Der rote Faden" (the red thread — the running list of open threads) could
be dealt with (big analyses, long-running tests, second opinions, migrations) — not "you could
use more", but "with that we could do X and Y".

**If a lot is free, something BIG is proposed — that is what this block is for.** Unused
allowance expires. It does not carry over into the next week, it is simply gone; the loss is the
expiring window, never the spending. Whenever the 5-hour or the weekly window still has real
headroom, Claude says so AND names something that is worth doing with it. Yasin's own image:
„Schau mal, check mal alles durch, ob das gut ist." Good candidates, precisely because they are
expensive and never urgent:

- a pass over the entire project with HIGH thinking depth ("ultrathink") — architecture, dead
  code, contradictions; the things nobody schedules;
- a quality check of a whole area against its acceptance criteria, not just against the last diff;
- a big second-opinion analysis on another model (Codex/GPT) — a different architecture sees
  different errors than another read-through by the same one;
- a long test run that nobody volunteers to sit through: startup times, long-running tests, a
  full matrix.

Phrased as an invitation with a number next to it: „90 % der Woche sind noch frei — das ist der
Moment für den großen Review, billiger als auf schon bezahltem Kontingent wird er nie."
Never: „du solltest dein Kontingent mehr ausnutzen."

And: if an allowance is nearly empty (> ~85 %), that belongs in the same block just as much, with
the reset time next to it — then the message is „bis morgen früh lieber die kleinen Sachen",
which is the same information from the other side.

### Wake-up ping for the Codex display (Yasin 27.08.2026)

His wish, after `codex-limit.sh` on one day only returned
`{"primary": null, "secondary": null, "plan": "plus",
"alter_minuten": 107}`, i.e. no number at all: „Ja gerne
einbauen bitte. Auch in dem Skill einbauen. Auch in GitHub
warm-handoff."

**The problem:** `codex-limit.sh` does not read the allowances
live but from the LAST Codex session file. The number is
therefore only as fresh as the last Codex run — if that was
hours ago, the script shows an outdated state or, as above,
none at all. **`null` does not mean "0 % used"**,
but "since the last run no new `rate_limits`
block has arrived, the value is unknown" — a zero would be a
fabrication here, the same trap as with time of day and context size.

**The solution:** once per session issue a tiny Codex call
so that the server sends a fresh `rate_limits` block:

```bash
codex exec --skip-git-repo-check "Antworte nur mit: bereit"
```

- **When:** once per session, at the start — appended to a
  command that runs anyway (e.g. the session's first real
  Codex job), NEVER as its own, otherwise
  additional call just for measuring.
- **Cost named honestly:** this costs a few Codex tokens —
  negligible against a paid weekly allowance, but
  not zero. Therefore append it to a call that is due anyway,
  do not start it specially for this.
- **If Codex is not installed or not logged in:** quietly
  move on, report no error — the ping is a bonus
  for the display, not a mandatory step of the session.
- Afterwards `codex-limit.sh` shows the fresh state, and the
  "vor X h" in the Handoff block above matches
  reality again.

### Thinking about Codex, Gemini and OpenRouter together (Yasin 27.08.2026)

His instruction, after the wake-up ping was in place: „Nee, das ist
super, macht es." Meaning: see all THREE allowances as ONE picture,
not just Codex.

**The common core: with all three, whatever is not used
expires.** Codex on a paid subscription runs out within a
weekly window, whether used or not. Gemini provides
free requests which likewise expire with the window.
OpenRouter offers free models (Yasin uses
"Ox Alpha" there, among others, as a second reviewer) — there too an
unused request is not credit for next time, but
simply gone. The same attitude as with the Claude allowance above:
do not conserve, USE IT UP, as long as the window is running.

**Assignment — which work fits whom:**

| Work | Provider | Why |
|---|---|---|
| Large read/analysis/review runs, going through the whole project | Codex or OpenRouter | A different architecture sees different errors; expensive and rarely urgent — exactly what an expiring allowance is for |
| Second opinion on one's own code / one's own answer | Codex or OpenRouter (e.g. Ox Alpha) | No-self-review rule — Claude must not proofread itself |
| Rebuilds IN the code | Claude | Stays in the driver's seat, knows the history and the decisions |
| Research, very long contexts | Gemini | Large context window, built exactly for that |

**How to see the state — and where honestly nothing is measured:**

- **Codex:** `~/.claude/codex-limit.sh` (see above), fresh after the
  wake-up ping. Shows the percentage of the 7-day window plus
  reset time.
- **Gemini and OpenRouter:** here there is no script and no
  reliable measurement — no account balance is invented. Say honestly:
  „Bei Gemini/OpenRouter kann ich den Kontingentstand
  nicht auslesen, nur den Nutzungshinweis in der jeweiligen
  Oberfläche zeigen." A `~` or an estimated percentage
  would be the same fabrication here as with time of day or
  context size above — therefore deliberately omitted instead of guessed.

**Tone:** inviting, with a number next to it, never admonishing — as with the
Codex block above. If a lot is free with Codex, that is named AND
a fitting candidate is proposed right away („90 % der Woche
noch frei — das wäre der Moment für den großen Zweitmeinungs-
Lauf mit Ox Alpha oder Codex"). With Gemini/OpenRouter it stays
an invitation without a number: „Wenn dort noch Kontingent offen
ist, wäre jetzt der Moment für die Recherche/den Zweitreviewer"
— without claiming how much that is exactly.

## The wave workflow (the heart of this skill)

The economics reward a specific rhythm:

- **The user batches work into waves (Welle = wave)**: one big message with many tasks.
  Claude works through it (subagents welcome — they cache separately at 5 min, so batch
  their jobs too). During the wave the cache stays warm by itself; short back-and-forth
  messages in between are cheap — small side-topics are *encouraged* while the main work
  runs.
- **After each wave, Claude writes a handoff document** (Handoff = the written baton-pass
  artifact): a dated Markdown file (`_handoff-<projekt>-YYYY-MM-DD[-b].md`) containing what
  was delivered, running state, open items, project constraints — **and the current test
  checklist (Testliste = test list) at the bottom**. **Pre-seed every test item with an
  answer line**, ready to dictate into:

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

**The PATH of the handoff goes RIGHT AT THE TOP of the document — first of all,
before everything else.** The user opens the handoff in the editor; the file path is
nowhere visible there, and for the next session they have to supply it. Without that
line they piece it together in the Finder or type it out. That is why every handoff
begins with a ready-made hand-over sentence to copy — one line, selectable with a
double-click and pasteable straight into the fresh session:

```
> **Für die nächste Session — diese Zeile kopieren und einfügen:**
> `Ich habe das Handoff beantwortet: /Users/…/projekt/_handoff-projekt-2026-08-25.md`
```

Absolute path, no tilde shorthand (the agent would have to resolve that first), and in
backticks so a double-click grabs the whole thing.

**The project name belongs IN the file name — not just the date.** Users work in
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

3. **Collection area for the running session (Sammlung = collection area; Yasin
   25.08.2026).** Right at the end, after everything else, a third heading — the place
   where the user collects things WHILE Claude is working on the next wave:

   ```
   ---
   ## Sammlung für das nächste Handoff

   Alles, was dir während der laufenden Welle einfällt, hier hinein.
   Ich rühre diesen Abschnitt nicht an — ich lese ihn nur, wenn ich das
   nächste Handoff schreibe.

   >>>
   ```

   His reason, verbatim: „Wenn ich dir ein Handoff übergeben habe, fallen mir während
   du arbeitest neue Sachen ein, die will ich sammeln … sonst muss ich ein neues
   TextEdit-Dokument öffnen, dort sammeln, und dann Copy-Paste machen." (roughly: while
   you work, new things occur to me and I want to collect them without opening a second
   document and copy-pasting).

   **The rule about this is hard: Claude NEVER writes into a handoff the user is
   currently writing in.** A new handoff is always a NEW file; the old one stays word for
   word as he left it. His second annoyance hung on exactly this („dann sagt das Dokument
   ungesicherte Änderungen, und plötzlich ist meine Sammlung weg"): if Claude edits a file
   that is open in the editor, the versions collide. If the active file is never written
   to, that cannot happen.

   When the next handoff is written, the collection area is read along with the test
   answers — every point in it is either answered or carried into the red thread (Der
   rote Faden = the through-line/roadmap section), so it is visible that nothing was lost.

   **And open the SECOND-TO-LAST handoff again (Yasin 25.08.2026, 14:14).** His wish
   verbatim: „Vor dem neuen Handoff schauen, ob im alten Handoff was dazu gekommen ist,
   und nur diese Änderungen dann im neuen Handoff erwähnen." The reason is practical: he
   keeps collecting AFTER he has handed the handoff over — those lines therefore only
   come into being while Claude is already working on the wave, and would otherwise
   appear nowhere. Procedure when writing a new handoff:

   1. Read the handoff that was just answered (as always).
   2. **Additionally the one before it** — only the section „Sammlung für das nächste
      Handoff". If something stands there that does not appear in the current handoff,
      it is new.
   3. These points go **right at the top** of the new handoff, under a heading of their
      own such as „Aus deiner Sammlung übernommen" — one line per point saying what
      happens with it (answered / built in / landed in the red thread). That way he sees
      immediately that his interjections arrived, without doing copy-paste himself.
   4. Only then does the old handoff move to the archive.

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

**Closing the old handoff — only after a check IN THE SAME call (Yasin
25.08.2026, 14:21 — a real case of data loss).** His sentence: „Vorhin habe ich in der
alten Handoff-Liste, die du automatisch geschlossen hast, schon was Neues reingeschrieben
gehabt … aber das ist jetzt verloren gegangen, weil du es ja geschlossen hast." That is
exactly what happened: the unsaved-changes guard had run minutes earlier, the closing came
later, and in between he had kept writing. A check that does not sit immediately before
the action is worthless.

**SHARPENED on 26.08.2026, 14:07 — Claude does NOT close the old handoff at all any
more.** Yasin's reasoning verbatim: „Wenn ich unten was reinschreibe und das noch
nicht gespeichert habe, und du schließt dann das alte Handoff, nachdem du gearbeitet
hast — dann kannst du es ja gar nicht schließen, wenn ich da noch ungesicherte
Änderungen drin habe. Deswegen würde ich fast sagen: das alte Handoff gar nicht
schließen, sondern offen lassen, dass der User das schließt."

He is right, and the reason is more fundamental than the data loss of 25.08.: the
collection area exists precisely so that he keeps writing WHILE the wave is running.
Exactly at the moment when Claude finishes and wants to tidy up, the probability is
highest that unsaved text is sitting there. A cleanup step that strikes at just that
moment can only lose.

The rule is therefore now:

1. **The old handoff stays open. Period.** Claude does not close it, does not save
   it, does not touch it. The user closes it himself when he is done.
2. **Before the new handoff is written, its content is read anyway** — including the
   collection area, and via the unsaved-changes guard so that unsaved lines arrive too
   (`get text of (first document whose name is "…")`). Reading is harmless; only
   closing and writing are not.
3. **The new handoff is ALWAYS a new file** with a new name. That way there is never a
   collision between Claude's version and what lies open in the editor.
4. **Archiving (`mv`) happens only once the user has closed the document** — or not at
   all in this wave. A handoff still open in the editor is not moved; instead the new
   handoff notes in one line that archiving is still pending.
5. **Close + reopen remains exactly ONE exception:** when Claude itself has changed the
   file that the user has open (otherwise he reads a stale version). Even then the check
   applies in the SAME call, and on `modified: true` it is NOT closed but asked about.

When in doubt, always: **better one window too many open than one line of the user's
gone.**

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
- Concrete arithmetic for the sweetspot (Sweetspot = the optimal hand-off point): a
  300-step wave at 220k context ≈ 300 × 22k ≈ 6.6M equivalents; the same wave in a fresh
  ~30k session ≈ 0.9M. A fresh session's rebuild is cheap because the new prefix is
  small — the expensive thing is never the handoff, it is running a big wave on top of a
  fat context.
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
- **A map, not just a to-do remainder (Yasin 25.08.2026).** The „Offen (nächste Wellen)"
  block at the end is good, but it only says what is STILL to come — not where the project
  knowledge lives. Every handoff therefore gets a short block **„Hauptdokumente"** (main
  documents) directly before it: the 3–6 files that really carry the current state
  (roadmap, project status, overview of open topics, current concept papers), each with an
  absolute path and ONE line saying what is in it and how fresh it is. Example:

  ```
  ## Hauptdokumente (wo was steht)

  - `/Users/…/projekt/ROADMAP-MASTER.md` — Fahrplan aller Wellen (Stand 23.08.)
  - `/Users/…/projekt/PROJEKT-STATUS.md` — was fertig/in Arbeit ist (Stand 25.08.)
  - `/Users/…/projekt/UEBERSICHT-OFFENE-THEMEN.md` — Themenspeicher, gröber als
    die Restliste unten
  ```

  Rules: only list documents that REALLY exist (check beforehand), mark outdated ones
  explicitly as outdated instead of quietly dragging them along, and never copy the
  content into the handoff — the path is the whole point („Reference, don't copy").
- **The lower part is a red thread, not a keyword list (Yasin 25.08.2026).**
  His wish: „dass man da unten nicht nur die Fragen und Tests hat, sondern einen roten
  Faden sieht, roadmapartig — was als nächste Welle kommt, was die übernächste, kurz, mit
  ein paar Details, damit man sich erinnert und motiviert ist, noch was dazuzuschreiben."

  So: the remainder list `Offen (nächste Wellen)` becomes a short **roadmap with answer
  fields**. One paragraph for each of the next two or three waves — what is coming, why,
  and one or two details that bring the thought back to mind. Then the same invitation as
  with the tests:

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

  The rest (the long enumeration of all open points) stays below it as a topic store —
  compressed, without answer fields. The roadmap is the invitation to think along, the
  list is the memory.
- **Archive old handoffs, never delete them (Yasin 25.08.2026).** Once a new handoff is
  written and its answers are incorporated, the PREVIOUS one moves into a subfolder
  `handoff-archiv/` of the same project (create it if missing):

  ```bash
  mkdir -p "<projekt>/handoff-archiv"
  mv "<projekt>/_handoff-projekt-2026-08-24-b.md" "<projekt>/handoff-archiv/"
  ```

  Move, don't delete — the user tidies up himself if he wants to. That way there is
  always only ONE active handoff in the project folder, and the question „which is the
  right one?" no longer arises. The new handoff names the archive folder in one line so
  the way back stays visible. Only archive when the old document contains no unprocessed
  answers any more (otherwise it stays put, with a note in the new handoff).
- One deliberate difference: Pocock writes handoffs to the temp directory (transit document)
  and recommends `/compact` for same-directory continuation. This skill writes them **into
  the project** (dated, part of the working rhythm, the user annotates them) and prefers
  handoff + fresh session over `/compact` past the context threshold — on subscription
  plans, `/compact` keeps the huge expensive prefix alive; a fresh ~20k session does not.

## RECOGNIZING a cache rebuild and announcing it (Yasin 25.08.2026)

His wish: „Wenn sich so ein Cache neu aufbaut, bekommst du das mit und kannst du das
dem User dann sagen — dass der Cache gerade neu aufgebaut hat, weil er eben zu spät war
oder was auch immer der Grund war."

**CORRECTION of 26.08.2026 — there IS a signal, and a hard one at that.** What used to
stand here was „es gibt kein Signal, das einen Cache-Miss meldet". That was wrong: every
line of the session file carries `cache_creation_input_tokens` (written at the 2× price)
next to `cache_read_input_tokens` (read at the 0.1× price). **The ratio of the two sums IS
the hit rate.**

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

Interpretation: **below ~10 % written/read = the cache was warm.** Individual lines with a
large new write are almost always ADDITIONS (the transcript grows, the new part is written
once), not rebuilds. A real rebuild looks different: a lot of writing with almost no
reading.

**Why this matters — it clears up the most common misunderstanding.** Yasin asked on
25.08. and again on 26.08.: „269 Anfragen — heißt das, du hast 269-mal den Cache neu
aufgebaut?" No. And without this measurement the answer was a mere assertion. With it,
it is evidence: in the measured session 22,171k read against 562k written —
**2.5 %**, with only 6 of 147 requests showing any notable new write.

**What still does NOT work:** reading the CAUSE of a miss out of the data. Whether the
pause was too long, a model switch came in between, or it was evicted server-side — the
file does not say. For that, the derivation below applies — and with no established
cause, nothing is asserted.

**The three cost items that belong in every explanation** (the third was long left out):
cache read ×0.1 · cache write ×2 · **own output ×5**. In the measured session the output
made up almost a quarter of the total cost. Long answers and detailed handoffs are worth
their money, but they are not free — anyone who only talks about context size explains
only two thirds of the bill to the user.

**And a rule for Claude itself:** every interim message („Agent X ist fertig") is a FULL
request and costs as much as a user message — at 200k context roughly 20k equivalents. If
several agents land shortly after one another, their reports get bundled instead of being
sent individually.

**What does work — reliably:** measuring the gap. A cache miss through time expiry is by
far the most common cause, and it is derivable from two `date` readings:

1. Read `date` with every answer anyway (rule 1 above). The last time read is thereby
   known — it stands in one's own previous text.
2. Read it again on the next turn. Difference > 60 minutes (or > 5 minutes if the
   session is demonstrably running in 5-minute mode) ⇒ the cache was gone, and the
   current turn rebuilt it.

Then ONCE, in passing, with reason and number:

> „Nebenbei: zwischen deiner letzten Nachricht und dieser lagen 1 h 40 — der Cache ist
> in der Zeit abgelaufen und mit diesem Turn neu aufgebaut worden. Kein Beinbruch, nur
> damit du weißt, warum die Antwort etwas teurer war als sonst."

Further causes that Claude also knows FOR CERTAIN, because it was its own action or it
stands in the transcript — those may be named too:
- a model or effort switch in the middle of the session,
- a change to CLAUDE.md / to the system prompt during the session,
- an MCP server that restarted (visible from an error message in the transcript).

Causes Claude CANNOT see (plan limit reached → 5-minute TTL, server-side eviction) are
not guessed at. If none of these causes is established, the rule is: say nothing.

Two rules about tone: **once per event, not as a standing warning**, and never as a
reproach — the user took a break, that is his right. The sentence serves as explanation
(„why did quota just disappear there"), not as education. The logbook entry gets the same
finding as a line with cause and estimated waste.

## Long agent runs, the user as bottleneck, Fable low (Yasin 28.08.2026)

Three rules that come out of the Welle (wave) of 27./28.08.2026. All three share
the same core: **The most expensive resource is not the model, it is the
human waiting for it — and every request that happens only because someone
wants to report „fertig" (done).**

### a) Agents running longer than an hour deliver into a FILE

A subagent whose work is expected to take **longer than one hour**
(research, review with many sources, large rebuilds) does not report its
result into the chat, but **writes it into a file** — convention:
`docs/reviews/<YYYY-MM-DD>-<topic>.md` (or the place customary in the
project).

Why: If the agent finishes after 90 minutes, the main session is either
long since on a break (cache cold, the completion ping triggers a
rebuild) or it is actively waiting and burning requests while it does.
Both are more expensive than a file that simply sits there.

Procedure:

1. **At the start** the orchestrator tells the agent the target path and the
   assignment: „Schreib das Ergebnis nach `docs/reviews/2026-08-28-x.md`.
   Melde dich erst, wenn die Datei vollständig ist; die Meldung darf nur
   den Pfad und zwei Sätze enthalten." (write the result to that path;
   report only once the file is complete, with just the path and two
   sentences).
2. **In the Handoff (handover document)** the orchestrator enters a line
   stating which file is **expected** from which agent:

   ```
   ## Erwartete Agenten-Ergebnisse
   - [ ] docs/reviews/2026-08-28-tageszeit-und-kontingente.md (Recherche-Agent, gestartet 17:02)
   - [ ] docs/reviews/2026-08-28-skills-mcp-ballast.md (Analyse-Agent, gestartet 17:05)
   ```

3. **The NEXT session** checks first thing, while reading the handoff,
   whether the expected files exist (`ls docs/reviews/`), ticks them off and
   reads them in the course of reading the handoff — **within the same first
   request**. That way the agent finishing costs no request of its own, no
   rebuild and no waiting time.
4. If an expected file is missing, that goes into the first status block of
   the new session („Review-Datei X fehlt — Agent abgebrochen?"), instead of
   silently disappearing.

Result in numbers: two reviews of 200–600 lines each arrived that way in the
follow-up session on 27.08. — as part of the first request instead of as two
additional completion pings into a 220k session (2 × 22k equivalents saved,
plus no rebuild after the night break).

### b) The user is the bottleneck — cut waves so they run through

Yasin, 28.08.2026: The human cannot sit at the terminal all the time; every
question that halts a wave costs hours of real time, not seconds. Therefore:

- **Cut waves so that as much as possible runs WITHOUT a question.**
  If an assignment has two readings that are both defensible: take the more
  likely one, mark it in the handoff („angenommen: X; falls Y gemeint war,
  ist die Änderung in Datei Z rückgängig zu machen"), and keep working. Stop
  only when a wrong assumption destroys data, costs money or has outside
  effects (push, mail, order).
- **Questions are COLLECTED into the handoff**, not asked one by one in the
  chat. A section `## Fragen an dich` with prepared answer lines
  (`>>>Antwort:`) that the user answers in the editor whenever he wants. One
  question in the chat blocks; ten questions in the handoff block nothing.
- **Agents get several tasks bundled** and report only once EVERYTHING is
  done — not after each subtask. Three assignments to one agent are one
  completion ping; three agents with one assignment each are three requests
  in the main context. Bundle as long as the tasks do not block each other
  or drive the runtime past an hour (then rule a applies).
- **The assignment to the agent contains the contract:** what the result is,
  where it goes, how long the report may be, and explicitly „keine
  Rückfragen — entscheide selbst und dokumentiere die Annahme" (no
  questions — decide yourself and document the assumption).

### c) Fable 5 as agent model: ALWAYS effort low

User rule (Yasin): If Fable 5 is used as a subagent model, then
**exclusively with effort low**. Reason: Fable low is fast and cheap enough
for mechanics, research and text work; the higher effort eats time and quota
without the results in these tasks getting any better. For tasks that really
need high effort (design decisions, security review), choose a different
model (Opus 5, or Codex/GPT-5.6 as a second opinion) — do not turn Fable up.

When starting an agent, model and thinking depth stand visibly in the
description, so the user sees it in the terminal:

```
gut:  "Fable/low · Kostentabelle aus Session-JSONL bauen"
```

## Honesty rules

- There is no background timer: Claude only acts when a request arrives. That is exactly why
  the handoff is written *proactively at the end of a wave*, not "when the hour is nearly up".
- Cost claims should be shown as arithmetic when it matters (cache-write vs. re-read pricing),
  not asserted.
- A cache rebuild is reported when it is DERIVABLE (see section above) — never guessed.

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

## Four rules from the handoff test of 29.08.2026 (Yasin)

### a) The Sammlung (collection) is copied VERBATIM — and read in the same call

What happened: the session of 28.08. read the „Sammlung für das nächste
Handoff" (collection for the next handoff) at ~16:45, then worked for 3
hours, and wrote the new handoff at 19:45 — **without reading the
collection again.** Everything Yasin had entered there between 18:53 and
19:42 (eight items: microphone warning, system audio quality, HUD
transparency, sleep-mode look, filter reset …) was missing from the new
handoff. He had to copy it in himself the next day and rightly asked:
„Hast du das mitgenommen? Ich bin mir unsicher."

Two rules, both hard:

1. **The collection is read IMMEDIATELY before the new handoff is
   written** — in the same tool call as the unsaved-changes guard, not
   hours earlier. A reading that does not stand directly before the
   writing is worthless (the same principle as with closing old
   handoffs, 25.08.).
2. **It is copied one to one, not rewritten.** Yasin, verbatim (29.08.,
   13:22): „Wenn du das wieder umschreibst, dann weiß ich nicht mehr, ob
   es die letzte Sammlung ist." At the very top of the new handoff there
   is therefore a block:

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

   First the copy (so the user can SEE the comparison), then the
   mapping. Summarizing is allowed — but only IN ADDITION to the
   verbatim copy, never instead of it.

### b) Use Codex according to account size — small account = quality assurance only

Yasin, 28.08. 20:08, after Codex was stuck in the 5-hour limit and the
proposal was to give it the main work from 23:05 on: „Nein,
ich bin mit dem Vorschlag nicht einverstanden. Wenn Codex so knapp
ist, dann sollten wir Codex nur für wichtige Qualitätsmanagement-
Sachen nutzen — der soll dann nur prüfen — und nicht, dass wir zwei,
drei Stunden warten, bis der wieder Kontingent hat. Ich habe nur
einen Zwanzig-Dollar-Account bei Codex. Nicht versuchen, jedes
letzte Tröpfchen Token auszusaugen."

The section "Use up the paid quota" above stays correct — but it applies
to the quota one HAS. The rule thereby becomes account-dependent:

| Codex account | Use |
|---|---|
| Small (Plus, ~$20/month: tight 5h window) | **Checking work only:** code review, second opinion, test runs, acceptance. No build assignments, no night shifts, no "carry on from 23:05". If the window is not enough, Claude (or an Opus subagent) does the work — do not wait. |
| Large (Pro/Team, wide window) | As before: use generously, also for rebuilds and long analyses. |

Why this does not contradict "use up the quota":
With the small account the 5-hour window is the bottleneck, not the
week. A build assignment eats it in an hour, and then Codex is missing
exactly where it has the greatest value — as a DIFFERENT architecture
that sees Claude's mistakes. Checking work is short, targeted and
valuable; the main work Claude can do itself. Whoever enlarges the
account switches the row — the skill asks once at setup which account is
in place, and remembers it.

### c) The end marker must stand out — Markdown does not help in the editor

Yasin, 28.08. 20:00: „Kann man denn nicht Buchstaben größer machen?
Bei MD geht das nicht, gell. Das ‚Hiermit sind Fragen … zu Ende'
müsste eigentlich auffälliger sein."

Correct: in TextEdit a `##` heading is just two hashes in front of normal
text. What stands out in plain text are **lines and whitespace**, not
markup. The two closing blocks (end marker, collection area) therefore
get a banner line:

```
═══════════════════════════════════════════════════════════
   ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
   Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
═══════════════════════════════════════════════════════════

>>>Userantwort:
```

Capitals, double line, three blank lines before it. That works in any
editor without rendering.

### d) "Which agents are working right now?" — what the host shows and what it does not

Yasin's question (28.08. 18:53, screenshot of the status line): whether it
can say down there WHICH agents are working. Honest answer:

- **What is visible:** Claude Code lists running background agents with
  their short description under the input line ("← for agents"). That is
  why model + thinking depth belong in that description (rule of 26.08.:
  „Opus5/high · Thema") — then everything is right there.
- **What does NOT work:** the own status line (`ctx 17% | 7d:10%`) is not
  handed an agent list by the host; it cannot display one. Whoever wants
  it there has to unfold the host's agent display.
- **The single announcement in the chat when the fleet starts** remains
  the complete overview: how many agents, which model, which work
  package. After that, radio silence.

## Guiding principle — the whole skill in one sentence (Yasin 29.08.2026, 14:01)

> **Handoff → frische Session → Handoff.** Der Nutzer sammelt über
> Stunden alles in EIN Handoff (Antworten, Ideen, Kritik), startet
> eine neue Session, der Agent arbeitet alles durch und schreibt das
> nächste Handoff — und dazwischen immer eine frische Session.

Why this is the most economical rhythm: the costs sit in the requests
(each one reads the whole history), not in the user's messages. So: keep
the main context small (a fresh session per wave), put the work into few
subagents with SEVERAL tasks (few reports = few requests), and make the
handoff thorough — with cost table, Testliste (test list), Der rote Faden
(the red thread, i.e. the running narrative) and the verbatim collection —
because it replaces a whole context. A thin handoff saves nothing; it
shifts the costs into follow-up questions.

Three details that belong with it (all from 29.08.2026):

- **Tab suggestions from the terminal are requests.** Claude Code shows
  grey suggestion lines; whoever accepts one with Tab and sends it off
  triggers a full request (context × 0.1). The line cannot be labelled —
  it comes from the program. Only use it if you really want the
  suggestion.
- **Agent completion pings are requests from the program, not from the
  agent.** Every "Agent X finished" message wakes the main agent — that
  is a request, even if it stays silent. Its one-liner about it („zwei
  von sieben durch") only costs ~50 tokens of extra output. What SAVES
  requests is not silence, but fewer, larger agents (three tasks in one =
  one completion ping).
- **The collection area carries the path of its handoff** in the banner
  line („aus: /Users/…/_handoff-projekt-2026-08-29.md"), so that with
  several handoffs open it is clear which collection this is — and the
  path is ready to copy.

## Wave 23 — cheap in tokens, but 2 hrs 20 through a serial tail (29.08.2026)

Wave 23 (Aitomat, merge report see commit `1f308c86`) ran with few, larger
agents according to the old rule above ("three tasks in one = one
completion ping"). Result: **cheap by measurement** (little main context
consumed, few completion pings), but **2 hours 20 minutes of wall-clock
time**, because the agents did not really run at the same time — several
tasks in one agent means the agent works through them INTERNALLY one after
another, and if a second Wächter (guardian agent) waits for the first one's
result before starting its own workers, a serial tail of waiting times
arises that no cost line shows. Yasin waited ~3 hours for a result that
could have been finished, in substance, in a fraction of the time.

The lesson: **token cost and wall-clock time are two different axes.**
Fewer/larger agents save requests (axis 1), but bundle work serially in
wall-clock time (axis 2) — expensive precisely when the user is waiting
instead of working alongside. The rule is therefore sharpened, without
discarding the old insight:

- **One working agent = ONE assignment, ~30 minutes** (instead of ~40
  minutes / 2–3 tasks). A single focused assignment can be finished faster
  AND merged faster, without the internal processing of several tasks in
  the same agent creating an invisible queue.
- **The Wächter starts ALL workers in a single message** simultaneously,
  never one after another — the serial kick-off was the actual cause of
  the tail in wave 23, not the number of agents itself.
- **Every worker first pulls the current branch tip** before touching
  anything — with parallel instead of serial execution, an outdated base
  is otherwise more likely, because several workers branch off from the
  same state at the same time.
- **Merge immediately on landing, not collected** — whoever waits for the
  last worker in order to do all merges at once builds the serial tail
  back in at the end.
- **Full test suite only once, right at the end**, against the merged
  result — not after every single merge, otherwise the runtime of the
  suite multiplies by the number of workers.
- **The Wächter writes an interim status after 60 minutes**, in case the
  wave is still running, and **the handoff starts even without a finished
  Wächter** — in wave 23 an interim status after an hour would have shown
  the user that he is not waiting on a hung system.

In short: fast AND cheap needs both — small assignments AND real
simultaneity at the start. One alone is not enough.

## 29.08.2026, 23:35 — The machine crash

Wave 24: the Wächter started 12 workers at the same time, each in its own
worktree with its own cold build. 400+ swift-frontend processes, load ~70 on
12 cores, 18 GB RAM → swap → the machine froze, Yasin had to reboot; the
session broke off, 90 minutes lost. Yasin: „Sowas sollte nicht mehr
passieren." Rule: workers do not build; only the Wächter builds, once,
serially.

## Wave 25 — one Wächter per topic area (30.08.2026)

Yasin, 30.08.2026, in substance: „Je Themenbereich ein Opus-Wächter, der
auf 3–5 Arbeiter aufpasst, Aufträge 15–25 Minuten."

After wave 23 (cheap, but 2 hrs 20 through a serial tail) and wave 24 (fast
in theory, but a machine crash through 12 simultaneous cold builds) it was
clear: ONE Wächter per wave is the wrong size. It is a bottleneck when it
leads too many workers, and it can no longer order the build access. Hence
the rules of wave 25:

- **One Wächter PER TOPIC AREA** (interface, audio, tests, docs …), each
  with **at most 4–6 workers** (Yasin's number was 3–5; 4–6 is the upper
  limit recorded in the skill). Each topic Wächter merges into its own
  integration branch. The **main session** brings the integration branches
  together and then starts **one merge Wächter** for the single build, the
  full suite, the bundle and the QA round. That way the main session is
  woken once per topic instead of once per worker — and still remains the
  instance that knows the overall state.
- **Assignments of 15–25 minutes** instead of ~30. Shorter assignments land
  closer together; a Wächter with five workers otherwise waits for the
  slowest and builds the serial tail back in on a small scale.
- **Build lock:** `mkdir /tmp/<projekt>-build.lock` before every build,
  `rmdir` afterwards. `mkdir` is atomic, so the lock works across agents,
  worktrees and sessions. Never more than one build per machine — the
  mechanical version of the lesson of 29.08.
- **Model choice:** Fable 5 as a worker only for assignments the user has
  marked as "important" (there the faster model pays off); everything else
  Opus/low. **Sonnet only for trivial work without building.**

Also made precise on 30.08. (from the Codex review of 29.08.):

- **Parallel beats serial within a wave.** The old contradiction ("the
  Wächter starts all of them at once" vs. "user absent → serial") is
  resolved like this: a Wächter ALWAYS starts its workers in parallel. The
  pacing rule applies only to non-Wächter work of the main session.
- **Escalation exception:** questions belong in the handoff — except for
  irreversible/destructive actions, security/credentials, anything visible
  from outside, real money being spent, or repo contents going to external
  models. There, ask in the chat immediately, before acting.
- **Cost calculation for subagents corrected:** the first step of a fresh
  subagent pays its start context ×2, only afterwards ×0.1. Break-even at
  220k main and 30k agent context: 60k ÷ (22k − 3k) ≈ 7 steps per agent.
  Shorter assignments you do yourself.

## Wave 25 — the numbers (30.08.2026)

Wave 25 ran from 00:46 to 01:50 — 64 minutes — with 3 topic Wächter
(topic guardians) plus 1 merge Wächter (merge guardian), 15 workers, 29
requests, 1,192k equivalent tokens, 5 completion pings, and no crash.
For comparison: wave 22 needed 58 requests / 2,075k / ~2 hours, wave 23
43 requests / 1,531k / 2 hrs 20, and wave 24 62 requests / 3,143k /
2 hrs 10. The topic-Wächter structure was therefore the cheapest AND the
fastest so far. It dissolves the trade-off of wave 23 (cheap, but slow),
because the topic guardians start their 4–6 workers in parallel and the
merge guardian pulls the serial tail — build, full suite, bundle, QA —
together into a single pass instead of repeating it per worker.

From this follows a rule about the NUMBER of guardians: one guardian per
disjoint topic with 4–6 assignments. Below 4 assignments the start-up
overhead (start_ctx × 2) does not pay off, and above 6 the guardian itself
becomes the bottleneck.

## Wave 26 — plan as a file, labels, push, Codex as quality manager (30.08.2026)

Four rules come from this night, each from a sentence Yasin said while the
wave was running. His words are kept in German, verbatim.

**1. The wave plan becomes a file the user can read (02:28).**

> „Mir gefällt es sehr gut mit diesem Plan für drei Wächter … dass du da so
> das dann öffnest und dann dass ich mir es anschauen kann, das ist eine
> sehr gute Maßnahme. Das sollten wir auch im Skill aufnehmen"

Before wave 26 the plan for a wave lived in the prompts of the guardians —
the user could see the agents running but not what they had been told to
do. Writing it as `docs/reviews/<date>-welleN-plan.md` first, committing
it, opening it in TextEdit and only THEN starting all guardians in one
message costs one file and buys two things: the user can look the wave over
before it is expensive to change, and every guardian reads the same text
instead of a paraphrase of it. The file has structure rules on top and one
table per topic (ID · assignment · acceptance criterion · model/effort).

**2. Labels also for the workers, not only the guardians (02:31).** The
user reads the list of running agents at the bottom of the screen and wants
model and effort visible there. So a guardian labels the workers it spawns
the same way the main session labels the guardians: `Modell/Effort · ID
Kurzname`, e.g. `Fable/low · A1 Aufnahme-Rot`. One thing has to be said out
loud rather than left as a puzzle: Codex is a shell command, not an agent,
so it never shows up in that list at all.

**3. Push belongs to the job (02:36).** The user looked at GitHub during the
wave and saw nothing moving. The cause was not a slow agent — the skill
agent had committed but never pushed. Hence: every guardian and every skill
agent pushes its branch before it reports done, and names the pushed hash
in the report. Local-only work is not delivered work.

**4. Codex as quality manager of the wave (03:05).** With a fresh Codex
quota, every topic guardian has its integration branch reviewed by Codex
BEFORE the closing report and fixes the P1 findings itself. The evidence
that this is worth a call: in job A7 of this wave, Codex found four P1
issues across three Fable assignments that the building agents had missed.
The wave then ends reviewed instead of "to be reviewed later".

**The numbers of wave 26.** 02:24–03:17, 53 minutes: 3 topic guardians +
1 merge guardian + 1 skill agent, 17 assignments, 34 requests, 1,159k
equivalent, 5 completion pings, main-session context flat at 114k. It is a
control measurement for wave 25 (29 requests / 1,192k / 64 min for 15
assignments) and it confirms it: the structure repeats.

## Wave 27 — the ceiling of the guardian structure (30.08.2026)

03:39–04:57, 78 minutes: 4 topic guardians + merge guardian + skill agent,
Codex quality-manager pass per guardian, 19 assignments, 41 requests,
1,160k equivalent, 7 completion pings (plus one stray worker message and
one API abort). The fourth guardian cost no extra tokens but 25 extra
minutes: guardian B alone ran 45 minutes, and for the first time the merge
guardian had conflicts to resolve, because two topics (HUD crash, HUD
recording indicator) edited the SAME files. Lesson: **cut topics along
files, not along words** — same files, one guardian, however differently
the two jobs are named.

Three side findings of the wave, now rules in SKILL.md: a worker whose
guardian has already finished reports into the main session instead — read
it, do not restart the work; an agent killed by an API error is resumed
with `SendMessage` to the SAME agent, not replaced by a fresh one; and
when the user says "Absturz", `~/Library/Logs/DiagnosticReports/*.ips`
belongs to the session-start look — six crash files all named the same
line and turned a vague report into a one-line fix.

## "Dreaming" and dosed commits (Yasin, 30.08.2026, 15:05)

> „Wegen Langzeitgedächtnis haben wir dann sowas wie Dreaming drin. Das
> heißt, wenn du sowieso schon die Session dann schließt … dass du dann
> eben mit jeder Session das Gedächtnis, das Kurzzeit-/Langzeit-, dann
> auffrischt, und das wollen wir halt je Projekt zusammenhalten … im
> Handoff gleichzeitig das Memory, und dann sieht der User das, der kann
> auch mal was dazu sagen oder löschen … und natürlich nicht extra Kosten
> haben."

Hence: the `## Gedächtnis` block of the handoff is refreshed as a STEP of
writing the handoff — no extra agent, no extra request — one memory per
project, inside the handoff, visible and editable by the user. Claude's
own memory file is no longer filled; one place, not two.

> „Wegen GitHub: Da haben wir halt gestern hundertachtundfünfzig
> Contributions gemacht. Das sollte man vielleicht doch nicht so
> übertreiben … dass wir pro Tag maximal eher fünfzig Contributions
> haben, wenn wir so viel arbeiten wie gestern … nicht für jeden
> Kleinkrimskrams ein Contribution."

Hence: workers commit freely on their own branch, but the guardian folds
each worker branch in with `git merge --squash` and ONE commit per
assignment. Target ≤ 50 commits a day even on full days.

## "Die Moral der Geschichte" (Yasin, 30.08.2026, 15:06)

> „Ja und ansonsten habe ich immer noch nicht kapiert, was das Sparsamste
> ist in Sachen Warm-Handoff-Skill. Wie sollten wir da am besten arbeiten,
> was ist denn jetzt die Moral der Geschichte? … alles immer sammeln, jede
> Session, soweit es geht, aber eben tokensparend sammeln … und weiterhin
> dokumentieren, die nächsten Tage, um ganz sicher zu gehen, was wie viel
> Verbrauch ist, und da eben den Warm-Handoff-Skill perfektionieren."

Hence the new section at the top of SKILL.md, "Die sparsamste Arbeitsweise
in fünf Sätzen": one session per wave, collecting costs nothing, guardians
instead of pings, stay under 200k context, close with a handoff carrying
the cost table — plus the resolution to measure every session with one
logbook line for the next few days.
