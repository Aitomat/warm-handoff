"""Checks the public skill surface, progressive disclosure, and internal links."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "docs/language-matrix.json").read_text(encoding="utf-8"))
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class PublicSurfaceTests(unittest.TestCase):
    def test_compact_entry_is_shorter_than_full_and_selects_adapters(self):
        compact = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        full = (ROOT / "variants/full/SKILL.md").read_text(encoding="utf-8")
        # 14.09.2026: von 800 auf 900 angehoben. Der kompakte Einstieg traegt
        # jetzt die drei Stopp-Regeln und die Abschnittsfolge, weil genau diese
        # Punkte uebersprungen wurden, solange sie nur in der Referenz standen.
        self.assertLess(len(compact.split()), 900)
        self.assertGreater(len(full.split()), len(compact.split()))
        self.assertIn("references/codex.md", compact)
        self.assertIn("references/claude-code.md", compact)
        self.assertNotIn("CLAUDE.md", compact)
        self.assertNotIn("AGENTS.md", compact)

    def test_readme_exposes_variants_prompts_and_deferred_spanish(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in ("$warm-handoff", "/warm-handoff", "variants/full/SKILL.md",
                         "variants/compact-de/SKILL.md", "variants/full-de/SKILL.md",
                         "Spanish is deferred", "Do not copy the whole repository",
                         "compact-en", "compact-de", "full-en", "full-de"):
            self.assertIn(required, readme)

    def test_four_installable_variants_have_unique_skill_names(self):
        packages = MATRIX["packages"]
        self.assertEqual(set(packages), {"compact-en", "compact-de", "full-en", "full-de"})
        names = []
        for package in packages.values():
            entry = ROOT / package["entry"]
            self.assertEqual(entry.name, "SKILL.md")
            frontmatter = entry.read_text(encoding="utf-8").split("---", 2)[1]
            names.append(re.search(r"^name:\s*(\S+)$", frontmatter, re.MULTILINE).group(1))
        self.assertEqual(len(names), len(set(names)))

    def test_german_full_variants_recommend_the_german_compact_name(self):
        for source in (ROOT / "variants/full/SKILL.de.md", ROOT / "variants/full-de/SKILL.md"):
            introduction = source.read_text(encoding="utf-8").split("<!-- rule:WH-01 -->", 1)[0]
            self.assertIn("`warm-handoff-de`", introduction)

    def test_package_manifests_build_offline_without_historical_helpers(self):
        forbidden = {"docs/.sol-err", "scripts/codex-limit.sh", "scripts/skills-uebersicht.sh"}
        safe_scripts = {"scripts/handoff-rtf.sh", "scripts/render_rtf.py", "scripts/handoff_common.py"}
        for package_id, package in MATRIX["packages"].items():
            resources = package["resources"]
            self.assertFalse(forbidden.intersection(resources), package_id)
            self.assertFalse(any(item.startswith(("docs/", "tests/")) for item in resources), package_id)
            self.assertFalse(any("history" in item or "historie" in item for item in resources), package_id)
            self.assertEqual({item for item in resources if item.startswith("scripts/")}, safe_scripts)
            with tempfile.TemporaryDirectory(prefix="warm-handoff-package-") as directory:
                target = Path(directory)
                shutil.copy2(ROOT / package["entry"], target / "SKILL.md")
                for item in resources:
                    destination = target / item
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / item, destination)
                for source in target.rglob("*.md"):
                    for raw in LINK.findall(source.read_text(encoding="utf-8")):
                        if raw.startswith(("http://", "https://", "#")):
                            continue
                        self.assertTrue((source.parent / raw.split("#", 1)[0]).resolve().exists(),
                                        (package_id, source, raw))
                self.assertFalse(any((target / item).exists() for item in forbidden), package_id)

    def test_full_variant_uses_revision_local_reference_links(self):
        for source in (ROOT / "variants/full/SKILL.md", ROOT / "variants/full-de/SKILL.md"):
            text = source.read_text(encoding="utf-8")
            self.assertNotIn("github.com/Aitomat/warm-handoff/blob/main", text)
            self.assertIn("references/handoff-format", text)

    def test_active_instructions_exclude_personal_paths_and_historical_numbers(self):
        forbidden = ("/Users/", "W53", "223k", "4.380k", "240k", "258k",
                     "Yasins ausdrücklich gewähltes")
        for pair in MATRIX["pairs"]:
            for key in ("en", "de"):
                if pair[key].startswith("README"):
                    continue
                text = (ROOT / pair[key]).read_text(encoding="utf-8")
                for token in forbidden:
                    self.assertNotIn(token, text, (pair[key], token))

    def test_every_relative_markdown_link_exists(self):
        for pair in MATRIX["pairs"]:
            for key in ("en", "de"):
                source = ROOT / pair[key]
                for raw in LINK.findall(source.read_text(encoding="utf-8")):
                    if raw.startswith(("http://", "https://", "#")):
                        continue
                    target = raw.split("#", 1)[0]
                    base = ROOT if source.parts[-3:-1] == ("variants", "full") else source.parent
                    self.assertTrue((base / target).resolve().exists(), (source, raw))

    def test_provider_and_evidence_boundaries_are_explicit(self):
        codex = (ROOT / "references/codex.md").read_text(encoding="utf-8")
        claude = (ROOT / "references/claude-code.md").read_text(encoding="utf-8")
        routing = (ROOT / "references/model-routing.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", codex)
        self.assertIn("unknown", codex)
        self.assertIn("CLAUDE.md", claude)
        self.assertIn("version- and configuration-dependent", claude)
        self.assertIn("API specification", routing)
        self.assertIn("Client or host boundary", routing)
        self.assertIn("Session measurement", routing)


if __name__ == "__main__":
    unittest.main()
