# HANDOFF FOR CODEX — the checklist to work through

Whoever writes a handoff — Codex, Claude, or a guardian — works through this page
top to bottom. It is a short form, not a replacement: the binding texts are
[SKILL.md](SKILL.md), [handoff format](references/handoff-format.md),
[RTF on macOS](references/rtf-macos.md) and
[wave execution](references/wave-execution.md).
German edition: [HANDOFF-FÜR-CODEX.md](HANDOFF-FÜR-CODEX.md).

## 0. Hard rules — tick every box

A Codex lead has skipped exactly these before. The checklist is in the
[Codex adapter](references/codex.md) (rule CDX-05); in short:

- [ ] Timestamps from `date`, never estimated.
- [ ] First line = absolute path of the document, second line = as-of time.
- [ ] New handoff directly in the archive folder; never moved, never overwriting an answered one.
- [ ] One inbox: handoff footer until wave start, then the interjections file.
- [ ] Open [handoff format](references/handoff-format.md) in full first.
- [ ] Read the predecessor unfiltered, first line to last.
- [ ] Bundle at wave end: build, install, push, handoff — in one pass.

## 1. Read everything first — never guess the source

- The **named** predecessor handoff, not the one with the newest timestamp.
- The RTF answers: `textutil -convert txt -stdout FILE.rtf`.
- The Zwischenrufe (interjections) file and the chat steering messages.
- **Only the saved state counts. Cmd-S is the user's release within existing authorization.** Text left
  unsaved in an editor has not been read: ask for the save, or mark the gap
  explicitly as a gap. Never save, close, or recreate the user's answer file in
  order to read it.
- `[Pasted text]` / `Pasted Content` is **not content**. Open the referenced
  file; if it is missing, leave that input explicitly open.
- Preserve user originals verbatim; put interpretation and replies in separate
  sections.
- **Read it unfiltered (2026-09-14).** Read the predecessor handoff from the
  first line to the last. Never truncate long lines, never grep only for
  `>>>Userantwort:`, never filter "to save tokens" — that is exactly how the
  through line, roadmap, measurement, main documents, memory, and logbook once
  vanished from the successor revision. Read oversized files in blocks, but
  completely.
- **Open the reference** before writing: `references/handoff-format.md` in the
  skill repo (rules HF-05 and HF-06). "I know the format" does not count.

## 2. The required blocks, in this order

1. **Header:** line 1 the document's own absolute path, line 2 `Stand:` from
   `date`, then the **copy line** as one unbroken line pointing at the new
   editable answer file: `Ich habe das Handoff bearbeitet: /absolute/path/new.rtf`.
   Then the title **carrying the file's own revision ID** (`…-r.md` → title names `r`), measured time with time zone, predecessor, and a note
   about the `>>>` answer fields.
2. **State in three sentences** — objective, verified state, next action; plus
   mode (interim / resumable / complete) and the authorization in force.
3. **Remaining budget** — measurement source, age, scope; otherwise "not measured".
4. **Expected agent results** — ID, owner, observed status, worktree/branch/base,
   report path, known runtime limits.
5. **New user input since the predecessor (verbatim, HF-08)** and **what I did
   with it** — every new original mapped to a status and evidence. Older originals stay linked in the archived predecessor; every still-open older wish appears under "Running and pending" with its source.
6. **Previous test answers — what came of them** and **test list vN** with empty
   `>>>Userantwort:` fields. No open test counts as passed.
7. **Questions for you** with `>>>Antwort:`; keep optional questions apart from
   the decisions that actually block the next step.
8. **The through line**, **short roadmap**, **measurement of the wave** (numbers,
   what went wrong, what it cost, lessons), **main documents**, **further
   documents**, **active tools of this project** — real paths, actual
   availability.
9. **Memory** — four to six concrete long-term and short-term points each.
10. **Cost table** — source, age, main/worker shares, measurement gaps.
10b. **Logbook** — what actually happened in this wave, with timestamps.
11. Last of all, **collection for the next handoff** with origin path and `>>>`.

**Exactly ONE active collection / Zwischenrufe inbox**, and it switches with the
wave clock (user 2026-09-14): between handoff and wave start the RTF footer
`SAMMLUNG FÜR DAS NÄCHSTE HANDOFF` is the only inbox — the Zwischenrufe file is
**not** created together with the handoff. It comes into being at wave start and
is then the only inbox until the next handoff. Two parallel inboxes have already
swallowed answers.

**Do not wait, close out.** At the end of a wave do not wait for one more agent
report: write the handoff, open it, push, report. Outstanding reports belong
under "running and pending"; they do not hold up completion.

At wave start, create and open the interjections file as `.md` in the project root, never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it. Follow HF-07.

Worker briefs keep applicable user rules binding; a lead must not silently disable them. Record any conflict with host permissions. Wave numbers share one project-wide sequence across hosts; reserve the next unused number in the saved plan (WV-01).

## 3. The four scripts

Always use them; never rebuild them by hand.

| Script | Purpose | Call |
| --- | --- | --- |
| [`handoff-rtf.sh`](scripts/handoff-rtf.sh) | Markdown → RTF twin: clickable link fields, 18 pt, gold answer paragraphs | `scripts/handoff-rtf.sh docs/handoff-new.md /project/handoff-new.rtf --project-root /project` |
| [`handoff-inputs.py`](scripts/handoff-inputs.py) | Snapshot of the saved sources with hash and timestamp before reading and writing | `python3 scripts/handoff-inputs.py …` |
| [`handoff-pruefen.py`](scripts/handoff-pruefen.py) | **Required before and after rendering:** path and as-of lines, revision ID in the title, copy line, self-references in the header, HF-06 section order; with an RTF twin also its header | `python3 scripts/handoff-pruefen.py docs/handoff-new.md` |
| [`sammlung-pruefen.sh`](scripts/sammlung-pruefen.sh) | **Required step before finalizing:** requires the immediate predecessor's final collection footer verbatim, checks the reference to its answer fields, and reports answers repeated verbatim (HF-08) | `scripts/sammlung-pruefen.sh docs/handoff-new.md [prev.rtf]` — pass answered predecessors as the saved RTF |

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
- Behind `>>>`, pasted and typed text stays black on gold at 18 pt, including continuation and the document default. Agent text resets the background; exact control words and evidence scopes are in RT-03/RT-03b of the RTF reference linked above. Interjections stay `.md`.
- **Archive answered handoffs in `handoff-archiv/`** of the same project
  (`mv`, never `rm`; user 2026-09-13 03:31).
- After generating, `grep -c "file://" FILE.rtf` must be > 0 as soon as the
  document contains local references.
- Roundtrip and hyperlink verification run automatically. They do **not** prove
  readability, link clicks, or paste behavior in another application — keep those
  three evidence scopes apart and name what stays open.
- Regressions: `TMPDIR=/tmp python3 -m unittest discover -s tests -v`.

## 5. Before handing over

- `handoff-pruefen.py` and `sammlung-pruefen.sh` have run and are clean.
- All sources rechecked for late additions; originals reconciled point by point.
- Local links checked; real commit/push evidence in the report, no invented hashes.
- Only owned paths changed.
- For wave work: own wait loops and background processes ended, expensive builds
  behind the shared project lock, one build per topic guardian at the very end.
  See [wave execution](references/wave-execution.md).
- Open remainders named explicitly instead of quietly counted as done.
