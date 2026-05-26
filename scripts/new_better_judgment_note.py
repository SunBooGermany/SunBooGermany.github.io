#!/usr/bin/env python3
"""Create a Better Judgment note from the repository template."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


CATEGORIES = {
    "decision-making": "For Wiser Decision-Making",
    "social-phenomena": "Understanding Social Phenomena",
    "global-affairs": "Understanding Global Affairs",
}

SOURCE_TYPES = (
    "book",
    "interview",
    "lecture",
    "essay",
    "article",
    "personal-reflection",
    "public-affairs",
)


def yaml_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "better-judgment-note"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a Better Judgment note in _better_judgment/."
    )
    parser.add_argument("--title", required=True, help="Title for the note.")
    parser.add_argument("--category", choices=CATEGORIES, required=True)
    parser.add_argument("--source-type", choices=SOURCE_TYPES, required=True)
    parser.add_argument("--source-title", required=True)
    parser.add_argument("--author-or-speaker", required=True)
    parser.add_argument("--date", default=date.today().isoformat(), help="Publication date (YYYY-MM-DD).")
    parser.add_argument("--slug", help="Optional safe URL/file slug; defaults to a slug of the title.")
    parser.add_argument("--year", default="TODO")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument("--excerpt", default="TODO: add a one or two sentence analytical summary.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing note at the same path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        note_date = date.fromisoformat(args.date)
    except ValueError:
        print("Error: --date must be in YYYY-MM-DD format.", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[1]
    template_path = root / "_drafts" / "TEMPLATE-better-judgment-note.md"
    note_slug = slugify(args.slug or args.title)
    output_dir = (
        root
        / "_better_judgment"
        / args.category
        / note_date.strftime("%Y")
        / note_date.strftime("%m")
        / note_date.strftime("%d")
    )
    output_path = output_dir / f"{note_slug}.md"

    if output_path.exists() and not args.force:
        print(f"Error: note already exists: {output_path}", file=sys.stderr)
        print("Use --force to overwrite it.", file=sys.stderr)
        return 1

    raw_tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    tags = raw_tags or ["TODO"]
    template = template_path.read_text(encoding="utf-8")
    body = template.split("---", 2)[2].lstrip("\n")
    tag_lines = "\n".join(f'  - "{yaml_value(tag)}"' for tag in tags)
    note = f"""---
layout: judgment-post
title: "{yaml_value(args.title)}"
date: {note_date.isoformat()}
category: {args.category}
category_label: "{yaml_value(CATEGORIES[args.category])}"
source_type: "{yaml_value(args.source_type)}"
source_title: "{yaml_value(args.source_title)}"
author_or_speaker: "{yaml_value(args.author_or_speaker)}"
year: "{yaml_value(args.year)}"
source_url: "{yaml_value(args.source_url)}"
tags:
{tag_lines}
excerpt: "{yaml_value(args.excerpt)}"
language: "en-ko"
---

{body}"""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(note, encoding="utf-8")
    print(output_path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
