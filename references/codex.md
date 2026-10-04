# Codex Adapter

<!-- rule:CDX-01 -->
## Instruction and tool discovery

Read the applicable `AGENTS.md` files and the user's current instructions before acting. Inspect the tools, skills, apps, filesystem permissions, approval policy, and agent slots actually exposed in this session. Do not assume a shell, browser, subagent count, writable path, network access, or approval state from another Codex host.

Invoke this skill as `$warm-handoff` where the host supports named skills. The compact skill stays provider-neutral; this file maps it to Codex.

<!-- rule:CDX-02 -->
## Permissions and durable work

Use the narrowest available tool that completes the action. Read-only inspection and reversible work normally proceed inside the authorized task. Honor explicit file ownership. Ask for or use approval only when the host requires it for an action that is authorized and necessary. Never treat a handoff as permission to publish, install globally, control UI, contact people, or perform destructive work.

Write required plans and reports before claiming completion. Verify persisted files by rereading or hashing them when installation or exact preservation matters.

For every RTF handoff, invoke `scripts/handoff-rtf.sh SOURCE NEW_OUTPUT` from the skill directory; follow [RTF safety](rtf-macos.md). Never generate the final RTF directly with `textutil`: it is only a reader/verification tool in this workflow.

Worker briefs keep applicable user rules binding; a lead must not silently disable them. Record any conflict with host permissions. Wave numbers share one project-wide sequence across hosts; reserve the next unused number in the saved plan (WV-01).

At wave start, create and open the interjections file as `.md` in the project root, never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it. Follow HF-07.

<!-- rule:CDX-03 -->
## Agents and guardian mode

Delegate only when the user, project rules, or active workflow calls for agents. Check real slot availability first. Give each worker a short self-contained brief, exclusive paths, acceptance criteria, and delivery path. Let automatic completion delivery carry routine results.

When a project opts into guardian mode, route substantive research, analysis, implementation, QA, visual inspection, reports, and handoff writing through guardians and workers. The main session performs concise coordination, necessary decisions, and batched acceptance without parallel detail duplication. Do not request status before 25 minutes unless blocked. If no slot is available, report or queue the work; do not silently perform a duplicate copy in the main session.

<!-- rule:CDX-04 -->
## Models, context, and telemetry

Treat model availability, context capacity, reasoning controls, caching, quotas, and cost displays as changeable host facts. Use [model routing](model-routing.md). A published OpenAI API context window does not prove the effective limit of the current Codex client. If the host exposes no effective limit or session telemetry, say it is unknown; do not insert remembered numbers.

Verified 2026-09-11 against official OpenAI documentation: the public API model pages list GPT-6 Astra and GPT-5.6 Sol with 1,050,000-token context windows. This is API specification only. OpenAI's prompt-caching guide describes API caching, not a guarantee about a Codex subscription session.

Sources: [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).

<!-- rule:CDX-05 -->
## Hard rules for a Codex lead

A Codex lead session tends to skip these. Each one is a gate, not advice; a handoff that misses one is not finished.

- [ ] Every timestamp comes from `date` at the moment of writing, never from an estimate.
- [ ] First line of every handoff, report, and interjections file: its own absolute path; second line: the as-of time from `date`.
- [ ] The new handoff is created directly in the project's archive folder and never moved; an answered handoff is never overwritten.
- [ ] Exactly one inbox: the handoff footer until wave start, then the interjections file as `.md` until the next handoff.
- [ ] Before writing, open [handoff format](handoff-format.md) in full; "I know the format" does not count.
- [ ] Read the predecessor unfiltered, first line to last — no truncation, no grep for answer markers only.
- [ ] Bundle at wave end: build, install, commit and push within the authorization, write and open the handoff in one pass; outstanding reports go under "Running and pending".
- [ ] RTF only through `scripts/handoff-rtf.sh`.
