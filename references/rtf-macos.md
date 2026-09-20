# RTF on macOS

<!-- rule:RT-01 -->
## Safe generation

RTF is an optional editable twin of an agent-authored Markdown handoff. It requires macOS, Python 3, Bash, and `textutil`.

Generate handoff and Zwischenrufe RTFs exclusively through `scripts/handoff-rtf.sh`, run from the repository or installed skill directory with absolute source/output paths. Do not rebuild RTF by hand or invoke `render_rtf.py` directly; use `textutil` only to read and verify.

Cmd-S releases saved user input within the existing authorization. Keep exactly one active interjections inbox: the handoff footer or the agreed file; the other only links to it. Archive answered handoffs in the project's archive folder using `mv`, never `rm`; do not move the active user input file.

**Create a new handoff directly in the archive folder.** Do not write it into the project root and move it later — every move changes a path the document has already been linked under. So write `<project>/handoff-archiv/_handoff-<project>-<date>-<id>.md` and `.rtf` from the start (`mkdir -p` the folder if missing); the user deletes there himself what he does not need. **The interjections file stays in the project root**, where the user clears it by hand.

```sh
scripts/handoff-rtf.sh /project/docs/handoff.md /project/handoff.rtf --project-root /project
```

The output path must be new. The renderer refuses existing files and symlinks, writes through a temporary file, verifies plain text and hyperlink fields, and publishes exclusively. Relative links resolve from `--project-root`, otherwise the nearest `.git` marker, otherwise the Markdown directory. Explicit missing Markdown links and local paths fail instead of becoming dead links.

<!-- rule:RT-02 -->
## Verbatim input and links

Wrap preserved user text in `<!-- user-original:start -->` and `<!-- user-original:end -->`. Its visible text stays literal. Markdown links, supported document markers, URLs, paths in inline code, and real absolute paths remain link candidates. Slash compounds such as `root-/worker usage` or `token-/cost telemetry` are prose and must not be parsed as root paths.

<!-- rule:RT-03 -->
## Gold answer continuation

Lines beginning with `>>>` and all subsequent nonempty continuation lines are gold, 18-point answer paragraphs. A blank line also receives gold and ends the answer; a heading, code fence, or `<!-- answer:end -->` ends it before the next paragraph. Always separate agent text using one of these boundaries. For user text spanning blank lines or containing literal Markdown, use a `user-original` block: every line in it is gold. Typing in a gold paragraph, pressing Return, saving, and reopening must keep continued user text gold and 18 pt. A later agent paragraph must have no answer background.

The automated AppKit test covers this storage and save/reload behavior. A manual TextEdit check remains distinct because launching or focusing the editor can disturb the user's desktop.

The **document default** carries the same 18 pt gold, so pasted plain text and
typed text inherit it instead of falling back to the RTF built-in 12 pt with no
background. The header therefore sets a `Normal` stylesheet entry and the same
character state before the first paragraph; agent paragraphs, headings and code
blocks reset with `\pard\plain\f0\cf2`. Use the complete GOLD state below for
Cocoa character shading; `\highlight` alone is insufficient, and `\cb0` reads as
black rather than "no background", so `\plain` is the only clean reset. Verify
with `textutil -convert html -stdout FILE.rtf`: the answer class carries an
18 px font and the gold background, agent text carries no background. The same
gold rule applies to the Zwischenrufe RTF, not only to the handoff.

<!-- rule:RT-03b -->
## Black on gold, 18 pt, for text pasted behind `>>>` (evidence W58-E1, 2026-09-13)

Typing or pasting (Cmd-V) at the end of a gold answer paragraph must stay black
text on gold at 18 pt. Cocoa honors only character-level shading, so a renderer
uses all of the following. These are verification requirements for the bundled
renderer, not permission to use another generation path:

- colour table `;gold;black;` — gold is entry 1 (`\red255\green231\blue153`),
  black is entry 2;
- `GOLD = \cb1\cbpat1\chshdng0\chcbpat1\highlight1\cf2` — `\chshdng0\chcbpat1`
  is the only part Cocoa paints on the character level, and `\cf2` forces black
  glyphs so user typing is never gold on gold;
- `RESET = \plain\f0\cf2` — `\cb0` reads as black rather than "no background",
  so `\plain` is the only clean reset;
- answer paragraphs are emitted as `RESET + \fs36 + GOLD`; `\fs36` = 18 pt.

Evidence W58-E1: a test file opened in TextEdit via osascript, cursor at end of
document, `keystroke "Test 123"`, saved — the RTF at the insertion point reads
`\fs36 \cf0 \cb2 >>> … Test 123`, with `\cb2` the gold
`\red255\green231\blue153` and `\cf0` auto/black; `textutil -convert txt`
returns the text in full.

<!-- rule:RT-04 -->
## Three evidence scopes

- Renderer roundtrip: generated text and hyperlink fields.
- TextEdit/AppKit continuation: typing and paragraph style after save/reload.
- Application paste: behavior in the target application.

Do not claim one scope from evidence in another. Opening files, merging tabs, or manipulating TextEdit windows is allowed only when the user authorized UI control. Never overwrite the user's answered RTF.

<!-- rule:RT-05 -->
## Path line at the top of every document

Every document you create or revise — plan, report, concept, roadmap, handoff,
interjections file — starts with **its own absolute path** as the very first
line, with nothing above it, not even a heading. Below that the as-of date, then
the heading:

```markdown
/absolute/path/to/the/document.md
As of: DD.MM.YYYY, HH:MM

# Document heading
```

The point is that the user can copy the top line and have the path with it
instead of hunting for it; when a document moves, the line moves with it. Give
paths in replies in full, from the root, for the same reason.

<!-- rule:RT-06 -->
## Close and reopen documents you changed

TextEdit keeps showing the state it loaded the file with; a change on disk never
reaches it. So when you change a file that may be open, close it **first** and
reopen it **after**:

```sh
osascript -e 'tell application "TextEdit" to close (every document whose path contains "<filename>")'
open -a TextEdit "<full path>"
```

Close only your own document, never "every document" — leave other open files
alone. And only close what holds no unsaved input: for the Zwischenrufe file and
the handoff, read what is saved and otherwise leave them open. Applies to every
document whose path you name in a reply.

<!-- rule:RT-07 -->
## Interjections as Markdown, with answers written into the file

A project may keep the interjections file as a plain `.md` instead of an RTF
twin; the renderer rightly refuses to append to an existing RTF, so an RTF inbox
cannot be answered in place. Append an answer block safely — never touch unsaved
input:

```sh
M=$(osascript -e 'tell application "TextEdit" to get modified of (first document whose path contains "<filename>")')
# only when M is "false": close without saving, append, reopen
osascript -e 'tell application "TextEdit" to close (every document whose path contains "<filename>") saving no'
cat >> "<full path>" <<'EOT'   # quoted heredoc: backticks and $ stay literal
…
EOT
open -a TextEdit "<full path>"
```

If `modified` is `true`, do not close: answer in chat and append on the next wake-up.
