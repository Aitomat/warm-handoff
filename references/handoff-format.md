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

<!-- rule:HF-05 -->
## Read it completely, never filtered (2026-09-14)

Read the previous handoff unfiltered, first line to last, before writing the new one. Never truncate long lines, never grep only for `>>>User answer:`, never filter "to save tokens" — that is exactly how the through-line, roadmap, measurement, main documents, memory, and logbook disappear from the successor revision. Read oversized files in blocks, but completely. And at the end of a wave, do not wait for one more agent report; outstanding reports belong under "Running and pending" and do not hold up completion.

<!-- rule:HF-06 -->
## Full section order (mandatory, 2026-09-14)

The eight required sections above are the minimum. The shipped order is:

1. Copyable absolute path — 2. Editing note and `>>>I edited the handoff:` — 3. The state in three sentences — 4. Objective and authorization — 5. Verified state — 6. Running and pending — 7. The user's collection, verbatim, separated by source — 8. What I made of it — 9. Decisions and questions with `>>>User answer:` — 10. Test list with `>>>User answer:` per item — 11. The through-line — 12. Short roadmap — 13. Measurement of the wave — 14. Main documents and further documents — 15. Memory (durable/session) — 16. Logbook — 17. `COLLECTION FOR THE NEXT HANDOFF`.

A missing section means the handoff is not finished. Check the list against the file before rendering.


<!-- rule:HF-07 -->
## Answer inside the Zwischenrufe file (2026-09-14)

The Zwischenrufe file is a conversation, not a letterbox. Once you have read and
acted on saved interjections, write your answer into that same file — not only
into the chat:

1. Below the answered interjections add a block
   `ZWISCHENRUFE BIS HIER BEARBEITET — <time>` with your answers: one sentence
   per point saying what became of it (done, scheduled as topic X, declined with
   a reason).
2. Below that the marker `AB HIER NEUE ZWISCHENRUFE` and one empty `>>>` line.
3. Only then report in chat. The user sees at a glance what arrived, without
   searching the chat history.

The user must never write anything twice. If they had to paste interjections
into the chat because you missed them, that belongs in the wave's measurement as
a failure.

See also [wave execution](wave-execution.md), [evidence scope](evidence-scope.md), and [RTF on macOS](rtf-macos.md).
