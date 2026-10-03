const fs = require('fs');

// Modules 3-6 in one doc (replaces the Modules 3-4 doc in the BIOL 130 Project)
const CARDS = ['cards_m34.json', 'cards_m56.json'].flatMap(f => JSON.parse(fs.readFileSync(f, 'utf8')));
const DIAGRAMS = Object.assign({}, ...['diagrams_m34.json', 'diagrams_m56.json'].map(f => JSON.parse(fs.readFileSync(f, 'utf8'))));
const ARTIFACT_URL = "https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm";

// Text stand-in for each figure (this doc is plain markdown, so figures are
// described rather than drawn -- a short "what it shows / what to sketch"
// line). Defaults to the SVG's own aria-label; the two whose aria-labels are
// too generic to answer a diagram question from get fuller descriptions that
// carry each panel's caption.
const DESC_OVERRIDE_M12 = {
  microscopy_comparison: "Three panels side by side: light microscopy shows only the whole-cell shape; fluorescence shows a dark field where one tagged structure glows; electron microscopy shows fine ultrastructure, but only in a fixed (non-living) sample",
  electronegativity_spectrum: "One continuum of electronegativity difference (ΔEN): from no ΔEN (equal sharing; nonpolar covalent, e.g. C–H), through polar covalent (e.g. O–H in water), to large ΔEN (full electron transfer; ionic, e.g. Na–Cl)",
};
const DESC_OVERRIDE = {};
function diagramLine(c) {
  if (!c.diagram) return null;
  const d = DIAGRAMS[c.diagram];
  if (!d) throw new Error(`card ${c.type}#${c.id}: unknown diagram ${c.diagram}`);
  let desc = DESC_OVERRIDE[c.diagram] || d.svg.match(/aria-label="([^"]+)"/)[1];
  desc = desc.replace(/\b5 prime\b/g, "5′").replace(/\b3 prime\b/g, "3′");
  return `**◇ Diagram — ${d.title}.** ${desc}.`;
}

const CIRCLED = ["①", "②", "③", "④", "⑤"];
const LETTERS = [..."ABCDEFGHIJKLMNOP"];

const TYPE_LABEL = { combo: "보기 Combination", match: "Matching", tf: "True / False", mc: "Multiple Choice" };

// box fields (combo only) contain a small amount of literal HTML: <b>, <br><br>, <br>.
// Convert that to markdown rather than emitting raw tags into the doc.
function boxToMd(box) {
  return box
    .replace(/<b>(.*?)<\/b>/g, "**$1**")
    .replace(/<br\s*\/?>\s*<br\s*\/?>/g, "\n\n")
    .replace(/<br\s*\/?>/g, "\n")
    .split("\n").map(l => l.trim()).filter(Boolean)
    .map(l => "> " + l).join("\n>\n");
}

// deterministic shuffle (independent of the Anki build's own shuffle -- each
// surface gets its own, there's no requirement they match)
function seededShuffle(arr, seed) {
  const a = arr.slice();
  let s = 0;
  for (let i = 0; i < seed.length; i++) s = (s * 31 + seed.charCodeAt(i)) >>> 0;
  function rnd() { s = (s * 1103515245 + 12345) >>> 0; return s / 4294967296; }
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const MOD_ORDER = [3, 4, 5, 6, 0];
const TOPIC_ORDER = {
  3: ["Membrane Structure & Fluidity", "Endomembrane System", "Mitochondria & Chloroplasts",
      "Passive Transport & Osmosis", "Active Transport", "Bulk Transport"],
  4: ["DNA: Evidence & Structure", "Gene Expression & RNA", "Transcription Mechanism", "RNA Processing: Prok vs Euk"],
  5: ["Amino Acids & Peptide Bonds", "Levels of Protein Structure", "Translation Machinery & Genetic Code",
      "Translation Stages: Prok vs Euk", "Regulation & Protein Sorting"],
  6: ["Energy & Metabolism", "ATP & Energetic Coupling", "Thermodynamics & Free Energy", "Enzymes & Their Regulation"],
  0: ["Connecting Modules 1–4", "Connecting Modules 1–6"],
};
const MOD_TITLE = {
  3: "Module 3 — Cells and Membranes",
  4: "Module 4 — Nucleic Acids and Information Flow",
  5: "Module 5 — Protein Structure, Function and Synthesis",
  6: "Module 6 — Making Life Work",
  0: "Connecting Modules 1–6 — Cross-Module Synthesis",
};

let qNum = 0;
const lines = [];

lines.push("# BIOL 130 — Modules 3–6 Flashcards");
lines.push("");
lines.push("*Dr. Vivian Dayeh · Introductory Cell Biology · Fall 2026 · University of Waterloo*");
lines.push("");
lines.push(
  "Suneung-style analytical questions in four selectable-answer formats — 보기 (bogi) combination, matching, " +
  "true/false, and multiple choice — built from the Module 3 (pp. 32–51), Module 4 (pp. 52–67), Module 5 (pp. 68–84) " +
  "and Module 6 (pp. 85–94) lecture notes. " +
  "Questions test reasoning, not recall: most put a concept to work in an experiment, a real-world case (drugs, " +
  "diseases, lab techniques), or a diagram, and the final section connects these modules with each other and with Modules 1–2. " +
  "Think through your answer before checking it against the key. " +
  `For the interactive, auto-graded version — now covering Modules 1–6, with the diagrams drawn in — use the [study page](${ARTIFACT_URL}); ` +
  "Modules 1–2 have their own doc in this Project. Items marked **◇ Diagram** show a figure in the interactive and " +
  "Anki versions; here, each figure is described in one line of text instead, so you can sketch it yourself."
);
lines.push("");

const counts = { combo: 0, match: 0, tf: 0, mc: 0 };
CARDS.forEach(c => counts[c.type]++);
lines.push(
  `**${CARDS.length} items total** — 보기 Combination: ${counts.combo} · Matching: ${counts.match} ` +
  `(${CARDS.filter(c => c.type === "match").reduce((s, c) => s + c.pairs.length, 0)} pairs) · ` +
  `True/False: ${counts.tf} · Multiple Choice: ${counts.mc} · ◇ ${CARDS.filter(c => c.diagram).length} items include a diagram`
);
lines.push("");
lines.push("---");
lines.push("");

for (const c of CARDS) {
  if (!TOPIC_ORDER[c.mod].includes(c.topic)) { console.warn("appending unlisted topic:", c.mod, c.topic); TOPIC_ORDER[c.mod].push(c.topic); }
}
for (const mod of MOD_ORDER) {
  lines.push(`## ${MOD_TITLE[mod]}`);
  lines.push("");
  for (const topic of TOPIC_ORDER[mod]) {
    const topicCards = CARDS.filter(c => c.mod === mod && c.topic === topic).sort((a, b) => a.id - b.id);
    if (topicCards.length === 0) continue;
    lines.push(`### ${topic}`);
    lines.push("");
    for (const c of topicCards) {
      qNum++;
      const badge = `[${TYPE_LABEL[c.type]}${c.points ? " · " + c.points + "점" : ""}]`;

      if (c.type === "combo") {
        lines.push(`**Q${qNum}. ${badge} ${c.title}**`);
        lines.push("");
        lines.push(c.stem);
        lines.push("");
        if (diagramLine(c)) { lines.push(diagramLine(c)); lines.push(""); }
        lines.push(boxToMd(c.box));
        lines.push("");
        lines.push("**<보기>**");
        c.statements.forEach(s => lines.push(`- ${s.label}. ${s.text}`));
        lines.push("");
        lines.push(c.choices.map((ch, i) => `${CIRCLED[i]} ${ch}`).join("　 "));
        lines.push("");
        lines.push(`**Answer: ${CIRCLED[c.answerIndex]} ${c.choices[c.answerIndex]}**`);
        c.statements.forEach(s => lines.push(`- ${s.label} — **${s.correct ? "O" : "X"}** — ${s.explanation}`));
        if (c.links) lines.push("", `*Concepts linked:* ${c.links}`);

      } else if (c.type === "match") {
        lines.push(`**Q${qNum}. ${badge}${c.title ? " " + c.title : ""}**`);
        lines.push("");
        lines.push(c.prompt);
        lines.push("");
        if (diagramLine(c)) { lines.push(diagramLine(c)); lines.push(""); }
        const n = c.pairs.length;
        const order = seededShuffle([...Array(n).keys()], `md-match-${c.id}`);
        lines.push(`**${c.leftLabel || "Items"}**`);
        c.pairs.forEach((pr, i) => lines.push(`${LETTERS[i]}. ${pr.left}`));
        lines.push("");
        lines.push(`**${c.rightLabel || "Match"}**`);
        order.forEach((origIdx, k) => lines.push(`${k + 1}. ${c.pairs[origIdx].right}`));
        lines.push("");
        lines.push("**Correct matches:**");
        c.pairs.forEach((pr, i) => lines.push(`- ${LETTERS[i]} = ${pr.left} → ${pr.right}`));
        if (c.explanation) lines.push("", c.explanation);
        if (c.links) lines.push("", `*Concepts linked:* ${c.links}`);

      } else if (c.type === "tf") {
        lines.push(`**Q${qNum}. ${badge}**`);
        lines.push("");
        if (c.box) { lines.push(`> ${c.box}`); lines.push(""); }
        if (diagramLine(c)) { lines.push(diagramLine(c)); lines.push(""); }
        lines.push(`**Claim:** ${c.claim}`);
        lines.push("");
        lines.push(`**Answer: ${c.answer ? "True" : "False"}**`);
        lines.push("");
        lines.push(c.explanation);
        if (c.links) lines.push("", `*Concepts linked:* ${c.links}`);

      } else if (c.type === "mc") {
        lines.push(`**Q${qNum}. ${badge}**`);
        lines.push("");
        lines.push(c.stem);
        lines.push("");
        if (diagramLine(c)) { lines.push(diagramLine(c)); lines.push(""); }
        lines.push(c.options.map((opt, i) => `${CIRCLED[i]} ${opt}`).join("　 "));
        lines.push("");
        lines.push(`**Answer: ${CIRCLED[c.answerIndex]} ${c.options[c.answerIndex]}**`);
        lines.push("");
        lines.push(c.explanation);
        if (c.links) lines.push("", `*Concepts linked:* ${c.links}`);
      }

      lines.push("");
      lines.push("---");
      lines.push("");
    }
  }
}

const md = lines.join("\n").replace(/\n{3,}/g, "\n\n");
if (qNum !== CARDS.length) { console.error(`ERROR: emitted ${qNum} questions but dataset has ${CARDS.length}`); process.exit(1); }
fs.writeFileSync("biol130_modules3-6.md", md);
console.log(`Wrote biol130_modules3-6.md — ${qNum} questions, ${md.length} chars`);
