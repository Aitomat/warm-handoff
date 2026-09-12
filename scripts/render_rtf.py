#!/usr/bin/env python3
"""RTF mit absoluten Linkfeldern, Text-Roundtrip und exklusiver Veröffentlichung."""
import argparse
import re
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit
from handoff_common import publish_new


def rtf(text):
    result = []
    for char in text:
        if char in '\\{}':
            result.append('\\' + char)
        elif char == '\t':
            result.append('\\tab ')
        elif ord(char) < 128:
            result.append(char)
        else:
            for offset in range(0, len(char.encode('utf-16-le')), 2):
                unit = int.from_bytes(char.encode('utf-16-le')[offset:offset+2], 'little')
                result.append('\\u%d?' % (unit if unit < 32768 else unit - 65536))
    return ''.join(result)


def target(raw, base, future=None):
    raw = raw.strip('<>')
    parts = urlsplit(raw)
    if parts.scheme in ('http', 'https'):
        if not parts.netloc or any(c in raw for c in '\r\n"'):
            raise ValueError(f'Invalid web link: {raw}')
        return quote(raw, safe=':/?#[]@!$&\'()*+,;=%-._~')
    if parts.scheme and parts.scheme != 'file':
        raise ValueError(f'Unsupported link scheme: {parts.scheme}')
    if parts.scheme == 'file' and parts.netloc not in ('', 'localhost'):
        raise ValueError('Remote file URI unsupported')
    if parts.fragment or parts.query:
        raise ValueError('Lokale Anker/Query nicht unterstützt; Sonderzeichen im Dateinamen prozentkodieren')
    path = Path(unquote(parts.path)).expanduser()
    if not path.is_absolute():
        path = base / path
    if future is not None and path.resolve() == future:
        return future.as_uri()
    return path.resolve(strict=True).as_uri()


# Gold-Steuerwoerter der Antwortfelder und zugleich des Dokumentstandards.
# Cocoa/TextEdit liest \\highlight nicht; dort faerbt nur \\cb/\\cbpat, und fuer
# die Zeichenebene (das, was getippter Text erbt) nur \\chshdng0\\chcbpat.
# \\cf2 ist ausdruecklich Schwarz: ohne es erbt eingefuegter Text irgendeine
# geerbte Vordergrundfarbe -- Yasin, 13.09.2026: "es wird gelbe Schrift
# eingefuegt, und kleiner, nicht schwarze Schrift mit gelbem Hintergrund".
GOLD = '\\cb1\\cbpat1\\chshdng0\\chcbpat1\\highlight1\\cf2'
# \\cb0 waere in Cocoa schwarz; \\plain ist der einzige saubere Reset auf
# "kein Hintergrund" fuer Agententext, Ueberschriften und Codebloecke.
# \\cf2 haelt die Schrift auch dort ausdruecklich schwarz.
RESET = '\\plain\\f0\\cf2'


TOKEN = re.compile(
    r'(?P<marker>⟦\s*(?P<kind>Screenshot|Bild|Datei|Dokument|Kopie|Video|Audio)\s*:\s*(?P<marked>.*?)\s*⟧)'
    r'|\[(?P<label>[^\]\n]+)\]\((?P<dest><[^>\n]+>|[^)\s]+)\)'
    r'|`(?P<code>[^`\n]+)`|https?://[^\s<>]+'
    r'|(?<![\w/.-])(?:/|~/)[^\s<>`]+'
    r'|(?<![\w~/.-])(?:[\w.-]+/)*[\w.-]+\.(?:md|rtf|txt|sh|py|swift|json|csv|html|png|jpg|jpeg|pdf|plist|yml|yaml)(?![\w/])')


def inline(line, base, links, future=None):
    encoded, plain, cursor = [], [], 0
    for match in TOKEN.finditer(line):
        encoded.append(rtf(line[cursor:match.start()]))
        plain.append(line[cursor:match.start()])
        label, destination = match.group(0), None
        tail = ''
        if match.group('marker') is not None:
            raw = match.group('marked').strip().strip('„“”«»\"\'')
            if match.group('kind') == 'Kopie':
                # Kopie-Marker sind häufig wörtliche Zitate, keine Dateiangaben.
                # Ein fehlendes oder ungeeignetes Ziel lässt das Original unverändert.
                try:
                    destination = target(raw, base, future)
                except (OSError, ValueError):
                    destination = None
            else:
                # Dokumentmarker können Anzeigename und tatsächlichen Pfad trennen.
                # Zuerst den vollständigen Pfad prüfen: Dateinamen dürfen „ — “ enthalten.
                try:
                    destination = target(raw, base, future)
                except (OSError, ValueError):
                    if match.group('kind') != 'Dokument' or ' — ' not in raw:
                        raise
                    destination = target(raw.rsplit(' — ', 1)[1].strip().strip('„“”«»\"\''), base, future)
        elif match.group('label') is not None:
            label = match.group('label')
            destination = target(match.group('dest'), base, future)
        elif match.group('code') is not None:
            label = match.group('code')
            candidate = base / label
            if label.startswith(('/', '~/','https://','http://')) or candidate.exists():
                try:
                    destination = target(label, base, future)
                except (OSError, ValueError):
                    destination = None  # z. B. Pfad mit Leerzeichen, an der Wortgrenze abgeschnitten
        else:
            label = label.rstrip('.,;:')
            tail = match.group(0)[len(label):]
            if label.startswith(('/', '~/','https://','http://')) or (base / label).exists():
                try:
                    destination = target(label, base, future)
                except (OSError, ValueError):
                    destination = None  # nicht existierender oder abgeschnittener Pfad bleibt Klartext
        if destination:
            links.append(destination)
            encoded.append('{\\field{\\*\\fldinst HYPERLINK "' + rtf(destination) + '"}{\\fldrslt ' + rtf(label) + '}}')
        else:
            encoded.append(rtf(label))
        plain.append(label)
        encoded.append(rtf(tail))
        plain.append(tail)
        cursor = match.end()
    encoded.append(rtf(line[cursor:]))
    plain.append(line[cursor:])
    return ''.join(encoded), ''.join(plain)


def project_base(source, explicit=None):
    """Git-Projektwurzel (auch Worktree-.git-Datei), sonst Quellverzeichnis."""
    if explicit:
        base = Path(explicit).expanduser().resolve(strict=True)
        if not base.is_dir():
            raise ValueError('Projektwurzel muss ein Verzeichnis sein')
        return base
    for parent in source.parents:
        if (parent / '.git').exists():
            return parent
    return source.parent


def render(source, output, project_root=None):
    source = Path(source).resolve(strict=True)
    if Path(output).exists() or Path(output).is_symlink():
        raise FileExistsError(f'Existing answer document protected: {output}')
    base = project_base(source, project_root)
    future = Path(output).resolve()
    lines = source.read_text(encoding='utf-8').splitlines()
    body, visible, links = [], [], []
    fence = None
    user_original = False
    answer_continuation = False
    for line in lines:
        continuation_for_line = answer_continuation
        answer_continuation = False
        if fence is None and not user_original and line == '<!-- answer:end -->':
            continue
        # Originalblöcke erhalten jede Zeile wörtlich, auch Markdown und Pfadangaben.
        # Marker in normalen Codeblöcken bleiben dagegen sichtbare Beispiele.
        if fence is None and line == '<!-- user-original:start -->':
            if user_original:
                raise ValueError('Nested user-original block')
            user_original = True
            continue
        if fence is None and line == '<!-- user-original:end -->':
            if not user_original:
                raise ValueError('Unmatched user-original end')
            user_original = False
            continue
        if user_original:
            body.append('{\\pard' + RESET + '\\fs36' + GOLD + ' ' + rtf(line) + '\\par}\n')
            visible.append(line)
            continue
        boundary = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if boundary and fence is None:
            fence = boundary.group(1)
            continue
        if boundary and fence and boundary.group(1)[0] == fence[0] and len(boundary.group(1)) >= len(fence) and not boundary.group(2).strip():
            fence = None
            continue
        if fence:
            body.append('{\\pard' + RESET + '\\fs30 ' + rtf(line) + '\\par}\n')
            visible.append(line)
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            line = heading.group(2)
        if line.startswith('> Ich habe das Handoff beantwortet:'):
            line = line[2:]
        # Kopierzeile ist eine ungeteilte Pfadangabe, auch mit Leerzeichen.
        copyline = re.match(r'^(Ich habe das Handoff beantwortet: )(.+)$', line)
        if copyline:
            raw = copyline.group(2).strip('`')
            destination = target(raw, base, future)
            links.append(destination)
            plain = copyline.group(1) + raw
            encoded = rtf(copyline.group(1)) + '{\\field{\\*\\fldinst HYPERLINK "' + rtf(destination) + '"}{\\fldrslt ' + rtf(raw) + '}}'
        else:
            encoded, plain = inline(line, base, links, future)
        style = '\\fs48\\b ' if heading else '\\fs36 '
        is_answer_marker = line.startswith('>>>')
        is_answer = is_answer_marker or (continuation_for_line and not heading)
        if is_answer:
            # Auch Antwortzeilen starten mit \plain: sonst leckt Fettdruck einer
            # vorangegangenen Ueberschrift in das Antwortfeld.
            style = RESET + style + GOLD + ' '
        else:
            style = RESET + style
        body.append('{\\pard' + style + encoded + '\\par}\n')
        visible.append(plain)
        answer_continuation = is_answer and bool(line.strip())
    if user_original:
        raise ValueError('Unclosed user-original block')
    # Dokumentstandard: 18 pt Gold. Alles, was ausserhalb der erzeugten
    # Absatzgruppen entsteht -- ein neuer Absatz hinter \par, per Cmd-V
    # eingefuegter Klartext, getippter Text -- erbt diesen Zustand. Ohne ihn galt
    # der RTF-Urstandard 12 pt ohne Hintergrund (Yasin, 12.09.2026, 21:03:
    # "wenn ich Cmd-V mache und Text eingebe ... kleine Schrift und ohne gelb").
    data = ('{\\rtf1\\ansi\\deff0\\uc1{\\fonttbl{\\f0 Helvetica;}}'
            '{\\colortbl;\\red255\\green231\\blue153;\\red0\\green0\\blue0;}'
            '{\\stylesheet{\\s0\\f0\\fs36' + GOLD + ' Normal;}}'
            '\\f0\\fs36' + GOLD + '\n' + ''.join(body) + '}').encode('ascii')
    fields = re.findall(rb'\\fldinst HYPERLINK "([^"\r\n]+)"', data)
    if [f.decode('ascii') for f in fields] != links:
        raise ValueError('RTF hyperlink field verification failed')
    with tempfile.TemporaryDirectory(prefix='handoff-rtf-') as tmp:
        check = Path(tmp) / 'check.rtf'
        check.write_bytes(data)
        text = subprocess.run(['textutil','-convert','txt','-stdout',str(check)],
                              check=True, capture_output=True).stdout.decode('utf-8')
        if text.rstrip('\n') != '\n'.join(visible).rstrip('\n'):
            raise ValueError('RTF plain-text roundtrip differs')
    publish_new(output, data)
    print(f'{Path(output).absolute()} — text roundtrip and {len(links)} hyperlink fields verified; viewer QA pending')


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('source')
        parser.add_argument('output', nargs='?')
        parser.add_argument('--project-root', help='Basis relativer Dokumentlinks; sonst nächste Git-Wurzel')
        args = parser.parse_args()
        render(args.source, args.output or str(Path(args.source).with_suffix('.rtf')), args.project_root)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(2)
