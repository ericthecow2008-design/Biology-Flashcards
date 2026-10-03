// Render every diagram in a diagrams JSON inside a .diagramfig figure using the
// shared palette, in light and dark, and element-screenshot each one.
// Usage: DIAGRAMS=diagrams_m56.json OUT=gallery_m56 [KEYS=a,b] node shoot_gallery.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const src = process.env.DIAGRAMS || 'diagrams_m56.json';
const outDir = path.resolve(__dirname, process.env.OUT || 'gallery_m56');
fs.mkdirSync(outDir, { recursive: true });
const diagrams = JSON.parse(fs.readFileSync(path.join(__dirname, src), 'utf8'));
const keys = process.env.KEYS ? process.env.KEYS.split(',') : Object.keys(diagrams);

const LIGHT = `--bg:#F5F6F1;--surface:#FFFFFF;--ink:#1B2E28;--ink-soft:#52645C;--ink-faint:#8B9A93;--border:#DCDFD3;
--accent:#B87820;--mod1:#215F7D;--mod2:#4D6B34;--bridge:#6E4C72;--good:#2F7A4C;--review:#A84B34;--visual:#4B58A6;`;
const DARK = `--bg:#111C17;--surface:#17251F;--ink:#EAF0EC;--ink-soft:#AFC0B7;--ink-faint:#75897F;--border:#2A3D34;
--accent:#E1A24E;--mod1:#7CB6D6;--mod2:#9BC17E;--bridge:#CBA6CE;--good:#7FCC98;--review:#E28E70;--visual:#AEB9EE;`;

function page(vars) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  :root{${vars}} body{margin:0;padding:16px;background:var(--bg);font-family:Georgia,serif;}
  .diagramfig{margin:0 0 24px;padding:14px;background:var(--surface);border:1px solid var(--border);border-radius:6px;display:inline-block;}
  .diagramfig svg{display:block;color:var(--ink);}
  .diagramfig svg text{font-family:"Segoe UI","Helvetica Neue",Arial,"Noto Sans",sans-serif;}
  figcaption{font-size:12px;color:var(--ink-soft);margin-top:8px;}
  </style></head><body>${keys.map(k => {
    const d = diagrams[k]; const w = d.svg.match(/viewBox="0 0 ([\d.]+)/)[1];
    return `<div><figure class="diagramfig" id="${k}">${d.svg.replace('<svg ', `<svg style="width:${w}px" `)}<figcaption>${d.title}</figcaption></figure></div>`;
  }).join('')}</body></html>`;
}

(async () => {
  const exe = require('./find_chromium')();  // any Chromium already on disk
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  const pg = await browser.newPage({ viewport: { width: 760, height: 900 } });
  for (const [mode, vars] of [['light', LIGHT], ['dark', DARK]]) {
    await pg.setContent(page(vars));
    for (const k of keys) await pg.locator(`#${k}`).screenshot({ path: path.join(outDir, `${k}__${mode}.png`) });
  }
  await browser.close();
  console.log(`shot ${keys.length} diagrams x 2 themes into ${path.basename(outDir)}/`);
})().catch(e => { console.error(e); process.exit(1); });
