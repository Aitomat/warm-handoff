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

## Die sparsamste Arbeitsweise in fünf Sätzen

For the user, in plain words (asked for on 30.08.2026, 15:06: *"was ist denn jetzt die
Moral der Geschichte?"*):

1. **Eine Session pro Welle** — plan, guardians, merge, handoff all in one; a fresh session
   costs its ~200k start build, so only start one past ~200k context.
2. **Sammeln kostet nichts** — collect test answers, ideas and critique in the handoff file
   for hours; that is zero requests, while every chat message costs a full context re-read.
3. **Wächter statt Pings** — one guardian per topic starts the workers, so the main session
   is woken 5–7 times instead of 15–20.
4. **Unter 200k Kontext bleiben** — the main session only plans, merges and reads reports;
   everything else lives in agents.
5. **Handoff mit Kostentabelle** schließt die Welle ab — measured numbers, not feelings.

**Vorsatz (30.08.2026):** measure EVERY session for the next few days — one logbook line
each (requests, equivalent, pings, wall clock, jobs) — so this skill gets perfected on
evidence, not on memory.

## The facts (Claude Code docs, 2026-08)

- Pro/Max: **1-hour sliding cache TTL** — every request resets it. Subagents: strict 5 min.
- Cache killers regardless of clock: mid-session `/model` or `/effort` change, editing
  CLAUDE.md/system prompt, MCP server restart. Set model + effort at session START.
- Prices relative to fresh input: **cache read ×0.1 · cache write ×2 (1-h TTL) · own output ×5.**
- Every request re-reads the whole prefix. Cost = requests × context. The user's messages
  are a rounding error; the agent's own tool steps and reports are the bill.

## Every reply — three honesty rules

1. **Timestamp at the very START of every reply**, from a `date` call in THAT reply
   (`date "+%d.%m.%Y %H:%M"`, piggybacked on any command). No `date` this turn → no timestamp.
   Never extrapolate, never `~19:40`. **This includes interim messages** — "guardian A is
   building, I'm waiting for both" is a full request, and only a timestamp at the front of it
   shows the user that a request just ran and kept the cache warm (user, 30.08.2026, 15:44).
   A reply whose first line is not a timestamp looks free, and nothing about it is free.
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

**What a subagent really costs.** A fresh subagent is NOT free: its first step pays its own
start context ×2 (cache write), and only every further step costs ×0.1. So a wave costs

```
main_ctx × 0.1 × own_steps  +  N agents × start_ctx × 2  +  N × start_ctx × 0.1 × agent_steps
                                └── the line that is usually forgotten ──┘
```

Worked example, 220k main context and 30k agent context: one step done in the main session
costs 220k × 0.1 = 22k; the same step inside an agent costs 30k × 0.1 = 3k, but the agent
first burns 30k × 2 = 60k once. Break-even: 60k ÷ (22k − 3k) ≈ **7 steps per agent**.
Below that, doing it yourself is cheaper; above that, delegating wins and keeps growing.
Both contexts are measured, not assumed — with a 120k main context the break-even moves to
60k ÷ (12k − 3k) ≈ 7 steps too, with a 400k one it drops to ≈ 2. Say the number, not "agents
are cheap".
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

- **The wave plan is a FILE, written before the guardians start** (user, 30.08.2026, 02:28:
  he wants to see the plan and be able to look it over). Before spawning anything, the main
  session writes `docs/reviews/<date>-welleN-plan.md`: first the structure rules that apply
  to every job (branch base, build lock, no questions, report contract, one squashed
  commit per job, push before "done"),
  then ONE TABLE PER TOPIC with the columns **ID · assignment · acceptance criterion ·
  model/effort**. It commits that file, opens it immediately (`open -a TextEdit <file>`),
  and only then starts ALL guardians in a SINGLE message, each brief pointing at the file
  („dein Thema ist Tabelle B in <pfad>") instead of repeating the plan. One file = one
  place the user reads, one place the guardians read, no drift between the two.
- **Dose the commits: one commit per job, ≤ 50 a day** (user, 30.08.2026, 15:05 — the day
  before had produced 158 contributions: *"das sollte man vielleicht doch nicht so
  übertreiben … eher fünfzig Contributions"*). Workers commit early and often on their own
  branch, but the guardian folds each worker branch into the topic branch with
  `git merge --squash` + ONE commit per job, so the contribution graph shows real units of
  work instead of every Kleinkram. Put this line in the plan file's structure rules too, so
  every guardian reads it. Rule of thumb: a commit a reviewer would want to read alone.
- **Push is part of the job.** Every guardian and every skill agent pushes its branch
  (`git push -u origin <branch>`) BEFORE it reports done — not after, not "the main session
  will". On 30.08.2026 02:36 the user looked at GitHub and saw nothing moving, because a
  skill agent had committed but not pushed. A branch that only exists locally is not
  delivered, and the report must name the pushed hash.
- **Guardian agent (Wächter).** For a build wave, ONE orchestrating agent (Opus, low/normal
  effort) gets the whole plan as a file, spawns the worker agents itself, merges, tests,
  bundles, cleans `.build` of merged worktrees, writes the report — the main session is
  woken ONCE instead of once per agent (8 → 1 notifications ≈ 140k saved at 190k ctx).
  Workers' questions land at the guardian, so briefs must be complete: paths, goal,
  limits, acceptance criteria, "no questions — decide, document the assumption".
- **One guardian PER TOPIC, not one per wave** (30.08.2026). A guardian watching 12 workers
  is a bottleneck and a crash risk; give each topic area (UI, audio, tests, docs …) its own
  Opus guardian with **4–6 workers at most**. Each topic guardian merges into its own
  integration branch. The main session merges the integration branches and then starts ONE
  **merge guardian** for the single full build, the full suite, the bundle and the QA pass.
  The main session is woken once per topic guardian, not once per worker.
- **How MANY guardians? Count the topics, not the workers** (user asked, 30.08.2026, 02:24:
  „drei Wächter, vier Wächter, zwei Wächter — was ist am sinnvollsten?"). The answer is
  mechanical: **one guardian per disjoint topic that carries 4–6 jobs of its own.** Below 4
  jobs a topic does not earn a guardian — the guardian pays `start_ctx × 2` just to exist
  (60k at a 30k start context), which only amortizes over several worker steps; fold such a
  topic into a neighbouring guardian or do it in the main session. Above 6 the guardian itself
  becomes the bottleneck: it merges, builds and tests serially, and the last workers wait.
  **Two guardians** are right only for two genuinely separate areas — with more topics they
  serialize what could have run side by side (wave 23: one guardian, cheapest in tokens,
  slowest on the clock at 2 h 20). **Four or more** are fine when there really are four
  independent areas, and wasteful when the fourth is a slice of the third — wave 24 put 12
  workers under one guardian and paid for it with 12 completion pings and a crash. Wave 25's
  three topic guardians + one merge guardian over 15 workers (5 per guardian) is the measured
  optimum so far: 29 requests, 1.192k, 64 minutes. So: three is usually right because three
  disjoint areas of 4–6 jobs is what a wave usually has — but derive the number from the plan,
  never pick it as a habit.
- **Build lock — never more than one build per machine.** Before any build:
  `mkdir /tmp/<project>-build.lock` (fails if it exists → wait or skip; `rmdir` when done).
  `mkdir` is atomic, so it works across agents and worktrees. This is the mechanical guard
  behind "workers do not build" after the 29.08. crash.
- **The guardian starts every worker at once, in a single message** (one batch of Agent
  calls), never one after another — a serial tail of workers is what turns a cheap wave
  into a long one. Each worker's FIRST step is to pull the current branch tip (`git pull`
  / `git fetch && git rebase`) before touching any file, so it never builds on a stale base.
- **Workers do NOT build or test.** They write code + tests, at most `swiftc -parse`, and
  commit early. Only the guardian builds — ONCE, serially, in the main repo — and runs the
  suite. 12 workers × one cold build each = 400+ compiler processes, load 70, 18 GB RAM
  swapped to a halt, forced reboot, 90 minutes lost (29.08.2026). If workers must build,
  never more than 4 at once; `memory_pressure` before the full suite.
- **Cut agents to 15–25 minutes, ONE task each** (30.08.2026 — was ~30 min, was 40 min /
  2–3 tasks; a single focused job lands faster and is easier to merge, and a shorter brief
  is what keeps a topic guardian's 4–6 workers landing together). Longer work delivers into a FILE
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
- **Model + effort in the visible label — for guardians AND for their workers**
  (user, 30.08.2026, 02:31). The label pattern is `Modell/Effort · ID Kurzname`, e.g.
  `Fable/low · A1 Aufnahme-Rot`, `Opus5/high · Verlauf-Tempo`. A guardian must label the
  workers it spawns the same way, because the user reads the running-agent list at the
  bottom of the screen and wants to see model and effort there without asking. Exception to
  state openly: **Codex runs as a shell command, not as an agent — it never appears in that
  list**; say so instead of letting the user hunt for it.
  Fable 5 as subagent: **always effort low**, and **only for jobs the user marked "wichtig"
  / important** — those are worth the faster model. Everything else: Opus (low). **Sonnet only
  for trivia that does not build** (renames, moving text, listing files); never for a build
  job. For hard review/design use Opus or a second architecture (Codex/GPT). Never review
  your own output yourself — route to Codex.
- **Agents test before the user.** Full suite + a QA agent that launches the app and clicks
  every test item once; the user should mostly say "works, thanks". **The QA agent closes
  the windows/processes it opened for testing** before it reports done — the user shouldn't
  inherit a pile of leftover test instances.
- Report contract: ≤ 300 words, status/decisions/evidence-with-paths/risks/next; no
  chronicle, no pasted logs. Subagent tokens still hit the weekly quota — what they save is
  the MAIN context (each step ≈ 1/5 the cost, and nothing of it stays in the session).
- Pacing — **the parallel rule wins inside a wave** (resolves the old contradiction): a
  guardian ALWAYS starts its workers in parallel, in one message, whether the user is there
  or not. The "user away → sequential" pacing applies only to NON-guardian work the main
  session does on its own (small edits, reviews, checks): spread those out so each completion
  keeps the cache warm instead of burning them in one burst and then idling. Never invent
  busywork.

## Evidence — measured waves (Aitomat, 29./30.08.2026)

| Wave | Structure | Requests | Equivalent | Completion pings | Wall clock |
|---|---|---|---|---|---|
| 22 | 6 workers + merge agent, main session orchestrates | 58 | 2.075k | 8 | ~2 h |
| 23 | 1 guardian, few large agents | 43 | 1.531k | 1 | 2 h 20 |
| 24 | 1 guardian, 12 workers, all building | 62 | 3.143k | 1 + 12 | 2 h 10 |
| 25 | 3 topic guardians + merge guardian, 15 workers | 29 | 1.192k | 5 | 64 min |
| 26 | 3 topic guardians + merge guardian + skill agent, 17 jobs | 34 | 1.159k | 5 | 53 min |
| 27 | 4 topic guardians + merge + skill agent, Codex QM each, 19 jobs | 41 | 1.160k | 7 | 78 min |
| 28 | 2 topic guardians **cut along FILES** + merge + skill agent, 11 jobs + skill | 33 | 1.080k | 5 | 57 min |

Full derivation, per-job normalisation and the percentages: **[`docs/evidenz.md`](docs/evidenz.md)**
(German). Short version: against wave 22 — the same app, the same user, no guardian
structure — the measured saving is **43–50 % of requests and 43–48 % of the main-context
equivalent**; normalised per job (wave 22 did 7 jobs, waves 25–28 did 15–19) it is
**73–79 %**. That is where "saves up to 70 %" comes from, and it is the conservative reading.

Reading it: wave 23 was the cheapest in tokens of the structures known AT THAT TIME (one
guardian = one wake-up; waves 25–28 later beat it) but the slowest
in wall clock — tokens and waiting time are two different axes. Wave 24 looks worst on every
number, but 90 of its 130 minutes and roughly 2.400k of its equivalent are the machine crash
(12 parallel cold builds); **without the crash it was ≈ 40 minutes and ≈ 700k** — the fastest
wave so far. That is what the build lock and the 4–6-workers-per-guardian rule protect.
**Wave 25 (00:46–01:50, 30.08.2026, no crash) resolves that trade-off: the topic-guardian
structure was the cheapest AND the fastest so far** — fewest requests (29 for 15 build jobs),
lowest equivalent of any completed wave, and 64 minutes wall clock against 2 h+ for every
earlier structure. The topic guardians start their workers in parallel, and the merge guardian
collapses the serial tail into a single build; that is where both axes win at once.
**Wave 26 (02:24–03:17, 30.08.2026) is the control measurement** and it confirms wave 25:
the same structure — 3 topic guardians + merge guardian, plus a skill agent — carried 17
jobs in 34 requests, 1.159k equivalent, 5 completion pings and 53 minutes. Two waves in a
row at ~1.2M and under an hour, one of them with two jobs more than the other, is a
structure that repeats, not a lucky run.
**Wave 27 (03:39–04:57, 30.08.2026) shows the ceiling:** a FOURTH topic guardian cost the
same tokens as three (41 requests, 1.160k) but added 25 minutes — guardian B alone ran
45 min, and the merge guardian had to resolve conflicts for the first time, because two
topics (HUD crash and HUD recording indicator) touched the SAME files.
**Cut topics along files, not along words.** Anything editing the same files belongs to ONE
guardian, however differently the two jobs are named.
**Wave 28 (15:12–16:09, 30.08.2026) is the proof of that rule:** two guardians cut strictly
along files carried 11 jobs plus the skill wave in 33 requests, 1.080k, 5 pings, 57 minutes —
the cheapest equivalent measured so far, and **zero merge conflicts**. Fewer, file-disjoint
guardians beat more, topic-disjoint ones.

## Lessons (measured)

Only what the log actually shows — no extrapolation:

- **Topic guardians roughly halve requests and wall clock** against one guardian with 12
  workers: 62 requests / 2 h 10 (W24) → 29 / 64 min (W25) → 34 / 53 min (W26).
- **The start-up cache build (≈ 200k, once) is the single largest item of a short session.**
  That is why continuing in the SAME session beats a fresh one as long as context < 200k.
- **Context stayed at ~114k across a whole wave**, because all the work lived in agents —
  the main session only planned, merged and read reports.
- **Completion pings are the main session's cost driver:** 5 instead of 13 is the difference
  between wave 25/26 and wave 24, and it is worth more than any wording trick.
- **The Codex quality-manager pass finds real P1s** — 4 of them in three Fable jobs (W26-A7).
- **A fourth guardian buys nothing** (W27: 41 / 1.160k / 78 min against 34 / 1.159k / 53 min
  for three) — the extra topic overlapped in files and produced the first merge conflicts.
- **Every guardian needs its OWN worktree** (W28). Guardians A and B shared the main repo and
  switched each other's branch out from under their feet mid-wave. Rule:
  `git worktree add ~/Code/<projekt>-w<N>-<topic> -b w<N>-<topic> <base>`, workers branch from
  the guardian's integration branch into their own worktrees, and **nobody ever switches the
  branch in the main repo**. Clean up merged worktrees' `.build` afterwards.
- **Wait AT the build lock, actively — never stop and report.** In W28 guardian A halted while
  waiting for `/tmp/<app>-build.lock` and had to be nudged: that is one avoidable request plus
  idle minutes. The loop is
  `while ! mkdir /tmp/<app>-build.lock 2>/dev/null; do sleep 30; done` … `rmdir` after, and
  "the lock is busy" is never a reason to send a message.
- **One logbook line per session, always** (`~/.claude/warm-handoff-log.md`): date, context,
  what the wave was, rebuilds, requests, equivalent, waste, handoff path. It costs nothing —
  it rides along on a command that runs anyway — and it is the only reason the evidence table
  above exists at all. A wave without its logbook line is a wave that cannot be compared.
- **Stray worker messages are normal, not a fault.** A worker whose guardian has already
  finished reports into the main session instead (1× in W27). Read it, note it, do not
  restart the work — the guardian's merge already contains it.
- **An API abort is resumable.** If an agent dies mid-job (API error, host restart), do NOT
  spawn a fresh one: send `SendMessage` to the SAME agent id/name — it keeps its context and
  carries on. Only start over if it never produced anything.
- **When the user says "Absturz" (crash), look at the crash reports first**, in the same call
  as everything else: `ls -t ~/Library/Logs/DiagnosticReports/<App>-*.ips | head`, then read
  the topmost stack. In W27 six `.ips` files all named the same line, which turned a vague
  report into a one-line fix. This belongs to the session-start look, not to a later step.
- **A pause > 60 min costs a rebuild (≈ context × 2)** — at 114k that is ≈ 230k, still less
  than a fresh session that pays its ~200k start build plus re-briefing.

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
- **Codex as quality manager of the wave** (user, 30.08.2026, 03:05). Whenever the Codex
  quota is fresh, EVERY topic guardian has its integration branch reviewed by Codex before
  it writes its closing report, and fixes the P1 findings itself — the wave ends reviewed,
  not "reviewed later". Command shape: `git diff <base>..HEAD | codex exec
  --skip-git-repo-check "Review this. Find bugs, risks, missing tests."` Evidence that this
  is not ceremony: in wave 26, job A7 let Codex look at three Fable assignments and it
  found **4 P1 issues** that the building agents had not seen. Costs one Codex call per
  guardian and zero main-session requests.

## The wave workflow and the handoff file

Write the handoff after every big wave, unprompted. Path `<project>/_handoff-<projekt>-YYYY-MM-DD[-b].md`
(project name in the file name AND title). Hard-wrap prose at ~60–70 chars; commands,
paths, URLs on one line. Reference, don't copy (paths/URLs); redact secrets; name skills
for the next session. This skill is written in English, but everything in **bold German**
below is literal output text for a German-speaking user — write those headings and banners
into the handoff file exactly as they stand, do not translate them. Glossary for the recurring
German terms: *Handoff* = the handover document, *Welle* = wave, *Wächter* = guardian agent,
*Sammlung* = the user's free-form collection area, *Testliste* = test list, *Der rote Faden*
= the through-line / next waves, *Hauptdokumente* = key documents, *Gedächtnis* = memory,
*Kostentabelle* = cost table. Structure, top to bottom:

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
   Then, MANDATORY, directly after Hauptdokumente and before the Kostentabelle, the memory
   block — the project's own memory file, inside the handoff (user, 30.08.2026: he wants to
   switch Claude's own memory file off and carry the memory in the handoff instead). Heading
   `## Gedächtnis`, two labelled lists of **4–6 lines each**, short and concrete:
   ```
   **Langzeit (gilt immer):**   → north star, working rules, model policy, house
                                   rules that survive every wave
   **Kurzzeit (diese Wochen):** → branch + tip + test count, what is open,
                                   machine/disk state, current test items
   ```
   Template to copy the shape from: `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-30-e.md`,
   section `## Gedächtnis`. Carry the long-term list forward verbatim from the previous
   handoff unless something actually changed; rewrite the short-term list every time.
   **„Dreaming" — the memory is refreshed while the handoff is written** (user, 30.08.2026,
   15:05): reread the previous handoff's `## Gedächtnis` and fold this session's durable
   findings into it — new long-term rules up, stale short-term lines out. This is a STEP of
   writing the handoff, never a separate agent and never an extra request; the file is open
   in front of you anyway, so it costs nothing. One memory per project, living in that
   project's handoff, visible and editable by the user (he may change or delete lines, and
   `>>>` works here like everywhere else). **Claude's own memory file is no longer filled** —
   the handoff's `## Gedächtnis` replaces it, so there is one place, not two.
   Example to copy the shape from: `/Users/pro16/Code/aitomat/_handoff-aitomat-2026-08-30-g.md`,
   section `## Gedächtnis`.
8. **Kostentabelle** via `~/.claude/session-costs.sh --markdown` (unit = span between two
   user messages; explain k = thousand, context column ≠ cost) + honest findings, then the
   closing line with MEASURED context and start context: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** with `aus: /abs/path` and an empty `>>>`.
   The user collects here while the next wave runs — collecting costs zero requests.

Questions for the user go into the handoff (`## Fragen an dich` with `>>>Antwort:`),
not the chat: one chat question blocks a wave, ten in the file block nothing. Cut waves
so they run through without asking; take the likelier reading and document it.
**Escalation exception — ask in the chat, immediately, before acting**, when the ambiguity
touches: irreversible or destructive actions (`rm`, history rewrite, force-push, dropping
data), anything security- or credential-related, anything externally visible (sending mail,
publishing, deploying, changing a live shop), spending real money or a large quota, or
sending repository content to an external model. Everything else goes in the handoff.

## Editor rules (macOS / TextEdit)

**Open EVERY new user-facing document the moment it exists: `open -a TextEdit <file>`.** Not
only the handoff — a plan, a QA report, a review file, a test list: if it is meant for the
user to read, it gets opened in the same turn it is written. No exceptions, no "tell me if
you want me to open it".

- Offer once:
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
`scripts/session-costs.sh` (identical German alias `session-kosten.sh` in the repo; the installer copies `session-costs.sh` — use that name everywhere), `scripts/codex-limit.sh` → copy to `~/.claude/`.
Terminal-neutral: say "your status line", not a specific host's field.
