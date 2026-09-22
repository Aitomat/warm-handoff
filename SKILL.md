---
name: warm-handoff
description: Preserve user input and verified work across pauses, resume safely, and execute explicitly authorized work waves with provider-neutral evidence and file ownership.
---

# Warm Handoff

Use this compact entry point for routine work. Read only the reference needed for the current action. The `warm-handoff-full` variant covers teaching, adoption, and audits.

<!-- rule:WH-01 -->
## 1. Establish scope

Treat the user's latest saved handoff and later messages as one ordered input stream. Read project instructions first, identify the named source and feedback files, and record the authorized scope, prohibited actions, file ownership, and required evidence. A handoff records intent; it grants no permission the user did not give.

Select one host adapter: [Codex](references/codex.md) or [Claude Code](references/claude-code.md). Keep the core rules provider-neutral.

<!-- rule:WH-02 -->
## 2. Resume without loss

Read the complete saved source, including embedded or appended user text. Preserve user originals verbatim and put interpretations or answers in separate sections. Compare late additions before acting. Verify repository state and completed claims from files, Git state, tests, or other direct evidence; label anything else unknown.

Three stop rules when you write a handoff:

1. **Open the reference first.** Read [handoff format](references/handoff-format.md) in full; it holds the document contract and the mandatory section order. "I know the format" does not count.
2. **Read the predecessor unfiltered,** first line to last. Never truncate, never grep only for answer markers, never filter to save tokens — that is how the through-line, roadmap, measurement, memory, and logbook get lost.
3. **Do not wait, close out.** Do not hold a wave open for one more agent report; outstanding reports go under "Running and pending".

<!-- rule:WH-03 -->
## 3. Work inside authorization

Make progress until the authorized outcome is complete. Split independent work only when the host and assignment allow it. Give each worker exclusive paths, acceptance criteria, and explicit file boundaries; never exceed actual concurrency. Guardians are optional coordination roles, not a default layer. Keep shared resources serialized.

Builds are the scarce resource, and the limit is memory, not agent count: **one build at a time**, with the lock in the project's test script, not in a worker prompt — a prompt is a request, a script is a gate. A final build counts only when it reached the tests; a run that dies earlier must be repeated, and whoever changes anything afterwards builds again. Keep builds in the foreground, cap how many workers run at once, and smoke-build once before the first worker starts.

For pre-flight checklists, the lock snippet, worker briefs, and wave choreography, read [wave execution](references/wave-execution.md). For model selection and changing platform facts, read [model routing](references/model-routing.md) and [evidence scope](references/evidence-scope.md).

<!-- rule:WH-04 -->
## 4. Preserve document safety

Never overwrite a user's answered handoff. Write a new Markdown source and, on macOS when requested, a new editable RTF twin. Verify plain-text roundtrip and link fields before publishing. Renderer verification proves neither editor continuation nor application paste behavior; test those separately.

Text pasted or typed behind `>>>` must stay black on gold at 18 pt; the exact control words are in [RTF on macOS](references/rtf-macos.md). Create a new handoff directly in the project's archive folder and never move it afterwards — every move breaks a path the document was already linked under; archive answered handoffs with `mv`, never `rm`. Every document begins with its own absolute path as the first line, then its as-of date. When you change a document the user may have open, close and reopen it for him, but never touch unsaved input.

Keep exactly one inbox at a time, switched by the wave clock: between handoff and wave start the handoff is the only inbox; the interjections file is created at wave start and is the only inbox until the next handoff. Answer short items at once; schedule longer ones into the next wave.

Read [RTF on macOS](references/rtf-macos.md) before rendering or opening documents. Generate handoff and interjection twins exclusively through `scripts/handoff-rtf.sh` from the skill directory. Cmd-S releases saved input within the existing authorization.

<!-- rule:WH-05 -->
## 5. Use optional helpers deliberately

[Context Mode](references/context-mode.md) can reduce large command and file output. Treat installation, MCP availability, and hooks as separate states. Never install it without permission.

<!-- rule:WH-06 -->
## 6. Close with evidence

Before completion, reread the designated feedback source, inspect status, run the required targeted checks, and confirm only owned paths changed. Report completed, pending, and running work with evidence and the next action. Write the durable report before the short chat response. Take every timestamp from the system clock, never from an estimate.

On every wake-up of the main session — a worker notification, a timer, a resumed turn — compare the modification time of the designated interjections file against the last read. Changed: read the saved additions before acting or reporting. Unchanged: leave it closed. Saved state only; the user's save is the release. Never watch the file: a save is not a request and must wake nothing.

Finish a clean wave without asking: all workers done and the full suite green means build, install, publish, and write the handoff. Ask only on an unclean finish — red tests, an unresolved finding, a blocked worker — and then name what is missing and propose a next step.

Spanish localization is deferred. Audio, video, and website material are outside this skill.
