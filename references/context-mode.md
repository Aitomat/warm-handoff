# Optional Context Mode

<!-- rule:CM-01 -->
## Purpose

Context Mode can process large files, logs, command output, and structured data while returning a focused result. Use it when the raw output would consume material context. Small fixed outputs and file edits still belong in the host's ordinary tools.

<!-- rule:CM-02 -->
## Three independent states

Check and report these separately:

1. **Package installed:** files are present in the configured environment.
2. **MCP reachable:** a Context Mode tool can be called in this session.
3. **Hooks effective:** the expected capture or indexing hooks are registered and operating.

One state does not prove another. Use the plugin's diagnostic tool when available; otherwise label the untested states unknown.

<!-- rule:CM-03 -->
## Permission boundary

Do not install, upgrade, enable hooks, or change global settings without explicit permission. A project may recommend Context Mode, but the warm-handoff skill must still work without it. Never expose secrets or bypass host filesystem rules through a processing tool.
