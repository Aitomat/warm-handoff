#!/usr/bin/env bash
# skills-uebersicht.sh — erzeugt ~/.claude/SKILLS-UEBERSICHT.md neu:
# alle Skills (global ~/.claude/skills, ~/.agents/skills, Plugins) mit einer
# Zeile Zweck, gruppiert; Plugins mit ihren Agenten; globale Agenten; MCP-Server;
# plus Anleitung "so schaltest du je Projekt ab".
# Aufruf: bash ~/.claude/skills/warm-handoff/scripts/skills-uebersicht.sh [ziel.md]
set -euo pipefail
OUT="${1:-$HOME/.claude/SKILLS-UEBERSICHT.md}"
python3 - "$OUT" <<'PY'
import os, re, sys, json, glob, datetime
H = os.path.expanduser('~'); out = sys.argv[1]

def desc(p, n=140):
    try: t = open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
    m = re.match(r'---\n(.*?)\n---', t, re.S)
    fm = m.group(1) if m else ''
    d = re.search(r'^description:\s*(.*?)(?=^\w[\w-]*:|\Z)', fm, re.S | re.M)
    s = d.group(1) if d else t.strip().split('\n')[0]
    s = re.sub(r'^[>|]-?\s*', '', s.strip()); s = ' '.join(s.split()).strip('"\' ')
    return (s[:n] + '…') if len(s) > n else s

def group(name):
    for pat, g in [(r'^ads(-|$)', 'ads-* (Werbung)'), (r'^seo(-|$)', 'seo-* (SEO)'),
                   (r'^firecrawl(-|$)', 'firecrawl-* (Web-Scraping)'), (r'-hamer$', '*-hamer (GNM-Wissensbasen)'),
                   (r'^(cloudflare|durable-objects|sandbox-sdk|wrangler|workers-|web-perf|agents-sdk)', 'Cloudflare / Workers'),
                   (r'^cmux', 'cmux (Terminal)'), (r'^aquacentrum|^shop-klon', 'Aquacentrum / WooCommerce'),
                   (r'^(warm-handoff|cache-fenster|handoff|aitomat-qa|three-brain|graphify)$', 'Arbeitsweise / Aitomat')]:
        if re.search(pat, name): return g
    return 'Sonstige'

lines = [f'# Skills-Übersicht — erzeugt {datetime.datetime.now():%d.%m.%Y, %H:%M}', '',
         'Erzeugt von `~/.claude/skills/warm-handoff/scripts/skills-uebersicht.sh`. Nicht von Hand pflegen — Skript neu laufen lassen.',
         'Jeder hier gelistete Skill kostet in JEDEM Projekt Startkontext (Name + Beschreibung), ob gebraucht oder nicht.', '']

# 1) globale Skills (~/.claude/skills, inkl. Symlinks nach ~/.agents/skills)
groups = {}
for d in sorted(glob.glob(f'{H}/.claude/skills/*/')):
    n = os.path.basename(d.rstrip('/')); p = d + 'SKILL.md'
    if not os.path.exists(p): continue
    src = ' (→ ~/.agents/skills)' if os.path.islink(d.rstrip('/')) else ''
    groups.setdefault(group(n), []).append(f'- `{n}`{src} — {desc(p)}')
extra = [os.path.basename(d.rstrip('/')) for d in glob.glob(f'{H}/.agents/skills/*/')
         if not os.path.exists(f'{H}/.claude/skills/' + os.path.basename(d.rstrip('/')))]
total = sum(len(v) for v in groups.values())
lines += [f'## 1. Globale Skills — {total} (`~/.claude/skills`, per `skillOverrides` je Projekt abschaltbar)', '']
for g in sorted(groups, key=lambda x: (x == 'Sonstige', x)):
    lines += [f'### {g} ({len(groups[g])})', ''] + groups[g] + ['']
if extra:
    lines += ['### Nur in ~/.agents/skills (nicht verlinkt)', ''] + [f'- `{n}`' for n in extra] + ['']

# 2) Plugins mit Skills + Agenten
lines += ['## 2. Plugins (`enabledPlugins` je Projekt abschaltbar — ganz oder gar nicht)', '']
settings = json.load(open(f'{H}/.claude/settings.json'))
enabled = settings.get('enabledPlugins', {})
for d in sorted(glob.glob(f'{H}/.claude/plugins/cache/*/*/*/')):
    mk, pl, ver = d.rstrip('/').split('/')[-3:]
    pid = f'{pl}@{mk}'
    st = 'AN' if enabled.get(pid) else 'aus'
    sk = [os.path.basename(s.rstrip('/')) for s in sorted(glob.glob(d + 'skills/*/'))]
    ag = [os.path.basename(a)[:-3] for a in sorted(glob.glob(d + 'agents/*.md'))]
    lines.append(f'- **{pid}** {ver} — global {st}; Skills: {", ".join(sk) or "–"}; Agenten: {", ".join(ag) or "–"}')
lines.append('')

# 3) globale Agenten
ags = sorted(glob.glob(f'{H}/.claude/agents/*.md'))
lines += [f'## 3. Globale Agenten — {len(ags)} (`~/.claude/agents`, KEIN Projekt-Schalter; nur verschieben)', '']
lines += [f'- `{os.path.basename(a)[:-3]}` — {desc(a, 100)}' for a in ags] + ['']

# 4) MCP-Server
lines += ['## 4. MCP-Server', '']
try:
    cj = json.load(open(f'{H}/.claude.json'))
    for n, c in (cj.get('mcpServers') or {}).items():
        lines.append(f'- global `{n}` — {c.get("command","")} {" ".join(c.get("args",[]))}'.rstrip())
    for proj, pc in (cj.get('projects') or {}).items():
        for n in (pc.get('mcpServers') or {}): lines.append(f'- Projekt {proj}: `{n}`')
except Exception as e: lines.append(f'- (~/.claude.json nicht lesbar: {e})')
for mj in glob.glob(f'{H}/Code/*/.mcp.json'):
    try: lines.append(f'- `{mj}`: ' + ', '.join(json.load(open(mj)).get('mcpServers', {})))
    except Exception: pass
lines.append('- Claude.ai-Connectoren (Gmail, Drive, Notion …) sind *deferred*: nur der Name kostet Kontext, nicht das Schema.')
lines.append('')

# 5) Abschalten
lines += ['## 5. So schaltest du je Projekt ab', '',
 'Datei `<projekt>/.claude/settings.json` (Projekt schlägt `~/.claude/settings.json`; `settings.local.json` schlägt beides).',
 'Skill-Namen müssen einzeln stehen — es gibt KEINE Wildcards. Werte: `on` · `name-only` · `user-invocable-only` · `off`.', '',
 '```json', '{', '  "enabledPlugins": {', '    "example-skills@anthropic-agent-skills": false,',
 '    "plugin-dev@claude-plugins-official": false', '  },', '  "skillOverrides": {',
 '    "ads": "off",', '    "seo": "off",', '    "firecrawl": "off"', '  }', '}', '```', '',
 'Vorlage mit allen 97 Aitomat-fremden Skills: `/Users/pro16/Code/aitomat/.claude/settings.json`.',
 'Globale Agenten (`~/.claude/agents/*.md`) haben keinen Projekt-Schalter — nur nach `~/.claude/agents-inaktiv/` verschieben.',
 'Prüfen: neue Session starten, erste Anfrage im Session-JSONL → `cache_creation_input_tokens` = Startkontext.', '']
open(out, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'{out}: {len(lines)} Zeilen, {total} globale Skills, {len(ags)} Agenten')
PY
