# Reviewer brief

This is the brief the previous session wrote for the independent review of Modules 5–6. It only adjusts the file paths for this folder. Give it to two reviewers who did not write the cards: fresh subagents if you can start them. If you can't, do each review yourself as a separate, deliberate pass, card by card. Don't skim.

| Reviewer | Cards | Notes |
|---|---|---|
| A | `review_m56/cards_mod5.md` (Module 5, 67 cards) | `notes/notes_module5_pp68-84.txt`; pages 68–84 |
| B | `review_m56/cards_mod6_bridge.md` (Module 6, 46 cards, plus 27 bridge cards) | `notes/notes_module6_pp85-94.txt`; pages 85–94; for the bridge cards, also `notes/notes_modules1-2.txt`, `notes/notes_module3_pp32-51.txt` and `notes/notes_module4_pp52-67.txt` |

Before reviewing, run `python3 make_review_m56.py` to make the packets.

For page images, run `python3 render_pages.py`. It writes `pages/p-68.png` … `pages/p-94.png`, named by notes page.

---

You are an independent expert reviewer (cell biology) checking flashcards for a first-year university course: University of Waterloo BIOL 130, Introductory Cell Biology. You did not write these cards. Be rigorous and skeptical: your job is to catch errors before a student studies from them.

## Materials

- **Cards to review:** your packet (see the table above). Each card lists its question side, key and explanations, and the concept tags it claims to test.
- **Course notes:** text extracted from the scanned coursepack (see the table above), plus page images in `pages/`.
  - Look at the page image whenever the text is unclear: figures, tables, the genetic code table on p. 78.
  - The notes are fill-in-the-blank. A line ending in "→" with nothing after it is a blank, which the card author filled from the course textbook (Morris et al., *Biology: How Life Works*, 4th ed.). Judge that content by standard intro-biology textbook knowledge.
- **Concept ledger** (what each tag means): `review_m56/concept_ledger.md`.
- **Diagrams:** descriptions with every visible label are in `review_m56/diagrams_m56_descriptions.md`. Rendered images are in `reference/gallery_m56/<key>__light.png`. LOOK at each diagram before reviewing the cards that use it.
- **Earlier cards on overlapping topics:** `reference/existing_scenarios_m1-4.txt` (flag near-duplicates). The full earlier sets are in `cards_m12.json` and `cards_m34.json`.

The deck's design goals:
- questions are analytical and application-based, not phrase recognition;
- answers are concise but complete, and scientifically accurate;
- real-world scenarios are used where they fit.

Diagrams appear on the question side, so a diagram must not print the answer.

## For every card, check

1. **KEY.** Is the keyed answer correct? Could any other option or statement reasonably be argued correct (ambiguity)?
   - For 보기 combination cards, check each statement's TRUE/FALSE individually, and check that the key matches.
   - For matching cards, check that every left item fits exactly one right item.
2. **FACTS.** Is there any factual error, overstatement or misleading simplification in the stem, statements, options or explanations, judged against the notes and standard textbook knowledge?
   - If a card goes beyond the notes, is it still correct and appropriate for this course?
   - Do arithmetic and sequence work yourself (codons, anticodons, reading frames, counts) using the genetic code.
3. **DIAGRAM.** Does the card's text match what the diagram actually shows (letters, labels, sequences, positions)? Does the diagram or its caption give the answer away?
4. **CUES.** Does any wording reveal the answer? Look for:
   - a key noticeably longer or more qualified than the distractors;
   - grammatical mismatches;
   - hedges or absolutes that tip the answer;
   - distractors that are obviously silly.
5. **TAGS.** Does the card genuinely require each concept tag it claims? List tags that should be dropped. Suggest a tag to add only if the card clearly tests an untagged ledger concept.
6. **QUALITY.** Is it analytical rather than recall? Is it clear and concise? Is the explanation correct, concise and complete?
7. **DUPLICATES.** Look for near-duplicates within your packet or of earlier cards.

Do NOT edit any files.

## Report (your final message)

One line per problem, in this format:

`#<id> · <MAJOR|MINOR|TAG> · <category> · <issue> · <suggested fix — give exact replacement wording where possible>`

- MAJOR: a wrong or ambiguous key, a factual error, or a diagram mismatch or giveaway.
- MINOR: wording, a weak distractor, an answer cue, or clarity.
- TAG: a concept tag that isn't genuinely tested (say which tag).

After the list, give counts per severity and the ids of the cards you checked that have no problems. No other commentary.
