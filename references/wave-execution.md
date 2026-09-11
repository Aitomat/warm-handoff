# Authorized Work Waves

<!-- rule:WV-01 -->
## Authorization and plan

A wave begins only after the user authorizes its objective and side effects. Persist a plan before starting workers. For every packet record: ID, outcome, exclusive paths, dependencies, acceptance criteria, model or effort when relevant, prohibited actions, and report path.

<!-- rule:WV-02 -->
## Capacity and ownership

Read the host's actual agent inventory and machine constraints. Never promise more parallelism than exists. One agent owns each writable path. Partition by files and independently testable outcomes. Serialize builds, shared test state, mutable services, integration, and release actions.

<!-- rule:WV-03 -->
## Direct workers and optional guardian mode

Direct workers suit independent packets. Guardians suit packets that need worker coordination, review, or integration. Do not add a guardian layer merely for labels.

Projects may explicitly opt into **guardian mode**. In that mode, substantive research, analysis, implementation, QA, visual inspection, reports, and handoff writing go through a guardian and its workers. The main session limits itself to concise coordination, necessary decisions, and batched acceptance; it does not duplicate detail work in parallel. Use short self-contained briefs and automatic result delivery. Do not ask for status before 25 minutes unless there is a real blocker. If slots are unavailable, report the host limit and queue or reduce the wave instead of doing duplicate work.

<!-- rule:WV-04 -->
## Execution and integration

Start independent packets together only when the host supports it. Workers must stop before touching unowned files. A result report states changed paths, tests, evidence, limitations, and unresolved dependencies. Integration verifies the diff and reruns the smallest meaningful combined checks. A start notification or worker claim is not acceptance evidence.

<!-- rule:WV-05 -->
## Communication

Let host completion delivery carry routine results. Send updates for a real blocker, a decision that changes scope, or a material risk. Keep the user-facing thread focused on choices and verified outcomes. User instructions override generic delegation preferences for that workflow.

See [Codex](codex.md), [Claude Code](claude-code.md), [model routing](model-routing.md), and [evidence scope](evidence-scope.md).
