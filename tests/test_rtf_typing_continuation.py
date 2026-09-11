"""AppKit regression for continuing a gold answer field before agent text."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


SWIFT_PROBE = r"""
import AppKit
import Foundation

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2])
let data = try Data(contentsOf: input)
var attributes: NSDictionary? = nil
guard let storage = NSTextStorage(rtf: data, documentAttributes: &attributes) else {
    fatalError("Could not load RTF")
}

let layout = NSLayoutManager()
let container = NSTextContainer(size: NSSize(width: 800, height: 800))
layout.addTextContainer(container)
storage.addLayoutManager(layout)
let view = NSTextView(frame: NSRect(x: 0, y: 0, width: 800, height: 800), textContainer: container)

let marker = (storage.string as NSString).range(of: ">>>Userantwort:")
guard marker.location != NSNotFound else { fatalError("Answer marker missing") }
view.setSelectedRange(NSRange(location: NSMaxRange(marker) + 1, length: 0))
view.insertText("Erster Absatz", replacementRange: view.selectedRange())
view.insertNewline(nil)
view.insertText("Fortsetzung", replacementRange: view.selectedRange())

let whole = NSRange(location: 0, length: storage.length)
guard let saved = view.rtf(from: whole) else {
    fatalError("Could not save RTF")
}
try saved.write(to: output)

let savedData = try Data(contentsOf: output)
guard let reloaded = NSTextStorage(rtf: savedData, documentAttributes: nil) else {
    fatalError("Could not reload RTF")
}
let target = (reloaded.string as NSString).range(of: "Fortsetzung")
guard target.location != NSNotFound else { fatalError("Inserted text missing") }
let attrs = reloaded.attributes(at: target.location, effectiveRange: nil)
let color = attrs[.backgroundColor] as? NSColor
let font = attrs[.font] as? NSFont
let rgb = color?.usingColorSpace(.deviceRGB)
let agent = (reloaded.string as NSString).range(of: "Agentenantwort")
guard agent.location != NSNotFound else { fatalError("Agent reply missing") }
let agentColor = reloaded.attribute(.backgroundColor, at: agent.location, effectiveRange: nil) as? NSColor
let payload: [String: Any] = [
    "red": rgb?.redComponent ?? -1,
    "green": rgb?.greenComponent ?? -1,
    "blue": rgb?.blueComponent ?? -1,
    "fontSize": font?.pointSize ?? -1,
    "agentHasBackground": agentColor != nil,
]
let encoded = try JSONSerialization.data(withJSONObject: payload, options: [.sortedKeys])
print(String(decoding: encoded, as: UTF8.self))
"""


class TypingContinuationTests(unittest.TestCase):
    def test_new_text_after_answer_paragraph_keeps_gold_and_18pt(self):
        with tempfile.TemporaryDirectory(prefix="handoff-typing-") as directory:
            root = Path(directory)
            source = root / "source.md"
            rendered = root / "answer.rtf"
            saved = root / "saved.rtf"
            probe = root / "probe.swift"
            source.write_text(">>>Userantwort:\n\nAgentenantwort", encoding="utf-8")
            probe.write_text(textwrap.dedent(SWIFT_PROBE), encoding="utf-8")

            result = subprocess.run(
                [str(SCRIPTS / "handoff-rtf.sh"), str(source), str(rendered)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run(
                ["swift", str(probe), str(rendered), str(saved)],
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "TMPDIR": "/tmp"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = json.loads(result.stdout)
            self.assertGreater(observed["red"], 0.95)
            self.assertGreater(observed["green"], 0.88)
            self.assertLess(observed["green"], 0.95)
            self.assertGreater(observed["blue"], 0.55)
            self.assertLess(observed["blue"], 0.7)
            self.assertAlmostEqual(observed["fontSize"], 18.0, places=1)
            self.assertFalse(observed["agentHasBackground"])


if __name__ == "__main__":
    unittest.main()
