# Sunwoo Kim Personal Homepage

This is Sunwoo Kim's academic homepage with a Jekyll-based research log for reviewed daily technical notes.

## Files

- `index.html`: main website
- `styles.css`: website styling
- `script.js`: English/Korean language toggle and content rendering
- `favicon.svg`: browser icon
- `robots.txt`: search-engine crawling rule
- `sitemap.xml`: Jekyll-rendered sitemap for the homepage, research-log pages, and posts
- `_layouts/`, `_data/`, and `categories/`: research-log presentation and category infrastructure
- `_drafts/TEMPLATE-research-note.md`: required structure for a research note
- `scripts/new_research_note.py`: scaffolds a post with validated category metadata

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

The script creates a dated Markdown file in `_posts/`. Replace every `TODO` placeholder, verify all bibliographic fields against the source, and write all twelve required sections before publishing. Do not claim guarantees or results beyond what the cited work establishes.

## Local preview

With Ruby and Bundler installed, GitHub Pages-compatible rendering can be previewed with:

```bash
gem install bundler jekyll
jekyll serve
```

Open `http://127.0.0.1:4000/` and verify the homepage, `/research-log/`, all three category pages, and `/sitemap.xml`.

## Notes

- The homepage intentionally does not display a phone number.
- The profile image uses the public GitHub avatar URL. Replace it with a professional photo by saving a file such as `profile.jpg` and editing the `<img>` source in `index.html`.
- If a custom domain is purchased later, update the canonical URL and sitemap URL.
