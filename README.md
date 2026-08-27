# warm-handoff 🏄

**A cache-aware session pacer for Claude Code — it counts your requests, measures your
context, watches your paid quota, and writes the handoff at the right moment.**

*By [Yasin Akgün](https://github.com/Aitomat) — built and refined during daily work on the
macOS app [Aitomat](https://aitomat.ai), where every rule below was paid for in real
sessions and then checked against measured numbers.*

In one measured working session, **147 requests went to the model — only 13 of them came
from the user.** The other 134 were the agent's own tool-steps and status notes. If you
don't know that, you optimise the wrong dial: you write shorter messages while the actual
bill is being run up by a work loop you never see.

That measurement changed this skill. It used to be about context size and handoff timing.
It is now about **fewer requests first**, shorter output second, smaller context third —
with every number read from the session file instead of guessed.

---

## The measurement that drives everything

Same session, full cost breakdown:

| Item | Tokens | Factor | Equivalent |
|---|---|---|---|
| Cache read | 22,171k | ×0.1 | 2,217k |
| Cache written | 562k | ×2 | 1,125k |
| **Own output** | 208k | **×5** | **1,038k** |

Two pieces of vocabulary first, because the table is unreadable without them — and because
this is exactly where Yasin got stuck the first time he saw it. **"k" means thousand**, so
22,171k is 22,171,000 tokens: yes, twenty-two million in one session. And **"equivalent"**
means tokens converted to one common price, so three items billed at three different rates
can be compared and added up.

**Twenty-two million read is not a typo, and here is the picture that makes it click: the
conversation is a book.** The model has no memory between two requests. Before every single
answer it reads the WHOLE book again from the start — every earlier message, every file it
read, every tool result. With 147 requests and a book averaging ~151k tokens ("pages"), that
is 147 × 151k = 22,171k pages read. The context in that session grew from 54k to 223k while
this was happening.

The arithmetic then closes exactly, which is what makes it worth trusting:

```
147 requests × ~151k average context = 22,171k read     × 0.1 = 2,217k
                                          562k written    × 2   = 1,125k
                                          208k own output × 5   = 1,038k
                                                            total = 4,380k
```

Three things most cache advice gets wrong, all visible in that table:

1. **Output is the forgotten item.** At ×5 it was nearly a quarter of the total. Anyone who
   only talks about context size has explained two thirds of the bill.
2. **The cache-write factor is 2×, not 1.25×** — 1.25 applies to the 5-minute TTL, while
   Pro/Max runs on the 1-hour one. Using the wrong factor prices a rebuild ~60 % too cheap.
3. **Requests, not messages, are the unit of cost.** Every tool-step re-reads the whole
   prefix at ~1/10. A fat context is therefore cheap to *talk* on and expensive to *work* on.

The skill ships the bash/Python one-liners that read all of this out of
`~/.claude/projects/<project>/<session>.jsonl`: current context, request count, how many
requests you actually triggered, growth per step, and the break-even point for starting
fresh. None of those numbers is visible while a session runs, which is the whole reason for
reading them off disk rather than estimating them.

## "So we get the 147 requests down to 14?" — almost, and here is the honest version

Yasin asked exactly that after seeing the table. The answer is *yes* for the main context and
*no* for the work, and the difference is the thing worth understanding.

**The work does not disappear. It moves.** A wave still needs its hundred file reads,
searches, edits and test runs. What changes is *where* they happen:

| Where the 100 steps run | Context each step re-reads | Cost |
|---|---|---|
| Your main session at 220k | 100 × 22k | **2,200k equivalents** |
| A subagent at ~30k | 100 × 3k | **300k** |

**Factor ~7** — and none of those steps appears as a request in the main session at all,
because only two things cross the boundary: the assignment and the final report.

So what is the realistic floor for a wave run purely as orchestration?

| Requests | What for |
|---|---|
| 1 | reading the handoff |
| 1–2 | launching the whole fleet in ONE bundled reply |
| 1 per agent | its closing report — unavoidable, that is how a result arrives |
| 2–3 | build, test, commit, each through one script |
| 1 | writing the handoff |
| 1 | the closing message |

Roughly **13–20 requests instead of 147**, for the same delivered work. Your conversation
with Claude sits on top of that and is *wanted* — the thing being cut is the machine's own
chatter, never your thinking.

## Fewer requests: the technique list

A second model (GPT-5.6 via Codex) was given the same numbers and estimated what each
technique would have saved in that exact session. Target picture: **35–55 requests instead
of 147**, total cost from 4,380k down to 1,350–2,050k equivalents.

| Technique | Effect |
|---|---|
| Batch independent reads/searches into ONE reply | −25 to −45 requests |
| One script that does ten things and prints one summary | −20 to −35 requests |
| Cut agents by work package, not by sub-step | −30 to −60 requests |
| Reports as files; only result, risks and path come back | −0.3 to −0.7M |
| Cap agent report length (max 300 words, no chronicle) | −0.2 to −0.4M output |
| Pre-filter command output (`grep`/`jq`/`tail`) | −0.1 to −0.3M |
| Own output budget (interim ≤100 words, closing ≤500) | 208k → 50–80k output |
| Hand off earlier (at 100–120k instead of 223k) | −0.3 to −0.7M read |

These are estimates for one session, they overlap, and they must not be added up — but the
direction is not in doubt, and the skill states the arithmetic every time it makes a claim.

## Why a subagent is the biggest lever

Yasin's description of the mechanism is clearer than any documentation:

> *"When you send a subagent out, it doesn't start like a new session at 80,000 tokens times
> two, but at, say, 10,000 times two. Internally it burns a lot, some of it cheap, some
> expensive — but it gives back LITTLE, because it only returns the result. And that keeps
> the current session small and cheap."*

Three numbers make that concrete:

1. **Startup.** A fresh main session measured **82k** before any work happened, and
   rebuilding that costs 82k × 2. A subagent starts with its assignment plus its own tool
   schemas — on the order of **10–20k**, so ~20–40k once. Same mechanism, a quarter of the
   entry fee.
2. **What it burns inside.** It reads, searches, edits, runs tests: dozens of steps, some
   cheap and some genuinely expensive — but every one of them re-reads *its* ~15k context
   rather than your 220k. That is the 100 × 3k versus 100 × 22k from the table above.
3. **What comes back.** Two things cross into your context: the assignment you wrote, and a
   report capped at 300 words. The chronicle, the logs, the dead ends, the six files it read
   and discarded — all of that stays in the agent's context and dies with it.

Expensive work, cheap receipt. In the measured session six agents together burned more than
a million tokens and nothing of it reached the main context except assignments and reports.

**What that is worth — two statements, deliberately kept apart.** They are usually mashed
into one comparison (147 steps on one side, 600 on the other), which puts a different amount
of work on each side and makes delegation look like it saves nothing. It does save.

*One: the same work, merely delegated.*

```
All in the main context:  147 steps × 151k × 0.1              = 2,217k
Delegated:                 14 main requests × 345k × 0.1 =  483k
                          147 agent steps  ×  30k × 0.1 =  441k
                                                   total =  924k
```

**2.4× less for exactly the same work** — because every step is priced against the agent's
small context instead of your fat one, roughly a fifth per work-step.

*Two, separately:* pocket that saving and you're done. Reinvest it and you get a multiple of
the work for the same quota — an agent works more thoroughly than you would in passing, so
147 steps quickly become 600. At 600 agent steps (1,800k) plus the 483k of main requests the
bill is level with where you started — but **four times as much has been done**. That is the
point of "token maximisation": more work for the same quota, not less spending.

So: **cheaper for the same work, and far more work for the same price** — whichever of the
two you want. What subagent tokens are not is *free*: they draw on the same weekly quota.
What they don't load is your main context, which is the whole trick.

The skill is equally clear about when a subagent does *not* pay: below ~3–5 tool steps, for
strictly sequential work, or when a lot of shared context would have to be shipped across
first — its own startup is roughly 1–3 requests plus briefing plus report.

One small rule with an outsized effect on trust: **the model and effort go into the agent's
displayed name.** `Opus5/high · history performance` instead of `history performance, round
2`, so you can see in your own terminal whether something expensive is running — and stop it
before the tokens are gone.

## What one message actually costs — and when it costs nothing

This is the most useful piece of mechanics in the whole skill, and almost nobody knows it.
Yasin had to ask three times before it got explained properly:

> *"While the AI has just been given a new request and hasn't answered yet, you can slip
> further requests in. But if it answers in between and then picks up the new request, it
> costs ten per cent of the current context again."*

Exactly right — which means **timing beats brevity**. A short message sent at the wrong
moment costs far more than a long one sent at the right moment.

| Situation | Your message | Cost |
|---|---|---|
| Claude's own tool loop is running (reading, running commands, launching agents) | is appended to the turn already in flight | **near zero** |
| **Subagents are computing, Claude is waiting for them** | triggers a new request | **the full 10 %** |
| Claude has answered and is idle | triggers a new request | **the full 10 %** |

The middle row is the counter-intuitive one: while subagents work, the *main* agent is doing
nothing — it is sitting there waiting for their reports. A message then costs exactly as much
as one sent into a dead-quiet session.

Put numbers on it at 220k context: "near zero" means ~140 token equivalents (50 words,
written into the cache once at ×2). "The full 10 %" means ~22,000. **A factor of 150 for the
same sentence, decided purely by when you press Enter.**

Two footnotes, both in your favour:

- **Messages in quick succession are bundled into ONE request** if they land before the
  answer starts. Two thoughts back to back cost once, not twice.
- **The question is cheap; the answer is not.** Output is billed at ×5, so a 300-word reply
  is ~2,000 equivalents — fourteen times the question that caused it. The skill therefore
  tells Claude to answer interjections *short* and push the detail into the handoff. Throttle
  the rambling, not the question.

Practical upshot: interrupt freely while you can see it working. When only the subagents are
running, collect instead — ideally in the handoff's collection area, where writing costs
literally nothing, because no request comes into being at all.

## The per-session cost table

*"Couldn't you just make a table where we have everything per session at a glance — so you
can see what cost how many tokens and when? That would be brilliant."* So the skill ships
`session-costs.sh`. Its unit is deliberately the **stretch between two of your messages** —
what a human actually experiences ("I said something, then something happened"), not the
individual model request, which nobody ever sees.

```
| # | Time  | What it was about          | Req. | Context | read   | written | output | equiv. |
| 1 | 14:05 | Handoff answered …         |  147 | 223k    | 22171k | 562k    | 208k   | 4380k  |
| 6 | 17:22 | So the thing I mentioned … |   25 | 319k    |  7346k | 108k    |  69k   | 1297k  |
| Σ |       | 10 stretches               |  246 | 345k    | 49906k | 811k    | 396k   | 8594k  |

Most expensive stretch:  #1 at 14:05 (4380k equivalents, 147 requests)
Requests per message:    24.6 on average
Share of own output:     23 % of total cost
Cache hit rate:          1.6 % written (under 10 % = warm)
```

Reading it, column by column — and this explanation ships *with* the table, because its
author didn't understand his own table at first sight:

| Column | Meaning |
|---|---|
| **#** | the stretch, counted from one message of yours to the next |
| **Time** | when it began, in your local time |
| **What it was about** | the first words of your message, so you recognise the row |
| **Req.** | how many model requests that one sentence set off |
| **Context** | how thick the book was at the END of that stretch — **not a cost column** |
| **read** | requests × book thickness; the biggest item, priced ×0.1 |
| **written** | what was newly written into the cache, priced ×2 |
| **output** | what Claude itself wrote, priced ×5 |
| **equiv.** | the three items converted to one price and added |

**The context column does not add up.** "319k" in the second row does not mean that stretch
cost 319k; it means the book was 319,000 tokens thick when the stretch ended. It sits there
to *explain* the read column — the thicker the book, the more expensive every further
request. Which is why it grows steadily while the cost columns jump around.

**A row showing 0 requests is not a bug either.** It means that message arrived while work
was already running, got appended to the turn in flight, and triggered no request of its own
— the near-free case from the table above. A zero there is the cheapest row you can get.

The four lines under the table are the real yield: which wave was expensive, how many steps
one sentence sets off, what your own chatter costs, and whether the cache was warm at all.
The skill puts the table into every handoff, right before the closing context line — it
doesn't replace that single number, it explains it.

## The cost line under every answer

*"Could you say with every message what cost how much? Just that token figure, additionally,
under your answers."* So Claude appends one plain line — read, written, output, each with its
factor, plus the session total. It costs nothing extra because the measurement is piggybacked
onto the `date` call the timestamp needs anyway; measured on its own it would be a thermometer
that heats the room.

```
Last measured request: 366k read (×0.1) + 0.4k written (×2) + 2.9k output (×5) ≈ 52k ·
session so far: 265 requests, 9,520k
```

**Note the label — it says "last measured request", not "this round", and that matters.** All
three numbers come from the last *completed* request, not from the answer they sit under; the
cost of the running answer isn't settled until it is finished. With read and written you never
notice (the context moves by a few per cent per step). With output you do: a short answer can
sit under the output figure of a long one. Claude may estimate the running answer's output
from its word count (words × ~1.4), but then it has to mark it as an estimate standing next to
two measurements.

**The line has a second job: it speaks up when a round was unusually expensive.** Not at a
fixed threshold, but when a round costs more than about twice this session's own running
average — measured from the session file. The tone is deliberately friendly rather than
scolding, and it always names the cause plus a cheaper route: *"that round was expensive
(≈120k) because I read three large files in full — next time a targeted search does it"*, or
*"those five short messages cost ≈180k together at a 350k context; collected into one they'd
have been ≈37k"*. The responsibility is almost always Claude's, not yours — whole-file reads,
unfiltered command output, over-long answers, per-agent chatter — and the skill says so, so
the feature doesn't turn into user re-education. At most once per wave. And it works the other
way too: a wave that went well gets named as well ("the whole wave ran through subagents — 40k
in the main context for six work packages").

## What it does

- 🧮 **Counts and measures instead of guessing.** Context size, request count, steps per
  message and break-even all come from the session file. A sentence like "cache is fresh
  (~20k)" written without looking is treated as a fabrication — in the incident that
  produced this rule, the real number was ~80k.
- 🤖 **Subagents as the default route, not the exception** (see the section above for the
  arithmetic). The skill carries a **subagent contract** — status, decisions, evidence with
  paths, risks, next step; max 300 words, detail into files — because an uncapped report is
  how a subagent's savings leak straight back into your context at ×5.
- 🔇 **No more per-agent status chatter.** An earlier version told Claude to announce every
  agent start and landing "because those lines keep the cache warm". Revoked: your terminal
  already shows running agents, and Claude's own tool-steps reset the timer anyway. Five
  such notes at 220k context cost ~110k equivalents — for text you were already looking at.
  Now: one summary when the fleet lands, plus reports only for a decision, a blocker, or a
  milestone.
- 📉 **Measurable cache hit rate, not assertions.** Every session line carries
  `cache_creation_input_tokens` next to `cache_read_input_tokens` — their ratio *is* the hit
  rate. In the measured session: 22,171k read against 562k written = **2.5 %**, with only 6
  of 147 requests doing a noteworthy write. That finally settles the question Yasin asked
  twice: *"147 requests — did you rebuild the cache 147 times?"* No. And now that answer
  is evidence, not a claim.
- 🔋 **Shows the paid quota you already bought — and suggests what to spend it on.** Claude
  sees neither its own quota percentages nor Codex's. The skill ships a script that reads
  Codex's `rate_limits` block out of its session files, plus a status-line snippet that
  parks your own 5-hour/weekly percentages where Claude can read them. Both land in a
  **"What's left in the tank"** block at the top of every handoff, with a concrete proposal
  ("Codex has 90 % free — the startup-time analysis and the endurance test are exactly that
  kind of work"). It is paid quota, not a budget to conserve — see *Use the quota you already
  paid for* below.
- ⏱ **Timestamps every reply — date AND time, read fresh, never estimated.** An LLM has
  no sense of elapsed time: if Claude extrapolates from an earlier clock read ("it was
  16:28 two agents ago, so ~16:47"), stamps drift by 15+ minutes and mislead you about
  the cache window. Hard rule: a timestamp may only come from a `date` call in that same
  reply (costs nothing — piggybacked on any command); no read → no stamp. And no `~`
  stamps: a tilde does not make a guess honest.
- ⚠️ **Warns before cache-killing actions**: mid-session model/effort switches, flaky MCP
  servers, prefix changes.
- 📏 **Recommends a fresh session at a sweetspot that moves with the work ahead**: ~200k
  before a big build wave, ~250k mixed, ~300k if only conversation is coming, 400k as the
  hard ceiling. The threshold moves because cost is *steps × context*, and only the work
  ahead decides how many steps there will be — 300 build steps at 300k is ~9M equivalents,
  the same wave from a fresh 30k session ~0.9M, while ten quiet exchanges at 300k are ~0.3M
  and matter to nobody. It also announces *how much still fits* ("context 148k, target
  200k — good for about one more wave or a dozen questions").
- 📝 **Writes a handoff automatically after every work wave**: delivered work, running state,
  a **map of the main project documents**, a short **roadmap with answer fields** for the
  next two or three waves — and **your test checklist at the bottom**, ready to annotate.
  The file path sits at the very top as a copy-paste line for the next session.
- 👀 **Opens every user-facing document in your text editor automatically** (`open -a
  TextEdit` on macOS) — handoffs, plans, reports, checklists. You *see* when something is
  ready instead of hunting for file paths. Each document carries a one-line header
  inviting comments, marked with `>>>` at line start — Claude reads those back as your
  answers, and checks for unsaved editor changes before reading (offering to adopt or
  save them). Lost a closed document? TextEdit ▸ File ▸ Open Recent brings it back.
- 🛟 **Your unsaved lines are never at risk.** Claude does not close, save or edit the old
  handoff at all — you close it when you're done. A new handoff is always a new file, so
  Claude's version can never collide with what is open in your editor. That rule exists
  because the earlier "tidy up afterwards" behaviour destroyed real notes twice. Motto:
  better one window too many open than one line of yours gone.
- 🔁 **Teaches the wave workflow**: batch work into big waves, chat cheaply in between,
  answer the test list in a plain text editor (you see the whole document — chat inputs
  collapse long dictation into `[pasted text]`, so you can't even re-read what you said),
  then hand the file to the next session. **Press ⌘S before handing it over** — Claude
  reads from disk; on macOS it will also check TextEdit for unsaved changes and offer to
  take them over. The handoff carries a **collection area** you keep writing into while the
  next wave runs; Claude reads it, never writes into it.

## Install

The skill itself goes to `~/.claude/skills/warm-handoff/`. The three helper scripts it calls
(`ctx.sh`, `codex-limit.sh`, `session-costs.sh`) are referenced by path as `~/.claude/*.sh`
throughout the skill, so they belong one level up, directly in `~/.claude/` — not inside the
skill folder.

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

(or clone this repo — `SKILL.md` goes to `~/.claude/skills/warm-handoff/SKILL.md`, everything
in `scripts/` goes to `~/.claude/`, keeping the filenames as they are)

### Make it always-on

Skills fire when their description matches the situation. To have it active in **every**
session without typing anything, add one line to your global `~/.claude/CLAUDE.md`:

```
At the start of every session, invoke the warm-handoff skill.
```

## What a cache rebuild costs (and where you see it)

You **cannot** see a rebuild in the context counter — the context is the same size before and
after; only the price changed. Where you *do* see it: your **5-hour and weekly usage quota**,
which drops noticeably faster whenever a big prefix gets re-written. That's the whole game:
a lost cache doesn't make your session bigger, it makes it more expensive.

Corollary, with honest arithmetic: **a short message costs ~1/10 of your WHOLE context.**
At 30k context that is pocket change — chat freely. At 200k+ it is ~20k full-price token
equivalents per exchange, and ten quick back-and-forths equal one full context read. So:
the bigger the context, the more you should batch — ideally one long, structured message
per wave (handoff to handoff, answers collected under the test items), short questions
only when they truly can't wait. Every message still resets the 1-hour timer.

(That ~1/10 applies to a message sent into an *idle* session. Sent while Claude's tool loop
is turning, the same message is near-free — see *What one message actually costs* above. The
batching advice is for the pauses, not for the middle of a wave.)

## And count the startup cost of a fresh session

This README used to promise "~20k" for a fresh session. Yasin caught the gap: *"you're not
accounting for the fact that a new session starts at 70,000 tokens for me, and that gets
multiplied by two because the cache is rebuilt."* He was right, and it takes four steps to
see why — none of them obvious the first time.

**Step 1 — what "start context" even is.** Before you type a single character, a session is
already full. The system prompt, every tool schema, your installed skills, the project's
CLAUDE.md and its rules: all of that is loaded *before* you do anything. That is your floor.
Measured right after session start in one real project, before a single line of work: **82k**
— not 20k. Your own floor depends on how many skills and MCP servers you have installed,
which is exactly why the skill measures it per project instead of quoting a figure.

**Step 2 — why the rebuild is × 2 and not × 1.25.** Writing something into the cache costs
more than reading it back out, and how much more depends on how long it is stored: the
5-minute TTL costs 1.25×, the **1-hour TTL costs 2×** — and the 1-hour one is the Pro/Max
default. Use 1.25 and you price your fresh session about 60 % too cheap. This is the single
most common arithmetic error in cache discussions, and Yasin found it in this very skill
(*"I thought that had to be times two"* — it did). Reading back stays 0.1× either way.

**Step 3 — what a "step" is.** Not your messages. Overwhelmingly Claude's own tool calls:
each file read, each search, each command, each test run. In the measured session, 147
requests stood against 13 messages from the user. So when the formula below says "break-even
at 8 steps", it means eight *tool calls* — which a build wave burns through in under a
minute, and a conversation may not reach in an hour.

**Step 4 — the arithmetic.**

```
Rebuild, ONE-TIME       = start context × 2      (1-h TTL; × 1.25 only on 5-min TTL)
Step in the new session = start context × 0.1
Step in the old session = current context × 0.1
Break-even (in steps)   = (start context × 2) / ((old − new) × 0.1)
```

Worked example from that session: start 82k, current 287k → the rebuild costs ~164k once,
and every step after it saves 20.5k → **break-even at ~8 steps.**

**And what the number actually means.** Starting fresh is an investment with a payback period
measured in tool calls, not in minutes or messages. Going through the test list, answering
questions, a couple of small fixes — that is under ~6 steps, so stay put even at 260k+; the
rebuild would cost more than it saves. A build wave, a review, a migration — hundreds of
steps, so switch: you pass break-even before the first file is written, and everything after
that is pure profit. Which is why the skill always asks *"what comes next?"* before
recommending anything. Without that question, the recommendation is a coin flip.

## When does the hour start?

The timer resets on **every request** — your messages AND Claude's own tool-steps. So the
hour counts from Claude's last output: if the final handoff message lands at 16:30,
answering before ~17:30 stays warm. Reading costs nothing; only replying is a new request.
While subagents run, Claude's own tool-steps keep the cache warm for free — which is
exactly why it no longer needs to write you status notes to do it.

**But "free" applies to your reading, never to Claude's writing.** Every answer Claude
produces is itself a request: it re-reads the whole context at 10 % (~22k equivalents at
220k) *and* pays for its own output tokens at ×5 on top — a 300-word reply adds roughly 2,000
more. There is no way to keep the clock warm for nothing; every timer reset is a paid
request. That is precisely why the per-agent status notes were cut: they reset a timer that
the tool-steps were resetting anyway, and charged you a full request for the privilege.

## Pacing: parallel for speed, sequential for warmth

Subagent scheduling is a cache instrument: run them **in parallel** when you're present
and want speed; run them **sequentially** when you step away — each completion report is
a new request that resets the 1-hour timer, so you come back hours later to a warm cache
and a finished handoff. Tell Claude which mode you need ("I'm in a hurry" vs. "I'm going
to bed — here's the queue"). Honest limit: warmth needs real queued work; Claude must never
invent busywork just to touch the cache.

Picking the *tier* is part of the plan too: mechanical work (finding files, listing call
sites, doc sweeps) goes to a fast, cheap model at low effort; design decisions and
correctness reviews go to a strong model at high effort. And reviewing your own output is a
separate job — a second opinion from a different model catches what a same-architecture
re-read cannot.

## The window as a friendly coach

The 1-hour window is meant as a POSITIVE motivator, not cost-anxiety: "answer within the
hour and the wave keeps riding" works like a streak — it nudges you to test now, dictate
answers now, launch the next wave now, while everything is fresh. The pre-seeded test
questions remove the blank page: cursor after the marker, speak, done.

The same goes for the numbers: "room for about 2 more waves" is a streak counter, not an
invoice. The skill is instructed to be casual and never admonishing — and to teach, not
just to keep time. Every cost statement leads with the number and the reason ("that's 22k
equivalents, because the context is 220k and reading costs a tenth"), clears up the common
misunderstandings, and names its own earlier mistakes out loud rather than silently
overwriting them.

## Use the quota you already paid for

Unused quota does not roll over. At the end of the week it is simply gone — so the loss is
the window closing on it, never the spending. That reframing is deliberate: warm-handoff is
not a thrift device, it is a pacing device.

So when your 5-hour or weekly window still has real room, the skill is instructed to say so
*and* propose something big, in Yasin's words: *"Go on, check everything through, see whether
it's any good."* The candidates it suggests are the expensive, never-urgent jobs nobody ever
schedules:

- a full pass over the whole project at high reasoning effort ("ultrathink") — architecture,
  dead code, contradictions;
- a quality check of a whole area against its acceptance criteria, not just the last diff;
- a large second-opinion analysis on a *different* model — a different architecture sees
  different mistakes than a re-read by the same one;
- a long test run nobody wants to sit through: startup times, endurance runs, a full matrix.

Always phrased with the number attached ("90 % of the week is still free — this is the moment
for the big review"), never as a scolding. The same block works from the other side too: past
~85 % used it prints the reset time, and the message becomes "small stuff until tomorrow
morning".

## The facts it is built on

| Rule | Value |
|---|---|
| Pro/Max cache TTL | 1 hour, **sliding** — every exchange resets it |
| Over plan limits (paid credits) | drops to 5 minutes automatically |
| Subagents | always 5 minutes, even on Max |
| Cache read / cache write / own output | ×0.1 / ×2 (1-h TTL) / ×5 |
| Env overrides | `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1` |

Source: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching).

## Honest limits

Credibility matters more here than a bigger headline number, so:

- **The measurements come from real working sessions on a subscription plan with the
  1-hour cache** — one project (Aitomat), one developer's rhythm. Your ratios will differ — which is the
  point of shipping the measuring scripts rather than just the results.
- **The technique effects are estimates**, produced by a second model reasoning over the
  same session data. They overlap and must not be summed.
- **Dollar figures are API list-price equivalents.** On a Pro/Max subscription nobody pays
  that sum; it measures what your quota is being charged. The price constants in the
  scripts are for one model tier — adjust them for yours.
- **The cause of a cache miss is not readable from the data.** The skill reports a rebuild
  only when it can derive it (a >1h gap between two `date` reads, a model switch, a
  CLAUDE.md edit, an MCP restart) and otherwise says nothing rather than guessing.
- **There is no background telemetry and no background timer.** Claude acts only when a
  request arrives — which is precisely why the handoff is written proactively at the end of
  a wave instead of "when the hour is nearly up".
- The quota reading for Codex is **only as fresh as your last Codex run**, and the skill
  always prints the age of that measurement alongside it.

## Why not just any handoff skill?

There are at least eight published handoff skills. None of them decide the *timing*: they
write a document when you ask. warm-handoff treats the handoff as the exit move of a cache
economy — it tells you when continuing is cheap, when a restart is cheaper, and produces the
document at exactly that moment, test list included. And since the 26.08.2026 measurement it
goes one step further: the handoff is explicitly the *weakest* of its three levers. Fewer
requests and shorter output save more.

## Changelog highlights

The skill is under continuous, evidence-driven revision — including revoking its own rules
when the data says so.

- **26.08.2026** — "Fewer requests" becomes the primary goal, with the measured cost table
  and the cross-checked technique list. Subagents promoted to the default route with a
  written contract. Per-agent status notes **revoked**. Cache hit rate made measurable.
  Codex + Claude Code quota surfaced at the top of every handoff. Claude no longer closes
  the old handoff at all. Teaching mandate added: number first, then the rule. Later the
  same day: the timing rule for messages (near-free mid-loop, full 10 % while subagents run
  or Claude is idle), the honest floor of 13–20 requests for an orchestration wave, subagent
  startup costs spelled out, model + effort required in every agent's displayed name, and
  quota reframed from "don't waste it" to "spend it before it expires". Plus the per-session
  cost table (`session-costs.sh`), with the "the conversation is a book" explanation that
  makes 22 million tokens read in one session stop looking like a typo.
- **25.08.2026** — Context size, step count and break-even read from the session file
  instead of estimated; the "~20k fresh session" claim replaced by a measured 82k floor;
  cache-write factor corrected from 1.25× to 2×; sweetspot turned into a calculation that
  says how much still fits; collection area, roadmap thread and document map added to the
  handoff; handoff archiving instead of deletion.
- **24.08.2026** — Timestamp discipline hardened (no `~` stamps, date always included);
  project name required in every handoff file name.
- **22.08.2026** — First public release: cache facts, wave workflow, handoff ritual,
  editor integration, logbook.

## Author

Built and maintained by **Yasin Akgün** — [github.com/Aitomat](https://github.com/Aitomat).
The skill grew out of building [Aitomat](https://aitomat.ai), a macOS app, with Claude Code
every day: every rule in here started as a session that went wrong or a bill that looked
odd, and stayed only after the numbers backed it up. That is also why rules get **revoked**
here when a later measurement contradicts them.

Issues, measurements from your own sessions, and pull requests are welcome.

## Credits & prior art

- [Matt Pocock's /handoff skill](https://www.aihero.dev/skills-handoff)
  ([mattpocock/skills](https://github.com/mattpocock/skills)) — the clearest thinking on
  *how* to write a handoff document. We adopt his rules (reference settled docs instead of
  copying them, redact secrets, suggest skills for the next agent) and deliberately differ
  on two points: our handoffs live *in the project* as dated, user-annotated working
  documents, and past the context threshold we prefer handoff + fresh session over
  `/compact` — on subscription plans a fresh small session beats keeping a huge cached
  prefix alive.
- Further handoff implementations: [392fyc](https://github.com/392fyc/claude-handoff),
  [REMvisual](https://github.com/REMvisual/claude-handoff),
  [willseltzer](https://github.com/willseltzer/claude-handoff),
  [ykdojo](https://github.com/ykdojo/claude-code-tips/blob/main/skills/handoff/SKILL.md).

## License

MIT
