import json
import html
import hashlib
import random
import re
import genanki

# The Modules 3-6 deck = the delivered Modules 3-4 cards (unchanged, same GUIDs)
# + the Modules 5-6 cards. Add later sets to these two lists the same way.
CARD_FILES = ["cards_m34.json", "cards_m56.json"]
DIAGRAM_FILES = ["diagrams_m34.json", "diagrams_m56.json"]

CARDS = []
for fn in CARD_FILES:
    with open(fn) as f:
        CARDS += json.load(f)
# ids must be unique across every set (the web page keys progress by id alone,
# and each note's GUID is derived from type + id)
_ids = [c["id"] for c in CARDS]
assert len(_ids) == len(set(_ids)), f"duplicate card ids: {sorted(i for i in set(_ids) if _ids.count(i) > 1)}"

DIAGRAMS = {}
for fn in DIAGRAM_FILES:
    with open(fn) as f:
        part = json.load(f)
    clash = set(part) & set(DIAGRAMS)
    assert not clash, f"diagram key clash in {fn}: {sorted(clash)}"
    DIAGRAMS.update(part)
_missing = sorted({c["diagram"] for c in CARDS if c.get("diagram") and c["diagram"] not in DIAGRAMS})
assert not _missing, f"cards reference unknown diagrams: {_missing}"

combo_cards = [c for c in CARDS if c["type"] == "combo"]
match_cards = [c for c in CARDS if c["type"] == "match"]
tf_cards    = [c for c in CARDS if c["type"] == "tf"]
mc_cards    = [c for c in CARDS if c["type"] == "mc"]

assert len(combo_cards) + len(match_cards) + len(tf_cards) + len(mc_cards) == len(CARDS)

CIRCLED = ["①", "②", "③", "④", "⑤"]
LETTERS = [chr(ord("A") + i) for i in range(16)]

MOD_TAG = {0: "Bridge", 1: "Module_1", 2: "Module_2", 3: "Module_3", 4: "Module_4", 5: "Module_5", 6: "Module_6"}
FORMAT_TAG = {"combo": "Combination", "match": "Matching", "tf": "True_False", "mc": "Multiple_Choice"}


def esc(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def stable_id(seed: str) -> int:
    """Deterministic id from a string, so re-running this script regenerates
    the same model/deck ids (safe to re-run without minting new ones)."""
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def slug_tag(s: str) -> str:
    return (
        s.strip()
        .replace(" & ", "_")
        .replace("&", "and")
        .replace(" ", "_")
        .replace("/", "-")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
    )


def mod_tags(c):
    tags = [f"Mod::{MOD_TAG[c['mod']]}", f"Topic::{slug_tag(c['topic'])}", f"Format::{FORMAT_TAG[c['type']]}"]
    if c.get("diagram"):
        tags.append("Has_Diagram")
    return tags


# ---------------------------------------------------------------------------
# Diagram embedding: same fix as the web artifact -- pin each SVG to its own
# native viewBox pixel width (max-width:none) instead of letting it shrink to
# fit the card, so small diagram label text never scales below legible size
# on a narrow Anki window/phone screen. The figure sits inside an
# overflow-x:auto wrapper so an oversized diagram scrolls instead of
# shrinking. Unlike the web artifact, this can't add a scroll hint only when
# the diagram actually overflows (that used a JS scrollWidth check; Anki
# templates are plain HTML/CSS with no script, and script execution isn't
# reliable across Anki's various client apps), so the hint here is static
# and always shown alongside a diagram -- a small, constant cost in exchange
# for working the same way in every Anki client.
# ---------------------------------------------------------------------------
VIEWBOX_RE = re.compile(r'^<svg viewBox="0 0 ([\d.]+) ([\d.]+)"')


def diagram_html_for(c):
    key = c.get("diagram")
    if not key:
        return ""
    assert key in DIAGRAMS, f"card {c['type']}#{c['id']} references unknown diagram key {key!r}"
    d = DIAGRAMS[key]
    m = VIEWBOX_RE.match(d["svg"])
    if m:
        w = round(float(m.group(1)))
        svg_html = d["svg"].replace("<svg ", f'<svg style="width:{w}px;max-width:none;" ', 1)
    else:
        svg_html = d["svg"]
    return (
        f'<figure class="diagramfig">{svg_html}<figcaption>{esc(d["title"])}</figcaption></figure>'
        f'<div class="scrollhint">↔ scroll sideways if the diagram is cut off</div>'
    )


# ---------------------------------------------------------------------------
# Shared CSS: v3's layout language (passage box, <bogi> label, circled-number
# choices, O/X explanation rows) unchanged, plus:
#  - CSS custom properties on .card / the night-mode selectors, mirroring the
#    web artifact's palette, so the diagrams' var(--xxx) fill/stroke
#    references resolve correctly in both Anki day and night mode (the rest
#    of this stylesheet keeps its original hardcoded hex colors -- only the
#    new diagram markup needs the variables, so nothing else was rewritten).
#  - .diagramfig / figcaption / .scrollhint rules for the embedded SVGs.
# ---------------------------------------------------------------------------
SHARED_CSS = """
.card {
  --bg:#F5F6F1; --surface:#FFFFFF; --surface-2:#EDEFE6;
  --ink:#1B2E28; --ink-soft:#52645C; --ink-faint:#8B9A93;
  --border:#DCDFD3;
  --accent:#B87820; --accent-bg:#F1E2C8;
  --mod1:#215F7D; --mod1-bg:#E1EBF0;
  --mod2:#4D6B34; --mod2-bg:#E7EEDC;
  --bridge:#6E4C72; --bridge-bg:#EDE3ED;
  --good:#2F7A4C; --good-bg:#DFEEE3;
  --review:#A84B34; --review-bg:#F3E1D9;
  --visual:#4B58A6; --visual-bg:#E7E9F5;

  font-family: "Noto Serif KR", "Nanum Myeongjo", "Batang", "Georgia", serif;
  font-size: 17px;
  line-height: 1.6;
  color: #1B2E28;
  background-color: #F5F6F1;
  text-align: left;
}
.exam { max-width: 680px; margin: 0 auto; padding: 8px 10px 4px; }
.head {
  font-weight: 700; font-size: 13px; letter-spacing: .04em; text-transform: uppercase;
  color: #52645C; border-bottom: 2px solid #1B2E28; padding-bottom: 6px; margin-bottom: 14px;
  display: flex; justify-content: space-between; align-items: baseline;
}
.pts { font-weight: 700; color: #B87820; text-transform: none; letter-spacing: 0; font-size: 13px; }
.stem { margin-bottom: 10px; font-size: 17px; }
.stem.claimtext { font-weight: 700; font-size: 18px; margin-top: 4px; }
.passage {
  border: 1px solid #1B2E28; border-radius: 6px; padding: 12px 14px; margin: 10px 0 16px; background: #FFFFFF;
}
.bogi {
  border: 1px solid #1B2E28; border-radius: 6px; padding: 20px 14px 10px; position: relative; margin: 18px 0 10px; background: #FFFFFF;
}
.bogilabel {
  position: absolute; top: -13px; left: 50%; transform: translateX(-50%);
  background: #F5F6F1; padding: 0 10px; font-weight: 700;
}
.st { margin: 5px 0 8px 1.7em; text-indent: -1.7em; }
.choices { display: flex; flex-wrap: wrap; gap: 7px 24px; margin-top: 10px; font-size: 16px; }
.matchwrap { display: flex; gap: 20px; margin-top: 12px; }
.matchcol { flex: 1; min-width: 0; }
.matchcol-label {
  font-family: "Courier New", monospace; font-size: 11px; text-transform: uppercase; letter-spacing: .07em;
  color: #8B9A93; margin-bottom: 7px;
}
.matchcol .st { margin-left: 1.6em; text-indent: -1.6em; }
.ans { font-size: 19px; font-weight: 700; margin: 4px 0 12px; color: #2F7A4C; }
.matchkey { margin: 4px 0 14px; }
.expl .row, .matchkey .row { margin: 7px 0 10px; }
.tf { display: inline-block; font-weight: 700; min-width: 1.5em; }
.T { color: #2F7A4C; }
.F { color: #A84B34; }
.links { margin-top: 14px; font-size: 14px; color: #52645C; border-top: 1px dashed #DCDFD3; padding-top: 8px; }

.diagramfig {
  margin: 10px 0 16px; padding: 14px 14px 10px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 6px; text-align: left; overflow-x: auto;
}
.diagramfig svg { display: inline-block; height: auto; color: var(--ink); }
.diagramfig svg text { font-family: "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif; }
.diagramfig figcaption { font-size: 12px; color: #52645C; margin-top: 8px; }
.scrollhint { font-size: 11.5px; color: var(--visual); text-align: center; margin: -8px 0 12px; font-weight: 600; }

/* Anki night-mode support: older Anki used .nightMode, current Anki uses .night_mode */
.nightMode .card, .nightMode.card, .night_mode .card, .night_mode.card {
  --bg:#111C17; --surface:#17251F; --surface-2:#1E2F27;
  --ink:#EAF0EC; --ink-soft:#AFC0B7; --ink-faint:#75897F;
  --border:#2A3D34;
  --accent:#E1A24E; --accent-bg:#3A2C15;
  --mod1:#7CB6D6; --mod1-bg:#1B2E38;
  --mod2:#9BC17E; --mod2-bg:#26301C;
  --bridge:#CBA6CE; --bridge-bg:#332639;
  --good:#7FCC98; --good-bg:#1E3627;
  --review:#E28E70; --review-bg:#3B2620;
  --visual:#AEB9EE; --visual-bg:#272C48;
  background: #111C17; color: #EAF0EC;
}
.nightMode .passage, .nightMode .bogi, .night_mode .passage, .night_mode .bogi { border-color: #2A3D34; background: #17251F; }
.nightMode .head, .night_mode .head { border-color: #2A3D34; color: #AFC0B7; }
.nightMode .bogilabel, .night_mode .bogilabel { background: #111C17; }
.nightMode .matchcol-label, .night_mode .matchcol-label { color: #75897F; }
.nightMode .links, .night_mode .links { border-color: #2A3D34; color: #AFC0B7; }
.nightMode .ans, .nightMode .T, .night_mode .ans, .night_mode .T { color: #7FCC98; }
.nightMode .F, .night_mode .F { color: #E28E70; }
.nightMode .pts, .night_mode .pts { color: #E1A24E; }
.nightMode .diagramfig figcaption, .night_mode .diagramfig figcaption { color: #AFC0B7; }
"""

# ---------------------------------------------------------------------------
# Model: combo (보기 combination)
# ---------------------------------------------------------------------------
MODEL_COMBO_ID = stable_id("biol130-suneung-model-combo-v4")
model_combo = genanki.Model(
    MODEL_COMBO_ID,
    "BIOL 130 Suneung — 보기 Combination (+ Diagrams)",
    fields=[{"name": n} for n in ["Title", "Points", "Stem", "Diagram", "Box", "Statements", "Choices", "Answer", "Explanation", "Links"]],
    templates=[{
        "name": "Card 1",
        "qfmt": """<div class="exam"><div class="head">{{Title}} <span class="pts">[{{Points}}점]</span></div>
<div class="stem">{{Stem}}</div>
{{Diagram}}
<div class="passage">{{Box}}</div>
<div class="bogi"><div class="bogilabel">&lt;보 기&gt;</div>{{Statements}}</div>
<div class="choices">{{Choices}}</div></div>""",
        "afmt": """{{FrontSide}}<hr id="answer"><div class="exam">
<div class="ans">Answer: {{Answer}}</div>
<div class="expl">{{Explanation}}</div>
<div class="links"><b>Concepts linked:</b> {{Links}}</div></div>""",
    }],
    css=SHARED_CSS,
)

# ---------------------------------------------------------------------------
# Model: match
# ---------------------------------------------------------------------------
MODEL_MATCH_ID = stable_id("biol130-suneung-model-match-v4")
model_match = genanki.Model(
    MODEL_MATCH_ID,
    "BIOL 130 Suneung — Matching (+ Diagrams)",
    fields=[{"name": n} for n in ["Title", "Points", "Prompt", "Diagram", "LeftLabel", "RightLabel", "LeftItems", "RightItems", "AnswerKey", "Explanation", "Links"]],
    templates=[{
        "name": "Card 1",
        "qfmt": """<div class="exam"><div class="head">{{Title}} <span class="pts">[{{Points}}점]</span></div>
<div class="stem">{{Prompt}}</div>
{{Diagram}}
<div class="matchwrap">
  <div class="matchcol"><div class="matchcol-label">{{LeftLabel}}</div>{{LeftItems}}</div>
  <div class="matchcol"><div class="matchcol-label">{{RightLabel}}</div>{{RightItems}}</div>
</div></div>""",
        "afmt": """{{FrontSide}}<hr id="answer"><div class="exam">
<div class="ans">Correct matches</div>
<div class="matchkey">{{AnswerKey}}</div>
<div class="expl">{{Explanation}}</div>
<div class="links"><b>Concepts linked:</b> {{Links}}</div></div>""",
    }],
    css=SHARED_CSS,
)

# ---------------------------------------------------------------------------
# Model: tf — true/false scenario judgment
# ---------------------------------------------------------------------------
MODEL_TF_ID = stable_id("biol130-suneung-model-tf-v4")
model_tf = genanki.Model(
    MODEL_TF_ID,
    "BIOL 130 Suneung — True/False (+ Diagrams)",
    fields=[{"name": n} for n in ["Points", "Box", "Diagram", "Claim", "Answer", "Explanation", "Links"]],
    templates=[{
        "name": "Card 1",
        "qfmt": """<div class="exam"><div class="head">True / False <span class="pts">[{{Points}}점]</span></div>
<div class="passage">{{Box}}</div>
{{Diagram}}
<div class="stem claimtext">{{Claim}}</div></div>""",
        "afmt": """{{FrontSide}}<hr id="answer"><div class="exam">
<div class="ans">{{Answer}}</div>
<div class="expl">{{Explanation}}</div>
<div class="links"><b>Concepts linked:</b> {{Links}}</div></div>""",
    }],
    css=SHARED_CSS,
)

# ---------------------------------------------------------------------------
# Model: mc — plain single-best-answer multiple choice
# ---------------------------------------------------------------------------
MODEL_MC_ID = stable_id("biol130-suneung-model-mc-v4")
model_mc = genanki.Model(
    MODEL_MC_ID,
    "BIOL 130 Suneung — Multiple Choice (+ Diagrams)",
    fields=[{"name": n} for n in ["Stem", "Diagram", "Points", "Options", "Answer", "Explanation", "Links"]],
    templates=[{
        "name": "Card 1",
        "qfmt": """<div class="exam"><div class="head">Multiple Choice <span class="pts">[{{Points}}점]</span></div>
<div class="stem">{{Stem}}</div>
{{Diagram}}
<div class="choices">{{Options}}</div></div>""",
        "afmt": """{{FrontSide}}<hr id="answer"><div class="exam">
<div class="ans">Answer: {{Answer}}</div>
<div class="expl">{{Explanation}}</div>
<div class="links"><b>Concepts linked:</b> {{Links}}</div></div>""",
    }],
    css=SHARED_CSS,
)

# Deck title and file name say only what the deck covers (course::modules, or
# course::lecture) -- never style labels like "Suneung". Anki matches decks by
# NAME on import, so the deck id itself doesn't matter much.
# NOTE: the four note types above are shared with every deck already in Eric's
# Anki (same model ids, fields, templates, CSS). Never change them.
DECK_NAME = "BIOL 130::Modules 3-6"
OUT_FILE = "BIOL130_Modules3-6.apkg"
DECK_ID = stable_id("biol130-flashcards-deck-modules-3-6")
deck = genanki.Deck(DECK_ID, DECK_NAME)

n_combo = n_match = n_tf = n_mc = 0
n_diagram = 0

# ---- combo ----
for c in combo_cards:
    stmt_html = "".join(f'<div class="st">{esc(s["label"])}. {esc(s["text"])}</div>' for s in c["statements"])
    choices_html = "".join(f'<span>{CIRCLED[i]} {esc(ch)}</span>' for i, ch in enumerate(c["choices"]))
    answer_str = f'{CIRCLED[c["answerIndex"]]} {esc(c["choices"][c["answerIndex"]])}'
    expl_html = "".join(
        f'<div class="row"><span class="tf {"T" if s["correct"] else "F"}">{esc(s["label"])} {"O" if s["correct"] else "X"}</span> {esc(s["explanation"])}</div>'
        for s in c["statements"]
    )
    diag_html = diagram_html_for(c)
    if diag_html:
        n_diagram += 1
    note = genanki.Note(
        model=model_combo,
        fields=[esc(c["title"]), str(c.get("points", "")), esc(c["stem"]), diag_html, c["box"], stmt_html, choices_html, answer_str, expl_html, esc(c.get("links", ""))],
        tags=mod_tags(c),
        guid=genanki.guid_for(f"biol130-card-v4-combo-{c['id']}"),
    )
    deck.add_note(note)
    n_combo += 1

# ---- match ----
for c in match_cards:
    pairs = c["pairs"]
    n = len(pairs)
    order = list(range(n))
    rnd = random.Random(f"biol130-match-shuffle-{c['id']}")
    tries = 0
    while True:
        rnd.shuffle(order)
        tries += 1
        # avoid the degenerate case where the shuffle lands on the identity
        # order (right column would visually line up with left, trivializing
        # the exercise) -- reseed and retry a few times if that happens.
        if n < 2 or order != list(range(n)) or tries > 8:
            break
    left_html = "".join(f'<div class="st">{LETTERS[i]}. {esc(pr["left"])}</div>' for i, pr in enumerate(pairs))
    right_html = "".join(f'<div class="st">{k + 1}. {esc(pairs[origIdx]["right"])}</div>' for k, origIdx in enumerate(order))
    key_html = "".join(f'<div class="row"><span class="tf T">{LETTERS[i]}</span> {esc(pr["left"])} = {esc(pr["right"])}</div>' for i, pr in enumerate(pairs))
    diag_html = diagram_html_for(c)
    if diag_html:
        n_diagram += 1
    note = genanki.Note(
        model=model_match,
        fields=[
            esc(c.get("title", "")), str(c.get("points", "")), esc(c["prompt"]), diag_html,
            esc(c.get("leftLabel", "Items")), esc(c.get("rightLabel", "Match")),
            left_html, right_html, key_html, esc(c.get("explanation", "")), esc(c.get("links", "")),
        ],
        tags=mod_tags(c),
        guid=genanki.guid_for(f"biol130-card-v4-match-{c['id']}"),
    )
    deck.add_note(note)
    n_match += 1

# ---- tf ----
for c in tf_cards:
    answer_str = f'<span class="tf {"T" if c["answer"] else "F"}">{"True" if c["answer"] else "False"}</span>'
    diag_html = diagram_html_for(c)
    if diag_html:
        n_diagram += 1
    note = genanki.Note(
        model=model_tf,
        fields=[str(c.get("points", "")), esc(c.get("box", "")), diag_html, esc(c["claim"]), answer_str, esc(c["explanation"]), esc(c.get("links", ""))],
        tags=mod_tags(c),
        guid=genanki.guid_for(f"biol130-card-v4-tf-{c['id']}"),
    )
    deck.add_note(note)
    n_tf += 1

# ---- mc ----
for c in mc_cards:
    options_html = "".join(f'<span>{CIRCLED[i]} {esc(opt)}</span>' for i, opt in enumerate(c["options"]))
    answer_str = f'{CIRCLED[c["answerIndex"]]} {esc(c["options"][c["answerIndex"]])}'
    diag_html = diagram_html_for(c)
    if diag_html:
        n_diagram += 1
    note = genanki.Note(
        model=model_mc,
        fields=[esc(c["stem"]), diag_html, str(c.get("points", "")), options_html, answer_str, esc(c["explanation"]), esc(c.get("links", ""))],
        tags=mod_tags(c),
        guid=genanki.guid_for(f"biol130-card-v4-mc-{c['id']}"),
    )
    deck.add_note(note)
    n_mc += 1

pkg = genanki.Package(deck)
pkg.write_to_file(OUT_FILE)
total = n_combo + n_match + n_tf + n_mc
print(f"Wrote {total} notes to {OUT_FILE} (deck: {DECK_NAME})")
print(f"  combo={n_combo} match={n_match} tf={n_tf} mc={n_mc}")
print(f"  notes carrying a diagram: {n_diagram}")
print(f"  model ids: combo={MODEL_COMBO_ID} match={MODEL_MATCH_ID} tf={MODEL_TF_ID} mc={MODEL_MC_ID}")
print(f"  deck id: {DECK_ID}")
