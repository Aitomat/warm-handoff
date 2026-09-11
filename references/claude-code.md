# Claude Code Adapter

<!-- rule:CLA-01 -->
## Instructions and capabilities

Read the applicable `CLAUDE.md` and current user instructions. Inspect the Claude Code version, enabled tools, permissions, agent features, and workspace limits actually present. Invoke `/warm-handoff` where slash-command skills are supported. Treat hooks, agent teams, subagents, worktrees, and cache controls as version- and configuration-dependent.

<!-- rule:CLA-02 -->
## Agents and permissions

Use agents only inside the user's authorized scope. Assign exclusive files and explicit acceptance criteria. Agent completion messages are inputs to integration, not proof by themselves. Do not infer permission to push, install, open applications, or contact others from an old handoff or project template.

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
