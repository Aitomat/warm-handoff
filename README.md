# warm-handoff 🏄

**A Claude Code skill that paces your session around the prompt cache: it measures where
you stand, keeps requests down, and writes a handoff document at the right moment.**

## The problem

Claude Code caches your conversation prefix between turns. Working *inside* that cache is
fast and cheap; rebuilding it — because a pause was too long, or the model/effort changed
mid-session — is slow and expensive. None of this is visible while a session runs: not the
current context size, not how many requests a single message triggered, not whether the last
round was cheap or expensive. Without those numbers, people optimise the wrong thing — typing
shorter messages — while the real cost is a work loop of file reads, searches and edits they
never see.

## What it delivers

- **A timestamp under every reply** — date and time, read fresh from `date`, never
  extrapolated from an earlier turn.
- **Measured context size, not a guess** — read out of the session's own `.jsonl` file
  instead of estimated ("cache is fresh (~20k)" turned out to be ~80k in the incident that
  produced this rule).
- **A cost line under substantial replies** — what the last request cost, split into read /
  written / output, plus the running session total.
- **A handoff document at the end of a work wave** — delivered work, open items, a roadmap
  for the next waves, and the user's test checklist at the bottom, ready to annotate.
- **A cost table per session** — one row per exchange, so you can see which stretch of work
  was expensive and why.
- **Paid quota surfaced at the top of the handoff** — Claude Code's own 5-hour/weekly usage
  and Codex's, so quota that would otherwise silently expire gets suggested for something.

## Install

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

**To have it fire every session without typing anything**, add one line to your global
`~/.claude/CLAUDE.md`:

```
At the start of every session, invoke the warm-handoff skill.
```

## What a cost line and a cost table look like

Under a substantial reply:

```
Last measured request: 366k read (×0.1) + 0.4k written (×2) + 2.9k output (×5) ≈ 52k ·
session so far: 265 requests, 9,520k
```

In the handoff, one row per exchange (`session-costs.sh`):

```
| # | Time  | What it was about          | Req. | Context | read   | written | output | equiv. |
| 1 | 14:05 | Handoff answered …         |  147 | 223k    | 22171k | 562k    | 208k   | 4380k  |
| 6 | 17:22 | So the thing I mentioned … |   25 | 319k    |  7346k | 108k    |  69k   | 1297k  |
| Σ |       | 10 stretches                |  246 | 345k    | 49906k | 811k    | 396k   | 8594k  |

Most expensive stretch:  #1 at 14:05 (4380k equivalents, 147 requests)
Cache hit rate:          1.6 % written (under 10 % = warm)
```

`equiv.` is the three cost items — read (×0.1), written (×2), output (×5) — converted to one
common price and added up, so items billed at different rates can be compared.

## How it's meant to work

The skill assumes a **wave rhythm**: you send one bundled message with everything for the
next stretch of work, Claude works through it — subagents by default for anything with more
than a handful of steps, since their small context is far cheaper to work in than your fat
one — and at the end it writes a handoff document instead of trailing off in chat. You answer
the test list and add new ideas inside that document, in a plain text editor, at whatever
pace suits you. The next session starts from that file alone: a small, cheap, fully briefed
context instead of a five-hundred-thousand-token one. Short side questions in between are
fine and cheap; what the skill pushes back on is the *machine's* own chatter — status notes,
narrated tool steps, uncapped subagent reports — because that is where most of the 147
requests in the measured session actually went.

## Honest limits

- The measurements come from real sessions on a subscription plan with the 1-hour cache —
  one project, one developer's rhythm. Your ratios will differ, which is why the scripts
  that produce these numbers ship with the skill instead of just the results.
- The per-technique savings are estimates from a second model reasoning over the same
  session data. They overlap and must not be summed.
- Dollar figures are API list-price equivalents; nobody on a Pro/Max subscription pays that
  sum, it measures what the quota is being charged.
- The skill reports a cache rebuild only when it can derive a cause (a >1h gap, a model
  switch, a CLAUDE.md edit, an MCP restart) — otherwise it says nothing rather than guessing.

## The facts it is built on

| Rule | Value |
|---|---|
| Pro/Max cache TTL | 1 hour, **sliding** — every exchange resets it |
| Over plan limits (paid credits) | drops to 5 minutes automatically |
| Subagents | always 5 minutes, even on Max |
| Cache read / cache write / own output | ×0.1 / ×2 (1-h TTL) / ×5 |
| Env overrides | `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1` |

Source: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching).

## Author

Built and maintained by **Yasin Akgün** — [github.com/Aitomat](https://github.com/Aitomat).
The skill grew out of building [Aitomat](https://aitomat.ai), a macOS app, with Claude Code
every day: every rule in `SKILL.md` started as a session that went wrong or a bill that
looked odd, and stayed only after the numbers backed it up — which is also why rules get
revoked there when a later measurement contradicts them.

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
