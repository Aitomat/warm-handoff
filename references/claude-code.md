# Claude Code Adapter

<!-- rule:CLA-01 -->
## Instructions and capabilities

Read the applicable `AGENTS.md` and current user instructions. `AGENTS.md` is the one shared instruction file: current Claude Code versions load it as project instructions, so one file serves Codex, Claude, and other agents. Do not create a separate `CLAUDE.md`; if a project keeps one, it is only a pointer or symlink to `AGENTS.md`. Inspect the Claude Code version, enabled tools, permissions, agent features, and workspace limits actually present. Invoke `/warm-handoff` where slash-command skills are supported. Treat hooks, agent teams, subagents, worktrees, and cache controls as version- and configuration-dependent.

<!-- rule:CLA-02 -->
## Agents and permissions

Use agents only inside the user's authorized scope. Assign exclusive files and explicit acceptance criteria. Agent completion messages are inputs to integration, not proof by themselves. Do not infer permission to push, install, open applications, or contact others from an old handoff or project template.

Worker briefs keep applicable user rules binding; a lead must not silently disable them. Record any conflict with host permissions. Wave numbers share one project-wide sequence across hosts; reserve the next unused number in the saved plan (WV-01).

At wave start, create and open the interjections file as `.md` in the project root, never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it. Follow HF-07.

<!-- rule:CLA-03 -->
## Cache facts and limits

Verified 2026-09-11 against official Anthropic documentation:

- Claude context windows are model-dependent and can be up to 1M tokens; check the selected model's current page.
- Claude Code documents a one-hour default prompt-cache duration for the main conversation on subscription plans and a five-minute default for other interactions such as subagents, workflows, and forks.
- `promptCacheTtl`, `subagentPromptCacheTtl`, related environment variables, and subagent `cacheTtl` support depend on the installed Claude Code version and configuration.
- Changing effort usually invalidates the cache, while Anthropic documents an exception for Fable 5.1 in some API-key and subscription use.

These are documented client or API behaviors, not proof of the current session's effective context, cache hit, quota, or cost. Report those only from current host evidence. Do not reuse historical pricing ratios or universal cache-break rules.

Sources: [Claude Code prompt caching](https://code.claude.com/docs/en/prompt-caching), [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows).

<!-- rule:CLA-04 -->
## Handoff boundary

Before compacting, switching models, or ending a long run, write the new handoff and verify it on disk. Preserve the complete user collection, record any version-specific assumptions, and separate published platform facts from live session measurements.
