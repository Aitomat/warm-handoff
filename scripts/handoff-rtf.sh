#!/bin/bash
# handoff-rtf.sh — RTF-Zwilling für Handoff-Markdown (macOS)
#
#   handoff-rtf.sh <datei.md> [ziel.rtf]
#
# Erzeugt neben der Markdown-Datei eine gleichnamige .rtf:
#   * 18 pt Grundschrift, Überschriften fett und größer
#   * klickbare Links für absolute Pfade (/…), ~/-Pfade und URLs
#   * >>>-Zeilen (Zwischenrufe) gelb hinterlegt
#
# Weg: Markdown -> HTML (pandoc, falls vorhanden; sonst eigener Konverter)
#      -> textutil -convert rtf
#
# Markdown bleibt die Quelle. Die RTF ist nur die Lesefassung.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Aufruf: $(basename "$0") <datei.md> [ziel.rtf]" >&2
  exit 2
fi

SRC="$1"
if [ ! -f "$SRC" ]; then
  echo "Datei nicht gefunden: $SRC" >&2
  exit 1
fi

if [ $# -ge 2 ]; then
  OUT="$2"
else
  OUT="${SRC%.md}.rtf"
  [ "$OUT" = "$SRC" ] && OUT="$SRC.rtf"
fi

TMPDIR_RTF="$(mktemp -d "${TMPDIR:-/tmp}/handoff-rtf.XXXXXX")"
trap 'rm -rf "$TMPDIR_RTF"' EXIT
HTML="$TMPDIR_RTF/body.html"

CSS='<style>
/* textutil rechnet CSS-Größen mit Faktor 4/3 in RTF-Punkte um.
   Darum hier jeweils 3/4 der Zielgröße: 13.5 -> 18 pt usw. */
body { font-family: -apple-system, "Helvetica Neue", Helvetica, sans-serif; font-size: 13.5pt; }
h1 { font-size: 22.5pt; font-weight: bold; }
h2 { font-size: 18.75pt; font-weight: bold; }
h3 { font-size: 15.75pt; font-weight: bold; }
h4, h5, h6 { font-size: 14.25pt; font-weight: bold; }
code, pre { font-family: Menlo, monospace; font-size: 11.25pt; }
.zwischenruf { background-color: #FFF200; }
/* Kopf-Kopierzeile („Ich habe das Handoff beantwortet: …") muss in EINE Zeile
   passen: kleinere Schrift, kein Umbruch. 6.75 -> 9 pt. */
.kopfzeile, .kopfzeile code, .kopfzeile a { font-size: 6.75pt; white-space: nowrap; }
</style>'

MD2HTML_PY='
import html, os, re, sys

src = sys.argv[1]
with open(src, "r", encoding="utf-8", errors="replace") as fh:
    lines = fh.read().split("\n")

URL_RE  = re.compile(r"(?<![\w@/])(https?://[^\s<>()\[\]\"\x27]+)")
PATH_RE = re.compile(r"(?<![\w~./-])((?:~|/Users|/Applications|/Library|/opt|/usr|/etc|/var|/private|/tmp)/[^\s<>()\[\]\"\x27,;]+)")
MDLINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
# Marker wie ⟦Screenshot: ~/Dropbox/Screenshots/ScreenshotY 2026-09-03 um 18.25.55.jpg⟧
# Alles bis zum schliessenden ⟧ ist EIN Pfad, Leerzeichen inbegriffen.
MARKER_RE = re.compile(u"⟦\\s*(Screenshot|Bild|Datei|Kopie|Video|Audio)\\s*:\\s*(.*?)\\s*⟧", re.S)
QUOTES = u"„“”«»" + chr(34) + chr(39)

def file_href(p):
    q = os.path.expanduser(p.rstrip(".,;:"))
    return "file://" + "".join(
        (c if (c.isalnum() or c in "/-_.~!$&*+=@:") else "".join("%%%02X" % b for b in c.encode("utf-8")))
        for c in q
    )

def marker_sub(m):
    """⟦Screenshot: pfad mit leerzeichen⟧ -> klickbarer Link (HTML-escaped in/out)."""
    kind = m.group(1)
    raw = html.unescape(m.group(2)).strip().strip(QUOTES).strip()
    if not raw:
        return m.group(0)
    label = html.escape(raw)
    return u"⟦%s: <a href=\"%s\">%s</a>⟧" % (
        kind, html.escape(file_href(raw), quote=True), label)

def linkify(text):
    """text is already HTML-escaped; wrap URLs/paths in <a>."""
    # Marker zuerst: ihr Inhalt darf nicht mehr von PATH_RE zerlegt werden.
    if MARKER_RE.search(text):
        pieces = []
        pos = 0
        for m in MARKER_RE.finditer(text):
            pieces.append(linkify(text[pos:m.start()]))
            pieces.append(marker_sub(m))
            pos = m.end()
        pieces.append(linkify(text[pos:]))
        return "".join(pieces)

    def url_sub(m):
        u = m.group(1)
        tail = ""
        while u and u[-1] in ".,;:":
            tail = u[-1] + tail
            u = u[:-1]
        return "<a href=\"%s\">%s</a>%s" % (html.escape(u, quote=True), u, tail)
    text = URL_RE.sub(url_sub, text)

    def path_sub(m):
        p = m.group(1)
        tail = ""
        while p and p[-1] in ".,;:":
            tail = p[-1] + tail
            p = p[:-1]
        raw = html.unescape(p)
        return "<a href=\"%s\">%s</a>%s" % (html.escape(file_href(raw), quote=True), p, tail)
    return PATH_RE.sub(path_sub, text)

def inline(raw):
    """Markdown inline -> HTML."""
    parts = []
    for i, seg in enumerate(re.split(r"(`[^`]*`)", raw)):
        if i % 2 == 1:
            parts.append("<code>" + linkify(html.escape(seg[1:-1])) + "</code>")
            continue
        # markdown links first, on the raw text
        out = []
        pos = 0
        for m in MDLINK_RE.finditer(seg):
            out.append(linkify(html.escape(seg[pos:m.start()])))
            label = html.escape(m.group(1))
            target = m.group(2)
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                target = file_href(target) if target.startswith(("/", "~")) else target
            out.append("<a href=\"%s\">%s</a>" % (html.escape(target, quote=True), label))
            pos = m.end()
        out.append(linkify(html.escape(seg[pos:])))
        chunk = "".join(out)
        chunk = re.sub(r"\*\*([^*\n]+)\*\*", r"<b>\1</b>", chunk)
        chunk = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", chunk)
        parts.append(chunk)
    return "".join(parts)

out = []
in_code = False
list_stack = []
para = []
li_open = [False]

def flush_para():
    """Weiche Zeilenumbrüche des Markdowns zu einem Absatz zusammenfassen."""
    if not para:
        return
    text = inline(" ".join(para))
    del para[:]
    if li_open[0]:
        out.append("<li>%s</li>" % text)
        li_open[0] = False
    else:
        out.append("<p>%s</p>" % text)

def close_lists():
    flush_para()
    while list_stack:
        out.append("</%s>" % list_stack.pop())

for line in lines:
    fence = re.match(r"^\s*```", line)
    if fence:
        if in_code:
            out.append("</pre>")
            in_code = False
        else:
            close_lists()
            out.append("<pre>")
            in_code = True
        continue
    if in_code:
        out.append(linkify(html.escape(line)))
        continue

    stripped = line.strip()

    if stripped.startswith(">>>"):
        close_lists()
        out.append("<p class=\"zwischenruf\">%s</p>" % inline(stripped))
        continue

    if not stripped:
        close_lists()
        continue

    h = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if h:
        close_lists()
        lvl = len(h.group(1))
        out.append("<h%d>%s</h%d>" % (lvl, inline(h.group(2)), lvl))
        continue

    if re.match(r"^(\*\s*){3,}$|^(-\s*){3,}$|^(_\s*){3,}$", stripped):
        close_lists()
        out.append("<hr>")
        continue

    if stripped.startswith("|"):
        # Tabellenzeilen bleiben je eine Zeile (nicht zu einem Absatz verkleben)
        close_lists()
        if not re.match(r"^[|\s:-]+$", stripped):
            out.append("<p><code>%s</code></p>" % inline(stripped))
        continue

    ul = re.match(r"^\s*[-*+]\s+(.*)$", line)
    ol = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
    if ul or ol:
        want = "ul" if ul else "ol"
        flush_para()
        if not list_stack or list_stack[-1] != want:
            while list_stack:
                out.append("</%s>" % list_stack.pop())
            out.append("<%s>" % want)
            list_stack.append(want)
        para.append((ul or ol).group(1).strip())
        li_open[0] = True
        continue

    if stripped.startswith(">"):
        close_lists()
        body = stripped.lstrip("> ")
        if "Handoff beantwortet" in body:
            # Kopf-Kopierzeile: eine Zeile, kleine Schrift, Home-Pfad als ~ gekuerzt
            short = body.replace(os.path.expanduser("~"), "~")
            out.append("<p class=\"kopfzeile\">%s</p>" % inline(short))
            continue
        out.append("<blockquote>%s</blockquote>" % inline(body))
        continue

    # Fortsetzungszeile eines weich umbrochenen Absatzes bzw. Listenpunkts
    para.append(stripped)

close_lists()
if in_code:
    out.append("</pre>")

sys.stdout.write("\n".join(out))
'

if command -v pandoc >/dev/null 2>&1; then
  BODY="$(pandoc -f markdown -t html "$SRC")"
  # >>>-Zeilen und Pfad-/URL-Links nachrüsten (pandoc verlinkt nackte Pfade nicht)
  BODY="$(printf '%s' "$BODY" | python3 -c '
import html, os, re, sys
b = sys.stdin.read()
b = re.sub(r"<p>(&gt;&gt;&gt;.*?)</p>", r"<p class=\"zwischenruf\">\1</p>", b, flags=re.S)
# Kopf-Kopierzeile einzeilig: eigene Klasse, Home-Pfad gekuerzt
def kopf(m):
    inner = m.group(1).replace(html.escape(os.path.expanduser("~")), "~")
    return "<p class=\"kopfzeile\">%s</p>" % inner
b = re.sub(r"<blockquote>\s*<p>(.*?Handoff beantwortet.*?)</p>\s*</blockquote>", kopf, b, flags=re.S)
PATH_RE = re.compile(r"(?<![\w~./->])((?:~|/Users|/Applications|/Library|/opt|/usr|/etc|/var|/private|/tmp)/[^\s<>()\[\]\"\x27,;]+)")
MARKER_RE = re.compile(u"⟦\\s*(Screenshot|Bild|Datei|Kopie|Video|Audio)\\s*:\\s*(.*?)\\s*⟧", re.S)
QUOTES = u"„“”«»" + chr(34) + chr(39)
def href(p):
    q = os.path.expanduser(p)
    return "file://" + "".join((c if (c.isalnum() or c in "/-_.~!$&*+=@:") else "".join("%%%02X" % x for x in c.encode("utf-8"))) for c in q)
def repl(m):
    p = m.group(1)
    return "<a href=\"%s\">%s</a>" % (html.escape(href(html.unescape(p)), quote=True), p)
def marker(m):
    raw = html.unescape(m.group(2)).strip().strip(QUOTES).strip()
    if not raw:
        return m.group(0)
    return u"⟦%s: <a href=\"%s\">%s</a>⟧" % (m.group(1), html.escape(href(raw), quote=True), html.escape(raw))
parts = re.split(r"(<[^>]+>)", b)
for i in range(0, len(parts), 2):
    seg = parts[i]
    chunks = []
    pos = 0
    for m in MARKER_RE.finditer(seg):
        chunks.append(PATH_RE.sub(repl, seg[pos:m.start()]))
        chunks.append(marker(m))
        pos = m.end()
    chunks.append(PATH_RE.sub(repl, seg[pos:]))
    parts[i] = "".join(chunks)
sys.stdout.write("".join(parts))
')"
else
  BODY="$(python3 -c "$MD2HTML_PY" "$SRC")"
fi

{
  printf '%s' '<!DOCTYPE html><html><head><meta charset="utf-8">'
  printf '%s' "$CSS"
  printf '%s' '</head><body>'
  printf '%s' "$BODY"
  printf '%s' '</body></html>'
} > "$HTML"

textutil -convert rtf -format html -encoding UTF-8 -output "$OUT" "$HTML"

echo "$OUT"
