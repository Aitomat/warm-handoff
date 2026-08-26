---
name: warm-handoff
description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, measures context size, request count and cache hit rate from the session file instead of guessing, keeps the number of requests down (subagents first), warns before cache-destroying actions, surfaces the paid quota left in Codex and Claude Code, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", "quota", or when resuming after a gap.
---

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

*By Yasin Akgün ([github.com/Aitomat](https://github.com/Aitomat)) — grown out of daily
work on the macOS app [Aitomat](https://aitomat.ai) and sharpened continuously against
measured numbers, not invented at a desk. The dated quotes throughout are his, from the
sessions that produced each rule.*

Claude Code caches your conversation prefix. Working *inside* that cache is fast and cheap;
rebuilding it is slow and expensive. This skill makes the cache window visible, keeps you
inside it, keeps the number of requests small — and, when leaving is the better deal,
writes the handoff that lets a fresh session continue seamlessly.

It is also meant to TEACH. Every cost claim in here comes with the arithmetic behind it,
because a user who understands why a fat context is cheap to talk on and expensive to work
on will make better calls than one who is merely told to "be efficient".

## The facts (verified against Claude Code docs, 2026-08)

- **Pro/Max subscription: 1-hour cache TTL, sliding.** Every message and every cache hit
  resets the 1-hour timer. Stay under one hour between exchanges and the cache lives forever.
- **Fallback:** if you exceed plan limits and draw on paid usage credits, Claude Code drops
  to a 5-minute TTL automatically.
- **Subagents always use a strict 5-minute TTL**, even on Max.
- Env overrides: `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1`.
- **The three cost items, and all three matter:** cache read ×0.1 · cache write ×2 ·
  **your own output ×5**. The write factor depends on the TTL — **2× for the 1-hour
  storage** (the normal case on Pro/Max), 1.25× only for the 5-minute one. Using 1.25
  prices a rebuild about 60 % too cheap; this is the single most common arithmetic error
  in cache discussions.
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
   which grows context fast), read the current context size and state it in the reply.
   A threshold that nobody measures is decoration — this exact failure happened in
   practice: the user crossed 400k unnoticed while Claude was busy orchestrating, and
   had to point it out himself.

   **NEVER guess the context number — same rule as the clock (Yasin, 25.08.2026).**
   Claude cannot feel how full its context is. A sentence like "cache is fresh (~20k)"
   written without looking is a fabrication, and it is worse than saying nothing: the
   user reads it as a measurement and plans the wave around it. The real number at that
   moment was ~80k. Only three sources count:

   - the **status line** the user's terminal renders (`ctx 15% used (85% left)`) — if the
     user pastes or screenshots it, use exactly that number;
   - a monitor/tool call made in THIS turn that reports it;
   - **your own measurement — and this is the best of the three.** Yasin pushed back on
     this: *"it's odd that you can't see your own total context size — surely there must
     be a way."* He was right. Claude Code writes every request, `usage` block included,
     into the session file at
     `~/.claude/projects/<cwd-with-dashes>/<session-id>.jsonl`. The last line carrying
     `usage` has `cache_read_input_tokens + cache_creation_input_tokens` — that IS the
     current context size. One bash call is enough:

   ```bash
   proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"
   sess=$(ls -t "$proj"/*.jsonl | head -1)
   SESS="$sess" python3 -c '
   import json, os
   lines = open(os.environ["SESS"], "rb").read().decode("utf-8","ignore").splitlines()
   inp=out=cw=cr=0
   for l in lines:
       try: u=(json.loads(l).get("message") or {}).get("usage")
       except Exception: continue
       if not u: continue
       inp+=u.get("input_tokens",0); out+=u.get("output_tokens",0)
       cw+=u.get("cache_creation_input_tokens",0); cr+=u.get("cache_read_input_tokens",0)
   for l in reversed(lines):
       try: u=(json.loads(l).get("message") or {}).get("usage")
       except Exception: continue
       if u:
           print(f"context: {(u.get(\"cache_read_input_tokens\",0)+u.get(\"cache_creation_input_tokens\",0))/1000:.0f}k"); break
   print(f"API equivalent: ${(inp*15+out*75+cw*18.75+cr*1.5)/1_000_000:.2f}")'
   ```

   That makes the sweetspot announcement (below) defensible at any moment, without the
   user having to transcribe a status line. This measurement belongs at every wave end.

   Two honest limits: the file is appended per request, so the number is the state of the
   LAST request, not of this second. And the dollar figure is the API equivalent at list
   prices (the constants above are Opus-tier rates — adjust them for your model) — nobody
   on a Pro/Max subscription pays that sum; it measures what the quota is being charged.

   None of the three sources available → write "context: not measured" (or leave it out).
   The same goes for the closing line of a handoff: an invented "~60k" there is the same
   mistake, just archived.

   **What the status-line fields mean** (users ask, and the numbers look contradictory):
   - `ctx N% used` / `ctx 148k` — how full THIS conversation's context window is.
     Nothing to do with billing or quota; it resets to zero in a fresh session.
   - `5h:3%` — the rolling 5-hour usage window. Matches "current session" in the web UI
     under Settings ▸ Usage.
   - `7d:0%` — the weekly window as Claude Code sees it. This can differ sharply from
     the web UI's "all models 59 %", because the web number aggregates EVERYTHING
     (chats, other models) while the terminal field tracks the Claude-Code slice — and
     it updates in steps, not live. When they disagree, the web UI is the authority;
     say so instead of explaining the gap away.
   - The web UI also lists per-model bars (e.g. "90 %") with their own reset time. A red
     bar there is the real constraint even when the terminal shows 0 %.
5. **Recommend a fresh session at the sweetspot.** The threshold is not one number — it
   depends on what the NEXT stretch of work looks like:

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
   WORK on. Below ~150k, none of this matters; chat freely. And past ~500–600k answer
   quality degrades from sheer information load even while the cache is warm.
6. **Write the handoff automatically after every big work wave** — do not wait to be asked.

## The real lever: FEWER REQUESTS (26.08.2026)

This skill spent a long time focused on context size. A full measurement of one real
working session showed that was only a third of the truth:

| Item | Tokens | Factor | Equivalent |
|---|---|---|---|
| Cache read | 22,171k | ×0.1 | 2,217k |
| Cache written | 562k | ×2 | 1,125k |
| **Own output** | 208k | **×5** | **1,038k** |

**147 requests — 13 of them triggered by user messages.** The other 134 were Claude's own
tool-steps and interim status notes. And Claude's own OUTPUT accounted for nearly a
quarter of total cost — the item this skill previously did not mention at all.

Three goals follow, in this order: **fewer requests · shorter own output · smaller
context.** The handoff (this skill's original purpose) is the WEAKEST of the three levers.

### The technique list (cross-checked with a second model)

A second model (GPT-5.6 via Codex) was given the same numbers and estimated what each
technique would have saved in exactly that session. Target picture: **35–55 requests in
the main context instead of 147**, total cost from 4,380k down to 1,350–2,050k.

| Technique | How | Effect |
|---|---|---|
| **Batch tool calls** | Request every independent read/search/check in ONE reply, in parallel, and only then evaluate | −25 to −45 requests |
| **Script instead of single commands** | One call that does ten things and prints ONE summary, instead of ten calls | −20 to −35 requests |
| **Cut agents by work package** | ONE agent does "find cause + build fix + check tests", not three agents doing one part each | −30 to −60 requests |
| **Keep the orchestrator context lean** | The agent gets paths, goal, constraints, acceptance criteria — never the chat history | −0.2 to −0.5M read |
| **Reports as files** | The agent writes detail into a file; what comes back is result, risks, path | −0.3 to −0.7M |
| **Cap report length** | State it in the assignment: max 300 words, no work chronicle, no pasted logs | −0.2 to −0.4M output |
| **Bundle interim reports** | See the rule below | −15 to −30 requests |
| **Pre-filter output** | `grep`/`jq`/`tail` before printing; success in one line, on failure only the relevant lines | −0.1 to −0.3M |
| **Own output budget** | Interim notes ≤100 words, closing summary ≤500 words, detail into files rather than the chat | 208k → 50–80k output |
| **Hand off earlier** | At 100–120k instead of 223k | −0.3 to −0.7M read |

(The effects overlap and must not be added up.)

### Subagents are the default route, not the exception

The goal, as Yasin put it (26.08.2026): *"work with a strong model that acts as the boss, sends the
subagents out, uses few tokens, says everything in one bundle and makes few requests."*

Why that adds up: a subagent starts at ~10–20k instead of the full main context. Its 100
work-steps therefore read 100 × ~15k instead of 100 × ~220k. In the measured session six
agents together burned over a million tokens — none of which landed in the main context
except the assignments and the closing reports.

**When a subagent does NOT pay off** (honesty matters here too): below roughly 3–5 tool
steps, for strictly sequential work, or when a lot of shared context would have to be
transferred first. Its startup cost is roughly 1–3 requests plus briefing plus report.

**The subagent contract**, which belongs in every assignment:

> Work until you have a result or hit a real blocker. Report only: status, decisions,
> evidence with paths, risks, next step. At most 300 words, no work chronicle, no pasted
> logs or diffs — put detail in a file.

### Output is expensive — write shorter

Output costs **five times** the price of fresh input and fifty times a cache read. In
practice:

- **Don't narrate your own work.** What the user already sees in the terminal does not
  need to be repeated in prose.
- **Long content belongs in files**, not in the chat — that is exactly why the handoff is
  a file and not a chat message.
- **No "here's the whole thing again, just to be safe" version.** A pointer to the file
  is enough.
- The handoff itself stays thorough: it replaces an entire context and is therefore the
  best investment on the list. Thorough ≠ chatty.

### This skill should TEACH, not just keep time

Yasin's explicit request (26.08.2026, 16:53): *"the skill should also teach. People should understand
how this actually works — what happens to me happens to a lot of people."*

So for every cost statement made to the user:

1. **Number first, rule second.** Not "that's expensive", but "that's 22k equivalents,
   because the context is 220k and reading costs a tenth".
2. **Clear up misunderstandings actively.** The most common one: "X requests = X cache
   rebuilds". Wrong — see "Spotting a cache rebuild" below.
3. **Name your own mistakes.** When an earlier explanation was off (in one case: "saved
   almost half" — recalculated, it was closer to a third), correct it out loud rather
   than silently overwriting it.

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

## Spotting a cache rebuild — and saying so (25./26.08.2026)

Yasin's wish behind this: *"when the cache rebuilds, do you notice — and can you tell the user
that it just happened, and why?"*

**There IS a signal, and it is a hard one.** An earlier version of this skill claimed there
was none. That was wrong: every line of the session file carries
`cache_creation_input_tokens` (written at the 2× price) next to `cache_read_input_tokens`
(read at the 0.1× price). **The ratio of the two sums IS the hit rate.**

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
u=[(json.loads(l).get('message') or {}).get('usage') for l in open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines() if '\"usage\"' in l]
u=[x for x in u if x]
cr=sum(x.get('cache_read_input_tokens',0) for x in u); cw=sum(x.get('cache_creation_input_tokens',0) for x in u)
big=[x.get('cache_creation_input_tokens',0) for x in u if x.get('cache_creation_input_tokens',0)>20000]
print(f'{len(u)} requests · read {cr/1000:.0f}k · written {cw/1000:.0f}k ({cw/max(1,cr)*100:.1f} %) · large writes: {len(big)}')"
```

Reading it: **below ~10 % written/read = the cache was warm.** Individual lines with a
large write are almost always APPENDS (the conversation grows, the new part gets written
once), not rebuilds. A real rebuild looks different: lots of writing with almost no reading.

**Why this matters — it settles the most common misunderstanding.** Yasin asked on 25.08.
and again on 26.08.: "269 requests — does that mean you rebuilt the cache 269 times?" No. And without this
measurement the answer was a mere assertion. With it, it is evidence: in the measured
session, 22,171k read against 562k written — **2.5 %**, and of 147 requests only 6 had a
noteworthy write.

**What still does NOT work:** reading the CAUSE of a miss out of the data. Whether the
pause was too long, a model switch intervened, or the server evicted it, the file does not
say. For that, use the derivation below — and with no established cause, claim nothing.

**What does work, reliably:** measuring the gap. A cache miss by timeout is by far the most
common cause, and it is derivable from two `date` reads:

1. Read `date` in every reply anyway (rule 1 above). The last time read is therefore known
   — it stands in your own previous text.
2. Read again on the next turn. Difference > 60 minutes (or > 5 minutes if the session is
   demonstrably in 5-minute mode) ⇒ the cache was gone, and this turn rebuilt it.

Then say it ONCE, casually, with cause and number:

> "By the way: 1 h 40 passed between your last message and this one — the cache expired in
> the meantime and was rebuilt with this turn. No harm done, just so you know why this
> answer cost a bit more than usual."

Other causes Claude also KNOWS for certain, because they were its own action or stand in
the transcript — those may be named too:
- a model or effort switch mid-session,
- a change to CLAUDE.md / the system prompt during the session,
- an MCP server that restarted (visible as an error in the transcript).

Causes Claude cannot see (plan limit reached → 5-minute TTL, server-side eviction) are not
guessed at. If none of these is established: say nothing.

Two rules on tone: **once per event, not as a standing warning**, and never as a reproach —
the user took a break, which is their right. The sentence exists to explain ("why did quota
just disappear"), not to educate. The same finding goes into the logbook entry as a line
with cause and estimated waste.

## When does the hour actually start? (users always ask this)

The 1-hour timer resets on **every request in the session** — not just the user's
messages. That includes each of Claude's own tool-steps, and each status message Claude
emits when a background subagent finishes. Consequences worth telling the user:

- The hour counts from **Claude's last output**, whichever side produced the last
  activity. "Agent Y finished, here's the handoff" at 16:30 → the user has until ~17:30
  to answer warmly. Reading costs the user nothing; only their reply is a new request.
- While Claude waits on subagents, its own tool-steps keep the cache warm automatically —
  no dedicated keep-alive is needed during active waves.
- Work through subagents by default for heavy lifting: they run in their own small
  contexts (5-min TTL, cached separately), so the main context stays lean.

## Pacing: parallel for speed, sequential for warmth

Subagents are not just a context-saver — their SCHEDULING is a cache instrument. Two modes,
chosen by what the user needs right now (ask, or react to cues like "I'm in a hurry" /
"I'm going to bed"):

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

### Choosing WHICH subagent — cheap/fast vs. strong/slow

Picking the tier is part of the plan, not an afterthought. State the choice out loud in one
clause ("three readers on the fast model, the review on the strong one"), so the user can
veto before the tokens are spent.

| Work | Tier | Why |
|---|---|---|
| Finding files, listing call sites, mechanical renames, log sifting | fast/cheap, low effort | Answer is verifiable at a glance; a strong model adds nothing |
| Writing tests to an existing pattern, doc sweeps, format fixes | fast/cheap, low effort | The pattern is already decided |
| Design decisions, security/correctness review, "why is this wrong" | strong, high effort | Errors here are expensive and hard to spot later |
| Anything the user will ship without re-reading | strong | Treat it as production |

Cross-checking your OWN output is a separate job — a second opinion from a different model
(Codex/GPT, a second reviewer) catches what a same-architecture re-read cannot.

### Sequential vs. parallel — decide it, then say it

- **"I'm in a hurry"** → make a short plan first, then fan out in parallel. Say how many
  agents and what each one owns.
- **User is away / the steps depend on each other** → chain them one after another (also
  the cache-warm mode above).
- **Mixed** is normal: fan out the independent reads, then run the dependent build/review
  steps in sequence.

### Make the work visible — but do not narrate it

The user watches a status line and a task list, not Claude's reasoning. So:

- **Keep a live to-do list** for any task with more than ~3 steps, and update it as steps
  finish — that list IS the progress bar. Never let it go stale; a finished step still
  marked "in progress" is worse than no list.
- **Announce the whole fleet ONCE when it starts** — one block, what each agent owns.
  Then radio silence until the end.
- **Name the running total** at wave end: how many agents ran, what came back, what is
  still open.

**REVOKED on 26.08.2026 — no more per-agent status notes.** This section used to say
"announce each subagent when it starts AND when it lands, those lines double as
cache-refreshing requests". That was expensive and pointless. Yasin's objection, verbatim: *"You don't need to give me feedback when one has stopped. Then it stopped — until
they're all done, or until nearly an hour has passed so you keep the cache warm. I can see
in my terminal window that subagents are working."*

He is right on both counts:

1. **The host already shows running agents.** A line saying "agent 3 is done" is
   information the user already has in front of them — paid for with a full request.
2. **As cache warmers these notes are unnecessary,** because Claude's own tool-steps reset
   the timer at every step anyway. The note warms nothing that wasn't already warm.

The rule now:

- **During a wave, do NOT report per agent.** If five agents land, ONE summary is written
  when the last one is through.
- **Report on exactly three occasions:** a decision the user has to make · a blocker that
  cannot move without them · a completed milestone.
- **The clock is the exception:** if the user is present and the wave has been running for
  nearly an hour with no sign of life, send ONE bundled interim note — so the cache window
  doesn't lapse and they aren't left in the dark.
- **For a single long-running agent** (no fleet) the same applies: wait for the result,
  don't comment that it started.

Arithmetic from the measured session: five individual status notes at ~220k context are
roughly 110k token equivalents — for text the user is already looking at.

### Stay terminal- and tool-neutral

Some users run a multiplexer, others a plain Terminal/iTerm/Ghostty, VS Code, or a
different agent CLI entirely. Everything in this skill must survive that:

- Never assume a specific terminal's UI. Say "your status line", not the name of one
  particular field. If a feature exists only in one host (panes/surfaces, a custom status
  line), mark it as such in one clause and give the generic fallback.
- The handoff document is the portable artifact: a plain Markdown file any agent in any
  tool can read. Never encode state in a terminal-specific place instead.
- When another agent (Codex/GPT, Gemini) does the work, the SAME rules apply — timestamp,
  measured context, handoff, archive. Hand it the handoff file, not a chat summary.

## CALCULATE the sweetspot and announce it

Yasin's wish, verbatim (25.08.2026): *"Could we calculate the sweetspot and then
say: hey, you've reached your sweetspot, that's why I wrote a handoff, the wave just
finished too, better start a new session — that would be the most elegant thing."*

That works, and without magic. Two numbers suffice, both readable:

```
remaining steps in the window ≈ (target context − current context) / growth per step
```

- **Current context**: measured (rule 4) or from the status line — never guessed.
- **Growth per step**: from this session itself. Two data points are enough: context at the
  last handoff, context now, divided by the number of waves/steps in between. In practice:
  a build wave with tests costs roughly 40–80k, a round of conversation 2–5k.
- **Target context**: 200k / 250k / 300k depending on what comes next (table above).

That turns into an announcement the user can actually use — not "your context is big", but
**how much still fits**:

> "Context 148k, target 200k before the next build wave — that's good for about one more
> wave or a dozen questions. After that I'll write the handoff."

**When this announcement comes (unprompted):**
- at the end of every wave, together with the measured context number;
- as soon as the remaining budget drops below ONE further wave — then say it plainly:
  "that was the last wave for this session, the handoff is written, start fresh tomorrow";
- whenever the user asks where things stand.

**Tone (Yasin's explicit request):** short, casual, motivating — never admonishing. "Room for
about 2 more waves" is a streak counter, not an invoice. And when the budget gets tight,
the practical hint is welcome too: "from here on, better to collect longer messages instead
of many short ones" — the same thought from the user's side.

Honest limit: growth per step varies a lot (a screenshot costs more than a text reply). The
estimate is an order of magnitude, not a promise — phrase it that way ("about", "roughly"),
and always put the measured context number next to it.

### COUNT the startup cost of a fresh session

Yasin's objection, verbatim (25.08.2026): *"You're not accounting for the fact that a new
session starts at 70,000 tokens for me, and that gets multiplied by two because the cache
is rebuilt. So the calculation in our skill isn't perfect yet."*

He was right, and the evidence was in the same session (the Aitomat project): the
measurement taken right after
session start, before a single line of work, was **82k** — not the "~20k" this skill
assumed in several places. Skills, tool schemas, system prompts and project rules are
already there before the user does anything. The 20k figure was too optimistic and must be
MEASURED per project rather than guessed.

The full calculation has three items, not two — and the cache-write factor hangs on the
TTL: **2× for the 1-hour storage** (the Pro/Max default), 1.25× only for the 5-minute one.
Cache read stays 0.1×.

```
Rebuild, ONE-TIME       = start context × 2      (1-h TTL; × 1.25 only on 5-min TTL)
Step in the new session = start context × 0.1
Step in the old session = current context × 0.1
Break-even (in steps)   = (start context × 2) / ((old − new) × 0.1)
```

Example from the session: start 82k, current 287k → rebuild ~164k, saving 20.5k per step →
**break-even at ~8 steps.**

**The sentence most often misread:** "steps" are NOT the user's messages, but overwhelmingly
Claude's own tool calls. From which the rule that actually holds:

- **Only talking / going through the test list / a few small fixes** (< ~6 steps) → STAY,
  even at 260k+. The rebuild would cost more than it saves.
- **A build wave, a review, a migration** (hundreds of steps) → SWITCH as soon as the
  context is well above the start context. Break-even arrives around the sixth step;
  everything after that is pure gain.

That is why the sweetspot announcement ALWAYS carries this session's measured start context
and the question "what comes next?" — without both, the recommendation is a guess.

### COUNT the steps, don't estimate them

Yasin's follow-up assignment (25.08.2026): *"We need to look at how many steps that really is — the skill
should calculate it, know it, and show it to the user."*

Doable, and exactly: every request to the model stands as a line with `usage` in the
session file. Start context, current context, number of requests, and the share the user
triggered are all directly readable. This one call produces the complete sweetspot maths:

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
z = open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines()
u_all=[]; real_user=0
for l in z:
    try: d=json.loads(l)
    except Exception: continue
    m=d.get('message') or {}
    if m.get('usage'): u_all.append(m['usage'])
    if d.get('type')=='user':
        c=m.get('content')
        if isinstance(c,str): real_user+=1
        elif isinstance(c,list) and not any(isinstance(p,dict) and p.get('type')=='tool_result' for p in c): real_user+=1
k=lambda u:(u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0))/1000
start,now,n = k(u_all[0]), k(u_all[-1]), len(u_all)
save=(now-start)*0.1
fresh=start*2   # 1-h TTL (Pro/Max). On a demonstrable 5-min TTL: start*1.25
print('start %.0fk - now %.0fk - %d requests, %d of them from the user (%.1f steps per message)'
      % (start,now,n,real_user,n/max(1,real_user)))
print('a new session costs ~%.0fk once; saves %.1fk per step; break-even after %.0f steps'
      % (fresh, save, fresh/save) if save>0 else 'context still at start level - stay')
"
```

What the numbers mean, and how they become an announcement:

- **"Requests" is the number that counts — not the user's messages.** In a real build wave,
  205 requests stood against 15 user messages: roughly 14 steps per message on average, far
  above 100 inside the wave itself, and exactly 1 in conversation rounds. That is precisely
  why a fat context is cheap to TALK on and expensive to WORK on.
- **Break-even in steps** says when switching pays. If the expected step count of the next
  task is below it → stay. Above → switch.
- The announcement names both numbers and the recommendation in one sentence, e.g.:
  "287k, start was 82k — a switch costs ~102k once and pays off from ~5 steps. Going
  through the test list: stay. Next build wave: switch."

This measurement belongs at every wave end and in every answer to "should I start fresh?".

## Dictating into the terminal: keep it short, long stuff goes in the document

Important for anyone who speaks their messages instead of typing them:

**Terminals collapse long input into a placeholder.** Past a certain length many terminals
show only `[pasted text]` — the user then does NOT see what they actually said, cannot skim
it, cannot correct it, cannot find it again. A long dictation is effectively sent blind.

From which follows the division of labour this skill recommends anyway — now with the
concrete reason behind it:

- **Short messages belong in the terminal**: one question, one assignment, one correction.
  Short enough that it stays visible as text.
- **Everything long belongs in the handoff document in the text editor**: test answers,
  ideas, braindumps, criticism. There the user sees every word, can keep working for days,
  add and rearrange — and the agent reads the whole document in one go at the end.
- This is not a compromise, it is the better route: a handoff may grow for weeks until it
  is full. Then a fresh session, document in, off you go.

Claude says this to the user ONCE per setup — not on every long message.

## Make the paid quota visible — and use it up

Yasin's wish, verbatim (26.08.2026, 14:03): *"Can you even see whether I still have enough limit in
Codex? Could that be made visible — and could you point it out now and then? If I have an
account I pay for monthly, then the tokens should get used if there are any left. The skill
could say: hey, we've got time now, we still have plenty of tokens left in Codex or in your
weekly quota — think about what we could do with them. And that belongs right at the top of
the handoff, as the headline information."*

Both numbers are readable, and Claude sees neither on its own.

**Codex/GPT** — the Codex CLI has no usage command, but the server sends a `rate_limits`
block with every response, which the CLI writes into its session file
(`~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`). The last such block is the current state.
Save this as `~/.claude/codex-limit.sh`, `chmod +x` it, and it prints one line:

```bash
#!/usr/bin/env bash
# codex-limit.sh — how much of the Codex/GPT quota is used up.
#
# Where the number comes from: the Codex CLI has NO usage command. But the
# server sends a `rate_limits` block with every response, and the CLI writes
# it into the session file under ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl.
# The last such block is the current state.
#
# HONEST LIMIT: the number is only as fresh as the last Codex run. If you
# haven't used Codex for three days, you see a three-day-old state (and it is
# then more likely too high than too low — the window keeps moving). That is
# why the age of the measurement is always printed with it.
#
# Usage:
#   codex-limit.sh          -> one line for humans
#   codex-limit.sh --short  -> compact for the status line ("codex 10%/7d")
#   codex-limit.sh --json   -> raw values

set -uo pipefail
mode="${1:-}"
cache="$HOME/.claude/.codex-limit-cache${mode:+${mode//-/}}"

# Status lines render often — cache the result for 5 minutes.
if [ "$mode" = "--short" ] && [ -f "$cache" ]; then
  age=$(( $(date +%s) - $(stat -f %m "$cache" 2>/dev/null || echo 0) ))
  if [ "$age" -lt 300 ]; then
    cat "$cache"
    exit 0
  fi
fi

# Find the newest session file: scan the most recent day folders instead of the
# whole tree (too expensive on every render). The newest file need not be the
# one carrying a limit block (aborted runs), so keep looking until the first hit.
sess=""
for cand in $(ls -t "$HOME"/.codex/sessions/*/*/*/*.jsonl 2>/dev/null | head -40); do
  if grep -q '"rate_limits"' "$cand" 2>/dev/null; then
    sess="$cand"; break
  fi
done

if [ -z "$sess" ]; then
  [ "$mode" = "--short" ] || echo "Codex: no session data found"
  exit 0
fi

SESS="$sess" MODE="$mode" python3 <<'PY' > "$cache.tmp" 2>/dev/null
import json, os, time

path = os.environ["SESS"]
mode = os.environ.get("MODE", "")
last = None
with open(path, "rb") as f:
    for line in f.read().decode("utf-8", "ignore").splitlines():
        if '"rate_limits"' not in line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        # The block sits nested inside a token_count event.
        stack = [d]
        while stack:
            k = stack.pop()
            if isinstance(k, dict):
                if "rate_limits" in k and isinstance(k["rate_limits"], dict):
                    last = k["rate_limits"]
                stack.extend(k.values())
            elif isinstance(k, list):
                stack.extend(k)

if not last:
    raise SystemExit(0)

measured = os.path.getmtime(path)
age_min = (time.time() - measured) / 60

def window(b):
    if not b:
        return None
    p = b.get("used_percent")
    wm = b.get("window_minutes") or 0
    name = "7d" if wm >= 9000 else ("5h" if wm >= 250 else f"{wm}m")
    rest = ""
    ra = b.get("resets_at")
    if ra:
        s = ra - time.time()
        if s > 0:
            rest = f", reset in {int(s//86400)}d {int((s%86400)//3600)}h" if s > 86400 else f", reset in {int(s//3600)}h"
    return {"percent": p, "name": name, "rest": rest}

p1 = window(last.get("primary"))
p2 = window(last.get("secondary"))
plan = last.get("plan_type") or "?"

if mode == "--json":
    print(json.dumps({"primary": p1, "secondary": p2, "plan": plan,
                      "age_minutes": round(age_min)}, ensure_ascii=False))
elif mode == "--short":
    parts = [f"codex {x['percent']:.0f}%/{x['name']}" for x in (p1, p2) if x and x["percent"] is not None]
    if parts:
        print(" ".join(parts))
else:
    age = f"{age_min/60:.0f} h" if age_min >= 90 else f"{age_min:.0f} min"
    if age_min >= 2880:
        age = f"{age_min/1440:.0f} days"
    print(f"Codex ({plan}): " + " · ".join(
        f"{x['percent']:.0f} % of the {x['name']} window used{x['rest']}"
        for x in (p1, p2) if x and x["percent"] is not None
    ) + f"  [measured at the last Codex run, {age} ago]")
PY

if [ -s "$cache.tmp" ]; then
  mv "$cache.tmp" "$cache"
  cat "$cache"
else
  rm -f "$cache.tmp"
fi
```

Honest limit, always stated alongside: the number is only as fresh as the last Codex run.
Someone who hasn't used Codex for days sees a stale state — and it is more likely too high
than too low, because the window has moved on. The script names the age of the measurement
itself; that age belongs in the handoff too.

**Claude Code** — your own 5-hour and weekly percentages exist ONLY in the status line's
stdin JSON, not in the model context. So have the status line drop them on every render.
Add these lines to your `statusLine` command script (`~/.claude/statusline-command.sh` or
wherever yours lives) — the values come from the JSON the status line already receives on
stdin:

```bash
input=$(cat)
five=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

# Deliberate side effect: Claude cannot see its own quota percentages — they
# exist only in this stdin JSON. So park them in a file the skill can read.
if [ -n "$five" ] || [ -n "$week" ]; then
  printf '{"as_of":"%s","five_hour_percent":%s,"seven_day_percent":%s}\n' \
    "$(date '+%Y-%m-%d %H:%M')" "${five:-null}" "${week:-null}" \
    > "$HOME/.claude/.claude-quota" 2>/dev/null
fi
```

Claude then simply reads it:

```bash
cat ~/.claude/.claude-quota   # {"as_of":"…","five_hour_percent":3,"seven_day_percent":0}
```

Here too: the `as_of` timestamp belongs with the number, and where it disagrees with the
web UI (Settings ▸ Usage), the web UI is the authority — it counts everything, the terminal
field only the Claude-Code slice and only in steps.

**What this becomes in the handoff:** a short block **right at the top**, directly after the
three-sentence status, never at the end. Three lines are enough — two numbers and a
suggestion:

```
## What's left in the tank

- **Codex/GPT:** 10 % of the weekly window used, reset in 5 days
  (measured at the last Codex run, 24 h ago) → 90 % free.
- **Claude Code:** 5h 3 % · week 0 % (as of 14:12).
- **Suggestion:** Codex has plenty of room — the startup-time analysis and
  the 9-hour endurance test are exactly the kind of work for it.
```

Tone: casual and inviting, never admonishing — it is paid quota, not a budget to be
conserved. The suggestion is the actual point: when a lot is free, Claude names CONCRETE
open items from the roadmap that could be cleared with it (big analyses, long-running
tests, second opinions, migrations) — not "you could use more", but "with that we could do
X and Y".

And: if a quota is nearly exhausted (> ~85 %), that belongs in the same block just as much,
with the reset time next to it — then the message is "until tomorrow morning, better stick
to the small stuff", which is the same information from the other side.

## The window as a friendly coach (frame it this way)

Present the 1-hour window, the handoff ritual and the test list as POSITIVE motivators,
never as pressure or cost-anxiety. The sliding hour is a natural work rhythm: "answer
within the hour and the wave keeps riding" is the same gentle pull as a streak — it
nudges the user to test the delivered items now, dictate answers now, fire the next wave
now, while everything is fresh. The pre-seeded test questions make re-entry effortless
(no blank page — just put the cursor after the marker and speak). Claude should
occasionally voice this framing ("window's still warm — perfect moment for the test
list"), and celebrate kept streaks in the logbook rather than only counting waste.

## The wave workflow (the heart of this skill)

The economics reward a specific rhythm:

- **The user batches work into waves**: one big message with many tasks. Claude works through
  it (subagents welcome — they cache separately at 5 min, so batch their jobs too). During
  the wave the cache stays warm by itself; short back-and-forth messages in between are cheap
  — small side-topics are *encouraged* while the main work runs.
- **After each wave, Claude writes a handoff document**: a dated Markdown file
  (`_handoff-<project>-YYYY-MM-DD[-b].md`) containing what was delivered, running state,
  open items, project constraints — **and the current test checklist at the bottom**.
  **Pre-seed every test item with an answer line**, ready to dictate into:

  ```
  ## T3 — Dark/light toggle inverted
  <test description>

  >>>Answer:
  ```

  (Use the user's language for the marker — e.g. `>>>Userantwort:` for a German user.)

  The user just places the cursor after the marker and speaks. An item whose answer line
  stays empty simply wasn't tested yet — that's information too, not an error.
- **The user works in the handoff file with a plain text editor** (TextEdit or similar), not
  in the chat box: they answer each test point directly beneath it, and collect new ideas and
  findings in the same file — even across a long pause. Why an editor and not the terminal:
  chat inputs collapse long pastes into `[pasted text]`, so the user loses overview; in the
  editor they see the whole document. **Rule: save (⌘S) before telling Claude to read it** —
  unsaved editor changes are invisible on disk.
- **Next session starts with only the handoff** — a fresh, small context instead of 500k+,
  fully briefed, cache rebuilt once at minimum size. **Do not promise "~20k": measure it.**
  Skills, tool schemas and project rules are loaded before the user does anything — in the
  Aitomat project that floor was 82k (see "COUNT the startup cost of a fresh session"). Claude
  reads the annotated test answers and new ideas from the file and starts the next wave.

**The PATH of the handoff goes RIGHT AT THE TOP of the document — first, before anything
else.** The user opens the handoff in an editor; the file path is nowhere visible there,
and for the next session they have to supply it. Without this line they hunt for it in the
file manager or retype it. So every handoff starts with a ready-made handover sentence to
copy — one line, selectable by double-click, pasteable straight into the fresh session:

```
> **For the next session — copy and paste this line:**
> `I've answered the handoff: /Users/…/project/_handoff-project-2026-08-25.md`
```

Absolute path, no tilde shorthand (the agent would have to resolve it first), and in
backticks so a double-click grabs the whole thing.

**The project name belongs IN the file name — not just the date.** Users work in several
projects/sessions in parallel, and parallel sessions produce handoffs on the SAME day.
`_handoff-2026-08-24-b.md` is then ambiguous: which project is it from? Rule: every handoff
file name carries the project name, e.g. `_handoff-myproject-2026-08-24-b.md`. Same for the
`# Title` line inside the file (`# Handoff myproject — 24.08.2026, 23:40 (wave 9 B)`) and
for the logbook entry, so a file that has drifted out of its folder is still identifiable.
The suffix `-b`, `-c` … stays for the second/third handoff of one day within the same
project.

**Three fixed blocks at the very bottom of EVERY handoff** — after the last test item, in
this order:

1. **A free field for the user.** A short closing sentence marks the end of the Q&A/test
   part and invites everything that came up outside the list — new instructions, ideas,
   tips, tasks, gripes. Example (in the user's language):

   ```
   ---
   ## That's the end of the questions, answers and tests.

   Space for everything else — new instructions, ideas, tips, tasks
   that occurred to you:

   >>>Answer:
   ```

   Without this field, everything not covered by a test question has no home and gets lost
   between waves.

2. **Context state + "the next wave starts fresh"** as the last line of that part. Name the
   measured context size of the ending session and state explicitly that the next wave
   starts in a fresh session — this is the reassurance that a fat context is not a problem
   the user has to worry about:

   ```
   *Context of this session: ~285k. The next wave starts fresh out of exactly
   this handoff — nothing is lost.*
   ```

   Use the actually measured number (see rule 4 above); no measurement → write no number,
   not a guessed one. And don't promise a fresh-session size you haven't measured either.

3. **A collection area for the running session.** Last of all, after everything else, a
   third heading — the place where the user collects things WHILE Claude works on the next
   wave:

   ```
   ---
   ## Collection for the next handoff

   Anything that occurs to you during the running wave goes in here.
   I won't touch this section — I only read it when I write the next
   handoff.

   >>>
   ```

   Yasin's reason, verbatim: *"Once I've handed you a handoff, new things occur to me while
   you're working and I want to collect them … otherwise I have to open a new TextEdit
   document, collect there, and then copy-paste."*

   **The accompanying rule is hard: Claude NEVER writes into a handoff the user is
   currently writing in.** A new handoff is always a NEW file; the old one stays word for
   word as it was left. That was the source of a second complaint — *"then the document
   says unsaved changes, and suddenly my collection is gone"*: if Claude edits a file that
   is open in the editor, the versions collide. If the active file is never written to,
   that cannot happen.

   When writing the next handoff, the collection area is read like the test answers — every
   point in it is answered or absorbed into the roadmap, so it is visible that nothing fell
   through.

   **And open the SECOND-TO-LAST handoff again too.** Yasin's wish (25.08.2026, 14:14):
   *"Before the new handoff,
   check whether anything was added to the old handoff, and mention only those changes in
   the new one."* The reason is practical: the user keeps collecting AFTER handing the
   handoff over — those lines only come into being while Claude is already working on the
   wave, and would otherwise be recorded nowhere. Procedure when writing a new handoff:

   1. Read the handoff just answered (as always).
   2. **Additionally the one before it** — only the "Collection for the next handoff"
      section. Anything there that doesn't appear in the current handoff is new.
   3. Those points go **right at the top** of the new handoff, under their own heading like
      "Taken over from your collection" — one line per point saying what happened to it
      (answered / built / landed in the roadmap). That way the user sees immediately that
      their interjections arrived, without copy-pasting anything.
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

### Claude does NOT close the old handoff any more (26.08.2026)

This rule went through two rounds, and both were paid for with real data loss.

Round one (Yasin, 25.08.2026, 14:21): *"Earlier I had already written something new into the old handoff
list that you closed automatically … and now it's gone, because you closed it."* Exactly
so: the unsaved-changes guard had run minutes earlier, the close came later, and in between
he had kept writing. **A check that does not stand immediately before the action is
worthless.**

Round two (Yasin, 26.08.2026, 14:07) went further: *"If I write something at the bottom and haven't saved
it yet, and you then close the old handoff after you've finished working — you can't close
it at all if I still have unsaved changes in there. So I'd almost say: don't close the old
handoff at all, leave it open, let the user close it."*

He is right, and the reason is more fundamental than the data loss: the collection area
exists precisely so he can keep writing DURING the running wave. The moment Claude finishes
and wants to tidy up is exactly the moment unsaved text is most likely to be sitting there.
A cleanup step that strikes right then can only lose.

So the rule now is:

1. **The old handoff stays open. Full stop.** Claude does not close it, does not save it,
   does not touch it. The user closes it themselves when they are done.
2. **Its content is still read before the new handoff is written** — collection area
   included, via the unsaved-changes guard so unsaved lines arrive too
   (`get text of (first document whose name is "…")`). Reading is harmless; only closing
   and writing are not.
3. **The new handoff is ALWAYS a new file** with a new name. That way there is never a
   collision between Claude's version and what is open in the editor.
4. **Archiving (`mv`) only happens once the user has closed the document** — or not in this
   wave at all. A handoff still open in the editor does not get moved; the new handoff
   notes in one line that archiving is still pending.
5. **Close + reopen remains exactly ONE exception:** when Claude itself changed the file the
   user has open (otherwise they read a stale version). Even then the check happens in the
   SAME call, and on `modified: true` it is NOT closed but asked about.

When in doubt: **better one window too many open than one line of the user's gone.**

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
  user messages; it is FEWER REQUESTS and a SMALL context while the many work-steps run.
  (This is also why subagents pay off: the heavy lifting happens in their separate small
  contexts.)
- Don't forget the third item: **Claude's own output at ×5**. In the measured session it
  was nearly a quarter of the total. Anyone who only talks about context size has
  explained two thirds of the bill.
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
- **A map, not just a to-do list.** The "open (next waves)" block at the end is good, but it
  only says what is still to come — not where the project knowledge lives. So every handoff
  gets a short **"Main documents"** block right before it: the 3–6 files that actually carry
  the state (roadmap, project status, overview of open topics, current concept papers), each
  with an absolute path and ONE line on what is in it and how fresh it is. Example:

  ```
  ## Main documents (where things are written down)

  - `/Users/…/project/ROADMAP-MASTER.md` — plan for all waves (as of 23.08.)
  - `/Users/…/project/PROJECT-STATUS.md` — what's done / in progress (as of 25.08.)
  - `/Users/…/project/OPEN-TOPICS.md` — topic store, coarser than the list below
  ```

  Rules: only list documents that REALLY exist (check first), mark outdated ones explicitly
  as outdated instead of quietly dragging them along, and never copy the content in — the
  path is the whole point ("reference, don't copy").
- **The lower part is a narrative thread, not a keyword list.** Yasin's wish
  (25.08.2026): *"down there I
  don't just want the questions and tests, but a thread you can see, roadmap-like — what
  the next wave is, what the one after that is, short, with a couple of details, so you
  remember and feel motivated to add something."*

  So the to-do list `Open (next waves)` becomes a short **roadmap with answer fields**. One
  paragraph for each of the next two or three waves — what's coming, why, and one or two
  details that bring the thought back. Then the same invitation as with the tests:

  ```
  ## The thread — what comes next

  ### Next wave: live transcript under the HUD
  The text should run along during recording, with an interim state every
  5 minutes. Hangs off your 5-hour video plan; the audio side has been
  secured since wave 10, only the text is missing.

  >>>Anything to add here?

  ### The wave after: read-aloud, part 2
  Right-click service, read-aloud state in the HUD, speed, loading more voices.

  >>>Anything to add here?
  ```

  The rest (the long enumeration of all open points) stays below it as a topic store —
  compressed, without answer fields. The roadmap is the invitation to think along, the list
  is the memory.
- **Archive old handoffs, never delete them.** Once a new handoff is written and its answers
  are incorporated, the PREVIOUS one moves into a `handoff-archive/` subfolder of the same
  project (create it if missing):

  ```bash
  mkdir -p "<project>/handoff-archive"
  mv "<project>/_handoff-project-2026-08-24-b.md" "<project>/handoff-archive/"
  ```

  Move, don't delete — the user tidies up themselves if they want to. That way the project
  folder always holds exactly ONE active handoff, and the question "which is the right one?"
  never comes up. The new handoff names the archive folder in one line so the way back stays
  visible. Only archive when the old document has no unprocessed answers left (otherwise it
  stays put, with the reason stated in the new handoff) — and only once the user has closed
  it in the editor (see the rule above).
- One deliberate difference: Pocock writes handoffs to the temp directory (transit document)
  and recommends `/compact` for same-directory continuation. This skill writes them **into
  the project** (dated, part of the working rhythm, the user annotates them) and prefers
  handoff + fresh session over `/compact` past the context threshold — on subscription
  plans, `/compact` keeps the huge expensive prefix alive; a fresh small session does not.

## Honesty rules

- There is no background timer: Claude only acts when a request arrives. That is exactly why
  the handoff is written *proactively at the end of a wave*, not "when the hour is nearly up".
- Cost claims should be shown as arithmetic when it matters (cache-write vs. re-read pricing),
  not asserted.
- Numbers are measured, never felt: context size, request count and cache hit rate all come
  from the session file or the status line — never from an impression.
- A cache rebuild is reported when it is DERIVABLE (see the section above) — never guessed.

## The logbook (self-observation, optional but recommended)

Keep a running log at `~/.claude/warm-handoff-log.md`. **Append one line at every handoff**
(and whenever a cache-relevant event happens), format:

```
| 22.08.2026 14:40 | ctx 85k | 147 req | write/read 2.5% | 2 waves | rebuilds: 1 (pause 90min, no handoff) | est. waste ~60k tokens |
```

Log-worthy events: session start/end context size, number of requests and the write/read
ratio, waves completed, every cache rebuild **with its cause** (pause > 1h, mid-session
model/effort switch, MCP restart, prefix change), warnings the user overrode, and a rough
token-waste estimate for each avoidable rebuild.

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
the thresholds, the measurement calls and the wave workflow already active.
