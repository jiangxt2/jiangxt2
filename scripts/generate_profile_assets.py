#!/usr/bin/env python3
"""Generate the theme-aware SVG hero assets for the profile README."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "assets"


@dataclass(frozen=True)
class Theme:
    """Colors used to render one profile hero variant."""

    name: str
    background: str
    background_alt: str
    text: str
    muted: str
    line: str
    blue: str
    violet: str
    cyan: str
    green: str


THEMES = (
    Theme(
        name="dark",
        background="#0B1020",
        background_alt="#111827",
        text="#F8FAFC",
        muted="#94A3B8",
        line="#334155",
        blue="#60A5FA",
        violet="#A78BFA",
        cyan="#22D3EE",
        green="#34D399",
    ),
    Theme(
        name="light",
        background="#FFFFFF",
        background_alt="#F1F5F9",
        text="#0F172A",
        muted="#64748B",
        line="#CBD5E1",
        blue="#2563EB",
        violet="#7C3AED",
        cyan="#0891B2",
        green="#059669",
    ),
)


def render_svg(theme: Theme) -> str:
    """Render a deterministic, standalone SVG for *theme*."""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
  <title id="title">StormSpirit — Building Multimodal LakeHouse infrastructure</title>
  <desc id="desc">Text, image, audio, video, and table data converge into a governed LakeHouse for distributed analytics and AI delivery, with work across Pista, Tributo, Gravitino, Daft, and Ray.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{theme.background}"/>
      <stop offset="1" stop-color="{theme.background_alt}"/>
    </linearGradient>
    <linearGradient id="headline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{theme.blue}"/>
      <stop offset="0.52" stop-color="{theme.violet}"/>
      <stop offset="1" stop-color="{theme.cyan}"/>
    </linearGradient>
    <linearGradient id="route" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{theme.violet}"/>
      <stop offset="0.45" stop-color="{theme.blue}"/>
      <stop offset="0.74" stop-color="{theme.cyan}"/>
      <stop offset="1" stop-color="{theme.green}"/>
    </linearGradient>
    <radialGradient id="halo">
      <stop offset="0" stop-color="{theme.blue}" stop-opacity="0.16"/>
      <stop offset="0.55" stop-color="{theme.violet}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{theme.violet}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame">
      <rect width="1200" height="260" rx="24"/>
    </clipPath>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      text {{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
      .route-flow {{ stroke-dasharray: 2 14; animation: route-flow 18s linear infinite; }}
      @keyframes route-flow {{ to {{ stroke-dashoffset: -192; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .route-flow {{ animation: none; }}
      }}
    </style>
  </defs>

  <rect width="1200" height="260" rx="24" fill="url(#background)"/>
  <circle cx="940" cy="130" r="285" fill="url(#halo)" clip-path="url(#frame)"/>

  <g fill="none" stroke="{theme.line}" opacity="0.24">
    <circle cx="940" cy="130" r="62"/>
    <circle cx="940" cy="130" r="94"/>
  </g>

  <circle cx="52" cy="39" r="4" fill="{theme.green}"/>
  <text x="66" y="44" fill="{theme.muted}" font-size="12" font-weight="650" letter-spacing="2">STORMSPIRIT / JIANGXT2</text>

  <text x="52" y="103" fill="{theme.text}" font-size="35" font-weight="720" letter-spacing="-1">Building Multimodal</text>
  <text x="52" y="148" fill="url(#headline)" font-size="39" font-weight="760" letter-spacing="-1.2">LakeHouse infrastructure.</text>
  <text x="54" y="183" fill="{theme.muted}" font-size="15">Governed multimodal data for distributed analytics and AI delivery.</text>

  <text x="54" y="226" fill="{theme.muted}" font-size="11" font-weight="650" letter-spacing="1.7">PROJECTS</text>
  <text x="137" y="226" fill="{theme.text}" font-size="13" font-weight="600">Pista · Tributo · Gravitino · Daft · Ray</text>

  <g fill="none" stroke="{theme.line}" stroke-width="1.5" opacity="0.7">
    <path d="M 716 48 C 800 48 838 96 904 119"/>
    <path d="M 688 88 C 790 88 838 112 904 125"/>
    <path d="M 678 130 C 785 130 837 130 904 130"/>
    <path d="M 688 172 C 790 172 838 148 904 135"/>
    <path d="M 716 212 C 800 212 838 164 904 141"/>
    <path d="M 976 116 C 1026 91 1063 78 1103 78"/>
    <path d="M 976 144 C 1026 169 1063 182 1103 182"/>
  </g>
  <g class="route-flow" fill="none" stroke="url(#route)" stroke-linecap="round" stroke-width="2.5" opacity="0.9">
    <path d="M 716 48 C 800 48 838 96 904 119"/>
    <path d="M 688 88 C 790 88 838 112 904 125"/>
    <path d="M 678 130 C 785 130 837 130 904 130"/>
    <path d="M 688 172 C 790 172 838 148 904 135"/>
    <path d="M 716 212 C 800 212 838 164 904 141"/>
    <path d="M 976 116 C 1026 91 1063 78 1103 78"/>
    <path d="M 976 144 C 1026 169 1063 182 1103 182"/>
  </g>

  <g fill="{theme.background_alt}" stroke-width="2">
    <circle cx="716" cy="48" r="6" stroke="{theme.violet}"/>
    <circle cx="688" cy="88" r="6" stroke="{theme.blue}"/>
    <circle cx="678" cy="130" r="6" stroke="{theme.cyan}"/>
    <circle cx="688" cy="172" r="6" stroke="{theme.green}"/>
    <circle cx="716" cy="212" r="6" stroke="{theme.violet}"/>
  </g>
  <g fill="{theme.muted}" font-size="9" font-weight="700" letter-spacing="1.2" text-anchor="end">
    <text x="701" y="51">TEXT</text>
    <text x="673" y="91">IMAGE</text>
    <text x="663" y="133">AUDIO</text>
    <text x="673" y="175">VIDEO</text>
    <text x="701" y="215">TABLE</text>
  </g>

  <circle cx="940" cy="130" r="38" fill="{theme.background_alt}" stroke="url(#route)" stroke-width="2.5"/>
  <circle cx="940" cy="130" r="27" fill="none" stroke="{theme.line}"/>
  <circle cx="940" cy="130" r="4" fill="{theme.cyan}" filter="url(#glow)"/>
  <text x="940" y="115" text-anchor="middle" fill="{theme.muted}" font-size="9" font-weight="700" letter-spacing="1.3">LAKE</text>
  <text x="940" y="154" text-anchor="middle" fill="{theme.text}" font-size="11" font-weight="700" letter-spacing="1.1">HOUSE</text>

  <circle cx="1103" cy="78" r="8" fill="{theme.background_alt}" stroke="{theme.blue}" stroke-width="2"/>
  <circle cx="1103" cy="182" r="8" fill="{theme.background_alt}" stroke="{theme.green}" stroke-width="2"/>
  <text x="1120" y="82" fill="{theme.muted}" font-size="9" font-weight="700" letter-spacing="1.1">ANALYTICS</text>
  <text x="1120" y="186" fill="{theme.muted}" font-size="9" font-weight="700" letter-spacing="1.1">AI / ML</text>

  <text x="1148" y="226" text-anchor="end" fill="{theme.muted}" font-size="11">github.com/jiangxt2</text>
</svg>
'''


def generated_assets() -> dict[str, str]:
    """Return generated asset names and contents."""

    return {f"profile-{theme.name}.svg": render_svg(theme) for theme in THEMES}


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
    print(f"Generated {len(THEMES)} profile assets in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
