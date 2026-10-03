// Build the study page (all modules) from flashcards_template.html.
// Usage: node build_html.js   ->  biol130-flashcards.html, cards_all.json, diagrams_all.json
// Add a new set by appending its files to the two lists below.
const fs = require('fs');

const CARD_FILES = ['cards_m12.json', 'cards_m34.json', 'cards_m56.json'];
const DIAGRAM_FILES = ['diagrams_m12.json', 'diagrams_m34.json', 'diagrams_m56.json'];

const cards = CARD_FILES.flatMap(f => JSON.parse(fs.readFileSync(f, 'utf8')));
const diagrams = {};
for (const f of DIAGRAM_FILES) {
  const part = JSON.parse(fs.readFileSync(f, 'utf8'));
  const clash = Object.keys(part).filter(k => k in diagrams);
  if (clash.length) { console.error(`diagram key clash in ${f}:`, clash); process.exit(1); }
  Object.assign(diagrams, part);
}
// the page keys saved progress by card id alone, so ids must be unique across every set
const ids = cards.map(c => c.id);
const dupIds = [...new Set(ids.filter((x, i) => ids.indexOf(x) !== i))];
if (dupIds.length) { console.error('duplicate ids:', dupIds); process.exit(1); }
const missing = cards.filter(c => c.diagram && !diagrams[c.diagram]);
if (missing.length) { console.error('cards with unknown diagrams:', missing.map(c => c.id)); process.exit(1); }

const mods = [...new Set(cards.map(c => c.mod).filter(m => m > 0))].sort((a, b) => a - b);
const range = `${mods[0]}–${mods[mods.length - 1]}`;  // e.g. "1–6"

fs.writeFileSync('cards_all.json', JSON.stringify(cards, null, 1));
fs.writeFileSync('diagrams_all.json', JSON.stringify(diagrams, null, 1));

const template = fs.readFileSync('flashcards_template.html', 'utf8');
function injectOnce(html, placeholder, value) {
  const n = html.split(placeholder).length - 1;
  if (n !== 1) { console.error(`expected 1 ${placeholder}, found ${n}`); process.exit(1); }
  return html.replace(placeholder, () => value.replace(/<\/script/gi, '<\\/script'));
}
let out = injectOnce(template, '__CARDS_JSON__', JSON.stringify(cards));
out = injectOnce(out, '__DIAGRAMS_JSON__', JSON.stringify(diagrams));
out = out.split('__MOD_RANGE__').join(range);
fs.writeFileSync('biol130-flashcards.html', out);

const by = (f) => cards.reduce((a, c) => (a[f(c)] = (a[f(c)] || 0) + 1, a), {});
console.log(`Wrote biol130-flashcards.html (Modules ${range}), ${(out.length / 1024).toFixed(0)} KB`);
console.log('cards:', cards.length, 'by module:', by(c => c.mod), 'by format:', by(c => c.type));
console.log('diagrams:', Object.keys(diagrams).length, '| cards with a diagram:', cards.filter(c => c.diagram).length);
