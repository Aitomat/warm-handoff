# warm-handoff 🏄

**A cache-aware session pacer for Claude Code — with a built-in handoff ritual.**

Claude Code caches your conversation prefix (on Pro/Max: a **1-hour sliding TTL** — every
message resets the timer). Working inside that window is cheap; rebuilding a 500k-token
context is not. Plenty of skills write handoff documents. This one answers the harder
question first: **when** — by coupling the handoff moment to cache economics.

## What it does

- ⏱ **Timestamps every reply** so you can see at a glance whether you're still inside the
  1-hour window — the cheapest cache monitor there is.
- ⚠️ **Warns before cache-killing actions**: mid-session model/effort switches, flaky MCP
  servers, prefix changes.
- 📏 **Recommends a fresh session past ~400k context** (configurable judgment call): beyond
  that, handoff + restart beats another cache write — and quality drops from context overload.
- 📝 **Writes a handoff automatically after every work wave**: delivered work, running state,
  open items — and **your test checklist at the bottom**, ready to annotate.
- 🔁 **Teaches the wave workflow**: batch work into big waves, chat cheaply in between,
  answer the test list in a plain text editor (you see the whole document — chat inputs
  collapse long text into `[pasted text]`), save with ⌘S, hand the file to the next session.
  Fresh session starts at ~20k context instead of 500k+.

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

## The facts it is built on

| Rule | Value |
|---|---|
| Pro/Max cache TTL | 1 hour, **sliding** — every exchange resets it |
| Over plan limits (paid credits) | drops to 5 minutes automatically |
| Subagents | always 5 minutes, even on Max |
| Env overrides | `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1` |

Source: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching).

## Why not just any handoff skill?

There are at least eight published handoff skills. None of them decide the *timing*: they
write a document when you ask. warm-handoff treats the handoff as the exit move of a cache
economy — it tells you when continuing is cheap, when a restart is cheaper, and produces the
document at exactly that moment, test list included.

## License

MIT
