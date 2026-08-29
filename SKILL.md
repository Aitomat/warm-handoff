---
name: warm-handoff
description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, warns before cache-destroying actions, recommends a fresh session past a context threshold, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", or when resuming after a gap.
---

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

**One sentence:** Handoff → fresh session → handoff. The user collects everything
(test answers, ideas, critique) in ONE handoff file over hours, starts a fresh session,
the agent works it all off through a few subagents and writes the next handoff.
Full history with dated user quotes and the reasoning behind every rule:
`references/historie.md` (read it when a rule here seems odd — do not load it by default).

## The facts (Claude Code docs, 2026-08)

- Pro/Max: **1-hour sliding cache TTL** — every request resets it. Subagents: strict 5 min.
- Cache killers regardless of clock: mid-session `/model` or `/effort` change, editing
  CLAUDE.md/system prompt, MCP server restart. Set model + effort at session START.
- Prices relative to fresh input: **cache read ×0.1 · cache write ×2 (1-h TTL) · own output ×5.**
- Every request re-reads the whole prefix. Cost = requests × context. The user's messages
  are a rounding error; the agent's own tool steps and reports are the bill.

## Every reply — three honesty rules

1. **Timestamp from a `date` call in THAT reply** (`date "+%d.%m.%Y %H:%M"`, piggybacked on
   any command). No `date` this turn → no timestamp. Never extrapolate, never `~19:40`.
2. **Never guess context size.** Sources: the user's status line, or `~/.claude/ctx.sh`
   appended to a command that runs anyway (`date … && ~/.claude/ctx.sh`). It reads the
   session JSONL (`cache_read + cache_creation` of the last request). None → "not measured".
3. **Cost line under every substantive reply**, from the LAST COMPLETED request, labeled so:
   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Skip it on one-liners. If a round cost > 2× the
   session's average, say why ONCE per wave, kindly, with the cheaper path — the cause is
   almost always the agent (whole files read, raw output, long replies), not the user.

## Sweetspot — when to hand off

| What comes next | Hand off at |
|---|---|
| Big build/review wave (hundreds of tool steps) | ~200k |
| Mixed | ~250k |
| Only talk / small edits | ~300k |
| Anything | 400k hard ceiling |

Break-even for a fresh session: `(start_ctx × 2) / ((old_ctx − start_ctx) × 0.1)` steps.
Start context is MEASURED per project (82–125k seen), never assumed "~20k". Steps = tool
calls, not user messages. Talking on a fat context is cheap; working on it is not.
Say it at every wave end, casually: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
While the agent's own tool loop runs, a user message is nearly free (attached to the next
request); while subagents run or the agent idles, it costs the full context × 0.1.

## The real lever: fewer requests

Measured: 147 requests, 13 from the user; own output = 23 % of cost. Targets, in order:
**fewer requests · shorter own output · smaller context.** Techniques: batch all independent
reads in one reply · one script that does ten things and prints one summary · pre-filter
output (`grep`/`tail`) · grep instead of reading whole files · no per-agent status messages
(one summary when the fleet lands) · reports as files, not chat · own output budget:
interim ≤ 100 words, final ≤ 500, details in files. Terminal tab-suggestions and every
agent completion notification are full requests too.

## Subagents — the default way to work

- **Guardian agent (Wächter).** For a build wave, ONE orchestrating agent (Opus, low/normal
  effort) gets the whole plan as a file, spawns the worker agents itself, merges, tests,
  bundles, cleans `.build` of merged worktrees, writes the report — the main session is
  woken ONCE instead of once per agent (8 → 1 notifications ≈ 140k saved at 190k ctx).
  Workers' questions land at the guardian, so briefs must be complete: paths, goal,
  limits, acceptance criteria, "no questions — decide, document the assumption".
- **The guardian starts every worker at once, in a single message** (one batch of Agent
  calls), never one after another — a serial tail of workers is what turns a cheap wave
  into a long one. Each worker's FIRST step is to pull the current branch tip (`git pull`
  / `git fetch && git rebase`) before touching any file, so it never builds on a stale base.
- **Workers do NOT build or test.** They write code + tests, at most `swiftc -parse`, and
  commit early. Only the guardian builds — ONCE, serially, in the main repo — and runs the
  suite. 12 workers × one cold build each = 400+ compiler processes, load 70, 18 GB RAM
  swapped to a halt, forced reboot, 90 minutes lost (29.08.2026). If workers must build,
  never more than 4 at once; `memory_pressure` before the full suite.
- **Cut agents to ~30 minutes, ONE task each** (not 40 minutes / 2–3 tasks — a single focused
  job lands faster and is easier to merge). Longer work delivers into a FILE
  (`docs/reviews/<date>-<topic>.md`) and reports only the path; the handoff lists the
  expected files and the next session checks `ls` first. Never wait for a straggler.
- **Merge each worker's branch the moment it lands**, don't batch merges for later — conflicts
  are cheaper to resolve one at a time, right after the work is fresh. Run the FULL test
  suite only ONCE, at the very end, against the merged result; a flaky/failing individual
  test gets investigated on its own rather than re-running the whole suite.
- **Guardian writes an interim status file after 60 minutes** if the wave is still running
  (path in the handoff-to-be, e.g. `docs/wellen/<date>-zwischenstand.md`) — so a session that
  checks in mid-wave, or a handoff written before the guardian finishes, has something real
  to point to. **The handoff starts even without a finished guardian**: list the guardian and
  its still-running workers under "expected agent results", the next session checks them.
- **Model + effort in the visible label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
  Fable 5 as subagent: **always effort low**; for hard review/design use Opus or a second
  architecture (Codex/GPT). Never review your own output yourself — route to Codex.
- **Agents test before the user.** Full suite + a QA agent that launches the app and clicks
  every test item once; the user should mostly say "works, thanks". **The QA agent closes
  the windows/processes it opened for testing** before it reports done — the user shouldn't
  inherit a pile of leftover test instances.
- Report contract: ≤ 300 words, status/decisions/evidence-with-paths/risks/next; no
  chronicle, no pasted logs. Subagent tokens still hit the weekly quota — what they save is
  the MAIN context (each step ≈ 1/5 the cost, and nothing of it stays in the session).
- Pacing: user present + in a hurry → parallel; user away → sequential (each completion
  keeps the cache warm). Never invent busywork.

## Paid quota — see it, use it, by account size

- `~/.claude/codex-limit.sh [--kurz|--json]` reads Codex `rate_limits` from its last session
  file — only as fresh as the last Codex run; `null` = unknown, not 0. Once per session send
  a tiny ping attached to the first real Codex call (`codex exec --skip-git-repo-check
  "Antworte nur mit: bereit"`). Claude Code quota: `cat ~/.claude/.claude-kontingent`
  (5h/7d %, written by the status line; web UI is the authority when they differ).
- Handoff block "Was noch im Tank ist" right after the status: numbers + measurement age +
  a CONCRETE proposal if lots is free (big review, long test run, second opinion). Unused
  quota expires. Gemini/OpenRouter: no readable balance — say so, never estimate.
- **Small Codex account (Plus, ~20 $)** → Codex does ONLY QA: review, second opinion,
  test runs, acceptance. No build jobs, no "continue at 23:05". Large account → use freely.

## The wave workflow and the handoff file

Write the handoff after every big wave, unprompted. Path `<project>/_handoff-<projekt>-YYYY-MM-DD[-b].md`
(project name in the file name AND title). Hard-wrap prose at ~60–70 chars; commands,
paths, URLs on one line. Reference, don't copy (paths/URLs); redact secrets; name skills
for the next session. Structure, top to bottom:

1. Title with date/time. Then the copy-line for the next session:
   `> \`Ich habe das Handoff beantwortet: /abs/path/_handoff-….md\``
   plus "you can write directly in this file — start lines with >>> or name + timestamp".
2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   (`- [ ] path (agent, started HH:MM)`).
3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — read the previous
   handoff's collection area IMMEDIATELY before writing (same tool call as the unsaved-
   changes guard, including unsaved editor text) and copy it VERBATIM, then a block
   "Was ich daraus gemacht habe" mapping each item → built / answered / roadmap.
   Also check the handoff BEFORE that one for late additions. Never rewrite the user's text.
4. Previous test answers → what became of them, one line each ("your T1 answer taken as:
   … — correct?"). Unanswered items carry over, marked.
5. **Testliste vN** — every item pre-seeded with an empty `>>>Userantwort:` line.
6. Banner (Markdown headings don't stand out in TextEdit — lines and caps do):
   ```
   ═══════════════════════════════════════════════════════════
      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   ═══════════════════════════════════════════════════════════
   >>>Userantwort:
   ```
7. **Der rote Faden** — next 2–3 waves as short paragraphs, each with
   `>>>Hast du dazu noch was anzumerken?`; then a compact Themenspeicher; then
   **Hauptdokumente** (3–6 real files with absolute path + one line + freshness).
8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (unit = span between two
   user messages; explain k = thousand, context column ≠ cost) + honest findings, then the
   closing line with MEASURED context and start context: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** with `aus: /abs/path` and an empty `>>>`.
   The user collects here while the next wave runs — collecting costs zero requests.

Questions for the user go into the handoff (`## Fragen an dich` with `>>>Antwort:`),
not the chat: one chat question blocks a wave, ten in the file block nothing. Cut waves
so they run through without asking; take the likelier reading and document it.

## Editor rules (macOS / TextEdit)

- Open every user-facing document immediately: `open -a TextEdit <file>`. This applies to any
  newly mentioned document, not only the handoff — a plan, a QA report, a review file: the
  moment it exists and is meant for the user to read, open it. Offer once:
  tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt default font
  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md` default app via `duti`.
- **Unsaved-changes guard before reading:**
  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
  if modified, read the live text (`… get text of (first document whose name is "…")`).
- **Never write into, close, save or move the handoff the user has open.** A new handoff is
  always a NEW file. Archive old ones to `handoff-archiv/` (mv, never rm) only after the
  user closed them; otherwise note "archiving pending" in the new handoff.
- If Claude edited a file the user has open and it is unmodified → close + reopen so they
  see the new version; modified → ask, never close.
- Say once: long dictation belongs in the handoff file, short commands in the terminal
  (terminals collapse long input to `[pasted text]`); TextEdit ▸ File ▸ Open Recent finds
  lost handoffs.

## Cache rebuild — detect, don't guess

Hit rate = Σ cache_creation / Σ cache_read from the session JSONL; < 10 % = warm. Big
single writes are usually appends, not rebuilds. Mention a rebuild ONCE, with the cause,
only when it is derivable: gap > 60 min between two `date` reads, a model/effort switch,
a CLAUDE.md edit, an MCP restart. Unknown cause → say nothing. Explain costs as arithmetic
("22k because context is 220k and reads cost ×0.1"), never as assertion; correct your own
earlier misstatements explicitly.

## Logbook and setup

Append one line per handoff to `~/.claude/warm-handoff-log.md`:
`| 22.08.2026 14:40 | ctx 85k | 2 waves | rebuilds: 1 (pause 90min) | est. waste ~60k |`
Summarize patterns every ~50 entries. Always-on: add "At the start of every session,
invoke the warm-handoff skill." to `~/.claude/CLAUDE.md`. Scripts: `scripts/ctx.sh`,
`scripts/session-costs.sh` (= `session-kosten.sh`), `scripts/codex-limit.sh` → copy to `~/.claude/`.
Terminal-neutral: say "your status line", not a specific host's field.
