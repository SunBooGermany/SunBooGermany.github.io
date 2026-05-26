# Sunwoo Kim Personal Homepage

This is Sunwoo Kim's academic homepage with a Jekyll-based Research Blog for reviewed technical notes and a Better Judgment Notes collection for occasional analytical reflections.

## Files

- `index.html`: main website
- `styles.css`: website styling
- `script.js`: English/Korean language toggle and content rendering
- `favicon.svg`: browser icon
- `robots.txt`: search-engine crawling rule
- `sitemap.xml`: Jekyll-rendered sitemap for both writing collections and their category pages
- `_layouts/`, `_data/`, `categories/`, and `judgment-categories/`: presentation and category infrastructure
- `_drafts/TEMPLATE-research-note.md`: required structure for a research note
- `_drafts/TEMPLATE-better-judgment-note.md`: required structure for a Better Judgment note
- `scripts/new_research_note.py`: scaffolds a post with validated category metadata
- `scripts/new_better_judgment_note.py`: scaffolds a reflection note with validated category and source metadata

## Recommended deployment: GitHub Pages

1. Create a public GitHub repository named exactly:

   `SunBooGermany.github.io`

2. Upload every file in this folder to the root of that repository. Do not add a `.nojekyll` file; GitHub Pages must run Jekyll to publish the research log.

3. GitHub Pages will serve the site at:

   `https://sunboogermany.github.io/`

4. After deployment, open Google Search Console and submit:

   `https://sunboogermany.github.io/sitemap.xml`

## Add a daily research note

Only these category slugs are permitted:

- `safe-constrained-rl` (`Safe & Constrained RL`)
- `nonlinear-optimization` (`Nonlinear Optimization`)
- `probabilistic-heuristic-model` (`Probabilistic Heuristics & Bayesian Search`)

Create a post skeleton from the template:

```bash
python scripts/new_research_note.py \
  --title "Critical note title" \
  --category safe-constrained-rl \
  --paper-title "Paper title" \
  --authors "Authors" \
  --venue "Venue" \
  --year "2026" \
  --source-url "https://example.org/stable-source" \
  --tag constrained-rl
```

The script creates a dated Markdown file in `_posts/`. Replace every `TODO` placeholder and write all ten default sections before publishing. Do not add separate research-connection or proposed-extension sections unless explicitly requested.

Populate front matter metadata and the `References` section only from the supplied paper, source text, metadata, bibliography, or verified source material. When available from those sources, include the paper's references in `References`; never infer missing citation details, and leave or report missing metadata rather than fabricate it. Do not claim guarantees or results beyond what the cited work establishes.

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

## Local preview

With Ruby and Bundler installed, GitHub Pages-compatible rendering can be previewed with:

```bash
gem install bundler jekyll
jekyll serve
```

Open `http://127.0.0.1:4000/` and verify the homepage at desktop and mobile widths, `/research-log/`, `/better-judgment/`, all category pages, and `/sitemap.xml`.

## Notes

- The homepage intentionally does not display a phone number.
- The profile image uses the public GitHub avatar URL. Replace it with a professional photo by saving a file such as `profile.jpg` and editing the `<img>` source in `index.html`.
- If a custom domain is purchased later, update the canonical URL and sitemap URL.
