const fs = require('fs');

const cards = JSON.parse(fs.readFileSync('cards_m56.json', 'utf8'));
const diagrams = JSON.parse(fs.readFileSync('diagrams_m56.json', 'utf8'));
let errors = [];

// id uniqueness within each type
const byType = {};
cards.forEach(c => { byType[c.type] = byType[c.type] || []; byType[c.type].push(c); });
for (const t of Object.keys(byType)) {
  const ids = byType[t].map(c => c.id);
  const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dupes.length) errors.push(`${t}: duplicate ids ${dupes}`);
}

// leak scan across the whole file (word-boundary match so legitimate prose
// like "...becomes undefined" doesn't false-positive)
const raw = JSON.stringify(cards);
for (const bad of [/"undefined"/, / NaN\b/, ':null[,}]', '${']) {
  const re = bad instanceof RegExp ? bad : new RegExp(bad.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (re.test(raw)) errors.push(`Leak scan: found ${bad} somewhere in the file`);
}

cards.forEach(c => {
  const tag = `${c.type}#${c.id}`;

  // diagram field validity
  if (c.diagram !== undefined && !diagrams[c.diagram]) {
    errors.push(`${tag}: diagram key "${c.diagram}" not found in diagrams.json`);
  }

  if (c.type === 'combo') {
    for (const f of ['title', 'stem', 'box', 'statements', 'choices', 'answerIndex', 'points']) {
      if (c[f] === undefined) errors.push(`${tag}: missing field ${f}`);
    }
    if (!Array.isArray(c.statements) || c.statements.length < 2) errors.push(`${tag}: statements should be an array of 2+`);
    (c.statements || []).forEach((s, i) => {
      for (const f of ['label', 'text', 'correct', 'explanation']) {
        if (s[f] === undefined) errors.push(`${tag}: statement[${i}] missing ${f}`);
      }
    });
    if (Array.isArray(c.choices) && c.answerIndex !== undefined) {
      if (c.answerIndex < 0 || c.answerIndex >= c.choices.length) errors.push(`${tag}: answerIndex out of range`);
      else {
        // the choice string at answerIndex should exactly match the set of correct labels, comma-joined
        const correctLabels = (c.statements || []).filter(s => s.correct).map(s => s.label);
        const expected = correctLabels.join(', ');
        const actual = c.choices[c.answerIndex];
        if (actual !== expected) errors.push(`${tag}: answerIndex choice "${actual}" doesn't match correct-statement set "${expected}"`);
      }
      // choices should be unique
      const cset = new Set(c.choices);
      if (cset.size !== c.choices.length) errors.push(`${tag}: duplicate entries in choices`);
    }
    // box should contain literal HTML (that's the established convention for combo)
    if (typeof c.box === 'string' && !/<b>|<br/.test(c.box)) {
      // not an error, just structurally unusual -- combo boxes in this deck always use (가)/(나) bolded labels
      if (!/\(가\)|\(나\)/.test(c.box)) errors.push(`${tag}: box has no (가)/(나) markers or HTML formatting -- check by hand`);
    }
  }

  else if (c.type === 'match') {
    for (const f of ['title', 'prompt', 'leftLabel', 'rightLabel', 'pairs', 'points']) {
      if (c[f] === undefined) errors.push(`${tag}: missing field ${f}`);
    }
    if (!Array.isArray(c.pairs) || c.pairs.length < 3) errors.push(`${tag}: pairs should be an array of 3+`);
    // NOTE: some match cards are intentional category-sorts (many lefts -> few
    // repeated right-hand category labels, e.g. "EMS"/"Non-EMS"), so repeated
    // rights are only suspicious when almost every pair is unique already and
    // just one or two happen to collide (an accidental copy/paste duplicate).
    const rights = (c.pairs || []).map(p => p.right);
    const distinctRights = new Set(rights).size;
    const isCategorySort = distinctRights <= Math.ceil(rights.length / 2);
    if (!isCategorySort && distinctRights !== rights.length) {
      errors.push(`${tag}: duplicate 'right' values among pairs (breaks matching uniqueness) -- rights: ${JSON.stringify(rights)}`);
    }
    (c.pairs || []).forEach((p, i) => {
      if (!p.left || !p.right) errors.push(`${tag}: pair[${i}] missing left/right`);
    });
  }

  else if (c.type === 'tf') {
    for (const f of ['box', 'claim', 'answer', 'explanation', 'points']) {
      if (c[f] === undefined) errors.push(`${tag}: missing field ${f}`);
    }
    if (typeof c.answer !== 'boolean') errors.push(`${tag}: answer is not boolean`);
    if (typeof c.box === 'string' && /<b>|<br/.test(c.box)) errors.push(`${tag}: tf box contains raw HTML tags (should be plain text)`);
    if (typeof c.claim === 'string' && /<b>|<br/.test(c.claim)) errors.push(`${tag}: tf claim contains raw HTML tags (should be plain text)`);
  }

  else if (c.type === 'mc') {
    for (const f of ['stem', 'options', 'answerIndex', 'explanation', 'points']) {
      if (c[f] === undefined) errors.push(`${tag}: missing field ${f}`);
    }
    if (!Array.isArray(c.options) || c.options.length < 4) errors.push(`${tag}: options should be an array of 4+`);
    if (c.answerIndex < 0 || c.answerIndex >= (c.options || []).length) errors.push(`${tag}: answerIndex out of range`);
    const oset = new Set(c.options);
    if (c.options && oset.size !== c.options.length) errors.push(`${tag}: duplicate options`);
  }

  else {
    errors.push(`${tag}: unknown type "${c.type}"`);
  }
});

console.log('Total cards checked:', cards.length);
if (errors.length) {
  console.log(`\n${errors.length} ISSUE(S) FOUND:`);
  errors.forEach(e => console.log(' -', e));
  process.exit(1);
} else {
  console.log('ALL CLEAR — no structural issues found.');
}

// extra checks for the Modules 5-6 set: ids globally unique (the web artifact keys
// progress by id alone) and disjoint from the Modules 1-2 ids
const old = ['cards_m12.json', 'cards_m34.json'].flatMap(f => JSON.parse(fs.readFileSync(f, 'utf8')));
const allIds = [...old, ...cards].map(c => c.id);
const dup = allIds.filter((x, i) => allIds.indexOf(x) !== i);
console.log(dup.length ? `GLOBAL ID CLASH: ${dup}` : 'ids globally unique across Modules 1-6 (' + allIds.length + ')');
// statement labels, choice sets, stray whitespace / entities
let lint = [];
for (const c of cards) {
  const s = JSON.stringify(c);
  if (/  /.test(s)) lint.push(`${c.type}#${c.id}: double space`);
  if (/&amp;|&lt;|&gt;|&#/.test(s)) lint.push(`${c.type}#${c.id}: HTML entity`);
  if (/[“”‘’]/.test(s)) lint.push(`${c.type}#${c.id}: curly quote`);
  if (c.type === 'combo' && c.statements.map(x => x.label).join('') !== 'ㄱㄴㄷ') lint.push(`${c.type}#${c.id}: labels`);
  if (c.type === 'combo' && c.choices.length !== 5) lint.push(`${c.type}#${c.id}: choices != 5`);
  if (c.type === 'mc' && c.options.length !== 5) lint.push(`${c.type}#${c.id}: options != 5`);
}
console.log(lint.length ? lint.join('\n') : 'lint clean');
