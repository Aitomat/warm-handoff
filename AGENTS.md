# Codex instructions for warm-handoff

Read `SKILL.md` in full before working on this repository. Its six rules and the references they name are binding here for Codex too; use `references/codex.md` as the host adapter. User instructions and the actual host permissions take precedence. Every change to an active rule must also be reflected in this file.

## Scope and resumption

- Read the complete latest saved handoff, later user messages, applicable project instructions, and the designated feedback source. Preserve original user text verbatim. A handoff does not add authorization.
- Check claims against files, Git state, and relevant tests. Mark unverified claims as unknown. Keep each worker within exclusive paths; delegate only when the assignment and host permit it.
- Before writing a new handoff, read `references/handoff-format.md` completely and the predecessor from first to last line. Use its required section order. Close a wave with outstanding reports recorded as pending; do not wait for one more report.

## Inbox and wake-ups

- Use one inbox at a time. Before a wave starts, the handoff footer and its `>>>User answer:` lines are the inbox; do not create a Zwischenrufe file alongside it. At wave start, create and open the Zwischenrufe file; it remains the inbox until the next handoff.
- Saving (`Cmd-S`) releases saved input within existing authorization. **Saving does not itself wake or trigger an agent.** On each actual new request, notification, timer wake-up, or resumed turn, compare the designated inbox file's modification time with the last read. Read saved additions only if it changed, before acting or reporting. If unchanged, do not reopen it. Never use unsaved editor text.
- Answer short Zwischenrufe promptly and schedule longer ones into the next wave. Follow `references/handoff-format.md` when writing replies into that file.

## Work waves and documents

- Read `references/wave-execution.md` before a work wave. Keep paths exclusive and shared resources serialized. Guardians are optional unless the project explicitly selects guardian mode. In that mode, let guardians and workers handle substantive work; the main session coordinates and accepts results. Do not send routine status pings while waiting.
- Only one build runs at a time; enforce the lock in the project's test script, not just a prompt. Smoke-build before workers start. A final build counts only after reaching tests; repeat it if tooling aborts earlier or code changes afterwards. Topic guardians build at the end with targeted tests; the merge guardian runs the full suite. **Give the longest-running guardian/largest topic first access to the build slot, then the next largest.** Workers do not build. Wait in the foreground as specified in `references/wave-execution.md`.
- Never overwrite an answered handoff. Create the new Markdown source directly in the project's archive folder with its absolute path as the first line, followed by the date; create a new editable RTF when requested. Use only `scripts/handoff-rtf.sh` for handoff and Zwischenrufe RTFs. Preserve text behind `>>>` as black on gold at 18 pt; verify text roundtrip and links. Archive answered handoffs with `mv`, never `rm`.
- Do not install optional helpers without permission. Before completion, reread changed feedback, inspect Git status, run the relevant checks, write the durable report, and state completed, pending, and running work with evidence. Use system time for timestamps. A clean wave proceeds through build, install, publication, and handoff within its authorization; ask for direction on an unclean finish.
