"""Build the Anki deck for the Modules 6-8 set (all four formats, case studies included).

Usage (from the kit folder):  python3 tools/build_apkg.py
  -> outputs/BIOL130_Modules6-8.apkg, deck "BIOL 130::Modules 6-8"

Uses Eric's four existing note types exactly as they are in his decks (ref/note_types.json: same ids,
fields, templates and CSS), and fills the fields in exactly the format of his existing notes, so the
new cards look like every other card he has. Each note's GUID is guid_for("biol130-card-v4-{type}-{id}"),
the scheme every BIOL 130 deck uses; ids are unique across all sets, so nothing collides.
Options: --cards FILE (default work/cards_m68.json), --deck NAME, --out FILE, --deck-seed TEXT
"""
import argparse, hashlib, html, json, os, random, re, sys
import genanki

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *a: os.path.join(ROOT, *a)

CIRCLED = ["①", "②", "③", "④", "⑤"]
MOD_TAG = {0: "Bridge", 1: "Module_1", 2: "Module_2", 3: "Module_3", 4: "Module_4", 5: "Module_5",
           6: "Module_6", 7: "Module_7", 8: "Module_8"}
FORMAT_TAG = {"combo": "Combination", "match": "Matching", "tf": "True_False", "mc": "Multiple_Choice"}
MODEL_ID = {"combo": 3125599791, "match": 3840893743, "tf": 1392138497, "mc": 1294902607}


def esc(s):
    return "" if s is None else html.escape(str(s), quote=True)


def stable_id(text):
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def slug_tag(s):
    # same rule as every earlier BIOL 130 deck: "DNA: Evidence & Structure" -> "DNA:_Evidence_Structure"
    return "_".join(s.replace("&", "").split())


def tags_for(c):
    t = [f"Mod::{MOD_TAG[c['mod']]}", f"Topic::{slug_tag(c['topic'])}", f"Format::{FORMAT_TAG[c['type']]}"]
    if c.get("diagram"):
        t.append("Has_Diagram")
    return t


def diagram_html(c, diagrams):
    """The diagram exactly as Eric's other notes carry it: pinned to its own width so small labels never
    shrink on a phone; the figure scrolls sideways instead."""
    key = c.get("diagram")
    if not key:
        return ""
    d = diagrams[key]
    w = re.search(r'viewBox="0 0 ([\d.]+)', d["svg"]).group(1)
    svg = d["svg"].replace("<svg ", f'<svg style="width:{w}px;max-width:none;" ', 1)
    return (f'<figure class="diagramfig">{svg}<figcaption>{esc(d["title"])}</figcaption></figure>'
            f'<div class="scrollhint">↔ scroll sideways if the diagram is cut off</div>')


def fields_for(c, diagrams):
    t = c["type"]
    if t == "combo":
        st = "".join(f'<div class="st">{s["label"]}. {esc(s["text"])}</div>' for s in c["statements"])
        ch = "".join(f"<span>{CIRCLED[i]} {esc(x)}</span>" for i, x in enumerate(c["choices"]))
        ex = "".join(f'<div class="row"><span class="tf {"T" if s["correct"] else "F"}">{s["label"]} {"O" if s["correct"] else "X"}</span> {esc(s["explanation"])}</div>'
                     for s in c["statements"])
        return [esc(c["title"]), str(c["points"]), esc(c["stem"]), diagram_html(c, diagrams), c["box"], st, ch,
                f'{CIRCLED[c["answerIndex"]]} {esc(c["choices"][c["answerIndex"]])}', ex, esc(c["links"])]
    if t == "tf":
        ans = '<span class="tf T">True</span>' if c["answer"] else '<span class="tf F">False</span>'
        return [str(c["points"]), esc(c.get("box", "")), diagram_html(c, diagrams), esc(c["claim"]), ans,
                esc(c["explanation"]), esc(c["links"])]
    if t == "mc":
        opts = "".join(f"<span>{CIRCLED[i]} {esc(o)}</span>" for i, o in enumerate(c["options"]))
        return [esc(c["stem"]), diagram_html(c, diagrams), str(c["points"]), opts,
                f'{CIRCLED[c["answerIndex"]]} {esc(c["options"][c["answerIndex"]])}', esc(c["explanation"]), esc(c["links"])]
    if t == "match":
        L = [chr(ord("A") + i) for i in range(len(c["pairs"]))]
        rights = [p["right"] for p in c["pairs"]]
        order = list(range(len(rights)))
        random.Random(int(hashlib.sha256(f"biol130-match-order-{c['id']}".encode()).hexdigest()[:12], 16)).shuffle(order)
        left = "".join(f'<div class="st">{L[i]}. {esc(p["left"])}</div>' for i, p in enumerate(c["pairs"]))
        right = "".join(f'<div class="st">{j + 1}. {esc(rights[i])}</div>' for j, i in enumerate(order))
        key = "".join(f'<div class="row"><span class="tf T">{L[i]}</span> {esc(p["left"])} = {esc(p["right"])}</div>'
                      for i, p in enumerate(c["pairs"]))
        return [esc(c["title"]), str(c["points"]), esc(c["prompt"]), diagram_html(c, diagrams), esc(c["leftLabel"]),
                esc(c["rightLabel"]), left, right, key, esc(c["explanation"]), esc(c["links"])]
    raise ValueError(f"unknown card type {t}")


def load_models():
    nt = json.load(open(R("ref", "note_types.json"), encoding="utf-8"))
    out = {}
    for t, mid in MODEL_ID.items():
        m = nt[str(mid)]
        out[t] = genanki.Model(m["id"], m["name"], fields=[{"name": f} for f in m["fields"]],
                               templates=m["templates"], css=m["css"], sort_field_index=m.get("sortf", 0))
    return out


def build(cards, diagrams, deck_name, out_file, deck_seed):
    ids = [c["id"] for c in cards]
    assert len(ids) == len(set(ids)), "duplicate card ids"
    missing = sorted({c["diagram"] for c in cards if c.get("diagram") and c["diagram"] not in diagrams})
    assert not missing, f"unknown diagrams: {missing}"
    models = load_models()
    deck = genanki.Deck(stable_id(deck_seed), deck_name)
    for c in cards:
        deck.add_note(genanki.Note(model=models[c["type"]], fields=fields_for(c, diagrams), tags=tags_for(c),
                                   guid=genanki.guid_for(f"biol130-card-v4-{c['type']}-{c['id']}")))
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    genanki.Package(deck).write_to_file(out_file)
    return deck


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards", action="append", default=None)
    ap.add_argument("--deck", default="BIOL 130::Modules 6-8")
    ap.add_argument("--out", default=R("outputs", "BIOL130_Modules6-8.apkg"))
    ap.add_argument("--deck-seed", default="biol130-flashcards-deck-modules-6-8")
    a = ap.parse_args()
    cards = []
    for fn in a.cards or [R("work", "cards_m68.json")]:
        cards += json.load(open(fn, encoding="utf-8"))
    diagrams = json.load(open(R("ref", "live_diagrams.json"), encoding="utf-8"))
    if os.path.exists(R("work", "diagrams_m68.json")):
        new = json.load(open(R("work", "diagrams_m68.json"), encoding="utf-8"))
        clash = set(new) & set(diagrams)
        assert not clash, f"new diagram keys clash with the study page's: {clash}"
        diagrams.update(new)
    deck = build(cards, diagrams, a.deck, a.out, a.deck_seed)
    print(f"wrote {len(cards)} notes to {os.path.relpath(a.out, ROOT)} (deck {a.deck!r}, deck id {deck.deck_id}); "
          f"{sum(1 for c in cards if c.get('diagram'))} with a diagram")


if __name__ == "__main__":
    main()
