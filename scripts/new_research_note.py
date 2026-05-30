#!/usr/bin/env python3
"""Create a research-note post from the repository template."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


TAXONOMY = {
    "application_reviews": {
        "green-chemical-systems": "Green Chemical Systems",
        "energy-grids": "Energy Grids",
        "bioprocess-systems": "Bioprocess Systems",
        "chemical-plants": "Chemical Plants",
    },
    "algorithmic_reviews": {
        "safe-constrained-rl": "Safe & Constrained RL",
        "stochastic-nonlinear-optimization": "Stochastic & Nonlinear Optimization",
        "llm-probabilistic-approaches": "LLM & Probabilistic Approaches",
        "graph-represented-methods": "Graph-Represented Methods",
    },
}

LEGACY_CATEGORY_ALIASES = {
    "safe-constrained-rl": ("algorithmic_reviews", "safe-constrained-rl"),
    "nonlinear-optimization": ("algorithmic_reviews", "stochastic-nonlinear-optimization"),
    "probabilistic-heuristic-model": ("algorithmic_reviews", "llm-probabilistic-approaches"),
}


def yaml_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "research-note"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a daily research note in _posts/.")
    parser.add_argument("--title", required=True, help="Title for the note.")
    parser.add_argument("--title-ko", default="TODO: Korean title", help="Korean title for the note.")
    parser.add_argument("--research-group", choices=TAXONOMY.keys())
    parser.add_argument("--research-category", help="Category slug within the selected research group.")
    parser.add_argument(
        "--category",
        choices=LEGACY_CATEGORY_ALIASES.keys(),
        help="Legacy category argument. Prefer --research-group and --research-category.",
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Publication date (YYYY-MM-DD).")
    parser.add_argument("--slug", help="Optional URL/file slug; defaults to a slug of the title.")
    parser.add_argument("--paper-title", default="TODO: paper title")
    parser.add_argument("--authors", default="TODO: authors")
    parser.add_argument("--venue", default="TODO: venue")
    parser.add_argument("--year", default="TODO")
    parser.add_argument("--doi", default="")
    parser.add_argument("--arxiv", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--tag", action="append", dest="tag_list", help="Repeat to add tags.")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument("--excerpt", default="TODO: add a one or two sentence critical summary.")
    parser.add_argument("--excerpt-ko", default="TODO: add the Korean translation of the summary.")
    return parser.parse_args()


def resolve_taxonomy(args: argparse.Namespace) -> tuple[str, str, str]:
    group = args.research_group
    category = args.research_category

    if args.category and not category:
        group, category = LEGACY_CATEGORY_ALIASES[args.category]
        if args.category != category:
            print(
                f"Warning: legacy category '{args.category}' maps to '{category}'.",
                file=sys.stderr,
            )

    if not group or not category:
        raise ValueError("Provide --research-group and --research-category.")

    valid_categories = TAXONOMY[group]
    if category not in valid_categories:
        options = ", ".join(sorted(valid_categories))
        raise ValueError(f"Category '{category}' is not valid for {group}. Choose one of: {options}.")

    return group, category, valid_categories[category]


def collect_tags(args: argparse.Namespace) -> list[str]:
    tags: list[str] = []
    if args.tags:
        tags.extend(tag.strip() for tag in args.tags.split(",") if tag.strip())
    if args.tag_list:
        tags.extend(tag.strip() for tag in args.tag_list if tag.strip())
    return tags or ["TODO"]


def main() -> int:
    args = parse_args()
    try:
        note_date = date.fromisoformat(args.date)
    except ValueError:
        print("Error: --date must be in YYYY-MM-DD format.", file=sys.stderr)
        return 2

    try:
        research_group, research_category, research_label = resolve_taxonomy(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    application_category = research_category if research_group == "application_reviews" else ""
    application_label = research_label if application_category else ""
    method_category = research_category if research_group == "algorithmic_reviews" else ""
    method_label = research_label if method_category else ""

    root = Path(__file__).resolve().parents[1]
    template_path = root / "_drafts" / "TEMPLATE-research-note.md"
    posts_dir = root / "_posts"
    note_slug = slugify(args.slug or args.title)
    output_path = posts_dir / f"{note_date.isoformat()}-{note_slug}.md"

    if output_path.exists():
        print(f"Error: post already exists: {output_path}", file=sys.stderr)
        return 1

    template = template_path.read_text(encoding="utf-8")
    body = template.split("---", 2)[2].lstrip("\n")
    tag_lines = "\n".join(f'  - "{yaml_value(tag)}"' for tag in collect_tags(args))
    note = f"""---
layout: post
title: "{yaml_value(args.title)}"
title_ko: "{yaml_value(args.title_ko)}"
date: {note_date.isoformat()}
category: {research_category}
category_label: "{yaml_value(research_label)}"
research_group: {research_group}
research_category: {research_category}
research_category_label: "{yaml_value(research_label)}"
application_category: "{yaml_value(application_category)}"
application_category_label: "{yaml_value(application_label)}"
method_category: "{yaml_value(method_category)}"
method_category_label: "{yaml_value(method_label)}"
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
excerpt_ko: "{yaml_value(args.excerpt_ko)}"
language: "en-ko"
has_korean_note: false
---

{body}"""

    posts_dir.mkdir(exist_ok=True)
    output_path.write_text(note, encoding="utf-8")
    print(output_path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
