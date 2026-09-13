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

Label each agent the same way in the plan and in the report: `A · Topic · Model/effort`.

Expensive builds and tests run behind a shared project lock held by the role the
plan names. A directory lock is atomic; the PID inside it makes an orphaned lock
recognizable after a crash without anyone removing a live foreign lock:

```sh
L=/tmp/project-build.lock
while ! mkdir $L 2>/dev/null; do
  P=$(cat $L/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $L 2>/dev/null; sleep 30
done; echo $$ > $L/pid
… build/tests …; rm -f $L/pid; rmdir $L
```

**Waiting means waiting, never reporting.** Whoever is queued on the lock does
not file a "blocked" interim note and does not start a second attempt alongside.
Run tests through the project's own test script rather than the raw toolchain
command, and set `TMPDIR=/tmp`. **One build per topic guardian, at the very end —
not one per worker:** the guardian collects the worker results and builds once
over the integrated state. Guardians end their own wait loops and background
processes before writing the report; a report filed next to a still-running
background run of one's own is not a report.

Projects may explicitly opt into **guardian mode**. In that mode, substantive research, analysis, implementation, QA, visual inspection, reports, and handoff writing go through a guardian and its workers. The main session limits itself to concise coordination, necessary decisions, and batched acceptance; it does not duplicate detail work in parallel. Use short self-contained briefs and automatic result delivery. Do not ask for status before 25 minutes unless there is a real blocker. If slots are unavailable, report the host limit and queue or reduce the wave instead of doing duplicate work.

<!-- rule:WV-04 -->
## Two build slots (rule 4 v2, 2026-09-13)

At most TWO builds run at a time (user, 2026-09-13 03:23: „Zwei Builds
gleichzeitig erlauben bitte"; 04:00: „mehr wie zwei nicht"). This replaces the
earlier one-lock, strictly sequential rule. Each topic guardian builds once, at
the end of its topic, with its targeted tests only; the full suite belongs to the
merge guardian, who waits for ALL done markers. Order runs from the largest topic
to the smallest. A guardian claims a free slot as soon as at most ONE predecessor
is still without a done marker:

```
TRASH=<project trash directory>               # never rm; move corpses here
M=/tmp/<wave>-fertig; VOR="a b"               # my predecessors in build order; A: empty, B: "a"
while [ "$(for v in $VOR; do [ -f $M-$v ] || echo x; done | wc -l)" -gt 1 ]; do sleep 30; done
L=""; while [ -z "$L" ]; do
  for s in 1 2; do C=/tmp/aitomat-build-$s.lock
    if mkdir $C 2>/dev/null; then L=$C; break; fi
    P=$(cat $C/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $C 2>/dev/null
    [ -f $C ] && mv $C "$TRASH"/lock-leiche-$s-$$   # file corpse instead of directory (W58, 01:48)
  done; [ -z "$L" ] && sleep 30
done; echo $$ > $L/pid; uptime
… build + targeted tests …
rm -f $L/pid; rmdir $L; touch $M-<me>
```

A lock directory whose pid no longer exists is cleared with `rmdir`. A lock that
exists as a FILE instead of a directory is a corpse (observed W58, 01:48): move
it to the project's trash directory, never `rm` it. Wait in the foreground
(repeat the wait command; a host timeout of up to 600000 ms is fine), never
detached, and never report before the build finished. Workers and subagents do
not build (`swiftc -parse` at most). Log `uptime` before the build, and compare
load average and wall-clock duration against the previous wave in the report.

## Execution and integration

Start independent packets together only when the host supports it. Workers must stop before touching unowned files. A result report states changed paths, tests, evidence, limitations, and unresolved dependencies. Integration verifies the diff and reruns the smallest meaningful combined checks. A start notification or worker claim is not acceptance evidence.

<!-- rule:WV-05 -->
## Communication

Let host completion delivery carry routine results. Send updates for a real blocker, a decision that changes scope, or a material risk. Keep the user-facing thread focused on choices and verified outcomes. User instructions override generic delegation preferences for that workflow. On every wake-up of the main session, check the interjections file's modification time and read it if it changed, before acting or reporting (user rule of 2026-09-13).

See [Codex](codex.md), [Claude Code](claude-code.md), [model routing](model-routing.md), and [evidence scope](evidence-scope.md).
