# RTF on macOS

<!-- rule:RT-01 -->
## Safe generation

RTF is an optional editable twin of an agent-authored Markdown handoff. It requires macOS, Python 3, Bash, and `textutil`.

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
blocks reset with `\pard\plain\f0`. Cocoa and TextEdit ignore `\highlight`
entirely — only `\cb`/`\cbpat` paint a background there — and `\cb0` reads as
black rather than "no background", so `\plain` is the only clean reset. Verify
with `textutil -convert html -stdout FILE.rtf`: the answer class carries an
18 px font and the gold background, agent text carries no background. The same
gold rule applies to the Zwischenrufe RTF, not only to the handoff.

<!-- rule:RT-03b -->
## Black on gold, 18 pt, for text pasted behind `>>>` (evidence W58-E1, 2026-09-13)

Typing or pasting (Cmd-V) at the end of a gold answer paragraph must stay black
text on gold at 18 pt. Cocoa honors only character-level shading, so a renderer
needs all of the following — naming the control words matters because Codex
users may render without `scripts/render_rtf.py`:

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
