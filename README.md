# warm-handoff 🏄

> **Primary language: English · Deutsche Fassung: [README.de.md](README.de.md)**

**A Claude Code skill that paces your session around the prompt-cache window: it measures
where you stand, keeps the number of requests down, and writes a handoff document at the
right moment.**

Author: **Yasin Akgün** ([github.com/Aitomat](https://github.com/Aitomat)). The skill grew
out of building [Aitomat](https://aitomat.ai), a macOS app, with Claude Code every day —
every rule in it started as a session that went wrong or a bill that looked odd.

---

## Contents

1. [The problem in three minutes](#1-the-problem-in-three-minutes)
2. [The cost arithmetic, with real numbers](#2-the-cost-arithmetic-with-real-numbers)
3. [The wave workflow](#3-the-wave-workflow)
4. [Subagent economics](#4-subagent-economics)
5. [What the skill makes visible: cost line, cost table, quota](#5-what-the-skill-makes-visible)
6. [Install](#6-install)
7. [The scripts](#7-the-scripts)
8. [Honest limits](#8-honest-limits)
9. [The facts everything rests on](#9-the-facts-everything-rests-on)
10. [Credits, prior art, license](#10-credits-prior-art-license)

---

## 1. The problem in three minutes

If you use Claude Code, you see a chat interface. What you don't see:

- **Every message is not one request but many.** Claude reads a file, greps, edits, runs a
  command, reads the result — each of those steps is its own model request, and **every
  single one** sends the entire conversation so far along with it. A harmless "please
  implement this and test it" can trigger 30 to 150 requests.
- **The transcript grows and is re-sent every time.** After two hours of work the
  conversation is 200,000–500,000 tokens. Each of those 150 steps carries that backpack.
- **There is a cache that makes this bearable — but only inside its window.** Claude Code
  puts the conversation prefix into a prompt cache. Reading from the cache costs a tenth.
  On Pro/Max that cache lives for **one hour, sliding** — every request resets the clock.
  Take an hour-long break, switch the model, change the effort, or edit CLAUDE.md, and the
  cache is rebuilt: the whole prefix gets written once at **double** price.
- **None of this is shown anywhere.** No counter shows the context size, none the request
  count, none whether the last round was cheap or expensive. So people optimise the wrong
  thing — they type shorter messages — while the real cost sits in a work loop of file
  reads they never see.

The measurement that started this skill: one stretch of a real session — "I answered the
handoff, please implement" — cost **147 requests** at 223k context, **4,380k
token-equivalents**. The same amount of work, delegated to subagents and batched, takes
**14 requests** in the main context. That is the lever this skill is about: not writing
shorter, but **fewer requests inside the fat context**.

## 2. The cost arithmetic, with real numbers

All numbers in this skill are normalised to "fresh input = 1" (Anthropic list-price
ratios, Opus tier). On a subscription nobody pays this sum in dollars — it measures **what
loads the quota**, and on Pro/Max the quota is the currency that runs out.

| Item | Factor | What it means in practice |
|---|---:|---|
| Cache **read** | **×0.1** | The warm prefix is re-read at a tenth of the price on every request |
| Cache **write** (1-h TTL) | **×2** | New text enters the cache once at double price; a rebuild rewrites EVERYTHING |
| Model **output** | **×5** | Every word Claude types costs fivefold — chat explanations are the biggest item Claude alone is responsible for |
| Fresh input | ×1 | The reference unit |

### Why the request count dominates everything

One request at 220k context costs **220k × 0.1 = 22,000 equivalents** — just for reading,
before anything happens. At 30k (a fresh subagent) it's **3,000**.

```
Everything in the main context:  147 steps × 151k × 0.1              = 2,217k
Delegated:                        14 main requests × 345k × 0.1  =  483k
                                 147 agent steps   ×  30k × 0.1  =  441k
                                                          total  =  924k
```

**2.4× cheaper for exactly the same work** — only because each step runs against the
agent's small context instead of the session's fat one. Adding the other techniques
(capping completion reports, not narrating tool steps, explanations into the handoff
instead of the chat), the measured stretch drops from 4,380k to **1,350–2,050k — roughly
55–70 % saved**.

### Timing, not brevity: when a message costs almost nothing

The question everyone asks: "Does my interjection cost anything right now?" The answer
depends not on length but on **timing**:

| Situation | What happens to the message | Cost |
|---|---|---|
| Claude's own tool loop is running (reading, executing, launching an agent) | attached to the next request that was due anyway | **almost zero** (~140 equivalents for 50 words) |
| Subagents are computing, Claude itself is waiting | triggers a new request | **the full 10 %** of the context (22k at 220k) |
| Idle after Claude's reply | triggers a new request | **the full 10 %** |

The catch: the question is cheap, **the answer is not** — a 300-word reply is ~2,000
equivalents (×5). That's why the skill keeps answers to mid-wave questions short and
pushes details into the handoff, where they cost single instead of fivefold.

### What a rebuild costs — and how it's recognised

A session at 287k context that started at 82k: a mid-session model or effort switch
rewrites ~287k × 2, **~574k equivalents** — for nothing. That's why the skill warns before
`/model`, `/effort`, CLAUDE.md edits and MCP restarts, and reports a rebuild only when it
can name the cause (>1 h pause, a switch, a prefix change) — otherwise it stays silent
rather than guessing.

An important misconception it actively clears up: **"147 requests ≠ 147 rebuilds."**
Inside the window all 147 run against the warm cache. Measured cache-write rates in these
sessions were 1.6–3.3 % — warm throughout.

## 3. The wave workflow

The arithmetic rewards a specific rhythm. The skill calls it **waves**:

```
┌──────────────────────────────────────────────────────────────────────┐
│  1. The user sends ONE bundled message (or an answered handoff):     │
│     everything for the next stretch of work                          │
│                                                                      │
│  2. Claude works the wave — subagents for anything with more than    │
│     a handful of steps; interjections are welcome and cheap while    │
│     Claude itself is visibly churning                                │
│                                                                      │
│  3. At the end Claude writes a HANDOFF DOCUMENT instead of trailing  │
│     off in chat: delivered work, open items, roadmap, cost table,    │
│     quota status, questions — and the test list with answer lines    │
│                                                                      │
│  4. The user opens the handoff in a text editor, answers the tests,  │
│     collects new ideas in the collection area — at their own pace,   │
│     even across a long pause. Costs exactly zero requests.           │
│                                                                      │
│  5. The next session starts from ONLY the handoff: small context,    │
│     cache rebuilt once at minimum size, fully briefed                │
└──────────────────────────────────────────────────────────────────────┘
```

### Why an editor and not the chat box

The terminal collapses long input into `[pasted text]` — you lose the overview. In an
editor (TextEdit, VS Code, anything) you see the whole document, jump between test items,
add notes, let the file sit for two days. And it costs **zero requests** while you
collect. Rule: **⌘S before asking Claude to read the file** — unsaved editor changes are
invisible on disk.

### What a handoff looks like

```markdown
> **For the next session — copy and paste this line:**
> `I answered the handoff: /Users/…/project/_handoff-project-2026-08-27-b.md`

# Handoff Project — 27.08.2026, 18:21

## Quota
Claude Code: 5-h window 34 % · week 61 % (resets Mon 09:00) · Codex: 10 %/7d (reading 2 h old)

## Delivered in this wave
- …

## Expected agent results
- [ ] docs/reviews/2026-08-27-tageszeit-und-kontingente.md (research agent, started 17:02)

## Open items / roadmap
- Wave 19: …

## Questions for you
1. Should the trash-can route also apply to folders?
>>>Answer:

## Test list v70
## T1 — Tag filter without beachball
Set the filter to "invoice", 2,000 entries, must not hang.
>>>Answer:

## T2 — Hyperlink editor
…
>>>Answer:

# This session's cost table
| # | Time | What it was about | Req. | Context | read | written | output | equiv. |
…

## Collection for the next handoff
>>>
```

The details — the path at the very top ready to copy, the project name in the file name,
pre-seeded answer lines, what belongs in a handoff and what doesn't (rules adopted from
Matt Pocock's `/handoff`) — are in `SKILL.md`, section "The wave workflow".

### The user is the bottleneck

The newest rule in the skill (28.08.2026): a human cannot sit at the terminal all day.
Every clarifying question that halts a wave costs hours of wall-clock time. So waves are
cut to **run through without questions**: defensible assumptions are made and flagged in
the handoff, questions are **collected** into the handoff instead of asked one by one in
chat, and agents get **several tasks bundled** and report only when everything is done.
Agents expected to run longer than an hour write their result to a file
(`docs/reviews/<date>-<topic>.md`); the handoff lists the expected file, and the **next**
session checks for it while reading the handoff — so the agent finishing costs no request
of its own and no rebuild after the overnight pause.

## 4. Subagent economics

In this skill subagents are **the default route, not the exception** — anything with more
than a handful of steps goes to an agent. The reasons, in numbers:

| | Main context (220k) | Subagent (~30k) |
|---|---:|---:|
| Cost per work step (×0.1) | 22,000 | 3,000 |
| Cache TTL | 1 h sliding | 5 min (always, even on Max) |
| Startup cost | — | 1–3 requests + the task text |
| Report back into main context | — | becomes a ×2 cache write — **cap it!** |

Three things to know:

1. **Subagent tokens are not free.** They load the same weekly quota. What they do NOT
   load is the main context — which stays small, fast and responsive.
2. **The savings can be reinvested.** An agent works more thoroughly than you would on the
   side: 147 steps become 600. Then the bill is roughly even again — but **four times as
   much got done**. That is "token maximisation": more work for the same quota, not less
   output.
3. **The report is the hidden cost centre.** Every agent report is written into the main
   context (×2) and then re-read on every later request (×0.1). So every agent gets a
   report cap ("≤ 250 words, no diffs") and long results go into files.

Model choice (from the table in the skill): finding files, renames, log sifting, tests to
an existing pattern → **fast/cheap, effort low** (with Fable 5 as agent model: always
low). Design decisions, security review → strong model, high effort, or a different model
(Codex/GPT) as a second opinion. Model and effort are visible in the agent description
(`"Fable/low · rename test files"`) so the user sees in the terminal who is working.

Parallel vs. sequential: **parallel for speed, sequential for warmth** — agents cache
separately at 5 minutes; launch five at once and you have five cold caches.

## 5. What the skill makes visible

### The timestamp

Under every reply: date and time, read fresh from `date`, never extrapolated from an
earlier turn. The user sees for themselves how long ago the last request was and whether
the window is still open.

### The cost line

Under substantial replies (`ctx.sh`, appended to the `date` call that runs anyway, so the
measurement itself costs no request):

```
Last measured request: 366k read (×0.1) + 0.4k written (×2) + 2.9k output (×5) ≈ 52k ·
session so far: 265 requests, 9,520k
```

Plus a note when something was expensive: "That was 12 requests because I launched three
agents and read their reports — 4,600k."

### The per-session cost table

At the end of each wave, in the handoff (`session-costs.sh --markdown`). The row unit is
deliberately the **stretch between two user messages** — the unit a human experiences ("I
said something, then something happened"), not the individual model request nobody sees.

| # | Time | What it was about | Req. | Context | read | written | output | equiv. |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 17:00 | Handoff read, nine agents launched | 36 | 148k | 4130k | 282k | 110k | 1529k |
| 2 | 17:35 | *(batched)* | 0 | — | 0 | 0 | 0 | **0** |
| 3 | 17:35 | Your cost questions | 6 | 156k | 906k | 11k | 19k | 208k |
| 4 | 17:38 | `/context all` evaluated | 10 | 180k | 1706k | 43k | 8k | 298k |
| 5 | 17:48 | Timing and batching explained | 5 | 188k | 907k | 11k | 9k | 159k |
| 6 | 18:15 | *(batched — six questions)* | 0 | — | 0 | 0 | 0 | **0** |
| 7 | 18:21 | Remaining work, build, handoff | 20 | 220k | 4080k | 59k | 41k | 729k |
| **Σ** | | **7 stretches** | **82** | **220k** | **12671k** | **416k** | **200k** | **3102k** |

How to read it:

- **equiv.** = read × 0.1 + written × 2 + output × 5 — all three items on one price and
  summed. Row 1: 4130 × 0.1 + 282 × 2 + 110 × 5 = 413 + 564 + 550 ≈ 1529k.
- **Context does NOT add up.** "180k" in row 4 means: that's how fat the conversation was
  at the end of that stretch — not that the stretch cost 180k.
- **Two rows sit at zero.** Not a rounding error: those messages arrived while Claude was
  mid-loop and got batched into the running round.
- **Output 200k × 5 = 1,000k — a third of the total.** The one item Claude alone is
  responsible for. Lesson: talk less, write more into the document.
- **82 main-context requests for nine work packages** — the 500+ work steps ran inside the
  agents. In the main context they would have cost ~7,500k instead of 3,102k.

### The quota block

At the top of the handoff: what's left of the paid quota — Claude Code's own 5-hour and
weekly windows (parked from the status line into a file, because Claude cannot otherwise
see its own percentages) and Codex/GPT (`codex-limit.sh`, parsed from the `rate_limits`
block of the last Codex session, with the age of the reading). The point: if you pay
monthly, **use the quota up** — the skill suggests what the remainder could still buy
("week at 61 %, resets Monday: enough for the Codex second opinion on wave 19"). More in
`SKILL.md`, "Was noch im Tank ist".

Side findings from a 27.08.2026 review (in the Aitomat project's `docs/reviews`): the old
"peak hours" quota reduction for Claude Code Pro/Max was removed on 06.05.2026 — time of
day no longer affects price or quota, only 529 overload errors. And the skill listing in
the context is capped at ~2,000 tokens; a 405k session start does not come from 89
installed skills but from something else (`/context all` tells you what).

## 6. Install

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

Or clone the repo: `SKILL.md` goes to `~/.claude/skills/warm-handoff/SKILL.md`, everything
in `scripts/` goes to `~/.claude/`, keeping the file names.

**To have it fire in every session without typing anything**, one line in your global
`~/.claude/CLAUDE.md`:

```
At the start of every session, invoke the warm-handoff skill. Put the time in every reply.
```

Manually: `/warm-handoff`, or just say "cache", "handoff", "wave done", "fresh session".

Requirements: macOS or Linux, `bash`, `python3` (for the cost scripts), `jq` optional. The
scripts only read the local session files under `~/.claude/projects/` and
`~/.codex/sessions/` — nothing leaves the machine.

## 7. The scripts

| Script | What it does | Usage |
|---|---|---|
| `scripts/ctx.sh` | What was spent since the last user message and **on what**: request count, what happened inside them (agent reports, file access, commands, own replies), split into read/write/output. Produces the cost line. | `date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh` — always appended to a command that runs anyway, so the measurement costs nothing |
| `scripts/session-costs.sh` | The per-session cost table, wave by wave, from the session's `.jsonl`. Names the most expensive stretch and the cache hit rate. | `session-costs.sh` (current project, newest session) · `session-costs.sh <session.jsonl>` · `session-costs.sh --markdown` (ready for the handoff) |
| `scripts/codex-limit.sh` | How much of the Codex/GPT quota is used. The Codex CLI has no usage command; the script reads the `rate_limits` block from the last session file and prints the age of the reading. | `codex-limit.sh` · `--kurz` (status line: `codex 10%/7d`) · `--json` |

Also described in the skill: a small status-line script that parks Claude Code's own
percentages from the stdin JSON into a file so the skill can quote them in the handoff,
and a "wake-up ping" for the Codex readout (one mini call so the reading is fresh).

## 8. Honest limits

- The measurements come from real sessions of one developer on a subscription plan with
  the 1-hour cache, in one project (Swift/macOS). Other projects, other ratios — which is
  why the scripts ship, not just the results.
- The per-technique savings are estimates a second model (Codex/GPT) computed over the
  same session data. The items overlap and must not be summed.
- The "equivalents" are list-price ratios. On Pro/Max nobody pays that sum; it measures
  quota load, and Anthropic does not document the quota-to-token conversion.
- A rebuild is reported only when a cause can be derived. Without one, the skill prefers
  silence.
- The skill explicitly teaches: "first the number, then the rule." When an earlier
  explanation in the skill was wrong (it happened — "almost half saved" turned out to be
  about a third), it gets corrected and the correction stays readable.

## 9. The facts everything rests on

| Rule | Value |
|---|---|
| Pro/Max cache TTL | 1 hour, **sliding** — every request resets it |
| Over plan limits (paid credits) | drops to 5 minutes automatically |
| Subagents | always 5 minutes, even on Max |
| Cache read / write / model output | ×0.1 / ×2 (1-h TTL) / ×5 |
| Env overrides | `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1` |
| Skill listing in context | capped (`skillListingBudgetFraction`, ~2,000 tokens) |

Sources: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching),
[Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices),
[Extend Claude with skills](https://docs.claude.com/en/docs/claude-code/skills). As of 27.08.2026.

## 10. Credits, prior art, license

- [Matt Pocock's /handoff skill](https://www.aihero.dev/skills-handoff)
  ([mattpocock/skills](https://github.com/mattpocock/skills)) — the clearest thinking on
  *how* to write a handoff. Adopted: reference settled docs instead of copying them, redact
  secrets, suggest skills for the next agent. Deliberately different: our handoffs live *in
  the project* as dated, user-annotated working documents, and past the context threshold
  we prefer handoff + fresh session over `/compact`.
- Further handoff implementations: [392fyc](https://github.com/392fyc/claude-handoff),
  [REMvisual](https://github.com/REMvisual/claude-handoff),
  [willseltzer](https://github.com/willseltzer/claude-handoff),
  [ykdojo](https://github.com/ykdojo/claude-code-tips/blob/main/skills/handoff/SKILL.md).
- Second opinions on the arithmetic: Codex/GPT-5.6 and Ox Alpha (OpenRouter).

Issues, measurements from your own sessions, and pull requests are welcome — in English or
German. `SKILL.md` mixes English rules with German passages that record the sessions the
rules came from; the scripts are commented in German.

License: MIT.
