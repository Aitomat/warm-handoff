# Handoff Format

<!-- rule:HF-01 -->
## New revision, clear entry point

Create a new dated file for every handoff. Never overwrite an answered source. Put a copyable first line with the absolute path of the new file. In the RTF twin that first line is the RTF's own absolute path as a link; the Markdown path does not appear there (`scripts/handoff-rtf.sh` swaps it; user 2026-09-28 02:52). The Markdown keeps its own path. Include project, date, and revision in the title.

**Read only the saved state.** Saving is the user's release; text left unsaved in
an editor has not been read. Ask for the save, or mark the gap explicitly as a
gap — never save, close, or recreate the user's answer file in order to read it.

**Keep exactly one active collection inbox**, the single place where the user
answers and interjects: either the answer file's collection section or the agreed
interjections file. The other location only links to it. Two parallel inboxes lose
answers.

<!-- rule:HF-02 -->
## Required sections

1. **Preserved user input:** the complete verbatim collection of what is new since the previous revision, without interpretation; older originals by link only (HF-08).
2. **Objective and authorization:** desired outcome, allowed and prohibited actions, and file ownership.
3. **Verified state:** branch or HEAD, changed files, passing checks, and evidence paths.
4. **Running and pending:** started work, dependencies, unknown state, and real blockers.
5. **Decisions and questions:** only points requiring user choice; put `>>>User answer:` and one blank gold answer paragraph under each question.
6. **Acceptance:** short reproducible steps, expected result, and manual checks that remain unverified.
7. **Memory:** a few durable rules and session-specific next steps, kept separate.
8. **Collection for the next handoff:** a distinct verbatim user area at the end.

<!-- rule:HF-03 -->
## Separate originals from interpretation

Use `<!-- user-original:start -->` and `<!-- user-original:end -->` when the renderer must protect a verbatim block. Change neither spelling nor order inside it. Put agent replies, decisions, and summaries outside. A byte archive may additionally preserve the unchanged source; the readable snapshot does not replace it.

<!-- rule:HF-04 -->
## Completion requires evidence

Call work complete only when an artifact, commit, status, or test proves the result. “Started,” file existence, and agent reports are not final evidence. For an open manual check, name the exact remaining step.

Archive answered handoffs in `handoff-archiv/` of the same project, created if missing, and move them with `mv`, never `rm` (user 2026-09-13 03:31). A new handoff is always a NEW file; archive the old one only after its answers have been carried over.

**Create a new handoff directly inside `handoff-archiv/` — do not write it to the
project root first (user, 2026-09-16 20:19).** Reason in his words: "wenn ich es dann
später verschiebe, dann ändert sich ja der Pfadname des Handoffs und lieber haben wir
es schon im richtigen Ordner". Every later move invalidates the path the document was
already linked under. So:

```sh
mkdir -p "<project>/handoff-archiv"
# write both twins here from the start:
#   <project>/handoff-archiv/_handoff-<project>-<date>-<id>.md
#   <project>/handoff-archiv/_handoff-<project>-<date>-<id>.rtf
```

The user deletes there himself what he no longer needs; he never has to move a file.
**The Zwischenrufe file is the exception and stays in the project root** — he clears
that one by hand. Link the handoff by its archive path in every message that names it.

<!-- rule:HF-05 -->
## Read it completely, never filtered (2026-09-14)

Read the previous handoff unfiltered, first line to last, before writing the new one. Never truncate long lines, never grep only for `>>>User answer:`, never filter "to save tokens" — that is exactly how the through-line, roadmap, measurement, main documents, memory, and logbook disappear from the successor revision. Read oversized files in blocks, but completely. And at the end of a wave, do not wait for one more agent report; outstanding reports belong under "Running and pending" and do not hold up completion.

<!-- rule:HF-06 -->
## Full section order (mandatory, 2026-09-14)

The eight required sections above are the minimum. The shipped order is:

1. Header: own absolute path, as-of line (HF-01), then the copy line `Ich habe das Handoff bearbeitet: <absolute path to the .rtf>` — 2. Editing note — WITHOUT its own `>>>` line below it (BE and BF carried a meaningless gold line in the header; user 2026-09-14 23:14). The first `>>>User answer:` belongs under the first question — 3. The state in three sentences — 4. Objective and authorization — 5. Verified state — 6. Running and pending — 7. The user's collection, verbatim, separated by source, new input only (HF-08) — 8. What I made of it — 9. Decisions and questions with `>>>User answer:` — 10. Test list with `>>>User answer:` per item — 11. The through-line — 12. Short roadmap — 13. Measurement of the wave — 14. Main documents and further documents — 15. Memory (durable/session) — 16. Logbook — 17. `COLLECTION FOR THE NEXT HANDOFF`.

A missing section means the handoff is not finished. Check the list against the file before rendering.


<!-- rule:HF-07 -->
## Answer the interjections Markdown file

At wave start, create and open the interjections file as `.md` in the project root, never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it.

When modification time is unchanged, do not reopen or rewrite the file. If changed saved state contains no new user input, record "nein". Answer short items promptly; schedule longer ones into the next wave.

<!-- rule:HF-08 -->
## Carry only new input verbatim, link the older (2026-10-04)

The verbatim collection holds only what the user entered **after the previous
handoff**: its collection footer, the wave's Zwischenrufe file, and the chat
messages of the wave. **Answers, questions, and test answers from the
predecessor's answer fields are NOT repeated verbatim** — neither as a section
"<id> — new answers" nor in the collection. They appear only under "What I made
of it", one line per item with its source:

`F2 → skill shortened, rule HF-08 sharpened (source: _handoff-<project>-<date>-CL, F2)`

User, 2026-10-06 02:42 (T34): "Ich brauch nicht, dass du die alten Handoff-Dateien
Fragen und Antworten und Tests mitnimmst"; likewise 2026-10-04 23:43: "keine
Wiederholungen vom alten Handoff". `sammlung-pruefen.sh` therefore requires only the
collection footer verbatim, checks that the answer fields are referenced by the
predecessor's name, and reports answers repeated verbatim (40+ characters) as a finding. Originals
that the predecessor had itself carried over from earlier revisions are NOT copied
again. They stay in the archived predecessor, which is never changed or deleted.
One line replaces them:

`Older originals: <absolute path of the predecessor>, section "<name>"`

Reason, in the user's words (2026-10-04 17:01): "was bringt es uns denn, wenn es
im Handoff drin ist, das haben wir doch schon im alten Handoff drin". Measured on
the handoff that triggered the rule: 110 kB, a large part of it originals copied
for the second and third time.

Three conditions keep this lossless:

1. **Every wish from an older original that is still open gets its own row under
   "Running and pending"**, with its source (handoff revision and time). A wish
   that lives only inside an old original is lost, because the next session reads
   the new handoff, not the chain behind it.
2. **Reading stays complete (HF-05).** The saving is in the new document, not in
   the reading of the predecessor.
3. **The link must resolve.** If the predecessor is missing or was moved, carry
   its originals verbatim once more instead of linking into nothing.

`scripts/sammlung-pruefen.sh` checks the immediate predecessor only, for the same
reason.

<!-- rule:HF-09 -->
## Revision ID, header, and addenda (2026-10-02)

A revision carries its ID consistently: in the file name (`…-2026-10-02-r.md` and `.rtf`), the title, the copy line, and the editing note. The header is: line 1 the document's own absolute path, line 2 `Stand:` from `date`, then `Ich habe das Handoff bearbeitet: <own .rtf path>`, then the title.

- Never create a new revision as a copy of the previous one with only the path line replaced. Whoever copies replaces every self-reference (title, "answer in …", "x replaces y", measurement row, document list) and checks afterwards. Evidence: handoff r of the website session carried the title "(q)" and sent answers to q.
- An addendum after rendering goes into the Markdown and becomes a new revision through `scripts/handoff-rtf.sh`. Never write straight into the RTF: Markdown and RTF drift apart, and whoever writes the next handoff from the Markdown loses the addendum.
- Run `scripts/handoff-pruefen.py <handoff.md>` before and after rendering; it checks path, as-of line, revision ID, copy line, header self-references, and section order. Pass answered predecessors to `scripts/sammlung-pruefen.sh` as the saved RTF, because the agent's Markdown does not contain the answers.

See also [wave execution](wave-execution.md), [evidence scope](evidence-scope.md), and [RTF on macOS](rtf-macos.md).

Document path and as-of lines follow RT-05 in [RTF on macOS](rtf-macos.md).

### Timestamp on every NEW request (user, 2026-09-16 21:58)

**The first line of the first reply to a new user message carries
`Name, DD.MM.YYYY-HH:MM`.** Not on every interim message inside the same reply
chain — only at the start. The timestamp is the user's signal that work has begun.

The time comes **only** from `date "+%d.%m.%Y-%H:%M"`, never from an estimate
(the user measured a 15-minute drift on 2026-09-12). He has asked for this three times.

It applies to **every** new user message, including an interjection the lead answers as a new
request, and in long sessions as much as in the first reply: the user counts his requests by
these stamps (2026-10-08 22:35: "Der signalisiert mir halt, wie viel Anfragen das insgesamt waren").

<!-- rule:HF-10 -->
## The archive keeps the RTF; the collection stays (user, 2026-10-08)

- **RTF handoffs stay in the archive folder for good** as the project's documentation. New
  handoffs are created there (WH-04), so nothing ever has to move.
- **The user may delete Markdown sources himself; the agent never deletes** a handoff, MD or RTF.
- **The verbatim collection stays in every handoff** (new input only, HF-08). "What I made of it"
  is the compact interpretation next to it, not its replacement; the user wants both
  (22:53: "dann lass man das lieber so").
