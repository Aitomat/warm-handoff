"""Vollständige neue Dateien atomar veröffentlichen; keine Editoroperationen."""
import os
from pathlib import Path
import tempfile


def publish_new(path, data):
    """link(2) schützt auch bei Konkurrenz vorhandene Dateien und Symlinks."""
    path = Path(path).absolute()
    fd, temp = tempfile.mkstemp(prefix='.handoff-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temp, path)
    finally:
        os.unlink(temp)
