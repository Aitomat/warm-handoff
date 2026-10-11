# Claude Code Adapter

<!-- rule:CLA-01 -->
## Instructions and capabilities

Read the applicable `AGENTS.md` and current user instructions. `AGENTS.md` is the one shared instruction file: current Claude Code versions load it as project instructions, so one file serves Codex, Claude, and other agents. Do not create a separate `CLAUDE.md`; if a project keeps one, it is only a pointer or symlink to `AGENTS.md`. Inspect the Claude Code version, enabled tools, permissions, agent features, and workspace limits actually present. Invoke `/warm-handoff` where slash-command skills are supported. Treat hooks, agent teams, subagents, worktrees, and cache controls as version- and configuration-dependent.

<!-- rule:CLA-02 -->
## Agents and permissions

Use agents only inside the user's authorized scope. Assign exclusive files and explicit acceptance criteria. Agent completion messages are inputs to integration, not proof by themselves. Do not infer permission to push, install, open applications, or contact others from an old handoff or project template.

Worker briefs keep applicable user rules binding; a lead must not silently disable them. Record any conflict with host permissions. Wave numbers share one project-wide sequence across hosts; reserve the next unused number in the saved plan (WV-01).

At wave start, create the interjections file as `.md` in the project root and open it in an editor the user can type into (on macOS: `open -a TextEdit "<full path>"`, never a read-only viewer such as a cmux markdown tab), never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it. Follow HF-07.

<!-- rule:CLA-03 -->
## Cache facts and limits

Verified 2026-09-11 against official Anthropic documentation:

- Claude context windows are model-dependent and can be up to 1M tokens; check the selected model's current page.
- Claude Code documents a one-hour default prompt-cache duration for the main conversation on subscription plans and a five-minute default for other interactions such as subagents, workflows, and forks.
- `promptCacheTtl`, `subagentPromptCacheTtl`, related environment variables, and subagent `cacheTtl` support depend on the installed Claude Code version and configuration.
- Changing effort usually invalidates the cache, while Anthropic documents an exception for Fable 5.1 in some API-key and subscription use. Rechecked 2026-10-11: Claude Code now documents that switching effort keeps the cache for Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 via API key or Claude subscription; provider, version and configuration can exclude this. In direct API calls a changed request-wide effort or thinking setting invalidates at least the message cache.
- Switching the model inside a session processes the whole history again without hits from the old model's cache: the rebuild is billed as a cache write (1.25× base input for five minutes, 2× for one hour), while a cache read normally costs 10 % of base input and less on some newer models. Check the current pricing page before quoting a number.

These are documented client or API behaviors, not proof of the current session's effective context, cache hit, quota, or cost. Report those only from current host evidence. Do not reuse historical pricing ratios or universal cache-break rules.

Sources: [Claude Code prompt caching](https://code.claude.com/docs/en/prompt-caching), [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows), [API prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

<!-- rule:CLA-04 -->
## Handoff boundary

Before compacting, switching models, or ending a long run, write the new handoff and verify it on disk. Preserve the complete user collection, record any version-specific assumptions, and separate published platform facts from live session measurements.

Claude sessions run long and drop the request stamp easily: the first reply to every new user message starts with `Name, DD.MM.YYYY-HH:MM` from `date` (HF-09), even deep into a wave.

<!-- rule:CLA-05 -->
## Compacting well: one session instead of many

A long project does not need a fresh session for every step. Keep one session running and run `/compact` at a good moment: between two steps, when the state is on disk.

1. **Ask first what to type afterwards.** Before compacting, ask the agent: "What should I enter after `/compact`?" It writes a continuation block into a file (where things stand, what runs, the next step, which files to read) and gives you one sentence to paste.
2. **Compact, then paste.** After `/compact`, copying and pasting that sentence is enough; the agent rereads the file instead of relying on the summary.
3. **Why it matters:** a fresh session rebuilds the whole cache and loses the working rhythm; a compacted session keeps its rules and memory files and only drops the raw history.

Observation, not documented behavior: in recent Claude Code versions a session was compacted automatically after roughly one hour of inactivity, so the large context did not have to be rebuilt in full. Do not rely on it; write the continuation block before any long pause.

Measured example: one main session ran for more than 57 hours with five compactions and carried several complete work waves, including one with 57 packets.

<!-- rule:CLA-06 -->
## Cron wake-up: a status report that keeps the cache warm

During a long wave, schedule a **one-shot** wake-up (in Claude Code via `CronCreate`) about 50 minutes ahead, and give it real work: a short status report for the user. After the report, set the next one-shot wake-up if the wave is still running. Never create a recurring job.

- **Cache:** with the one-hour main-session cache, a wake-up after about 50 minutes falls inside the window, provided it runs on time. It is not a guaranteed latest read time: if the agent is busy, the wake-up waits until the current step ends, and the session must be open.
- **The user knows when the agent reads again.** Interjections can be collected and saved until the next report instead of being sent one by one; urgent matters still go into the chat.
- **Limits:** that a wake-up generally prevents automatic compaction is not established; a full context can still trigger one. A wake-up costs a request; pair it with a useful report rather than an empty ping. Loading this skill never creates a wake-up by itself (WV-14).

Source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks).

<!-- rule:CLA-07 -->
## Status line as cockpit

Put the numbers a long run depends on into the terminal's footer or status line instead of asking for them: for example context size, the five-hour and weekly usage, the second provider's remaining limit, and the session cost. In a multiplexer such as cmux the footer stays visible across panes, so the user sees at a glance when to compact, when to slow down, or when a reset is near. The status line is a display; an agent still reports only measured values and labels the rest unknown (MR-02).
