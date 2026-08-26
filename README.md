# warm-handoff 🏄

**A cache-aware session pacer for Claude Code — it counts your requests, measures your
context, watches your paid quota, and writes the handoff at the right moment.**

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
fresh.

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

## What it does

- 🧮 **Counts and measures instead of guessing.** Context size, request count, steps per
  message and break-even all come from the session file. A sentence like "cache is fresh
  (~20k)" written without looking is treated as a fabrication — in the incident that
  produced this rule, the real number was ~80k.
- 🤖 **Subagents as the default route, not the exception.** A subagent starts at ~10–20k
  instead of your full context, so its 100 work-steps read 100 × ~15k instead of
  100 × ~220k. Nothing lands in the main context except the assignment and the report.
  The skill carries a **subagent contract** (status, decisions, evidence with paths, risks,
  next step — max 300 words, detail into files) and is honest about when a subagent does
  *not* pay: below ~3–5 tool steps, or for strictly sequential work.
- 🔇 **No more per-agent status chatter.** An earlier version told Claude to announce every
  agent start and landing "because those lines keep the cache warm". Revoked: your terminal
  already shows running agents, and Claude's own tool-steps reset the timer anyway. Five
  such notes at 220k context cost ~110k equivalents — for text you were already looking at.
  Now: one summary when the fleet lands, plus reports only for a decision, a blocker, or a
  milestone.
- 📉 **Measurable cache hit rate, not assertions.** Every session line carries
  `cache_creation_input_tokens` next to `cache_read_input_tokens` — their ratio *is* the hit
  rate. In the measured session: 22,171k read against 562k written = **2.5 %**, with only 6
  of 147 requests doing a noteworthy write. That finally settles the most common question
  users ask: *"147 requests — did you rebuild the cache 147 times?"* No. And now that is
  evidence, not a claim.
- 🔋 **Shows the paid quota you already bought — and suggests what to spend it on.** Claude
  sees neither its own quota percentages nor Codex's. The skill ships a script that reads
  Codex's `rate_limits` block out of its session files, plus a status-line snippet that
  parks your own 5-hour/weekly percentages where Claude can read them. Both land in a
  **"What's left in the tank"** block at the top of every handoff, with a concrete proposal
  ("Codex has 90 % free — the startup-time analysis and the endurance test are exactly that
  kind of work"). It is paid quota, not a budget to conserve.
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
  hard ceiling. It also announces *how much still fits* ("context 148k, target 200k — good
  for about one more wave or a dozen questions").
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

```bash
mkdir -p ~/.claude/skills/warm-handoff
curl -fsSL https://raw.githubusercontent.com/Aitomat/warm-handoff/main/SKILL.md \
  -o ~/.claude/skills/warm-handoff/SKILL.md
```

(or clone this repo and symlink/copy the folder into `~/.claude/skills/`)

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

**And count the startup cost of a fresh session.** This README used to promise "~20k". A
measurement taken right after session start, before a single line of work, came back at
**82k** — skills, tool schemas and project rules are loaded before you do anything. So the
skill measures your floor per project instead of quoting a number:

```
Rebuild, ONE-TIME       = start context × 2      (1-h TTL; × 1.25 only on 5-min TTL)
Step in the new session = start context × 0.1
Step in the old session = current context × 0.1
Break-even (in steps)   = (start context × 2) / ((old − new) × 0.1)
```

Worked example from that session: start 82k, current 287k → rebuild ~164k, saving 20.5k per
step → **break-even at ~8 steps.** Which gives the rule that actually holds: going through
the test list (< ~6 steps) → stay, even at 260k+. A build wave, review or migration
(hundreds of steps) → switch.

## When does the hour start?

The timer resets on **every request** — your messages AND Claude's own tool-steps. So the
hour counts from Claude's last output: if the final handoff message lands at 16:30,
answering before ~17:30 stays warm. Reading costs nothing; only replying is a new request.
While subagents run, Claude's own tool-steps keep the cache warm for free — which is
exactly why it no longer needs to write you status notes to do it.

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
  1-hour cache**, one project, one user's rhythm. Your ratios will differ — which is the
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
  the old handoff at all. Teaching mandate added: number first, then the rule.
- **25.08.2026** — Context size, step count and break-even read from the session file
  instead of estimated; the "~20k fresh session" claim replaced by a measured 82k floor;
  cache-write factor corrected from 1.25× to 2×; sweetspot turned into a calculation that
  says how much still fits; collection area, roadmap thread and document map added to the
  handoff; handoff archiving instead of deletion.
- **24.08.2026** — Timestamp discipline hardened (no `~` stamps, date always included);
  project name required in every handoff file name.
- **22.08.2026** — First public release: cache facts, wave workflow, handoff ritual,
  editor integration, logbook.

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
