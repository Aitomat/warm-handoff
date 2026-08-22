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

## What a cache rebuild costs (and where you see it)

You **cannot** see a rebuild in the context counter — the context is the same size before and
after; only the price changed. Where you *do* see it: your **5-hour and weekly usage quota**,
which drops noticeably faster whenever a big prefix gets re-written. That's the whole game:
a lost cache doesn't make your session bigger, it makes it more expensive.

Corollary: **short messages inside a warm cache are essentially free.** The cached prefix is
re-read at ~1/10 of normal price; you pay full price only for the few new tokens — and every
message resets the 1-hour timer. So chat freely between waves; batch only the big work
packages, never the conversation.

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
