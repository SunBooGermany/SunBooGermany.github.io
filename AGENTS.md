# AGENTS.md

## Repository purpose

This repository hosts Sunwoo Kim's personal academic homepage:

https://sunboogermany.github.io/

The site is a global research-brand platform for AI-enabled optimization, safe and constrained reinforcement learning, stochastic and nonlinear optimization, process systems engineering, chemical engineering, green hydrogen, direct air capture, and decision making under uncertainty.

The site should communicate a serious research identity, not a generic blog.

## Non-negotiable constraints

Do not break the deployed homepage.
Do not remove existing homepage sections unless explicitly requested.
Do not remove Google Scholar, LinkedIn, GitHub, or email links.
Do not remove English/Korean support.
Do not remove the Research Blog.
Do not remove Better Judgment Notes.
Do not merge Better Judgment Notes into the Research Blog.
Do not fabricate papers, awards, affiliations, citations, or achievements.
Do not overstate novelty, guarantees, safety, feasibility, or optimality.
Do not paste long copyrighted passages from papers.
Summarize papers in original language.
Do not attempt to trigger Chrome Translate or any browser-level translation UI from site JavaScript.

## Research Blog taxonomy

Research Blog has two fixed groups: Application Reviews and Algorithmic Reviews.

Use exactly these Application Reviews category slugs:

1. green-chemical-systems
2. energy-grids
3. bioprocess-systems
4. chemical-plants

Display labels:

1. Green Chemical Systems
2. Energy Grids
3. Bioprocess Systems
4. Chemical Plants

Use exactly these Algorithmic Reviews category slugs:

1. safe-constrained-rl
2. stochastic-nonlinear-optimization
3. llm-probabilistic-approaches
4. graph-represented-methods

Display labels:

1. Safe & Constrained RL
2. Stochastic & Nonlinear Optimization
3. LLM & Probabilistic Approaches
4. Graph-Represented Methods

Do not create new categories unless explicitly requested.

Legacy category URLs must remain available:

- nonlinear-optimization should point users toward stochastic-nonlinear-optimization.
- probabilistic-heuristic-model should point users toward llm-probabilistic-approaches.
- safe-constrained-rl remains a current category.

## Better Judgment Notes purpose

Better Judgment Notes remain a separate writing section focused on decision making, social phenomena, global affairs, philosophical reflections, and ideas from books, interviews, conversations, lectures, essays, and public affairs.

Use exactly these internal category slugs:

1. decision-making
2. social-phenomena
3. global-affairs

Display labels:

1. For Wiser Decision-Making / 더 현명한 의사결정을 내리기 위하여
2. Understanding Social Phenomena / 사회 현상을 이해하기 위하여
3. Understanding Global Affairs / 국제 정세의 흐름을 이해하기 위하여

Allowed `source_type` values:

- book
- interview
- lecture
- essay
- article
- personal-reflection
- public-affairs

## Better Judgment post format

Every Better Judgment note must use the `judgment-post` layout and contain:

1. Core insight
2. Why this matters
3. Decision-making principle
4. What this explains about people or systems
5. Practical implication
6. Limits of the idea
7. Connection to my life and research
8. Source metadata

The tone must be reflective but analytical, readable, practical without cliche, and intellectually serious. Clearly distinguish personal interpretation from verified facts. For public affairs or international politics, check factual claims against reliable sources before publication; do not make unsupported political or social claims.

Include Korean notes or translations only when provided. Do not fabricate Korean translations.

## Daily research-note purpose

Each daily note should show critical research judgment, not just summarize a paper.

Target readers:
- RL researchers
- safe/constrained RL researchers
- AI researchers
- optimization researchers
- process systems engineering researchers
- chemical engineering researchers
- clean-energy system researchers
- technical entrepreneurs

Tone:
- rigorous
- critical
- precise
- readable
- not promotional
- not exaggerated

## Required research-post structure

Each research post should contain:

1. Positioning
2. Problem setting
3. Prior research gap
4. Core idea
5. Mathematical structure
6. Why it can work
7. Assumptions and limitations
8. Critical assessment
9. References

Include a Korean note or Korean translation block only when provided. Use the existing collapsible `details` convention with `id="korean-note"` and `class="korean-note-block"` so the Korean Note button works.

Do not add separate sections connecting the paper to Sunwoo Kim's research or proposing extensions by default. Include such sections only when the user explicitly requests them.

## References policy

The `References` section must identify the focal paper and include references from the paper when they are available in the provided material.
Use reference details only from the provided paper, supplied source text, supplied metadata or bibliography, or verified source material.
Do not infer or fabricate missing references.
If the material does not provide enough reference information, leave missing items blank or report them as missing metadata in the final report.
Fill front matter metadata fields only when they are confirmed from the provided material or verified source material.

## Research post front matter schema

Use this schema for new Research Blog posts:

```yaml
---
layout: post
title: "..."
date: YYYY-MM-DD
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
research_group: algorithmic_reviews
research_category: safe-constrained-rl
research_category_label: "Safe & Constrained RL"
application_category: ""
application_category_label: ""
method_category: safe-constrained-rl
method_category_label: "Safe & Constrained RL"
paper_title: "..."
authors: "..."
venue: "..."
year: "..."
doi: ""
arxiv: ""
source_url: ""
tags:
  - ...
excerpt: "One or two sentence summary for listing pages."
language: "en-ko"
has_korean_note: false
---
```

Keep `category` and `category_label` for backward compatibility. For application-focused reviews, set `research_group: application_reviews`, set `application_category`, and leave `method_category` blank unless a secondary method category is explicitly needed. For algorithm-focused reviews, set `research_group: algorithmic_reviews`, set `method_category`, and leave `application_category` blank unless a secondary application category is explicitly needed.

## Quality rules

If a paper proves a theorem, state precisely what is proved.
If a paper only provides empirical evidence, do not describe it as a guarantee.
If assumptions are strong, say so.
If scalability is unclear, say so.
If feasibility or safety is approximate, say so.
Explain important equations intuitively when needed without changing their mathematical meaning.
If an explicitly requested connection or extension is speculative, label it as a proposed direction rather than a result.
Use English as the main language for published posts.
Include Korean notes or translations when provided.

## Equation rendering policy

Use native MathML for equations in research notes when notation requires mathematical layout, including superscripts, subscripts, accents, summations, matrices, expectations, or optimization constraints.
Do not render mathematical equations as fenced `text` code blocks or approximate mathematical layout with plain-text symbols when MathML can express the notation precisely.
Use inline `<math>...</math>` for mathematical notation inside prose and `<math display="block" aria-label="...">...</math>` for displayed equations.
Include an informative `aria-label` on displayed equations.
Plain-text code blocks may still be used for algorithm flows, pseudocode, or terminal-like sequences that are not mathematical notation.
Rely on the browser's native MathML layout by default; do not add global or research-post CSS that changes the `math` display mode, font, sizing, wrapping, overflow, or alignment unless it has been explicitly tested and requested.

## Sunwoo Kim's research positioning

When relevant, connect papers to:
- stochastic optimization
- robust optimization
- safe and constrained RL
- nonlinear optimization
- model predictive control
- multi-timescale decision making
- hydrogen and clean-energy supply chains
- direct air capture
- feasibility-critical planning and control
- optimization-compatible neural networks
- ICNN/PICNN/convexity-preserving surrogates
- Bellman/continuation-value approximation
- planning under exogenous Markovian uncertainty

## Commit style

For infrastructure:
Add Jekyll research-log infrastructure

For daily notes:
Add research note: <short title>
