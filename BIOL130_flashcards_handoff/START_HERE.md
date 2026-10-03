# Start here: finish my BIOL 130 Modules 5–6 flashcards

Hi, I'm Eric. A previous Claude session built my BIOL 130 flashcards for Modules 1–4 and drafted Modules 5–6, then ran out of usage partway through reviewing them. Everything it made is in this folder.

If you're a Claude Code cloud session working in my GitHub repository, also read `CLAUDE.md`. It covers setup and how to hand the finished files back.

Please finish Modules 5–6 so they're indistinguishable from my earlier sets: same question style, same card formats, same look in Anki and on my study page.

**Read these first, in full:**
1. `STYLE_GUIDE.md`: how every card is written and built. Those rules are what make the cards feel like mine.
2. This file: where things stand and what's left.
3. About 20 cards from `cards_m34.json` (finished and reviewed) and 20 from `cards_m56.json` (the drafts), to calibrate tone and difficulty.

Work through the steps without stopping to ask me, unless something can't be undone. If you have to make a judgement call, make it and tell me at the end.

## What I want back

1. **The Anki deck "BIOL 130::Modules 3-6"**, as the file `BIOL130_Modules3-6.apkg`. It contains the 191 finished Modules 3–4 cards exactly as they are, plus the reviewed Modules 5–6 cards and the new bridge cards.
2. **My study page updated to Modules 1–6:** https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm. Read it, then republish the new `biol130-flashcards.html` to that same link. My progress is saved by card id, so it carries over. If you can't publish to that link, send me the HTML file instead; don't make a new page.
3. **My BIOL 130 Project doc**, if you can see the Project: replace `claude/biol-130-modules-3-4-flashcards.md` with `claude/biol-130-modules-3-6-flashcards.md`, which `build_md_m36.js` builds. If you can't see the Project, send me the .md file.
4. **A short final message:**
   - card counts;
   - what the review changed;
   - anything you weren't sure about;
   - the Anki import steps below.

In a GitHub repository, also put the deck, the HTML and the .md file in `deliverables/`, commit them and push your branch. That's how I'll download them.

## Where things stand

| Part | Status |
|---|---|
| Notes | Module 5 is pp. 68–84, "Protein Structure, Function and Synthesis". Module 6 is pp. 85–94, "Making Life Work": metabolism, ATP, thermodynamics, enzymes. The text of every module (1–6) is in `notes/`, and the PDF pages 68–94 are `notes/BIOL130_notes_pp68-94.pdf`, whose page 1 is p. 68. |
| Concept ledger | **Done.** `concept_ledger_m56.json`: 83 Module 5–6 concepts with page references, plus 27 links to Modules 1–4 for bridge cards. |
| Diagrams | **Done and checked.** 15 diagrams in `diagrams_m56_a.py`, `_b.py` and `_c.py`, built into `diagrams_m56.json`. The colour and overlap checks pass (overlaps in two fonts), and every diagram was looked at in light and dark mode. Rendered images are in `reference/gallery_m56/`. |
| Cards | **Drafted, not yet independently reviewed.** 140 cards in four source files: `cards_m5a.py`, `cards_m5b.py`, `cards_m6.py` and `cards_bridge56.py`. They're built into `cards_m56.json`. |
| Tools | **Tested end to end on these drafts.** The deck, study page and doc all build and pass their checks, including Anki's own import test. |

The 140 cards break down like this:
- **By module:** 67 for Module 5, 46 for Module 6 and 27 bridge cards ("Connecting Modules 1–6").
- **By format:** 26 combination, 11 matching, 66 true/false (32 true, 34 false) and 37 multiple choice.
- **Diagrams:** 47 cards use one.
- **Coverage:** every concept is tested at least twice. The bridge cards touch Module 1 six times, Module 2 thirteen times, Module 3 seven times and Module 4 five times.

Don't redo the steps marked done. Spend the effort on review.

## What's left, in order

**1. Independent review.** This is the step the last session was starting.
1. Run `python3 make_review_m56.py` to make the review packets in `review_m56/`.
2. Follow `REVIEWER_BRIEF.md`: two reviewers who didn't write the cards, one for Module 5 and one for Module 6 plus the bridge cards. They check every key and fact against the notes, look for answer cues and diagram giveaways, and flag tags that aren't really tested.
3. Before trusting any reviewer finding, check it against the notes yourself. Reviewers can be wrong too.

**2. Fix.**
1. Edit the card source files. `astpatch.py` changes a single argument of one card safely (usage is in its docstring).
2. Tag removals or additions, and dropping a diagram from a card, go in the `REVIEW` map at the top of `build_cards_m56.py`.
3. Rebuild with `python3 build_cards_m56.py && node validate_m56.js`. Both must pass. The build output must still show "under-tested: none"; if a fix drops a concept below two cards, write a new card for it.
4. Keep the balance figures the build prints roughly where they are:
   - mixed combination answers;
   - spread-out MC key positions;
   - MC key rarely the longest option;
   - TF about half true;
   - hedge and absolute words split across true and false.

**3. Re-review.** Review only the changed cards. Repeat until a round finds nothing major; Modules 3–4 needed three rounds.

**4. Diagram changes, if any.**
1. Edit `diagrams_m56_*.py`.
2. Run `python3 build_diagrams_m56.py diagrams_m56.json diagrams_m56_a diagrams_m56_b diagrams_m56_c`.
3. Run `DIAGRAMS=diagrams_m56.json python3 scan_fills.py`.
4. Run `DIAGRAMS=diagrams_m56.json node check_overlaps.js`, and again with `FONT="DejaVu Sans"` added.
5. Run `node shoot_gallery.js` and look at the images in light and dark mode.

**5. Build and verify.**
- Anki deck: `python3 build_apkg_m36.py && python3 verify_apkg_m36.py`. Every line must say OK, including the Anki-engine import tests.
- Study page: `node build_html.js && node smoke_test.js`, then look at the screenshots in `verify/`. The pills are captured mid-fade, so a pale pill there is not a bug.
- Project doc: `node build_md_m36.js`.

**6. Deliver** everything under "What I want back".

**Setup:**
1. Run `pip install -r requirements.txt` (add `--break-system-packages` if pip asks). This installs:
   - genanki, which builds the deck;
   - anki, used only for the import tests;
   - PyMuPDF, used only for `render_pages.py`.
2. Run `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install` for the browser checks.
3. Those checks find any Chromium already on the machine (`find_chromium.js`). If none is found, try `npx playwright install chromium`.
4. If no browser can run, still build and verify the deck and doc. Tell me which checks you skipped.

## Anki import steps (put these in your final message)

I already have "BIOL 130::Modules 3-4" in Anki, with my review history. Anki matches decks by name and never moves cards it already has, so:

1. In Anki, rename **BIOL 130::Modules 3-4** to **BIOL 130::Modules 3-6** (gear icon → Rename). If that deck still has its old name, "BIOL 130::Modules 3-4 (Suneung + Diagrams)", rename that one.
2. Import `BIOL130_Modules3-6.apkg`. Anki recognises the 191 cards I already have (no duplicates, progress kept), and the new cards join the same deck.

`verify_apkg_m36.py` tests exactly this sequence with Anki's own engine.

## Don't

- Don't change or rebuild the finished Modules 1–4 cards (`cards_m12.json`, `cards_m34.json`). If you find a real error in one, list it in your final message instead.
- Don't change the four Anki note types, the GUID scheme or any existing ids.
- Don't put "Suneung" or any other style label in deck or file names.
- Don't make a new study page instead of updating mine.

## File map

| Files | What they are |
|---|---|
| `cards_m12.json`, `diagrams_m12.json` | Modules 1–2: finished (169 cards). |
| `cards_m34.json`, `diagrams_m34.json` | Modules 3–4: finished (191 cards). |
| `cards_m5a.py`, `cards_m5b.py`, `cards_m6.py`, `cards_bridge56.py` | Modules 5–6 card sources. **Edit these.** |
| `concept_ledger_m56.json` | Concept slugs used in the card tags. |
| `diagrams_m56_a.py`, `_b.py`, `_c.py` | Modules 5–6 diagram sources. |
| `cards_m56.json`, `cards_m56_audit.json`, `diagrams_m56.json` | Built from the sources. Don't hand-edit. |
| `cardkit.py`, `svgkit.py`, `astpatch.py` | Card constructors, SVG helpers and the safe card editor. |
| `build_cards_m56.py`, `validate_m56.js`, `make_review_m56.py` | Build and balance the cards, validate them, and make the review packets. |
| `build_diagrams_m56.py`, `scan_fills.py`, `check_overlaps.js`, `shoot_gallery.js` | Assemble and check diagrams, and render them to images. |
| `build_apkg_m36.py`, `verify_apkg_m36.py`, `inspect_apkg.py` | Build and verify the Modules 3–6 Anki deck. |
| `flashcards_template.html`, `build_html.js`, `smoke_test.js` | Build and test the study page. Module 5 and 6 colours are already in the template. |
| `build_md_m36.js` | Build the Project doc. |
| `REVIEWER_BRIEF.md` | The brief for the independent reviewers. |
| `render_pages.py` | Render the notes pages to images (`pages/p-68.png` …). |
| `find_chromium.js` | Lets the browser checks use any Chromium already installed. |
| `CLAUDE.md`, `README.md`, `requirements.txt`, `package.json`, `.gitignore` | Repository setup for Claude Code cloud sessions. |
| `deliverables/` | Where the finished deck, study page and doc go. |
| `notes/` | Text of the notes for Modules 1–6, and PDF pages 68–94. |
| `reference/` | Kept for checks and comparison: my current Modules 3–4 deck (the verifier compares against it), the Modules 3–4 concept ledger, scenarios already used in Modules 1–4, and rendered Modules 5–6 diagrams. |
