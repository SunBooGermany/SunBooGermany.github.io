/* Build and export every weekly note from the same paginated web layout. */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const http = require('node:http');
const { spawnSync } = require('node:child_process');
let chromium;
try { ({ chromium } = require('playwright')); }
catch {
  ({ chromium } = require(path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright')));
}

const site = path.resolve(__dirname, '..');
const workspace = path.dirname(site);
const build = path.join(workspace, 'course-work/build-lecture');
const qa = path.join(workspace, 'course-work/qa/lecture-pages');
const skipBuild = process.argv.includes('--skip-build');
const checkOnly = process.argv.includes('--check-only');
const selectedNames = process.argv.find(arg => arg.startsWith('--only='))?.slice(7).split(',');
fs.mkdirSync(qa, { recursive: true });
if (!skipBuild) {
  const result = spawnSync(process.platform === 'win32' ? 'bundle.bat' : 'bundle',
    ['exec', 'jekyll', 'build', '--destination', build],
    { cwd: site, stdio: 'inherit', shell: process.platform === 'win32' });
  if (result.status !== 0) throw new Error('Jekyll build failed. Check the local Ruby/Jekyll installation.');
}

const courses = path.join(site, 'courses');
const documents = [];
function discover(directory) {
  for (const item of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, item.name);
    if (item.isDirectory()) discover(absolute);
    else if (/^week-\d+(?:-reading)?\.md$/.test(item.name)) {
      const source = fs.readFileSync(absolute, 'utf8');
      const field = name => source.match(new RegExp(`^${name}:\\s*(.+)$`, 'm'))?.[1].trim().replace(/^['"]|['"]$/g, '');
      if (field('layout') !== 'course-note') continue;
      if (!source.includes('<!-- lecture-page -->')) throw new Error(`${absolute}: explicit lecture pages are missing`);
      documents.push({ name: path.basename(absolute, '.md'), route: field('permalink'), en: field('pdf_en'), ko: field('pdf_ko') });
    }
  }
}
discover(courses);
const publicURL = fs.readFileSync(path.join(site, '_config.yml'), 'utf8').match(/^url:\s*["']?([^"'\s]+).*$/m)[1];
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.png': 'image/png', '.svg': 'image/svg+xml', '.pdf': 'application/pdf' };
const server = http.createServer((request, response) => {
  try {
    const requested = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const target = path.resolve(build, '.' + requested, requested.endsWith('/') ? 'index.html' : '');
    if (!target.startsWith(build + path.sep)) { response.writeHead(403).end(); return; }
    response.setHeader('Content-Type', types[path.extname(target)] || 'application/octet-stream');
    response.end(fs.readFileSync(target));
  } catch { response.writeHead(404).end('Not found'); }
});

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const reports = [];
  try {
    for (const note of documents.filter(note => !selectedNames || selectedNames.includes(note.name))) {
      for (const language of ['en', 'ko']) {
        const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
        await context.addInitScript(lang => localStorage.setItem('sunwoo-lang', lang), language);
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        const response = await page.goto(base + note.route, { waitUntil: 'networkidle' });
        if (response.status() !== 200) throw new Error(`Missing note: ${note.route}`);
        await page.evaluate(() => document.fonts.ready);
        const measure = async () => page.evaluate(() => {
          const panel = document.querySelector('.lecture-pages:not([hidden])');
          return {
            language: document.documentElement.lang,
            text: panel.innerText,
            math: panel.querySelectorAll('math').length,
            images: [...panel.querySelectorAll('img')].map(img => ({ source: img.getAttribute('src'), broken: !img.complete || !img.naturalWidth })),
            viewportOverflow: document.documentElement.scrollWidth > innerWidth + 1,
            pages: [...panel.querySelectorAll('.lecture-page')].map((slide, i) => {
              const content = slide.querySelector('.lecture-page-content');
              const footer = slide.querySelector('footer');
              const children = [...content.children];
              const bounds = content.getBoundingClientRect();
              return {
                number: i + 1, title: content.querySelector('h2')?.innerText,
                width: slide.getBoundingClientRect().width, height: slide.getBoundingClientRect().height,
                overflow: content.scrollHeight > content.clientHeight + 2,
                horizontalOverflow: content.scrollWidth > content.clientWidth + 2,
                footerOverlap: children.some(child => child.getBoundingClientRect().bottom > footer.getBoundingClientRect().top + 1),
                background: getComputedStyle(slide).backgroundColor,
                bodyFont: parseFloat(getComputedStyle(content).fontSize),
                contentHeight: bounds.height, usedHeight: content.scrollHeight,
              };
            })
          };
        });
        const desktop = await measure();
        function validate(result, mode) {
          const badPages = result.pages.filter(slide => !slide.title || slide.overflow || slide.footerOverlap || (mode !== 'mobile' && slide.horizontalOverflow) || slide.background !== 'rgb(255, 255, 255)');
          if (result.language !== language || result.images.some(img => img.broken) || (mode !== 'print' && result.viewportOverflow) || badPages.length || errors.length) {
            throw new Error(JSON.stringify({ note: note.name, language, mode, badPages, brokenImages: result.images.filter(img => img.broken), viewportOverflow: result.viewportOverflow, errors }, null, 2));
          }
        }
        validate(desktop, 'desktop');
        await page.locator('.lecture-pages:not([hidden]) .lecture-page').first().screenshot({ path: path.join(qa, `${note.name}-${language}-first.png`) });
        await page.emulateMedia({ media: 'print' });
        const print = await measure();
        validate(print, 'print');
        if (!checkOnly) {
          if (!note[language]) throw new Error(`Missing ${language} PDF destination for ${note.name}`);
          await page.evaluate(({ base, publicURL }) => {
            for (const link of document.querySelectorAll('a[href]')) {
              if (link.href.startsWith(base + '/')) {
                const url = new URL(link.href);
                link.href = publicURL + url.pathname + url.search + url.hash;
              }
            }
          }, { base, publicURL });
          const output = path.resolve(site, '.' + note[language]);
          if (!output.startsWith(site + path.sep)) throw new Error('PDF output must stay inside the site.');
          await page.pdf({ path: output, printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, tagged: true });
          // Keep the preview's downloads current after exporting new companions.
          const previewOutput = path.resolve(build, '.' + note[language]);
          if (!previewOutput.startsWith(build + path.sep)) throw new Error('Preview output must stay inside the build.');
          fs.mkdirSync(path.dirname(previewOutput), { recursive: true });
          fs.copyFileSync(output, previewOutput);
        }
        await page.emulateMedia({ media: 'screen' });
        await page.locator('[data-language-toggle]').click();
        if (await page.locator('html').getAttribute('lang') === language) throw new Error('Language toggle failed');
        await page.locator('[data-language-toggle]').click();
        await page.setViewportSize({ width: 390, height: 844 });
        const mobile = await measure();
        validate(mobile, 'mobile');
        await page.locator('.lecture-pages:not([hidden]) .lecture-page').first().screenshot({ path: path.join(qa, `${note.name}-${language}-mobile.png`) });
        reports.push({ note: note.name, language, count: desktop.pages.length, math: desktop.math, images: desktop.images.length,
          text: desktop.text, desktop: desktop.pages, print: print.pages, mobile: mobile.pages });
        await context.close();
      }
    }
    const reportPath = path.join(qa, 'browser-report.json');
    const previous = selectedNames && fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath, 'utf8')).filter(item => !selectedNames.includes(item.note)) : [];
    fs.writeFileSync(reportPath, JSON.stringify([...previous, ...reports], null, 2));
    console.log(JSON.stringify(reports.map(({ note, language, count, math, images }) => ({ note, language, pages: count, math, images, checks: 'desktop, print, mobile, language toggle' })), null, 2));
  } finally { await browser.close(); server.close(); }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });
