# AGENTS.md

## Repository purpose

This repository hosts Sunwoo Kim's personal academic homepage:

https://sunboogermany.github.io/

The site is intended to become a global research-brand platform for AI-enabled optimization, safe and constrained reinforcement learning, nonlinear optimization, probabilistic heuristic methods, process systems engineering, chemical engineering, green hydrogen, direct air capture, and decision making under uncertainty.

The site should communicate a serious research identity, not a generic blog.

## Non-negotiable constraints

Do not break the deployed homepage.
Do not remove existing homepage sections unless explicitly requested.
Do not remove Google Scholar, LinkedIn, GitHub, or email links.
Do not remove English/Korean support.
Do not fabricate papers, awards, affiliations, citations, or achievements.
Do not overstate novelty, guarantees, safety, feasibility, or optimality.
Do not paste long copyrighted passages from papers.
Summarize papers in original language.

## Research-log categories

Use exactly these internal category slugs:

1. safe-constrained-rl
2. nonlinear-optimization
3. probabilistic-heuristic-model

Display labels:

1. Safe & Constrained RL
2. Nonlinear Optimization
3. Probabilistic Heuristics & Bayesian Search

Do not create new categories unless explicitly requested.

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

## Required post structure

Each post should contain:

1. Positioning
2. Problem setting
3. Prior research gap
4. Core idea
5. Mathematical structure
6. Why it can work
7. Assumptions and limitations
8. Critical assessment
9. Connection to my research
10. Possible extension
11. Korean technical note
12. Citation and metadata

## Front matter schema

Every post must use:

---
layout: post
title: "..."
date: YYYY-MM-DD
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
paper_title: "..."
authors: "..."
venue: "..."
year: "..."
doi: "..."
arxiv: ""
source_url: ""
tags:
  - ...
excerpt: "One or two sentence summary for listing pages."
language: "en-ko"
---

## Quality rules

If a paper proves a theorem, state precisely what is proved.
If a paper only provides empirical evidence, do not describe it as a guarantee.
If assumptions are strong, say so.
If scalability is unclear, say so.
If feasibility or safety is approximate, say so.
If the connection to Sunwoo Kim's research is speculative, label it as a possible extension rather than a result.

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
