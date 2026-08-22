---
name: warm-handoff
description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, warns before cache-destroying actions, recommends a fresh session past a context threshold, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", or when resuming after a gap.
---

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

Claude Code caches your conversation prefix. Working *inside* that cache is fast and cheap;
rebuilding it is slow and expensive. This skill makes the cache window visible, keeps you
inside it, and — when leaving it is the better deal — writes the handoff that lets a fresh
session continue seamlessly.

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

1. **Timestamp every reply** (e.g. `(22.08.2026, 12:50)`). The user can then see at a glance
   whether the last exchange is under an hour old — no tooling required. This is the cheapest
   cache monitor that exists.
2. **State the window when asked** ("am I still cached?"): last exchange + 60 minutes,
   sliding. Answering the question itself resets the timer.
3. **Warn before cache-destroying actions** — a mid-session `/model` or `/effort` change, a
   flaky MCP server in the config — *before* the user pays for it.
4. **Recommend a fresh session past the threshold.** Default: at ~**400k tokens of context**,
   say so proactively. Above that, a handoff + fresh start is many times cheaper than another
   full cache write, and past ~500–600k answer quality degrades from sheer information load
   even while the cache is warm. Under ~150k, keeping the cache warm on request is fine.
5. **Write the handoff automatically after every big work wave** — do not wait to be asked.

## What a cache rebuild looks like (and doesn't)

- **You cannot see a rebuild in the context counter.** Context size is the same before and
  after — it's the same content, just frozen again. The counter measures size, not cost.
- **Where you DO see it: your 5-hour and weekly usage quota.** A rebuild re-writes the whole
  prefix at cache-write rates, so the quota drops noticeably faster. A lost cache doesn't
  make your context bigger — it makes it more expensive.
- **Short messages inside a warm cache are essentially free — send them freely.** Each
  message re-reads the cached prefix at ~1/10 of normal price and pays full price only for
  the few new tokens. Quick questions and small side-topics between waves are encouraged:
  they cost almost nothing AND they reset the 1-hour timer. Batching is only for big work
  packages (so they run as one wave) — never for chat.

## The wave workflow (the heart of this skill)

The economics reward a specific rhythm:

- **The user batches work into waves**: one big message with many tasks. Claude works through
  it (subagents welcome — they cache separately at 5 min, so batch their jobs too). During
  the wave the cache stays warm by itself; short back-and-forth messages in between are cheap
  — small side-topics are *encouraged* while the main work runs.
- **After each wave, Claude writes a handoff document**: a dated Markdown file
  (`_handoff-YYYY-MM-DD.md`) containing what was delivered, running state, open items,
  project constraints — **and the current test checklist at the bottom**, with an empty
  answer line (`>>`) under every test item.
- **The user works in the handoff file with a plain text editor** (TextEdit or similar), not
  in the chat box: they answer each test point directly beneath it, and collect new ideas and
  findings in the same file — even across a long pause. Why an editor and not the terminal:
  chat inputs collapse long pastes into `[pasted text]`, so the user loses overview; in the
  editor they see the whole document. **Rule: save (⌘S) before telling Claude to read it** —
  unsaved editor changes are invisible on disk.
- **Next session starts with only the handoff** — fresh context (~20k instead of 500k+),
  fully briefed, cache rebuilt once at minimum size. Claude reads the annotated test answers
  and new ideas from the file and starts the next wave.

**Open the handoff for the user automatically.** Right after writing it, open the file in a
plain text editor so the user *sees* that the wave is done and the annotated test list is
ready — on macOS: `open -a TextEdit <file>` (always name the editor explicitly; the system
default for `.md` is often an IDE or preview app the user doesn't want). On Windows:
`notepad <file>`; on Linux: `xdg-open <file>`.

If the user mentions that double-clicking `.md` files opens the wrong app, offer to fix the
default (macOS, via [duti](https://github.com/moretension/duti): `brew install duti && duti
-s com.apple.TextEdit .md all`) — many users have fought and lost this battle manually.

**Tip for lost handoffs** (tell the user once): if they closed the document and can't find
the file, TextEdit ▸ **Ablage ▸ Benutzte Dokumente** (File ▸ Open Recent) brings back any
recently closed handoff without hunting through Finder.

When Claude finishes a handoff it should say so and explain the loop to the user once:
*"Handoff written, your test list is at the bottom. Answer under the test points, add new
ideas, ⌘S — and give the file to a fresh session (or to me, if you're still in the window)."*

## When to stay vs. when to hand off

| Situation | Recommendation |
|---|---|
| Pause < 1 h ahead, context < 150k | Just continue; optionally keep warm on request (max ~3 cycles) |
| Pause < 1 h, context 150–400k | Continue, but write the handoff now as insurance |
| Context > 400k | Handoff + fresh session — say so proactively |
| Pause > 1 h (cache gone anyway) | Never rebuild the giant context: handoff + fresh session |
| Mid-session model/effort change wanted | Warn: full cache rebuild; suggest doing it at the next fresh session instead |

## Writing the handoff well (rules adopted from Matt Pocock's /handoff)

- **Reference, don't copy.** Specs, plans, commits, diffs and issues that are already written
  down get linked by path or URL — never pasted into the handoff. Keeps the file small and
  the settled detail in ONE place instead of two that drift.
- **Redact secrets** (keys, tokens, passwords) before writing the file.
- **Name suggested skills** for the next session — what the fresh agent should reach for.
- One deliberate difference: Pocock writes handoffs to the temp directory (transit document)
  and recommends `/compact` for same-directory continuation. This skill writes them **into
  the project** (dated, part of the working rhythm, the user annotates them) and prefers
  handoff + fresh session over `/compact` past the context threshold — on subscription
  plans, `/compact` keeps the huge expensive prefix alive; a fresh ~20k session does not.

## Honesty rules

- There is no background timer: Claude only acts when a request arrives. That is exactly why
  the handoff is written *proactively at the end of a wave*, not "when the hour is nearly up".
- Cost claims should be shown as arithmetic when it matters (cache-write vs. re-read pricing),
  not asserted.

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
