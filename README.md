# warm-handoff 🏄

**Primary language: English · [Complete German edition](README.de.md)**

Warm Handoff preserves user input and verified project state across pauses. It also defines safe, evidence-based work waves for Codex and Claude Code without treating either host as the core workflow.

Every change to an active rule is also carried into `AGENTS.md`. `AGENTS.md` is the one shared instruction file for Codex, Claude Code, and other agents; current Claude Code versions read it too. A `CLAUDE.md` is optional — at most a one-line pointer or a symlink to `AGENTS.md`.

## Why an interjections file and a handoff

Agents work for hours; the human should not sit and wait for them. Warm Handoff gives him two plain documents instead of a chat he has to watch:

- **The handoff** is the bridge between sessions. It carries what was verified, what is still running or open, and the questions the next session must answer. The user answers in it at his own pace; saving (Cmd-S) is the release. RTF handoffs stay in the archive for good, as the project's documentation.
- **The interjections file** is the inbox while a wave runs. Every idea, correction, or question that comes to mind goes in there and is saved; the lead picks it up on its next wake-up without being interrupted.

The advantage: **the human stays creative while the agents work.** He can keep thinking, dictating, and adding for hours, and nothing gets lost, because:

1. **Questions first.** The lead filters the user's new questions out of the answered handoff and answers what it can at once, in the chat and as a copy in the interjections file, in parallel with the wave start. Deeper answers follow from the topic agents. Questions answered hours later are questions already forgotten.
2. **Late ideas still land.** An interjection for an assignment that has not started yet goes into its brief as an addendum; one for a running assignment becomes a follow-up.
3. **Small things do not wait.** One of the parallel agent slots works only through small tasks, one after another, while the long, hard topics start first on the others.
4. **Every new request is stamped.** Each first reply starts with `Name, DD.MM.YYYY-HH:MM` from the system clock, so the user can see when work started and count his requests.

<!-- section:SURFACES -->
## Choose a surface

| Need | English | German | Installable entry |
|---|---|---|---|
| Routine, low-context use | [Compact skill](SKILL.md) | [Installable compact German skill](variants/compact-de/SKILL.md) | package `compact-en` or `compact-de` |
| Adoption, training, audit | [Full skill](variants/full/SKILL.md) | [Installable full German skill](variants/full-de/SKILL.md) | package `full-en` or `full-de` |
| Codex host behavior | [Codex adapter](references/codex.md) | [Codex adapter](references/codex.de.md) | load on demand |
| Claude Code behavior | [Claude adapter](references/claude-code.md) | [Claude adapter](references/claude-code.de.md) | load on demand |

All unqualified active files are English. Every active instruction has a `.de.md` semantic counterpart listed in [the machine-readable language matrix](docs/language-matrix.json). Spanish is deferred. Audio, video, and website material remain future proposals.

<!-- section:INSTALLATION -->
## Install one variant

Inspect an existing destination first and preserve it separately. Do not merge files into an occupied skill directory.

Choose exactly one package from `docs/language-matrix.json`. Copy its `entry` into a new destination as `SKILL.md`, then copy only its listed `resources`, preserving their relative paths. Typical destination parents are `~/.codex/skills/` for Codex and `~/.claude/skills/` for Claude Code. The four package IDs are `compact-en`, `compact-de`, `full-en`, and `full-de`; every installed package has a unique skill name.

| Package | Entry copied as `SKILL.md` | Skill name | Codex invocation | Claude Code invocation |
|---|---|---|---|---|
| `compact-en` | `SKILL.md` | `warm-handoff` | `$warm-handoff` | `/warm-handoff` |
| `compact-de` | `variants/compact-de/SKILL.md` | `warm-handoff-de` | `$warm-handoff-de` | `/warm-handoff-de` |
| `full-en` | `variants/full/SKILL.md` | `warm-handoff-full` | `$warm-handoff-full` | `/warm-handoff-full` |
| `full-de` | `variants/full-de/SKILL.md` | `warm-handoff-full-de` | `$warm-handoff-full-de` | `/warm-handoff-full-de` |

Do not copy the whole repository. Historical evidence, personal helpers, review artifacts, tests, and files such as `docs/.sol-err`, `scripts/codex-limit.sh`, or `scripts/skills-uebersicht.sh` are not part of an active package. The package manifest includes only the selected entry, its revision-local references, the renderer, validation, and reply scripts, and the matching project-agreement template. No global settings or project instruction files are changed by installation.

RTF support is optional and macOS-only. It needs Bash, Python 3, and `textutil`:

Generate requested handoff RTFs exclusively with `scripts/handoff-rtf.sh`, using absolute source/output paths and a new output filename. Text behind `>>>` stays black on gold at 18 pt. See [RTF safety](references/rtf-macos.md) for control words, answer boundaries, and verification limits.

At wave start, create the interjections file as `.md` in the project root and open it in an editor the user can type into (on macOS: `open -a TextEdit "<full path>"`, never a read-only viewer such as a cmux markdown tab), never as an RTF inbox; it is the only inbox until the next handoff. Read only saved additions; append replies in that same Markdown file with `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <time>`, and `AB HIER NEUE ZWISCHENRUFE` plus an empty `>>>` line. If the editor has unsaved input or its state is unknown, defer the append; never save or close it. Follow HF-07.

Cmd-S releases saved input within existing authorization. Keep exactly one active Zwischenrufe inbox (handoff footer or agreed file); the other only links to it. Archive answered handoffs in the project's `handoff-archiv/` with `mv`, never `rm`; do not move the active input file. **New handoffs are created directly in `handoff-archiv/` (user, 2026-09-16 20:19).** Do not create them in the project root and move them later — every move changes the path the document has already been linked under. So write `<project>/handoff-archiv/_handoff-<project>-<date>-<id>.md` and `.rtf` from the start (`mkdir -p` the folder if missing). The user deletes there himself what he does not need; he no longer has to move anything. **The Zwischenrufe file stays in the project root** — he clears that one by hand. Run the tests below from the repository checkout; tests are not included in installed packages.

```sh
scripts/handoff-rtf.sh /project/docs/handoff.md /project/handoff.rtf --project-root /project
python3 -m unittest discover -s tests -v
```

<!-- section:CODEX-START -->
## Start with Codex

### Compact English (`compact-en`)

<!-- prompt:compact-en-codex -->
```text
$warm-handoff
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Preserve user originals, verify current Git and test state, and continue only within the stated authorization. Use the Codex adapter and write the requested durable report before completion.
```

### Compact German (`compact-de`)

<!-- prompt:compact-de-codex -->
```text
$warm-handoff-de
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Work in German, preserve user originals, and continue only within the stated authorization. Use the Codex adapter and write the requested durable report before completion.
```

### Full English (`full-en`)

<!-- prompt:full-en-codex -->
```text
$warm-handoff-full
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full English workflow, preserve user originals, and continue only within the stated authorization. Use the Codex adapter and write the requested durable report before completion.
```

### Full German (`full-de`)

<!-- prompt:full-de-codex -->
```text
$warm-handoff-full-de
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full German workflow, preserve user originals, and continue only within the stated authorization. Use the Codex adapter and write the requested durable report before completion.
```

<!-- section:CLAUDE-START -->
## Start with Claude Code

### Compact English (`compact-en`)

<!-- prompt:compact-en-claude -->
```text
/warm-handoff
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Preserve user originals, verify current Git and test state, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Compact German (`compact-de`)

<!-- prompt:compact-de-claude -->
```text
/warm-handoff-de
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Work in German, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Full English (`full-en`)

<!-- prompt:full-en-claude -->
```text
/warm-handoff-full
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full English workflow, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Full German (`full-de`)

<!-- prompt:full-de-claude -->
```text
/warm-handoff-full-de
Read the applicable AGENTS.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full German workflow, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

<!-- section:REFERENCES -->
## Core references

- [Handoff format](references/handoff-format.md)
- [Authorized work waves](references/wave-execution.md)
- [RTF on macOS](references/rtf-macos.md)
- [Optional Context Mode](references/context-mode.md)
- [Model routing](references/model-routing.md)
- [Evidence scope](references/evidence-scope.md)

Platform and cache claims are dated and sourced in the adapters and model-routing reference. API specifications, effective host limits, and measured session values remain separate.

## Credits and license

Created by Yasin Akgün through day-to-day work on Aitomat. The handoff structure builds on [Matt Pocock's `/handoff`](https://www.aihero.dev/skills-handoff) and related public implementations. Contributions in English or German are welcome. See [LICENSE](LICENSE).
