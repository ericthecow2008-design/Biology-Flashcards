// End-to-end check of the built study page in headless Chromium.
// Usage: node smoke_test.js        (after node build_html.js)
//   NEW_MODS=5,6,0  modules whose cards get answered + screenshotted (default 5,6,0)
//   NEW_ID_MIN=2000 ids at/above this count as "new" for the screenshots
//   CHROMIUM_PATH   optional browser binary (see find_chromium.js)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FILE_URL = 'file://' + path.resolve(__dirname, 'biol130-flashcards.html');
const cards = require('./cards_all.json');
const diagrams = require('./diagrams_all.json');
const NEW_MODS = (process.env.NEW_MODS || '5,6,0').split(',').map(Number);
const NEW_ID_MIN = Number(process.env.NEW_ID_MIN || 2000);
const OUT = path.resolve(__dirname, 'verify');
fs.mkdirSync(OUT, { recursive: true });
const executablePath = require('./find_chromium')();  // any Chromium already on disk

let fails = 0;
const fail = (m) => { fails++; console.log('FAIL:', m); };
const ok = (m) => console.log('OK:', m);

(async () => {
  const browser = await chromium.launch({ executablePath, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 900, height: 1000 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto(FILE_URL);
  await page.waitForSelector('#card');

  const mods = [...new Set(cards.map(c => c.mod).filter(m => m > 0))].sort((a, b) => a - b);
  const range = `${mods[0]}–${mods[mods.length - 1]}`;
  const st = await page.textContent('#statline');
  st.includes(String(cards.length)) ? ok(`statline shows ${cards.length} items`) : fail('statline: ' + st);
  const h1 = await page.textContent('h1');
  h1.includes(`Modules ${range}`) ? ok('title: ' + h1) : fail('title: ' + h1);
  const pills = await page.$$eval('#modRow button', bs => bs.map(b => b.textContent));
  const wantPills = ['All modules', ...mods.map(m => `Module ${m}`), 'Bridge'];
  JSON.stringify(pills) === JSON.stringify(wantPills) ? ok('module pills: ' + pills.join(' | ')) : fail('pills: ' + pills);

  let answered = 0;
  const order = [...NEW_MODS, ...[...mods, 0].filter(m => !NEW_MODS.includes(m))];
  for (const key of order) {
    await page.click(`#modRow button[data-key="${key}"]`);
    const expected = cards.filter(c => c.mod === key);
    const cc = await page.textContent('#cardCount');
    if (!cc.includes(`of ${expected.length}`)) { fail(`mod ${key}: count "${cc}" vs ${expected.length}`); continue; }
    const answeredTypes = new Set();
    let bad = 0, withFig = 0;
    for (let i = 0; i < expected.length; i++) {
      const c = expected[i];
      const info = await page.evaluate(() => {
        const card = document.getElementById('card');
        const fig = card.querySelector('.diagramfig');
        return { text: card.textContent, hasFig: !!fig, cap: fig ? fig.querySelector('figcaption').textContent : null,
                 svgOk: fig ? !!fig.querySelector('svg[viewBox]') : null };
      });
      const probe = (c.title || (c.type === 'tf' ? c.claim : c.stem)).slice(0, 50);
      if (!info.text.includes(probe)) { bad++; if (bad < 4) fail(`mod ${key} item ${i + 1}: expected card #${c.id} ("${probe}")`); }
      if (c.diagram) {
        withFig++;
        if (!(info.hasFig && info.svgOk && info.cap === diagrams[c.diagram].title)) { bad++; fail(`#${c.id}: diagram ${c.diagram} not rendered`); }
      } else if (info.hasFig) { bad++; fail(`#${c.id}: unexpected diagram`); }

      // answer the first card of each format correctly in the new modules
      if (NEW_MODS.includes(key) && !answeredTypes.has(c.type)) {
        answeredTypes.add(c.type); answered++;
        if (c.type === 'combo' || c.type === 'mc') await page.click(`#card .choicebtn[data-idx="${c.answerIndex}"]`);
        else if (c.type === 'tf') await page.click(`#card .tfbtn[data-val="${c.answer}"]`);
        else {
          for (let j = 0; j < c.pairs.length; j++) {
            await page.click(`#card .chip.left[data-left="${j}"]`);
            await page.click(`#card .chip.right[data-right="${j}"]`);
          }
          await page.click('#checkMatchBtn');
        }
        const res = await page.evaluate(() => {
          const r = document.querySelector('#card .resultbox');
          return r ? { cls: r.className, txt: r.textContent } : null;
        });
        const expl = c.type === 'combo' ? c.statements[0].explanation : c.explanation;
        if (!res || !res.cls.includes('correct') || res.cls.includes('incorrect') || !res.txt.includes(expl.slice(0, 40)) && c.type !== 'combo')
          fail(`#${c.id} (${c.type}): answering correctly did not show a correct result`);
        else ok(`mod ${key}: answered ${c.type} #${c.id} correctly -> result + explanation shown`);
      }
      if (i < expected.length - 1) await page.click('#nextBtn');
    }
    bad === 0 ? ok(`mod ${key}: all ${expected.length} cards render in order (${withFig} with diagrams)`) : fail(`mod ${key}: ${bad} problems`);
  }
  const st2 = await page.textContent('#statline');
  st2.includes(String(answered)) ? ok('statline after answering: ' + st2.replace(/\s+/g, ' ')) : fail('statline after answering: ' + st2);

  // phone width: no horizontal page scroll
  await page.setViewportSize({ width: 390, height: 900 });
  await page.click(`#modRow button[data-key="${NEW_MODS[0]}"]`);
  const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  over <= 0 ? ok('390px: no horizontal page overflow') : fail(`390px: page overflows by ${over}px`);
  await page.screenshot({ path: path.join(OUT, `phone_mod${NEW_MODS[0]}_light.png`), fullPage: false });

  // light/dark screenshots: up to two diagram cards per new module, plus one new bridge card
  await page.setViewportSize({ width: 900, height: 1000 });
  const shots = [];
  for (const m of NEW_MODS.filter(m => m > 0)) {
    cards.filter(c => c.mod === m && c.diagram && c.id >= NEW_ID_MIN).slice(0, 2).forEach(c => shots.push([`m${m}_${c.type}_${c.id}`, c]));
  }
  const br = cards.find(c => c.mod === 0 && c.id >= NEW_ID_MIN && c.type === 'combo');
  if (br) shots.push([`bridge_${br.type}_${br.id}`, br]);
  for (const scheme of ['light', 'dark']) {
    await page.emulateMedia({ colorScheme: scheme });
    for (const [name, c] of shots) {
      await page.click(`#modRow button[data-key="${c.mod}"]`);
      const list = cards.filter(x => x.mod === c.mod);
      const idx = list.findIndex(x => x.id === c.id);
      for (let k = 0; k < idx; k++) await page.click('#nextBtn');
      await page.locator('.wrap').screenshot({ path: path.join(OUT, `${name}__${scheme}.png`) });
    }
  }
  console.log(`screenshots in ${OUT} -- look at them (light and dark) before publishing`);
  errs.length ? fail('console/page errors: ' + errs.join(' | ')) : ok('no console or page errors');
  await browser.close();
  console.log(fails ? `\n${fails} FAILURE(S)` : '\nALL CHECKS PASSED');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
