"""Am Dokumentende getippter Text: schwarze Schrift auf Gold, 18 pt.

Yasin, 13.09.2026: „es wird gelbe Schrift eingefuegt, und kleiner, nicht
schwarze Schrift mit gelbem Hintergrund. Darueber siehst du die normale
Schriftgroesse und den gelben Hintergrund. Das brauchen wir."

Geprueft wird zweifach: die Steuerwoerter der letzten `>>>`-Zeile und des
Dokumentstandards im erzeugten RTF, und der AppKit-Roundtrip, bei dem hinter
das letzte Zeichen getippt und danach neu eingelesen wird.
"""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Gold-Hintergrund, wie ihn der Renderer schreibt, plus ausdruecklich Schwarz.
GOLD_WORDS = ("\\cb1", "\\cbpat1", "\\chshdng0", "\\chcbpat1", "\\cf2")


SWIFT_PROBE = r"""
import AppKit
import Foundation

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let data = try Data(contentsOf: input)
guard let storage = NSTextStorage(rtf: data, documentAttributes: nil) else {
    fatalError("Could not load RTF")
}
let layout = NSLayoutManager()
let container = NSTextContainer(size: NSSize(width: 800, height: 800))
layout.addTextContainer(container)
storage.addLayoutManager(layout)
let view = NSTextView(frame: NSRect(x: 0, y: 0, width: 800, height: 800),
                      textContainer: container)

// Genau das, was Yasin tut: ans Dokumentende klicken und tippen.
view.setSelectedRange(NSRange(location: storage.length, length: 0))
view.insertText("Test 123", replacementRange: view.selectedRange())

guard let saved = view.rtf(from: NSRange(location: 0, length: storage.length)),
      let reloaded = NSTextStorage(rtf: saved, documentAttributes: nil) else {
    fatalError("Could not roundtrip RTF")
}
let target = (reloaded.string as NSString).range(of: "Test 123")
guard target.location != NSNotFound else { fatalError("Inserted text missing") }
let attrs = reloaded.attributes(at: target.location, effectiveRange: nil)
let back = (attrs[.backgroundColor] as? NSColor)?.usingColorSpace(.deviceRGB)
let fore = ((attrs[.foregroundColor] as? NSColor) ?? NSColor.textColor)
    .usingColorSpace(.deviceRGB)
let font = attrs[.font] as? NSFont
let payload: [String: Any] = [
    "backRed": back?.redComponent ?? -1,
    "backGreen": back?.greenComponent ?? -1,
    "backBlue": back?.blueComponent ?? -1,
    "foreRed": fore?.redComponent ?? -1,
    "foreGreen": fore?.greenComponent ?? -1,
    "foreBlue": fore?.blueComponent ?? -1,
    "fontSize": font?.pointSize ?? -1,
]
let encoded = try JSONSerialization.data(withJSONObject: payload,
                                         options: [.sortedKeys])
print(String(decoding: encoded, as: UTF8.self))
"""

MARKDOWN = "# Titel\n\nAgententext.\n\n>>> Antwortbereich\n"


class EndOfDocumentTypingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="handoff-endtyping-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        source = self.root / "source.md"
        source.write_text(MARKDOWN, encoding="utf-8")
        self.rendered = self.root / "answer.rtf"
        result = subprocess.run(
            [str(SCRIPTS / "handoff-rtf.sh"), str(source), str(self.rendered)],
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_last_answer_paragraph_carries_black_on_gold_18pt(self):
        lines = self.rendered.read_text().splitlines()
        answer = [line for line in lines if "Antwortbereich" in line]
        self.assertEqual(len(answer), 1, lines)
        self.assertIn("\\fs36", answer[0])
        for word in GOLD_WORDS:
            self.assertIn(word, answer[0], answer[0])

    def test_document_default_is_black_on_gold_18pt(self):
        header = self.rendered.read_text().splitlines()[0]
        # Schwarz muss als eigener Farbtabelleneintrag existieren, sonst kann
        # \cf2 nicht "schwarze Schrift" bedeuten.
        self.assertIn("{\\colortbl;\\red255\\green231\\blue153;"
                      "\\red0\\green0\\blue0;}", header)
        self.assertIn("\\f0\\fs36", header)
        for word in GOLD_WORDS:
            self.assertIn(word, header, header)

    def test_typing_at_the_very_end_stays_black_on_gold_18pt(self):
        probe = self.root / "probe.swift"
        probe.write_text(textwrap.dedent(SWIFT_PROBE), encoding="utf-8")
        result = subprocess.run(
            ["swift", str(probe), str(self.rendered)],
            capture_output=True, text=True, check=False,
            env={**os.environ, "TMPDIR": "/tmp"})
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        # Gold #ffe799
        self.assertGreater(observed["backRed"], 0.95)
        self.assertGreater(observed["backGreen"], 0.88)
        self.assertLess(observed["backGreen"], 0.95)
        self.assertGreater(observed["backBlue"], 0.55)
        self.assertLess(observed["backBlue"], 0.7)
        # Schwarz, keinesfalls die Goldfarbe als Schrift.
        for channel in ("foreRed", "foreGreen", "foreBlue"):
            self.assertLess(observed[channel], 0.2, observed)
        self.assertAlmostEqual(observed["fontSize"], 18.0, places=1)


if __name__ == "__main__":
    unittest.main()
