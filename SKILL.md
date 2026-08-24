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

1. **Timestamp every reply** (e.g. `(22.08.2026, 12:50)`) — and **only from a `date` call
   made in THAT SAME reply. Hard rule: no `date` run in this turn → write NO timestamp at
   all.** An LLM has no sense of elapsed time; the classic failure is extrapolating from a
   `date` read a few turns earlier ("it was 16:28, two agents finished, so ~16:47") — that
   produced stamps 15+ minutes wrong in practice. Extrapolated ≠ read. Piggyback the read
   onto any tool call the reply makes anyway (`… && date "+%H:%M"`), or run `date` alone;
   a missing stamp is honest, a guessed one actively misleads the user who relies on it
   to judge the cache window. This is the cheapest cache monitor that exists.
   **Always stamp DATE + time together** (`date "+%d.%m.%Y %H:%M"`), even when the day
   obviously hasn't changed — handoffs and logs get read days later, and a bare "16:47"
   is ambiguous by then. The read costs nothing: append it to any command the reply
   already runs.
   **The #1 trap: replies to background-agent notifications.** When a subagent
   finishes and Claude writes a short status update, that reply usually makes NO
   tool call — so there is nothing to piggyback on, and the temptation is to
   extrapolate ("last read 18:34, three agents done, so ~19:40"). A tilde does
   NOT make a guess honest — `~19:40` is still a fabricated stamp (real time was
   20:02 in practice, 24.08.2026). Rule: agent-status replies either run `date`
   as their one tool call, or carry NO time at all. Never `~`-stamps.
2. **State the window when asked** ("am I still cached?"): last exchange + 60 minutes,
   sliding. Answering the question itself resets the timer.
3. **Warn before cache-destroying actions** — a mid-session `/model` or `/effort` change, a
   flaky MCP server in the config — *before* the user pays for it.
4. **Measure the context size at every wave end — don't wait to be asked.** The skill has
   no background process; the threshold rule only works if Claude actually checks. So:
   at every handoff/wave end (and whenever finishing a large batch of subagent work,
   which grows context fast), read the current context size from the status line or a
   monitor and state it in the reply. A threshold that nobody measures is decoration —
   this exact failure happened once: the user crossed 400k unnoticed while Claude was
   busy orchestrating, and had to point it out himself.
5. **Recommend a fresh session at the sweetspot.** Default: around ~**200k tokens of
   context** — once the wave is done and the handoff is written, say so proactively;
   ~**400k** is the hard ceiling, never ride past it. Rationale: every further work-step
   re-reads the whole prefix at 1/10, so a big wave on a fat context costs multiples of
   the same wave in a fresh ~30k session, and past ~500–600k answer quality degrades from
   sheer information load even while the cache is warm. Under ~150k, staying is fine.
5. **Write the handoff automatically after every big work wave** — do not wait to be asked.

## What a cache rebuild looks like (and doesn't)

- **You cannot see a rebuild in the context counter.** Context size is the same before and
  after — it's the same content, just frozen again. The counter measures size, not cost.
- **Where you DO see it: your 5-hour and weekly usage quota.** A rebuild re-writes the whole
  prefix at cache-write rates, so the quota drops noticeably faster. A lost cache doesn't
  make your context bigger — it makes it more expensive.
- **A short message costs ~1/10 of the WHOLE context — cheap when small, real when fat.**
  At 30k context, chat freely (near-free, and it resets the 1-hour timer). At 200k+, each
  exchange is ~20k full-price equivalents and ten quick back-and-forths equal one full
  context read: batch conversation too — ideally ONE long structured message per wave,
  handoff to handoff, answers collected under the test items; short questions only when
  they can't wait.

## When does the hour actually start? (users always ask this)

The 1-hour timer resets on **every request in the session** — not just the user's
messages. That includes each of Claude's own tool-steps, and each status message Claude
emits when a background subagent finishes. Consequences worth telling the user:

- The hour counts from **Claude's last output**, whichever side produced the last
  activity. "Agent Y finished, here's the handoff" at 16:30 → the user has until ~17:30
  to answer warmly. Reading costs the user nothing; only their reply is a new request.
- While Claude waits on subagents, its own "agent X done" interim reports keep the cache
  warm automatically — no dedicated keep-alive needed during active waves.
- Work through subagents by default for heavy lifting: they run in their own small
  contexts (5-min TTL, cached separately), so the main context stays lean while the
  completion notifications double as free cache refreshes.

## Pacing: parallel for speed, sequential for warmth

Subagents are not just a context-saver — their SCHEDULING is a cache instrument. Two modes,
chosen by what the user needs right now (ask, or react to cues like "Zeitdruck" /
"ich gehe ins Bett"):

- **User is present and wants speed** → run subagents IN PARALLEL. Everything lands fast;
  the user answers between waves and the timer never gets close to expiring.
- **User steps away (lunch, evening, night)** → run subagents SEQUENTIALLY. Each completion
  wakes Claude, produces a report — a new request that resets the 1-hour timer. The user
  returns hours later to a still-warm cache and a finished handoff, having typed nothing.
  Claude's goal while the user is away: always produce SOME output within each hour, work
  chained through the queue, handoff at the end.
- Honest limit: sequential mode keeps the cache warm only while real work remains. For an
  8-hour absence, first build a work queue big enough to span it (backlog items, review
  rounds, doc sweeps) — plan it WITH the user before they leave. Never invent busywork
  just to touch the cache; if the queue runs dry, write the handoff and let the cache go.
- Model economics: the orchestrator holds the big cached context — subagents don't. Run
  subagents on a strong model with LOW reasoning effort for mechanical work and reserve
  high effort for hard review/design steps; set the session's model+effort once at start
  (mid-session switches kill the cache).

## The window as a friendly coach (frame it this way)

Present the 1-hour window, the handoff ritual and the test list as POSITIVE motivators,
never as pressure or cost-anxiety. The sliding hour is a natural work rhythm: "answer
within the hour and the wave keeps riding" is the same gentle pull as a streak — it
nudges the user to test the delivered items now, dictate answers now, fire the next wave
now, while everything is fresh. The pre-seeded test questions make re-entry effortless
(no blank page — just put the cursor after the marker and speak). Claude should
occasionally voice this framing ("window's still warm — perfect moment for the test
list"), and celebrate kept streaks in the logbook rather than only counting waste.

## The wave workflow (the heart of this skill)

The economics reward a specific rhythm:

- **The user batches work into waves**: one big message with many tasks. Claude works through
  it (subagents welcome — they cache separately at 5 min, so batch their jobs too). During
  the wave the cache stays warm by itself; short back-and-forth messages in between are cheap
  — small side-topics are *encouraged* while the main work runs.
- **After each wave, Claude writes a handoff document**: a dated Markdown file
  (`_handoff-YYYY-MM-DD.md`) containing what was delivered, running state, open items,
  project constraints — **and the current test checklist at the bottom**. **Pre-seed every
  test item with an answer line**, ready to dictate into:

  ```
  ## T3 — Dark/light toggle inverted
  <test description>

  >>>Answer:
  ```

  (Use the user's language for the marker — e.g. `>>>Userantwort:` for a German user.)

  The user just places the cursor after the marker and speaks. An item whose answer line
  stays empty simply wasn't tested yet — that's information too, not an error.- **The user works in the handoff file with a plain text editor** (TextEdit or similar), not
  in the chat box: they answer each test point directly beneath it, and collect new ideas and
  findings in the same file — even across a long pause. Why an editor and not the terminal:
  chat inputs collapse long pastes into `[pasted text]`, so the user loses overview; in the
  editor they see the whole document. **Rule: save (⌘S) before telling Claude to read it** —
  unsaved editor changes are invisible on disk.
- **Next session starts with only the handoff** — fresh context (~20k instead of 500k+),
  fully briefed, cache rebuilt once at minimum size. Claude reads the annotated test answers
  and new ideas from the file and starts the next wave.

**Keep lines narrow.** Users often park the editor beside their terminal on a split
screen and bump the font size (⌘+) — long lines then wrap unpredictably or run off
screen. Hard-wrap prose at roughly **60–70 characters** per line; narrower is better.
The ONE exception: commands, paths and URLs stay on a single line however long, so a
triple-click copies them whole. After the first document, ask the user once whether
the width suits them (narrower? wider?) and remember the preference.

**Open the handoff for the user automatically.** Right after writing it, open the file in a
plain text editor so the user *sees* that the wave is done and the annotated test list is
ready — on macOS: `open -a TextEdit <file>` (always name the editor explicitly; the system
default for `.md` is often an IDE or preview app the user doesn't want). On Windows:
`notepad <file>`; on Linux: `xdg-open <file>`.

**Open as a tab, not a new window.** Users who live in this workflow accumulate many open
documents; each new floating window adds clutter. macOS controls this globally: offer once
to run `defaults write -g AppleWindowTabbingMode always` so new documents open as tabs in
the existing TextEdit window (reversible with `defaults delete -g AppleWindowTabbingMode`,
or per System Settings ▸ Desktop & Dock ▸ "Prefer tabs"). Mention that this is a
system-wide setting — if the user dislikes it, they say so and Claude reverts it.

Caveat: tabbing only joins windows on the SAME Space/desktop — if the user's main TextEdit
window lives on another Space, macOS opens a separate window anyway. Fallback after
opening: merge windows into tabs via the menu (needs Automation permission; try the
localized title first):

```bash
osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Alle Fenster zusammenführen" of menu "Fenster" of menu bar 1' \
|| osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Merge All Windows" of menu "Window" of menu bar 1'
```

If the user mentions that double-clicking `.md` files opens the wrong app, offer to fix the
default (macOS, via [duti](https://github.com/moretension/duti): `brew install duti && duti
-s com.apple.TextEdit .md all`) — many users have fought and lost this battle manually.

**Every user-facing document, not just handoffs.** Whenever Claude creates a document the
user is meant to read or react to (a plan, a report, a checklist, a draft), open it in the
text editor immediately — users rarely dig through folders for a path printed in the chat,
and an editor window is the visible signal "this is ready for you". Put a short header at
the top of each such document:

```
> You can comment directly in this file — start the line with >>> or with your
> name + timestamp, e.g. "J. Doe, 2026-08-22 14:40:".
```

(Write the header in the user's language.) The marker is a convention, not a syntax:
`>>>` is only the default. A name + timestamp prefix is even better — it says *who* answered *when*,
which matters once several annotation rounds pile up in one document. **Claude infers the
user's marker from the document itself**: whatever consistent prefix appears on the
answer lines is treated as the user's voice; don't force a format.

Tip Claude should offer once (macOS): the system has no built-in dynamic timestamp —
System Settings ▸ Keyboard ▸ Text Replacements can only insert static text. For a live
`name + date + time` snippet the user needs a text-expansion tool (any snippet app; if the
user dictates with a tool that supports snippets, that's the natural place for it).

When Claude later re-reads any of these documents, it treats the marked lines as the
user's comments/answers and runs the unsaved-changes guard below first.

**Unsaved-changes guard (macOS).** Claude reads files from disk, so unsaved editor changes
are invisible — but on macOS, Claude can check for them. Before reading an annotated
handoff, ask TextEdit whether the document is open with unsaved changes:

```bash
osascript -e 'tell application "TextEdit" to get {name, modified} of documents'
```

If the handoff shows `modified: true`, tell the user: *"Your handoff has unsaved changes —
shall I take them over?"* and on confirmation either save it for them
(`osascript -e 'tell application "TextEdit" to save (first document whose name is "<file>")'`)
or read the live window text directly
(`… to get text of (first document whose name is "<file>")`). Requires macOS automation
permission for TextEdit (one-time prompt). This turns the ⌘S rule from a hard requirement
into a safety net — but still teach ⌘S as the habit, since the guard only sees documents
that are open in TextEdit.

**Open documents LARGE — fix the font default, not the zoom.** Users bump every freshly
opened document with ⌘+ because TextEdit opens plain text tiny (default 11 pt) — and
TextEdit's per-window zoom is NOT scriptable, so Claude cannot read or restore it when
reopening a document. The durable lever is TextEdit's default plain-text font size:

```bash
defaults read com.apple.TextEdit NSFontSize          # unset = 11 pt
defaults write com.apple.TextEdit NSFontSize 18
defaults write com.apple.TextEdit NSFixedPitchFontSize 18
```

Offer this once (pick ~18 pt, adjust on feedback; reversible with `defaults delete`).
Documents opened AFTER the change come up large natively — no zooming. Already-open
windows keep their old size until the user quits and reopens TextEdit (never quit it
for them). This pairs with the narrow-line rule: big font + ~60–70-char lines is exactly
the split-screen setup the wave workflow assumes. When closing + reopening a document to
reload it from disk (TextEdit does not live-reload), warn the user once that per-window
zoom is lost — the font default is what makes that painless.

**Reload edited documents in the editor — every time, unprompted.** TextEdit does not
live-reload files changed on disk. Whenever Claude (or a subagent) edits a document the
user has open, run the unsaved-changes guard on exactly those files, then: unmodified →
close and reopen it so the user sees the new version; modified → do NOT close — tell the
user which of their unsaved edits collide, offer to merge them into the new version, and
only reload after they confirm. Skipping this leaves the user reading a stale document
while believing it is current — worse than any extra window shuffle.

**Tip for lost handoffs** (tell the user once): if they closed the document and can't find
the file, TextEdit ▸ **File ▸ Open Recent** brings back any
recently closed handoff without hunting through Finder.

**Carry the old test list forward.** When writing a NEW handoff while an older one exists:
read the old handoff first and check its answer lines. Answered items get incorporated —
and the new handoff says so explicitly per item ("Your T1 answer from the previous list is
taken into account: <one-line summary> — correct?"), so the user can veto a misreading.
Unanswered items and items whose fix needs a re-test move into the new list unchanged
(marked as carried over). The old handoff stays untouched as the record; only the newest
one is the active working document. **Close the old handoff's editor tab automatically**
when opening the new one (macOS: `osascript -e 'tell application "TextEdit" to close
(documents whose name is "<old file>")'`) — but ONLY if it has no unsaved changes and its
answers were incorporated; otherwise leave it open and tell the user why. A stale handoff
sitting next to the active one is how users end up answering the wrong document.

When Claude finishes a handoff it should say so and explain the loop to the user once:
*"Handoff written, your test list is at the bottom. Answer under the test points, add new
ideas, ⌘S — and give the file to a fresh session (or to me, if you're still in the window)."*

## The economics, honestly (teach this to the user once)

- Every request inside a warm cache re-reads the WHOLE prefix at ~1/10 price. At 220k
  context a short question costs ~22k full-price token equivalents; ten such exchanges
  ≈ one full context read. The user's instinct "batch my messages" is directionally right —
- — BUT the user's messages are a rounding error. Claude's own tool loop dominates:
  every file read, every command is a request that re-reads the prefix. A working day
  can be 500+ requests, of which the user sent ~20. The lever is therefore NOT fewer
  user messages; it is a SMALL context while the many work-steps run. (This is also why
  subagents pay off: the heavy lifting happens in their separate small contexts.)
- Concrete arithmetic for the sweetspot: a 300-step wave at 220k context ≈ 300 × 22k
  ≈ 6.6M equivalents; the same wave in a fresh ~30k session ≈ 0.9M. A fresh session's
  rebuild is cheap because the new prefix is small — the expensive thing is never the
  handoff, it is running a big wave on top of a fat context.
- Rule of thumb that follows: hand off BEFORE each big new wave once context has grown
  past ~150–250k — not at a fixed percentage, and not after every wave regardless of
  size. **Sweetspot: hand off around ~200k, hard ceiling well before 400k.** Below ~50k,
  short questions are near-free — chat freely; past ~150k, batch conversation too
  (one structured message per wave). Every message resets the 1-hour timer either way.

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
