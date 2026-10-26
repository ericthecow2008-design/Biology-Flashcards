// End-to-end test of outputs/biol130-flashcards.html in headless Chromium (run after tools/update_page.py).
// Checks the header and pills; that every module kept its old cards; that every new card (all four
// formats) renders in order with its diagram and accepts its keyed answer; the Case studies filter alone
// and with each module; module colours; phone width; console errors. Saves screenshots to
// outputs/screens/: LOOK at them (light and dark) before publishing.
// Usage (from the kit folder):  node tools/page_test.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const FILE_URL = 'file://' + path.join(ROOT, 'outputs', 'biol130-flashcards.html');
const cards = JSON.parse(fs.readFileSync(path.join(ROOT, 'outputs', 'page_cards.json'), 'utf8'));
const diagrams = JSON.parse(fs.readFileSync(path.join(ROOT, 'outputs', 'page_diagrams.json'), 'utf8'));
const batch = JSON.parse(fs.readFileSync(path.join(ROOT, 'work', 'cards_m68.json'), 'utf8'));
const newIds = new Set(batch.map(c => c.id));
const before = cards.filter(c => !newIds.has(c.id));  // what the page held before this set
const OUT = path.join(ROOT, 'outputs', 'screens');
fs.mkdirSync(OUT, { recursive: true });

let fails = 0;
const fail = m => { fails++; console.log('FAIL:', m); };
const ok = m => console.log('OK:', m);
const probe = c => (c.title || (c.type === 'tf' ? c.claim : c.stem)).slice(0, 50);

async function answer(page, c) {
  if (c.type === 'combo' || c.type === 'mc') await page.click(`#card .choicebtn[data-idx="${c.answerIndex}"]`);
  else if (c.type === 'tf') await page.click(`#card .tfbtn[data-val="${c.answer}"]`);
  else {
    for (let j = 0; j < c.pairs.length; j++) {
      await page.click(`#card .chip[data-left="${j}"]`);
      await page.click(`#card .chip[data-right="${j}"]`);
    }
    await page.click('#checkMatchBtn');
  }
  const cls = await page.evaluate(() => { const r = document.querySelector('#card .resultbox'); return r ? r.className : ''; });
  return / correct/.test(' ' + cls) && !/incorrect/.test(cls);
}

async function cardInfo(page) {
  return page.evaluate(() => {
    const card = document.getElementById('card'); const fig = card.querySelector('.diagramfig');
    return { text: card.textContent, cap: fig ? fig.querySelector('figcaption').textContent : null,
             svg: fig ? !!fig.querySelector('svg[viewBox]') : false };
  });
}

(async () => {
  const browser = await chromium.launch({ executablePath: require('./find_chromium')(), args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 900, height: 1000 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error' && !/fonts\.googleapis|ERR_|net::/.test(m.text())) errs.push(m.text()); });
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto(FILE_URL);
  await page.waitForSelector('#card');

  const mods = [...new Set(cards.map(c => c.mod).filter(m => m > 0))].sort((a, b) => a - b);
  const st = await page.textContent('#statline');
  st.includes(String(cards.length)) ? ok(`statline shows ${cards.length} items`) : fail('statline: ' + st);
  const h1 = await page.textContent('h1');
  h1.includes(`Modules 1–${mods[mods.length - 1]}`) ? ok('title: ' + h1) : fail('title: ' + h1);
  const pills = await page.$$eval('#modRow button', bs => bs.map(b => b.textContent));
  const want = ['All modules', ...mods.map(m => `Module ${m}`), 'Bridge'];
  JSON.stringify(pills) === JSON.stringify(want) ? ok('module pills: ' + pills.join(' | ')) : fail('module pills: ' + pills.join(' | '));
  const types = await page.$$eval('#typeRow button', bs => bs.map(b => b.textContent));
  types[types.length - 1] === 'Case studies' ? ok('format pills end with Case studies') : fail('format pills: ' + types);

  // every module: old cards kept, new cards render in order with their diagrams and accept their keyed answer
  let walked = 0, answered = 0;
  for (const m of [...mods, 0]) {
    await page.click(`#modRow button[data-key="${m}"]`);
    await page.click('#typeRow button[data-key="all"]');
    const inView = cards.filter(c => c.mod === m);
    const n = before.filter(c => c.mod === m).length + batch.filter(c => c.mod === m).length;
    const cc = await page.textContent('#cardCount');
    if (!cc.includes(`of ${n}`) || inView.length !== n) { fail(`Module ${m}: "${cc}" but expected ${n} cards`); continue; }
    if (!inView.some(c => newIds.has(c.id))) continue;
    let bad = 0;
    for (let i = 0; i < inView.length; i++) {
      const c = inView[i];
      if (newIds.has(c.id)) {
        walked++;
        const info = await cardInfo(page);
        if (!info.text.includes(probe(c))) { bad++; if (bad < 4) fail(`Module ${m} item ${i + 1}: expected #${c.id} "${probe(c)}"`); }
        else if (c.diagram && !(info.svg && info.cap === diagrams[c.diagram].title)) { bad++; fail(`#${c.id}: diagram ${c.diagram} not shown`); }
        else if (!c.diagram && info.svg) { bad++; fail(`#${c.id}: shows a diagram it shouldn't`); }
        else if (!(await answer(page, c))) { bad++; fail(`#${c.id} (${c.type}): answering with the key did not show "Correct"`); }
        else answered++;
      }
      if (i < inView.length - 1) await page.click('#nextBtn');
    }
    if (!bad) ok(`${m === 0 ? 'Bridge' : 'Module ' + m}: ${n} cards; every new one renders and accepts its key`);
  }
  answered === batch.length ? ok(`all ${batch.length} new cards checked`) : fail(`only ${answered} of ${batch.length} new cards passed (${walked} reached)`);

  // the Case studies filter, alone and with each module
  await page.click('#typeRow button[data-key="case"]');
  for (const m of [...new Set(batch.filter(c => c.caseStudy).map(c => c.mod))]) {
    await page.click(`#modRow button[data-key="${m}"]`);
    const inView = cards.filter(c => c.mod === m && c.caseStudy);
    const cc = await page.textContent('#cardCount');
    const opts = await page.$$eval('#topicSelect option', os => os.map(o => o.textContent));
    const topics = [...new Set(inView.map(c => c.topic))];
    cc.includes(`of ${inView.length}`) && topics.every(t => opts.includes(t))
      ? ok(`Module ${m} + Case studies: ${inView.length} cards; topics ${topics.join(' | ')}`)
      : fail(`Module ${m} + Case studies: "${cc}" (expected ${inView.length}); topic menu ${opts}`);
  }
  await page.click('#modRow button[data-key="all"]');
  const allCase = cards.filter(c => c.caseStudy).length;
  const ccAll = await page.textContent('#cardCount');
  ccAll.includes(`of ${allCase}`) ? ok(`Case studies pill: ${allCase} cards`) : fail(`Case studies pill: "${ccAll}", expected ${allCase}`);
  await page.click('#typeRow button[data-key="all"]');

  // new module pills get their own colour when active
  for (const m of mods.filter(x => x >= 7)) {
    await page.click(`#modRow button[data-key="${m}"]`);
    await page.waitForTimeout(400);  // pills fade between colours
    const bg = await page.$eval(`#modRow button[data-key="${m}"]`, b => getComputedStyle(b).backgroundColor);
    const wantBg = await page.evaluate(k => { const i = document.createElement('i'); i.style.color = `var(--mod${k})`;
      document.body.appendChild(i); const c = getComputedStyle(i).color; i.remove(); return c; }, m);
    bg === wantBg ? ok(`Module ${m} pill has its own colour (${bg})`) : fail(`Module ${m} pill colour ${bg}, expected ${wantBg}`);
  }

  // screenshots: per module, the first new card of each format (question, then answered), light and dark
  for (const scheme of ['light', 'dark']) {
    await page.emulateMedia({ colorScheme: scheme });
    for (const m of [...new Set(batch.map(c => c.mod))]) {
      await page.click(`#modRow button[data-key="${m}"]`);
      await page.click('#typeRow button[data-key="all"]');
      const inView = cards.filter(c => c.mod === m);
      const firsts = ['combo', 'match', 'tf', 'mc'].map(t => inView.findIndex(c => newIds.has(c.id) && c.type === t && !c.caseStudy))
        .concat([inView.findIndex(c => newIds.has(c.id) && c.caseStudy)]).filter(i => i >= 0);
      let at = 0;
      for (const idx of firsts.sort((a, b) => a - b)) {
        while (at < idx) { await page.click('#nextBtn'); at++; }
        const c = inView[idx];
        const name = `mod${m}_${c.caseStudy ? 'case' : c.type}_${c.id}`;
        await page.waitForTimeout(150);
        await (await page.$('#card')).screenshot({ path: path.join(OUT, `${name}_question_${scheme}.png`) });
        await answer(page, c);
        await page.waitForTimeout(150);
        await (await page.$('#card')).screenshot({ path: path.join(OUT, `${name}_answered_${scheme}.png`) });
      }
    }
    await page.screenshot({ path: path.join(OUT, `header_${scheme}.png`), clip: { x: 0, y: 0, width: 900, height: 420 } });
  }
  await page.emulateMedia({ colorScheme: 'light' });

  // phone width: no sideways page scroll on any new card
  await page.setViewportSize({ width: 390, height: 900 });
  let widest = 0;
  for (const m of [...new Set(batch.map(c => c.mod))]) {
    await page.click(`#modRow button[data-key="${m}"]`);
    const inView = cards.filter(c => c.mod === m);
    for (let i = 0; i < inView.length; i++) {
      if (newIds.has(inView[i].id)) widest = Math.max(widest, await page.evaluate(() => document.documentElement.scrollWidth));
      if (i < inView.length - 1) await page.click('#nextBtn');
    }
  }
  widest <= 390 ? ok(`phone width: no sideways page scroll (widest ${widest}px)`) : fail(`page scrolls sideways at 390px (${widest}px)`);

  errs.length ? fail('console errors: ' + errs.join(' | ')) : ok('no console errors');
  await browser.close();
  console.log(fails ? `\n${fails} FAILURE(S)` : `\nALL CHECKS PASSED (screenshots in outputs/screens/)`);
  process.exit(fails ? 1 : 0);
})();
