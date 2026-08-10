"""Static validation for the GitHub profile README and generated SVG assets."""

from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_profile_assets  # noqa: E402


class ProfileAssetTest(unittest.TestCase):
    """Validate deterministic and safe profile assets."""

    def test_checked_in_assets_match_generator(self) -> None:
        self.assertEqual([], generate_profile_assets.check_assets(ROOT / "assets"))

    def test_svg_assets_are_well_formed_and_self_contained(self) -> None:
        expected_view_box = "0 0 1200 260"
        for name in ("profile-dark.svg", "profile-light.svg"):
            with self.subTest(name=name):
                content = (ROOT / "assets" / name).read_text(encoding="utf-8")
                root = ET.fromstring(content)
                self.assertEqual(expected_view_box, root.attrib["viewBox"])
                self.assertEqual("img", root.attrib["role"])
                self.assertNotIn("<script", content.lower())
                self.assertNotIn("http://", content.replace("http://www.w3.org/2000/svg", ""))
                self.assertNotIn("https://", content)
                self.assertIn("prefers-reduced-motion", content)
                self.assertIn("StormSpirit", content)
                self.assertIn("Multimodal LakeHouse infrastructure", content)
                self.assertIn(
                    "Governed multimodal data for distributed analytics and AI delivery.",
                    content,
                )
                self.assertIn(">LAKE</text>", content)
                self.assertIn(">HOUSE</text>", content)
                for project in ("Pista", "Tributo", "Gravitino", "Daft", "Ray"):
                    self.assertIn(project, content)
                for modality in ("TEXT", "IMAGE", "AUDIO", "VIDEO", "TABLE"):
                    self.assertIn(modality, content)

    def test_readme_references_existing_theme_assets(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in ("profile-dark.svg", "profile-light.svg"):
            self.assertTrue((ROOT / "assets" / name).is_file())
            self.assertIn(f"./assets/{name}", readme)
        self.assertIn("prefers-color-scheme: dark", readme)
        self.assertIn("prefers-color-scheme: light", readme)

    def test_readme_is_intentionally_image_only(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("<picture>", readme)
        self.assertIn("Multimodal LakeHouse infrastructure", readme)
        self.assertNotIn("###", readme)
        self.assertNotIn("<details>", readme)
        self.assertNotIn("mailto:", readme)

    def test_repository_contains_no_obvious_secret_markers(self) -> None:
        markers = ("github_pat_", "ghp_", "AKIA", "password=", "token=")
        paths = [ROOT / "README.md", *sorted((ROOT / "assets").glob("*.svg"))]
        for path in paths:
            content = path.read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(path=path.name, marker=marker):
                    self.assertNotIn(marker, content)


if __name__ == "__main__":
    unittest.main()
