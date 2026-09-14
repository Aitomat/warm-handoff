---
name: warm-handoff
description: Preserve user input and verified work across pauses, resume safely, and execute explicitly authorized work waves with provider-neutral evidence and file ownership.
---

# Warm Handoff

Use this compact entry point for routine work. Read only the reference needed for the current action. The `warm-handoff-full` variant covers teaching, adoption, and audits.

<!-- rule:WH-01 -->
## 1. Establish scope

Treat the user's latest saved handoff and later messages as one ordered input stream. Read project instructions first, identify the named source and feedback files, and record the authorized scope, prohibited actions, file ownership, and required evidence. A handoff records intent; it does not grant permissions that the user did not give.

Select one host adapter: [Codex](references/codex.md) or [Claude Code](references/claude-code.md). Keep the core rules provider-neutral.

<!-- rule:WH-02 -->
## 2. Resume without loss

Read the complete saved source, including embedded or appended user text. Preserve user originals verbatim and put interpretations or answers in separate sections. Compare late additions before acting. Verify repository state and completed claims from files, Git state, tests, or other direct evidence; label anything else unknown.

For the document contract and required sections, read [handoff format](references/handoff-format.md).

### Writing a handoff: three stop rules (2026-09-14)

1. **Open the reference first.** Read `references/handoff-format.md` in full before writing — it holds the mandatory 17-part section order (HF-06). "I know the format" does not count.
2. **Read the predecessor unfiltered.** First line to last. Never truncate lines, never grep only for `>>>User answer:`, never filter "to save tokens" — that is how the through-line, roadmap, measurement, memory, and logbook get lost.
3. **Do not wait, close out.** At the end of a wave do not wait for one more agent report; outstanding reports go under "Running and pending".


<!-- rule:WH-03 -->
## 3. Work inside authorization

Make progress until the authorized outcome is complete. Split independent work only when the host and assignment allow it. Give each worker exclusive paths and acceptance criteria; never exceed actual concurrency. Guardians are optional coordination roles, not a default layer. Keep shared resources serialized and builds limited to the two slots of rule 4 v2.

### Rule 4 v2 — at most TWO builds at a time (2026-09-13)

Each topic guardian builds ONCE at the end of its topic with targeted tests; the
full suite belongs to the merge guardian. Two slot locks, largest topic first,
wait in the foreground, workers do not build. Details and the slot-lock snippet
are in [wave execution](references/wave-execution.md).

For execution details, read [wave execution](references/wave-execution.md). For model selection and changing platform facts, read [model routing](references/model-routing.md) and [evidence scope](references/evidence-scope.md).

<!-- rule:WH-04 -->
## 4. Preserve document safety

Never overwrite a user's answered handoff. Write a new Markdown source and, when requested on macOS, a new editable RTF twin. Verify plain-text roundtrip and link fields before publishing. Renderer verification does not prove TextEdit continuation behavior or application paste behavior; test those separately.

Text pasted or typed behind `>>>` must stay black on gold at 18 pt (`\fs36`); the exact control words are in [RTF on macOS](references/rtf-macos.md) (evidence W58-E1, 2026-09-13). Archive answered handoffs in `handoff-archiv/` of the same project (`mv`, never `rm`; user 2026-09-13 03:31).

### One inbox at a time, switched by the wave clock (2026-09-14)

Between handoff and wave start the handoff is the only inbox (`COLLECTION FOR THE NEXT HANDOFF` plus the `>>>User answer:` lines); the Zwischenrufe file does **not** exist then and is never created together with the handoff (user 2026-09-14). Only at wave start do you create it, open it in TextEdit, and it stays the only inbox until the next handoff. The same gold rule applies to every user line there. Answer short items at once; schedule longer ones into the next wave with a note.

Read [RTF on macOS](references/rtf-macos.md) before rendering or opening documents.

<!-- rule:WH-05 -->
## 5. Use optional helpers deliberately

[Context Mode](references/context-mode.md) can reduce large command and file output. Treat installation, MCP availability, and hooks as separate states. Never install it without permission.

<!-- rule:WH-06 -->
## 6. Close with evidence

Before completion, reread the designated feedback source, inspect status, run the required targeted checks, and confirm only owned paths changed. Report completed, pending, and running work with evidence and the next action. Write the requested durable report before returning a short chat response.

### Check the interjections file on every wake-up (2026-09-13)

The user's rule of 2026-09-13 (05:17): every time the main session wakes up — a worker or guardian notification, a timer, a resumed turn — compare the modification time of the designated interjections file with the time of the last read. Changed: read the saved additions before acting or reporting. Unchanged: do not open it. Saved state only; the user's Cmd-S is the release.

Spanish localization is deferred. Audio, video, and website material are outside this skill.
