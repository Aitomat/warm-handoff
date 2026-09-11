"""Semantic-surface parity checks for the active English and German editions."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "docs/language-matrix.json").read_text(encoding="utf-8"))
RULE = re.compile(r"<!--\s*rule:([A-Z]+-\d+)\s*-->")
SECTION = re.compile(r"<!--\s*section:([A-Z-]+)\s*-->")
PROMPT = re.compile(r"<!--\s*prompt:([a-z-]+)\s*-->\s*```text\n(.*?)\n```", re.DOTALL)
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def normalized_link(link):
    if link.startswith(("http://", "https://")):
        return link.replace(".de.md", ".md")
    path, marker, fragment = link.partition("#")
    path = path.replace(".de.md", ".md")
    return path + (marker + fragment if marker else "")


class LocaleParityTests(unittest.TestCase):
    def test_language_declaration_and_pairs_exist(self):
        self.assertEqual(MATRIX["canonical_language"], "en")
        self.assertEqual(MATRIX["complete_languages"], ["en", "de"])
        self.assertIn("es", MATRIX["deferred_languages"])
        for pair in MATRIX["pairs"]:
            self.assertTrue((ROOT / pair["en"]).is_file(), pair)
            self.assertTrue((ROOT / pair["de"]).is_file(), pair)

    def test_stable_rule_ids_match(self):
        for pair in MATRIX["pairs"]:
            if "rule_prefix" not in pair:
                continue
            english = RULE.findall((ROOT / pair["en"]).read_text(encoding="utf-8"))
            german = RULE.findall((ROOT / pair["de"]).read_text(encoding="utf-8"))
            self.assertTrue(english, pair)
            self.assertEqual(english, german, pair)
            self.assertTrue(all(rule.startswith(pair["rule_prefix"] + "-") for rule in english))

    def test_local_link_surfaces_match_after_locale_normalization(self):
        for pair in MATRIX["pairs"]:
            english = {normalized_link(x) for x in LINK.findall((ROOT / pair["en"]).read_text(encoding="utf-8"))}
            german = {normalized_link(x) for x in LINK.findall((ROOT / pair["de"]).read_text(encoding="utf-8"))}
            self.assertEqual(english, german, pair)

    def test_readme_section_and_prompt_contracts_match(self):
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        german = (ROOT / "README.de.md").read_text(encoding="utf-8")
        self.assertEqual(SECTION.findall(english), SECTION.findall(german))
        self.assertEqual(
            ["SURFACES", "INSTALLATION", "CODEX-START", "CLAUDE-START", "REFERENCES"],
            SECTION.findall(english),
        )
        english_prompts = dict(PROMPT.findall(english))
        german_prompts = dict(PROMPT.findall(german))
        expected_prompts = {
            f"{package_id}-{host}"
            for package_id in MATRIX["packages"]
            for host in ("codex", "claude")
        }
        self.assertEqual(set(english_prompts), expected_prompts)
        self.assertEqual(set(english_prompts), set(german_prompts))
        for package_id, package in MATRIX["packages"].items():
            entry = (ROOT / package["entry"]).read_text(encoding="utf-8").split("---", 2)[1]
            name = re.search(r"^name:\s*(\S+)$", entry, re.MULTILINE).group(1)
            contracts = {
                f"{package_id}-codex": (f"${name}", "AGENTS.md", "<ABSOLUTE_HANDOFF_PATH>", "Codex"),
                f"{package_id}-claude": (f"/{name}", "CLAUDE.md", "<ABSOLUTE_HANDOFF_PATH>", "Claude Code"),
            }
            for prompt_id, required in contracts.items():
                self.assertEqual(english_prompts[prompt_id].splitlines()[0], required[0])
                self.assertEqual(german_prompts[prompt_id].splitlines()[0], required[0])
                for token in required:
                    self.assertIn(token, english_prompts[prompt_id])
                    self.assertIn(token, german_prompts[prompt_id])

    def test_manual_semantic_review_scope_is_explicit(self):
        review = MATRIX["manual_semantic_review"]
        self.assertEqual(review["status"], "implementation_self_review_complete")
        self.assertEqual(review["reviewed_pairs"], len(MATRIX["pairs"]))
        self.assertIn("does not prove semantic equivalence", review["limitation"])

    def test_installable_german_entries_match_reviewed_mirrors(self):
        mirrors = {
            "SKILL.de.md": "variants/compact-de/SKILL.md",
            "variants/full/SKILL.de.md": "variants/full-de/SKILL.md",
        }
        for mirror, entry in mirrors.items():
            self.assertEqual(
                (ROOT / mirror).read_text(encoding="utf-8"),
                (ROOT / entry).read_text(encoding="utf-8"),
                (mirror, entry),
            )


if __name__ == "__main__":
    unittest.main()
