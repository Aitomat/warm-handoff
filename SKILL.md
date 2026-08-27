---
name: warm-handoff
description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, measures context size, request count and cache hit rate from the session file instead of guessing, keeps the number of requests down (subagents first), warns before cache-destroying actions, surfaces the paid quota left in Codex and Claude Code, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", "quota", or when resuming after a gap.
---

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

*By Yasin Akgün ([github.com/Aitomat](https://github.com/Aitomat)) — grown out of daily
work on the macOS app [Aitomat](https://aitomat.ai) and sharpened continuously against
measured numbers, not invented at a desk. The dated quotes throughout are his, from the
sessions that produced each rule.*

Claude Code caches your conversation prefix. Working *inside* that cache is fast and cheap;
rebuilding it is slow and expensive. This skill makes the cache window visible, keeps you
inside it, keeps the number of requests small — and, when leaving is the better deal, writes
the handoff that lets a fresh session continue seamlessly.

It is also meant to TEACH. Every cost claim comes with the arithmetic behind it, because a
user who understands why a fat context is cheap to talk on and expensive to work on will make
better calls than one who is merely told to "be efficient". Three teaching rules apply
throughout, from Yasin's explicit request (26.08.2026, 16:53: *"the skill should also teach.
People should understand how this actually works — what happens to me happens to a lot of
people."*):

1. **Number first, rule second.** Not "that's expensive", but "that's 22k equivalents,
   because the context is 220k and reading costs a tenth".
2. **Clear up misunderstandings actively.** The most common one: "X requests = X cache
   rebuilds" (wrong — see "Spotting a cache rebuild" below).
3. **Name your own mistakes.** When an earlier explanation was off (one case: "saved almost
   half" — recalculated, it was closer to a third), correct it out loud rather than silently
   overwriting it.

## 1. The facts (verified against Claude Code docs, 2026-08)

- **Pro/Max subscription: 1-hour cache TTL, sliding.** Every message and every cache hit
  resets the 1-hour timer. Stay under one hour between exchanges and the cache lives forever.
- **Fallback:** exceeding plan limits and drawing on paid usage credits drops Claude Code to
  a 5-minute TTL automatically.
- **Subagents always use a strict 5-minute TTL**, even on Max.
- Env overrides: `ENABLE_PROMPT_CACHING_1H=1`, `FORCE_PROMPT_CACHING_5M=1`.
- **The three cost items, and all three matter:** cache read ×0.1 · cache write ×2 ·
  **own output ×5**. The write factor depends on the TTL — **2× for the 1-hour storage**
  (the normal case on Pro/Max), 1.25× only for the 5-minute one. Using 1.25 prices a rebuild
  about 60 % too cheap; this is the single most common arithmetic error in cache discussions.
- **What kills the cache instantly, regardless of the clock:** switching model or reasoning
  effort mid-session, editing the system prompt / CLAUDE.md mid-session, an MCP server that
  crashes and restarts (stdio servers showing "Connection Failed" are prime suspects), and
  anything else that changes the cached prefix. Set model and effort at the START, never
  mid-session — before the first message it costs nothing.

## 2. What Claude does when this skill is active

1. Timestamp every reply (section 3).
2. State the cache window when asked ("am I still cached?"): last exchange + 60 minutes,
   sliding. Answering the question itself resets the timer.
3. Warn before cache-destroying actions — a mid-session `/model` or `/effort` change, a
   flaky MCP server in the config — *before* the user pays for it.
4. Measure context size at every wave end, don't wait to be asked (section 4).
5. Keep the number of requests down, subagents as the default route (sections 5–7).
6. Recommend a fresh session at the sweetspot (section 8).
7. Surface paid quota — Codex and Claude Code — at the top of every handoff (section 11).
8. Write a handoff document automatically after every big work wave (section 12) — do not
   wait to be asked.

## 3. Timestamps — the hard rule

**Every reply gets a timestamp** (e.g. `(22.08.2026, 12:50)`) — and **only from a `date`
call made in THAT SAME reply. No `date` run in this turn → write NO timestamp at all.**

An LLM has no sense of elapsed time; the classic failure is extrapolating from a `date` read
a few turns earlier ("it was 16:28, two agents finished, so ~16:47") — that produced stamps
15+ minutes wrong in practice. Extrapolated ≠ read. Piggyback the read onto any tool call the
reply makes anyway (`… && date "+%H:%M"`), or run `date` alone; a missing stamp is honest, a
guessed one actively misleads the user who relies on it to judge the cache window. This is
the cheapest cache monitor that exists.

**Always stamp DATE + time together** (`date "+%d.%m.%Y %H:%M"`), even when the day obviously
hasn't changed — handoffs and logs get read days later, and a bare "16:47" is ambiguous by
then. The read costs nothing: append it to any command the reply already runs.

**The #1 trap: replies to background-agent notifications.** When a subagent finishes and
Claude writes a short status update, that reply usually makes NO tool call — so there is
nothing to piggyback on, and the temptation is to extrapolate ("last read 18:34, three agents
done, so ~19:40"). A tilde does NOT make a guess honest — `~19:40` is still a fabricated
stamp (real time was 20:02 in practice, 24.08.2026). Rule: agent-status replies either run
`date` as their one tool call, or carry NO time at all. Never `~`-stamps.

## 4. Measure instead of guessing

**Never guess a number you could measure — the same rule applies to the clock, the context
size, and the cost of a round.** A sentence like "cache is fresh (~20k)" written without
looking is a fabrication, and it is worse than saying nothing: the user reads it as a
measurement and plans the wave around it. In the incident that produced this rule (Yasin,
25.08.2026), the real number was ~80k. Yasin's own push-back is the reason a real measurement
exists at all: *"it's odd that you can't see your own total context size — surely there must
be a way."* He was right — Claude Code writes every request, `usage` block included, into the
session file at `~/.claude/projects/<cwd-with-dashes>/<session-id>.jsonl`.

### Context size

Three sources count, in this order of preference:

1. the **status line** the user's terminal renders (`ctx 15% used (85% left)`) — if the user
   pastes or screenshots it, use exactly that number;
2. a monitor/tool call made in THIS turn that reports it;
3. **your own measurement — the best of the three.** The last line carrying `usage` has
   `cache_read_input_tokens + cache_creation_input_tokens` — that IS the current context
   size:

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"
sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c '
import json, os
lines = open(os.environ["SESS"], "rb").read().decode("utf-8","ignore").splitlines()
inp=out=cw=cr=0
for l in lines:
    try: u=(json.loads(l).get("message") or {}).get("usage")
    except Exception: continue
    if not u: continue
    inp+=u.get("input_tokens",0); out+=u.get("output_tokens",0)
    cw+=u.get("cache_creation_input_tokens",0); cr+=u.get("cache_read_input_tokens",0)
for l in reversed(lines):
    try: u=(json.loads(l).get("message") or {}).get("usage")
    except Exception: continue
    if u:
        print(f"context: {(u.get(\"cache_read_input_tokens\",0)+u.get(\"cache_creation_input_tokens\",0))/1000:.0f}k"); break
print(f"API equivalent: ${(inp*15+out*75+cw*18.75+cr*1.5)/1_000_000:.2f}")'
```

Two honest limits: the file is appended per request, so the number is the state of the LAST
request, not of this second. And the dollar figure is the API equivalent at list prices (the
constants above are Opus-tier rates — adjust for your model); nobody on a Pro/Max
subscription pays that sum, it measures what the quota is being charged.

**None of the three sources available → write "context: not measured" (or leave it out).**
The same goes for a handoff's closing line: an invented "~60k" there is the same mistake,
just archived.

**What the status-line fields mean** (users ask, and the numbers look contradictory):
- `ctx N% used` / `ctx 148k` — how full THIS conversation's context window is. Nothing to do
  with billing or quota; resets to zero in a fresh session.
- `5h:3%` — the rolling 5-hour usage window. Matches "current session" in the web UI under
  Settings ▸ Usage.
- `7d:0%` — the weekly window as Claude Code sees it. Can differ sharply from the web UI's
  "all models 59 %", because the web number aggregates EVERYTHING (chats, other models)
  while the terminal field tracks only the Claude-Code slice, and updates in steps, not
  live. When they disagree, the web UI is the authority — say so instead of explaining the
  gap away.
- The web UI also lists per-model bars (e.g. "90 %") with their own reset time. A red bar
  there is the real constraint even when the terminal shows 0 %.

This measurement belongs at every wave end and whenever finishing a large batch of subagent
work — context grows fast there, and a threshold that nobody measures is decoration. This
exact failure happened in practice: the user crossed 400k unnoticed while Claude was busy
orchestrating, and had to point it out himself.

## 5. The real lever: fewer requests

A full measurement of one real working session (26.08.2026) showed context size was only a
third of the truth:

| Item | Tokens | Factor | Equivalent |
|---|---|---|---|
| Cache read | 22,171k | ×0.1 | 2,217k |
| Cache written | 562k | ×2 | 1,125k |
| **Own output** | 208k | **×5** | **1,038k** |

**147 requests — 13 of them triggered by user messages.** The other 134 were Claude's own
tool-steps and interim status notes. Claude's own OUTPUT accounted for nearly a quarter of
total cost. The pattern generalises: a working day can be 500+ requests, of which the user
sent ~20. The user's instinct "batch my messages" is directionally right, but the user's
messages are a rounding error — the lever is not fewer user messages, it is fewer requests
overall and a small context while the many work-steps run.

**Two pieces of vocabulary the table needs**, because this is exactly where Yasin got stuck
the first time he saw it: **"k" means thousand**, so 22,171k is 22,171,000 tokens — twenty-two
million, in one session. And **"equivalent"** means tokens converted to one common price, so
three items billed at three different rates can be compared and added.

**The picture that makes 22 million clicks: the conversation is a book.** The model has no
memory between two requests. Before every single answer it reads the WHOLE book again from
the start — every earlier message, every file it read, every tool result. With 147 requests
and a book averaging ~151k tokens ("pages"), that is 147 × 151k = 22,171k pages read. The
arithmetic closes exactly, which is what makes it worth trusting:

```
147 requests × ~151k average context = 22,171k read     × 0.1 = 2,217k
                                          562k written    × 2   = 1,125k
                                          208k own output × 5   = 1,038k
                                                            total = 4,380k
```

Three goals follow, in this order: **fewer requests · shorter own output · smaller
context.** The handoff (this skill's original purpose) is the WEAKEST of the three levers.

### The technique list (cross-checked with a second model)

A second model (GPT-5.6 via Codex) was given the same numbers and estimated what each
technique would have saved in exactly that session. Target picture: **35–55 requests instead
of 147**, total cost from 4,380k down to 1,350–2,050k equivalents. (The effects overlap and
must not be summed.)

| Technique | How | Effect |
|---|---|---|
| **Batch tool calls** | Request every independent read/search/check in ONE reply, in parallel, and only then evaluate | −25 to −45 requests |
| **Script instead of single commands** | One call that does ten things and prints ONE summary, instead of ten calls | −20 to −35 requests |
| **Cut agents by work package** | ONE agent does "find cause + build fix + check tests", not three agents doing one part each | −30 to −60 requests |
| **Keep the orchestrator context lean** | The agent gets paths, goal, constraints, acceptance criteria — never the chat history | −0.2 to −0.5M read |
| **Reports as files** | The agent writes detail into a file; what comes back is result, risks, path | −0.3 to −0.7M |
| **Cap report length** | State it in the assignment: max 300 words, no work chronicle, no pasted logs | −0.2 to −0.4M output |
| **Bundle interim reports** | See "Messages during the work" below | −15 to −30 requests |
| **Pre-filter output** | `grep`/`jq`/`tail` before printing; success in one line, on failure only the relevant lines | −0.1 to −0.3M |
| **Own output budget** | Interim notes ≤100 words, closing summary ≤500 words, detail into files rather than chat | 208k → 50–80k output |
| **Hand off earlier** | At 100–120k instead of 223k | −0.3 to −0.7M read |

### How few requests are realistic? (the honest answer)

Yasin asked the obvious follow-up (26.08.2026): *"So we're trying to get the 147 requests
down to 14, say — can you put it like that?"*

Yes for the MAIN context. No for the work itself — it does not disappear, it moves into the
subagents (see section 7):

- 100 work-steps in the main context at 220k → 100 × 22k = **2,200k equivalents**.
- The same 100 steps inside a subagent carrying ~30k → 100 × 3k = **300k**. **Factor ~7** —
  and not one of those 100 steps appears as a request in the main session.

The realistic floor for a pure orchestration wave, item by item:

| Requests | What for |
|---|---|
| 1 | reading the handoff |
| 1–2 | launching the whole fleet in ONE bundled reply |
| 1 per agent | its closing report — unavoidable, that is how the result arrives |
| 2–3 | build, test, commit, each through ONE script |
| 1 | writing the handoff |
| 1 | the closing message |

That lands at roughly **13–20 requests instead of 147** for the same delivered work.
Conversation with the user comes on top — and it is wanted, not waste. The number to shrink
is the machine's own chatter, never the user's thinking.

### Output is expensive — write shorter

Output costs **five times** the price of fresh input and fifty times a cache read. In
practice: don't narrate your own work (what the user already sees in the terminal does not
need repeating in prose); long content belongs in files, not chat — that is exactly why the
handoff is a file, not a chat message; no "here's the whole thing again, just to be safe"
duplicate — a pointer to the file is enough. The handoff itself stays thorough: it replaces
an entire context and is therefore the best investment on the list. Thorough ≠ chatty.

## 6. Messages during the work are almost free

Yasin asked this three times (26.08.2026, 17:26), because the answer changes how you use the
tool: *"Does this message cost nothing right now because you happen to be working? Or do you
mean because they're short messages?"*

It is not brevity. It is **timing** — and the gap between the two cases is enormous. His own
description of the mechanism is exactly right: *"While the AI has just been given a new
request and hasn't answered yet, you can slip further requests in. But if it answers in
between and then picks up the new request, it costs ten per cent of the current context
again."*

- **Claude is mid-loop** (tools running, files being read). The message is appended to the
  turn already in flight and rides along with the next request, which would have happened
  anyway. **No additional request comes into being.** You pay for the message text alone,
  written into the cache once: 50 words ≈ 70 tokens × 2 ≈ **140 equivalents**.
- **Claude is idle** (it has answered, nothing is running). Now the message TRIGGERS a
  request that would not otherwise exist: **the whole context × 0.1**. At 220k that is
  **22,000 equivalents** — roughly 150 times as much.

**Precision, because "while something is running" means two different things** (Yasin asked
straight back, 26.08.2026, 17:37 — rightly). What matters is not whether something somewhere
is computing, but whether Claude's OWN tool loop is turning:

| Situation | A message from the user | Cost |
|---|---|---|
| Claude's own tool loop is running (reading a file, running a command, launching an agent) | is appended, rides along | **near zero** |
| **Subagents are computing, Claude is waiting** | triggers a new request | **the full 10 %** |
| After Claude's answer, idle | triggers a new request | **the full 10 %** |

The middle row is the surprising one: while subagents work, the MAIN AGENT IS NOT WORKING —
it is waiting for their reports. A message sent then costs exactly as much as one sent into a
completely idle session.

One consolation: **several messages in quick succession are bundled into ONE request** as
long as they arrive before the answer starts. Two thoughts back to back cost once, not twice.

**The catch that gets overlooked:** the question is cheap — the ANSWER is not. Output costs
×5, so a 300-word reply is ~2,000 equivalents, fourteen times the question that prompted it.
Hence the rule for interjections during a running wave: **answer short, detail goes into the
handoff.** Don't throttle the question, throttle your own rambling.

What the user takes away — say it to them ONCE:

> As long as you can see me rattling away, write whenever you like. When only the subagents
> are running, or when I'm waiting on you, collect instead and send it in one go — best of
> all into the collection area of the handoff, where it costs nothing at all.

That collection area (section 12) costs precisely zero, because no request comes into being.

## 7. Subagents are the default route, not the exception

Yasin's goal (26.08.2026): *"work with a strong model that acts as the boss, sends the
subagents out, uses few tokens, says everything in one bundle and makes few requests."*

**Why the startup cost is the decisive difference.** His own description beats any
documentation (26.08.2026): *"When you send a subagent out, it doesn't start like a new
session at 80,000 tokens times two, but at, say, 10,000 times two. Internally it burns a lot,
some of it cheap, some expensive — but it gives back LITTLE, because it only returns the
result. And that keeps the current session small and cheap."*

The same thing, item by item:

1. **Start context.** A fresh session in a real project measured **82k** before a single line
   of work — skills, tool schemas and project rules load before anyone does anything — and
   the rebuild costs that × 2. A subagent starts with its assignment plus its own tool
   schemas, on the order of **10–20k**; × 2 that is ~20–40k, once.
2. **What happens inside.** The agent reads, searches, edits, runs tests — dozens of steps,
   each re-reading only ITS small context at ×0.1. Some steps are cheap, some (long file
   reads, test output) are not, but every one is priced against ~15k instead of your 220k.
   That is why 100 steps cost ~300k there and ~2,200k here.
3. **What flows back into the main context.** Exactly two things: the assignment you wrote
   and the closing report you capped at 300 words. The chronicle, the logs, the dead ends
   stay in the agent's context and die with it.

Expensive work, cheap receipt — the largest single lever in this skill. In the measured
session six agents together burned over a million tokens, and none of it landed in the main
context except assignments and reports.

**The honest arithmetic, as TWO separate statements.** They get mashed into one comparison
all the time — 147 steps on one side against 600 on the other — which puts a different amount
of work on each side and makes delegation look like it saves nothing. Kept apart, both are
true.

*One: the same work, merely delegated — this genuinely gets cheaper.*

```
All in the main context:  147 steps × 151k × 0.1              = 2,217k
Delegated:                 14 main requests × 345k × 0.1 =  483k
                          147 agent steps  ×  30k × 0.1 =  441k
                                                   total =  924k
```

**2.4× less for exactly the same work** — every step is priced against the agent's small
context instead of the session's fat one, roughly a fifth per work-step.

*Two, a SEPARATE thought:* whoever does not pocket the saving but reinvests it gets a
multiple of the work for the same quota. An agent works more thoroughly than you would in
passing, so 147 steps quickly become 600:

```
 14 main requests × 345k × 0.1 =   483k
600 agent steps   ×  30k × 0.1 = 1,800k
                          total = 2,283k
```

The bill is roughly level again — but **four times as much has been done.** That is what
"token maximisation" means: more work for the same quota, not less spending.

> **Subagents do both: the same work markedly cheaper (factor ~2.4) — and, if you spend the
> saving again, a multiple of the work at the same price.**

**Subagent tokens are not free.** They draw on the same weekly quota. What they don't load is
the MAIN CONTEXT — the session stays small, fast and responsive, and that is their real
value.

**When a subagent does NOT pay off:** below roughly 3–5 tool steps, for strictly sequential
work, or when a lot of shared context would have to be transferred first. Its startup cost is
roughly 1–3 requests plus briefing plus report.

**The subagent contract**, which belongs in every assignment:

> Work until you have a result or hit a real blocker. Report only: status, decisions,
> evidence with paths, risks, next step. At most 300 words, no work chronicle, no pasted logs
> or diffs — put detail in a file.

**Model and reasoning effort belong in the DISPLAYED name** (26.08.2026, 17:35). Yasin's
objection: *"When you send subagents out — can you show down there which kind is working
right now? GPT-5.6 high, extra high, or Opus 5? You set the effort as well. Right now I never
see which agent it is."* Fix: the host displays the agent's short description, so the model
belongs inside it, not just the task:

```
bad:   "history performance, round 2"
good:  "Opus5/high · history performance"
good:  "Fable/low · rename test files"
good:  "GPT5.6 · timing tests"            (Codex run)
```

If no model is set, the agent inherits the session model — label that too ("inherited")
instead of leaving it unsaid. Same rule for the fleet-start announcement: the ONE start
message says who runs on which model at which effort.

### Choosing the tier — cheap/fast vs. strong/slow

State the choice out loud in one clause ("three readers on the fast model, the review on the
strong one"), so the user can veto before the tokens are spent.

| Work | Tier | Why |
|---|---|---|
| Finding files, listing call sites, mechanical renames, log sifting | fast/cheap, low effort | Answer is verifiable at a glance; a strong model adds nothing |
| Writing tests to an existing pattern, doc sweeps, format fixes | fast/cheap, low effort | The pattern is already decided |
| Design decisions, security/correctness review, "why is this wrong" | strong, high effort | Errors here are expensive and hard to spot later |
| Anything the user will ship without re-reading | strong | Treat it as production |

Cross-checking your OWN output is a separate job — a second opinion from a different model
(Codex/GPT, a second reviewer) catches what a same-architecture re-read cannot.

### Pacing: parallel for speed, sequential for warmth

Subagent scheduling is itself a cache instrument. Two modes, chosen by what the user needs
right now (ask, or react to cues like "I'm in a hurry" / "I'm going to bed"):

- **Present, wants speed** → run subagents IN PARALLEL. Say how many agents and what each one
  owns; everything lands fast, the user answers between waves.
- **Steps away** (lunch, evening, night) → run subagents SEQUENTIALLY. Each completion wakes
  Claude, produces a report — a new request that resets the 1-hour timer — so the user
  returns hours later to a still-warm cache and a finished handoff, having typed nothing.
  Claude's goal while away: produce SOME output within each hour, chained through the queue,
  handoff at the end.
- **Mixed is normal**: fan out the independent reads in parallel, then run the dependent
  build/review steps in sequence.
- Honest limit: sequential mode keeps the cache warm only while real work remains. For a long
  absence, build a work queue big enough to span it (backlog items, review rounds, doc
  sweeps) — plan it WITH the user before they leave. Never invent busywork just to touch the
  cache; if the queue runs dry, write the handoff and let the cache go.
- Model economics: the orchestrator holds the big cached context, subagents don't. Run
  subagents on a strong model with LOW reasoning effort for mechanical work, reserve high
  effort for hard review/design steps; set the session's model+effort once at start
  (mid-session switches kill the cache).

### Make the work visible — but do not narrate it

The user watches a status line and a task list, not Claude's reasoning:

- **Keep a live to-do list** for any task with more than ~3 steps, updated as steps finish —
  that list IS the progress bar. A finished step still marked "in progress" is worse than no
  list.
- **Announce the whole fleet ONCE when it starts** — one block, what each agent owns. Then
  radio silence until the end.
- **Name the running total at wave end**: how many agents ran, what came back, what is still
  open.

**No per-agent status notes (revoked 26.08.2026).** An earlier version of this rule said
"announce each subagent when it starts AND when it lands — those lines double as
cache-refreshing requests". Yasin's objection, verbatim: *"You don't need to give me feedback
when one has stopped. Then it stopped — until they're all done, or until nearly an hour has
passed so you keep the cache warm. I can see in my terminal window that subagents are
working."* He is right on both counts: the host already shows running agents (paying a full
request to repeat that is waste), and as cache warmers the notes are unnecessary because
Claude's own tool-steps reset the timer at every step anyway. Arithmetic: five individual
status notes at ~220k context are roughly **110k token equivalents** — for text the user was
already looking at.

The rule now:

- **During a wave, do NOT report per agent.** If five agents land, ONE summary is written
  when the last one is through.
- **Report on exactly three occasions:** a decision the user has to make · a blocker that
  cannot move without them · a completed milestone.
- **The clock is the exception:** if the user is present and the wave has run nearly an hour
  with no sign of life, send ONE bundled interim note so the cache window doesn't lapse.
- **A single long-running agent** (no fleet) follows the same rule: wait for the result,
  don't comment that it started.

### Stay terminal- and tool-neutral

Some users run a multiplexer, others a plain Terminal/iTerm/Ghostty, VS Code, or a different
agent CLI entirely. Say "your status line", not the name of one particular field; if a
feature exists only in one host (panes/surfaces, a custom status line), mark it as such and
give the generic fallback. The handoff document is the portable artifact — a plain Markdown
file any agent in any tool can read; never encode state in a terminal-specific place instead.
When another agent (Codex/GPT, Gemini) does the work, the SAME rules apply — timestamp,
measured context, handoff, archive — hand it the handoff file, not a chat summary.

## 8. The sweetspot — when to hand off

The threshold is not one number — it depends on what the NEXT stretch of work looks like:

| What comes next | Hand off at |
|---|---|
| A big build/review wave (hundreds of tool-steps) | **~200k** |
| Mixed: some building, mostly discussion | ~250k |
| Only conversation, answers, small edits | **~300k** |
| Anything | **400k = hard ceiling**, never ride past it |

The reason the number moves: cost scales with *tool-steps × context*, and the user's own
messages are a rounding error. 300 work-steps on a 300k context is ~9M equivalents; the same
wave from a fresh 30k session is ~0.9M. Ten quiet exchanges on 300k cost ~0.3M — nothing.
Below ~150k none of this matters, chat freely. Past ~500–600k answer quality also degrades
from sheer information load even while the cache stays warm.

### Calculate the sweetspot and announce it

Yasin's wish, verbatim (25.08.2026): *"Could we calculate the sweetspot and then say: hey,
you've reached your sweetspot, that's why I wrote a handoff, the wave just finished too,
better start a new session — that would be the most elegant thing."*

Two measured numbers suffice:

```
remaining steps in the window ≈ (target context − current context) / growth per step
```

- **Current context**: measured (section 4) — never guessed.
- **Growth per step**: from this session itself. Two data points suffice: context at the
  last handoff, context now, divided by waves/steps in between. In practice: a build wave
  with tests costs roughly 40–80k, a round of conversation 2–5k.
- **Target context**: 200k / 250k / 300k depending on what comes next (table above).

That turns into an announcement the user can actually use — not "your context is big", but
how much still fits:

> "Context 148k, target 200k before the next build wave — that's good for about one more
> wave or a dozen questions. After that I'll write the handoff."

Say it unprompted: at the end of every wave together with the measured context; as soon as
the remaining budget drops below ONE further wave ("that was the last wave for this session,
the handoff is written, start fresh tomorrow"); whenever the user asks where things stand.

**Tone:** short, casual, motivating, never admonishing. "Room for about 2 more waves" is a
streak counter, not an invoice. When the budget gets tight, the practical hint helps too:
"from here on, better to collect longer messages instead of many short ones."

Honest limit: growth per step varies a lot (a screenshot costs more than a text reply). The
estimate is an order of magnitude, not a promise — phrase it that way ("about", "roughly"),
always next to the measured context number.

### Count the startup cost of a fresh session

Yasin's objection, verbatim (25.08.2026): *"You're not accounting for the fact that a new
session starts at 70,000 tokens for me, and that gets multiplied by two because the cache is
rebuilt. So the calculation in our skill isn't perfect yet."*

He was right — the measurement taken right after session start, before a single line of
work, was **82k**, not the "~20k" this skill assumed in several places. Skills, tool schemas,
system prompts and project rules are already loaded before the user does anything; that
figure must be MEASURED per project rather than guessed.

The full calculation has three items, and the cache-write factor hangs on the TTL: **2× for
the 1-hour storage** (Pro/Max default), 1.25× only for the 5-minute one. Cache read stays
0.1×.

```
Rebuild, ONE-TIME       = start context × 2      (1-h TTL; × 1.25 only on 5-min TTL)
Step in the new session = start context × 0.1
Step in the old session = current context × 0.1
Break-even (in steps)   = (start context × 2) / ((old − new) × 0.1)
```

Worked example: start 82k, current 287k → the rebuild costs ~164k once, saving 20.5k per
step → **break-even at ~8 steps.**

**The sentence most often misread:** "steps" are NOT the user's messages, but overwhelmingly
Claude's own tool calls. The rule that actually follows:

- **Only talking / going through the test list / a few small fixes** (< ~6 steps) → STAY,
  even at 260k+. The rebuild would cost more than it saves.
- **A build wave, a review, a migration** (hundreds of steps) → SWITCH as soon as context is
  well above the start context. Break-even arrives around the sixth step; everything after
  that is pure gain.

The sweetspot announcement ALWAYS carries this session's measured start context and the
question "what comes next?" — without both, the recommendation is a guess.

### Count the steps, don't estimate them

Yasin's follow-up (25.08.2026): *"We need to look at how many steps that really is — the
skill should calculate it, know it, and show it to the user."*

Every request stands as a line with `usage` in the session file. This one call produces the
complete sweetspot maths — start context, current context, request count, and the share the
user triggered:

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
z = open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines()
u_all=[]; real_user=0
for l in z:
    try: d=json.loads(l)
    except Exception: continue
    m=d.get('message') or {}
    if m.get('usage'): u_all.append(m['usage'])
    if d.get('type')=='user':
        c=m.get('content')
        if isinstance(c,str): real_user+=1
        elif isinstance(c,list) and not any(isinstance(p,dict) and p.get('type')=='tool_result' for p in c): real_user+=1
k=lambda u:(u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0))/1000
start,now,n = k(u_all[0]), k(u_all[-1]), len(u_all)
save=(now-start)*0.1
fresh=start*2   # 1-h TTL (Pro/Max). On a demonstrable 5-min TTL: start*1.25
print('start %.0fk - now %.0fk - %d requests, %d of them from the user (%.1f steps per message)'
      % (start,now,n,real_user,n/max(1,real_user)))
print('a new session costs ~%.0fk once; saves %.1fk per step; break-even after %.0f steps'
      % (fresh, save, fresh/save) if save>0 else 'context still at start level - stay')
"
```

- **"Requests" is what counts — not the user's messages.** In a real build wave, 205
  requests stood against 15 user messages: roughly 14 steps per message on average, far
  above 100 inside the wave itself, and exactly 1 in conversation rounds. That is precisely
  why a fat context is cheap to TALK on and expensive to WORK on.
- **Break-even in steps** says when switching pays: below it, stay; above it, switch.
- Announce both numbers and the recommendation in one sentence, e.g.: "287k, start was 82k —
  a switch costs ~102k once and pays off from ~5 steps. Going through the test list: stay.
  Next build wave: switch."

This measurement belongs at every wave end and in every answer to "should I start fresh?".

### When to stay vs. when to hand off

| Situation | Recommendation |
|---|---|
| Pause < 1 h ahead, context < 150k | Just continue; optionally keep warm on request (max ~3 cycles) |
| Pause < 1 h, context 150–400k | Continue, but write the handoff now as insurance |
| Big build wave ahead, context > ~200k | Hand off FIRST, then start the wave fresh |
| Only talk/small edits ahead, context < ~300k | Stay — talking on a fat context is cheap |
| Context > 400k | Handoff + fresh session — say so proactively |
| Pause > 1 h (cache gone anyway) | Never rebuild the giant context: handoff + fresh session |
| Mid-session model/effort change wanted | Warn: full cache rebuild; suggest doing it at the next fresh session instead |

### The window as a friendly coach

Present the 1-hour window, the handoff ritual and the test list as POSITIVE motivators, never
as pressure or cost-anxiety. The sliding hour is a natural work rhythm: "answer within the
hour and the wave keeps riding" is the same gentle pull as a streak — it nudges the user to
test delivered items now, dictate answers now, fire the next wave now, while everything is
fresh. The pre-seeded test questions make re-entry effortless (no blank page — cursor after
the marker, speak). Occasionally voice this framing ("window's still warm — perfect moment
for the test list"), and celebrate kept streaks in the logbook rather than only counting
waste.

## 9. What a cache rebuild looks like — and spotting one

- **You cannot see a rebuild in the context counter.** Context size is the same before and
  after — same content, just frozen again. The counter measures size, not cost.
- **Where you DO see it: the 5-hour and weekly usage quota.** A rebuild re-writes the whole
  prefix at cache-write rates, so the quota drops noticeably faster. A lost cache doesn't
  make the context bigger — it makes it more expensive.
- **A short message costs ~1/10 of the WHOLE context — cheap when small, real when fat.** At
  30k, chat freely (near-free, and it resets the 1-hour timer). At 200k+, each exchange is
  ~20k full-price equivalents, and ten quick back-and-forths equal one full context read:
  batch conversation too — ideally ONE long structured message per wave, handoff to handoff,
  answers collected under the test items; short questions only when they can't wait.

Yasin's wish behind the next part: *"when the cache rebuilds, do you notice — and can you
tell the user that it just happened, and why?"* (25./26.08.2026)

**There IS a signal, and it is a hard one.** An earlier version of this skill claimed there
was none — wrong. Every line of the session file carries `cache_creation_input_tokens`
(written at 2×) next to `cache_read_input_tokens` (read at 0.1×). **The ratio of the two sums
IS the hit rate:**

```bash
proj="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"; sess=$(ls -t "$proj"/*.jsonl | head -1)
SESS="$sess" python3 -c "
import json, os
u=[(json.loads(l).get('message') or {}).get('usage') for l in open(os.environ['SESS'],'rb').read().decode('utf-8','ignore').splitlines() if '\"usage\"' in l]
u=[x for x in u if x]
cr=sum(x.get('cache_read_input_tokens',0) for x in u); cw=sum(x.get('cache_creation_input_tokens',0) for x in u)
big=[x.get('cache_creation_input_tokens',0) for x in u if x.get('cache_creation_input_tokens',0)>20000]
print(f'{len(u)} requests · read {cr/1000:.0f}k · written {cw/1000:.0f}k ({cw/max(1,cr)*100:.1f} %) · large writes: {len(big)}')"
```

Reading it: **below ~10 % written/read = the cache was warm.** A single line with a large
write is almost always an APPEND (the conversation grows, the new part gets written once),
not a rebuild. A real rebuild looks different: lots of writing with almost no reading.

**Why this matters — it settles the most common misunderstanding.** Yasin asked on 25.08 and
again on 26.08: "269 requests — does that mean you rebuilt the cache 269 times?" No. Without
this measurement the answer was a mere assertion; with it, it is evidence — in the measured
session, 22,171k read against 562k written, **2.5 %**, and of 147 requests only 6 had a
noteworthy write.

**What still does NOT work:** reading the CAUSE of a miss out of the data — whether the pause
was too long, a model switch intervened, or the server evicted it, the file does not say. For
the cause, use the derivation below; with no established cause, claim nothing.

**What does work, reliably: measuring the gap.** A cache miss by timeout is the most common
cause, and it is derivable from two `date` reads: read `date` in every reply anyway (section
3) — the last time read stands in your own previous text; read again on the next turn.
Difference > 60 minutes (or > 5 minutes if the session is demonstrably in 5-minute mode) ⇒
the cache was gone, and this turn rebuilt it. Then say it ONCE, casually, with cause and
number:

> "By the way: 1 h 40 passed between your last message and this one — the cache expired in
> the meantime and was rebuilt with this turn. No harm done, just so you know why this answer
> cost a bit more than usual."

Other causes Claude can also KNOW for certain, because they were its own action or stand in
the transcript, may be named too: a model or effort switch mid-session, a change to CLAUDE.md
/ the system prompt during the session, an MCP server that restarted (visible as an error).
Causes Claude cannot see (plan limit reached → 5-minute TTL, server-side eviction) are not
guessed at — if none of these is established, say nothing.

Tone: **once per event, not a standing warning**, and never a reproach — the user took a
break, which is their right. The sentence exists to explain ("why did quota just
disappear"), not to educate. The same finding goes into the logbook entry with cause and
estimated waste.

### When does the hour actually start?

The 1-hour timer resets on **every request in the session** — not just the user's messages.
That includes each of Claude's own tool-steps, and each status message Claude emits when a
background subagent finishes. Consequences worth telling the user:

- The hour counts from **Claude's last output**, whichever side produced the last activity.
  "Agent Y finished, here's the handoff" at 16:30 → the user has until ~17:30 to answer
  warmly. Reading costs the user nothing; only their reply is a new request.
- While Claude waits on subagents, its own tool-steps keep the cache warm automatically — no
  dedicated keep-alive is needed during active waves.
- **The other half of the truth: EVERY ANSWER costs too.** A request is a request no matter
  who triggers it — Claude's own reply re-reads the whole context at 10 % (at 220k that is
  ~22k equivalents) and pays for its own output tokens on top, at **five times** the price. A
  300-word answer is ~2,000 equivalents extra. There is no such thing as keeping the clock
  warm for free: every timer reset is a paid request. That is not an argument against
  answering — it is an argument against rambling, and the reason empty interim notes were
  cut.

## 10. Cost visibility tools

### The cost line under every answer

Yasin's wish (26.08.2026, 18:06): *"Could you say with every message you put out what cost
how much — ten per cent, two hundred per cent? Just that token figure, additionally, under
your answers."* And the counter-question right behind it: *"Or does that blow the skill
apart?"* It does not — it is the skill's core: make cost visible instead of talking about it.
But it has a trap you hit immediately when building it.

**The trap:** a measurement needs a tool call, and a tool call IS a request — at 350k context
that is 35k equivalents. Build the cost display naively and you pay more for measuring than
the display will ever save — a thermometer that heats the room.

**The fix:** `~/.claude/ctx.sh` is NEVER called on its own, but appended to a command that
runs anyway — usually the same `date` that supplies the timestamp:

```bash
date "+%d.%m.%Y %H:%M" && ~/.claude/ctx.sh
```

Output (a real line):

```
COST | context 366k · last request: 366k read ×0.1 + 0.4k written ×2
       + 2.9k output ×5 = 52k | session: 265 requests, 9520k
```

Under the answer that becomes one plain-language line:

> *Last measured request: 366k read (×0.1) + 0.4k written (×2) + 2.9k output (×5) ≈ 52k ·
> session so far: 265 requests, 9,520k*

**Two honesty rules, the same as for the clock and the context size:**

1. **All three numbers come from the LAST COMPLETED request** — not from the answer the line
   sits under. The cost of the running answer is only settled once it is finished. Yasin
   asked exactly the right question (26.08.2026): *"Those 2,600 output tokens — were they
   really this answer's?"* No. With read and written you barely notice, since context grows
   by a few per cent per step; with OUTPUT you very much do — a short answer can sit under
   the output figure of a long one. That is why the line is labelled **"last measured
   request"**, not "this round". You COULD estimate the running answer's output from its word
   count (words × ~1.4) — allowed, but mark it as an estimate next to two measurements
   ("≈2.6k estimated").
2. **No measurement this turn, no number** — or an extrapolation of the last state explicitly
   marked with `~`. Never an invented one.

**The line's second job: speak up when a round was unusually expensive** (26.08.2026, 18:17).
Yasin's wording: *"That's the most brilliant part, that at the end you say exactly what I
wanted to see — then the user sees what he has just burned. And if he has burned a lot, you
can point it out: hey, that was silly of you. In some form, quite nicely."*

- **When at all:** only when a round sits well above this session's own average — roughly
  more than twice the running average cost per request, measured from the session file, not
  guessed.
- **The tone is explicitly NOT a telling-off** — name the cause and a concrete cheaper route:

  > "That round was expensive (≈120k) because I read three large files in full — next time a
  > targeted search does the job."

  > "Those five short messages cost ≈180k together, because the context is 350k by now.
  > Collected into one they'd have been ≈37k."
- **The responsibility is almost always the AGENT's, not the user's** — whole-file reads,
  unfiltered command output, over-long answers, per-subagent status notes are things the
  agent stops doing, not the user.
- **At most ONCE per wave**, or the hint becomes nagging.
- **The other direction belongs with it**: a wave that went well gets named too ("the whole
  wave ran through subagents — 40k in the main context for six work packages"). This feature
  motivates, it does not admonish.
- **Left out** in pure interjections and one-liners — a cost line under a three-word sentence
  is noise. Belongs at the end of every substantial answer, at wave end, and in the handoff.

### The per-session cost table

Yasin's wish (26.08.2026, 17:51): *"Couldn't you just make a table where we have everything
per session at a glance — so you can see what cost how many tokens and when? That would be
brilliant."*

Built as `~/.claude/session-costs.sh`. Its unit is deliberately the **stretch between two of
the user's messages** — what a human experiences ("I said something, then something
happened"), not the individual model request, which nobody sees.

```bash
~/.claude/session-costs.sh              # current project, newest session
~/.claude/session-costs.sh --markdown   # just the table, ready for the handoff
```

Example output (a real session):

```
| # | Time  | What it was about              | Req. | Context | read   | written | output | equiv. |
| 1 | 14:05 | Handoff answered …             |  147 | 223k    | 22171k | 562k    | 208k   | 4380k  |
| 6 | 17:22 | So the thing I mentioned …     |   25 | 319k    |  7346k | 108k    |  69k   | 1297k  |
| Σ |       | 10 stretches                   |  246 | 345k    | 49906k | 811k    | 396k   | 8594k  |

Most expensive stretch:  #1 at 14:05 (4380k equivalents, 147 requests)
Requests per message:    24.6 on average
Share of own output:     23 % of total cost
Cache hit rate:          1.6 % written (under 10 % = warm)
```

**How to read it** — Yasin's own questions, verbatim, are exactly why this explanation ships
with the table: *"22,171k — is that 22 million tokens read? What was read there? Why does
line 2 say 241k as context? I don't get this table at all."* See "the conversation is a
book" in section 5 for the underlying mechanism; the arithmetic there closes exactly onto the
`equiv.` column here.

| Column | Meaning |
|---|---|
| **#** | number of the stretch (one stretch = from one user message to the next) |
| **Time** | when the stretch began, in local time |
| **What it was about** | the first words of the message, so the row is recognisable |
| **Req.** | how many model requests that one message set off |
| **Context** | how thick the book was at the END of the stretch — **not a cost column** |
| **read** | requests × book thickness; the largest item, priced ×0.1 |
| **written** | what was newly written into the cache, priced ×2 |
| **output** | what Claude itself wrote, priced ×5 |
| **equiv.** | the three items converted to one price and added up |

**The context column does not add up.** "319k" in a row does not mean that stretch cost
319k — it means the book was 319,000 tokens thick when the stretch ended. It EXPLAINS the
read column: the thicker the book, the more expensive every further request, which is why it
grows steadily while the cost columns jump around.

**A row showing 0 requests is not a bug.** It means that message arrived while work was
already running, got appended to the turn in flight, and triggered no request of its own —
the near-free case from section 6. A zero there is the cheapest row you can get.

The four lines under the table are the actual yield: which wave was expensive, how many
steps one message sets off, what the user's own chatter costs, and whether the cache was
warm at all. **This table belongs in every handoff**, right before the closing context line
— it doesn't replace that single number, it explains it.

**Two things the script does deliberately — easy to get wrong when rebuilding it:** the
session file stores UTC while the user thinks in local time (convert, or the table looks
wrong); and not every line of type "user" is a message from the human — tool results, agent
completion notices and skill loads carry the same type. Without a filter the table
disintegrates into system rows.

## 11. Make the paid quota visible — and use it up

Yasin's wish, verbatim (26.08.2026, 14:03): *"Can you even see whether I still have enough
limit in Codex? Could that be made visible — and could you point it out now and then? If I
have an account I pay for monthly, then the tokens should get used if there are any left. …
That belongs right at the top of the handoff, as the headline information."*

Both numbers are readable, and Claude sees neither on its own.

**Codex/GPT** — the Codex CLI has no usage command, but the server sends a `rate_limits`
block with every response, which the CLI writes into its session file
(`~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`). The last such block is the current state.
Save this as `~/.claude/codex-limit.sh`, `chmod +x` it:

```bash
#!/usr/bin/env bash
# codex-limit.sh — how much of the Codex/GPT quota is used up.
#
# Where the number comes from: the Codex CLI has NO usage command. But the
# server sends a `rate_limits` block with every response, and the CLI writes
# it into the session file under ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl.
# The last such block is the current state.
#
# HONEST LIMIT: the number is only as fresh as the last Codex run. If you
# haven't used Codex for three days, you see a three-day-old state (and it is
# then more likely too high than too low — the window keeps moving). That is
# why the age of the measurement is always printed with it.
#
# Usage:
#   codex-limit.sh          -> one line for humans
#   codex-limit.sh --short  -> compact for the status line ("codex 10%/7d")
#   codex-limit.sh --json   -> raw values

set -uo pipefail
mode="${1:-}"
cache="$HOME/.claude/.codex-limit-cache${mode:+${mode//-/}}"

# Status lines render often — cache the result for 5 minutes.
if [ "$mode" = "--short" ] && [ -f "$cache" ]; then
  age=$(( $(date +%s) - $(stat -f %m "$cache" 2>/dev/null || echo 0) ))
  if [ "$age" -lt 300 ]; then
    cat "$cache"
    exit 0
  fi
fi

# Find the newest session file: scan the most recent day folders instead of the
# whole tree (too expensive on every render). The newest file need not be the
# one carrying a limit block (aborted runs), so keep looking until the first hit.
sess=""
for cand in $(ls -t "$HOME"/.codex/sessions/*/*/*/*.jsonl 2>/dev/null | head -40); do
  if grep -q '"rate_limits"' "$cand" 2>/dev/null; then
    sess="$cand"; break
  fi
done

if [ -z "$sess" ]; then
  [ "$mode" = "--short" ] || echo "Codex: no session data found"
  exit 0
fi

SESS="$sess" MODE="$mode" python3 <<'PY' > "$cache.tmp" 2>/dev/null
import json, os, time

path = os.environ["SESS"]
mode = os.environ.get("MODE", "")
last = None
with open(path, "rb") as f:
    for line in f.read().decode("utf-8", "ignore").splitlines():
        if '"rate_limits"' not in line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        # The block sits nested inside a token_count event.
        stack = [d]
        while stack:
            k = stack.pop()
            if isinstance(k, dict):
                if "rate_limits" in k and isinstance(k["rate_limits"], dict):
                    last = k["rate_limits"]
                stack.extend(k.values())
            elif isinstance(k, list):
                stack.extend(k)

if not last:
    raise SystemExit(0)

measured = os.path.getmtime(path)
age_min = (time.time() - measured) / 60

def window(b):
    if not b:
        return None
    p = b.get("used_percent")
    wm = b.get("window_minutes") or 0
    name = "7d" if wm >= 9000 else ("5h" if wm >= 250 else f"{wm}m")
    rest = ""
    ra = b.get("resets_at")
    if ra:
        s = ra - time.time()
        if s > 0:
            rest = f", reset in {int(s//86400)}d {int((s%86400)//3600)}h" if s > 86400 else f", reset in {int(s//3600)}h"
    return {"percent": p, "name": name, "rest": rest}

p1 = window(last.get("primary"))
p2 = window(last.get("secondary"))
plan = last.get("plan_type") or "?"

if mode == "--json":
    print(json.dumps({"primary": p1, "secondary": p2, "plan": plan,
                      "age_minutes": round(age_min)}, ensure_ascii=False))
elif mode == "--short":
    parts = [f"codex {x['percent']:.0f}%/{x['name']}" for x in (p1, p2) if x and x["percent"] is not None]
    if parts:
        print(" ".join(parts))
else:
    age = f"{age_min/60:.0f} h" if age_min >= 90 else f"{age_min:.0f} min"
    if age_min >= 2880:
        age = f"{age_min/1440:.0f} days"
    print(f"Codex ({plan}): " + " · ".join(
        f"{x['percent']:.0f} % of the {x['name']} window used{x['rest']}"
        for x in (p1, p2) if x and x["percent"] is not None
    ) + f"  [measured at the last Codex run, {age} ago]")
PY

if [ -s "$cache.tmp" ]; then
  mv "$cache.tmp" "$cache"
  cat "$cache"
else
  rm -f "$cache.tmp"
fi
```

**Claude Code** — the 5-hour and weekly percentages exist ONLY in the status line's stdin
JSON, not in the model context. Have the status line drop them on every render. Add these
lines to your `statusLine` command script (`~/.claude/statusline-command.sh` or wherever
yours lives) — the values come from the JSON the status line already receives on stdin:

```bash
input=$(cat)
five=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

# Deliberate side effect: Claude cannot see its own quota percentages — they
# exist only in this stdin JSON. So park them in a file the skill can read.
if [ -n "$five" ] || [ -n "$week" ]; then
  printf '{"as_of":"%s","five_hour_percent":%s,"seven_day_percent":%s}\n' \
    "$(date '+%Y-%m-%d %H:%M')" "${five:-null}" "${week:-null}" \
    > "$HOME/.claude/.claude-quota" 2>/dev/null
fi
```

Claude then simply reads it: `cat ~/.claude/.claude-quota` (e.g.
`{"as_of":"…","five_hour_percent":3,"seven_day_percent":0}`). Here too, the `as_of` timestamp
belongs with the number, and where it disagrees with the web UI (Settings ▸ Usage), the web
UI is the authority.

**What this becomes in the handoff:** a short block **right at the top**, directly after the
three-sentence status, never at the end:

```
## What's left in the tank

- **Codex/GPT:** 10 % of the weekly window used, reset in 5 days
  (measured at the last Codex run, 24 h ago) → 90 % free.
- **Claude Code:** 5h 3 % · week 0 % (as of 14:12).
- **Suggestion:** Codex has plenty of room — the startup-time analysis and
  the 9-hour endurance test are exactly the kind of work for it.
```

Tone: casual and inviting, never admonishing — it is paid quota, not a budget to conserve.
**When a lot is free, PROPOSE something big** — unused quota expires, it does not roll into
next week; the loss is the window closing on it, never the spending. Yasin's own framing:
*"Go on, check everything through, see whether it's any good."* Good candidates, precisely
because they are expensive and never urgent:

- a full pass over the whole project at HIGH reasoning effort ("ultrathink") — architecture,
  dead code, inconsistencies;
- a quality check of an entire area against its acceptance criteria, not just the last diff;
- a large second-opinion analysis on a different model (Codex/GPT) — a different
  architecture sees different mistakes than a re-read by the same one;
- a long test run nobody wants to sit through: startup times, endurance runs, a full matrix.

Phrase it as an invitation with the number attached: *"90 % of the week is still free — this
is the moment for the big review, it'll never be cheaper than on quota you've already paid
for."* Never: "you should use your quota more." And if a quota is nearly exhausted
(> ~85 %), that belongs in the same block with the reset time next to it — then the message
is "until tomorrow morning, better stick to the small stuff", the same information from the
other side.

### Wake-up ping for the Codex readout (27.08.2026)

His request, after `codex-limit.sh` came back with nothing but `{"primary": null,
"secondary": null, "plan": "plus", "age_minutes": 107}` on an otherwise quiet day: *"Yes,
please build that in. Into the skill too. Into the GitHub warm-handoff too."*

**The problem:** `codex-limit.sh` reads quotas out of the LAST Codex session file, so the
number is only as fresh as the last run — if that was hours ago, the script shows either a
stale state or, as above, none at all. **`null` does not mean "0 % used"** — it means "no
fresh `rate_limits` block has arrived since the last run, the value is unknown." Printing a
zero would be a fabrication, the same trap as guessing the clock or the context size.

**The fix:** fire one tiny Codex call per session so the server sends back a fresh
`rate_limits` block:

```bash
codex exec --skip-git-repo-check "Reply with just: ready"
```

- **When:** once per session, at the start — piggybacked onto a call that would run anyway
  (e.g. the session's first real Codex task), NEVER as its own separate call made purely for
  the measurement.
- **Cost, stated honestly:** this burns a few Codex tokens — negligible against a paid weekly
  quota, but not zero. Hence: hang it off a call that's due anyway.
- **If Codex isn't installed or logged in:** proceed silently, no error — the ping is a bonus
  for the readout, not a required step.
- After that, `codex-limit.sh` shows the fresh state, and the "X h ago" in the handoff block
  matches reality again.

### Codex, Gemini and OpenRouter as one picture (27.08.2026)

His instruction once the wake-up ping was in place: *"No, that's great, do it."* Meaning: see
all THREE quotas as ONE picture, not just Codex.

**The shared core: on all three, what goes unused simply expires.** Codex on a paid plan runs
out on a weekly window regardless of use. Gemini hands out free requests that expire on the
same kind of window. OpenRouter offers free models too (Yasin uses "Ox Alpha" there as a
second reviewer, among others) — an unused request there is not credit toward next time
either, it is simply gone. Same stance as with the Claude quota: don't conserve it, use it up
while the window runs.

**Assignment — which work suits which provider:**

| Work | Provider | Why |
|---|---|---|
| Large read/analysis/review passes, sweeping a whole project | Codex or OpenRouter | A different architecture sees different mistakes; expensive and rarely urgent — exactly what expiring quota is for |
| Second opinion on Claude's own code or answer | Codex or OpenRouter (e.g. Ox Alpha) | The no-self-review rule — Claude must not grade its own homework |
| Changes IN the code | Claude | Stays in the driver's seat, knows the history and the decisions |
| Research, very long contexts | Gemini | Built for exactly that — a large context window |

**How to see the state:** Codex via `~/.claude/codex-limit.sh` (above), fresh after the
wake-up ping — shows percent of the 7-day window plus reset time. Gemini and OpenRouter: no
script and no reliable reading exists — no balance gets invented. Say so plainly: *"For
Gemini/OpenRouter I can't read the quota state, only show the usage hint in each provider's
own interface."* A `~` or an estimated percentage here would be the same fabrication as with
the clock or context size — left out on purpose rather than guessed.

Tone: inviting, with the number attached where one exists, never admonishing. When Codex has
plenty free, name it AND propose a fitting candidate right away ("90 % of the week still
free — that would be the moment for the big second-opinion pass with Ox Alpha or Codex"). For
Gemini/OpenRouter it stays an invitation without a number.

## 12. The handoff document

### The wave workflow (the heart of this skill)

- **The user batches work into waves**: one big message with many tasks. Claude works
  through it (subagents welcome — they cache separately at 5 min, so batch their jobs too).
  During the wave the cache stays warm by itself; short back-and-forth in between is cheap —
  small side-topics are *encouraged* while the main work runs.
- **After each wave, Claude writes a handoff document**: a dated Markdown file
  (`_handoff-<project>-YYYY-MM-DD[-b].md`) with what was delivered, running state, open
  items, project constraints — **and the current test checklist at the bottom**.
  **Pre-seed every test item with an answer line**, ready to dictate into:

  ```
  ## T3 — Dark/light toggle inverted
  <test description>

  >>>Answer:
  ```

  (Use the user's language for the marker — e.g. `>>>Userantwort:` for a German user.) The
  user just places the cursor after the marker and speaks. An item whose answer line stays
  empty simply wasn't tested yet — information, not an error.
- **The user works in the handoff file with a plain text editor** (TextEdit or similar), not
  the chat box: chat inputs collapse long pastes into `[pasted text]`, losing overview; in
  the editor the user sees the whole document. **Rule: save (⌘S) before telling Claude to
  read it** — unsaved editor changes are invisible on disk.
- **The next session starts with only the handoff** — a fresh, small context instead of
  500k+, fully briefed, cache rebuilt once at minimum size. **Do not promise "~20k": measure
  it** (in the Aitomat project that floor was 82k — section 8). Claude reads the annotated
  test answers and new ideas from the file and starts the next wave.

**The PATH goes RIGHT AT THE TOP of the document, first, before anything else** — the file
path is nowhere visible in the editor, so every handoff starts with a ready-made handover
sentence to copy, absolute path, no tilde, in backticks so a double-click grabs it whole:

```
> **For the next session — copy and paste this line:**
> `I've answered the handoff: /Users/…/project/_handoff-project-2026-08-25.md`
```

**The project name belongs in the file name.** Parallel sessions can produce handoffs on the
SAME day; `_handoff-2026-08-24-b.md` is then ambiguous. Rule: every handoff file name carries
the project name (`_handoff-myproject-2026-08-24-b.md`), same for the `# Title` line inside
(`# Handoff myproject — 24.08.2026, 23:40 (wave 9 B)`) and the logbook entry. The suffix
`-b`, `-c` … stays for the second/third handoff of one day within the same project.

**Three fixed blocks at the very bottom, in this order:**

1. **A free field for the user** — a short closing sentence marking the end of the Q&A/test
   part, inviting anything that came up outside the list:

   ```
   ---
   ## That's the end of the questions, answers and tests.

   Space for everything else — new instructions, ideas, tips, tasks
   that occurred to you:

   >>>Answer:
   ```

   Without it, anything not covered by a test question has no home and gets lost between
   waves.

2. **Context state + "the next wave starts fresh"**, as the last line:

   ```
   *Context of this session: ~285k. The next wave starts fresh out of exactly
   this handoff — nothing is lost.*
   ```

   Use the actually measured number; no measurement → no number, not a guessed one — and
   don't promise a fresh-session size that wasn't measured either.

3. **A collection area for the running session**, last of all:

   ```
   ---
   ## Collection for the next handoff

   Anything that occurs to you during the running wave goes in here.
   I won't touch this section — I only read it when I write the next
   handoff.

   >>>
   ```

   Yasin's reason, verbatim: *"Once I've handed you a handoff, new things occur to me while
   you're working and I want to collect them … otherwise I have to open a new TextEdit
   document, collect there, and then copy-paste."*

   **The accompanying rule is hard: Claude NEVER writes into a handoff the user is currently
   writing in.** A new handoff is always a NEW file; the old one stays word for word as it
   was left — the source of a second complaint (*"then the document says unsaved changes,
   and suddenly my collection is gone"*): if Claude edits a file that's open in the editor,
   the versions collide; if the active file is never written to, that cannot happen. When
   writing the next handoff, the collection area is read like the test answers — every point
   answered or absorbed into the roadmap.

   **And read the SECOND-TO-LAST handoff again too.** Yasin's wish (25.08.2026, 14:14):
   *"Before the new handoff, check whether anything was added to the old handoff, and mention
   only those changes in the new one."* Reason: the user keeps collecting AFTER handing the
   handoff over, and those lines would otherwise be recorded nowhere. Procedure:

   1. Read the handoff just answered (as always).
   2. Additionally the one before it — only its "Collection for the next handoff" section.
      Anything there that doesn't appear in the current handoff is new.
   3. Those points go right at the top of the new handoff, under a heading like "Taken over
      from your collection" — one line per point saying what happened to it (answered /
      built / landed in the roadmap).
   4. Only then does the old handoff move to the archive.

### Claude does NOT close the old handoff any more (26.08.2026)

This rule went through two rounds, both paid for with real data loss.

Round one (Yasin, 25.08.2026, 14:21): *"Earlier I had already written something new into the
old handoff list that you closed automatically … and now it's gone, because you closed it."*
A check that does not stand immediately before the action is worthless — the unsaved-changes
guard had run minutes earlier, the close came later, and he had kept writing in between.

Round two (Yasin, 26.08.2026, 14:07) went further: *"If I write something at the bottom and
haven't saved it yet, and you then close the old handoff after you've finished working — you
can't close it at all if I still have unsaved changes in there. So I'd almost say: don't
close the old handoff at all, leave it open, let the user close it."* The reason is more
fundamental than the data loss: the collection area exists precisely so he can keep writing
DURING the running wave — the moment Claude finishes and wants to tidy up is exactly the
moment unsaved text is most likely sitting there.

The rule now:

1. **The old handoff stays open. Full stop.** Claude does not close, save or touch it. The
   user closes it themselves when done.
2. **Its content is still read before the new handoff is written** — collection area
   included, via the unsaved-changes guard so unsaved lines arrive too.
3. **The new handoff is ALWAYS a new file** with a new name — no collision is possible
   between Claude's version and what's open in the editor.
4. **Archiving (`mv`) only happens once the user has closed the document** — or not this
   wave at all; the new handoff notes in one line that archiving is still pending.
5. **Close + reopen remains exactly ONE exception:** when Claude itself changed the file the
   user has open. Even then the check happens in the SAME call, and on `modified: true` it
   is NOT closed but asked about.

When in doubt: **better one window too many open than one line of the user's gone.** When
Claude finishes a handoff it says so and explains the loop once: *"Handoff written, your test
list is at the bottom. Answer under the test points, add new ideas, ⌘S — and give the file to
a fresh session (or to me, if you're still in the window)."*

**Carry the old test list forward.** When writing a NEW handoff while an older one exists:
read it first and check its answer lines. Answered items get incorporated, and the new
handoff says so explicitly per item ("Your T1 answer from the previous list is taken into
account: <summary> — correct?"), so the user can veto a misreading. Unanswered items and
items needing a re-test move into the new list unchanged, marked as carried over. The old
handoff stays untouched as the record; only the newest one is the active working document.

### Editor integration (macOS)

**Open every user-facing document automatically** — handoffs, plans, reports, checklists —
right after writing, so the user *sees* it's ready instead of hunting for a path: `open -a
TextEdit <file>` (always name the editor explicitly; the system default for `.md` is often an
IDE or preview app the user doesn't want). Windows: `notepad <file>`; Linux: `xdg-open
<file>`.

**Open as a tab, not a new window.** Offer once to run `defaults write -g
AppleWindowTabbingMode always` so new documents open as tabs in the existing TextEdit window
(reversible with `defaults delete -g AppleWindowTabbingMode`, or via System Settings ▸
Desktop & Dock). Mention it's system-wide; revert if the user dislikes it. Caveat: tabbing
only joins windows on the SAME Space — if the main TextEdit window lives elsewhere, macOS
opens a separate window anyway; fallback is merging via the menu (needs Automation
permission; try the localized title first):

```bash
osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Alle Fenster zusammenführen" of menu "Fenster" of menu bar 1' \
|| osascript -e 'tell application "System Events" to tell process "TextEdit" to click menu item "Merge All Windows" of menu "Window" of menu bar 1'
```

If double-clicking `.md` opens the wrong app, offer the fix via
[duti](https://github.com/moretension/duti): `brew install duti && duti -s com.apple.TextEdit
.md all`.

**Every such document gets a short header**, in the user's language:

```
> You can comment directly in this file — start the line with >>> or with your
> name + timestamp, e.g. "J. Doe, 2026-08-22 14:40:".
```

The marker is a convention, not a syntax — `>>>` is only the default; a name + timestamp
prefix is even better once several annotation rounds pile up. **Claude infers the user's
marker from the document itself**: whatever consistent prefix appears on the answer lines is
the user's voice. (Tip to offer once, macOS: there's no built-in dynamic timestamp — Text
Replacements only inserts static text; a live snippet needs a text-expansion tool.)

**Unsaved-changes guard (macOS).** Claude reads files from disk, so unsaved editor changes
are invisible — but on macOS it can check for them before reading an annotated handoff:

```bash
osascript -e 'tell application "TextEdit" to get {name, modified} of documents'
```

If `modified: true`: *"Your handoff has unsaved changes — shall I take them over?"* and on
confirmation either save it (`osascript -e 'tell application "TextEdit" to save (first
document whose name is "<file>")'`) or read the live text directly (`… to get text of (first
document whose name is "<file>")`). Requires one-time macOS automation permission for
TextEdit. This turns ⌘S from a hard requirement into a safety net — but still teach ⌘S,
since the guard only sees documents open in TextEdit.

**Open documents LARGE — fix the font default, not the zoom.** TextEdit opens plain text
tiny (default 11 pt) and its per-window zoom is NOT scriptable, so Claude cannot restore it
on reopen. The durable lever is the default plain-text font size:

```bash
defaults read com.apple.TextEdit NSFontSize          # unset = 11 pt
defaults write com.apple.TextEdit NSFontSize 18
defaults write com.apple.TextEdit NSFixedPitchFontSize 18
```

Offer once (~18 pt, adjust on feedback; reversible with `defaults delete`). Already-open
windows keep their old size until the user quits and reopens TextEdit (never quit it for
them). Pairs with the narrow-line rule below. Warn once, when closing + reopening a document
to reload it, that per-window zoom is lost.

**Reload edited documents — every time, unprompted.** TextEdit does not live-reload files
changed on disk. Whenever Claude (or a subagent) edits a document the user has open, run the
unsaved-changes guard on exactly those files: unmodified → close and reopen so the user sees
the new version; modified → do NOT close — tell the user which edits collide, offer to merge,
reload only after they confirm. Skipping this leaves the user reading a stale document while
believing it's current.

**Tip for lost handoffs** (tell the user once): TextEdit ▸ File ▸ Open Recent brings back any
recently closed handoff without hunting through Finder.

**Keep lines narrow.** Users often park the editor beside their terminal on a split screen
and bump the font size — long lines then wrap unpredictably. Hard-wrap prose at roughly
**60–70 characters**; narrower is better. Exception: commands, paths and URLs stay on one
line however long, so a triple-click copies them whole. After the first document, ask once
whether the width suits and remember the preference.

### Writing the handoff well (rules adopted from Matt Pocock's /handoff)

- **Reference, don't copy.** Specs, plans, commits, diffs and issues already written down get
  linked by path or URL — never pasted in. Keeps the file small and the settled detail in ONE
  place instead of two that drift.
- **Redact secrets** (keys, tokens, passwords) before writing the file.
- **Name suggested skills** for the next session.
- **A map, not just a to-do list.** Every handoff gets a short **"Main documents"** block
  right before the roadmap: the 3–6 files that actually carry the state, each with an
  absolute path and one line on content and freshness:

  ```
  ## Main documents (where things are written down)

  - `/Users/…/project/ROADMAP-MASTER.md` — plan for all waves (as of 23.08.)
  - `/Users/…/project/PROJECT-STATUS.md` — what's done / in progress (as of 25.08.)
  - `/Users/…/project/OPEN-TOPICS.md` — topic store, coarser than the list below
  ```

  Only list documents that REALLY exist (check first), mark outdated ones explicitly instead
  of quietly dragging them along, and never copy content in.
- **The lower part is a narrative thread, not a keyword list.** Yasin's wish (25.08.2026):
  *"down there I don't just want the questions and tests, but a thread you can see,
  roadmap-like — what the next wave is, what the one after that is, short, with a couple of
  details, so you remember and feel motivated to add something."* So the to-do list "Open
  (next waves)" becomes a short **roadmap with answer fields** — one paragraph per each of
  the next two or three waves, what's coming and why, plus the same invitation as the tests:

  ```
  ## The thread — what comes next

  ### Next wave: live transcript under the HUD
  The text should run along during recording, with an interim state every
  5 minutes. Hangs off your 5-hour video plan; the audio side has been
  secured since wave 10, only the text is missing.

  >>>Anything to add here?

  ### The wave after: read-aloud, part 2
  Right-click service, read-aloud state in the HUD, speed, loading more voices.

  >>>Anything to add here?
  ```

  The long enumeration of all open points stays below it as a compressed topic store without
  answer fields — the roadmap is the invitation to think along, the list is the memory.
- **Archive old handoffs, never delete them.** Once a new handoff is written and its answers
  incorporated, the PREVIOUS one moves into a `handoff-archive/` subfolder (create if
  missing):

  ```bash
  mkdir -p "<project>/handoff-archive"
  mv "<project>/_handoff-project-2026-08-24-b.md" "<project>/handoff-archive/"
  ```

  Move, don't delete. The project folder then always holds exactly ONE active handoff, so
  "which is the right one?" never comes up; the new handoff names the archive folder in one
  line. Only archive when the old document has no unprocessed answers left (otherwise state
  the reason and leave it), and only once the user has closed it in the editor.
- One deliberate difference from Pocock: he writes handoffs to the temp directory and
  recommends `/compact` for same-directory continuation. This skill writes them **into the
  project** (dated, part of the working rhythm, the user annotates them) and prefers handoff
  + fresh session over `/compact` past the context threshold — on subscription plans,
  `/compact` keeps the huge expensive prefix alive; a fresh small session does not.

## 13. Dictating into the terminal

**Terminals collapse long input into a placeholder.** Past a certain length many terminals
show only `[pasted text]` — the user then can't see, skim, correct or re-find what they
actually said. A long dictation is effectively sent blind. From which follows the division
of labour this skill recommends anyway, now with the concrete reason:

- **Short messages belong in the terminal**: one question, one assignment, one correction —
  short enough to stay visible as text.
- **Everything long belongs in the handoff document**: test answers, ideas, braindumps,
  criticism. There the user sees every word, can keep working for days, add and rearrange —
  and the agent reads the whole document at once, at the end.

This is not a compromise, it's the better route: a handoff may grow for weeks until full,
then a fresh session, document in, off you go. Say this to the user ONCE per setup, not on
every long message.

## 14. Honesty rules

- There is no background timer: Claude only acts when a request arrives. That is exactly why
  the handoff is written *proactively at the end of a wave*, not "when the hour is nearly up".
- Cost claims are shown as arithmetic when it matters (cache-write vs. re-read pricing), not
  asserted.
- Numbers are measured, never felt: context size, request count and cache hit rate all come
  from the session file or the status line — never from an impression.
- A cache rebuild is reported when it is DERIVABLE (section 9) — never guessed.

## 15. The logbook (self-observation, optional but recommended)

Keep a running log at `~/.claude/warm-handoff-log.md`. **Append one line at every handoff**
(and whenever a cache-relevant event happens):

```
| 22.08.2026 14:40 | ctx 85k | 147 req | write/read 2.5% | 2 waves | rebuilds: 1 (pause 90min, no handoff) | est. waste ~60k tokens |
```

Log-worthy events: session start/end context size, request count and the write/read ratio,
waves completed, every cache rebuild **with its cause** (pause > 1h, mid-session model/effort
switch, MCP restart, prefix change), warnings the user overrode, and a rough token-waste
estimate for each avoidable rebuild.

**Every ~50 entries:** write a short summary block at the top — recurring patterns and
concrete recommendations ("6 of 8 sessions lost the cache to a >1h pause without a handoff,
costing roughly X — schedule the handoff before breaks"; "effort was switched mid-session 3
times despite warnings"). Then continue logging below it.

Honest limits: there is no background telemetry — the log only covers sessions where this
skill is active, and waste numbers are estimates, clearly labeled as such. That is enough for
pattern-spotting, which is the point.

## 16. Make it always-on (recommended setup)

Add one line to your global `~/.claude/CLAUDE.md` (or the project's `CLAUDE.md`):

```
At the start of every session, invoke the warm-handoff skill.
```

Then you never need to type `/warm-handoff` — the session opens with the timestamp habit,
the thresholds, the measurement calls and the wave workflow already active.
