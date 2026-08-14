# Sunwoo Kim Personal Homepage

This is Sunwoo Kim's academic homepage with a Jekyll-based Research Blog for reviewed technical notes and a Better Judgment Notes collection for occasional analytical reflections.

## Files

- `index.html`: main website
- `styles.css`: website styling
- `script.js`: English/Korean language toggle and homepage content rendering
- `assets/images/sunwoo-profile-20260530.jpg`: local homepage profile photo
- `_data/research_taxonomy.yml`: two-group Research Blog taxonomy
- `_data/categories.yml`: flat category list for compatibility and sitemap generation
- `_data/judgment_categories.yml`: Better Judgment category data
- `_layouts/`, `categories/`, and `judgment-categories/`: writing layouts and archive pages
- `_drafts/TEMPLATE-research-note.md`: required structure for a research note
- `_drafts/TEMPLATE-better-judgment-note.md`: required structure for a Better Judgment note
- `scripts/new_research_note.py`: scaffolds a post with validated research taxonomy metadata
- `scripts/new_better_judgment_note.py`: scaffolds a reflection note with validated category and source metadata
- `sitemap.xml`: Jekyll-rendered sitemap for homepage, writing pages, archives, and posts

## Recommended deployment: GitHub Pages

1. Create a public GitHub repository named exactly:

   `SunBooGermany.github.io`

2. Upload every file in this folder to the root of that repository. Do not add a `.nojekyll` file; GitHub Pages must run Jekyll to publish the Research Blog and Better Judgment pages.

3. GitHub Pages will serve the site at:

   `https://sunboogermany.github.io/`

4. After deployment, open Google Search Console and submit:

   `https://sunboogermany.github.io/sitemap.xml`

## Research Blog taxonomy

Research Blog posts are organized into two groups.

Application Reviews:

- `green-chemical-systems` (`Green Chemical Systems`)
- `energy-grids` (`Energy Grids`)
- `bioprocess-systems` (`Bioprocess Systems`)
- `chemical-plants` (`Chemical Plants`)

Algorithmic Reviews:

- `safe-constrained-rl` (`Safe & Constrained RL`)
- `stochastic-nonlinear-optimization` (`Mathematical Optimization`)
- `llm-probabilistic-approaches` (`LLM & Probabilistic Approaches`)
- `graph-represented-methods` (`Graph-Represented Methods`)

Legacy archive URLs remain available for older links:

- `/categories/nonlinear-optimization/`
- `/categories/probabilistic-heuristic-model/`

## Add a daily research note

Create a post skeleton from the template:

```bash
python scripts/new_research_note.py \
  --date 2026-05-28 \
  --research-group algorithmic_reviews \
  --research-category stochastic-nonlinear-optimization \
  --title "Trust Regions for Nonlinear Stochastic MPC" \
  --paper-title "..." \
  --authors "..." \
  --venue "..." \
  --tags "trust region, stochastic MPC, nonlinear optimization"
```

For an application-focused review, use `--research-group application_reviews` and one of the application category slugs. For an algorithm-focused review, use `--research-group algorithmic_reviews` and one of the algorithmic category slugs.

The script creates a dated Markdown file in `_posts/`. Replace every `TODO` placeholder and write the required sections before publishing. Do not add separate research-connection or proposed-extension sections unless explicitly requested.

Populate front matter metadata and the `References` section only from the supplied paper, source text, metadata, bibliography, or verified source material. When available from those sources, include the paper's references in `References`; never infer missing citation details, and leave or report missing metadata rather than fabricate it. Do not claim guarantees or results beyond what the cited work establishes.

## Add bilingual versions

Do not try to trigger Chrome's built-in translation UI. Websites cannot reliably open Chrome Translate through JavaScript.

Every new homepage post should include a complete English version and a complete Korean version.

Use the in-site language-panel convention:

1. Write the complete English version first.
2. Keep the English version clean English only; do not mix Korean prose into it.
3. Add `<!-- ko -->` after the English version.
4. Write the complete Korean translation after `<!-- ko -->`.
5. Set `has_korean_note: false`.
6. Add `title_ko` and `excerpt_ko` in front matter.

```markdown
## Positioning

English version goes here.

## References

English references go here.

<!-- ko -->

## 포지셔닝

한국어 번역본을 여기에 작성합니다.

## 참고문헌

한국어 참고문헌 정보를 여기에 작성합니다.
```

Do not add short `Korean Note` or `Korean technical note` blocks for new posts. Legacy note blocks can remain only for older posts that already use them.

## Format technical equations

Research-note equations use native MathML so superscripts, subscripts, accents, and optimization notation render as mathematical typography without an external script dependency. Use inline `<math>...</math>` notation in prose and a labelled display element for important equations:

```html
<math display="block" aria-label="Estimated Lyapunov action value">
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>D</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>+</mo>
  <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>T</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
</math>
```

Do not place display equations in fenced `text` blocks. Fenced text blocks remain appropriate for algorithm flows or pseudocode.

## Add a Better Judgment note

Better Judgment Notes use only these categories:

- `decision-making` (`For Wiser Decision-Making` / `더 현명한 의사결정을 내리기 위하여`)
- `social-phenomena` (`Understanding Social Phenomena` / `사회 현상을 이해하기 위하여`)
- `global-affairs` (`Understanding Global Affairs` / `국제 정세의 흐름을 이해하기 위하여`)

Allowed `source_type` values are `book`, `interview`, `lecture`, `essay`, `article`, `personal-reflection`, and `public-affairs`.

Create a note skeleton:

```bash
python scripts/new_better_judgment_note.py \
  --date 2026-05-26 \
  --category decision-making \
  --title "Decision Quality and Long-Term Thinking" \
  --source-type book \
  --source-title "TODO: verified source title" \
  --author-or-speaker "TODO: verified author" \
  --tags "decision making,judgment,long-term thinking"
```

The script writes a collection document beneath `_better_judgment/<category>/<year>/<month>/<day>/`, producing a categorized `/better-judgment/` URL through Jekyll's supported collection `:path` permalink. It refuses to overwrite an existing note unless `--force` is explicitly passed. Replace placeholders before publication and do not present interpretation as verified fact. Any note involving current public affairs or international politics must be checked against reliable sources before it is published.

Better Judgment Notes should also use the bilingual version convention above for new notes.

## Local preview and validation

With Ruby and Bundler installed, GitHub Pages-compatible rendering can be previewed with:

```bash
gem install bundler jekyll
jekyll serve
```

Open `http://127.0.0.1:4000/` and verify:

- homepage loads correctly
- profile photo appears without distortion
- three homepage cards appear: Profile & Credentials, Research Blog, Better Judgment Notes
- mobile layout has no horizontal overflow
- `/research-log/` shows Application Reviews and Algorithmic Reviews
- all eight Research Blog category pages work
- legacy category URLs still work
- `/better-judgment/` and Better Judgment category pages work
- English/Korean language toggle shows the correct version on bilingual posts
- `/sitemap.xml` includes current writing archives

## Notes

- The homepage intentionally does not display a phone number.
- The homepage uses a local profile photo at `assets/images/sunwoo-profile-20260530.jpg`.
- If a custom domain is purchased later, update the canonical URL and sitemap URL.
