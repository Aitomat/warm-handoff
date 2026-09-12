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

<!-- rule:RT-04 -->
## Three evidence scopes

- Renderer roundtrip: generated text and hyperlink fields.
- TextEdit/AppKit continuation: typing and paragraph style after save/reload.
- Application paste: behavior in the target application.

Do not claim one scope from evidence in another. Opening files, merging tabs, or manipulating TextEdit windows is allowed only when the user authorized UI control. Never overwrite the user's answered RTF.
