# Model Routing

<!-- rule:MR-01 -->
## Route by task and evidence

Choose a model for the task's reasoning depth, latency, tool use, and verified availability. Use a cheaper or faster model for bounded transformations and a stronger model for ambiguous integration or review only when the host offers it. Do not encode a personal model lineup as a universal rule.

<!-- rule:MR-02 -->
## Keep three scopes separate

1. **API specification:** published model context window, features, and API pricing.
2. **Client or host boundary:** models, reasoning settings, context, quotas, caching, and tools the current product exposes.
3. **Session measurement:** request counts, tokens, cache behavior, elapsed time, or cost observed in this run.

Never convert one scope into another without direct evidence. Unknown effective limits remain unknown.

<!-- rule:MR-03 -->
## Current verified notes

Checked 2026-09-11 from official primary documentation only:

- OpenAI API pages list GPT-6 Astra and GPT-5.6 Sol with 1,050,000-token context windows. This does not establish a Codex host limit.
- OpenAI API prompt caching for GPT-5.6 and later documents a 30-minute minimum/default retention and automatic caching for eligible prefixes starting at 1,024 visible input tokens. This does not establish cache behavior or billing for a Codex subscription.
- Anthropic documents model-dependent Claude context windows up to 1M tokens and separate Claude Code cache defaults for main subscription conversations and other interactions. These do not establish the live session's cache or quota.

Sources: [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), [Claude context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows), [Claude Code prompt caching](https://code.claude.com/docs/en/prompt-caching).
