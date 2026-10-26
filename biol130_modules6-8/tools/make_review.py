"""Write the reviewer packets, one per part, so several reviewers can work in parallel:
  work/review/cards_mod6.md, cards_mod7.md, cards_mod8.md, cards_bridge.md  (cards with keys, explanations
  and claimed concept tags; case-study cards are marked) and work/review/diagrams.md (each diagram's
  description and every visible label).

A part with more than 60 cards is also written in two halves (e.g. cards_mod7_a.md and cards_mod7_b.md,
split at the topic boundary nearest the middle), so each half can go to its own pair of reviewers.

Usage (from the kit folder):  python3 tools/make_review.py
Run tools/shoot_gallery.js first so every diagram has an image; the packets name each image and this
script lists any that are missing.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *a: os.path.join(ROOT, *a)
CIRC = "①②③④⑤"
TYPE = {"combo": "보기 COMBINATION", "match": "MATCHING", "tf": "TRUE/FALSE", "mc": "MULTIPLE CHOICE"}
PART = {6: "cards_mod6.md", 7: "cards_mod7.md", 8: "cards_mod8.md", 0: "cards_bridge.md"}


def flatten(obj, out):
    for k, v in obj.items():
        if isinstance(v, dict):
            flatten(v, out)
        else:
            out[k] = v
    return out


def plain(s):
    s = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n", s or "")
    return re.sub(r"</?b>", "", re.sub(r"<br\s*/?>", "\n", s))


def main():
    audit = json.load(open(R("work", "cards_m68_audit.json"), encoding="utf-8"))
    new_d = json.load(open(R("work", "diagrams_m68.json"), encoding="utf-8")) if os.path.exists(R("work", "diagrams_m68.json")) else {}
    diagrams = {**json.load(open(R("ref", "live_diagrams.json"), encoding="utf-8")), **new_d}
    ledger = flatten(json.load(open(R("work", "concept_ledger_m68.json"), encoding="utf-8")), {})
    os.makedirs(R("work", "review"), exist_ok=True)
    missing = set()

    def image(key):
        p = f"work/gallery/{key}__light.png"
        if not os.path.exists(R(p)):
            missing.add(key)
        return p

    def render(c):
        d = c.get("diagram")
        head = (f"### #{c['id']} · {TYPE[c['type']]}{' · CASE STUDY' if c.get('caseStudy') else ''} · "
                f"{'Bridge' if c['mod'] == 0 else 'Module ' + str(c['mod'])} · {c['topic']} · {c['points']} pt")
        if d:
            head += f" · diagram `{d}` (\"{diagrams[d]['title']}\"; image: {image(d)})"
        L = [head]
        if c.get("title"):
            L.append(f"Title: {c['title']}")
        t = c["type"]
        if t == "combo":
            L += [f"Stem: {c['stem']}", "Box:\n" + "\n".join("> " + x for x in plain(c["box"]).split("\n"))]
            L += [f"- {s['label']}. {s['text']}" for s in c["statements"]]
            L.append("Choices: " + "   ".join(f"{CIRC[i]} {x}" for i, x in enumerate(c["choices"])))
            L.append(f"**Key**: {CIRC[c['answerIndex']]} {c['choices'][c['answerIndex']]}")
            L += [f"- {s['label']} {'TRUE' if s['correct'] else 'FALSE'}: {s['explanation']}" for s in c["statements"]]
        elif t == "tf":
            L += [f"Scenario: {c['box']}", f"Claim: {c['claim']}", f"**Key**: {'TRUE' if c['answer'] else 'FALSE'}",
                  f"Explanation: {c['explanation']}"]
        elif t == "mc":
            L += [f"Stem: {c['stem']}"] + [f"{CIRC[i]} {o}" for i, o in enumerate(c["options"])]
            L += [f"**Key**: {CIRC[c['answerIndex']]}", f"Explanation: {c['explanation']}"]
        else:
            L += [f"Prompt: {c['prompt']}", f"Pairs ({c['leftLabel']} → {c['rightLabel']}):"]
            L += [f"- {p['left']} → {p['right']}" for p in c["pairs"]]
            L += [f"Explanation: {c['explanation']}"]
        L.append(f"Links line (answer side): {c['links']}")
        L.append("Concept tags claimed (each should be genuinely tested by this card):")
        L += [f"  - `{k}`: {ledger.get(k, '(not in the ledger)')}" for k in c["concepts"]]
        return L + ["", "---", ""]

    written = []
    for m, name in PART.items():
        cs = [c for c in audit if c["mod"] == m]
        if not cs:
            continue
        title = "Bridge cards (Connecting Modules 1–8)" if m == 0 else f"Module {m}"

        def packet(fname, part_cs, heading):
            out = [f"# Reviewer packet: {heading}", "",
                   f"{len(part_cs)} cards. Diagram descriptions and every visible label: work/review/diagrams.md. "
                   "Open each card's image before judging the card.", ""]
            for c in part_cs:
                out += render(c)
            open(R("work", "review", fname), "w", encoding="utf-8").write("\n".join(out))
            written.append(f"{fname} ({len(part_cs)})")

        packet(name, cs, title)
        if len(cs) > 60:
            # split at the topic boundary nearest the middle (or the middle, if no boundary is near it)
            cuts = [i for i in range(1, len(cs)) if cs[i]["topic"] != cs[i - 1]["topic"]
                    and 0.35 * len(cs) <= i <= 0.65 * len(cs)]
            cut = min(cuts, key=lambda i: abs(i - len(cs) / 2)) if cuts else len(cs) // 2
            stem = name[:-3]
            packet(stem + "_a.md", cs[:cut], f"{title}, first half")
            packet(stem + "_b.md", cs[cut:], f"{title}, second half")
    with open(R("work", "review", "diagrams.md"), "w", encoding="utf-8") as f:
        for k in sorted({c["diagram"] for c in audit if c.get("diagram")}):
            v = diagrams[k]
            aria = html.unescape(re.search(r'aria-label="([^"]+)"', v["svg"]).group(1))
            texts = [html.unescape(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", v["svg"]) if t.strip()]
            f.write(f"## `{k}`: {v['title']}\n\nDescription: {aria}\n\nAll visible text: {' | '.join(texts)}\n\n")
    print("wrote work/review/" + ", ".join(written) + " and diagrams.md")
    if missing:
        print("MISSING images (shoot them first):", ", ".join(sorted(missing)))
        print("  new diagrams:     node tools/shoot_gallery.js")
        reused = sorted(k for k in missing if k not in new_d)
        if reused:
            print("  reused diagrams:  DIAGRAMS=ref/live_diagrams.json KEYS=" + ",".join(reused) + " node tools/shoot_gallery.js")


if __name__ == "__main__":
    main()
