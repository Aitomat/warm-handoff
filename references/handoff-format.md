# Handoff Format

<!-- rule:HF-01 -->
## New revision, clear entry point

Create a new dated file for every handoff. Never overwrite an answered source. Put a copyable first line with the absolute path of the new file. Include project, date, and revision in the title.

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

See also [wave execution](wave-execution.md), [evidence scope](evidence-scope.md), and [RTF on macOS](rtf-macos.md).
