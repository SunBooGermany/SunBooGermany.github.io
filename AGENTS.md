# AGENTS.md

## Site Scope

This is Sunwoo Kim's Jekyll GitHub Pages homepage:
`https://sunboogermany.github.io/`.

For normal post publishing, do not modify `index.html`, `styles.css`, `script.js`,
`_config.yml`, layouts, data files, or unrelated posts unless the user explicitly
requests it.

## Research Blog Posts

Research Blog posts live in `_posts/` and use `layout: post`.

For a normal publishing task, create exactly one new Markdown file named
`YYYY-MM-DD-safe-slug.md`. Prefer:

```bash
python scripts/new_research_note.py --title "..." --category safe-constrained-rl --tags "tag one,tag two" --draft path/to/draft.md
```

Use current category slugs from `_data/research_taxonomy.yml`. Legacy archive
slugs must remain available, but do not use them for new posts unless explicitly
requested. The generator fills taxonomy labels and application/method fields.

Write a complete English version first, then `<!-- ko -->`, then a complete
Korean version. Keep English panels clean English only. Set `language: "en-ko"`
and `has_korean_note: false` for new posts.

Use only confirmed paper metadata, source URLs, references, authors, venues, and
years. Leave unavailable metadata blank and report it at the end.

## Writing Style

For Research Blog posts and Better Judgment essays, write like a researcher
thinking in public: technical, skeptical, concise, and concrete. Preserve the
user's core argument, notation, and level of detail when editing supplied text.
Use first person only for reflective or personal writing; use direct analytical
prose for technical posts. Keep necessary mathematical, optimization, and
engineering terms; do not oversimplify them.

Avoid generic AI essay style. Do not use filler such as "In today's rapidly
evolving world," "delve into," "tapestry," "realm," "unlock," "seamless,"
"robust" as vague praise, "crucial," "pivotal," "it is important to note,"
"not only...but also," or similar inflated phrasing. Avoid forced three-part
lists, motivational endings, and generic concluding paragraphs. Remove empty
transitions such as "Moreover," "Furthermore," and "Additionally" unless the
logical relation is specific.

Prefer concrete claims over vague framing. Preserve uncertainty when the evidence
is limited: say "this is weak," "this assumption is strong," "this only works
if...," or "the argument does not prove..." when appropriate. Use varied sentence
length. Allow short blunt sentences.

Bad: "This study provides a crucial and robust framework for addressing complex
challenges in modern energy systems."

Good: "This framework is useful only if the learned continuation value remains
reliable inside the optimization loop. The main risk is not approximation error
itself, but biased decisions caused by locally wrong value gradients."

Bad: "In this post, I will delve into the fascinating world of reinforcement
learning and optimization."

Good: "This post is about one narrow question: when does an RL policy become
unreliable because it confuses epistemic and aleatoric uncertainty?"

Before finalizing a post, run this short self-audit:

1. Does any paragraph sound like generic AI filler?
2. Are there inflated adjectives or vague claims?
3. Is the conclusion saying something real, or just wrapping up?
4. Would a skeptical researcher find the statement precise?

## Research Writing Constraints

Summarize papers in original language; do not paste long copyrighted passages. Do
not fabricate sources or references. Do not overstate novelty, guarantees, safety,
feasibility, optimality, or theorem-backed claims. If a connection or extension is
speculative, label it as a proposed direction.

Use native MathML for mathematical notation that needs superscripts, subscripts,
summations, matrices, or optimization constraints. Use fenced code blocks only for
pseudocode, algorithm sketches, or terminal-like text.

## Better Judgment Notes

Better Judgment Notes are separate from the Research Blog. They live in
`_better_judgment/` and use `layout: judgment-post`. Prefer
`scripts/new_better_judgment_note.py` for new notes. Do not merge Better Judgment
content into Research Blog posts unless explicitly requested.

When the user asks to publish their pasted Better Judgment essay as-is, preserve
the supplied essay structure and make only the minimum front matter/path changes.

## Finish Checklist

Before finishing, verify the changed file list. Run feasible syntax/build checks.
Confirm the Research Blog index and relevant category page will include a new
post. Summarize files changed, missing metadata, and any checks that could not be
run. Commit or push only when the user explicitly asks to publish, upload, or
commit.
