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
- 📏 **Recommends a fresh session around ~200k context (hard ceiling before 400k)** (configurable judgment call): beyond
  that, handoff + restart beats another cache write — and quality drops from context overload.
- 📝 **Writes a handoff automatically after every work wave**: delivered work, running state,
  open items — and **your test checklist at the bottom**, ready to annotate.
- 👀 **Opens every user-facing document in your text editor automatically** (`open -a
  TextEdit` on macOS) — handoffs, plans, reports, checklists. You *see* when something is
  ready instead of hunting for file paths. Each document carries a one-line header
  inviting comments, marked with `>>>` at line start — Claude reads those back as your
  answers, and checks for unsaved editor changes before reading (offering to adopt or
  save them). Lost a closed document? TextEdit ▸ File ▸ Open Recent brings it back.
- 🔁 **Teaches the wave workflow**: batch work into big waves, chat cheaply in between,
  answer the test list in a plain text editor (you see the whole document — chat inputs
  collapse long text into `[pasted text]`), then hand the file to the next session.
  **Press ⌘S before handing it over:** Claude can only read what is saved on disk — your
  typed-but-unsaved edits are invisible to it, and the editor's autosave is delayed, so
  without saving, Claude may silently read an outdated version of your answers.
  On macOS the skill adds a safety net: before reading, Claude asks TextEdit (via
  AppleScript) whether the document has unsaved changes — and if so, offers to take them
  over or save them for you.
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

Corollary, with honest arithmetic: **a short message costs ~1/10 of your WHOLE context.**
At 30k context that is pocket change — chat freely. At 200k+ it is ~20k full-price token
equivalents per exchange, and ten quick back-and-forths equal one full context read. So:
the bigger the context, the more you should batch — ideally one long, structured message
per wave (handoff to handoff, answers collected under the test items), short questions
only when they truly can't wait. Every message still resets the 1-hour timer.

**Sweetspot for a fresh session: ~200k context.** Once the wave is done and the handoff
is written, don't ride a fat context onward "because the cache is warm" — every further
work-step re-reads it at 1/10. Recommended: hand off and restart around ~200k, and well
before 400k in any case. (Claude's own tool-steps dominate request count, so a small
context while work runs matters far more than how often the user writes.)

## The window as a friendly coach

The 1-hour window is meant as a POSITIVE motivator, not cost-anxiety: "answer within the
hour and the wave keeps riding" works like a streak — it nudges you to test now, dictate
answers now, launch the next wave now, while everything is fresh. The pre-seeded test
questions remove the blank page: cursor after the marker, speak, done.

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
