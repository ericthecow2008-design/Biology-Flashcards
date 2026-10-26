# BIOL 130 flashcards: style guide

This is how every card in my BIOL 130 series is written and built. It covers Modules 1–2 (169 cards), Modules 3–6 (331 cards), the Modules 1–5 case studies (25 cards), the Modules 6–8 set and every set after them. New cards should be indistinguishable from the old ones.

I'm Eric, a first-year Health student at the University of Waterloo. The course is BIOL 130, Introductory Cell Biology, taught by Dr. Vivian Dayeh in Fall 2026. I study with Anki and a web study page. My time is limited, so every card has to earn its place.

## What a good card does

- **It tests reasoning, not recognition.** Each card makes me use a concept:
  - predict what happens in an experiment or to a patient;
  - read data or a diagram;
  - compare two cases;
  - or find the flaw in a claim.

  Never ask "what is X called?". Never write a claim I could judge just by spotting a phrase from the notes.
- **It uses real situations** wherever the biology allows: drugs and poisons, diseases and mutations, vaccines, lab techniques, everyday life. Examples already used include:
  - cyanide stopping secondary transport;
  - chloramphenicol's side effects (it also hits mitochondrial ribosomes);
  - the wrong IV bag;
  - why oral rehydration solution contains sugar;
  - designing a vaccine mRNA;
  - sickle-cell disease;
  - chloroquine raising lysosomal pH.

  The Modules 1–5 case studies used: CJD from reused brain electrodes, HeLa cells, antifungal creams for athlete's foot, DAPI/phalloidin staining, the gut methanogen *M. smithii*, a salt-water conductivity demo, salivary amylase in the stomach, ancient DNA vs RNA, galactosemia, olestra, Tay-Sachs and enzyme replacement therapy, hemodialysis, insulin and GLUT4, omeprazole, TB surviving in macrophages, φX174's base composition, SMA and nusinersen, the dystrophin gene's size, E. coli's heat-shock σ32, the insulin gene in beta vs muscle cells, Shiga toxin, codon-optimized vaccine mRNA, cystic fibrosis nonsense mutations and read-through drugs, scurvy, and AGT mistargeting in primary hyperoxaluria.

  Don't reuse a scenario an earlier set already used.
- **It connects modules.** Cards within a module can lean on earlier modules where that's natural. For example, a protein-folding card might need Module 2's bond types.

  Every set also ends with a bridge section, topic "Connecting Modules 1–N", stored as `mod: 0` in the data. It's about 15–20% of the set. Each bridge card must genuinely need concepts from two or more modules, and Modules 1–2 must be included, not just the neighbouring modules.
- **It stays inside the lecture notes.** Dr. Dayeh's notes decide what is tested: her topics, terms, numbers and simplifications. The real-world framing can come from outside the notes, but the biology being tested can't. Case details from outside the notes (drug names, disease facts, numbers) must still be correct by current science.

  The notes are fill-in-the-blank handouts: a line ending in "→" with nothing after it is a blank. Fill blanks from the course textbook (Morris et al., *Biology: How Life Works*, 4th ed.) at intro level. Check the page images for figures and tables; don't trust the extracted text alone.
- **Its answers are concise but complete.** An explanation is one to three sentences. It says why the key is right and, when a wrong answer is tempting, why that one is wrong. No filler, and no restating the question.
- **Together, the cards cover everything.** Before writing, list every testable concept in the notes, with page references. This is the concept ledger. Every concept must be genuinely tested by at least two cards. A card's concept tags list only what it really tests.
- **It doesn't repeat an earlier card.** Search the earlier cards before writing. A new card can test a concept again, but not with the same statement in new words.

## The four formats (Korean Suneung style)

Points (점) mark difficulty, as on the Suneung: 1–2 for true/false and multiple choice, 2–3 for combination, and 2–4 for matching.

1. **보기 Combination.** The parts are:
   - a short title;
   - a stem;
   - a box with labelled panels (가), (나)… holding setups, data or definitions;
   - three statements ㄱ / ㄴ / ㄷ, each true or false with its own one-line explanation;
   - five answer choices, each a set of statements (ㄱ, ㄱ, ㄴ, and so on).

   The statements should make me reason from the box, not just recall.
2. **Matching.** Four to seven pairs (usually five) plus one explanation. Each right-hand item fits exactly one left-hand item, unless the card is a deliberate sort into categories.
3. **True/False.** An optional scenario box, one claim, the answer and an explanation. Aim for roughly half true and half false.
4. **Multiple choice.** A stem and five options with one key. The wrong options are real misconceptions, written to match the key in grammar and length.

Modules 3–4 is a good model for the mix in a two-module set:
- about 20% combination;
- 8% matching;
- 45% true/false;
- 27% multiple choice;
- about a quarter to a third of all cards with a diagram.

## Case-study 보기 cards (the kind I like most)

These are 보기 combination cards built around one real case, like the oral rehydration card below. The Modules 1–5 case studies (ids 3001–3025) are all in this style, and the study page's **Case studies** filter shows them. Each case card:

- starts from one real case (a disease, a drug, a lab result, an everyday observation) and keeps it at the centre. The statements are about that case, not general facts with a story attached;
- has a question-side diagram of the system involved. The diagram shows structure or data only, and the statements make me read it;
- has a two-part box, and a statement uses each part. Usually (가) gives a mechanism detail and (나) a twist or an experiment;
- has three statements of different kinds: a misconception trap, an explanation of the case using course concepts, and a what-if that changes one part of the system.

**Example: "Why oral rehydration solution contains sugar"** (Module 3, 3점, with a diagram of the intestinal cell's Na+/glucose symporter and basal Na+/K+ pump)

*Stem:* Cholera causes severe diarrhea, but the intestinal Na+/glucose symporter keeps working. Using the diagram, which statements in <보기> are correct?

*Box:*
- (가) Oral rehydration solution (ORS), water with both Na+ and glucose, has saved millions of cholera patients.
- (나) Plain water, or salt water without sugar, rehydrates cholera patients much less effectively.

*Statements:*
- ㄱ. The symporter hydrolyzes ATP to move glucose against its gradient.

  **X.** It is secondary active transport: Na+ flowing down its gradient drives glucose uphill. The ATP is spent by the basal Na+/K+ pump.
- ㄴ. ORS works because Na+ and glucose absorbed together through the symporter raise the solute concentration inside intestinal cells, and water follows by osmosis.

  **O.** Moving solute into the cells (and on into the blood) creates the osmotic pull that draws water out of the gut.
- ㄷ. If the basal Na+/K+ pumps stopped, glucose uptake from the gut would eventually fail even though the symporter itself uses no ATP.

  **O.** The pump keeps Na+ low inside the cell; without it the Na+ gradient runs down and the symporter loses its driving force.

*Key:* ㄴ, ㄷ.

## Fairness: no free points

- **Combination keys vary.** Different cards have one, two or all three statements true, and ㄱ isn't always the true one. Across a set, aim for the existing deck's mix: about 1 in 4 cards with one true statement, 3 in 5 with two and 1 in 7 with all three. ("ㄱ, ㄴ, ㄷ" can only be choice ⑤, so too many all-true cards crowd ⑤.) You just write the statements and mark which are true; the builder reorders them to balance the patterns and spreads the key's position evenly over ①–⑤.
- **No statement gives away another.** A true statement's wording mustn't hand over the answer to another statement on the same card. Likewise, no false statement should be one the stem or box flatly contradicts.
- **The MC key doesn't stand out.** It shouldn't be the longest, most hedged or most specific option. The builder spreads the key's position; you keep the options parallel.
- **Wording doesn't give the answer away.** In true/false claims and in 보기 statements alike, hedge words (can, could, may, likely) and absolute words (must, only, always, never, just as) appear in both true and false statements. Check this across the whole set: the case batch's first draft had "can/could" almost only on true statements and "must/just as" only on false ones. The true statement also shouldn't usually be the longest.
- **No cheap tricks.** No "all of the above" or "none of the above", no trick wording, and nothing a careful student could reasonably argue either way.
- **Question-side diagrams don't leak the answer.** They show structure, data and labels only. They never show:
  - the answer;
  - the rule being tested;
  - verdict labels such as "uphill" or "downhill";
  - arrows that trace the very route a statement asks about.

  If a diagram can't avoid giving the answer away, drop it from that card.

## Diagrams

Diagrams are real, drawn by hand as inline SVG: never image files, never "diagram goes here" placeholders. Use them where structure or data is the point: pathways, molecular structures, experimental setups, graphs, organelle layouts, energy profiles.

- Use the page's palette variables only, so the diagram works in light and dark mode: `--ink`, `--ink-soft`, `--ink-faint`, `--bg`, `--surface`, `--border`, `--accent`, `--bridge`, `--mod1`, `--mod2`, `--review`, `--visual`, `--good`.
- Give every `<text>` element an explicit fill. SVG's default is black, which disappears in dark mode.
- Keep each diagram at most 640 px wide (it scrolls sideways on a phone), with font size at least 8.5.
- Labels must not overlap (the checker tests this in two fonts). Use masks where lines cross.
- Give each diagram an `aria-label` and a short title; the title becomes its caption.
- `svgkit.py` has the drawing helpers. Look at every diagram in light and dark mode before using it.

## Writing conventions

- Write chemistry and strand ends in plain ASCII: 5', 3', H2O, Na+, NH3+, CO2, ATP. "→" is fine.
- The data has no HTML entities, no curly quotes and no double spaces.
- Combination boxes are written as `<b>(가)</b> text<br><br><b>(나)</b> text`. Every other field is plain text.
- Each card ends with a short `links` line: the concepts it connects, separated by " · ", plus "Real-world: …" when it uses a scenario.

## Examples (from the finished Modules 3–4 set)

**보기 Combination: "Designing a vaccine mRNA"** (Module 4, 3점)

*Stem:* mRNA vaccines deliver a lab-made mRNA encoding a viral protein into the cytoplasm of human cells, where it is translated. Which statements in <보기> are correct?

*Box:*
- (가) Manufacturers give the synthetic mRNA a 5' cap and a poly(A) tail.
- (나) The synthetic mRNA contains no introns.

*Statements:*
- ㄱ. The cap is needed so the cell's ribosomes recognize the mRNA and translate it.

  **O.** Without a cap, ribosomes would not recognize the mRNA; the cap also protects it from exonucleases.
- ㄴ. Leaving out introns makes sense because the mRNA goes straight to the cytoplasm, while splicing happens in the nucleus.

  **O.** Processing, including intron removal, happens in the nucleus before export, so an mRNA delivered to the cytoplasm must already be mature.
- ㄷ. The vaccine mRNA must be converted into DNA and enter the nucleus before any protein can be made.

  **X.** Ribosomes translate mRNA directly in the cytoplasm; nothing needs to be copied into DNA.

*Choices:* ① ㄴ ② ㄱ, ㄴ ③ ㄱ, ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ. *Key:* ②.

*Links:* 5' cap · Splicing happens in the nucleus · Real-world: mRNA vaccines

**True/False** (Module 3, 2점)

*Box:* Cyanide stops mitochondria from making ATP. In a poisoned cell, the Na+/K+ pumps slow, and the Na+ and K+ gradients across the plasma membrane gradually run down.

*Claim:* Secondary active transport in this cell would also decline, even though secondary transporters never use ATP themselves.

*Answer:* **True.** Secondary transporters run on ion gradients that primary (ATP-driven) pumps build. When ATP runs out, the gradients fade, and so does everything they drive.

**Multiple choice** (Module 3, 2점)

*Stem:* Chloramphenicol, an antibiotic that blocks bacterial ribosomes, can cause serious side effects (such as bone-marrow suppression) by also blocking protein synthesis inside one human organelle. Which organelle is it, and why is it vulnerable?

*Options:*
- Mitochondria: they descend from bacteria and keep bacteria-like ribosomes **(key)**
- Rough ER: its ribosomes are attached to a membrane, like some bacterial ones
- Nucleus: it holds the cell's DNA, which the drug stops cells from reading
- Golgi apparatus: it modifies newly made proteins, so it depends on ribosomes
- Lysosomes: their digestive enzymes are proteins that need constant replacement

*Explanation:* Mitochondria originated as endosymbiotic proteobacteria and keep their own DNA and ribosomes in the matrix, so a drug aimed at bacterial ribosomes can hit them too. Cytosolic and rough-ER ribosomes are the eukaryotic type.

**Matching: "If this organelle failed…"** (Module 3, 3점)

*Prompt:* Match each failing structure in an animal cell to its most direct consequence.

| Failing structure | Most direct consequence |
|---|---|
| Rough ER | Proteins destined for secretion or the plasma membrane are no longer made |
| Golgi apparatus | Proteins leave the ER but are not modified, given sugars, or sorted to their destinations |
| Lysosomes | Worn-out proteins, lipids and nucleic acids pile up undigested |
| Mitochondria | Far less ATP is made from the energy stored in sugars |
| Cytoskeleton | The cell loses the protein scaffold that gives it its structure |

## How each set is built and checked

1. Read the notes and page images, then write the concept ledger.
2. Draw the diagrams, run the fill and overlap checks, and look at each one in light and dark mode.
3. Write the cards as Python source using `cardkit.py`. The constructors are `combo`, `case` (a case-study 보기 card), `match`, `tf`, `mc` and `S` for a statement. Each card lists its concept tags.
4. Build the set. The build script:
   - assigns ids;
   - balances the keys, the key positions and the choices;
   - checks tags and diagram keys;
   - audits coverage.
5. **Independent review.** Someone who didn't write the cards (fresh subagents if possible) checks every card against the notes and against the earlier cards for repeats. Patch, rebuild and review again until a round finds nothing major. If reviewers can't be run (for example, when usage limits stop them), do each review yourself as a separate, deliberate pass, card by card.

   The first review round on Modules 3–4 caught real problems, so don't skip this step. It found:
   - an explanation that stated a false general rule;
   - a matching set where one item fit two answers;
   - a true/false claim that was missing a needed qualifier;
   - diagrams that printed the answer;
   - about 80 tags for concepts the cards didn't really test.

   Later rounds also fixed hedge words that predicted FALSE, and MC keys that were usually the longest option. The case-study review replaced statements that restated earlier cards and a diagram whose arrows traced the answer.
6. Build the Anki deck, the study page and the Project doc, and test each one.

## Outputs

**Anki deck.**
- Decks are named only by course and modules (or lecture), never with style labels. For example, the deck "BIOL 130::Modules 3-6" goes in the file `BIOL130_Modules3-6.apkg`, the Modules 1–5 case studies are "BIOL 130::Modules 1-5" in `BIOL130_Modules1-5.apkg`, and the Modules 6–8 set, case studies included, is "BIOL 130::Modules 6-8" in `BIOL130_Modules6-8.apkg`.
- Always reuse the four existing note types, with the same fields, templates and CSS. Their model ids are:
  - combination 3125599791;
  - matching 3840893743;
  - true/false 1392138497;
  - multiple choice 1294902607.

  Their names still say "Suneung"; leave them alone.
- Each note's GUID is `genanki.guid_for(f"biol130-card-v4-{type}-{id}")`.
- Card ids are unique across all sets, because the study page saves progress by id:
  - Modules 1–2 use 1–346;
  - Modules 3–4 use 1001–1350;
  - Modules 5–6 use 2001+ for combination, 2101+ for matching, 2201+ for true/false and 2301+ for multiple choice;
  - the Modules 1–5 case studies use 3001–3025;
  - the Modules 6–8 set uses 3101–3299 for combination (case studies included), 3301–3399 for matching, 3401–3699 for true/false and 3701–3999 for multiple choice;
  - the next set starts at 4001.

**Study page.** One page holds every module: https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm. Update it in place: read it, then republish to the same link. Never start a new page; my saved progress lives there. Build on the page's current data, not on local copies, because later sessions may have edited cards. Case-study cards carry `caseStudy: true`, which puts them under the **Case studies** filter.

**Project doc.** Each set also goes into my BIOL 130 Project as a markdown doc (`claude/biol-130-modules-…-flashcards.md`; the case studies are `claude/biol-130-modules-1-5-case-studies.md`; the Modules 6–8 set is `claude/biol-130-modules-6-8-flashcards.md`), with each diagram described in one line.

## Modules 6–8: names to reuse

The notes cover Module 6 "Making Life Work" (pp. 85–94), Module 7 "Cellular Respiration" (pp. 95–110) and Module 8 "Photosynthesis" (pp. 111–120). Cards use these topic names, so the study page's topic menu stays tidy and any later set for these modules can reuse them:

- **Module 6.** These are the topics its 46 regular cards already use: Energy & Metabolism · ATP & Energetic Coupling · Thermodynamics & Free Energy · Enzymes & Their Regulation.
- **Module 7:** Overview of Cellular Respiration · Glycolysis · Pyruvate Oxidation & Citric Acid Cycle · Oxidative Phosphorylation · Anaerobic Conditions & Fermentation · Metabolic Integration.
- **Module 8:** Overview of Photosynthesis · Pigments & Light Absorption · Photosystems & Electron Transport · Calvin Cycle.
- **Bridge:** Connecting Modules 1–8.

On the study page, Module 7 is crimson and Module 8 is brown. `tools/update_page.py` adds both modules the first time they get cards.
