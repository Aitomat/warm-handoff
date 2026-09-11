---
name: warm-handoff
description: Preserve original user feedback and verified work state across pauses; prepare or resume a handoff and plan or execute an authorized work wave from collected answers.
---

# Warm Handoff

Keep the user's intent, original answers and verified state available for the next
session. Use German for this workflow unless the user chooses another language.
Distinguish reading/collecting, planning, executing and handing off. Reading ideas
does not itself authorize implementation; existing authorization carries forward.

For a handoff or resume, read [handoff format](references/handoff-format.md).
Use the previous document's structure, retain every original answer and recheck
all agreed saved sources, including RTF, Zwischenrufe, chat and late additions.
Saving submits input: compare whole saved revisions at natural work steps and
before handoff, without polling or importing unsaved drafts by default. Missing
agreed saved sources mean incomplete import. Keep interpretation separate from input.

Read the active host adapter: [Codex](references/codex.md) or
[Claude Code](references/claude-code.md). Both support the same document-led cycle:
answered handoff → concrete plan → authorized work → verified next handoff.
No global configuration, model switch, publishing, Goal or monitoring is implied.

For delegated waves read [wave execution](references/wave-execution.md).
The main agent writes the concrete plan. Small connected work stays local;
authorized independent packets go directly to workers in isolated worktrees.
Use a guardian only when internal coordination is needed; preserve actual host
slots for workers. Briefs stay short and self-contained, with original evidence,
authorization, ownership and acceptance. Prefer delivered completion events over
repeated short status polls; follow host communication and waiting limits.

For the chosen RTF/TextEdit workflow, read [RTF safety and tab groups](references/rtf-macos.md).
The copy line belongs at the top and points at the new editable answer document.
Open all mentioned user-facing documents in the active TextEdit tab group or one
new common group. Never merge unrelated windows, overwrite an existing answer
file, or leave a newly created empty helper tab/window behind. Verify UI results;
when tools are unavailable, report exactly which documents remain unopened.

Pasted Content / [pasted text] applies to Codex and cmux as well as Claude:
use the actual supplied content or referenced file, never infer it from a collapsed
placeholder. Preserve long dictation in the agreed document and short steering in
chat. Follow the host's communication rules while work continues.

Report completed, pending and running work with evidence and the next action.
Telemetry needs source, age and scope; missing values are “nicht gemessen”.
Cache expiration is not memory loss. No artificial keepalive work or universal
context/cost assumptions. [Historical evidence](references/historie.md) preserves
provenance without overriding the current user or host.
