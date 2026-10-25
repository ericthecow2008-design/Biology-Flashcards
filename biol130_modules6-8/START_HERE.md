# START HERE: BIOL 130 flashcards for Modules 6–8 (about 230 cards)

You are making flashcards for Eric, a first-year Health student at the University of Waterloo taking BIOL 130 (Introductory Cell Biology, Dr. Vivian Dayeh, Fall 2026). He studies with Anki and a web study page. He already has cards for Modules 1–6 and liked the Modules 1–5 case-study cards best. He now wants a few hundred cards for Modules 6–8.

**Deliverables:**

1. **An Anki deck,** `outputs/BIOL130_Modules6-8.apkg`, holding the deck "BIOL 130::Modules 6-8".
2. **The cards added to his study page,** https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm. Update it in place; never make a new page.
3. **A Project doc,** `outputs/biol130_modules6-8_flashcards.md`.

Eric isn't watching while you work, so don't stop to ask him questions. Where something is unclear, take the most reasonable reading and mention it in your final report. Quality beats speed. Every card must be scientifically correct, analytical rather than recall, and free of answer cues. Each diagram must be accurate and must not give away an answer. All commands run from this folder, the one that holds this file.

## The set

| Part | Your files | Cards | Mix |
|---|---|---|---|
| Module 6 case studies | `work/cards_m6.py`, `work/diagrams_m6.py` | 5 | 5 case-study 보기 cards. Module 6 already has 46 regular cards on the study page. Add up to 10 more cards only for concepts those cards miss (check `ref/existing_cards_index.txt`). |
| Module 7 (Cellular Respiration), full set | `work/cards_m7.py`, `work/diagrams_m7.py` | ~100 | ~20 보기 (5 of them case studies), ~8 matching, ~45 true/false, ~27 multiple choice |
| Module 8 (Photosynthesis), full set | `work/cards_m8.py`, `work/diagrams_m8.py` | ~75 | ~15 보기 (5 of them case studies), ~6 matching, ~33 true/false, ~21 multiple choice |
| Bridge | `work/cards_bridge.py`, `work/diagrams_bridge.py` | ~40 | All four formats, topic "Connecting Modules 1–8" |

That comes to about 220–230 cards. If Eric's message asks for a different number, scale each part to match.

What "full set" means, from the style guide:
- **Coverage.** Every concept in the Module 7 and 8 notes is genuinely tested by at least 2 cards.
- **Diagrams.** About a third of cards have a diagram. One diagram can serve several cards, so plan roughly 25–35 diagrams for Modules 7–8, plus one for each case study.
- **Real situations.** Use real-world scenarios wherever the biology allows.
- **Case-study cards** follow `docs/CASE_STUDY_EXAMPLES.md`. Mark them with `case(...)` and they appear under the study page's "Case studies" filter.
- **Bridge cards** each genuinely need concepts from two or more modules. At least half of them should connect Modules 6–8 back to Modules 1–5. Useful links include:
  - redox and electronegativity (Module 2);
  - NAD+ and FAD as nucleotides (Module 2);
  - proton pumps, gradients and membranes (Module 3);
  - mitochondria, chloroplasts and endosymbiosis (Modules 1 and 3);
  - enzymes as proteins (Module 5);
  - glycogen, starch and fats as fuels (Module 2);
  - mitochondrial DNA and ribosomes (Modules 4 and 5);
  - photosynthesis compared with respiration (Modules 6–8).

## Read these first

1. `STYLE_GUIDE.md`, all of it. It is Eric's standing brief: the four formats with examples, fairness rules, diagram rules, and writing conventions.
2. `docs/CASE_STUDY_EXAMPLES.md`, plus the four images in `docs/example_diagrams/` (open them with the Read tool). Case cards look exactly like these.
3. The notes, `notes/notes_modules6-8_pp85-120.txt`. Module 6 is pp. 85–94, Module 7 pp. 95–110 and Module 8 pp. 111–120. The text comes from a scanned handout, so it is messy. Whenever text is garbled, and for every figure or table you rely on, open the page image `notes/pages/p-NNN.jpg`. The notes are fill-in-the-blank: a line ending in "→" (or "￫") with nothing after it is a blank, which you fill from the textbook (Morris et al., *Biology: How Life Works*, 4th ed.) at intro level.

## What's in the kit

| Path | What it is |
|---|---|
| `STYLE_GUIDE.md` | Eric's style guide. Follow it. |
| `docs/CASE_STUDY_EXAMPLES.md`, `docs/example_diagrams/` | Worked examples of case-study cards |
| `REVIEWER_BRIEF.md` | The brief for the independent reviewers |
| `notes/` | Course notes for Modules 6–8, as text and page images |
| `ref/live_cards.json`, `ref/live_diagrams.json` | All 525 cards and 74 diagrams on the study page now. Use them to look things up; never edit them. |
| `ref/existing_cards_index.txt` | One line per existing card, for duplicate checks (use grep) |
| `ref/live_page.html` | The study page as of Oct 17, a fallback only (see Phase 4) |
| `ref/note_types.json`, `ref/BIOL130_Modules3-6.apkg` | Eric's Anki note types and his Modules 3–6 deck, for building and import tests |
| `tools/` | The build and check scripts (each one's header says what it does) |
| `selftest/` | Proves the tools work on this machine. Its files also show the card syntax for every format. |
| `work/` | Where you write your files |
| `outputs/` | Where the deliverables go |

## Setup (once)

```bash
pip install --break-system-packages -r requirements.txt   # genanki + anki (the real Anki importer, for tests)
node -e "require('playwright')" || npm install            # Playwright, for rendering and checks
node tools/find_chromium.js || npx playwright install chromium
bash selftest/selftest.sh                                 # must end: 12 passed, 0 failed
```

If a setup step fails, fix it before going on.

## Work in phases, and save as you go

This is a long job. Keep `work/PROGRESS.md` as a checklist of the phases below, and tick each item as it's finished. **Commit and push after every phase.** If your session stops (usage limits, timeouts), a new session reads `PROGRESS.md` and continues from the first unticked item. Do the phases in this order: card ids are assigned by module order, so earlier parts keep their ids as later parts are added.

### Phase 1: concept ledger → `work/concept_ledger_m68.json`

List every testable concept in the notes, with its page:

```json
{"module_6": {"slug": "p92: one-line meaning", "...": "..."},
 "module_7": {"...": "..."},
 "module_8": {"...": "..."},
 "earlier_modules": {"m3_proton_pump_gradient": "Module 3: cells pump protons with ATP, making a gradient"}}
```

- Slugs are lowercase with underscores. Expect roughly 25–45 per module.
- `earlier_modules` holds only the Module 1–5 concepts your bridge cards use.
- Every card's tags must come from this file, and `build_cards.py` checks that they do.

### Phase 2: plan → `work/PLAN.md`

1. **Topics.** For each part, make a table by topic: the concepts it covers and how many cards of each format. The topic names are fixed, and `build_cards.py` rejects any other:
   - **Module 6:** Energy & Metabolism · ATP & Energetic Coupling · Thermodynamics & Free Energy · Enzymes & Their Regulation
   - **Module 7:** Overview of Cellular Respiration · Glycolysis · Pyruvate Oxidation & Citric Acid Cycle · Oxidative Phosphorylation · Anaerobic Conditions & Fermentation · Metabolic Integration
   - **Module 8:** Overview of Photosynthesis · Pigments & Light Absorption · Photosystems & Electron Transport · Calvin Cycle
   - **Bridge:** Connecting Modules 1–8
2. **Case studies.** List all 15: the real case, (가) and (나), and the three statements (trap / explanation / what-if, with which are true).
3. **Diagrams.** List every diagram with its key, title, what to draw, a **Must not show** list, and which cards use it.
4. **New, not repeated.** Don't reuse a scenario the style guide lists as used, and grep `ref/existing_cards_index.txt` for every case and key term. Module 6's existing cards use, among others: the instant cold pack, firefly light, aspirin, methanol and ethanol, isoleucine feedback inhibition, hexokinase induced fit, carbonic anhydrase, the sprinter's ATP, chlorophyll fluorescence and deep-sea vent bacteria. A new card may test a concept again, but never with the same statement in new words.

Case ideas to check, not to use blindly:
- a fluoride rinse slowing mouth bacteria's glycolysis (enolase);
- FDG-PET scans (a glucose look-alike trapped after its first glycolysis step);
- thiamine deficiency in heavy drinkers (pyruvate oxidation);
- the DNP "diet pill" or brown fat (a leaky proton gradient makes heat instead of ATP);
- carbon monoxide or rotenone blocking the electron transport chain;
- yeast in bread dough versus muscle in a sprint (two fermentations);
- a keto diet (fats entering as acetyl-CoA);
- herbicides that block photosystem II;
- autumn leaf colours (pigments);
- red and blue LED grow lights (absorption);
- greenhouse CO2 enrichment (carboxylation);
- Calvin's 14C-labelled algae.

### Phase 3: the four parts, one at a time (Module 6 case studies → Module 7 → Module 8 → bridge)

For each part:

**a. Diagrams.** Write `work/diagrams_<part>.py` with `tools/svgkit.py`; its docstring shows the pattern. Each file ends with `ALL = {key: function}`, and each function returns `(title, svg)`. Then run:

```bash
python3 tools/build_diagrams.py                      # every part so far -> work/diagrams_m68.json; must report 0 issues
node tools/check_overlaps.js                         # must say: unmasked collisions: 0
FONT='"DejaVu Sans"' node tools/check_overlaps.js    # same, in a second font
node tools/shoot_gallery.js                          # work/gallery/<key>__light.png and __dark.png
```

**Open every new PNG in both themes** and fix what you see. While a part is half-done, `python3 tools/build_diagrams.py --only m7` checks just that part.

The diagram rules are in the style guide. In short:
- palette colours only;
- every label has a fill;
- width at most 640, font size at least 8.5;
- labels never overlap or sit on a line (use `label_box` to mask a line);
- show structure, data and labels only, never an answer, the rule being tested, or a verdict;
- the aria-label describes the picture in one or two sentences.

**b. Cards.** Write `work/cards_<part>.py` with `tools/cardkit.py`. Its docstring shows every format, and `selftest/cards_m7.py` has working examples. Then run `python3 tools/build_cards.py`. Use `--only m7` for a quick check of one part.

- Write 보기 statements in any order and just mark which are true. The builder balances answer patterns and spreads keys over ①–⑤. Across the set, aim for about 1 in 4 보기 cards with one true statement, 3 in 5 with two and 1 in 7 with all three; the builder warns if all-true cards crowd ⑤.
- For multiple choice, give the key and four distractors and the builder places the key. Use `ordered=True` for numeric options that belong in ascending order.
- Fix every ERROR. Fix every WARNING about cues and balance.
- Coverage warnings for a module matter once its part is finished.
- Look at the "possible near-duplicates" list and fix real repeats.

Every label, number and step a statement mentions must appear in its diagram exactly.

**c. Review.** Run:

```bash
python3 tools/make_review.py                         # work/review/cards_<part>.md (and _a/_b halves for big parts), diagrams.md
```

If you reused study-page diagrams, shoot them first with `DIAGRAMS=ref/live_diagrams.json KEYS=a,b node tools/shoot_gallery.js`.

- Start **two reviewer subagents** that didn't write the cards. Give each the whole of `REVIEWER_BRIEF.md` and this part's packet.
- For a part over 60 cards (Module 7, Module 8), use its two half-packets instead, e.g. `cards_mod7_a.md` and `cards_mod7_b.md`: two reviewers per half, four in all.
- If you can't start subagents, do two separate, deliberate passes yourself, card by card.
- Fix every MAJOR and every reasonable MINOR, rebuild, and re-review the changed cards until a round finds nothing major.

**d. Save.** Tick the part in `PROGRESS.md`, then commit and push.

### Phase 4: the whole set, the deliverables, and delivery

1. **Final checks.** Run `python3 tools/build_cards.py` on everything. Coverage must show every Module 7 and 8 concept tested by 2 or more cards. There must be no WARNING, and the format mix must be close to the table above. Check the near-duplicate list once more across parts.
2. **The deck:** `python3 tools/build_apkg.py && python3 tools/verify_apkg.py`. This writes `outputs/BIOL130_Modules6-8.apkg` and must end ALL CHECKS PASSED.
3. **The study page.**
   1. Read the live page with the Artifact tool: action `read` on https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm. It saves the full HTML to a file and tells you the path.
   2. Run the following, then look at the screenshots in `outputs/screens/`, light and dark:

      ```bash
      python3 tools/update_page.py <that saved file>     # outputs/biol130-flashcards.html
      node tools/page_test.js                            # must end ALL CHECKS PASSED
      ```

   3. Only if you have no Artifact tool, or the read fails, use `ref/live_page.html` (the page as of Oct 17) instead, and say so in your report.
   4. Publish `outputs/biol130-flashcards.html` to the same URL: Artifact tool, publish with `url` = the page link. If the publish is refused because the page changed, read it again, rerun `update_page.py` and `page_test.js`, and publish again. If you republish after fixing cards that are already up, add `--replace` to `update_page.py`. If you have no Artifact tool, leave the file in `outputs/` and tell Eric it still needs publishing.
4. **The doc:** `python3 tools/build_md.py` writes `outputs/biol130_modules6-8_flashcards.md`. If you have the Projects tool, save it to `claude/biol-130-modules-6-8-flashcards.md` in his "BIOL 130" Project. Otherwise leave it in `outputs/` and tell Eric.
5. **Commit and push** `outputs/` and `work/`.
6. **Final message to Eric.** Keep it short and plain:
   - what you made: card counts per part and format, plus one line on the case studies;
   - where to download the deck: the branch and path, e.g. "on GitHub, open `outputs/BIOL130_Modules6-8.apkg` on branch X and click Download raw file";
   - how to import it. It's a new deck, "BIOL 130::Modules 6-8", and importing it doesn't change his other decks;
   - that the study page now has Modules 7 and 8, with the case studies under **Case studies**;
   - whether the Project doc was saved;
   - anything you couldn't do.

## Done means

- [ ] All four parts written and reviewed, with no MAJOR issue left
- [ ] every Module 7 and 8 concept tested by 2+ cards; format mix near the table; `build_cards.py` prints no ERROR or WARNING
- [ ] `build_diagrams.py` passes with 0 issues; `check_overlaps.js` reports 0 unmasked collisions in both fonts; every gallery image checked in light and dark
- [ ] `verify_apkg.py` and `page_test.js` both pass, and the screenshots look right
- [ ] study page published to the same URL (or the reason it isn't)
- [ ] Project doc saved (or left in `outputs/` with a note)
- [ ] everything committed and pushed, and the final message sent
