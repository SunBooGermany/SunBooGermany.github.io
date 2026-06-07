#!/usr/bin/env python3
"""Create a Research Blog post in _posts/."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys
import unicodedata


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
    "nonlinear-optimization": "stochastic-nonlinear-optimization",
    "probabilistic-heuristic-model": "llm-probabilistic-approaches",
}


def yaml_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "research-note"


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Research Blog Markdown post.")
    parser.add_argument("--title", required=True, help="English post title.")
    parser.add_argument("--title-ko", default="", help="Korean post title.")
    parser.add_argument(
        "--category",
        help="Current research category slug. Legacy slugs are mapped with a warning.",
    )
    parser.add_argument(
        "--research-category",
        help="Compatibility alias for --category.",
    )
    parser.add_argument(
        "--research-group",
        choices=TAXONOMY.keys(),
        help="Optional taxonomy group; inferred from --category when omitted.",
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Post date (YYYY-MM-DD).")
    parser.add_argument("--slug", help="Optional URL/file slug; defaults to a slug of --title.")
    parser.add_argument("--draft", help="Markdown body file. Use '-' to read stdin.")
    parser.add_argument("--stdin", action="store_true", help="Read Markdown body from stdin.")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument("--tag", action="append", dest="tag_list", help="Repeat to add one tag.")
    parser.add_argument("--excerpt", default="", help="English listing summary.")
    parser.add_argument("--excerpt-ko", default="", help="Korean listing summary.")
    parser.add_argument("--paper-title", default="")
    parser.add_argument("--authors", default="")
    parser.add_argument("--venue", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--doi", default="")
    parser.add_argument("--arxiv", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument(
        "--overwrite",
        "--force",
        action="store_true",
        help="Overwrite an existing post at the same path.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the rendered post without writing.")
    return parser.parse_args()


def find_category(slug: str, requested_group: str | None) -> tuple[str, str, str]:
    current_slug = LEGACY_CATEGORY_ALIASES.get(slug, slug)
    if current_slug != slug:
        print(
            f"Warning: legacy category '{slug}' maps to '{current_slug}'.",
            file=sys.stderr,
        )

    groups = [requested_group] if requested_group else TAXONOMY.keys()
    for group in groups:
        if group and current_slug in TAXONOMY[group]:
            return group, current_slug, TAXONOMY[group][current_slug]

    valid = ", ".join(
        sorted(category for categories in TAXONOMY.values() for category in categories)
    )
    raise ValueError(f"Unknown research category '{slug}'. Choose one of: {valid}.")


def resolve_taxonomy(args: argparse.Namespace) -> tuple[str, str, str]:
    category = args.category or args.research_category
    if not category:
        raise ValueError("Provide --category with a current research taxonomy slug.")
    return find_category(category, args.research_group)


def collect_tags(args: argparse.Namespace) -> list[str]:
    tags = split_csv(args.tags)
    if args.tag_list:
        tags.extend(tag.strip() for tag in args.tag_list if tag.strip())
    seen: set[str] = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
    return unique_tags or ["TODO"]


def read_template_body(root: Path) -> str:
    template_path = root / "_drafts" / "TEMPLATE-research-note.md"
    template = template_path.read_text(encoding="utf-8")
    parts = template.split("---", 2)
    return parts[2].lstrip("\n") if len(parts) == 3 else template


def read_body(args: argparse.Namespace, root: Path) -> str:
    if args.stdin and args.draft:
        raise ValueError("Use either --stdin or --draft, not both.")
    if args.stdin or args.draft == "-":
        body = sys.stdin.read()
    elif args.draft:
        draft_path = Path(args.draft)
        candidates = [draft_path]
        if not draft_path.is_absolute():
            candidates = [Path.cwd() / draft_path, root / draft_path]
        for candidate in candidates:
            if candidate.exists():
                body = candidate.read_text(encoding="utf-8")
                break
        else:
            raise ValueError(f"Draft file not found: {args.draft}")
    else:
        body = read_template_body(root)

    body = body.strip()
    if "<!-- ko -->" not in body:
        print("Warning: draft body does not contain '<!-- ko -->'.", file=sys.stderr)
    return body


def render_front_matter(
    args: argparse.Namespace,
    note_date: date,
    research_group: str,
    research_category: str,
    research_label: str,
    tags: list[str],
) -> str:
    application_category = research_category if research_group == "application_reviews" else ""
    application_label = research_label if application_category else ""
    method_category = research_category if research_group == "algorithmic_reviews" else ""
    method_label = research_label if method_category else ""
    tag_lines = "\n".join(f'  - "{yaml_value(tag)}"' for tag in tags)

    return f"""---
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
---"""


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    try:
        note_date = date.fromisoformat(args.date)
    except ValueError:
        print("Error: --date must be in YYYY-MM-DD format.", file=sys.stderr)
        return 2

    try:
        research_group, research_category, research_label = resolve_taxonomy(args)
        body = read_body(args, root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    output_path = root / "_posts" / f"{note_date.isoformat()}-{slugify(args.slug or args.title)}.md"
    if output_path.exists() and not args.overwrite:
        print(f"Error: post already exists: {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1

    front_matter = render_front_matter(
        args,
        note_date,
        research_group,
        research_category,
        research_label,
        collect_tags(args),
    )
    post = f"{front_matter}\n\n{body}\n"

    if args.dry_run:
        print(output_path.relative_to(root))
        print(post)
        return 0

    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(post, encoding="utf-8")
    print(output_path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
