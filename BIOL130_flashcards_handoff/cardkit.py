"""Compact constructors for BIOL 130 cards (all sets use these).

Each constructor returns a raw dict; the build script (build_cards_m56.py)
assigns ids, relabels
combo statements to balance the answer patterns, places MC answers at
balanced positions, and strips the audit-only `concepts` field.
"""

LABELS = ["ㄱ", "ㄴ", "ㄷ"]


def S(text, correct, explanation):
    """One <보기> statement (label assigned later)."""
    return {"text": text, "correct": bool(correct), "explanation": explanation}


def combo(topic, title, stem, box, statements, links, concepts, points=3, diagram=None):
    assert len(statements) == 3 and any(s["correct"] for s in statements), title
    c = {"type": "combo", "topic": topic, "points": points, "title": title,
         "stem": stem, "box": box, "statements": statements, "links": links,
         "concepts": concepts}
    if diagram:
        c["diagram"] = diagram
    return c


def match(topic, title, prompt, left_label, right_label, pairs, explanation, links, concepts,
          points=3, diagram=None):
    c = {"type": "match", "topic": topic, "points": points, "title": title, "prompt": prompt,
         "leftLabel": left_label, "rightLabel": right_label,
         "pairs": [{"left": l, "right": r} for l, r in pairs],
         "explanation": explanation, "links": links, "concepts": concepts}
    if diagram:
        c["diagram"] = diagram
    return c


def tf(topic, box, claim, answer, explanation, links, concepts, points=1, diagram=None):
    c = {"type": "tf", "topic": topic, "points": points, "box": box, "claim": claim,
         "answer": bool(answer), "explanation": explanation, "links": links,
         "concepts": concepts}
    if diagram:
        c["diagram"] = diagram
    return c


def mc(topic, stem, correct, distractors, explanation, links, concepts, points=1, diagram=None):
    assert len(distractors) == 4, stem[:60]
    c = {"type": "mc", "topic": topic, "points": points, "stem": stem,
         "correct": correct, "distractors": distractors, "explanation": explanation,
         "links": links, "concepts": concepts}
    if diagram:
        c["diagram"] = diagram
    return c
