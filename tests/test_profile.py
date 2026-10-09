"""Static validation for the GitHub profile README and generated SVG assets."""

from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_BASE = "https://raw.githubusercontent.com/jiangxt2/jiangxt2/master/assets/"
sys.path.insert(0, str(ROOT / "scripts"))

import generate_profile_assets  # noqa: E402


class ReadmeImages(HTMLParser):
    """Collect image sources and fallback descriptions from the README."""

    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.sources: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value for name, value in attrs if value is not None}
        if tag == "img":
            self.images.append(attributes)
        elif tag == "source":
            self.sources.append(attributes)


class ProfileAssetTest(unittest.TestCase):
    """Validate deterministic assets, safe SVGs, and usable README fallbacks."""

    def test_checked_in_assets_match_generator(self) -> None:
        self.assertEqual([], generate_profile_assets.check_assets(ROOT / "assets"))

    def test_svg_assets_are_well_formed_and_self_contained(self) -> None:
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        for path in sorted((ROOT / "assets").glob("*.svg")):
            with self.subTest(name=path.name):
                content = path.read_text(encoding="utf-8")
                root = ET.fromstring(content)
                expected_view_box = (
                    "0 0 600 420"
                    if path.name.startswith("profile-mobile-")
                    else "0 0 1200 420"
                    if path.name.startswith("profile-")
                    else "0 0 420 228"
                )
                self.assertEqual(expected_view_box, root.attrib["viewBox"])
                self.assertEqual("img", root.attrib["role"])
                for element_id in root.attrib["aria-labelledby"].split():
                    self.assertIsNotNone(root.find(f".//*[@id='{element_id}']"))
                self.assertTrue(root.findtext("svg:title", namespaces=namespace))
                self.assertTrue(root.findtext("svg:desc", namespaces=namespace))
                self.assertNotIn("<script", content.lower())
                self.assertNotIn("<foreignobject", content.lower())
                self.assertNotIn("http://", content.replace(namespace["svg"], ""))
                self.assertNotIn("https://", content)
                self.assertNotIn("animation:", content)
                for element in root.iter():
                    self.assertFalse(
                        any(name.startswith("on") for name in element.attrib)
                    )
                    self.assertFalse(any("href" in name for name in element.attrib))

    def test_readme_references_existing_theme_assets(self) -> None:
        parser = ReadmeImages()
        parser.feed((ROOT / "README.md").read_text(encoding="utf-8"))
        referenced = set()
        for attributes in parser.images + parser.sources:
            url = attributes.get("src") or attributes["srcset"]
            self.assertTrue(url.startswith(ASSET_BASE), url)
            name = url.removeprefix(ASSET_BASE)
            self.assertTrue((ROOT / "assets" / name).is_file(), name)
            referenced.add(name)
        self.assertEqual(
            {path.name for path in (ROOT / "assets").glob("*.svg")}
            | {"wechat-official-account.jpg"},
            referenced,
        )
        self.assertEqual(6, len(parser.images))
        for attributes in parser.images:
            self.assertGreater(len(attributes.get("alt", "")), 30)
        for attributes in parser.sources:
            self.assertIn("prefers-color-scheme:", attributes["media"])

    def test_readme_has_narrow_screen_banner_and_wrapping_cards(self) -> None:
        parser = ReadmeImages()
        parser.feed((ROOT / "README.md").read_text(encoding="utf-8"))
        for theme in ("light", "dark"):
            self.assertTrue(
                any(
                    attributes["srcset"].endswith(f"profile-mobile-{theme}.svg")
                    and attributes["media"]
                    == f"(max-width: 600px) and (prefers-color-scheme: {theme})"
                    for attributes in parser.sources
                )
            )
        self.assertEqual("100%", parser.images[0]["width"])
        for attributes in parser.images[1:5]:
            self.assertEqual("400", attributes["width"])
        self.assertEqual("180", parser.images[-1]["width"])
        self.assertEqual("180", parser.images[-1]["height"])
        self.assertTrue(
            parser.images[-1]["src"].endswith("/wechat-official-account.jpg")
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn('width="49%"', readme)
        self.assertNotIn("<table", readme)

    def test_readme_contains_profile_content_and_truthful_contribution_labels(
        self,
    ) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for heading in (
            "About me",
            "Selected projects",
            "Open-source contributions",
            "Focus & stack",
            "Let's connect",
        ):
            self.assertIn(f"## {heading}", readme)
        self.assertIn("Thunderkeg", readme)
        self.assertNotIn("StormSpirit", readme)
        self.assertIn("community-maintained", readme)
        spark_row = next(
            line for line in readme.splitlines() if "/apache/spark/pull/58066" in line
        )
        self.assertIn("**Merged**", spark_row)
        self.assertNotIn("Open PR", spark_row)
        for function in ("bitmap_and", "bitmap_or", "bitmap_andnot", "bitmap_xor"):
            self.assertIn(f"`{function}`", spark_row)
        self.assertIn("https://jiangxt2.github.io/", readme)

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
