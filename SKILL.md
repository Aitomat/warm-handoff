---
name: warm-handoff
description: Handoff, Welle (work wave), Zwischenrufe (interjections) and safe resume. Use at session start, when the user says "Handoff", "Welle", "Zwischenrufe", "weiter", "Sessionstart", hands over a saved handoff (.md/.rtf), or before a pause; preserves user input verbatim, executes explicitly authorized work waves with file ownership and provider-neutral evidence, and writes the next handoff.
---

# Warm Handoff

Compact entry: read only the reference the current step needs; use the separately installed `warm-handoff-full` for teaching or audits.

## Standing rules (every turn, not once)

1. The first reply to every new user message starts with `Name, DD.MM.YYYY-HH:MM` from `date "+%d.%m.%Y-%H:%M"` — never estimated, also after interjections (HF-09); a `UserPromptSubmit` hook may supply it.
2. Read only saved state; Cmd-S releases saved input within existing authorization. Never touch unsaved editor input.
3. Never overwrite an answered handoff; never `rm` — archive with `mv`.
4. Every document starts with its own absolute path as the first line, then its as-of date.
5. A handoff records intent; it grants no permission the user did not give.

<!-- rule:WH-01 -->
## 1. Establish scope

Read `AGENTS.md` (the one file for all agents) first; treat the latest saved handoff and later messages as one ordered input stream. Identify named source and feedback files; record authorized scope, prohibited actions, file ownership, and required evidence. Select one host adapter: [Codex](references/codex.md) or [Claude Code](references/claude-code.md); keep the core rules provider-neutral.

<!-- rule:WH-02 -->
## 2. Resume without loss

Read the complete saved source, including embedded user text. Keep user originals verbatim; answers go in separate sections. Compare late additions before acting. Verify claims from files, Git, tests, or other direct evidence; label the rest unknown.

Three stop rules when you write a handoff:

1. **Open the reference first.** Read [handoff format](references/handoff-format.md) in full (document contract, mandatory section order). "I know the format" does not count.
2. **Read the predecessor unfiltered,** first line to last. Never truncate, grep only for answer markers, or filter to save tokens.
3. **Do not wait, close out.** Never hold a wave open for one more agent report; outstanding reports go under "Running and pending".

<!-- rule:WH-03 -->
## 3. Work inside authorization

Worker briefs keep user rules binding; a lead never silently disables them. Record conflicts with host permissions. One project-wide wave number sequence across hosts; reserve the next free number in the saved plan (WV-01).

Continue until the authorized outcome is complete; split work only when host and assignment allow. During a wave, answer new user questions you can answer at once (chat plus interjections file), file late interjections as addendum or follow-up, and keep one slot as a small-task lane (WV-13). Give each worker exclusive paths and acceptance criteria; never exceed actual concurrency. Guardians are optional, not a default layer. Serialize shared resources.

One build at a time, locked by the project test script, in the foreground; smoke-build before the first worker. A final build counts only after reaching tests; rerun after later changes.

Checklists, lock snippet, briefs: [wave execution](references/wave-execution.md). Models and platform facts: [model routing](references/model-routing.md), [evidence scope](references/evidence-scope.md).

<!-- rule:WH-04 -->
## 4. Preserve document safety

Write a new Markdown source and, on macOS when requested, a new editable RTF twin — exclusively via `scripts/handoff-rtf.sh` from the skill directory; read [RTF on macOS](references/rtf-macos.md) before rendering or opening documents. Verify plain-text roundtrip and link fields. Text behind `>>>` stays black on gold at 18 pt.

Create a new handoff directly in the project's archive folder and never move it — a move breaks paths it was linked under. RTFs stay there for good (HF-10). After changing a document the user may have open, close and reopen it — only if no unsaved input.

Until wave start the handoff footer is the only inbox. At wave start, create the interjections file as `.md` in the project root and open it in an editor the user can type into (on macOS: `open -a TextEdit "<full path>"`, never a read-only viewer such as a cmux markdown tab), never as an RTF inbox; it stays the only inbox until the next handoff. Append replies there with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append. Follow HF-07.

<!-- rule:WH-05 -->
## 5. Use optional helpers deliberately

[Context Mode](references/context-mode.md) can reduce large command and file output. Never install it without permission.

<!-- rule:WH-06 -->
## 6. Close with evidence

Before completion, reread the feedback source, inspect status, run the required targeted checks, and confirm only owned paths changed. Report done, pending, and running work with evidence and the next action. Write the durable report before the short chat response; take every timestamp from `date`.

On every main-session wake-up (worker notification, timer, resumed turn) compare the interjections file's mtime with the last read: changed — read the saved additions before acting; unchanged — leave it closed. Never watch the file: a save is not a request and must wake nothing.

Clean wave (workers done, full suite green): build, install, publish, write the handoff — no question. Red tests, unresolved findings, or blocked workers: name the gap and propose the next step.
