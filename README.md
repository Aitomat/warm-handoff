# warm-handoff 🏄

**Primary language: English · [Complete German edition](README.de.md)**

Warm Handoff preserves user input and verified project state across pauses. It also defines safe, evidence-based work waves for Codex and Claude Code without treating either host as the core workflow.

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

Do not copy the whole repository. Historical evidence, personal helpers, review artifacts, tests, and files such as `docs/.sol-err`, `scripts/codex-limit.sh`, or `scripts/skills-uebersicht.sh` are not part of an active package. The package manifest includes only the selected entry, its revision-local references, the safe RTF renderer files, and the matching project-agreement template. No global settings or project instruction files are changed by installation.

RTF support is optional and macOS-only. It needs Bash, Python 3, and `textutil`:

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
Read the applicable CLAUDE.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Preserve user originals, verify current Git and test state, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Compact German (`compact-de`)

<!-- prompt:compact-de-claude -->
```text
/warm-handoff-de
Read the applicable CLAUDE.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Work in German, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Full English (`full-en`)

<!-- prompt:full-en-claude -->
```text
/warm-handoff-full
Read the applicable CLAUDE.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full English workflow, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
```

### Full German (`full-de`)

<!-- prompt:full-de-claude -->
```text
/warm-handoff-full-de
Read the applicable CLAUDE.md files and the complete saved handoff at <ABSOLUTE_HANDOFF_PATH>. Apply the full German workflow, preserve user originals, and continue only within the stated authorization. Use the Claude Code adapter and write the requested durable report before completion.
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
