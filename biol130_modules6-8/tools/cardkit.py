"""cardkit: the card constructors used in work/cards_*.py.

Each work/cards_*.py file builds a list called CARDS. The builder (tools/build_cards.py) reads every
such file, so you can keep one file per part: cards_m7.py, cards_m8.py, cards_case.py, cards_bridge.py.

    from cardkit import S, combo, case, tf, mc, match, box, with_mod, STEM_TAIL

    CARDS = with_mod(7, [
      # 보기 combination: three statements; write them in any order and mark which are true
      combo("Glycolysis", "A short title",
        "Read (가) and (나). Which statements in <보기> are correct?",
        box("first fact", "second fact"),
        [S("A statement.", True, "Why it is true, in one or two sentences."),
         S("A statement.", False, "Why it is false."),
         S("A statement.", True, "Why it is true.")],
        "Concept A · Concept B", ["slug_a", "slug_b"], points=3, diagram=None),

      # a case-study 보기 card: like combo, but built around one real case, always with a diagram;
      # shown under the study page's "Case studies" filter
      case("Glycolysis", "A short title", "The real case in one or two sentences." + STEM_TAIL,
        box("(가): a mechanism detail", "(나): a twist or an experiment"),
        [S(...), S(...), S(...)], "Concept A · Real-world: the case", ["slug_a"], points=3, diagram="key"),

      # true/false: an optional scenario box, one claim
      tf("Glycolysis", "The claim to judge.", False, "Why it is false.", "Concept A", ["slug_a"],
         points=1, box="A short scenario (optional).", diagram=None),

      # multiple choice: the key and four distractors; the builder places the key so positions ①-⑤
      # are used evenly and shuffles the distractors. Pass ordered=True to keep YOUR order (e.g. numbers
      # in ascending order); then options = [all five in order] and key_index = the key's position.
      mc("Glycolysis", "The question?", "the key option",
         ["distractor 1", "distractor 2", "distractor 3", "distractor 4"],
         "Why the key is right and the most tempting distractor wrong.", "Concept A", ["slug_a"], points=2),

      # matching: 4-7 pairs; each right item fits exactly one left item. The page and the deck shuffle
      # the right column themselves, so list the pairs in their natural order.
      match("Glycolysis", "A short title", "Match each X to its Y.", "X", "Y",
            [("left 1", "right 1"), ("left 2", "right 2"), ("left 3", "right 3"), ("left 4", "right 4")],
            "One explanation for the whole set.", "Concept A", ["slug_a"], points=3),
    ])

Bridge cards (connecting modules) go in their own list with with_mod(0, [...]) and topic
"Connecting Modules 1–8".
"""

STEM_TAIL = " Using the diagram, which statements in <보기> are correct?"


def S(text, correct, explanation):
    """One 보기 statement: its text, whether it is true, and a one-to-two-sentence explanation."""
    assert isinstance(correct, bool), "the second argument of S() is True or False"
    return {"text": text, "correct": correct, "explanation": explanation}


def box(*parts):
    """The (가)/(나)/(다) box. Pass plain text; the bold labels are added here."""
    labels = ["(가)", "(나)", "(다)", "(라)"]
    assert 1 <= len(parts) <= 4
    return "<br><br>".join(f"<b>{labels[i]}</b> {p}" for i, p in enumerate(parts))


def _combo(topic, title, stem, box_html, statements, links, concepts, points, diagram, is_case):
    assert len(statements) == 3, f"{title}: a 보기 card has exactly three statements"
    assert 1 <= sum(s["correct"] for s in statements) <= 3, f"{title}: at least one statement must be true"
    assert points in (2, 3), f"{title}: 보기 cards are worth 2 or 3 points"
    return {"type": "combo", "case": is_case, "topic": topic, "title": title, "stem": stem, "box": box_html,
            "statements": statements, "links": links, "concepts": list(concepts), "points": points, "diagram": diagram}


def combo(topic, title, stem, box_html, statements, links, concepts, points=3, diagram=None):
    return _combo(topic, title, stem, box_html, statements, links, concepts, points, diagram, False)


def case(topic, title, stem, box_html, statements, links, concepts, points=3, diagram=None):
    assert diagram, f"{title}: every case-study card has a diagram"
    return _combo(topic, title, stem, box_html, statements, links, concepts, points, diagram, True)


def tf(topic, claim, answer, explanation, links, concepts, points=1, box=None, diagram=None):
    assert isinstance(answer, bool), "tf answer is True or False"
    assert points in (1, 2), "true/false cards are worth 1 or 2 points"
    return {"type": "tf", "topic": topic, "claim": claim, "answer": answer, "explanation": explanation,
            "links": links, "concepts": list(concepts), "points": points, "box": box or "", "diagram": diagram}


def mc(topic, stem, key, distractors, explanation, links, concepts, points=1, diagram=None, ordered=False, key_index=None):
    """ordered=False: key + 4 distractors, placed by the builder. ordered=True: `distractors` is the full
    list of five options in display order and key_index says which one is right (`key` must equal it)."""
    assert points in (1, 2), "multiple-choice cards are worth 1 or 2 points"
    if ordered:
        assert len(distractors) == 5 and key_index is not None and distractors[key_index] == key, \
            "with ordered=True pass all five options and the key's index"
        options = list(distractors)
    else:
        assert len(distractors) == 4, "give exactly four distractors"
        assert key not in distractors
        options = [key] + list(distractors)
    return {"type": "mc", "topic": topic, "stem": stem, "key": key, "options": options, "ordered": ordered,
            "explanation": explanation, "links": links, "concepts": list(concepts), "points": points, "diagram": diagram}


def match(topic, title, prompt, left_label, right_label, pairs, explanation, links, concepts, points=3, diagram=None):
    assert 4 <= len(pairs) <= 7, f"{title}: matching cards have 4-7 pairs"
    assert points in (2, 3, 4), "matching cards are worth 2-4 points"
    return {"type": "match", "topic": topic, "title": title, "prompt": prompt, "leftLabel": left_label,
            "rightLabel": right_label, "pairs": [{"left": l, "right": r} for l, r in pairs],
            "explanation": explanation, "links": links, "concepts": list(concepts), "points": points, "diagram": diagram}


def with_mod(mod, cards):
    for c in cards:
        c["mod"] = mod
    return cards
