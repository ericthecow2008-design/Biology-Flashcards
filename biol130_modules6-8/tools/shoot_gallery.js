// Render every new diagram the way the study page shows it, in light and dark, one PNG each:
//   work/gallery/<key>__light.png and work/gallery/<key>__dark.png
// LOOK at every image (Read tool) before using a diagram: labels legible, nothing cramped,
// nothing invisible in dark mode, and nothing that prints a statement's answer.
// Usage (from the kit folder):  node tools/shoot_gallery.js        (KEYS=a,b to shoot only some)
//   DIAGRAMS=path/to.json OUT=folder to shoot another file
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const src = process.env.DIAGRAMS || path.join(ROOT, 'work', 'diagrams_m68.json');
const outDir = path.resolve(process.env.OUT || path.join(ROOT, 'work', 'gallery'));
fs.mkdirSync(outDir, { recursive: true });
const diagrams = JSON.parse(fs.readFileSync(src, 'utf8'));
const keys = process.env.KEYS ? process.env.KEYS.split(',') : Object.keys(diagrams);

const LIGHT = `--bg:#F5F6F1;--surface:#FFFFFF;--ink:#1B2E28;--ink-soft:#52645C;--ink-faint:#8B9A93;--border:#DCDFD3;
--accent:#B87820;--mod1:#215F7D;--mod2:#4D6B34;--bridge:#6E4C72;--good:#2F7A4C;--review:#A84B34;--visual:#4B58A6;`;
const DARK = `--bg:#111C17;--surface:#17251F;--ink:#EAF0EC;--ink-soft:#AFC0B7;--ink-faint:#75897F;--border:#2A3D34;
--accent:#E1A24E;--mod1:#7CB6D6;--mod2:#9BC17E;--bridge:#CBA6CE;--good:#7FCC98;--review:#E28E70;--visual:#AEB9EE;`;

function page(vars) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  :root{${vars}} body{margin:0;padding:16px;background:var(--bg);font-family:Georgia,serif;}
  .diagramfig{margin:0 0 24px;padding:16px 14px 12px;background:var(--surface);border:1px solid var(--border);border-radius:12px;display:inline-block;text-align:center;}
  .diagramfig svg{display:inline-block;color:var(--ink);}
  .diagramfig svg text{font-family:"Work Sans","Segoe UI","Helvetica Neue",Arial,"Noto Sans",sans-serif;}
  figcaption{font-size:12px;color:var(--ink-soft);margin-top:10px;}
  </style></head><body>${keys.map(k => {
    const d = diagrams[k]; const w = d.svg.match(/viewBox="0 0 ([\d.]+)/)[1];
    return `<div><figure class="diagramfig" id="${k}">${d.svg.replace('<svg ', `<svg style="width:${w}px" `)}<figcaption>${d.title}</figcaption></figure></div>`;
  }).join('')}</body></html>`;
}

(async () => {
  const browser = await chromium.launch({ executablePath: require('./find_chromium')(), args: ['--no-sandbox'] });
  const p = await browser.newPage({ viewport: { width: 720, height: 900 }, deviceScaleFactor: 1.5 });
  for (const [name, vars] of [['light', LIGHT], ['dark', DARK]]) {
    await p.setContent(page(vars));
    await p.evaluate(() => document.fonts.ready);
    for (const k of keys) {
      await (await p.$(`#${k}`)).screenshot({ path: path.join(outDir, `${k}__${name}.png`) });
    }
  }
  await browser.close();
  console.log(`shot ${keys.length} diagram(s) x 2 themes into ${path.relative(ROOT, outDir) || outDir}/`);
})();
