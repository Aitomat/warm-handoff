# warm-handoff bekannt machen — der Plan

Stand: 28.08.2026. Ziel: Claude-Code-Nutzer, die das Thema Cache-Fenster / Kontextkosten
noch nie gehört haben, finden den Skill und probieren ihn aus. Reihenfolge ist bewusst:
erst das Repo präsentabel, dann die Verzeichnisse (langsam, aber dauerhaft), dann die
Communities (schnell, aber flüchtig), dann Langform.

## 0. Voraussetzungen im Repo (vor jedem Post)

| Punkt | Status | Was tun |
|---|---|---|
| README ausführlich, engl. Einleitung oben | erledigt 28.08. | — |
| GitHub-Topics | erledigt 28.08. | `claude-code, claude, skills, prompt-caching, agent-workflow` |
| Release `v1.0.0` mit Tag | erledigt 28.08. | Release-Notes: 3 Sätze, Link auf README-Abschnitt 1 |
| LICENSE (MIT) | vorhanden | — |
| Discussions aktivieren | offen | GitHub → Settings → Features → Discussions; Kategorie „Measurements" anlegen, damit Leute eigene Kostentabellen posten |
| README-Badges | offen | Lizenz, Release-Version, „Claude Code Skill" — nur drei, kein Badge-Teppich |
| Ein Screenshot / GIF | offen | Kostenzeile + Kostentabelle im Terminal, 20 s GIF; das ist das Bild, das in jedem Post steht |
| `SKILL.md` Frontmatter englisch, Description mit Trigger-Wörtern | vorhanden | — |
| Englische Kurzfassung der Kernregeln | offen | `docs/quickstart-en.md`, eine Seite: Fakten, Faktoren, Wellen-Workflow, Install |

Badges (in README ganz oben, unter dem Titel):

```markdown
![License](https://img.shields.io/github/license/Aitomat/warm-handoff)
![Release](https://img.shields.io/github/v/release/Aitomat/warm-handoff)
![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)
```

## 1. Verzeichnisse und Listen (Woche 1 — langsam, aber dauerhaft)

Reihenfolge nach erwarteter Reichweite pro Aufwand:

1. **agentskills.io** — das Skill-Verzeichnis. Eintrag anlegen (Name, Description aus dem
   Frontmatter, Repo-Link, Kategorie „Workflow / Productivity"). Vorher prüfen, ob sie ein
   `skill.json`-Manifest oder bestimmte Ordnerstruktur erwarten.
2. **anthropics/skills** — PR mit Eintrag in die Community-Liste, falls dort eine gepflegt
   wird (README des Repos lesen: manche Listen nehmen nur Skills mit englischer SKILL.md
   → dann zuerst `docs/quickstart-en.md` liefern und im PR darauf verweisen).
3. **awesome-Listen** — je ein PR, eine Zeile, englisch, im Stil der jeweiligen Liste:
   - `hesreallyhim/awesome-claude-code` (größte Liste)
   - `awesome-claude-skills` (mehrere Forks — die mit den meisten Sternen nehmen)
   - `mattpocock/skills` — kein PR, aber ein Issue/Discussion: „warm-handoff builds on your
     /handoff, differs in X" — Matt verlinkt gern Ableger.
4. **GitHub-Topics-Seiten** laufen automatisch über die Topics (Schritt 0).

Textbaustein für alle Listen (eine Zeile):

> **warm-handoff** — Paces a Claude Code session around the 1-hour prompt cache: timestamps,
> measured context size, a cost line per reply, subagent-first delegation, and a handoff
> document you answer in a text editor. Measured: 147 → 14 requests, ~70 % cheaper per work
> stretch.

## 2. Communities (Woche 2 — schnell, flüchtig, am besten Di–Do vormittags US-Zeit)

Reihenfolge: **Reddit zuerst** (geringstes Risiko, Feedback für den HN-Text), dann **X**,
dann **Show HN** (nur einmal, gut vorbereitet).

### 2a. Reddit r/ClaudeAI (auch r/ClaudeCode, r/LocalLLaMA nur, wenn es dort um Kosten geht)

Flair: „Productivity" oder „Coding". Bild: das GIF aus Schritt 0. Auf Kommentare innerhalb
der ersten zwei Stunden antworten — das entscheidet über das Ranking.

**Entwurf:**

> **I measured what one Claude Code message actually costs — 147 requests. Here's the skill that got it down to 14.**
>
> I build a macOS app with Claude Code every day and my Max quota kept running out faster
> than the amount of work explained. So I read the session `.jsonl` files and counted.
>
> One "please implement what I answered in the test list" message = **147 model requests**,
> each re-reading a 223k-token context. Cache read is ×0.1, cache write ×2, Claude's own
> output ×5 (Anthropic list-price ratios). That single stretch cost ~4.4M token-equivalents.
> Not because I wrote too much — because the work loop (read file, grep, edit, run, read
> result) runs *inside* the fat main context.
>
> What actually helped, in order:
> 1. **Subagents by default** — every step runs against ~30k instead of ~300k. Same work,
>    2.4× cheaper. (Their tokens still count against the weekly quota — just not against the
>    main context.)
> 2. **Fewer round trips** — Claude writes a *handoff document* at the end of a work wave
>    (delivered / open / test checklist with answer lines). I answer it in TextEdit whenever I
>    want, which costs zero requests, and the next session starts from that file alone.
> 3. **Cap the reports** — every subagent report gets written into the cache (×2) and
>    re-read on every later request. "≤250 words, no diffs" is a real cost rule.
> 4. **Don't narrate** — Claude's own output is the ×5 item. In one session it was a third of
>    the bill.
>
> I packaged the rules plus three scripts (cost line per reply, per-session cost table,
> Codex quota readout) as a skill: https://github.com/Aitomat/warm-handoff
>
> Honest limits: one developer, one project, subscription plan. The per-technique savings
> are estimates and overlap. The scripts ship so you can measure your own sessions — I'd
> genuinely like to see other people's tables.

### 2b. X / Twitter

Thread, 5 Tweets, das GIF im ersten. Leute taggen, die über Claude-Code-Workflows schreiben
(Matt Pocock, Boris Cherny, die Autoren der awesome-Listen) — nur, wenn der Bezug echt ist.

1. „One Claude Code message cost me 147 model requests. I counted. Here's what I changed →"
2. Die Faktoren-Tabelle als Bild (×0.1 / ×2 / ×5).
3. Die Kostentabelle als Bild, mit den zwei Null-Zeilen markiert.
4. Der Wellen-Workflow in drei Zeilen.
5. Repo-Link + „scripts included, measure your own sessions".

### 2c. Hacker News — Show HN

Ein Versuch. Dienstag bis Donnerstag, 14–16 Uhr MESZ (8–10 Uhr ET). Titel ≤ 80 Zeichen,
keine Ausrufezeichen, kein „revolutionary". Link direkt aufs Repo. Den Text als ersten
Kommentar posten.

**Titel:**

> Show HN: Warm-handoff – pacing Claude Code sessions around the prompt cache

**Erster Kommentar:**

> Author here. This started as a puzzle: my Claude Code quota drained much faster than the
> visible work explained. Claude Code keeps session transcripts as JSONL, so I parsed them
> and counted requests per user message instead of guessing.
>
> Findings from one real project (macOS app, Max plan):
>
> - A single "implement this" message triggered 147 model requests. Each one re-reads the
>   whole prefix — 223k tokens at that point — from the prompt cache.
> - Cache read costs ×0.1, cache write ×2 (1-hour TTL), model output ×5, relative to fresh
>   input. So the cost driver is request count × context size, not message length.
> - The 1-hour cache on Pro/Max is sliding: any pause over an hour, any mid-session model or
>   effort change, any CLAUDE.md edit rebuilds it at ×2 over the whole prefix.
> - Subagents get a 5-minute cache always, but work against a ~30k context. Delegating the
>   same 147 steps: ~2.2M → ~0.9M equivalents.
>
> The skill is a SKILL.md (rules Claude follows) plus three bash scripts: a cost line
> under each reply (what the last request cost, split by read/write/output), a per-session
> cost table (one row per user message — two rows in the example are literally 0 because
> the messages arrived while Claude was mid-loop and got batched), and a Codex quota readout
> parsed from its session files because the CLI has no usage command.
>
> The workflow it pushes: batch work into "waves", end each wave with a handoff document
> that contains the test checklist with answer lines, answer that in a text editor (zero
> requests), start the next session from the file alone.
>
> Caveats I'd rather state myself: n=1 developer, the per-technique savings are estimates
> from a second model over the same data and overlap, and "token equivalents" are list-price
> ratios — nobody on a subscription pays that number, it measures quota load. The README is
> mostly German (English summary on top); the scripts are the portable part.
>
> Curious whether others see the same ratios, especially on the API with 5-minute caches.

### 2d. Discord / Foren

Anthropic-Discord (#claude-code-Kanal), falls Selbstpromotion erlaubt ist: nur der
Reddit-Text, gekürzt auf fünf Zeilen. Nicht mehrfach posten.

## 3. Langform (Woche 3–4)

- **Dev.to-Artikel** (englisch, 1.500 Wörter): „What one Claude Code message really costs —
  and how I got from 147 requests to 14". Struktur: Messung → Faktoren → drei Techniken mit
  Zahlen → Workflow → Grenzen. Tags: `claude`, `ai`, `productivity`, `devtools`. Auf Medium
  als Cross-Post mit Canonical-Link auf Dev.to.
- **Deutscher Artikel** (Blog / LinkedIn / heise-Developer-Leserbeitrag): dieselbe Struktur;
  die Zielgruppe deutscher Claude-Code-Nutzer ist klein, aber unbedient.
- **Kurzvideo** (60–90 s, Hoch- oder Querformat, Drehbuch in `drehbuch-video-DE.md`): das
  Terminal, eine Nachricht, die Kostenzeile, dann die Kostentabelle mit den Null-Zeilen,
  dann das Handoff in TextEdit. Ohne Gesicht, mit Untertiteln. YouTube Shorts + X + im
  README verlinkt.

## 4. Was danach zählt

- Auf **jedes** Issue innerhalb eines Tages reagieren — in den ersten Wochen ist das die
  ganze Reputation.
- Fremde Messungen (Discussions-Kategorie „Measurements") in einen Abschnitt „Other
  people's numbers" im README übernehmen — mit Namen. Das ist das stärkste Argument, das
  der Skill bekommen kann.
- Jede neue Regel im Skill weiter mit Datum und Anlass versehen; das ist das
  Alleinstellungsmerkmal gegenüber den anderen Handoff-Skills.
- Nicht: an mehreren Tagen hintereinander dasselbe posten, Bots, Sterne kaufen, in fremde
  Issues den Link setzen.

## 5. Zeitplan

| Woche | Kanal | Aufwand |
|---|---|---|
| 1 | Schritt 0 fertig, GIF, quickstart-en, agentskills.io, awesome-PRs | 3–4 h |
| 2 | Reddit (Di), X-Thread (Mi), Show HN (Do) | 2 h + Antworten |
| 3 | Dev.to + Medium | 3 h |
| 4 | Kurzvideo, deutscher Artikel | 3 h |
