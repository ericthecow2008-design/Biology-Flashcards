"""Render the Module 5-6 cards into reviewer packets (markdown)."""
import json, os, re, sys
os.makedirs("review_m56", exist_ok=True)

audit = json.load(open("cards_m56_audit.json"))
ledger = json.load(open("concept_ledger_m56.json"))
desc = {slug: d for cat in ledger.values() for slug, d in cat.items()}
diagrams = json.load(open("diagrams_m56.json"))
CIRC = "①②③④⑤"
TYPE = {"combo": "보기 COMBINATION", "match": "MATCHING", "tf": "TRUE/FALSE", "mc": "MULTIPLE CHOICE"}

def plain(html):
    s = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n", html)
    s = re.sub(r"<br\s*/?>", "\n", s)
    return re.sub(r"</?b>", "", s)

def render(c):
    L = []
    d = c.get("diagram")
    head = f"### #{c['id']} · {TYPE[c['type']]} · {c['topic']} · {c['points']} pt"
    if d:
        head += f" · DIAGRAM `{d}` (\"{diagrams[d]['title']}\")"
    L.append(head)
    L.append("**Question side**")
    if c["type"] == "combo":
        L.append(f"Title: {c['title']}")
        L.append(f"Stem: {c['stem']}")
        L.append("Box:\n" + "\n".join("> " + x for x in plain(c["box"]).split("\n")))
        for s in c["statements"]:
            L.append(f"- {s['label']}. {s['text']}")
        L.append("Choices: " + "   ".join(f"{CIRC[i]} {ch}" for i, ch in enumerate(c["choices"])))
        L.append("**Key**: " + f"{CIRC[c['answerIndex']]} {c['choices'][c['answerIndex']]}")
        for s in c["statements"]:
            L.append(f"- {s['label']} {'TRUE' if s['correct'] else 'FALSE'} — {s['explanation']}")
    elif c["type"] == "match":
        L.append(f"Title: {c['title']}")
        L.append(f"Prompt: {c['prompt']}  (left = {c['leftLabel']}, right = {c['rightLabel']}; right column is shuffled for the student)")
        L.append("**Key (correct pairs)**:")
        for p in c["pairs"]:
            L.append(f"- {p['left']}  →  {p['right']}")
        L.append(f"Explanation: {c['explanation']}")
    elif c["type"] == "tf":
        L.append(f"Context box: {c['box']}")
        L.append(f"Claim: {c['claim']}")
        L.append(f"**Key**: {'TRUE' if c['answer'] else 'FALSE'}")
        L.append(f"Explanation: {c['explanation']}")
    else:
        L.append(f"Stem: {c['stem']}")
        for i, o in enumerate(c["options"]):
            L.append(f"{CIRC[i]} {o}")
        L.append(f"**Key**: {CIRC[c['answerIndex']]} {c['options'][c['answerIndex']]}")
        L.append(f"Explanation: {c['explanation']}")
    L.append(f"Links line shown on answer side: {c['links']}")
    L.append("Concept tags claimed (each should be GENUINELY tested by this card):")
    for k in c["concepts"]:
        L.append(f"  - `{k}`: {desc[k]}")
    return "\n".join(L)

def packet(cards, path, title):
    out = [f"# {title}", "",
           f"{len(cards)} cards. Diagram descriptions (aria-labels) for every diagram used are in diagrams_m56_descriptions.md; "
           "rendered images are in gallery_m56_a/, gallery_m56_b/, gallery_m56_c/ (files <key>__light.png and _sheet_*.png).", ""]
    for c in cards:
        out += [render(c), "", "---", ""]
    open(path, "w").write("\n".join(out))
    print("wrote", path, len(cards))

m5 = [c for c in audit if c["mod"] == 5]
m6b = [c for c in audit if c["mod"] in (6, 0)]
which = sys.argv[1] if len(sys.argv) > 1 else "full"
packet(m5, "review_m56/cards_mod5.md", "Module 5 cards (Protein Structure, Function and Synthesis)")
packet(m6b, "review_m56/cards_mod6_bridge.md", "Module 6 cards (Making Life Work) + bridge cards connecting Modules 1–6")
with open("review_m56/diagrams_m56_descriptions.md", "w") as f:
    for k, v in diagrams.items():
        aria = re.search(r'aria-label="([^"]+)"', v["svg"]).group(1)
        texts = re.findall(r"<text[^>]*>([^<]*)</text>", v["svg"])
        f.write(f"## `{k}` — {v['title']}\n\nDescription: {aria}\n\nAll visible text labels: {' | '.join(t for t in texts if t.strip())}\n\n")
with open("review_m56/concept_ledger.md", "w") as f:
    for cat, slugs in ledger.items():
        f.write(f"## {cat}\n")
        for s, d in slugs.items():
            f.write(f"- `{s}`: {d}\n")
        f.write("\n")
print("wrote diagram descriptions and ledger")
