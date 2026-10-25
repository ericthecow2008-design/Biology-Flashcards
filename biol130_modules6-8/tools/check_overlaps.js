// Geometric layout check for the new diagrams, using real rendered geometry in Chromium.
//  - every pair of labels: their boxes must not overlap;
//  - every drawn outline (line, path, rect, circle, ellipse, polygon, polyline) is sampled every
//    ~1.5 px and must not run through a label, unless a mask (a rect filled with var(--surface) or
//    var(--bg), drawn after the shape and before the label, e.g. svgkit.label_box) covers that spot;
//  - every label must sit inside the drawing area.
// Usage (from the kit folder):  node tools/check_overlaps.js            (default font)
//                               FONT='"DejaVu Sans"' node tools/check_overlaps.js
//   DIAGRAMS=path/to.json to check another file (default work/diagrams_m68.json)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const src = process.env.DIAGRAMS || path.join(ROOT, 'work', 'diagrams_m68.json');
const diagrams = JSON.parse(fs.readFileSync(src, 'utf8'));
const FONT = process.env.FONT || '"Work Sans","Segoe UI","Helvetica Neue",Arial,"Noto Sans",sans-serif';
const VARS = `--bg:#F5F6F1;--surface:#FFFFFF;--ink:#1B2E28;--ink-soft:#52645C;--ink-faint:#8B9A93;--border:#DCDFD3;
--accent:#B87820;--mod1:#215F7D;--mod2:#4D6B34;--bridge:#6E4C72;--good:#2F7A4C;--review:#A84B34;--visual:#4B58A6;`;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
:root{${VARS}} body{margin:0;padding:10px;background:var(--surface);}
figure{margin:0 0 30px;} svg{display:block;color:var(--ink);} svg text{font-family:${FONT};}
</style></head><body>${Object.entries(diagrams).map(([k, d]) => {
  const w = d.svg.match(/viewBox="0 0 ([\d.]+)/)[1];
  return `<figure data-key="${k}">${d.svg.replace('<svg ', `<svg style="width:${w}px" `)}</figure>`;
}).join('')}<i id="probeS" style="color:var(--surface)"></i><i id="probeB" style="color:var(--bg)"></i></body></html>`;

(async () => {
  const browser = await chromium.launch({ executablePath: require('./find_chromium')(), args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 700, height: 900 } });
  await page.setContent(html);
  await page.evaluate(() => document.fonts.ready);
  const report = await page.evaluate(() => {
    const maskColors = [getComputedStyle(document.getElementById('probeS')).color,
                        getComputedStyle(document.getElementById('probeB')).color];
    const out = {};
    for (const fig of document.querySelectorAll('figure[data-key]')) {
      const key = fig.dataset.key;
      const svg = fig.querySelector('svg');
      const sb = svg.getBoundingClientRect();
      const all = Array.from(svg.querySelectorAll('*'));
      const order = new Map(all.map((el, i) => [el, i]));
      const inDefs = el => !!el.closest('defs, marker, clipPath, mask, pattern');
      const issues = [], masked = [];
      const texts = all.filter(el => el.tagName === 'text' && !inDefs(el)).map(t => {
        const r = t.getBoundingClientRect();
        const h = r.height;
        return { el: t, s: t.textContent.trim(), x0: r.left + 0.6, x1: r.right - 0.6, y0: r.top + 0.14 * h, y1: r.bottom - 0.12 * h };
      });
      for (const t of texts) {
        if (t.x0 < sb.left - 1 || t.x1 > sb.right + 1 || t.y0 < sb.top - 1 || t.y1 > sb.bottom + 1)
          issues.push(`label "${t.s}" runs outside the drawing area`);
      }
      for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i], b = texts[j];
        const w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
        if (w > 0.5 && h > 0.5 && w * h > 2) issues.push(`labels overlap: "${a.s}" / "${b.s}"`);
      }
      const masks = all.filter(el => el.tagName === 'rect' && !inDefs(el) && maskColors.includes(getComputedStyle(el).fill))
        .map(el => ({ el, r: el.getBoundingClientRect() }));
      const shapes = all.filter(el => el instanceof SVGGeometryElement && !inDefs(el));
      for (const sh of shapes) {
        const cs = getComputedStyle(sh);
        const stroked = cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0;
        const filled = cs.fill !== 'none' && !maskColors.includes(cs.fill);
        if (!stroked && !filled) continue;
        if (parseFloat(cs.opacity) === 0) continue;
        let len = 0;
        try { len = sh.getTotalLength(); } catch (e) { continue; }
        const m = sh.getScreenCTM();
        const hits = new Map();
        for (let d = 0; d <= len; d += 1.5) {
          const p = sh.getPointAtLength(d);
          const x = m.a * p.x + m.c * p.y + m.e, y = m.b * p.x + m.d * p.y + m.f;
          for (const t of texts) {
            if (x < t.x0 || x > t.x1 || y < t.y0 || y > t.y1) continue;
            const isMasked = masks.some(mk => order.get(mk.el) > order.get(sh) && order.get(mk.el) < order.get(t.el) &&
              x >= mk.r.left && x <= mk.r.right && y >= mk.r.top && y <= mk.r.bottom);
            const k = `${t.s}|${isMasked}`;
            hits.set(k, (hits.get(k) || 0) + 1);
          }
        }
        for (const [k, cnt] of hits) {
          const [s, isMasked] = k.split('|');
          const msg = `<${sh.tagName}> outline runs through label "${s}" (${cnt} points)`;
          (isMasked === 'true' ? masked : issues).push(msg);
        }
      }
      out[key] = { issues, masked };
    }
    return out;
  });
  await browser.close();
  let total = 0, totalMasked = 0;
  for (const [k, r] of Object.entries(report)) {
    total += r.issues.length; totalMasked += r.masked.length;
    for (const i of r.issues) console.log(`  ${k}: ${i}`);
  }
  console.log(`font: ${FONT.split(',')[0]} | diagrams: ${Object.keys(report).length} | masked crossings (fine): ${totalMasked} | unmasked collisions: ${total}`);
  process.exit(total ? 1 : 0);
})();
