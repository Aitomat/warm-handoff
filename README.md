# warm-handoff 🏄

> **Why is the skill file so short?** `SKILL.md` (~190 lines) is loaded into every session, so it is deliberately compact. The full history with dated user quotes and the reasoning behind every rule lives in `references/historie.md` (~1,900 lines, German-only) — long on purpose; read it when a rule looks odd. A complete German translation of the skill itself is `SKILL.de.md`.


> **Primary language: English · Deutsche Fassung: [README.de.md](README.de.md)**

**A Claude Code skill that paces your session around the prompt-cache window: it measures
where you stand, keeps the number of requests down, and writes a handoff document at the
right moment.**

Author: **Yasin Akgün** ([github.com/Aitomat](https://github.com/Aitomat)). The skill grew
out of building [Aitomat](https://aitomat.ai), a macOS app, with Claude Code every day —
every rule in it started as a session that went wrong or a bill that looked odd.

---

## Contents

0. [The moral, in five sentences](#0-the-moral-in-five-sentences)
1. [The problem in three minutes](#1-the-problem-in-three-minutes)
2. [The cost arithmetic, with real numbers](#2-the-cost-arithmetic-with-real-numbers)
3. [The wave workflow](#3-the-wave-workflow)
3b. [The Zwischenrufe file and the collection for the next handoff](#3b-the-zwischenrufe-file-and-the-collection-for-the-next-handoff)
3c. [Who plans what — main session and guardian](#3c-who-plans-what--main-session-and-guardian-have-different-jobs)
3d. [The RTF twin — the handoff as a working document](#3d-the-rtf-twin--the-handoff-as-a-working-document)
4. [Subagent economics](#4-subagent-economics)
5. [What the skill makes visible: cost line, cost table, quota](#5-what-the-skill-makes-visible)
6. [Install](#6-install)
7. [The scripts](#7-the-scripts)
8. [Honest limits](#8-honest-limits)
9. [The facts everything rests on](#9-the-facts-everything-rests-on)
10. [Credits, prior art, license](#10-credits-prior-art-license)

---

## 0. The moral, in five sentences

If you take one thing from this repo, take this:

1. **One session per wave.** Plan, start guardians, merge, write the handoff — all in one
   session. A fresh session costs its ~200k start build; it only pays off past ~200k context.
2. **Collecting costs nothing.** Type test answers, ideas and criticism into the handoff file
   for hours. Zero requests. A chat message, by contrast, re-reads the whole context — at a
   measured 119k context that is ≈ 12k per interruption.
3. **Guardians instead of pings.** One guardian per topic starts its own workers; the main
   session is woken 5× instead of 15×.
4. **Stay under 200k context.** The main session plans, merges, reads reports. Everything
   else lives in agents.
5. **A handoff with a cost table** closes the wave — measured numbers, not feelings.

**The single biggest lever against unnecessary requests** is point 2 — and it now has a file
of its own: the **Zwischenrufe file** with its „Sammlung für das nächste Handoff" block
(→ [section 3b](#3b-the-zwischenrufe-file-and-the-collection-for-the-next-handoff)). The
user's verdict on first use: „was sehr, sehr cleveres" — something very, very clever. The
arithmetic is simple: every chat message you send while the session is waiting on agents is a
**full request** — the whole context is read again, at 119k context roughly 12k tokens for a
„make that button yellow". The same line typed into the Zwischenrufe file costs **nothing**,
and the session picks it up on its next wake-up anyway. Ten stray thoughts during a wave: ten
requests versus none.

**Proven, not claimed:** [`docs/evidenz.md`](docs/evidenz.md) derives from the logbook and the
handoff cost tables that this structure saves **43–50 % of requests and 43–48 % of cost**
against the same work without it — and **73–79 % per completed job**. Every number there is
measured, with its source and the arithmetic shown.

### How a wave runs, for newcomers — copy it, then get it

1. **Start a session.** First message: "I answered the handoff:
   `/Users/…/project/_handoff-project-2026-08-30.md`". Claude reads it and knows everything.
2. **Claude writes the wave plan as a file** (`docs/reviews/YYYY-MM-DD-waveN-plan.md`) before
   any agent starts, so you can look it over first.
3. **Claude starts the guardians** — one per topic, topics cut along *files*. From here it
   runs without you.
4. **You test in parallel** and write everything you notice into the collection section at the
   bottom of the handoff document. Not into the chat. Don't forget ⌘S.
5. **Claude reports back once**, when everything is merged, built and pushed — with a cost
   table and a fresh handoff. Done; the next wave starts at step 1.

### Why working through TextEdit documents is calmer

The terminal collapses long input into `[pasted text]`. A document doesn't: you see the whole
thing, jump between test items, add notes, leave it lying around for two days. Above all it
**does not interrupt the running wave**. Ten items in the document cost the same as one
(nothing); ten items in the chat cost ten full requests and pull the agent out of its work ten
times. Nothing has to be remembered, nothing has to be "said quickly before I forget", nothing
gets lost. One rule: **⌘S before asking Claude to read the file** — unsaved changes are
invisible on disk.

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

## Your collection from the last handoff (copied verbatim)
…

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

## Gedächtnis (memory block — long-term / short-term, 4–6 lines each)
# This session's cost table
| # | Time | What it was about | Req. | Context | read | written | output | equiv. |
…

## Collection for the next handoff
>>>
```

Two of those blocks are easy to skip over and are in fact the core:

- **`## Gedächtnis`** (German for "memory", kept in German because that is how the user
  introduced it) — long-term (what holds permanently: preferences, decisions, prohibitions)
  and short-term (what only matters for the next wave), 4–6 lines each.
- **`## Your collection from the last handoff (copied verbatim)`** — everything the user wrote
  into the collection at the bottom during the last wave is carried **verbatim** into the top
  of the new handoff. Do not summarise, do not shorten, do not drop anything. And: **look at
  the collection once more before finalising** — the user often keeps writing while the
  handoff is already being drafted (wave 28, 16:39).

The details — the path at the very top ready to copy, the project name in the file name,
pre-seeded answer lines, what belongs in a handoff and what doesn't (rules adopted from
Matt Pocock's `/handoff`) — are in `SKILL.md`, section "The wave workflow".

### The user is the bottleneck

The newest rule in the skill (28.08.2026): a human cannot sit at the terminal all day.
Every clarifying question that halts a wave costs hours of wall-clock time. So waves are
cut to **run through without questions**: defensible assumptions are made and flagged in
the handoff, questions are **collected** into the handoff instead of asked one by one in
chat, and **guardians** get a whole topic bundled and report only when everything is done.
(Its *workers* still get exactly ONE job each, 15–25 minutes — bundling happens at the
guardian level, not the worker level.)
Agents expected to run longer than an hour write their result to a file
(`docs/reviews/<date>-<topic>.md`); the handoff lists the expected file, and the **next**
session checks for it while reading the handoff — so the agent finishing costs no request
of its own and no rebuild after the overnight pause.

## 3a. Project start — the start context is the first saving

Every request re-reads the prefix, and the prefix starts with the descriptions of EVERY
globally installed skill, plugin skill and agent. Measured in Aitomat (02.09.2026): **63k
tokens start context, 46 % of it skill and agent descriptions** — most of them irrelevant
for that project. So the first handoff of a new project now does a start-context diet:

1. Decide which skills, plugins and MCP servers the project needs — the generated list
   `~/.claude/SKILLS-UEBERSICHT.md` (`scripts/skills-uebersicht.sh`) has one line per tool.
2. Write `<project>/.claude/settings.json` with `"enabledPlugins": {"<id>@<marketplace>": false}`
   and `"skillOverrides": {"<skill>": "off"}` — one entry per skill, no wildcards.
3. Record the result in the handoff under the mandatory block
   `## Aktive Werkzeuge dieses Projekts`, and update it whenever a tool changes.

Why it matters even more on the API: there the prompt cache lives 5 minutes, not an hour,
so every pause rebuilds the whole start context at ×2. A lean start context plus a
collection file that costs zero requests is what keeps that affordable.

## 3b. The Zwischenrufe file and the collection for the next handoff

**Why.** While the main session is waiting on background agents, every chat message you send
is a **full request**: the entire context is read again. A quick „also: make that button
yellow" costs exactly as much as a fully written order. No skill can prevent this — the
message goes out the moment you press Enter. Ten stray thoughts during one wave are ten
requests for things that could all have waited until the session next woke up. On top of that,
terminals collapse long input into „[Pasted text]", so you cannot even see what you wrote.

**How.** One file per session, created at wave start and opened in TextEdit:

```
<project>/_zwischenrufe-<project>-YYYY-MM-DD-<a|b|c>.md
```

It has two sections:

- **„Zwischenrufe (für diese Session)"** — short notes for the wave that is running right now:
  a bug you can see, a correction, a screenshot path.
- **„Sammlung für das nächste Handoff"** — everything that is not urgent: ideas, new orders,
  criticism, wishes. At the next handoff this block is copied verbatim into the handoff file.
  That is why the handoff no longer carries a collection banner of its own.

You write your notes as lines starting with `>>>` (or name + time). Typing into a file is not
a request, so it costs nothing.

**Marker and answer.** The main session reads the file first on every wake-up — appended to a
command that runs anyway, so again with no extra request — and takes only what is new. It never
deletes anything. Instead it appends a marker line under the last entry it read:

```
— übernommen bis hier, 18:42 —

Antwort Claude, 03.09.2026-18:42:
D6 is done (Finder-style tab rounding), E9 still running.
I saw the screenshot — the handle was behind the frame.

— ab hier wieder Zwischenrufe —

>>>
```

Both sides can then see where "new" begins. **The answer goes into the same file** — the same
text you would otherwise have seen in the chat. You read the file, not the terminal; an answer
that only lands in the chat is an answer you have to go looking for.

**Rules for the agent.** Never write into the file while TextEdit has unsaved changes: read the
live text via `osascript`, write the merged text to disk, then close (`saving no`) and reopen —
and only when TextEdit reports `modified = false`. A new session starts a new file (next date,
next letter); the old one stays open until you close it. `scripts/sammlung-pruefen.sh` checks
before a handoff that no collection was forgotten.

**The user's verdict on first use** (02.09.2026, 19:57): „geniale Lösung — so sparen wir uns
jedes Mal mindestens eine Anfrage."

## 3c. Who plans what — main session and guardian have different jobs

The most expensive common mix-up: a guardian being asked to „work out what needs doing". That
is not its job. The division is sharp:

**The MAIN SESSION writes the wave plan** — as a file, BEFORE any guardian exists
(`docs/reviews/YYYY-MM-DD-waveNN-plan.md`). It contains **every single job** with its three
entries: **What** (the fully written order including evidence, screenshot paths and the user's
quote with a timestamp), **Acceptance** (how you can tell it is done — a test, a screenshot, a
grep) and **Model** (effort). Plus the structural rules that apply to every job, and the split
into tables — one guardian per table, with hard file ownership. Only the main session has the
whole context: the answered handoff, the Zwischenrufe file, the screenshots, the topic store.
Only it can therefore decide what this wave is even for.

**The GUARDIAN invents no jobs.** It receives one table and does exactly five things: it splits
the table into workers, **passes the order text on** (verbatim, not retold — the plan is the
source), builds serially behind the build lock, merges with `git merge --squash`, has Codex
review it and writes the report. Anything new it finds along the way belongs in the report —
not in a job it made up itself.

**Why this makes the main session's model matter.** If the main session writes the order texts,
the quality of ALL subagent prompts hangs on its model. A guardian cannot repair a bad order,
it can only execute it. A vague „make the window nicer" costs three attempts; an order with a
quoted piece of evidence, a screenshot path and an acceptance criterion costs one. The saving
from a cheaper main-session model can therefore be lost several times over elsewhere.

**Open measurement (user, 03.09.2026, 18:38):** so far the main session has run on Opus. The
next session will test **Fable/medium as the main session** and compare via the log line —
requests, tokens, wall clock, and above all: how many jobs needed a second attempt. Until that
line exists the question is open; it will be measured, not guessed.

## 3d. The RTF twin — the handoff as a working document

A handoff is not a printout, it is the place where the user answers. Markdown in a plain
editor makes that painful: headings look like ordinary lines, screenshot paths with spaces
are dead text, and the long copy-line at the top wraps into two. So **every handoff gets an
RTF twin**, produced right after the `.md` by `scripts/handoff-rtf.sh` (Markdown → HTML →
`textutil -convert rtf`, a macOS built-in — no extra dependency):

- **18 pt** body text, bold headings, `>>>` lines highlighted yellow, so structure is visible.
- **Clickable links for every path and URL** — screenshot paths that contain spaces become
  `file://` links with the spaces percent-encoded (`…/ScreenshotY%202026-09-03%20um%2021.10.04.jpg`),
  so one click opens the picture the paragraph is talking about.
- **The header copy-line stays on one line** — it is what the user pastes back into the next
  session, and a torn path is a broken path.
- **The user writes the answers into the RTF**, under the `>>>Userantwort:` markers that the
  handoff pre-seeds under every question and test item.

The agent reads those answers back with one command:

```bash
textutil -convert txt -stdout _handoff-projekt-2026-09-03-v.rtf
```

Division of labour: the `.md` is the source for what the agent writes (edit it, then
regenerate the twin), the `.rtf` carries what the user writes and is copied verbatim into the
next handoff's collection.

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
3. **The report is the hidden cost centre — and here is exactly why.** An agent report is
   paid for **twice over, in two different ways**:
   - **Once, at ×2:** the moment the report arrives it is appended to the main context and
     written into the cache. That is a one-off cache-write at ×2 — it does not repeat.
   - **Then forever, at ×0.1:** from that request on, the report is part of the warm prefix
     and is re-read on **every** later request at ×0.1. Ten more requests in that session =
     ten more ×0.1 readings of the same text.

   So a 4k report costs 8k once **plus** 0.4k × every remaining request of the session —
   after 20 requests that is 8k + 8k = 16k, i.e. **four times its own length**. The ×2 is
   not the expensive half; the endless ×0.1 tail is.

   (The subagent's own 5-minute cache TTL is a separate thing and does not enter this
   calculation: it governs what the agent pays *inside* its own loop, not what its report
   costs in the main context.)

   Hence the report cap ("≤ 300 words, no diffs" — the same number as the report contract in `SKILL.md`) and long results into files: a file path
   is 60 characters in the prefix, the file itself costs nothing until someone reads it.

Model choice (from the table in the skill): finding files, renames, log sifting, tests to
an existing pattern → **fast/cheap, effort low** (with Fable 5 as agent model: always
low). Design decisions, security review → strong model, high effort, or a different model
(Codex/GPT) as a second opinion. Model and effort are visible in the agent description
(`"Fable/low · rename test files"`) so the user sees in the terminal who is working.

Parallel vs. sequential: **parallel for speed, sequential for warmth** — agents cache
separately at 5 minutes; launch five at once and you have five cold caches. Inside a wave
the parallel rule always wins; the pacing rule applies only to work the main session does
itself.

### How a wave is actually structured (waves 25 and 26)

The shape that measured best: **one guardian per disjoint topic**, each with 4–6 workers,
each merging into its own integration branch — then ONE merge guardian for the single
build, the full suite, the bundle and the QA pass. The main session is woken once per
topic instead of once per worker.

| Wave | Structure | Requests | Equivalent | Completion pings | Wall clock |
|---|---|---:|---:|---:|---:|
| 24 | 1 guardian, 12 workers, all building | 62 | 3,143k | 1 + 12 | 2 h 10 |
| 25 | 3 topic guardians + merge guardian, 15 workers | 29 | 1,192k | 5 | 64 min |
| 26 | 3 topic guardians + merge guardian + skill agent, 17 jobs | 34 | 1,159k | 5 | 53 min |
| 27 | 4 topic guardians + merge + skill agent, 19 jobs | 41 | 1,160k | 7 | 78 min |
| 28 | 2 topic guardians **cut along files** + merge + skill agent, 11 jobs + skill | 33 | 1,080k | 5 | 57 min |

Waves 27 and 28 add the ceiling and the correction: a *fourth* guardian bought nothing (same
tokens, 25 minutes more, first merge conflicts), while **two guardians cut strictly along
FILES** produced the cheapest wave measured and zero conflicts. Cut topics along files, not
along words. Full arithmetic: [`docs/evidenz.md`](docs/evidenz.md).

Four rules the user added on 30.08.2026 while watching wave 26 run:

1. **The wave plan is a file, not a set of prompts.** Before anything starts, the main
   session writes `docs/reviews/<date>-welleN-plan.md` — structure rules on top, then one
   table per topic (ID · assignment · acceptance criterion · model/effort) — commits it,
   opens it in the editor, and only then starts all guardians in ONE message, each brief
   pointing at the file. The user can look the wave over before it is expensive to change.
2. **Model and effort in the label, for workers too**: `Modell/Effort · ID Kurzname`, e.g.
   `Fable/low · A1 Aufnahme-Rot`. The user reads the running-agent list at the bottom of
   the screen. Codex is a shell command, not an agent — it never appears there; say so.
3. **Push belongs to the job.** Guardians and skill agents push their branch before
   reporting done, and name the pushed hash. A branch that exists only locally is not
   delivered.
4. **Codex as quality manager.** With fresh Codex quota, every topic guardian has its
   integration branch reviewed before its closing report and fixes the P1s itself. In wave
   26 that found 4 P1 issues across three Fable assignments.

### Lessons, measured

- Topic guardians roughly halve requests and wall clock against one guardian with 12
  workers (62 / 2 h 10 → 29 / 64 min → 34 / 53 min).
- The start-up cache build (≈ 200k, once) is the largest single item of a short session —
  so continuing in the same session beats a fresh one while context stays under 200k.
- Context stayed flat at ~114k across a whole wave, because all the work lived in agents.
- Completion pings are the main session's cost driver: 5 instead of 13.
- A pause > 60 min costs a rebuild (≈ context × 2) — at 114k ≈ 230k, still less than a
  fresh session paying its start build plus re-briefing.

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

for f in ctx.sh codex-limit.sh session-costs.sh session-kosten.sh; do
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
| `scripts/handoff-rtf.sh` | The RTF twin of a handoff: Markdown → HTML → `textutil -convert rtf`. 18 pt, bold headings, `>>>` lines yellow, every path/URL a clickable `file://` link (spaces percent-encoded), header copy-line kept on one line. The user answers in the `.rtf` under `>>>Userantwort:`; read it back with `textutil -convert txt -stdout <file>.rtf`. | `handoff-rtf.sh _handoff-projekt-2026-09-03.md` |
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
German. `SKILL.md` is English throughout; the German words that remain are literal quotes
of what the skill actually outputs (the cost line, banner text, handoff section names) —
those stay German because that is what the user reads. The full German twin is
`SKILL.de.md`; `references/historie.md`, which records the sessions the rules came from,
is German-only, and the scripts are commented in German.

### „Was ist eigentlich PR 1?" — pull requests in one paragraph

GitHub shows a tab **Pull requests** with a counter (`PR 1`). A pull request is somebody
else's proposed change: they copy the repository (fork), change something in their copy and
then *ask* for the change to be pulled into this one. Nothing is changed here until the
change is merged — a PR is a proposal plus a discussion thread, not an edit. Open it, read
the diff under "Files changed", and either **Merge pull request** (accept) or **Close**
(decline, with a friendly line saying why). The counter shows only the OPEN ones, so it
drops back to zero once each has been merged or closed.

License: MIT.
