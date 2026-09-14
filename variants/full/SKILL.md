---
name: warm-handoff-full
description: Run the complete warm-handoff workflow for lossless resumptions, editable handoff documents, evidence-aware model routing, and authorized multi-agent work waves.
---

# Warm Handoff — Full Workflow

Use this variant when introducing or auditing the workflow. For routine turns, prefer the compact `warm-handoff` skill. The stable rule IDs below match the compact English and German editions. Reference links are package-root relative: install this file as `SKILL.md` together with the resources declared for `full-en` in `docs/language-matrix.json`.

<!-- rule:WH-01 -->
## 1. Establish scope

1. Read the repository's instruction files before the handoff.
2. Identify the newest handoff, its named feedback or interjection file, and any later user messages.
3. Write down the objective, allowed and prohibited actions, owned paths, expected artifacts, test commands, and delivery boundary.
4. Inspect the current branch, worktree, and relevant files before believing completion claims.

Treat the sources as an ordered stream. Later instructions can refine earlier ones without erasing preserved user text. A handoff carries context and decisions; it does not expand permissions. Ask only when required information cannot be inferred or independent work can no longer continue.

Choose one provider adapter for this run: [Codex](references/codex.md) or [Claude Code](references/claude-code.md). Do not mix host-specific commands into the core workflow.

<!-- rule:WH-02 -->
## 2. Resume without loss

Read every saved source completely. For RTF on macOS, import the entire text with `textutil`; snippets or terminal previews are insufficient. Preserve user-authored blocks byte-for-byte when a byte archive is required and verbatim in the readable handoff. Put interpretation, decisions, and replies in separate labeled sections.

Before acting:

- reconcile duplicates and late additions;
- distinguish explicit decisions from suggestions and agent inference;
- verify referenced commits, files, test results, and running work;
- mark stale, unknown, or unverified state honestly;
- keep secrets and irrelevant transcript material out of the next handoff.

Use a new dated handoff instead of editing an answered source. The opening copy line should identify the new absolute handoff path. Include the preserved user collection, current objective and constraints, verified delivered work, pending or running work, open decisions, test instructions, concise memory, and the collection area for the next session. See [handoff format](references/handoff-format.md). **Mandatory (2026-09-14):** Read `references/handoff-format.md` in full before writing, and read the previous handoff unfiltered — never truncate lines, never grep only for `>>>User answer:`. The mandatory 17-part section order lives in the reference (HF-06). At the end of a wave, do not wait for agent reports; close out.

<!-- rule:WH-03 -->
## 3. Work inside authorization

Continue until the authorized outcome is complete. A useful work packet has one concrete objective, exclusive files, dependencies, acceptance criteria, prohibited actions, and a required report. Split work only when packets are independent. Respect the host's actual agent slots and the machine's resource limits; labels or plans cannot create capacity.

Use direct workers for independent implementation. Add a guardian only when several workers need internal coordination or integration. Keep shared builds, mutable environments, releases, and other contended resources serialized. Never let multiple agents edit the same file. Reread the feedback source before final integration because the user may have saved another complete revision.

Select models by task shape and verified availability, not folklore. Separate published API specification, effective client or host limits, and measurements from the current session. Current platform notes and their verification dates live in [model routing](references/model-routing.md) and [evidence scope](references/evidence-scope.md). See [wave execution](references/wave-execution.md) for the full packet and integration contract.

<!-- rule:WH-04 -->
## 4. Preserve document safety

Markdown is the agent-authored source. An RTF twin can be the user's editable response document on macOS. Never overwrite an existing answer file or follow an output symlink. Render to a temporary file, verify the text roundtrip and hyperlink fields, then publish exclusively.

Gold answer paragraphs begin with `>>>`. A blank paragraph immediately after an answer marker must also carry the gold 18-point style so text typed there and continued with Return retains the answer style. The next agent-authored paragraph must reset to the normal background.

Keep three claims separate:

1. renderer checks prove generated text and RTF link fields;
2. an AppKit/TextEdit continuation test proves formatting after typing, Return, save, and reload;
3. pasting into another application requires its own manual or application-level evidence.

Opening TextEdit or changing tab groups is a UI action and needs the task's authorization. See [RTF on macOS](references/rtf-macos.md).

<!-- rule:WH-05 -->
## 5. Use optional helpers deliberately

[Context Mode](references/context-mode.md) is optional. It can process large files or command output while returning a focused result. Check three states independently: whether the package is installed, whether its MCP tools are callable in this session, and whether its hooks are active. A working MCP call does not prove hooks; package presence does not prove either. Never install or upgrade it without permission.

<!-- rule:WH-06 -->
## 6. Close with evidence

At the last safe checkpoint:

1. reread the designated saved feedback source;
2. inspect Git and confirm only owned paths changed;
3. run the required targeted checks and record exact outcomes;
4. verify every completion claim from an artifact or command;
5. write the durable report at the requested path;
6. state completed, pending, running, and blocked work plus the next entry point.

Do not call work complete because a process started, a file exists, or another agent said it passed. If a manual check was not performed, leave it explicitly open.

Spanish localization is deferred. Audio, video, and website material remain future proposals and are not part of this package.
