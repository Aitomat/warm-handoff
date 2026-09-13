# Handoff Format

<!-- rule:HF-01 -->
## New revision, clear entry point

Create a new dated file for every handoff. Never overwrite an answered source. Put a copyable first line with the absolute path of the new file. Include project, date, and revision in the title.

**Read only the saved state.** Saving is the user's release; text left unsaved in
an editor has not been read. Ask for the save, or mark the gap explicitly as a
gap — never save, close, or recreate the user's answer file in order to read it.

**Keep exactly one active collection inbox**, the single place where the user
answers and interjects: either the answer file's collection section or the agreed
interjections file. The other location only links to it. Two parallel inboxes lose
answers.

<!-- rule:HF-02 -->
## Required sections

1. **Preserved user input:** the complete verbatim collection from the previous revision, without interpretation.
2. **Objective and authorization:** desired outcome, allowed and prohibited actions, and file ownership.
3. **Verified state:** branch or HEAD, changed files, passing checks, and evidence paths.
4. **Running and pending:** started work, dependencies, unknown state, and real blockers.
5. **Decisions and questions:** only points requiring user choice; put `>>>User answer:` and one blank gold answer paragraph under each question.
6. **Acceptance:** short reproducible steps, expected result, and manual checks that remain unverified.
7. **Memory:** a few durable rules and session-specific next steps, kept separate.
8. **Collection for the next handoff:** a distinct verbatim user area at the end.

<!-- rule:HF-03 -->
## Separate originals from interpretation

Use `<!-- user-original:start -->` and `<!-- user-original:end -->` when the renderer must protect a verbatim block. Change neither spelling nor order inside it. Put agent replies, decisions, and summaries outside. A byte archive may additionally preserve the unchanged source; the readable snapshot does not replace it.

<!-- rule:HF-04 -->
## Completion requires evidence

Call work complete only when an artifact, commit, status, or test proves the result. “Started,” file existence, and agent reports are not final evidence. For an open manual check, name the exact remaining step.

Archive answered handoffs in `handoff-archiv/` of the same project, created if missing, and move them with `mv`, never `rm` (user 2026-09-13 03:31). A new handoff is always a NEW file; archive the old one only after its answers have been carried over.

See also [wave execution](wave-execution.md), [evidence scope](evidence-scope.md), and [RTF on macOS](rtf-macos.md).
