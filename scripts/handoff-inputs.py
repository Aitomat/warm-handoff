#!/usr/bin/env python3
"""Explicit saved-source snapshots, revision checks and original-span ledger checks."""
import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import hashlib
import tempfile
from handoff_common import publish_new


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_source(path):
    path = Path(path).expanduser().resolve(strict=True)
    raw = path.read_bytes()
    if path.suffix.lower() == '.rtf':
        if not raw.startswith(b'{\\rtf'):
            raise ValueError(f'Invalid RTF: {path}')
        # Convert the captured bytes, not a file that can change mid-conversion.
        with tempfile.TemporaryDirectory(prefix='handoff-read-') as tmp:
            captured = Path(tmp) / 'source.rtf'
            captured.write_bytes(raw)
            text = subprocess.run(['textutil', '-convert', 'txt', '-stdout', str(captured)],
                                  check=True, capture_output=True).stdout.decode('utf-8')
    elif path.suffix.lower() in ('.md', '.txt'):
        text = raw.decode('utf-8')
    else:
        raise ValueError(f'Unsupported source format: {path}')
    return path, raw, text



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    snap = commands.add_parser('snapshot')
    snap.add_argument('--output', required=True)
    snap.add_argument('--first', action='store_true')
    snap.add_argument('--archive-dir', help='Originalbytes separat sichern; JSON enthält relativen Pfad und Hash.')
    snap.add_argument('sources', nargs='*')
    verify = commands.add_parser('verify')
    verify.add_argument('snapshot')
    ledger = commands.add_parser('ledger')
    ledger.add_argument('snapshot')
    ledger.add_argument('items')
    args = parser.parse_args()
    if args.command == 'snapshot':
        if bool(args.sources) == args.first:
            raise ValueError('Provide explicit sources OR --first (no sources).')
        output = Path(args.output).expanduser().absolute()
        if os.path.lexists(output):
            raise ValueError(f'Output already exists: {output}')
        archive_dir = Path(args.archive_dir).expanduser().resolve() if args.archive_dir else None
        sources = []
        for given in args.sources:
            path, raw, text = read_source(given)
            if any(s['path'] == str(path) for s in sources):
                raise ValueError(f'Duplicate source path: {path}')
            source = dict(path=str(path), sha256=digest(raw), text=text,
                          text_sha256=digest(text.encode('utf-8')))
            if archive_dir:
                archive_dir.mkdir(parents=True, exist_ok=True)
                archived = archive_dir / (digest(raw) + path.suffix.lower())
                try:
                    publish_new(archived, raw)
                except FileExistsError:
                    # Nur identische bereits archivierte Bytes wiederverwenden.
                    if archived.is_symlink() or archived.read_bytes() != raw:
                        raise ValueError(f'Conflicting archive: {archived}')
                source['archive_path'] = os.path.relpath(archived, output.parent.resolve())
            else:
                source['bytes_base64'] = base64.b64encode(raw).decode('ascii')
            sources.append(source)
        result = dict(version=2 if archive_dir else 1, saved_only=True, first=args.first,
                      read_at=datetime.now(timezone.utc).isoformat(), sources=sources)
        publish_new(output, json.dumps(result, ensure_ascii=False, indent=2).encode())
        print(f'Saved snapshot: {len(sources)} sources; unsaved editor text not included.')
        return
    snapshot = json.loads(Path(args.snapshot).read_text())
    if snapshot.get('version') not in (1, 2):
        raise ValueError('Unsupported snapshot version')
    sources = {s['path']: s for s in snapshot['sources']}
    if len(sources) != len(snapshot['sources']):
        raise ValueError('Duplicate source path')
    for source in sources.values():
        if ('bytes_base64' in source) == ('archive_path' in source):
            raise ValueError('Exactly one byte archive required')
        if 'archive_path' in source:
            raw = (Path(args.snapshot).resolve().parent / source['archive_path']).read_bytes()
        else:
            raw = base64.b64decode(source['bytes_base64'], validate=True)
        if digest(raw) != source['sha256']:
            raise ValueError('Corrupt snapshot archive')
        if digest(source['text'].encode('utf-8')) != source['text_sha256']:
            raise ValueError('Corrupt snapshot text')
    if args.command == 'verify':
        changed = [p for p, s in sources.items() if not Path(p).is_file()
                   or digest(Path(p).read_bytes()) != s['sha256']]
        if changed:
            raise ValueError('Sources changed/missing: ' + ', '.join(changed))
        print('Saved revisions unchanged; does not inspect unsaved editor text.')
        return
    items = json.loads(Path(args.items).read_text())
    seen = set()
    for item in items:
        if not item['id'] or item['id'] in seen:
            raise ValueError('Missing/duplicate item ID')
        seen.add(item['id'])
        text = sources[item['source']]['text']
        start, end = item['start'], item['end']
        if not (isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text)):
            raise ValueError('Invalid source span')
        if text[start:end] != item['original']:
            raise ValueError(f'Original changed: {item["id"]}')
        if item['status'] not in {'proposed','ready','running','done','deferred','needs_decision'}:
            raise ValueError('Invalid status')
        for key in ('interpretation', 'acceptance', 'evidence', 'next'):
            if key not in item:
                raise ValueError(f'Missing {key}')
        if item['status'] == 'done' and not item['evidence']:
            raise ValueError('Done item needs evidence')
    print(f'{len(items)} exact originals verified; semantic coverage needs reconciliation.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f'INCOMPLETE: {error}', file=sys.stderr)
        sys.exit(2)
