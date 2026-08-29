Reading additional input from stdin...
OpenAI Codex v0.144.5
--------
workdir: /Users/pro16/Code/warm-handoff
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 01a04f22-2a5c-7931-bfce-15ca20135604
--------
user
Review SKILL.md and SKILL.de.md as a Claude Code skill: clarity, contradictions, missing rules, English quality. Answer in Markdown, max 60 lines.
warning: `--dangerously-bypass-hook-trust` is enabled. Enabled hooks may run without review for this invocation.
warning: `--dangerously-bypass-hook-trust` is enabled. Enabled hooks may run without review for this invocation.
hook: SessionStart
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
I’ll review both files side by side, including any repository-level instructions that govern them, then return a concise issue list with actionable wording fixes.
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "pwd && rg --files -g 'AGENTS.md' -g 'SKILL.md' -g 'SKILL.de.md' -g '"'!node_modules'"'" in /Users/pro16/Code/warm-handoff
 succeeded in 0ms:
/Users/pro16/Code/warm-handoff
SKILL.de.md
SKILL.md

hook: PostToolUse
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "wc -l SKILL.md SKILL.de.md && sed -n '1,240p' SKILL.md && sed -n '1,260p' SKILL.de.md" in /Users/pro16/Code/warm-handoff
 succeeded in 0ms:
     190 SKILL.md
     194 SKILL.de.md
     384 total
---
name: warm-handoff
description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, warns before cache-destroying actions, recommends a fresh session past a context threshold, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", or when resuming after a gap.
---

# warm-handoff — ride the cache wave, hand off before it breaks 🏄

**One sentence:** Handoff → fresh session → handoff. The user collects everything
(test answers, ideas, critique) in ONE handoff file over hours, starts a fresh session,
the agent works it all off through a few subagents and writes the next handoff.
Full history with dated user quotes and the reasoning behind every rule:
`references/historie.md` (read it when a rule here seems odd — do not load it by default).

## The facts (Claude Code docs, 2026-08)

- Pro/Max: **1-hour sliding cache TTL** — every request resets it. Subagents: strict 5 min.
- Cache killers regardless of clock: mid-session `/model` or `/effort` change, editing
  CLAUDE.md/system prompt, MCP server restart. Set model + effort at session START.
- Prices relative to fresh input: **cache read ×0.1 · cache write ×2 (1-h TTL) · own output ×5.**
- Every request re-reads the whole prefix. Cost = requests × context. The user's messages
  are a rounding error; the agent's own tool steps and reports are the bill.

## Every reply — three honesty rules

1. **Timestamp from a `date` call in THAT reply** (`date "+%d.%m.%Y %H:%M"`, piggybacked on
   any command). No `date` this turn → no timestamp. Never extrapolate, never `~19:40`.
2. **Never guess context size.** Sources: the user's status line, or `~/.claude/ctx.sh`
   appended to a command that runs anyway (`date … && ~/.claude/ctx.sh`). It reads the
   session JSONL (`cache_read + cache_creation` of the last request). None → "not measured".
3. **Cost line under every substantive reply**, from the LAST COMPLETED request, labeled so:
   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Skip it on one-liners. If a round cost > 2× the
   session's average, say why ONCE per wave, kindly, with the cheaper path — the cause is
   almost always the agent (whole files read, raw output, long replies), not the user.

## Sweetspot — when to hand off

| What comes next | Hand off at |
|---|---|
| Big build/review wave (hundreds of tool steps) | ~200k |
| Mixed | ~250k |
| Only talk / small edits | ~300k |
| Anything | 400k hard ceiling |

Break-even for a fresh session: `(start_ctx × 2) / ((old_ctx − start_ctx) × 0.1)` steps.
Start context is MEASURED per project (82–125k seen), never assumed "~20k". Steps = tool
calls, not user messages. Talking on a fat context is cheap; working on it is not.
Say it at every wave end, casually: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
While the agent's own tool loop runs, a user message is nearly free (attached to the next
request); while subagents run or the agent idles, it costs the full context × 0.1.

## The real lever: fewer requests

Measured: 147 requests, 13 from the user; own output = 23 % of cost. Targets, in order:
**fewer requests · shorter own output · smaller context.** Techniques: batch all independent
reads in one reply · one script that does ten things and prints one summary · pre-filter
output (`grep`/`tail`) · grep instead of reading whole files · no per-agent status messages
(one summary when the fleet lands) · reports as files, not chat · own output budget:
interim ≤ 100 words, final ≤ 500, details in files. Terminal tab-suggestions and every
agent completion notification are full requests too.

## Subagents — the default way to work

- **Guardian agent (Wächter).** For a build wave, ONE orchestrating agent (Opus, low/normal
  effort) gets the whole plan as a file, spawns the worker agents itself, merges, tests,
  bundles, cleans `.build` of merged worktrees, writes the report — the main session is
  woken ONCE instead of once per agent (8 → 1 notifications ≈ 140k saved at 190k ctx).
  Workers' questions land at the guardian, so briefs must be complete: paths, goal,
  limits, acceptance criteria, "no questions — decide, document the assumption".
- **The guardian starts every worker at once, in a single message** (one batch of Agent
  calls), never one after another — a serial tail of workers is what turns a cheap wave
  into a long one. Each worker's FIRST step is to pull the current branch tip (`git pull`
  / `git fetch && git rebase`) before touching any file, so it never builds on a stale base.
- **Cut agents to ~30 minutes, ONE task each** (not 40 minutes / 2–3 tasks — a single focused
  job lands faster and is easier to merge). Longer work delivers into a FILE
  (`docs/reviews/<date>-<topic>.md`) and reports only the path; the handoff lists the
  expected files and the next session checks `ls` first. Never wait for a straggler.
- **Merge each worker's branch the moment it lands**, don't batch merges for later — conflicts
  are cheaper to resolve one at a time, right after the work is fresh. Run the FULL test
  suite only ONCE, at the very end, against the merged result; a flaky/failing individual
  test gets investigated on its own rather than re-running the whole suite.
- **Guardian writes an interim status file after 60 minutes** if the wave is still running
  (path in the handoff-to-be, e.g. `docs/wellen/<date>-zwischenstand.md`) — so a session that
  checks in mid-wave, or a handoff written before the guardian finishes, has something real
  to point to. **The handoff starts even without a finished guardian**: list the guardian and
  its still-running workers under "expected agent results", the next session checks them.
- **Model + effort in the visible label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
  Fable 5 as subagent: **always effort low**; for hard review/design use Opus or a second
  architecture (Codex/GPT). Never review your own output yourself — route to Codex.
- **Agents test before the user.** Full suite + a QA agent that launches the app and clicks
  every test item once; the user should mostly say "works, thanks". **The QA agent closes
  the windows/processes it opened for testing** before it reports done — the user shouldn't
  inherit a pile of leftover test instances.
- Report contract: ≤ 300 words, status/decisions/evidence-with-paths/risks/next; no
  chronicle, no pasted logs. Subagent tokens still hit the weekly quota — what they save is
  the MAIN context (each step ≈ 1/5 the cost, and nothing of it stays in the session).
- Pacing: user present + in a hurry → parallel; user away → sequential (each completion
  keeps the cache warm). Never invent busywork.

## Paid quota — see it, use it, by account size

- `~/.claude/codex-limit.sh [--kurz|--json]` reads Codex `rate_limits` from its last session
  file — only as fresh as the last Codex run; `null` = unknown, not 0. Once per session send
  a tiny ping attached to the first real Codex call (`codex exec --skip-git-repo-check
  "Antworte nur mit: bereit"`). Claude Code quota: `cat ~/.claude/.claude-kontingent`
  (5h/7d %, written by the status line; web UI is the authority when they differ).
- Handoff block "Was noch im Tank ist" right after the status: numbers + measurement age +
  a CONCRETE proposal if lots is free (big review, long test run, second opinion). Unused
  quota expires. Gemini/OpenRouter: no readable balance — say so, never estimate.
- **Small Codex account (Plus, ~20 $)** → Codex does ONLY QA: review, second opinion,
  test runs, acceptance. No build jobs, no "continue at 23:05". Large account → use freely.

## The wave workflow and the handoff file

Write the handoff after every big wave, unprompted. Path `<project>/_handoff-<projekt>-YYYY-MM-DD[-b].md`
(project name in the file name AND title). Hard-wrap prose at ~60–70 chars; commands,
paths, URLs on one line. Reference, don't copy (paths/URLs); redact secrets; name skills
for the next session. Structure, top to bottom:

1. Title with date/time. Then the copy-line for the next session:
   `> \`Ich habe das Handoff beantwortet: /abs/path/_handoff-….md\``
   plus "you can write directly in this file — start lines with >>> or name + timestamp".
2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   (`- [ ] path (agent, started HH:MM)`).
3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — read the previous
   handoff's collection area IMMEDIATELY before writing (same tool call as the unsaved-
   changes guard, including unsaved editor text) and copy it VERBATIM, then a block
   "Was ich daraus gemacht habe" mapping each item → built / answered / roadmap.
   Also check the handoff BEFORE that one for late additions. Never rewrite the user's text.
4. Previous test answers → what became of them, one line each ("your T1 answer taken as:
   … — correct?"). Unanswered items carry over, marked.
5. **Testliste vN** — every item pre-seeded with an empty `>>>Userantwort:` line.
6. Banner (Markdown headings don't stand out in TextEdit — lines and caps do):
   ```
   ═══════════════════════════════════════════════════════════
      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   ═══════════════════════════════════════════════════════════
   >>>Userantwort:
   ```
7. **Der rote Faden** — next 2–3 waves as short paragraphs, each with
   `>>>Hast du dazu noch was anzumerken?`; then a compact Themenspeicher; then
   **Hauptdokumente** (3–6 real files with absolute path + one line + freshness).
8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (unit = span between two
   user messages; explain k = thousand, context column ≠ cost) + honest findings, then the
   closing line with MEASURED context and start context: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** with `aus: /abs/path` and an empty `>>>`.
   The user collects here while the next wave runs — collecting costs zero requests.

Questions for the user go into the handoff (`## Fragen an dich` with `>>>Antwort:`),
not the chat: one chat question blocks a wave, ten in the file block nothing. Cut waves
so they run through without asking; take the likelier reading and document it.

## Editor rules (macOS / TextEdit)

- Open every user-facing document immediately: `open -a TextEdit <file>`. This applies to any
  newly mentioned document, not only the handoff — a plan, a QA report, a review file: the
  moment it exists and is meant for the user to read, open it. Offer once:
  tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt default font
  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md` default app via `duti`.
- **Unsaved-changes guard before reading:**
  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
  if modified, read the live text (`… get text of (first document whose name is "…")`).
- **Never write into, close, save or move the handoff the user has open.** A new handoff is
  always a NEW file. Archive old ones to `handoff-archiv/` (mv, never rm) only after the
  user closed them; otherwise note "archiving pending" in the new handoff.
- If Claude edited a file the user has open and it is unmodified → close + reopen so they
  see the new version; modified → ask, never close.
- Say once: long dictation belongs in the handoff file, short commands in the terminal
  (terminals collapse long input to `[pasted text]`); TextEdit ▸ File ▸ Open Recent finds
  lost handoffs.

## Cache rebuild — detect, don't guess

Hit rate = Σ cache_creation / Σ cache_read from the session JSONL; < 10 % = warm. Big
single writes are usually appends, not rebuilds. Mention a rebuild ONCE, with the cause,
only when it is derivable: gap > 60 min between two `date` reads, a model/effort switch,
a CLAUDE.md edit, an MCP restart. Unknown cause → say nothing. Explain costs as arithmetic
("22k because context is 220k and reads cost ×0.1"), never as assertion; correct your own
earlier misstatements explicitly.

## Logbook and setup

Append one line per handoff to `~/.claude/warm-handoff-log.md`:
`| 22.08.2026 14:40 | ctx 85k | 2 waves | rebuilds: 1 (pause 90min) | est. waste ~60k |`
Summarize patterns every ~50 entries. Always-on: add "At the start of every session,
invoke the warm-handoff skill." to `~/.claude/CLAUDE.md`. Scripts: `scripts/ctx.sh`,
`scripts/session-costs.sh`, `scripts/codex-limit.sh` → copy to `~/.claude/`.
Terminal-neutral: say "your status line", not a specific host's field.
---
name: warm-handoff
description: Zu Beginn jeder Arbeitssitzung und vor jeder längeren Pause nutzen — verfolgt das Claude-Code-Prompt-Cache-Fenster (1 Stunde gleitendes TTL auf Pro/Max), versieht jede Antwort mit einem Zeitstempel, damit der Nutzer das Fenster selbst sieht, warnt vor cache-zerstörenden Aktionen, empfiehlt ab einer Kontext-Schwelle eine frische Sitzung und schreibt ein Handoff-Dokument (mit der Testliste des Nutzers darin), damit die nächste Sitzung günstig und vollständig informiert startet. Auslöser: „cache", „handoff", „Pause", „frische Sitzung", „Welle fertig" oder beim Wiedereinstieg nach einer Lücke.
---

# warm-handoff — die Cache-Welle reiten, übergeben bevor sie bricht 🏄

**Ein Satz:** Handoff → frische Session → Handoff. Der Nutzer sammelt alles
(Testantworten, Ideen, Kritik) in EINEM Handoff-Dokument über Stunden, startet
eine frische Session, der Agent arbeitet alles durch mehrere Subagenten ab und
schreibt das nächste Handoff.
Vollständige Historie mit datierten Nutzer-Zitaten und der Begründung jeder Regel:
`references/historie.md` (lesen, wenn eine Regel hier seltsam wirkt — nicht standardmäßig laden).

## Die Fakten (Claude-Code-Doku, 2026-08)

- Pro/Max: **1 Stunde gleitendes Cache-TTL** — jede Anfrage setzt es zurück. Subagenten: strikt 5 Min.
- Cache-Killer unabhängig von der Uhr: `/model`- oder `/effort`-Wechsel mitten in der Sitzung,
  CLAUDE.md/Systemprompt bearbeiten, MCP-Server-Neustart. Modell + Effort beim Sitzungsstart festlegen.
- Preise relativ zu frischem Input: **Cache-Lesen ×0,1 · Cache-Schreiben ×2 (1-h-TTL) · eigene Ausgabe ×5.**
- Jede Anfrage liest den gesamten Prefix neu. Kosten = Anfragen × Kontext. Die Nachrichten
  des Nutzers sind ein Rundungsfehler; die eigenen Tool-Schritte und Berichte des Agenten sind die Rechnung.

## Jede Antwort — drei Ehrlichkeitsregeln

1. **Zeitstempel aus einem `date`-Aufruf IN DIESER Antwort** (`date "+%d.%m.%Y %H:%M"`,
   huckepack auf einen ohnehin laufenden Befehl). Kein `date` in dieser Runde → kein Zeitstempel.
   Nie extrapolieren, nie `~19:40`.
2. **Nie die Kontextgröße raten.** Quellen: die Statuszeile des Nutzers oder `~/.claude/ctx.sh`,
   angehängt an einen ohnehin laufenden Befehl (`date … && ~/.claude/ctx.sh`). Es liest die
   Session-JSONL (`cache_read + cache_creation` der letzten Anfrage). Keine → "nicht gemessen".
3. **Kostenzeile unter jeder inhaltlichen Antwort**, aus der LETZTEN ABGESCHLOSSENEN Anfrage, so beschriftet:
   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Bei Einzeilern weglassen. Wenn eine Runde > 2× den
   Sitzungsdurchschnitt kostet, EINMAL pro Welle freundlich sagen warum, mit dem günstigeren Weg —
   die Ursache liegt fast immer beim Agenten (ganze Dateien gelesen, Rohausgabe, lange Antworten), nicht beim Nutzer.

## Sweetspot — wann übergeben

| Was als Nächstes kommt | Übergabe bei |
|---|---|
| Große Bau-/Review-Welle (Hunderte Tool-Schritte) | ~200k |
| Gemischt | ~250k |
| Nur Gespräch / kleine Edits | ~300k |
| Alles | 400k harte Obergrenze |

Break-even für eine frische Session: `(Start-Kontext × 2) / ((alter_Kontext − Start-Kontext) × 0,1)` Schritte.
Der Startkontext wird pro Projekt GEMESSEN (82–125k gesehen), nie als "~20k" angenommen. Schritte = Tool-
Aufrufe, nicht Nutzer-Nachrichten. Reden auf fettem Kontext ist billig; Arbeiten darauf nicht.
Bei jedem Wellenende beiläufig sagen: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
Während die eigene Tool-Schleife des Agenten läuft, ist eine Nutzer-Nachricht fast gratis (hängt
sich an die nächste Anfrage an); während Subagenten laufen oder der Agent leerläuft, kostet sie den vollen Kontext × 0,1.

## Der eigentliche Hebel: weniger Anfragen

Gemessen: 147 Anfragen, 13 vom Nutzer; eigene Ausgabe = 23 % der Kosten. Ziele, in Reihenfolge:
**weniger Anfragen · kürzere eigene Ausgabe · kleinerer Kontext.** Techniken: alle unabhängigen
Lesevorgänge in einer Antwort bündeln · ein Skript, das zehn Dinge tut und eine Zusammenfassung
druckt · Ausgabe vorfiltern (`grep`/`tail`) · grep statt ganze Dateien lesen · keine Status-
Nachrichten pro Agent (eine Zusammenfassung, wenn die Flotte landet) · Berichte als Dateien, nicht
im Chat · Budget für eigene Ausgabe: Zwischenstand ≤ 100 Wörter, final ≤ 500, Details in Dateien.
Terminal-Tab-Vorschläge und jede Agenten-Fertigmeldung sind ebenfalls volle Anfragen.

## Subagenten — die Standardarbeitsweise

- **Wächter-Agent (Guardian).** Für eine Bau-Welle bekommt EIN orchestrierender Agent (Opus,
  low/normal Effort) den ganzen Plan als Datei, startet die Arbeits-Agenten selbst, merged,
  testet, bündelt, räumt `.build` von gemergten Worktrees auf, schreibt den Bericht — die
  Hauptsitzung wird EINMAL geweckt statt einmal pro Agent (8 → 1 Meldungen ≈ 140k gespart bei 190k Kontext).
  Fragen der Arbeiter landen beim Wächter, also müssen die Aufträge vollständig sein: Pfade, Ziel,
  Grenzen, Abnahmekriterien, "keine Rückfragen — entscheiden, die Annahme dokumentieren".
- **Der Wächter startet alle Arbeiter gleichzeitig, in EINER Nachricht** (ein Batch von Agent-
  Aufrufen), nie nacheinander — ein serieller Schwanz von Arbeitern macht aus einer günstigen
  Welle eine lange. Der ERSTE Schritt jedes Arbeiters ist, den aktuellen Branch-Tip zu ziehen
  (`git pull` / `git fetch && git rebase`), bevor er irgendeine Datei anfasst, damit er nie auf
  einer veralteten Basis baut.
- **Agenten auf ~30 Minuten, EINEN Auftrag kürzen** (nicht 40 Minuten / 2–3 Aufgaben — ein einziger
  fokussierter Auftrag landet schneller und lässt sich leichter mergen). Längere Arbeit liefert in
  eine DATEI (`docs/reviews/<datum>-<thema>.md`) und berichtet nur den Pfad; das Handoff listet
  die erwarteten Dateien, und die nächste Sitzung prüft zuerst mit `ls`. Nie auf einen Nachzügler warten.
- **Jeden Arbeiter-Branch sofort bei Landung mergen**, Merges nicht für später sammeln — Konflikte
  sind einzeln billiger zu lösen, direkt solange die Arbeit frisch ist. Die VOLLE Testsuite nur
  EINMAL laufen lassen, ganz am Ende, gegen das gemergte Ergebnis; ein wackelnder/fehlschlagender
  Einzeltest wird für sich untersucht statt die ganze Suite erneut zu fahren.
- **Der Wächter schreibt nach 60 Minuten eine Zwischenstand-Datei**, falls die Welle noch läuft
  (Pfad im kommenden Handoff, z. B. `docs/wellen/<datum>-zwischenstand.md`) — damit eine Sitzung,
  die mitten in der Welle nachschaut, oder ein Handoff, das vor Fertigstellung des Wächters
  geschrieben wird, etwas Reales zum Zeigen hat. **Das Handoff startet auch ohne fertigen Wächter**:
  den Wächter und seine noch laufenden Arbeiter unter "erwartete Agenten-Ergebnisse" listen,
  die nächste Sitzung prüft sie nach.
- **Modell + Effort im sichtbaren Label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
  Fable 5 als Subagent: **immer Effort low**; für schwieriges Review/Design Opus oder eine zweite
  Architektur (Codex/GPT) nutzen. Nie die eigene Ausgabe selbst reviewen — an Codex weiterleiten.
- **Agenten testen vor dem Nutzer.** Volle Suite + ein QA-Agent, der die App startet und jeden
  Testpunkt einmal anklickt; der Nutzer sollte meist nur "funktioniert, danke" sagen. **Der QA-
  Agent schließt die Fenster/Prozesse, die er zum Testen geöffnet hat**, bevor er fertig meldet —
  der Nutzer soll keinen Haufen liegengebliebener Testinstanzen erben.
- Berichtsvertrag: ≤ 300 Wörter, Status/Entscheidungen/Belege-mit-Pfaden/Risiken/Nächstes; keine
  Chronik, keine eingefügten Logs. Subagenten-Token zählen trotzdem aufs Wochenkontingent — was sie
  sparen, ist der HAUPTkontext (jeder Schritt ≈ 1/5 der Kosten, und nichts davon bleibt in der Sitzung).
- Taktung: Nutzer anwesend + in Eile → parallel; Nutzer abwesend → seriell (jede Fertigmeldung
  hält den Cache warm). Nie Beschäftigungstherapie erfinden.

## Bezahltes Kontingent — sehen, nutzen, nach Kontogröße

- `~/.claude/codex-limit.sh [--kurz|--json]` liest Codex `rate_limits` aus dessen letzter Session-
  Datei — nur so frisch wie der letzte Codex-Lauf; `null` = unbekannt, nicht 0. Einmal pro Sitzung
  einen kleinen Ping an den ersten echten Codex-Aufruf anhängen (`codex exec --skip-git-repo-check
  "Antworte nur mit: bereit"`). Claude-Code-Kontingent: `cat ~/.claude/.claude-kontingent`
  (5h/7d %, von der Statuszeile geschrieben; die Web-UI ist die Autorität bei Abweichungen).
- Handoff-Block "Was noch im Tank ist" direkt nach dem Status: Zahlen + Alter der Messung +
  ein KONKRETER Vorschlag, wenn viel frei ist (großes Review, langer Testlauf, Zweitmeinung).
  Ungenutztes Kontingent verfällt. Gemini/OpenRouter: kein auslesbares Guthaben — so sagen, nie schätzen.
- **Kleines Codex-Konto (Plus, ~20 $)** → Codex macht NUR QA: Review, Zweitmeinung, Testläufe,
  Abnahme. Keine Bau-Aufträge, kein "mach um 23:05 weiter". Großes Konto → frei nutzen.

## Der Wellen-Workflow und die Handoff-Datei

Das Handoff nach jeder großen Welle schreiben, ungefragt. Pfad `<projekt>/_handoff-<projekt>-JJJJ-MM-TT[-b].md`
(Projektname im Dateinamen UND im Titel). Fließtext bei ~60–70 Zeichen umbrechen; Befehle,
Pfade, URLs auf einer Zeile. Referenzieren, nicht kopieren (Pfade/URLs); Geheimnisse schwärzen;
Skills für die nächste Sitzung nennen. Struktur, von oben nach unten:

1. Titel mit Datum/Uhrzeit. Dann die Kopierzeile für die nächste Sitzung:
   `> \`Ich habe das Handoff beantwortet: /abs/pfad/_handoff-….md\``
   plus "du kannst direkt in diese Datei schreiben — Zeilen mit >>> oder Name + Zeitstempel beginnen".
2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   (`- [ ] Pfad (Agent, gestartet HH:MM)`).
3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — den Sammelbereich des
   vorigen Handoffs UNMITTELBAR vor dem Schreiben lesen (im selben Tool-Aufruf wie der
   Ungespeichert-Wächter, inklusive ungespeichertem Editor-Text) und WÖRTLICH kopieren, dann
   ein Block "Was ich daraus gemacht habe", der jeden Punkt auf gebaut / beantwortet / Roadmap
   abbildet. Auch das Handoff DAVOR auf Nachträge prüfen. Nie den Text des Nutzers umschreiben.
4. Vorige Testantworten → was daraus wurde, eine Zeile je Punkt ("deine T1-Antwort übernommen
   als: … — richtig?"). Unbeantwortete Punkte werden markiert übernommen.
5. **Testliste vN** — jeder Punkt vorbelegt mit einer leeren `>>>Userantwort:`-Zeile.
6. Banner (Markdown-Überschriften fallen in TextEdit nicht auf — Linien und Großbuchstaben schon):
   ```
   ═══════════════════════════════════════════════════════════
      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   ═══════════════════════════════════════════════════════════
   >>>Userantwort:
   ```
7. **Der rote Faden** — die nächsten 2–3 Wellen als kurze Absätze, jeweils mit
   `>>>Hast du dazu noch was anzumerken?`; danach ein kompakter Themenspeicher; dann
   **Hauptdokumente** (3–6 echte Dateien mit absolutem Pfad + einer Zeile + Aktualität).
8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (Einheit = Spanne zwischen zwei
   Nutzer-Nachrichten; k = Tausend erklären, Kontextspalte ≠ Kosten) + ehrliche Befunde, dann die
   Schlusszeile mit GEMESSENEM Kontext und Startkontext: *"Kontext dieser Session: 192k
   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit `aus: /abs/pfad` und einem leeren `>>>`.
   Der Nutzer sammelt hier, während die nächste Welle läuft — Sammeln kostet null Anfragen.

Fragen an den Nutzer gehören ins Handoff (`## Fragen an dich` mit `>>>Antwort:`), nicht in den
Chat: eine Chat-Frage blockiert eine Welle, zehn in der Datei blockieren nichts. Wellen so
zuschneiden, dass sie ohne Rückfrage durchlaufen; die wahrscheinlichere Lesart nehmen und dokumentieren.

## Editor-Regeln (macOS / TextEdit)

- Jedes nutzerseitige Dokument sofort öffnen: `open -a TextEdit <datei>`. Das gilt für jedes
  neu erwähnte Dokument, nicht nur das Handoff — einen Plan, einen QA-Bericht, eine Review-
  Datei: sobald es existiert und für den Nutzer zum Lesen gedacht ist, öffnen. Einmal anbieten:
  Tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt Standardschrift
  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md`-Standardapp via `duti`.
- **Ungespeichert-Wächter vor dem Lesen:**
  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
  falls geändert, den Live-Text lesen (`… get text of (first document whose name is "…")`).
- **Nie in das offene Handoff des Nutzers schreiben, es schließen, speichern oder verschieben.**
  Ein neues Handoff ist immer eine NEUE Datei. Alte nach `handoff-archiv/` archivieren (mv, nie rm)
  erst nachdem der Nutzer sie geschlossen hat; sonst "Archivierung ausstehend" im neuen Handoff vermerken.
- Wenn Claude eine vom Nutzer geöffnete Datei bearbeitet hat und sie unverändert ist → schließen
  + neu öffnen, damit die neue Version sichtbar wird; geändert → fragen, nie schließen.
- Einmal sagen: lange Diktate gehören ins Handoff-Dokument, kurze Befehle ins Terminal (Terminals
  klappen lange Eingaben zu `[pasted text]` zusammen); TextEdit ▸ Ablage ▸ Zuletzt geöffnet findet
  verlorene Handoffs.

## Cache-Neuaufbau — erkennen, nicht raten

Trefferquote = Σ cache_creation / Σ cache_read aus der Session-JSONL; < 10 % = warm. Große
Einzel-Schreibvorgänge sind meist Anhänge, keine Neuaufbauten. Einen Neuaufbau EINMAL erwähnen,
mit Ursache, nur wenn sie ableitbar ist: Lücke > 60 Min zwischen zwei `date`-Lesungen, ein Modell-/
Effort-Wechsel, eine CLAUDE.md-Bearbeitung, ein MCP-Neustart. Unbekannte Ursache → nichts sagen.
Kosten als Arithmetik erklären ("22k, weil der Kontext 220k groß ist und Lesen ×0,1 kostet"), nie
als Behauptung; eigene frühere Fehlaussagen explizit korrigieren.

## Logbuch und Setup

Pro Handoff eine Zeile an `~/.claude/warm-handoff-log.md` anhängen:
`| 22.08.2026 14:40 | ctx 85k | 2 Wellen | Neuaufbauten: 1 (Pause 90min) | geschätzte Verschwendung ~60k |`
Muster alle ~50 Einträge zusammenfassen. Immer aktiv: "Zu Beginn jeder Sitzung den warm-handoff-
Skill aufrufen." in `~/.claude/CLAUDE.md` ergänzen. Skripte: `scripts/ctx.sh`,
`scripts/session-costs.sh`, `scripts/codex-limit.sh` → nach `~/.claude/` kopieren.
Terminal-neutral: "deine Statuszeile" sagen, nicht ein Feld eines bestimmten Hosts.

hook: PostToolUse
hook: PostToolUse Completed
codex
The core workflow is understandable, but I’ve already found several operational conflicts—especially around agent pacing, cache accounting, and script naming. I’m checking exact line references and parity between the two language versions now.
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba SKILL.md | sed -n '1,230p'; nl -ba SKILL.de.md | sed -n '1,230p'; rg --files scripts references 2>/dev/null || true; rg -n \"session-(kosten|costs)|ctx\\.sh|codex-limit|every reply|Every reply|Jede Antwort|one-liners|Einzeilern|parallel|sequential|seriell|starts every worker|Subagents|Subagenten|Never review|Nie die eigene|Questions for the user|Fragen an den Nutzer|Always-on|Immer aktiv\" SKILL.md SKILL.de.md" in /Users/pro16/Code/warm-handoff
 succeeded in 0ms:
     1	---
     2	name: warm-handoff
     3	description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, warns before cache-destroying actions, recommends a fresh session past a context threshold, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", or when resuming after a gap.
     4	---
     5	
     6	# warm-handoff — ride the cache wave, hand off before it breaks 🏄
     7	
     8	**One sentence:** Handoff → fresh session → handoff. The user collects everything
     9	(test answers, ideas, critique) in ONE handoff file over hours, starts a fresh session,
    10	the agent works it all off through a few subagents and writes the next handoff.
    11	Full history with dated user quotes and the reasoning behind every rule:
    12	`references/historie.md` (read it when a rule here seems odd — do not load it by default).
    13	
    14	## The facts (Claude Code docs, 2026-08)
    15	
    16	- Pro/Max: **1-hour sliding cache TTL** — every request resets it. Subagents: strict 5 min.
    17	- Cache killers regardless of clock: mid-session `/model` or `/effort` change, editing
    18	  CLAUDE.md/system prompt, MCP server restart. Set model + effort at session START.
    19	- Prices relative to fresh input: **cache read ×0.1 · cache write ×2 (1-h TTL) · own output ×5.**
    20	- Every request re-reads the whole prefix. Cost = requests × context. The user's messages
    21	  are a rounding error; the agent's own tool steps and reports are the bill.
    22	
    23	## Every reply — three honesty rules
    24	
    25	1. **Timestamp from a `date` call in THAT reply** (`date "+%d.%m.%Y %H:%M"`, piggybacked on
    26	   any command). No `date` this turn → no timestamp. Never extrapolate, never `~19:40`.
    27	2. **Never guess context size.** Sources: the user's status line, or `~/.claude/ctx.sh`
    28	   appended to a command that runs anyway (`date … && ~/.claude/ctx.sh`). It reads the
    29	   session JSONL (`cache_read + cache_creation` of the last request). None → "not measured".
    30	3. **Cost line under every substantive reply**, from the LAST COMPLETED request, labeled so:
    31	   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
    32	   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Skip it on one-liners. If a round cost > 2× the
    33	   session's average, say why ONCE per wave, kindly, with the cheaper path — the cause is
    34	   almost always the agent (whole files read, raw output, long replies), not the user.
    35	
    36	## Sweetspot — when to hand off
    37	
    38	| What comes next | Hand off at |
    39	|---|---|
    40	| Big build/review wave (hundreds of tool steps) | ~200k |
    41	| Mixed | ~250k |
    42	| Only talk / small edits | ~300k |
    43	| Anything | 400k hard ceiling |
    44	
    45	Break-even for a fresh session: `(start_ctx × 2) / ((old_ctx − start_ctx) × 0.1)` steps.
    46	Start context is MEASURED per project (82–125k seen), never assumed "~20k". Steps = tool
    47	calls, not user messages. Talking on a fat context is cheap; working on it is not.
    48	Say it at every wave end, casually: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
    49	While the agent's own tool loop runs, a user message is nearly free (attached to the next
    50	request); while subagents run or the agent idles, it costs the full context × 0.1.
    51	
    52	## The real lever: fewer requests
    53	
    54	Measured: 147 requests, 13 from the user; own output = 23 % of cost. Targets, in order:
    55	**fewer requests · shorter own output · smaller context.** Techniques: batch all independent
    56	reads in one reply · one script that does ten things and prints one summary · pre-filter
    57	output (`grep`/`tail`) · grep instead of reading whole files · no per-agent status messages
    58	(one summary when the fleet lands) · reports as files, not chat · own output budget:
    59	interim ≤ 100 words, final ≤ 500, details in files. Terminal tab-suggestions and every
    60	agent completion notification are full requests too.
    61	
    62	## Subagents — the default way to work
    63	
    64	- **Guardian agent (Wächter).** For a build wave, ONE orchestrating agent (Opus, low/normal
    65	  effort) gets the whole plan as a file, spawns the worker agents itself, merges, tests,
    66	  bundles, cleans `.build` of merged worktrees, writes the report — the main session is
    67	  woken ONCE instead of once per agent (8 → 1 notifications ≈ 140k saved at 190k ctx).
    68	  Workers' questions land at the guardian, so briefs must be complete: paths, goal,
    69	  limits, acceptance criteria, "no questions — decide, document the assumption".
    70	- **The guardian starts every worker at once, in a single message** (one batch of Agent
    71	  calls), never one after another — a serial tail of workers is what turns a cheap wave
    72	  into a long one. Each worker's FIRST step is to pull the current branch tip (`git pull`
    73	  / `git fetch && git rebase`) before touching any file, so it never builds on a stale base.
    74	- **Cut agents to ~30 minutes, ONE task each** (not 40 minutes / 2–3 tasks — a single focused
    75	  job lands faster and is easier to merge). Longer work delivers into a FILE
    76	  (`docs/reviews/<date>-<topic>.md`) and reports only the path; the handoff lists the
    77	  expected files and the next session checks `ls` first. Never wait for a straggler.
    78	- **Merge each worker's branch the moment it lands**, don't batch merges for later — conflicts
    79	  are cheaper to resolve one at a time, right after the work is fresh. Run the FULL test
    80	  suite only ONCE, at the very end, against the merged result; a flaky/failing individual
    81	  test gets investigated on its own rather than re-running the whole suite.
    82	- **Guardian writes an interim status file after 60 minutes** if the wave is still running
    83	  (path in the handoff-to-be, e.g. `docs/wellen/<date>-zwischenstand.md`) — so a session that
    84	  checks in mid-wave, or a handoff written before the guardian finishes, has something real
    85	  to point to. **The handoff starts even without a finished guardian**: list the guardian and
    86	  its still-running workers under "expected agent results", the next session checks them.
    87	- **Model + effort in the visible label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
    88	  Fable 5 as subagent: **always effort low**; for hard review/design use Opus or a second
    89	  architecture (Codex/GPT). Never review your own output yourself — route to Codex.
    90	- **Agents test before the user.** Full suite + a QA agent that launches the app and clicks
    91	  every test item once; the user should mostly say "works, thanks". **The QA agent closes
    92	  the windows/processes it opened for testing** before it reports done — the user shouldn't
    93	  inherit a pile of leftover test instances.
    94	- Report contract: ≤ 300 words, status/decisions/evidence-with-paths/risks/next; no
    95	  chronicle, no pasted logs. Subagent tokens still hit the weekly quota — what they save is
    96	  the MAIN context (each step ≈ 1/5 the cost, and nothing of it stays in the session).
    97	- Pacing: user present + in a hurry → parallel; user away → sequential (each completion
    98	  keeps the cache warm). Never invent busywork.
    99	
   100	## Paid quota — see it, use it, by account size
   101	
   102	- `~/.claude/codex-limit.sh [--kurz|--json]` reads Codex `rate_limits` from its last session
   103	  file — only as fresh as the last Codex run; `null` = unknown, not 0. Once per session send
   104	  a tiny ping attached to the first real Codex call (`codex exec --skip-git-repo-check
   105	  "Antworte nur mit: bereit"`). Claude Code quota: `cat ~/.claude/.claude-kontingent`
   106	  (5h/7d %, written by the status line; web UI is the authority when they differ).
   107	- Handoff block "Was noch im Tank ist" right after the status: numbers + measurement age +
   108	  a CONCRETE proposal if lots is free (big review, long test run, second opinion). Unused
   109	  quota expires. Gemini/OpenRouter: no readable balance — say so, never estimate.
   110	- **Small Codex account (Plus, ~20 $)** → Codex does ONLY QA: review, second opinion,
   111	  test runs, acceptance. No build jobs, no "continue at 23:05". Large account → use freely.
   112	
   113	## The wave workflow and the handoff file
   114	
   115	Write the handoff after every big wave, unprompted. Path `<project>/_handoff-<projekt>-YYYY-MM-DD[-b].md`
   116	(project name in the file name AND title). Hard-wrap prose at ~60–70 chars; commands,
   117	paths, URLs on one line. Reference, don't copy (paths/URLs); redact secrets; name skills
   118	for the next session. Structure, top to bottom:
   119	
   120	1. Title with date/time. Then the copy-line for the next session:
   121	   `> \`Ich habe das Handoff beantwortet: /abs/path/_handoff-….md\``
   122	   plus "you can write directly in this file — start lines with >>> or name + timestamp".
   123	2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   124	   (`- [ ] path (agent, started HH:MM)`).
   125	3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — read the previous
   126	   handoff's collection area IMMEDIATELY before writing (same tool call as the unsaved-
   127	   changes guard, including unsaved editor text) and copy it VERBATIM, then a block
   128	   "Was ich daraus gemacht habe" mapping each item → built / answered / roadmap.
   129	   Also check the handoff BEFORE that one for late additions. Never rewrite the user's text.
   130	4. Previous test answers → what became of them, one line each ("your T1 answer taken as:
   131	   … — correct?"). Unanswered items carry over, marked.
   132	5. **Testliste vN** — every item pre-seeded with an empty `>>>Userantwort:` line.
   133	6. Banner (Markdown headings don't stand out in TextEdit — lines and caps do):
   134	   ```
   135	   ═══════════════════════════════════════════════════════════
   136	      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
   137	      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   138	   ═══════════════════════════════════════════════════════════
   139	   >>>Userantwort:
   140	   ```
   141	7. **Der rote Faden** — next 2–3 waves as short paragraphs, each with
   142	   `>>>Hast du dazu noch was anzumerken?`; then a compact Themenspeicher; then
   143	   **Hauptdokumente** (3–6 real files with absolute path + one line + freshness).
   144	8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (unit = span between two
   145	   user messages; explain k = thousand, context column ≠ cost) + honest findings, then the
   146	   closing line with MEASURED context and start context: *"Kontext dieser Session: 192k
   147	   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
   148	9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** with `aus: /abs/path` and an empty `>>>`.
   149	   The user collects here while the next wave runs — collecting costs zero requests.
   150	
   151	Questions for the user go into the handoff (`## Fragen an dich` with `>>>Antwort:`),
   152	not the chat: one chat question blocks a wave, ten in the file block nothing. Cut waves
   153	so they run through without asking; take the likelier reading and document it.
   154	
   155	## Editor rules (macOS / TextEdit)
   156	
   157	- Open every user-facing document immediately: `open -a TextEdit <file>`. This applies to any
   158	  newly mentioned document, not only the handoff — a plan, a QA report, a review file: the
   159	  moment it exists and is meant for the user to read, open it. Offer once:
   160	  tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt default font
   161	  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md` default app via `duti`.
   162	- **Unsaved-changes guard before reading:**
   163	  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
   164	  if modified, read the live text (`… get text of (first document whose name is "…")`).
   165	- **Never write into, close, save or move the handoff the user has open.** A new handoff is
   166	  always a NEW file. Archive old ones to `handoff-archiv/` (mv, never rm) only after the
   167	  user closed them; otherwise note "archiving pending" in the new handoff.
   168	- If Claude edited a file the user has open and it is unmodified → close + reopen so they
   169	  see the new version; modified → ask, never close.
   170	- Say once: long dictation belongs in the handoff file, short commands in the terminal
   171	  (terminals collapse long input to `[pasted text]`); TextEdit ▸ File ▸ Open Recent finds
   172	  lost handoffs.
   173	
   174	## Cache rebuild — detect, don't guess
   175	
   176	Hit rate = Σ cache_creation / Σ cache_read from the session JSONL; < 10 % = warm. Big
   177	single writes are usually appends, not rebuilds. Mention a rebuild ONCE, with the cause,
   178	only when it is derivable: gap > 60 min between two `date` reads, a model/effort switch,
   179	a CLAUDE.md edit, an MCP restart. Unknown cause → say nothing. Explain costs as arithmetic
   180	("22k because context is 220k and reads cost ×0.1"), never as assertion; correct your own
   181	earlier misstatements explicitly.
   182	
   183	## Logbook and setup
   184	
   185	Append one line per handoff to `~/.claude/warm-handoff-log.md`:
   186	`| 22.08.2026 14:40 | ctx 85k | 2 waves | rebuilds: 1 (pause 90min) | est. waste ~60k |`
   187	Summarize patterns every ~50 entries. Always-on: add "At the start of every session,
   188	invoke the warm-handoff skill." to `~/.claude/CLAUDE.md`. Scripts: `scripts/ctx.sh`,
   189	`scripts/session-costs.sh`, `scripts/codex-limit.sh` → copy to `~/.claude/`.
   190	Terminal-neutral: say "your status line", not a specific host's field.
     1	---
     2	name: warm-handoff
     3	description: Zu Beginn jeder Arbeitssitzung und vor jeder längeren Pause nutzen — verfolgt das Claude-Code-Prompt-Cache-Fenster (1 Stunde gleitendes TTL auf Pro/Max), versieht jede Antwort mit einem Zeitstempel, damit der Nutzer das Fenster selbst sieht, warnt vor cache-zerstörenden Aktionen, empfiehlt ab einer Kontext-Schwelle eine frische Sitzung und schreibt ein Handoff-Dokument (mit der Testliste des Nutzers darin), damit die nächste Sitzung günstig und vollständig informiert startet. Auslöser: „cache", „handoff", „Pause", „frische Sitzung", „Welle fertig" oder beim Wiedereinstieg nach einer Lücke.
     4	---
     5	
     6	# warm-handoff — die Cache-Welle reiten, übergeben bevor sie bricht 🏄
     7	
     8	**Ein Satz:** Handoff → frische Session → Handoff. Der Nutzer sammelt alles
     9	(Testantworten, Ideen, Kritik) in EINEM Handoff-Dokument über Stunden, startet
    10	eine frische Session, der Agent arbeitet alles durch mehrere Subagenten ab und
    11	schreibt das nächste Handoff.
    12	Vollständige Historie mit datierten Nutzer-Zitaten und der Begründung jeder Regel:
    13	`references/historie.md` (lesen, wenn eine Regel hier seltsam wirkt — nicht standardmäßig laden).
    14	
    15	## Die Fakten (Claude-Code-Doku, 2026-08)
    16	
    17	- Pro/Max: **1 Stunde gleitendes Cache-TTL** — jede Anfrage setzt es zurück. Subagenten: strikt 5 Min.
    18	- Cache-Killer unabhängig von der Uhr: `/model`- oder `/effort`-Wechsel mitten in der Sitzung,
    19	  CLAUDE.md/Systemprompt bearbeiten, MCP-Server-Neustart. Modell + Effort beim Sitzungsstart festlegen.
    20	- Preise relativ zu frischem Input: **Cache-Lesen ×0,1 · Cache-Schreiben ×2 (1-h-TTL) · eigene Ausgabe ×5.**
    21	- Jede Anfrage liest den gesamten Prefix neu. Kosten = Anfragen × Kontext. Die Nachrichten
    22	  des Nutzers sind ein Rundungsfehler; die eigenen Tool-Schritte und Berichte des Agenten sind die Rechnung.
    23	
    24	## Jede Antwort — drei Ehrlichkeitsregeln
    25	
    26	1. **Zeitstempel aus einem `date`-Aufruf IN DIESER Antwort** (`date "+%d.%m.%Y %H:%M"`,
    27	   huckepack auf einen ohnehin laufenden Befehl). Kein `date` in dieser Runde → kein Zeitstempel.
    28	   Nie extrapolieren, nie `~19:40`.
    29	2. **Nie die Kontextgröße raten.** Quellen: die Statuszeile des Nutzers oder `~/.claude/ctx.sh`,
    30	   angehängt an einen ohnehin laufenden Befehl (`date … && ~/.claude/ctx.sh`). Es liest die
    31	   Session-JSONL (`cache_read + cache_creation` der letzten Anfrage). Keine → "nicht gemessen".
    32	3. **Kostenzeile unter jeder inhaltlichen Antwort**, aus der LETZTEN ABGESCHLOSSENEN Anfrage, so beschriftet:
    33	   *Letzte gemessene Anfrage: 366k gelesen (×0,1) + 0,4k geschrieben (×2) + 2,9k Ausgabe (×5)
    34	   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Bei Einzeilern weglassen. Wenn eine Runde > 2× den
    35	   Sitzungsdurchschnitt kostet, EINMAL pro Welle freundlich sagen warum, mit dem günstigeren Weg —
    36	   die Ursache liegt fast immer beim Agenten (ganze Dateien gelesen, Rohausgabe, lange Antworten), nicht beim Nutzer.
    37	
    38	## Sweetspot — wann übergeben
    39	
    40	| Was als Nächstes kommt | Übergabe bei |
    41	|---|---|
    42	| Große Bau-/Review-Welle (Hunderte Tool-Schritte) | ~200k |
    43	| Gemischt | ~250k |
    44	| Nur Gespräch / kleine Edits | ~300k |
    45	| Alles | 400k harte Obergrenze |
    46	
    47	Break-even für eine frische Session: `(Start-Kontext × 2) / ((alter_Kontext − Start-Kontext) × 0,1)` Schritte.
    48	Der Startkontext wird pro Projekt GEMESSEN (82–125k gesehen), nie als "~20k" angenommen. Schritte = Tool-
    49	Aufrufe, nicht Nutzer-Nachrichten. Reden auf fettem Kontext ist billig; Arbeiten darauf nicht.
    50	Bei jedem Wellenende beiläufig sagen: "Kontext 148k, Ziel 200k — reicht für ~1 Welle."
    51	Während die eigene Tool-Schleife des Agenten läuft, ist eine Nutzer-Nachricht fast gratis (hängt
    52	sich an die nächste Anfrage an); während Subagenten laufen oder der Agent leerläuft, kostet sie den vollen Kontext × 0,1.
    53	
    54	## Der eigentliche Hebel: weniger Anfragen
    55	
    56	Gemessen: 147 Anfragen, 13 vom Nutzer; eigene Ausgabe = 23 % der Kosten. Ziele, in Reihenfolge:
    57	**weniger Anfragen · kürzere eigene Ausgabe · kleinerer Kontext.** Techniken: alle unabhängigen
    58	Lesevorgänge in einer Antwort bündeln · ein Skript, das zehn Dinge tut und eine Zusammenfassung
    59	druckt · Ausgabe vorfiltern (`grep`/`tail`) · grep statt ganze Dateien lesen · keine Status-
    60	Nachrichten pro Agent (eine Zusammenfassung, wenn die Flotte landet) · Berichte als Dateien, nicht
    61	im Chat · Budget für eigene Ausgabe: Zwischenstand ≤ 100 Wörter, final ≤ 500, Details in Dateien.
    62	Terminal-Tab-Vorschläge und jede Agenten-Fertigmeldung sind ebenfalls volle Anfragen.
    63	
    64	## Subagenten — die Standardarbeitsweise
    65	
    66	- **Wächter-Agent (Guardian).** Für eine Bau-Welle bekommt EIN orchestrierender Agent (Opus,
    67	  low/normal Effort) den ganzen Plan als Datei, startet die Arbeits-Agenten selbst, merged,
    68	  testet, bündelt, räumt `.build` von gemergten Worktrees auf, schreibt den Bericht — die
    69	  Hauptsitzung wird EINMAL geweckt statt einmal pro Agent (8 → 1 Meldungen ≈ 140k gespart bei 190k Kontext).
    70	  Fragen der Arbeiter landen beim Wächter, also müssen die Aufträge vollständig sein: Pfade, Ziel,
    71	  Grenzen, Abnahmekriterien, "keine Rückfragen — entscheiden, die Annahme dokumentieren".
    72	- **Der Wächter startet alle Arbeiter gleichzeitig, in EINER Nachricht** (ein Batch von Agent-
    73	  Aufrufen), nie nacheinander — ein serieller Schwanz von Arbeitern macht aus einer günstigen
    74	  Welle eine lange. Der ERSTE Schritt jedes Arbeiters ist, den aktuellen Branch-Tip zu ziehen
    75	  (`git pull` / `git fetch && git rebase`), bevor er irgendeine Datei anfasst, damit er nie auf
    76	  einer veralteten Basis baut.
    77	- **Agenten auf ~30 Minuten, EINEN Auftrag kürzen** (nicht 40 Minuten / 2–3 Aufgaben — ein einziger
    78	  fokussierter Auftrag landet schneller und lässt sich leichter mergen). Längere Arbeit liefert in
    79	  eine DATEI (`docs/reviews/<datum>-<thema>.md`) und berichtet nur den Pfad; das Handoff listet
    80	  die erwarteten Dateien, und die nächste Sitzung prüft zuerst mit `ls`. Nie auf einen Nachzügler warten.
    81	- **Jeden Arbeiter-Branch sofort bei Landung mergen**, Merges nicht für später sammeln — Konflikte
    82	  sind einzeln billiger zu lösen, direkt solange die Arbeit frisch ist. Die VOLLE Testsuite nur
    83	  EINMAL laufen lassen, ganz am Ende, gegen das gemergte Ergebnis; ein wackelnder/fehlschlagender
    84	  Einzeltest wird für sich untersucht statt die ganze Suite erneut zu fahren.
    85	- **Der Wächter schreibt nach 60 Minuten eine Zwischenstand-Datei**, falls die Welle noch läuft
    86	  (Pfad im kommenden Handoff, z. B. `docs/wellen/<datum>-zwischenstand.md`) — damit eine Sitzung,
    87	  die mitten in der Welle nachschaut, oder ein Handoff, das vor Fertigstellung des Wächters
    88	  geschrieben wird, etwas Reales zum Zeigen hat. **Das Handoff startet auch ohne fertigen Wächter**:
    89	  den Wächter und seine noch laufenden Arbeiter unter "erwartete Agenten-Ergebnisse" listen,
    90	  die nächste Sitzung prüft sie nach.
    91	- **Modell + Effort im sichtbaren Label**: `Opus5/high · Verlauf-Tempo`, `Fable/low · Scan`.
    92	  Fable 5 als Subagent: **immer Effort low**; für schwieriges Review/Design Opus oder eine zweite
    93	  Architektur (Codex/GPT) nutzen. Nie die eigene Ausgabe selbst reviewen — an Codex weiterleiten.
    94	- **Agenten testen vor dem Nutzer.** Volle Suite + ein QA-Agent, der die App startet und jeden
    95	  Testpunkt einmal anklickt; der Nutzer sollte meist nur "funktioniert, danke" sagen. **Der QA-
    96	  Agent schließt die Fenster/Prozesse, die er zum Testen geöffnet hat**, bevor er fertig meldet —
    97	  der Nutzer soll keinen Haufen liegengebliebener Testinstanzen erben.
    98	- Berichtsvertrag: ≤ 300 Wörter, Status/Entscheidungen/Belege-mit-Pfaden/Risiken/Nächstes; keine
    99	  Chronik, keine eingefügten Logs. Subagenten-Token zählen trotzdem aufs Wochenkontingent — was sie
   100	  sparen, ist der HAUPTkontext (jeder Schritt ≈ 1/5 der Kosten, und nichts davon bleibt in der Sitzung).
   101	- Taktung: Nutzer anwesend + in Eile → parallel; Nutzer abwesend → seriell (jede Fertigmeldung
   102	  hält den Cache warm). Nie Beschäftigungstherapie erfinden.
   103	
   104	## Bezahltes Kontingent — sehen, nutzen, nach Kontogröße
   105	
   106	- `~/.claude/codex-limit.sh [--kurz|--json]` liest Codex `rate_limits` aus dessen letzter Session-
   107	  Datei — nur so frisch wie der letzte Codex-Lauf; `null` = unbekannt, nicht 0. Einmal pro Sitzung
   108	  einen kleinen Ping an den ersten echten Codex-Aufruf anhängen (`codex exec --skip-git-repo-check
   109	  "Antworte nur mit: bereit"`). Claude-Code-Kontingent: `cat ~/.claude/.claude-kontingent`
   110	  (5h/7d %, von der Statuszeile geschrieben; die Web-UI ist die Autorität bei Abweichungen).
   111	- Handoff-Block "Was noch im Tank ist" direkt nach dem Status: Zahlen + Alter der Messung +
   112	  ein KONKRETER Vorschlag, wenn viel frei ist (großes Review, langer Testlauf, Zweitmeinung).
   113	  Ungenutztes Kontingent verfällt. Gemini/OpenRouter: kein auslesbares Guthaben — so sagen, nie schätzen.
   114	- **Kleines Codex-Konto (Plus, ~20 $)** → Codex macht NUR QA: Review, Zweitmeinung, Testläufe,
   115	  Abnahme. Keine Bau-Aufträge, kein "mach um 23:05 weiter". Großes Konto → frei nutzen.
   116	
   117	## Der Wellen-Workflow und die Handoff-Datei
   118	
   119	Das Handoff nach jeder großen Welle schreiben, ungefragt. Pfad `<projekt>/_handoff-<projekt>-JJJJ-MM-TT[-b].md`
   120	(Projektname im Dateinamen UND im Titel). Fließtext bei ~60–70 Zeichen umbrechen; Befehle,
   121	Pfade, URLs auf einer Zeile. Referenzieren, nicht kopieren (Pfade/URLs); Geheimnisse schwärzen;
   122	Skills für die nächste Sitzung nennen. Struktur, von oben nach unten:
   123	
   124	1. Titel mit Datum/Uhrzeit. Dann die Kopierzeile für die nächste Sitzung:
   125	   `> \`Ich habe das Handoff beantwortet: /abs/pfad/_handoff-….md\``
   126	   plus "du kannst direkt in diese Datei schreiben — Zeilen mit >>> oder Name + Zeitstempel beginnen".
   127	2. **Der Stand in drei Sätzen** · **Was noch im Tank ist** · **Erwartete Agenten-Ergebnisse**
   128	   (`- [ ] Pfad (Agent, gestartet HH:MM)`).
   129	3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** — den Sammelbereich des
   130	   vorigen Handoffs UNMITTELBAR vor dem Schreiben lesen (im selben Tool-Aufruf wie der
   131	   Ungespeichert-Wächter, inklusive ungespeichertem Editor-Text) und WÖRTLICH kopieren, dann
   132	   ein Block "Was ich daraus gemacht habe", der jeden Punkt auf gebaut / beantwortet / Roadmap
   133	   abbildet. Auch das Handoff DAVOR auf Nachträge prüfen. Nie den Text des Nutzers umschreiben.
   134	4. Vorige Testantworten → was daraus wurde, eine Zeile je Punkt ("deine T1-Antwort übernommen
   135	   als: … — richtig?"). Unbeantwortete Punkte werden markiert übernommen.
   136	5. **Testliste vN** — jeder Punkt vorbelegt mit einer leeren `>>>Userantwort:`-Zeile.
   137	6. Banner (Markdown-Überschriften fallen in TextEdit nicht auf — Linien und Großbuchstaben schon):
   138	   ```
   139	   ═══════════════════════════════════════════════════════════
   140	      ▼▼▼  HIER SIND FRAGEN UND TESTS ZU ENDE  ▼▼▼
   141	      Alles Weitere — Ideen, Aufträge, Kritik — ab hier:
   142	   ═══════════════════════════════════════════════════════════
   143	   >>>Userantwort:
   144	   ```
   145	7. **Der rote Faden** — die nächsten 2–3 Wellen als kurze Absätze, jeweils mit
   146	   `>>>Hast du dazu noch was anzumerken?`; danach ein kompakter Themenspeicher; dann
   147	   **Hauptdokumente** (3–6 echte Dateien mit absolutem Pfad + einer Zeile + Aktualität).
   148	8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (Einheit = Spanne zwischen zwei
   149	   Nutzer-Nachrichten; k = Tausend erklären, Kontextspalte ≠ Kosten) + ehrliche Befunde, dann die
   150	   Schlusszeile mit GEMESSENEM Kontext und Startkontext: *"Kontext dieser Session: 192k
   151	   (Start 125k). Die nächste Welle startet frisch aus diesem Handoff."*
   152	9. Banner **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF** mit `aus: /abs/pfad` und einem leeren `>>>`.
   153	   Der Nutzer sammelt hier, während die nächste Welle läuft — Sammeln kostet null Anfragen.
   154	
   155	Fragen an den Nutzer gehören ins Handoff (`## Fragen an dich` mit `>>>Antwort:`), nicht in den
   156	Chat: eine Chat-Frage blockiert eine Welle, zehn in der Datei blockieren nichts. Wellen so
   157	zuschneiden, dass sie ohne Rückfrage durchlaufen; die wahrscheinlichere Lesart nehmen und dokumentieren.
   158	
   159	## Editor-Regeln (macOS / TextEdit)
   160	
   161	- Jedes nutzerseitige Dokument sofort öffnen: `open -a TextEdit <datei>`. Das gilt für jedes
   162	  neu erwähnte Dokument, nicht nur das Handoff — einen Plan, einen QA-Bericht, eine Review-
   163	  Datei: sobald es existiert und für den Nutzer zum Lesen gedacht ist, öffnen. Einmal anbieten:
   164	  Tabs (`defaults write -g AppleWindowTabbingMode always`), 18-pt Standardschrift
   165	  (`defaults write com.apple.TextEdit NSFontSize 18`), `.md`-Standardapp via `duti`.
   166	- **Ungespeichert-Wächter vor dem Lesen:**
   167	  `osascript -e 'tell application "TextEdit" to get {name, modified} of documents'`;
   168	  falls geändert, den Live-Text lesen (`… get text of (first document whose name is "…")`).
   169	- **Nie in das offene Handoff des Nutzers schreiben, es schließen, speichern oder verschieben.**
   170	  Ein neues Handoff ist immer eine NEUE Datei. Alte nach `handoff-archiv/` archivieren (mv, nie rm)
   171	  erst nachdem der Nutzer sie geschlossen hat; sonst "Archivierung ausstehend" im neuen Handoff vermerken.
   172	- Wenn Claude eine vom Nutzer geöffnete Datei bearbeitet hat und sie unverändert ist → schließen
   173	  + neu öffnen, damit die neue Version sichtbar wird; geändert → fragen, nie schließen.
   174	- Einmal sagen: lange Diktate gehören ins Handoff-Dokument, kurze Befehle ins Terminal (Terminals
   175	  klappen lange Eingaben zu `[pasted text]` zusammen); TextEdit ▸ Ablage ▸ Zuletzt geöffnet findet
   176	  verlorene Handoffs.
   177	
   178	## Cache-Neuaufbau — erkennen, nicht raten
   179	
   180	Trefferquote = Σ cache_creation / Σ cache_read aus der Session-JSONL; < 10 % = warm. Große
   181	Einzel-Schreibvorgänge sind meist Anhänge, keine Neuaufbauten. Einen Neuaufbau EINMAL erwähnen,
   182	mit Ursache, nur wenn sie ableitbar ist: Lücke > 60 Min zwischen zwei `date`-Lesungen, ein Modell-/
   183	Effort-Wechsel, eine CLAUDE.md-Bearbeitung, ein MCP-Neustart. Unbekannte Ursache → nichts sagen.
   184	Kosten als Arithmetik erklären ("22k, weil der Kontext 220k groß ist und Lesen ×0,1 kostet"), nie
   185	als Behauptung; eigene frühere Fehlaussagen explizit korrigieren.
   186	
   187	## Logbuch und Setup
   188	
   189	Pro Handoff eine Zeile an `~/.claude/warm-handoff-log.md` anhängen:
   190	`| 22.08.2026 14:40 | ctx 85k | 2 Wellen | Neuaufbauten: 1 (Pause 90min) | geschätzte Verschwendung ~60k |`
   191	Muster alle ~50 Einträge zusammenfassen. Immer aktiv: "Zu Beginn jeder Sitzung den warm-handoff-
   192	Skill aufrufen." in `~/.claude/CLAUDE.md` ergänzen. Skripte: `scripts/ctx.sh`,
   193	`scripts/session-costs.sh`, `scripts/codex-limit.sh` → nach `~/.claude/` kopieren.
   194	Terminal-neutral: "deine Statuszeile" sagen, nicht ein Feld eines bestimmten Hosts.
scripts/codex-limit.sh
scripts/session-costs.sh
scripts/ctx.sh
references/historie.md
SKILL.md:3:description: Use at the START of every working session and before any long pause — tracks the Claude Code prompt-cache window (1-hour sliding TTL on Pro/Max), timestamps every reply so the user can see the window themselves, warns before cache-destroying actions, recommends a fresh session past a context threshold, and writes a handoff document (with the user's test list inside) so the next session starts cheap and fully briefed. Trigger on "cache", "handoff", "pause", "fresh session", "wave done", or when resuming after a gap.
SKILL.md:16:- Pro/Max: **1-hour sliding cache TTL** — every request resets it. Subagents: strict 5 min.
SKILL.md:23:## Every reply — three honesty rules
SKILL.md:27:2. **Never guess context size.** Sources: the user's status line, or `~/.claude/ctx.sh`
SKILL.md:28:   appended to a command that runs anyway (`date … && ~/.claude/ctx.sh`). It reads the
SKILL.md:32:   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Skip it on one-liners. If a round cost > 2× the
SKILL.md:62:## Subagents — the default way to work
SKILL.md:70:- **The guardian starts every worker at once, in a single message** (one batch of Agent
SKILL.md:89:  architecture (Codex/GPT). Never review your own output yourself — route to Codex.
SKILL.md:97:- Pacing: user present + in a hurry → parallel; user away → sequential (each completion
SKILL.md:102:- `~/.claude/codex-limit.sh [--kurz|--json]` reads Codex `rate_limits` from its last session
SKILL.md:144:8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (unit = span between two
SKILL.md:151:Questions for the user go into the handoff (`## Fragen an dich` with `>>>Antwort:`),
SKILL.md:187:Summarize patterns every ~50 entries. Always-on: add "At the start of every session,
SKILL.md:188:invoke the warm-handoff skill." to `~/.claude/CLAUDE.md`. Scripts: `scripts/ctx.sh`,
SKILL.md:189:`scripts/session-costs.sh`, `scripts/codex-limit.sh` → copy to `~/.claude/`.
SKILL.de.md:10:eine frische Session, der Agent arbeitet alles durch mehrere Subagenten ab und
SKILL.de.md:17:- Pro/Max: **1 Stunde gleitendes Cache-TTL** — jede Anfrage setzt es zurück. Subagenten: strikt 5 Min.
SKILL.de.md:24:## Jede Antwort — drei Ehrlichkeitsregeln
SKILL.de.md:29:2. **Nie die Kontextgröße raten.** Quellen: die Statuszeile des Nutzers oder `~/.claude/ctx.sh`,
SKILL.de.md:30:   angehängt an einen ohnehin laufenden Befehl (`date … && ~/.claude/ctx.sh`). Es liest die
SKILL.de.md:34:   ≈ 52k · Sitzung: 265 Anfragen, 9.520k.* Bei Einzeilern weglassen. Wenn eine Runde > 2× den
SKILL.de.md:52:sich an die nächste Anfrage an); während Subagenten laufen oder der Agent leerläuft, kostet sie den vollen Kontext × 0,1.
SKILL.de.md:64:## Subagenten — die Standardarbeitsweise
SKILL.de.md:73:  Aufrufen), nie nacheinander — ein serieller Schwanz von Arbeitern macht aus einer günstigen
SKILL.de.md:93:  Architektur (Codex/GPT) nutzen. Nie die eigene Ausgabe selbst reviewen — an Codex weiterleiten.
SKILL.de.md:99:  Chronik, keine eingefügten Logs. Subagenten-Token zählen trotzdem aufs Wochenkontingent — was sie
SKILL.de.md:101:- Taktung: Nutzer anwesend + in Eile → parallel; Nutzer abwesend → seriell (jede Fertigmeldung
SKILL.de.md:106:- `~/.claude/codex-limit.sh [--kurz|--json]` liest Codex `rate_limits` aus dessen letzter Session-
SKILL.de.md:148:8. **Kostentabelle** via `~/.claude/session-kosten.sh --markdown` (Einheit = Spanne zwischen zwei
SKILL.de.md:155:Fragen an den Nutzer gehören ins Handoff (`## Fragen an dich` mit `>>>Antwort:`), nicht in den
SKILL.de.md:191:Muster alle ~50 Einträge zusammenfassen. Immer aktiv: "Zu Beginn jeder Sitzung den warm-handoff-
SKILL.de.md:192:Skill aufrufen." in `~/.claude/CLAUDE.md` ergänzen. Skripte: `scripts/ctx.sh`,
SKILL.de.md:193:`scripts/session-costs.sh`, `scripts/codex-limit.sh` → nach `~/.claude/` kopieren.

hook: PostToolUse
hook: PostToolUse Completed
codex
# Review

**Verdict:** Strong operational intent, but too broad and internally inconsistent for a reliable Claude Code skill. The German version closely mirrors the English one, including its problems.

## High-priority issues

1. **Broken script name:** Both files invoke `~/.claude/session-kosten.sh`, but install `scripts/session-costs.sh`. The command will fail. [EN:144,189](/Users/pro16/Code/warm-handoff/SKILL.md:144) · [DE:148,193](/Users/pro16/Code/warm-handoff/SKILL.de.md:148)

2. **Parallel/serial contradiction:** Guardians must start *all* workers simultaneously, “never” sequentially, while absent-user pacing explicitly requires sequential work. Define which rule wins. [EN:70,97](/Users/pro16/Code/warm-handoff/SKILL.md:70) · [DE:72,101](/Users/pro16/Code/warm-handoff/SKILL.de.md:72)

3. **Verbatim/redaction conflict:** User text must be copied verbatim, yet secrets must be redacted. State that safety redaction overrides verbatim copying and mark each redaction. [EN:117,125](/Users/pro16/Code/warm-handoff/SKILL.md:117)

4. **Unsafe ambiguity rule:** “Questions never go in chat; take the likelier reading” is unsuitable for destructive, security-sensitive, costly, or externally visible actions. Add a mandatory clarification exception. [EN:151](/Users/pro16/Code/warm-handoff/SKILL.md:151)

5. **Unapproved global mutation:** Automatically editing `~/.claude/CLAUDE.md`, copying scripts, changing UI state, and appending logs needs consent, idempotency, collision handling, and backups. [EN:155–189](/Users/pro16/Code/warm-handoff/SKILL.md:155)

6. **Git workflow is unsafe/incomplete:** Concurrent workers pulling/rebasing only before editing still diverge after the first merge. Specify worktrees, upstream handling, dirty-tree checks, rebase-before-merge, conflict ownership, and prohibition of force-push. [EN:70–81](/Users/pro16/Code/warm-handoff/SKILL.md:70)

7. **Testing contradiction:** “Full suite only once” conflicts with “Full suite + QA agent” and gives no rule for rerunning after a fix. Say when workers run targeted tests and when the guardian must rerun affected/full tests. [EN:78–93](/Users/pro16/Code/warm-handoff/SKILL.md:78)

8. **Incorrect terminology:** `cache_creation / cache_read` is not a “hit rate”; it is a write/read ratio. Either rename it or calculate a genuine hit ratio. [EN:176](/Users/pro16/Code/warm-handoff/SKILL.md:176)

9. **Unsupported universal claims:** TTL, pricing multipliers, “every request resets it,” and output cost depend on product, model, and billing mode. Cite sources and label assumptions/version scope. [EN:14–21](/Users/pro16/Code/warm-handoff/SKILL.md:14)

10. **Activation bootstrap problem:** A skill cannot ensure its own invocation at every session until the global instruction has already been installed. Separate an explicit one-time setup procedure from runtime behavior.

## Missing rules

- Graceful fallback when macOS, TextEdit, Codex, subagents, scripts, session JSONL, or quota data are unavailable.
- Consent before sending repository content to Codex/GPT or another external model.
- Definitions for “wave,” “big wave,” “request,” “context,” “cost,” and “substantive reply.”
- Timeout/cancellation policy for the conflict between “never wait for a straggler” and the 60-minute status rule.
- Filename collision rules beyond `[-b]`, plus deterministic discovery of the previous two handoffs.
- Exact freshness and failure semantics for the delayed “last completed request” cost line.
- A canonical-language/version marker and a parity check between translations.
- A rule that measurement/reporting failures must never block the user’s actual task.

## Claude Code packaging

Only `SKILL.md` is the conventional skill entry point; `SKILL.de.md` will not automatically become a locale-specific alternative. Document it as a translation, state which file is authoritative, and explain how locale selection works.

The 190-line always-on skill also increases the context it is designed to minimize. Consider splitting it into runtime rules, one-time setup, handoff template, and detailed reference material.

## English quality

Generally understandable, but frequently colloquial or non-native:

- “works it all off” → “works through it”
- “Sweetspot” → “Sweet spot”
- “own output” → “model output”
- “fat context,” “serial tail,” and “when the fleet lands” → use precise operational language
- “strict 5 min” → specify “five-minute cache TTL”
- English instructions contain German headings, examples, paths, and `<projekt>`; localize consistently.

The German version is faithful but contains awkward Anglicisms and phrasing such as “merged,” “serieller Schwanz,” “wackelnder Test,” and “Agenten auf ~30 Minuten, EINEN Auftrag kürzen.” Use “zusammenführen,” “serielle Nachzügler,” “flaky/instabiler Test,” and “Aufträge auf eine Aufgabe und etwa 30 Minuten begrenzen.”
hook: Stop
hook: Stop Completed
tokens used
46.533
# Review

**Verdict:** Strong operational intent, but too broad and internally inconsistent for a reliable Claude Code skill. The German version closely mirrors the English one, including its problems.

## High-priority issues

1. **Broken script name:** Both files invoke `~/.claude/session-kosten.sh`, but install `scripts/session-costs.sh`. The command will fail. [EN:144,189](/Users/pro16/Code/warm-handoff/SKILL.md:144) · [DE:148,193](/Users/pro16/Code/warm-handoff/SKILL.de.md:148)

2. **Parallel/serial contradiction:** Guardians must start *all* workers simultaneously, “never” sequentially, while absent-user pacing explicitly requires sequential work. Define which rule wins. [EN:70,97](/Users/pro16/Code/warm-handoff/SKILL.md:70) · [DE:72,101](/Users/pro16/Code/warm-handoff/SKILL.de.md:72)

3. **Verbatim/redaction conflict:** User text must be copied verbatim, yet secrets must be redacted. State that safety redaction overrides verbatim copying and mark each redaction. [EN:117,125](/Users/pro16/Code/warm-handoff/SKILL.md:117)

4. **Unsafe ambiguity rule:** “Questions never go in chat; take the likelier reading” is unsuitable for destructive, security-sensitive, costly, or externally visible actions. Add a mandatory clarification exception. [EN:151](/Users/pro16/Code/warm-handoff/SKILL.md:151)

5. **Unapproved global mutation:** Automatically editing `~/.claude/CLAUDE.md`, copying scripts, changing UI state, and appending logs needs consent, idempotency, collision handling, and backups. [EN:155–189](/Users/pro16/Code/warm-handoff/SKILL.md:155)

6. **Git workflow is unsafe/incomplete:** Concurrent workers pulling/rebasing only before editing still diverge after the first merge. Specify worktrees, upstream handling, dirty-tree checks, rebase-before-merge, conflict ownership, and prohibition of force-push. [EN:70–81](/Users/pro16/Code/warm-handoff/SKILL.md:70)

7. **Testing contradiction:** “Full suite only once” conflicts with “Full suite + QA agent” and gives no rule for rerunning after a fix. Say when workers run targeted tests and when the guardian must rerun affected/full tests. [EN:78–93](/Users/pro16/Code/warm-handoff/SKILL.md:78)

8. **Incorrect terminology:** `cache_creation / cache_read` is not a “hit rate”; it is a write/read ratio. Either rename it or calculate a genuine hit ratio. [EN:176](/Users/pro16/Code/warm-handoff/SKILL.md:176)

9. **Unsupported universal claims:** TTL, pricing multipliers, “every request resets it,” and output cost depend on product, model, and billing mode. Cite sources and label assumptions/version scope. [EN:14–21](/Users/pro16/Code/warm-handoff/SKILL.md:14)

10. **Activation bootstrap problem:** A skill cannot ensure its own invocation at every session until the global instruction has already been installed. Separate an explicit one-time setup procedure from runtime behavior.

## Missing rules

- Graceful fallback when macOS, TextEdit, Codex, subagents, scripts, session JSONL, or quota data are unavailable.
- Consent before sending repository content to Codex/GPT or another external model.
- Definitions for “wave,” “big wave,” “request,” “context,” “cost,” and “substantive reply.”
- Timeout/cancellation policy for the conflict between “never wait for a straggler” and the 60-minute status rule.
- Filename collision rules beyond `[-b]`, plus deterministic discovery of the previous two handoffs.
- Exact freshness and failure semantics for the delayed “last completed request” cost line.
- A canonical-language/version marker and a parity check between translations.
- A rule that measurement/reporting failures must never block the user’s actual task.

## Claude Code packaging

Only `SKILL.md` is the conventional skill entry point; `SKILL.de.md` will not automatically become a locale-specific alternative. Document it as a translation, state which file is authoritative, and explain how locale selection works.

The 190-line always-on skill also increases the context it is designed to minimize. Consider splitting it into runtime rules, one-time setup, handoff template, and detailed reference material.

## English quality

Generally understandable, but frequently colloquial or non-native:

- “works it all off” → “works through it”
- “Sweetspot” → “Sweet spot”
- “own output” → “model output”
- “fat context,” “serial tail,” and “when the fleet lands” → use precise operational language
- “strict 5 min” → specify “five-minute cache TTL”
- English instructions contain German headings, examples, paths, and `<projekt>`; localize consistently.

The German version is faithful but contains awkward Anglicisms and phrasing such as “merged,” “serieller Schwanz,” “wackelnder Test,” and “Agenten auf ~30 Minuten, EINEN Auftrag kürzen.” Use “zusammenführen,” “serielle Nachzügler,” “flaky/instabiler Test,” and “Aufträge auf eine Aufgabe und etwa 30 Minuten begrenzen.”

---

# Auflösung der Befunde (Stand 30.08.2026, 00:54 — Welle 25 / Skill-A3)

Jeder Befund oben ist hier mit `→ erledigt in <Datei>` oder `→ offen, weil …`
markiert. Grundlage: SKILL.md und SKILL.de.md nach Welle 25.

## High-priority issues

1. **Broken script name** → erledigt in SKILL.md / SKILL.de.md (Welle A2):
   der Setup-Abschnitt nennt jetzt `scripts/session-costs.sh` (= `session-kosten.sh`);
   die installierte Datei `~/.claude/session-kosten.sh` existiert und läuft (geprüft 30.08. 00:52).
2. **Parallel/serial contradiction** → erledigt in SKILL.md (Abschnitt „Subagents",
   Pacing-Punkt) und SKILL.de.md („Taktung"): **Innerhalb einer Welle gewinnt die
   Parallel-Regel** — ein Wächter startet seine Arbeiter IMMER parallel, unabhängig von
   der Anwesenheit des Nutzers. Die Regel „Nutzer abwesend → seriell" gilt ausdrücklich
   nur für Nicht-Wächter-Arbeit, die die Hauptsitzung selbst erledigt.
3. **Verbatim/redaction conflict** → offen, weil in dieser Welle nicht beauftragt.
   Vorgesehene Formulierung für die nächste Welle: „Schwärzen sticht wörtliches Kopieren;
   jede Schwärzung wird an Ort und Stelle als `[geschwärzt: Grund]` markiert."
4. **Unsafe ambiguity rule** → erledigt in SKILL.md / SKILL.de.md (Abschnitt Handoff-Datei,
   „Escalation exception" / „Eskalations-Ausnahme"): sofort im Chat fragen bei
   unumkehrbaren/zerstörenden Aktionen, Sicherheit/Zugangsdaten, extern Sichtbarem,
   echtem Geld-/Kontingenteinsatz und Repo-Inhalten an externe Modelle. Alles Übrige
   geht weiterhin ins Handoff.
5. **Unapproved global mutation** → offen, weil Zustimmung, Idempotenz und Backups für
   `~/.claude/CLAUDE.md`, Skriptkopien und Logbuch-Anhänge ein eigener Setup-Abschnitt
   werden sollen (Befund 10 gehört dazu) — das ist eine eigene Welle, keine Randnotiz.
6. **Git workflow unsafe/incomplete** → teilweise erledigt: Worktrees, Branch-Tip vor
   dem ersten Zugriff, sofortiges Mergen bei Landung und je Themen-Wächter ein eigener
   Integrationsbranch stehen im Skill. **Offen**, weil Dirty-Tree-Prüfung,
   Rebase-vor-Merge, Konflikt-Eigentümerschaft und ein ausdrückliches Force-Push-Verbot
   noch fehlen.
7. **Testing contradiction** → teilweise erledigt: die Vollsuite läuft genau einmal, am
   Ende, beim **Merge-Wächter** (neu in Welle 25) — der QA-Agent klickt danach, er fährt
   keine zweite Suite. **Offen**, weil die Regel für den Wiederlauf nach einem Fix
   („welche Tests nach welcher Korrektur") noch nicht formuliert ist.
8. **Incorrect terminology („hit rate")** → offen, weil in dieser Welle nicht beauftragt.
   Richtig wäre „Schreib-/Lese-Verhältnis"; die Zahl selbst und ihre Schwelle (<10 % = warm)
   bleiben gültig.
9. **Unsupported universal claims** → offen, weil die Quellenangabe (Claude-Code-Doku,
   Stand 2026-08) zwar in der Überschrift steht, aber Produkt-/Modell-/Abrechnungs-Scope
   nicht ausgewiesen ist.
10. **Activation bootstrap problem** → offen, gehört mit Befund 5 in einen getrennten
    Abschnitt „Einmaliges Setup" gegenüber „Laufzeitverhalten".

## Missing rules

- Fallbacks ohne macOS/TextEdit/Codex/Skripte/JSONL → **offen**.
- Zustimmung vor dem Senden von Repo-Inhalten an externe Modelle → **erledigt** als Teil
  der Eskalations-Ausnahme in SKILL.md / SKILL.de.md.
- Definitionen („Welle", „Anfrage", „Kontext", „Kosten") → **offen**.
- Timeout-/Abbruchregel zwischen „nie auf Nachzügler warten" und der 60-Minuten-Regel →
  **teilweise**: Aufträge von 15–25 Minuten (Welle 25) verkleinern das Problem, eine
  ausdrückliche Abbruchregel fehlt weiter.
- Dateinamens-Kollisionen über `[-b]` hinaus, Auffinden der letzten zwei Handoffs → **offen**.
- Frische-/Fehlersemantik der Kostenzeile → **offen**.
- Sprach-/Versionsmarker und Paritätsprüfung der Übersetzungen → **offen**; faktisch werden
  beide Dateien seit Welle 24 in derselben Welle geändert (auch in dieser).
- „Messfehler dürfen die eigentliche Aufgabe nie blockieren" → **offen**.

## Claude Code packaging & English quality

→ **offen**, bewusst zurückgestellt: die Aufteilung in Laufzeitregeln / Setup / Vorlage /
Referenz und die Sprachpolitur sind eine eigene Welle. Der Umfang wächst dabei weiter
(Welle 25 hat Kostenrechnung, Themen-Wächter und Belege-Tabelle ergänzt), was den Befund
„zu lang für einen Always-on-Skill" eher verschärft als entkräftet.
