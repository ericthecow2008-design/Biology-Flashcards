// Geometric overlap audit for all diagrams, using real rendered geometry.
//  - Every stroked/filled shape outline (line, polyline, polygon, path, rect,
//    circle, ellipse) is sampled every ~1.5px via getPointAtLength and tested
//    against every <text>'s rendered bounding box. A shape whose outline runs
//    through a label is a collision; a label sitting wholly inside a shape
//    (e.g. "Na+" in its circle) never touches the outline, so it isn't flagged.
//  - Every <text> box is tested against every other <text> box.
// A crossing counts as "masked" (intentional line-behind-label treatment) if a
// var(--surface)/var(--bg) rect painted after the shape and before the text
// covers the crossing point.
// Usage: node check_overlaps.js            (reads diagrams.json)
//        DIAGRAMS=other.json node check_overlaps.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const diagrams = JSON.parse(fs.readFileSync(path.join(__dirname, process.env.DIAGRAMS || 'diagrams.json'), 'utf8'));
const html = `<!doctype html><html><head><style>
:root{--bg:#F5F6F1;--surface:#FFFFFF;--ink:#1B2E28;--ink-soft:#52645C;--ink-faint:#8B9A93;--border:#DCDFD3;
--accent:#B87820;--mod1:#215F7D;--mod2:#4D6B34;--bridge:#6E4C72;--good:#2F7A4C;--review:#A84B34;--visual:#4B58A6;}
body{margin:0;padding:10px;} svg{color:var(--ink);display:block;margin-bottom:20px;}
svg text{font-family:${process.env.FONT || `"Segoe UI","Helvetica Neue",Arial,"Noto Sans",sans-serif`};}
</style></head><body>${Object.entries(diagrams).map(([k, v]) => {
  const w = v.svg.match(/viewBox="0 0 ([\d.]+)/)[1];
  return `<div data-key="${k}">${v.svg.replace('<svg ', `<svg style="width:${w}px" `)}</div>`;
}).join('')}</body></html>`;

(async () => {
  const exe = require('./find_chromium')();  // any Chromium already on disk
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 900, height: 800 } });
  await page.setContent(html);
  const results = await page.evaluate(() => {
    const out = {};
    const PAD = 1.2; // shrink text boxes slightly so glyph-box edges merely grazing a shape don't count
    const SHAPES = 'line,polyline,polygon,path,rect,circle,ellipse';
    for (const holder of document.querySelectorAll('[data-key]')) {
      const key = holder.dataset.key; const svg = holder.querySelector('svg');
      const all = [...svg.querySelectorAll('*')];
      const order = new Map(all.map((el, i) => [el, i]));
      const texts = [...svg.querySelectorAll('text')].map(t => {
        const b = t.getBoundingClientRect();
        return { el: t, txt: t.textContent, r: { l: b.left + PAD, r: b.right - PAD, t: b.top + PAD, b: b.bottom - PAD } };
      });
      const masks = [...svg.querySelectorAll('rect')]
        .filter(r => /var\(--(surface|bg)\)/.test(r.getAttribute('fill') || ''))
        .map(r => ({ el: r, b: r.getBoundingClientRect() }));
      const hits = [];
      for (const sh of svg.querySelectorAll(SHAPES)) {
        if (sh.closest('defs')) continue;
        if (masks.some(m => m.el === sh)) continue; // masks themselves are not collisions
        const cs = getComputedStyle(sh);
        const stroked = cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0;
        const filled = cs.fill !== 'none' && sh.tagName !== 'line' && sh.tagName !== 'polyline';
        if (!stroked && !filled) continue;
        const len = sh.getTotalLength();
        const ctm = sh.getScreenCTM();
        const n = Math.max(2, Math.ceil(len / 1.5));
        const hitTexts = new Map();
        for (let i = 0; i <= n; i++) {
          const p = sh.getPointAtLength(len * i / n).matrixTransform(ctm);
          for (const t of texts) {
            if (p.x < t.r.l || p.x > t.r.r || p.y < t.r.t || p.y > t.r.b) continue;
            const masked = masks.some(m => order.get(m.el) > order.get(sh) && order.get(m.el) < order.get(t.el)
              && p.x >= m.b.left && p.x <= m.b.right && p.y >= m.b.top && p.y <= m.b.bottom);
            const prev = hitTexts.get(t) || { masked: 0, open: 0 };
            masked ? prev.masked++ : prev.open++;
            hitTexts.set(t, prev);
          }
        }
        for (const [t, c] of hitTexts) {
          const desc = sh.tagName + (sh.tagName === 'line' ? ` ${sh.getAttribute('x1')},${sh.getAttribute('y1')}→${sh.getAttribute('x2')},${sh.getAttribute('y2')}` : '')
            + ` [${stroked ? 'stroke' : 'fill-edge'}]`;
          hits.push({ open: c.open > 0, msg: `${c.open > 0 ? '' : 'masked '}"${t.txt}" × <${desc}>` });
        }
      }
      for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i].r, b = texts[j].r;
        if (a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b)
          hits.push({ open: true, msg: `TEXT×TEXT "${texts[i].txt}" / "${texts[j].txt}"` });
      }
      out[key] = hits;
    }
    return out;
  });
  await browser.close();
  let open = 0;
  for (const [k, hits] of Object.entries(results)) {
    if (!hits.length) continue;
    console.log(`== ${k}`);
    for (const h of hits) { console.log('   ' + h.msg); if (h.open) open++; }
  }
  console.log(`\nunmasked collisions: ${open}`);
})().catch(e => { console.error(e); process.exit(1); });
