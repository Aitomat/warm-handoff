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
L=/tmp/<project>-build.lock
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
## One build slot

Exactly ONE build runs at a time. The limit is memory, not agent count: measured
once on a memory-bound laptop, two concurrent builds of a compiled project left
the machine unusable for hours, while ten thinking agents barely registered.
Earlier editions of this skill allowed two slots; one slot replaces them.

- **The lock belongs in the project's test script, not in the worker prompt.** A
  prompt is a request — in one measured wave six of fourteen worktrees built at
  the same time despite it. A script is a gate every worker passes through.
- **A final build counts only when it reached the tests.** A run that aborts
  before the first test (tooling, cache, environment) is not a final build and is
  repeated; whoever changes anything after their run does a second one. Both runs
  go in the report. The rule saves load; it must never suppress evidence.
- **One build per topic owner, at the very end** — not one per worker. The owner
  collects the worker results and builds once over the integrated state. Workers
  and subagents do not build beyond a syntax or parse check.
- **Cap concurrent workers** (four is a sound ceiling on a single laptop). More
  is not faster when they queue behind one slot anyway.
- A paused build keeps its memory; pausing helps the CPU, not RAM. The answer is
  not to start the second build at all.

The slot itself, claimed after at most one predecessor is still unfinished:

```sh
TRASH=<project trash directory>               # never rm; move corpses here
M=/tmp/<wave>-done; PRED="a b"                # my predecessors in build order
while [ "$(for v in $PRED; do [ -f $M-$v ] || echo x; done | wc -l)" -gt 1 ]; do sleep 30; done
L=""; while [ -z "$L" ]; do
  for s in 1; do C=/tmp/<project>-build-$s.lock
    if mkdir $C 2>/dev/null; then L=$C; break; fi
    P=$(cat $C/pid 2>/dev/null); [ -n "$P" ] && ! kill -0 $P 2>/dev/null && rmdir $C 2>/dev/null
    [ -f $C ] && mv $C "$TRASH"/lock-corpse-$s-$$   # file corpse instead of directory
  done; [ -z "$L" ] && sleep 30
done; echo $$ > $L/pid; uptime
… build + targeted tests …
rm -f $L/pid; rmdir $L; touch $M-<me>
```

A lock directory whose pid no longer exists is cleared with `rmdir`. A lock that
exists as a FILE instead of a directory is a corpse: move it to the project's
trash directory, never `rm` it. Wait in the foreground (repeat the wait command;
a host timeout of up to 600000 ms is fine), never detached, and never report
before the build finished. Log `uptime` before the build, and compare load
average and wall-clock duration against the previous wave in the report.

## Execution and integration

Start independent packets together only when the host supports it. Workers must stop before touching unowned files. A result report states changed paths, tests, evidence, limitations, and unresolved dependencies. Integration verifies the diff and reruns the smallest meaningful combined checks. A start notification or worker claim is not acceptance evidence.

<!-- rule:WV-05 -->
## Communication

Let host completion delivery carry routine results. Send updates for a real blocker, a decision that changes scope, or a material risk. Keep the user-facing thread focused on choices and verified outcomes. User instructions override generic delegation preferences for that workflow. On every wake-up of the main session, check the interjections file's modification time and read it if it changed, before acting or reporting (user rule of 2026-09-13).

<!-- rule:WV-06 -->
## Permissions build agents actually need (2026-09-14)

A worker that cannot build delivers unverified code — more expensive than any
permission you saved. Settle these four points BEFORE the wave starts and write
them into every worker's brief:

1. **Write access to tool caches.** Compilers and package managers write outside
   the working directory (e.g. `~/.cache`). Without that right every test run
   dies before compilation. Grant it explicitly at the host (Codex: `--add-dir`).
2. **Resolve nested sandboxes.** An agent already inside a sandbox cannot let a
   tool open a second one. Typical evidence: `sandbox_apply: Operation not
   permitted`. The fix is the tool's own option to skip its internal check — not
   disabling the host sandbox. Put that option verbatim in the brief, and add
   that failed attempts do not count against the build-once rule.
3. **Require intermediate commits.** Workers that commit only at the end lose
   everything on any abort. Commit after each finished point; squash at the end.
4. **Clarify process lifetime.** Background processes of the main session can die
   with it. Check whether started workers survive an abort of the main session,
   and do not run long jobs next to abort-prone background commands.

Evidence 2026-09-14, wave 62: three workers delivered unverified code (point 2),
three more lost a quarter hour of work each (points 3 and 4).

<!-- rule:WV-07 -->
## Cap and measure load (2026-09-14)

Build slots cap the number of builds, not the number of processes. A single
build starts as many compiler processes as the machine has cores — two
concurrent builds bring the user's machine to its knees. Evidence 2026-09-14,
wave 62: two build slots on twelve cores produced sixteen compiler processes and
a load average of 104; the user could barely work.

So, in addition to the slots:

1. **Cap jobs per build.** At most a quarter of the cores per build (`-j 3` on
   twelve cores), so two builds together leave half the machine free. The option
   belongs in every worker's brief.
2. **Build politely.** Start builds and tests at low priority (`nice -n 10`) so
   the user's interface keeps precedence.
3. **Measure before and after.** Note the load average at wave start and at the
   end, and put it in the wave's measurement. A load above the core count means
   the wave was too wide; the next one runs with fewer concurrent workers.
4. **The machine belongs to the user.** Noticeable slowdown is a blocker, not a
   blemish: renice running builds (`renice +15`) instead of killing them, and
   narrow the wave immediately.

<!-- rule:WV-08 -->
## One smoke test before the wave (2026-09-14)

Before the wave starts, have ONE worker run the smallest real build-and-test —
not the main session, but a worker under exactly the permissions every worker
will get. Only when that run compiles do the others start.

Evidence 2026-09-14: without a smoke test four guardians set off, all four hit
the same sandbox obstacle, and the cause surfaced only an hour later. A single
smoke test would have shown it in three minutes. The same failure had occurred
in the previous wave — in another form, with the same effect: unverified code.

Check three things in the smoke test and record them in the wave plan: the
worker can write where the tooling must write; it can build and test; its
process survives an abort of the main session. Repeat the smoke test whenever
host, model, or permissions change.

Second lesson from the same day: the width of the wave is not the problem, the
load is. With a capped job count per build (WV-07) more workers run at once
without paralysing the machine — twelve topics in three batches cost more wall
clock than twelve in two.

<!-- rule:WV-09 -->
## Pre-flight before the first worker starts

Run this list once, before any worker is launched. Each item cost a measured
wave hours when it was skipped:

1. **Prime the tool caches.** Make sure prebuilt native modules the agent CLI
   needs are already in its plugin cache; otherwise every worker triggers its own
   package install (measured once: about 1500 processes and a load average of
   148). The same holds for compiler module caches: rename or clear stale ones
   before the wave, not during it.
2. **Smoke-build in a directory no worker will use.** A worker editing the file
   the smoke build is compiling invalidates the smoke test. See WV-08.
3. **Set the toolchain environment explicitly** in front of the test script in
   secondary working directories, where a bare call may pick the wrong toolchain.
4. **Confirm the four permission points of WV-06** and write them into every brief.
5. **Write one rules file for the workers and version it** — append the wave
   number, never copy the file. A copied file resurrects sentences the user has
   since forbidden. Workers leave stray unrelated files alone and always commit
   with an explicit file list, never with a catch-all add.

<!-- rule:WV-10 -->
## Wave choreography: start per topic, merge early, build late

Waiting, not building, is the cost of a wave. Measured with one build slot and
ten topics:

- **Start each worker as soon as ITS pre-work is ready** (the file:line list for
  its topic), not once the whole wave is planned. Staggering then comes for free
  and the first build starts minutes in.
- **Workers build in the foreground and never poll in the background.** The build
  queue is silent, so a worker that backgrounds sleep/poll loops re-wakes itself
  and its neighbours: one observed worker produced a loop every six seconds and
  drove the load average past 40, and a finished worker kept being woken at a
  large context each time. Put the ban verbatim in every brief. If a worker still
  loops, stop it, kill its loops, and run its final test yourself; its commits are
  safe.
- **Reuse built directories instead of creating fresh worktrees.** A copied build
  directory is not reused in a new path (absolute paths inside), so the first
  build there is a full rebuild — with one slot, five fresh worktrees are hours of
  queue. When a worker finishes, branch the next topic inside ITS directory and
  build incrementally. Stack a topic on a predecessor's branch when both touch
  the same file, and stop the finished worker's leftover processes before reusing
  its directory (look for shells whose command mentions its log file, not only
  its folder).
- **Merge early, build late.** Merge every finished topic into the wave branch
  immediately, merge only, no build; conflicts then surface one at a time. Use an
  explicit merge message: a default merge message silently drops required trailers.
- **State the file boundaries in every assignment** ("do not touch: …"). Six
  parallel topics with explicit boundaries produced zero conflicts.
- **Never edit sources in a directory where a build is running.** Put a late fix
  in a free built directory on its own branch and merge it after the suite.

<!-- rule:WV-11 -->
## Keep the first full suite green

Per topic, the wave is only as fast as its first full suite; in a measured wave
six topics built and merged in half an hour and then took four full suites to go
green. The levers:

- **Search for stale contracts before building.** A worker that changes visible
  texts, menu titles, messages, layout order, asset dimensions, or the NUMBER of
  built-in items greps the test tree for the old string or identifier BEFORE its
  build, adds every hit to its test filter, and rewrites it to the new, equally
  sharp contract. The lead repeats that search across all worker reports before
  the first full suite. Stale contracts in old tests are the most common cause of
  extra suites.
- **A test that fails twice is not "flaky under load" until proven.** One
  repeatedly failing test turned out to be a real collision in a short random
  suffix. Never install on a red full suite, however plausible the excuse.
- **A topic filter does not cover older tests a worker edited outside it.** List
  them in the merge notes; the full suite is their first real run.
- **Re-check every "not found" an agent reports** with one search of your own
  before acting on it.
- **Evidence before the assignment.** For a crash or a hang, read the crash
  report and the application's diagnostic log first; the assignment then states
  the cause as proven, likely, or guessed. Topics that ran on guesses cost whole
  waves; a proven backtrace was fixed in minutes.

<!-- rule:WV-12 -->
## Closing a wave

All workers done **and** the full suite green means finish without asking: build,
self-test, install, publish, and write the handoff. Ask only on an unclean finish
— red tests, an unresolved finding, a worker reporting blocked — and then deliver
no artifact but the question, with what is missing and a proposal.

Self-test the finished artifact itself, not the working tree, before installing
it, and read the exit code directly from the run rather than from a summary line
that can be truncated or rewritten.

The inbox follows the same clock as the wave: between handoff and wave start the
handoff is the only inbox; the interjections file is created at wave start and is
the only inbox until the next handoff.

See [Codex](codex.md), [Claude Code](claude-code.md), [model routing](model-routing.md), and [evidence scope](evidence-scope.md).
