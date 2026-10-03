"""Assemble the Modules 5-6 card set (same pipeline as build_cards_m34.py).

- ids: combo 2001+, match 2101+, tf 2201+, mc 2301+ (globally unique vs Modules 1-4)
- combo: statements re-ordered so the correct-answer patterns are balanced
  (1-true cards cycle through ㄱ/ㄴ/ㄷ, 2-true cards through the three pairs);
  5 answer choices drawn deterministically, listed in canonical order
- mc: correct option placed at balanced positions (a fresh permutation of 0-4
  for every block of five MC cards)
Writes cards_m56_audit.json (with `concepts`) and cards_m56.json (clean), then
prints balance statistics and a concept-coverage audit.
"""
import json, random, hashlib, collections, re
import cards_m5a, cards_m5b, cards_m6, cards_bridge56

LAB = ["ㄱ", "ㄴ", "ㄷ"]
CANON = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
ONE_TRUE = ["ㄴ", "ㄷ", "ㄱ", "ㄷ", "ㄴ", "ㄱ", "ㄷ", "ㄴ"]
TWO_TRUE = ["ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ"]
MOD_ORDER = [5, 6, 0]
TOPIC_ORDER = ["Amino Acids & Peptide Bonds", "Levels of Protein Structure",
               "Translation Machinery & Genetic Code", "Translation Stages: Prok vs Euk",
               "Regulation & Protein Sorting",
               "Energy & Metabolism", "ATP & Energetic Coupling", "Thermodynamics & Free Energy",
               "Enzymes & Their Regulation", "Connecting Modules 1–6"]

ledger = json.load(open("concept_ledger_m56.json"))
valid = {slug for cat in ledger.values() for slug in cat}
diagrams = json.load(open("diagrams_m56.json"))

raw = cards_m5a.CARDS + cards_m5b.CARDS + cards_m6.CARDS + cards_bridge56.CARDS

# ── independent-review follow-ups, keyed by the start of each card's title/claim/stem ──
REVIEW = {
    # tag trims from the independent review (tags a card does not genuinely need)
    "Four ways to unfold a protein": {"drop": ["hydrophilic_aa_hbond_surface"]},
    "The mRNA codon becomes GUA": {"drop": ["central_dogma_translation_final"]},
    "Using the genetic code table, which single-base change": {"drop": ["codon_triplet_nonoverlapping"]},
    "In the diagram, which way is the ribosome moving": {"drop": ["n_terminus_c_terminus"]},
    "Alanine was inserted wherever": {"drop": ["codon_anticodon_antiparallel"]},
    "Ribosomes can skip the leucine codons": {"drop": ["ribosome_a_p_e_sites"]},
    "The standard genetic code has 64 codons": {"drop": ["termination_release_factor"]},
    "Which RNAs are made by transcription": {"drop": ["gene_expression_overview_euk"]},
    "The bacterial ribosomes can bind the cap": {"drop": ["translation_components"]},
    "Each ribosome makes only part": {"drop": ["gene_expression_overview_euk"]},
    "This is possible because the two cell types": {"drop": ["genetic_code_64_redundant"]},
    "Where is the energy?": {"drop": ["m3_active_transport_atp"]},
    "Since much of it ends up as heat": {"drop": ["potential_vs_kinetic_energy"]},
    "Which way does the energy flow?": {"drop": ["atp_hydrolysis_exergonic_repulsion"]},
    "One molecule of an enzyme can convert": {"drop": ["active_site_binds_stabilizes_ts"]},
    "Given only its genome": {"drop": ["cells_need_energy_work"]},
    "Its cloverleaf is held together": {"drop": ["m2_nucleotide_atp_scaffold"]},
    "They therefore can't replace damaged hemoglobin": {"drop": ["ribosome_rna_protein_subunits"]},
}

def key_text(c):
    return c.get("title") or (c["claim"] if c["type"] == "tf" else c["stem"])

for k, spec in REVIEW.items():
    hits = [c for c in raw if key_text(c).startswith(k)]
    assert len(hits) == 1, f"review key {k!r} matched {len(hits)} cards"
    c = hits[0]
    for t in spec.get("drop", []):
        assert t in c["concepts"], f"{k!r}: tag {t} not present"
        c["concepts"].remove(t)
    for t in spec.get("add", []):
        assert t not in c["concepts"], f"{k!r}: tag {t} already present"
        c["concepts"].append(t)
    if spec.get("nodiag"):
        assert c.get("diagram"), f"{k!r}: has no diagram to drop"
        del c["diagram"]
    assert c["concepts"], f"{k!r}: no tags left"

raw = sorted(raw, key=lambda c: (MOD_ORDER.index(c["mod"]), TOPIC_ORDER.index(c["topic"])))

def seed(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:12], 16)

errors = []
for c in raw:
    for k in c["concepts"]:
        if k not in valid:
            errors.append(f"unknown concept slug {k!r} in {key_text(c)}"[:160])
    if len(set(c["concepts"])) != len(c["concepts"]):
        errors.append(f"duplicate concept tag in {key_text(c)[:80]}")
    if c.get("diagram") and c["diagram"] not in diagrams:
        errors.append(f"unknown diagram {c['diagram']}")
keys = [key_text(c)[:60] for c in raw]
dupk = [k for k, n in collections.Counter(keys).items() if n > 1]
if dupk:
    errors.append(f"duplicate card keys: {dupk}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)

next_id = {"combo": 2001, "match": 2101, "tf": 2201, "mc": 2301}
i1 = i2 = 0
mc_i = 0
mc_perm = []
out = []
for c in raw:
    t = c["type"]
    card = {"id": next_id[t], "type": t, "mod": c["mod"], "topic": c["topic"], "points": c["points"]}
    next_id[t] += 1
    if t == "combo":
        sts = c["statements"]
        ntrue = sum(s["correct"] for s in sts)
        if ntrue == 1:
            target = ONE_TRUE[i1 % len(ONE_TRUE)]; i1 += 1
        elif ntrue == 2:
            target = TWO_TRUE[i2 % len(TWO_TRUE)]; i2 += 1
        else:
            target = "ㄱ, ㄴ, ㄷ"
        want = [LAB.index(x) for x in target.split(", ")]
        trues = [s for s in sts if s["correct"]]
        falses = [s for s in sts if not s["correct"]]
        slots = [None] * 3
        for pos, s in zip(want, trues):
            slots[pos] = s
        rest = [p for p in range(3) if p not in want]
        for pos, s in zip(rest, falses):
            slots[pos] = s
        statements = [{"label": LAB[i], "text": s["text"], "correct": s["correct"], "explanation": s["explanation"]}
                      for i, s in enumerate(slots)]
        correct_str = ", ".join(st["label"] for st in statements if st["correct"])
        assert correct_str == target
        rnd = random.Random(seed("choices-" + c["title"]))
        others = [x for x in CANON if x != correct_str]
        picked = set(rnd.sample(others, 4)) | {correct_str}
        choices = [x for x in CANON if x in picked]
        card.update({"title": c["title"], "stem": c["stem"], "box": c["box"], "statements": statements,
                     "choices": choices, "answerIndex": choices.index(correct_str)})
    elif t == "match":
        card.update({k: c[k] for k in ["title", "prompt", "leftLabel", "rightLabel", "pairs", "explanation"]})
    elif t == "tf":
        card.update({k: c[k] for k in ["box", "claim", "answer", "explanation"]})
    elif t == "mc":
        if mc_i % 5 == 0:
            mc_perm = list(range(5))
            random.Random(seed(f"m56-mcblock-{mc_i}")).shuffle(mc_perm)
        pos = mc_perm[mc_i % 5]; mc_i += 1
        opts = list(c["distractors"])
        opts.insert(pos, c["correct"])
        assert len(set(opts)) == 5, c["stem"][:60]
        card.update({"stem": c["stem"], "options": opts, "answerIndex": pos, "explanation": c["explanation"]})
    card["links"] = c["links"]
    if c.get("diagram"):
        card["diagram"] = c["diagram"]
    audit = dict(card); audit["concepts"] = c["concepts"]
    out.append((card, audit))

clean = [a for a, _ in out]
audit = [b for _, b in out]
json.dump(clean, open("cards_m56.json", "w"), ensure_ascii=False, indent=1)
json.dump(audit, open("cards_m56_audit.json", "w"), ensure_ascii=False, indent=1)

C = collections.Counter
print("cards:", len(clean), dict(C(c["type"] for c in clean)))
print("by mod:", dict(C(c["mod"] for c in clean)))
print("by topic:", dict(C(c["topic"] for c in clean)))
print("combo answers:", dict(C(c["choices"][c["answerIndex"]] for c in clean if c["type"] == "combo")))
print("combo answer positions:", dict(C(c["answerIndex"] for c in clean if c["type"] == "combo")))
print("mc positions:", dict(C(c["answerIndex"] for c in clean if c["type"] == "mc")))
print("tf answers:", dict(C(c["answer"] for c in clean if c["type"] == "tf")))
print("points:", dict(C(c["points"] for c in clean)))
dg = C(c["diagram"] for c in clean if c.get("diagram"))
print("diagram cards:", sum(dg.values()), "| per diagram:", dict(sorted(dg.items())))
print("diagrams never used:", [k for k in diagrams if k not in dg])

# MC: is the key systematically the longest option?
mcs = [c for c in clean if c["type"] == "mc"]
longest = sum(1 for c in mcs if len(c["options"][c["answerIndex"]]) == max(len(o) for o in c["options"]))
shortest = sum(1 for c in mcs if len(c["options"][c["answerIndex"]]) == min(len(o) for o in c["options"]))
print(f"mc key is the longest option in {longest}/{len(mcs)}, shortest in {shortest}/{len(mcs)}")
for c in mcs:
    L = [len(o) for o in c["options"]]
    k = L[c["answerIndex"]]
    others = sorted(L[:c["answerIndex"]] + L[c["answerIndex"] + 1:])
    if k > others[-1] + 8:
        print(f"   key much longer than all distractors ({k} vs max {others[-1]}): {c['stem'][:70]}")

# TF: do hedge / absolute words predict the answer?
HEDGE = r"\b(can|could|may|might|likely|usually|often|some)\b"
ABS = r"\b(only|always|never|all|every|must|cannot|can't|no)\b"
for name, pat in (("hedge", HEDGE), ("absolute", ABS)):
    cnt = C(c["answer"] for c in clean if c["type"] == "tf" and re.search(pat, c["claim"], re.I))
    print(f"tf claims with {name} words: {dict(cnt)}")

# concept coverage (Module 5-6 concepts must each be tested at least twice)
use = C(k for a in audit for k in a["concepts"])
low = []
for cat, slugs in ledger.items():
    if cat.startswith("bridge"):
        continue
    for s in slugs:
        if use[s] < 2:
            low.append(f"{s} ({use[s]})")
print(f"Module 5-6 concepts: {sum(len(v) for k, v in ledger.items() if not k.startswith('bridge'))}; under-tested: {low or 'none'}")
print("bridge slugs used:", sorted(s for s in ledger['bridge_links_m1to4'] if use[s]))
by_mod_links = C()
for a in audit:
    if a["mod"] == 0:
        mods = {k[:2] for k in a["concepts"] if k[:2] in ("m1", "m2", "m3", "m4")}
        for m in mods:
            by_mod_links[m] += 1
print("bridge cards touching each earlier module:", dict(sorted(by_mod_links.items())))
