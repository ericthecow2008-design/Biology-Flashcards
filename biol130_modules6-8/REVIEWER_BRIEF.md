# Reviewer brief: BIOL 130 flashcards, Modules 6–8

Paths are relative to the kit folder (the folder that holds START_HERE.md).

You are an independent expert reviewer (cell biology and biochemistry) checking flashcards for a first-year university course: University of Waterloo BIOL 130, Introductory Cell Biology. You did not write these cards. Be rigorous and skeptical: your job is to catch errors before a student studies from them.

## The set

The cards come in four Korean-Suneung-style formats:

- **보기 combination:** a stem, a box with (가)/(나) facts, three statements ㄱ/ㄴ/ㄷ (any number of them true), and five answer choices drawn from {ㄱ, ㄴ, ㄷ, ㄱ+ㄴ, ㄱ+ㄷ, ㄴ+ㄷ, ㄱ+ㄴ+ㄷ}.
  - Cards marked **CASE STUDY** are built around one real case and always have a diagram.
  - A case card should have a misconception trap, a statement explaining the case, and a "what if", and a statement should use each of (가) and (나).
- **Matching:** 4–7 pairs. Each right-hand item must fit exactly one left-hand item.
- **True/false:** a short scenario and one claim.
- **Multiple choice:** five options with exactly one defensible key.

Your packet is one of the files in `work/review/` (`cards_mod6.md`, `cards_mod7_a.md`, `cards_mod7_b.md`, `cards_mod8_a.md`, `cards_bridge.md` and so on); you'll be told which. Bridge cards ("Connecting Modules 1–8") must genuinely need concepts from two or more modules. Many link Modules 6–8 back to Modules 1–5.

The student studies from the course notes and the textbook (Morris et al., *Biology: How Life Works*, 4th ed.). The real-world case details (drug names, disease facts, numbers) go beyond the notes on purpose, so they must be correct by current scientific knowledge. Check them as carefully as the course content, from your own knowledge. If you are not sure a case fact is right, say so and suggest safer wording.

## Your materials

- **Cards:** your packet. It holds each card's question, key, explanation(s), the links line, and the concept tags it claims (with what each tag means). Review every card in it.
- **Notes:** `notes/notes_modules6-8_pp85-120.txt` (Module 6 is pp. 85–94, Module 7 pp. 95–110, Module 8 pp. 111–120). Page images are in `notes/pages/p-085.jpg` … `p-120.jpg`; open them whenever the text is garbled, and for figures and tables. For bridge cards, judge Module 1–5 content by standard intro-biology knowledge.
- The notes are fill-in-the-blank. A line ending in "→" (or "￫") with nothing after it is a blank the card author filled from the textbook. Judge that content by standard intro-biology textbook knowledge.
- **Diagrams:** `work/review/diagrams.md` has each diagram's description and every visible label. The image path is printed in each card's header. OPEN AND LOOK at the image (Read tool) before reviewing a card that uses it.
- **Earlier cards (on the study page already):** `ref/existing_cards_index.txt`, one line per card. Flag near-duplicates: the same case, or the same statement in different words.

The deck's design goals:
- questions are analytical and application-based, not phrase recognition;
- answers are concise but complete, and scientifically accurate;
- real-world scenarios are used where they fit.

## For every card, check

1. **KEY.**
   - **보기:** check each statement's TRUE/FALSE individually, and check that the key matches.
   - **True/false:** is the keyed answer right?
   - **Multiple choice:** is exactly one option defensible?
   - **Matching:** does every left item fit exactly one right item?
   - **All formats:** could a careful student reasonably argue another answer (ambiguity)?
2. **FACTS.** Is there any factual error, overstatement or misleading simplification anywhere on the card? Judge course content against the notes and textbook knowledge, and case details against current science. Do every calculation yourself: ATP, NADH and FADH2 tallies, carbon counts, ΔG signs, H+ gradients, wavelengths, ratios, molecule counts per turn of a cycle.
3. **DIAGRAM.** Does the card's text match what the diagram actually shows (labels, numbers, positions, panel names, step numbers)? Does the diagram, its title or its description give any answer away? Is the diagram scientifically accurate?
4. **CUES.** Does any wording reveal the answer? Look for:
   - a key or true statement noticeably longer, more specific or more qualified than the others;
   - hedges ("can", "may", "might") only on true items, or absolutes ("must", "only", "always", "never", "just as") only on false ones;
   - a false statement or distractor that the stem or box flatly contradicts;
   - one statement whose wording hands over another's answer;
   - grammatical mismatches between stem and options;
   - obviously silly distractors.
5. **TAGS.** Does the card genuinely require each concept tag it claims? List tags that should be dropped.
6. **QUALITY.** Is the card analytical rather than recall? Is the wording clear and concise? Is each explanation correct, concise and complete, saying why the key is right and, where a wrong answer is tempting, why it's wrong? For case-study cards, is the case actually used rather than decorative?
7. **DUPLICATES.** Look for near-duplicates within your packet and of the earlier cards.

Do NOT edit any files.

## Report (your final message)

One line per problem, in this format:

`#<id> · <MAJOR|MINOR|TAG> · <category> · <issue> · <suggested fix — give exact replacement wording where possible>`

- MAJOR: a wrong or ambiguous key, a factual error, or a diagram mismatch or giveaway.
- MINOR: wording, a weak distractor, an answer cue, or clarity.
- TAG: a concept tag that isn't genuinely tested (say which tag).

After the list, give counts per severity and the ids of the cards you checked that have no problems. No other commentary.
