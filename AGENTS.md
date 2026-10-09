# AGENTS.md

## Site Scope

This is Sunwoo Kim's Jekyll GitHub Pages homepage:
`https://sunboogermany.github.io/`.

For normal post publishing, do not modify `index.html`, `styles.css`, `script.js`,
`_config.yml`, layouts, data files, or unrelated posts unless the user explicitly
requests it.

## Lecture Notes: Persistent Format Preference

The course title is "Surrogate Modeling for Process Prediction and Optimization"
("공정 예측과 최적화를 위한 서로게이트 모델링"). Use the course data for titles
and footers; do not label this course "AI for Chemical Engineers". The course
catalog is "Chemical Engineering Courses" ("화학공학 강의"). The user approved
the revised sequence on 2026-10-09:

1. Process prediction and surrogate modeling basics: define the prediction task,
   fit a steady-state regression baseline, and evaluate independent predictions.
   Week 1 is not a complete operating optimization workflow.
2. Multicomponent steady-state MLPs: scaling, forward/backpropagation, training,
   component errors, and concentration consistency.
3. Dynamic state-transition prediction and rollout with future inputs. RNN/LSTM
   and encoder–decoder architectures are optional extensions.
4. Physical consistency: residual losses and hard linear-equality projection.
5. Optimization problem definition and exact frozen-ReLU MILP formulation.
6. Practical formulations: bounds, scaling, OMLT, solver status/gaps/timing.
7. Design model structure for optimization: ICNN/PICNN and conditional LP usage.
8. Select operating conditions, revalidate with the reference process, compare
   economic performance, and identify useful additional data.

Week 1 uses engineering prediction questions as motivation. Operating optimization
is a brief course-roadmap preview. Existing later-topic calculations may remain
as clearly optional extensions, outside the early weeks' required deliverables.

Week 2 explicitly shows that unconstrained multicomponent outputs can violate
concentration or mole-fraction sums, even with small prediction errors. Briefly
preview post-training correction and projection inside training. Week 4 develops
KKT-hPINN, its linear-equality guarantee and matrix assumptions, and backpropagation
through the fixed projection layer in detail.

For every lecture note, including Week 1 and all subsequent weeks, use a white
academic slide format inspired by Stephen Boyd's Convex Optimization lecture
slides. The user established this project preference on 2026-10-09.

- Use white 4:3 landscape pages, dark readable text, clear titles, native MathML,
  and generous whitespace. Place relevant text, equations, tables, and figures
  together; use side-by-side text and figure placement where appropriate.
- Write complete pages, each with one main topic. Separate pages in Markdown
  with `<!-- lecture-page -->`. Start each page with an `##` heading; give
  continuation pages a descriptive title. Never shrink text to fit a dense page.
- Start each week's initial slides with motivation, before formal learning
  objectives: a concrete chemical process engineer's problem, its importance,
  what makes it difficult, and the approach taught that week. Make the situation
  engaging and relatable, with an answerable engineering question. Use relevant
  original illustrations or comics when helpful. Do not put boilerplate such as
  "illustrative scenario" or "설명을 위한 개념 그림" below motivation artwork.
  Explain the teaching model's assumptions on the relevant technical pages;
  preserve technical accuracy and uncertainty.
- Provide reading materials directly, not only a list of external links. Create
  a self-contained bilingual `week-NN-reading.md` companion with explanations,
  worked derivations, exercises with short answer checks, and verified primary
  sources. Use the same page format and provide English/Korean PDFs. Link it
  from the weekly note and its download actions. Cite third-party readings and
  link to their official originals without copying or republishing long passages.
- Preserve technical content, notation, units, results, references, and the
  complete English/Korean versions separated by `<!-- ko -->`.
- Use the shared `course-note` layout and `assets/courses/lecture-notes.css`;
  keep the syllabus in its document format. On mobile, preserve page boundaries
  while allowing the page height to expand for readable text.
- Keep web page divisions and downloadable PDF pages identical, with page
  numbers and course/week labels. Regenerate both language PDFs after changing
  a note. `node scripts/render_lecture_notes.cjs` builds, checks, and exports the
  weekly notes; it requires local Jekyll and Playwright.
- Inspect rendered pages in both languages for clipped or overlapping content,
  split equations/figures, and unintended blank pages before finishing.
- Refer to Boyd's slides for layout only; retain original course content and
  figures. Do not copy the slides' text, figures, or branding.

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

Do not put ordinary prose, slogans, takeaways, question prompts, role labels,
short contrastive statements, or one-sentence summaries inside fenced code
blocks or other text-box-like formatting. Write them as normal paragraphs. When
the user wants wording visibly marked, use quotation marks inline, for example
"a cheap valid bound can be faster than an expensive repeated solve." Reserve
fenced blocks only for actual code, terminal output, pseudocode, algorithm
sketches, or data formats whose spacing must be preserved.

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
5. Search for fenced code blocks. Is every fenced block actual code, terminal
   output, pseudocode, an algorithm sketch, or spacing-sensitive data? If a
   fenced block only emphasizes prose, a slogan, a takeaway, or a short contrast,
   rewrite it as a normal sentence or an inline quoted sentence.

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
