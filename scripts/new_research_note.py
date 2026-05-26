#!/usr/bin/env python3
"""Create a research-note post from the repository template."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


CATEGORIES = {
    "safe-constrained-rl": "Safe & Constrained RL",
    "nonlinear-optimization": "Nonlinear Optimization",
    "probabilistic-heuristic-model": "Probabilistic Heuristics & Bayesian Search",
}


def yaml_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "research-note"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a daily research note in _posts/.")
    parser.add_argument("--title", required=True, help="Title for the note.")
    parser.add_argument("--category", choices=CATEGORIES, required=True)
    parser.add_argument("--date", default=date.today().isoformat(), help="Publication date (YYYY-MM-DD).")
    parser.add_argument("--slug", help="Optional URL/file slug; defaults to a slug of the title.")
    parser.add_argument("--paper-title", default="TODO: paper title")
    parser.add_argument("--authors", default="TODO: authors")
    parser.add_argument("--venue", default="TODO: venue")
    parser.add_argument("--year", default="TODO")
    parser.add_argument("--doi", default="")
    parser.add_argument("--arxiv", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--tag", action="append", dest="tags", help="Repeat to add tags.")
    parser.add_argument("--excerpt", default="TODO: add a one or two sentence critical summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        note_date = date.fromisoformat(args.date)
    except ValueError:
        print("Error: --date must be in YYYY-MM-DD format.", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[1]
    template_path = root / "_drafts" / "TEMPLATE-research-note.md"
    posts_dir = root / "_posts"
    note_slug = slugify(args.slug or args.title)
    output_path = posts_dir / f"{note_date.isoformat()}-{note_slug}.md"

    if output_path.exists():
        print(f"Error: post already exists: {output_path}", file=sys.stderr)
        return 1

    tags = args.tags or ["TODO"]
    template = template_path.read_text(encoding="utf-8")
    body = template.split("---", 2)[2].lstrip("\n")
    tag_lines = "\n".join(f"  - {yaml_value(tag)}" for tag in tags)
    note = f"""---
layout: post
title: "{yaml_value(args.title)}"
date: {note_date.isoformat()}
category: {args.category}
category_label: "{yaml_value(CATEGORIES[args.category])}"
paper_title: "{yaml_value(args.paper_title)}"
authors: "{yaml_value(args.authors)}"
venue: "{yaml_value(args.venue)}"
year: "{yaml_value(args.year)}"
doi: "{yaml_value(args.doi)}"
arxiv: "{yaml_value(args.arxiv)}"
source_url: "{yaml_value(args.source_url)}"
tags:
{tag_lines}
excerpt: "{yaml_value(args.excerpt)}"
language: "en-ko"
---

{body}"""

    posts_dir.mkdir(exist_ok=True)
    output_path.write_text(note, encoding="utf-8")
    print(output_path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
