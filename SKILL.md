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
all agreed sources, including RTF, Zwischenrufe, chat and late additions. Missing
or unsaved sources mean incomplete import. Keep interpretation separate from input.

Read the active host adapter: [Codex](references/codex.md) or
[Claude Code](references/claude-code.md). Both support the same document-led cycle:
answered handoff → concrete plan → authorized work → verified next handoff.
No global configuration, model switch, publishing, Goal or monitoring is implied.

For delegated waves read [wave execution](references/wave-execution.md).
The Oberchef writes the complete plan; guardians coordinate assigned packets;
workers implement them in isolated worktrees. Delegate only when authorized and
within actual host slots/resources. At most four guardians; this is a ceiling,
not a reason to fill slots. Small connected work stays local.

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
