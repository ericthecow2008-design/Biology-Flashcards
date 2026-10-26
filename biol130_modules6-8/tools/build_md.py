"""Write the Project doc for the Modules 6-8 set: outputs/biol130_modules6-8_flashcards.md

Usage (from the kit folder):  python3 tools/build_md.py
Same layout as Eric's other BIOL 130 docs: grouped by module and topic, numbered questions in all four
formats with their keys and explanations, and each diagram described in one line (taken from its
aria-label) because the doc is plain markdown.
"""
import collections, hashlib, html, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *a: os.path.join(ROOT, *a)
ARTIFACT_URL = "https://claude.ai/artifact/6hd61Bm4Fyc2ZkqwWr6Ctm"
MOD_TITLE = {6: "Module 6 — Making Life Work", 7: "Module 7 — Cellular Respiration", 8: "Module 8 — Photosynthesis",
             0: "Connecting Modules 1–8 — Cross-Module Synthesis"}
MOD_ORDER = [6, 7, 8, 0]
CIRCLED = ["①", "②", "③", "④", "⑤"]
TYPE_LABEL = {"combo": "보기 Combination", "match": "Matching", "tf": "True / False", "mc": "Multiple Choice"}


def diagram_line(c, diagrams):
    if not c.get("diagram"):
        return []
    d = diagrams[c["diagram"]]
    desc = html.unescape(re.search(r'aria-label="([^"]+)"', d["svg"]).group(1))
    desc = re.sub(r"\b5 prime\b", "5′", re.sub(r"\b3 prime\b", "3′", desc)).rstrip(". ")
    return [f"**◇ Diagram — {d['title']}.** {desc}.", ""]


def box_lines(box):
    parts = [p.strip() for p in re.split(r"<br\s*/?>\s*<br\s*/?>", box) if p.strip()]
    out = []
    for i, p in enumerate(parts):
        out += ([">"] if i else []) + ["> " + re.sub(r"<b>(.*?)</b>", r"**\1**", p)]
    return out


def right_order(c):
    order = list(range(len(c["pairs"])))
    random.Random(int(hashlib.sha256(f"biol130-match-order-{c['id']}".encode()).hexdigest()[:12], 16)).shuffle(order)
    return order


def render(q, c, diagrams):
    t = c["type"]
    head = f"**Q{q}. [{TYPE_LABEL[t]} · {c['points']}점]" + (f" {c['title']}**" if c.get("title") else "**")
    L = [head, ""]
    if t == "combo":
        L += [c["stem"], ""] + diagram_line(c, diagrams) + box_lines(c["box"]) + ["", "**<보기>**"]
        L += [f"- {s['label']}. {s['text']}" for s in c["statements"]]
        L += ["", "　 ".join(f"{CIRCLED[i]} {x}" for i, x in enumerate(c["choices"])), "",
              f"**Answer: {CIRCLED[c['answerIndex']]} {c['choices'][c['answerIndex']]}**"]
        L += [f"- {s['label']} — **{'O' if s['correct'] else 'X'}** — {s['explanation']}" for s in c["statements"]]
    elif t == "tf":
        L += [f"> {c['box']}", ""] + diagram_line(c, diagrams)
        L += [f"**Claim:** {c['claim']}", "", f"**Answer: {'True' if c['answer'] else 'False'}**", "", c["explanation"]]
    elif t == "mc":
        L += [c["stem"], ""] + diagram_line(c, diagrams)
        L += ["　 ".join(f"{CIRCLED[i]} {o}" for i, o in enumerate(c["options"])), "",
              f"**Answer: {CIRCLED[c['answerIndex']]} {c['options'][c['answerIndex']]}**", "", c["explanation"]]
    else:
        letters = [chr(ord("A") + i) for i in range(len(c["pairs"]))]
        L += [c["prompt"], ""] + diagram_line(c, diagrams)
        L += [f"**{c['leftLabel']}**"] + [f"{letters[i]}. {p['left']}" for i, p in enumerate(c["pairs"])] + [""]
        L += [f"**{c['rightLabel']}**"] + [f"{k + 1}. {c['pairs'][i]['right']}" for k, i in enumerate(right_order(c))] + [""]
        L += ["**Correct matches:**"] + [f"- {letters[i]} = {p['left']} → {p['right']}" for i, p in enumerate(c["pairs"])]
        L += ["", c["explanation"]]
    L += ["", f"*Concepts linked:* {c['links']}", "", "---", ""]
    return L


def main():
    cards = json.load(open(R("work", "cards_m68.json"), encoding="utf-8"))
    diagrams = json.load(open(R("ref", "live_diagrams.json"), encoding="utf-8"))
    if os.path.exists(R("work", "diagrams_m68.json")):
        diagrams.update(json.load(open(R("work", "diagrams_m68.json"), encoding="utf-8")))
    n = collections.Counter(c["type"] for c in cards)
    ncase = sum(1 for c in cards if c.get("caseStudy"))
    pairs = sum(len(c["pairs"]) for c in cards if c["type"] == "match")
    L = ["# BIOL 130 — Modules 6–8 Flashcards", "",
         "*Dr. Vivian Dayeh · Introductory Cell Biology · Fall 2026 · University of Waterloo*", "",
         "Suneung-style analytical questions in four formats: 보기 combination, matching, true/false and multiple "
         "choice. Many are built on real-world cases, and the case-study 보기 questions each centre on one real case "
         "with a diagram. Modules 7 and 8 are covered in full; Module 6, which already has its own set, gets case "
         "studies; and the bridge section connects Modules 6–8 back to Modules 1–5. Think through each question before "
         f"checking the key. For the interactive, auto-graded version, use the [study page]({ARTIFACT_URL}) (pick "
         "**Case studies** in the format row for just the case studies). Items marked **◇ Diagram** show a figure on "
         "the study page and in Anki; here each figure is described in one line instead.", "",
         f"**{len(cards)} items total** — 보기 Combination: {n['combo']} (including {ncase} case studies) · "
         f"Matching: {n['match']} ({pairs} pairs) · True/False: {n['tf']} · Multiple Choice: {n['mc']} · "
         f"◇ {sum(1 for c in cards if c.get('diagram'))} items include a diagram", "", "---", ""]
    q = 0
    for m in MOD_ORDER:
        cs = [c for c in cards if c["mod"] == m]
        if not cs:
            continue
        L += [f"## {MOD_TITLE[m]}", ""]
        for t in list(dict.fromkeys(c["topic"] for c in cs)):
            L += [f"### {t}", ""]
            for c in [c for c in cs if c["topic"] == t]:
                q += 1
                L += render(q, c, diagrams)
    out = R("outputs", "biol130_modules6-8_flashcards.md")
    os.makedirs(R("outputs"), exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"wrote outputs/biol130_modules6-8_flashcards.md: {q} questions, {len(chr(10).join(L))} characters")


if __name__ == "__main__":
    main()
