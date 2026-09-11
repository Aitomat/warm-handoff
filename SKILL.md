---
name: warm-handoff
description: Preserve user input and verified work across pauses, resume safely, and execute explicitly authorized work waves with provider-neutral evidence and file ownership.
---

# Warm Handoff

Use this compact entry point for routine work. Read only the reference needed for the current action. Use the separately installed `warm-handoff-full` variant when teaching, adopting, or auditing the entire workflow.

<!-- rule:WH-01 -->
## 1. Establish scope

Treat the user's latest saved handoff and later messages as one ordered input stream. Read project instructions first, identify the named source and feedback files, and record the authorized scope, prohibited actions, file ownership, and required evidence. A handoff records intent; it does not grant permissions that the user did not give.

Select one host adapter: [Codex](references/codex.md) or [Claude Code](references/claude-code.md). Keep the core rules provider-neutral.

<!-- rule:WH-02 -->
## 2. Resume without loss

Read the complete saved source, including embedded or appended user text. Preserve user originals verbatim and put interpretations or answers in separate sections. Compare late additions before acting. Verify repository state and completed claims from files, Git state, tests, or other direct evidence; label anything else unknown.

For the document contract and required sections, read [handoff format](references/handoff-format.md).

<!-- rule:WH-03 -->
## 3. Work inside authorization

Make progress until the authorized outcome is complete. Split independent work only when the host and assignment allow it. Give each worker exclusive paths and acceptance criteria; never exceed actual concurrency. Guardians are optional coordination roles, not a default layer. Keep builds and shared resources serialized.

For execution details, read [wave execution](references/wave-execution.md). For model selection and changing platform facts, read [model routing](references/model-routing.md) and [evidence scope](references/evidence-scope.md).

<!-- rule:WH-04 -->
## 4. Preserve document safety

Never overwrite a user's answered handoff. Write a new Markdown source and, when requested on macOS, a new editable RTF twin. Verify plain-text roundtrip and link fields before publishing. Renderer verification does not prove TextEdit continuation behavior or application paste behavior; test those separately.

Read [RTF on macOS](references/rtf-macos.md) before rendering or opening documents.

<!-- rule:WH-05 -->
## 5. Use optional helpers deliberately

[Context Mode](references/context-mode.md) can reduce large command and file output. Treat package installation, MCP availability, and hook operation as separate states. Never install it without permission.

<!-- rule:WH-06 -->
## 6. Close with evidence

Before completion, reread the designated feedback source, inspect status, run the required targeted checks, and confirm only owned paths changed. Report completed, pending, and running work with evidence and the next action. Write the requested durable report before returning a short chat response.

Spanish localization is deferred. Audio, video, and website material are outside this skill.
