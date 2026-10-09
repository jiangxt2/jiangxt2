#!/usr/bin/env python3
"""Generate the theme-aware SVG assets for the GitHub profile README."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "assets"


@dataclass(frozen=True)
class Theme:
    """Colors shared by a profile banner and its project cards."""

    name: str
    background: str
    background_alt: str
    text: str
    muted: str
    line: str
    cyan: str
    green: str


THEMES = (
    Theme(
        name="dark",
        background="#0D1117",
        background_alt="#11232B",
        text="#E6EDF3",
        muted="#9DAEBB",
        line="#2A3B48",
        cyan="#39D0D8",
        green="#69D9A9",
    ),
    Theme(
        name="light",
        background="#FFFFFF",
        background_alt="#EDF5F6",
        text="#172B3A",
        muted="#536875",
        line="#D3E0E7",
        cyan="#087F8C",
        green="#117955",
    ),
)


@dataclass(frozen=True)
class Project:
    """Visible copy for one selected project card."""

    slug: str
    title: str
    description: tuple[str, str]
    stack: str


PROJECTS = (
    Project(
        slug="pista",
        title="Pista",
        description=(
            "Parameterized SQL pipelines",
            "and target-specific OLAP delivery.",
        ),
        stack="Spark SQL / Scala / OLAP",
    ),
    Project(
        slug="tributo",
        title="Tributo",
        description=(
            "Distributed training, model bundles,",
            "and batch / online inference.",
        ),
        stack="Ray / Python / ML",
    ),
    Project(
        slug="ray",
        title="Ray connectors",
        description=(
            "Doris, ClickHouse, and Hive I/O",
            "for distributed Ray workloads.",
        ),
        stack="Doris / ClickHouse / Hive",
    ),
    Project(
        slug="daft",
        title="Daft + Doris",
        description=("Read and write Apache Doris", "from Daft data pipelines."),
        stack="Daft / Python / Apache Doris",
    ),
)


def svg_document(
    theme: Theme, width: int, height: int, title: str, description: str, body: str
) -> str:
    """Wrap artwork in a self-contained, accessible SVG document."""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{theme.background}"/>
      <stop offset="1" stop-color="{theme.background_alt}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{theme.cyan}"/>
      <stop offset="1" stop-color="{theme.green}"/>
    </linearGradient>
    <radialGradient id="halo">
      <stop offset="0" stop-color="{theme.cyan}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{theme.cyan}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{width}" height="{height}" rx="20"/></clipPath>
    <style>
      text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    </style>
  </defs>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="20" fill="url(#background)" stroke="{theme.line}"/>
{body}
</svg>
'''


def render_svg(theme: Theme, *, compact: bool = False) -> str:
    """Render a desktop or narrow-screen banner for *theme*."""

    if compact:
        body = f'''  <circle cx="520" cy="60" r="210" fill="url(#halo)" clip-path="url(#frame)"/>
  <circle cx="42" cy="48" r="5" fill="{theme.green}"/>
  <text x="58" y="55" fill="{theme.muted}" font-size="26" font-weight="600" letter-spacing="1.5">THUNDERKEG / JIANGXT2</text>
  <text x="40" y="135" fill="{theme.text}" font-size="48" font-weight="700" letter-spacing="-1.5">Distributed data.</text>
  <text x="40" y="198" fill="url(#accent)" font-size="48" font-weight="700" letter-spacing="-1.5">AI infrastructure.</text>
  <path d="M 42 242 H 556" stroke="{theme.line}"/>
  <text x="42" y="287" fill="{theme.muted}" font-size="26">Distributed analytics.</text>
  <text x="42" y="326" fill="{theme.muted}" font-size="26">From data to model delivery.</text>
  <text x="42" y="382" fill="{theme.text}" font-size="26" font-weight="500">Spark · Ray · Daft · Gravitino · OLAP</text>'''
        return svg_document(
            theme,
            600,
            420,
            "Thunderkeg / jiangxt2 — Distributed data and AI infrastructure",
            "Distributed analytics, data connectivity, and model delivery with Spark, Ray, Daft, Gravitino, and OLAP systems.",
            body,
        )

    body = f'''  <circle cx="990" cy="210" r="330" fill="url(#halo)" clip-path="url(#frame)"/>
  <g fill="none" stroke="{theme.line}" opacity="0.3">
    <circle cx="938" cy="208" r="92"/>
    <circle cx="938" cy="208" r="142"/>
  </g>
  <g fill="none" stroke="url(#accent)" stroke-width="2" stroke-linecap="round" opacity="0.8">
    <path d="M 842 142 C 875 149 882 175 903 182"/>
    <path d="M 1034 142 C 1001 149 994 175 973 182"/>
    <path d="M 842 274 C 875 267 882 241 903 234"/>
    <path d="M 1034 274 C 1001 267 994 241 973 234"/>
  </g>
  <g fill="{theme.background}" stroke="{theme.line}" stroke-width="1">
    <rect x="716" y="86" width="140" height="56" rx="14"/>
    <rect x="1020" y="86" width="140" height="56" rx="14"/>
    <rect x="716" y="274" width="140" height="56" rx="14"/>
    <rect x="1020" y="274" width="140" height="56" rx="14"/>
  </g>
  <g fill="{theme.text}" font-size="20" font-weight="600" text-anchor="middle">
    <text x="786" y="121">Spark</text>
    <text x="1090" y="121">Ray</text>
    <text x="786" y="309">Gravitino</text>
    <text x="1090" y="309">Daft</text>
  </g>
  <circle cx="938" cy="208" r="55" fill="{theme.cyan}" opacity="0.06"/>
  <circle cx="938" cy="208" r="49" fill="none" stroke="{theme.line}" opacity="0.5"/>
  <circle cx="938" cy="208" r="44" fill="{theme.background}" stroke="url(#accent)" stroke-width="2"/>
  <text x="938" y="216" fill="{theme.text}" font-size="23" font-weight="600" text-anchor="middle">Data</text>
  <circle cx="60" cy="50" r="5" fill="{theme.green}"/>
  <text x="77" y="57" fill="{theme.muted}" font-size="20" font-weight="600" letter-spacing="2">THUNDERKEG / JIANGXT2</text>
  <text x="56" y="152" fill="{theme.text}" font-size="64" font-weight="700" letter-spacing="-2">Distributed data.</text>
  <text x="56" y="232" fill="url(#accent)" font-size="64" font-weight="700" letter-spacing="-2">AI infrastructure.</text>
  <text x="60" y="285" fill="{theme.muted}" font-size="23">Distributed analytics. From data to model delivery.</text>
  <path d="M 60 323 H 650" stroke="{theme.line}"/>
  <text x="60" y="368" fill="{theme.text}" font-size="21" font-weight="500">Spark · Ray · Daft · Gravitino · OLAP</text>
  <text x="1140" y="382" fill="{theme.muted}" font-size="17" text-anchor="end">github.com/jiangxt2</text>'''
    return svg_document(
        theme,
        1200,
        420,
        "Thunderkeg / jiangxt2 — Distributed data and AI infrastructure",
        "Building tools for distributed analytics, data connectivity, and model delivery across Spark, Ray, Daft, Gravitino, and OLAP systems.",
        body,
    )


def render_project(theme: Theme, project: Project) -> str:
    """Render one project card with legible copy at narrow widths."""

    body = f'''  <path d="M 28 30 H 64" stroke="url(#accent)" stroke-width="4" stroke-linecap="round"/>
  <path d="M 367 35 H 387 V 55 M 387 35 L 366 56" fill="none" stroke="{theme.muted}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="28" y="83" fill="{theme.text}" font-size="32" font-weight="700" letter-spacing="-0.7">{escape(project.title)}</text>
  <text x="28" y="125" fill="{theme.muted}" font-size="19">{escape(project.description[0])}</text>
  <text x="28" y="153" fill="{theme.muted}" font-size="19">{escape(project.description[1])}</text>
  <text x="28" y="199" fill="{theme.cyan}" font-size="18" font-weight="500">{escape(project.stack)}</text>'''
    return svg_document(
        theme,
        420,
        228,
        project.title,
        " ".join(project.description) + " " + project.stack + ".",
        body,
    )


def generated_assets() -> dict[str, str]:
    """Return generated asset names and contents."""

    assets = {}
    for theme in THEMES:
        assets[f"profile-{theme.name}.svg"] = render_svg(theme)
        assets[f"profile-mobile-{theme.name}.svg"] = render_svg(theme, compact=True)
        for project in PROJECTS:
            assets[f"project-{project.slug}-{theme.name}.svg"] = render_project(
                theme, project
            )
    return assets


def write_assets(output_dir: Path) -> None:
    """Write all generated assets into *output_dir*."""

    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in generated_assets().items():
        (output_dir / name).write_text(content, encoding="utf-8")


def check_assets(output_dir: Path) -> list[str]:
    """Return asset names that are missing or differ from generated output."""

    mismatches = []
    for name, expected in generated_assets().items():
        path = output_dir / name
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            mismatches.append(name)
    return mismatches


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify checked-in assets")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory for generated SVG files",
    )
    return parser.parse_args()


def main() -> int:
    """Generate assets or verify that checked-in assets are current."""

    args = parse_args()
    if args.check:
        mismatches = check_assets(args.output_dir)
        if mismatches:
            print("Profile assets are out of date: " + ", ".join(mismatches))
            return 1
        print("Profile assets are current.")
        return 0

    write_assets(args.output_dir)
    print(f"Generated {len(generated_assets())} profile assets in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
