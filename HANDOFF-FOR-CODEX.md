# HANDOFF FOR CODEX — the checklist to work through

Whoever writes a handoff — Codex, Claude, or a guardian — works through this page
top to bottom. It is a short form, not a replacement: the binding texts are
[SKILL.md](SKILL.md), [handoff format](references/handoff-format.md),
[RTF on macOS](references/rtf-macos.md) and
[wave execution](references/wave-execution.md).
German edition: [HANDOFF-FÜR-CODEX.md](HANDOFF-FÜR-CODEX.md).

## 1. Read everything first — never guess the source

- The **named** predecessor handoff, not the one with the newest timestamp.
- The RTF answers: `textutil -convert txt -stdout FILE.rtf`.
- The Zwischenrufe (interjections) file and the chat steering messages.
- **Only the saved state counts. Saving is the user's release.** Text left
  unsaved in an editor has not been read: ask for the save, or mark the gap
  explicitly as a gap. Never save, close, or recreate the user's answer file in
  order to read it.
- `[Pasted text]` / `Pasted Content` is **not content**. Open the referenced
  file; if it is missing, leave that input explicitly open.
- Preserve user originals verbatim; put interpretation and replies in separate
  sections.

## 2. The required blocks, in this order

1. **Copy line at the very top**, one unbroken line pointing at the new editable
   answer file. Then title, measured time with time zone, predecessor, and a note
   about the `>>>` answer fields.
2. **State in three sentences** — objective, verified state, next action; plus
   mode (interim / resumable / complete) and the authorization in force.
3. **Remaining budget** — measurement source, age, scope; otherwise "not measured".
4. **Expected agent results** — ID, owner, observed status, worktree/branch/base,
   report path, known runtime limits.
5. **Your collection from the last handoff (copied verbatim)** and **what I did
   with it** — every original mapped to a status and evidence.
6. **Previous test answers — what came of them** and **test list vN** with empty
   `>>>Userantwort:` fields. No open test counts as passed.
7. **Questions for you** with `>>>Antwort:`; keep optional questions apart from
   the decisions that actually block the next step.
8. **The through line**, **main documents**, **further documents**, **active
   tools of this project** — real paths, actual availability.
9. **Memory** — four to six concrete long-term and short-term points each.
10. **Cost table** — source, age, main/worker shares, measurement gaps.
11. Last of all, **collection for the next handoff** with origin path and `>>>`.

**Exactly ONE active collection / Zwischenrufe inbox.** Either the RTF footer or
the agreed Zwischenrufe file; the other place only links to it. Two parallel
inboxes have already swallowed answers.

## 3. The three scripts

Always use them; never rebuild them by hand.

| Script | Purpose | Call |
| --- | --- | --- |
| [`handoff-rtf.sh`](scripts/handoff-rtf.sh) | Markdown → RTF twin: clickable link fields, 18 pt, gold answer paragraphs | `scripts/handoff-rtf.sh docs/handoff-new.md /project/handoff-new.rtf --project-root /project` |
| [`handoff-inputs.py`](scripts/handoff-inputs.py) | Snapshot of the saved sources with hash and timestamp before reading and writing | `python3 scripts/handoff-inputs.py …` |
| [`sammlung-pruefen.sh`](scripts/sammlung-pruefen.sh) | **Required step before finalizing:** compares the `>>>` lines of the predecessors with the new handoff and names what is missing | `scripts/sammlung-pruefen.sh docs/handoff-new.md [prev1.md] [prev2.md]` |

For the open Zwischenrufe file also use
[`zwischenrufe-antwort.sh`](scripts/zwischenrufe-antwort.sh): **append only**,
never write into the middle, never close it unasked.

`sammlung-pruefen.sh` is a heuristic, not a completeness proof. Reconcile answers
outside recognized sections point by point as well.

## 4. The RTF twin

The Markdown is the agent source; the **RTF is the file the user answers in**.
Full detail in [RTF on macOS](references/rtf-macos.md).

- Always produce RTF through `scripts/handoff-rtf.sh`. Direct `textutil` is for
  reading and checking only, never for generating.
- The renderer **refuses any existing target**, symlinks included. A new version
  gets a new file name; the answered file stays untouched.
- Pass `--project-root` when the project root is known.
- **Gold is mandatory, including as the document default.** `>>>` paragraphs and
  `user-original` blocks are gold; beyond that the document default itself is
  18 pt gold, so **pasted and typed text** in an answer field is 18 pt gold too
  instead of falling back to 12 pt with no background. Agent text, headings and
  code blocks reset with `\pard\plain\f0`. The same gold rule applies to the
  **Zwischenrufe RTF**, not only to the handoff.
- After generating, `grep -c "file://" FILE.rtf` must be > 0 as soon as the
  document contains local references.
- Roundtrip and hyperlink verification run automatically. They do **not** prove
  readability, link clicks, or paste behavior in another application — keep those
  three evidence scopes apart and name what stays open.
- Regressions: `TMPDIR=/tmp python3 -m unittest discover -s tests -v`.

## 5. Before handing over

- `sammlung-pruefen.sh` has run and is clean.
- All sources rechecked for late additions; originals reconciled point by point.
- Local links checked; real commit/push evidence in the report, no invented hashes.
- Only owned paths changed.
- For wave work: own wait loops and background processes ended, expensive builds
  behind the shared project lock, one build per topic guardian at the very end.
  See [wave execution](references/wave-execution.md).
- Open remainders named explicitly instead of quietly counted as done.
