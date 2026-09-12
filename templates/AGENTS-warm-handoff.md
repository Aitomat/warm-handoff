# Warm-handoff project agreement

Copy only the rules the project adopts. Replace bracketed placeholders. This template does not grant permissions by itself.

<!-- rule:AG-01 -->
## Start and continuation

- At session start and before handoff, read `[handoff agreement path]` and the newest named handoff.
- Treat the saved handoff plus later user messages as one ordered input stream.
- Read `[feedback path]` completely at natural checkpoints and immediately before completion.
- Preserve user originals verbatim; put agent replies and interpretations in separate sections.

- Generate every RTF handoff with `scripts/handoff-rtf.sh` from the skill directory, following [RTF safety](../references/rtf-macos.md); never substitute direct `textutil` generation.

<!-- rule:AG-02 -->
## Scope and ownership

- Work only within the user's authorization and assigned paths.
- One agent owns each writable file. Stop and report before touching an unowned path.
- Never infer permission to install, publish, push, control UI, contact others, or perform destructive work.
- Serialize commands that share `[build lock or mutable resource]`.

<!-- rule:AG-03 -->
## Optional guardian mode

- Guardian mode: `[enabled / disabled]`.
- When enabled, substantive research, analysis, implementation, QA, visual inspection, reports, and handoff writing go through guardians and workers.
- The main session handles concise coordination, necessary decisions, and batched acceptance without duplicate detail work.
- Use short self-contained briefs, automatic completion delivery, and no status request before 25 minutes unless blocked.
- Respect actual host slots; queue or reduce work when capacity is unavailable.

<!-- rule:AG-04 -->
## Evidence and closure

- Verify repository state, changed paths, tests, and persisted reports before calling work complete.
- Separate API facts, client or host limits, and current-session measurements.
- Write the required durable report at `[report path]`.
- State completed, pending, running, and blocked work plus the next entry point.

Host-specific additions belong in the active adapter: [Codex](../references/codex.md) or [Claude Code](../references/claude-code.md).
