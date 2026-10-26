"""Assemble the Modules 6-8 set from every work/cards_*.py file and check it.

Usage (from the kit folder):  python3 tools/build_cards.py [--allow-missing-diagrams] [--only PART]
  --only m7   checks just work/cards_m7.py (any file whose name contains "m7") and prints its report,
              without writing the set files: use it while one part is being written.

Checks every card (module, topic name, concept tags in work/concept_ledger_m68.json, diagram exists,
no title or claim repeated, no card repeating one already on the study page) and stops on ERRORs.
The ledger has sections "module_6", "module_7", "module_8" and "earlier_modules" (concepts from
Modules 1-5 that bridge cards use); a bridge card's tags must span at least two sections.
Then it:
- sorts the cards by module and topic and assigns ids by format:
  보기 combination 3101-3299, matching 3301-3399, true/false 3401-3699, multiple choice 3701-3999;
- relabels each 보기 card's statements ㄱ/ㄴ/ㄷ so answer patterns are balanced, and draws its five
  choices so the key's position is spread evenly over ①-⑤ (case-study cards get caseStudy: true);
- places each multiple-choice key so positions ①-⑤ are used evenly (unless the card is ordered=True);
- prints the coverage audit (every Module 7 and 8 concept should be tested by at least 2 cards),
  the format mix per module, true/false balance, wording-cue checks and possible near-duplicates.
Fix every ERROR and WARNING before review. Writes work/cards_m68.json (what the outputs are built from)
and work/cards_m68_audit.json (the same plus each card's concept tags).
"""
import collections, glob, hashlib, importlib.util, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "work")]
W = lambda *a: os.path.join(ROOT, "work", *a)

ID_RANGES = {"combo": (3101, 3299), "match": (3301, 3399), "tf": (3401, 3699), "mc": (3701, 3999)}
LAB = ["ㄱ", "ㄴ", "ㄷ"]
CANON = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
ONE_TRUE = ["ㄴ", "ㄷ", "ㄱ", "ㄷ", "ㄴ", "ㄱ", "ㄷ", "ㄴ"]
TWO_TRUE = ["ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ"]
MOD_ORDER = [6, 7, 8, 0]
TYPE_ORDER = ["combo", "match", "tf", "mc"]
# Module 6 topics are the ones its cards already use on the study page; Modules 7-8 follow the notes'
# section headings. Reuse these exact names so the study page's topic menu stays tidy.
TOPICS = {
    6: ["Energy & Metabolism", "ATP & Energetic Coupling", "Thermodynamics & Free Energy", "Enzymes & Their Regulation"],
    7: ["Overview of Cellular Respiration", "Glycolysis", "Pyruvate Oxidation & Citric Acid Cycle",
        "Oxidative Phosphorylation", "Anaerobic Conditions & Fermentation", "Metabolic Integration"],
    8: ["Overview of Photosynthesis", "Pigments & Light Absorption", "Photosystems & Electron Transport", "Calvin Cycle"],
    0: ["Connecting Modules 1–8"],
}
FULL_SET_MODULES = ("module_7", "module_8")   # ledger sections where every concept needs >= 2 cards
HEDGES = re.compile(r"\b(can|could|may|might|likely|possibly|tends? to)\b", re.I)
ABSOLUTES = re.compile(r"\b(must|only|always|never|all|every|just as|cannot|can't)\b", re.I)
STOP = set("a an the of to in on and or is are be by for with as at it its this that from into than then not no "
           "which what when would will can could does do".split())


def plan_positions(need):
    """How many cards of each 보기 key go at each choice position ①-⑤ (0-4), as evenly as the keys allow."""
    # choices are listed in CANON order, so a key can only sit where enough smaller and larger
    # choices exist: ㄱ only at ①, ㄱ, ㄴ, ㄷ only at ⑤, the rest in a window of 2-3 positions
    feas = {k: list(range(max(0, CANON.index(k) - 2), min(4, CANON.index(k)) + 1)) for k in need}
    kinds = sorted(need, key=CANON.index)
    cnt = {k: collections.Counter() for k in kinds}
    tot = collections.Counter()
    for k in sorted(kinds, key=lambda k: (len(feas[k]), CANON.index(k))):   # greedy start, most constrained first
        for _ in range(need[k]):
            p = min(feas[k], key=lambda q: (tot[q], q))
            cnt[k][p] += 1
            tot[p] += 1
    # then even it out: while some position holds 2+ more keys than another position it can reach
    # (by moving one card along a chain of positions its key allows), move it. This ends at the most
    # even spread the keys allow.
    while True:
        moved = False
        for src in sorted(range(5), key=lambda p: (-tot[p], p)):
            prev, queue, target = {src: None}, [src], None
            while queue:
                p = queue.pop(0)
                if p != src and tot[p] <= tot[src] - 2:
                    target = p
                    break
                for k in kinds:
                    if cnt[k][p] > 0:
                        for r in feas[k]:
                            if r not in prev:
                                prev[r] = (p, k)
                                queue.append(r)
            if target is not None:
                r = target
                while prev[r] is not None:
                    p, k = prev[r]
                    cnt[k][p] -= 1
                    cnt[k][r] += 1
                    r = p
                tot[src] -= 1
                tot[target] += 1
                moved = True
                break
        if not moved:
            break
    return cnt


def seed(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:12], 16)


def words(s):
    return {w for w in re.findall(r"[a-z0-9']+", re.sub(r"<[^>]+>", " ", s.lower())) if w not in STOP and len(w) > 2}


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def text_of(c):
    if c["type"] == "combo":
        return c["stem"] + " " + c["box"] + " " + " ".join(s["text"] for s in c["statements"])
    if c["type"] == "tf":
        return c.get("box", "") + " " + c["claim"]
    if c["type"] == "mc":
        return c["stem"] + " " + " ".join(c["options"])
    return c.get("prompt", "") + " " + " ".join(p["left"] + " " + p["right"] for p in c["pairs"])


def label(c):
    return c.get("title") or (c.get("claim") or c.get("stem", ""))[:60]


def load_cards(only=None):
    files = sorted(glob.glob(W("cards_*.py")))
    if only:
        files = [f for f in files if only in os.path.basename(f)]
    if not files:
        sys.exit("no matching work/cards_*.py files")
    raw = []
    for fn in files:
        spec = importlib.util.spec_from_file_location(os.path.basename(fn)[:-3], fn)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for c in mod.CARDS:
            c["_file"] = os.path.basename(fn)
            raw.append(c)
    return raw, files


def main():
    allow_missing = "--allow-missing-diagrams" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    raw, files = load_cards(only)
    ledger_tree = json.load(open(W("concept_ledger_m68.json"), encoding="utf-8"))
    ledger = {}
    section_of = {}
    for sec, items in ledger_tree.items():
        for k, v in (items.items() if isinstance(items, dict) else []):
            ledger[k] = v
            section_of[k] = sec
    live_cards = json.load(open(os.path.join(ROOT, "ref", "live_cards.json"), encoding="utf-8"))
    live_diagrams = json.load(open(os.path.join(ROOT, "ref", "live_diagrams.json"), encoding="utf-8"))
    new_diagrams = json.load(open(W("diagrams_m68.json"), encoding="utf-8")) if os.path.exists(W("diagrams_m68.json")) else {}
    live_titles = {c.get("title") for c in live_cards if c.get("title")}

    errors = []
    for c in raw:
        t = f"[{c['_file']}] {label(c)}"
        if c.get("mod") not in TOPICS:
            errors.append(f"{t}: mod must be 6, 7, 8 or 0 (bridge); wrap each list in with_mod()")
            continue
        if c["topic"] not in TOPICS[c["mod"]]:
            errors.append(f"{t}: topic {c['topic']!r} is not one of {TOPICS[c['mod']]}")
        if not c["concepts"]:
            errors.append(f"{t}: no concept tags")
        for k in c["concepts"]:
            if k not in ledger:
                errors.append(f"{t}: unknown concept slug {k!r} (add it to work/concept_ledger_m68.json or fix the spelling)")
        if len(set(c["concepts"])) != len(c["concepts"]):
            errors.append(f"{t}: duplicate concept tag")
        if c["mod"] == 0:
            secs = {section_of.get(k) for k in c["concepts"] if k in section_of}
            if len(secs) < 2:
                errors.append(f"{t}: a bridge card needs tags from at least two ledger sections "
                              "(e.g. module_7 and earlier_modules)")
        d = c.get("diagram")
        if d and d not in new_diagrams and d not in live_diagrams and not allow_missing:
            errors.append(f"{t}: diagram {d!r} not found (run tools/build_diagrams.py first)")
        if c["type"] == "combo":
            if c.get("case") and not d:
                errors.append(f"{t}: a case-study card needs a diagram")
            if "<보기>" not in c["stem"]:
                errors.append(f"{t}: a 보기 stem ends with '...which statements in <보기> are correct?'")
        if c["type"] == "tf" and not c.get("box"):
            errors.append(f"{t}: every true/false card has a short scenario box")
        if c["type"] == "match":
            lefts = [p["left"] for p in c["pairs"]]
            rights = [p["right"] for p in c["pairs"]]
            if len(set(lefts)) != len(lefts) or len(set(rights)) != len(rights):
                errors.append(f"{t}: matching items must be unique on each side")
        if c.get("title") and c["title"] in live_titles:
            errors.append(f"{t}: title already used by a card on the study page")
        blob = json.dumps({k: v for k, v in c.items() if k not in ("_file", "concepts")}, ensure_ascii=False)
        if "  " in blob or re.search(r"[“”‘’]", blob):
            errors.append(f"{t}: no double spaces or curly quotes")
        if re.search(r"(?i)\b(all|none) of the above\b", blob):
            errors.append(f"{t}: no 'all/none of the above'")
    for kind, key in (("title", lambda c: c.get("title")), ("claim", lambda c: c.get("claim")), ("stem", lambda c: c.get("stem") if c["type"] == "mc" else None)):
        dup = [v for v, n in collections.Counter(key(c) for c in raw if key(c)).items() if n > 1]
        if dup:
            errors.append(f"repeated {kind}s: {dup[:5]}")
    if errors:
        print("\n".join("ERROR " + e for e in errors))
        print(f"\n{len(errors)} error(s): fix them and run again")
        sys.exit(1)

    raw.sort(key=lambda c: (MOD_ORDER.index(c["mod"]), TOPICS[c["mod"]].index(c["topic"]), TYPE_ORDER.index(c["type"])))
    next_id = {t: lo for t, (lo, hi) in ID_RANGES.items()}
    out = []
    for c in raw:
        cid = next_id[c["type"]]
        if cid > ID_RANGES[c["type"]][1]:
            sys.exit(f"too many {c['type']} cards for the id range {ID_RANGES[c['type']]}")
        next_id[c["type"]] += 1
        base = {"id": cid, "type": c["type"], "mod": c["mod"], "topic": c["topic"], "points": c["points"]}
        if c["type"] == "combo":
            card = dict(base, title=c["title"], stem=c["stem"], box=c["box"], statements=c["statements"],
                        choices=None, answerIndex=None, links=c["links"])
        elif c["type"] == "tf":
            card = dict(base, box=c["box"], claim=c["claim"], answer=c["answer"], explanation=c["explanation"], links=c["links"])
        elif c["type"] == "mc":
            card = dict(base, stem=c["stem"], options=c["options"], answerIndex=c["options"].index(c["key"]),
                        explanation=c["explanation"], links=c["links"], _ordered=c["ordered"])
        else:
            card = dict(base, title=c["title"], prompt=c["prompt"], leftLabel=c["leftLabel"], rightLabel=c["rightLabel"],
                        pairs=c["pairs"], explanation=c["explanation"], links=c["links"])
        if c.get("diagram"):
            card["diagram"] = c["diagram"]
        if c["type"] == "combo" and c.get("case"):
            card["caseStudy"] = True
        out.append([card, c["concepts"]])

    # ---- 보기 cards: statement order, then choices with the key spread over ①-⑤ ----
    combos = [card for card, _ in out if card["type"] == "combo"]
    i1 = i2 = 0
    for card in combos:
        sts = card["statements"]
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
        for pos, s in zip([p for p in range(3) if p not in want], falses):
            slots[pos] = s
        card["statements"] = [{"label": LAB[i], "text": s["text"], "correct": s["correct"], "explanation": s["explanation"]}
                              for i, s in enumerate(slots)]
    keys = [", ".join(s["label"] for s in c["statements"] if s["correct"]) for c in combos]
    if combos:
        need = collections.Counter(keys)
        cnt = plan_positions(need)
        kinds = sorted(need, key=CANON.index)
        plan = {k: [p for p in sorted(cnt[k]) for _ in range(cnt[k][p])] for k in kinds}
        for k in plan:
            random.Random(seed("m68-positions-" + k)).shuffle(plan[k])
        for card, k in zip(combos, keys):
            pos = plan[k].pop()
            kidx = CANON.index(k)
            rnd = random.Random(seed("m68-choices-" + card["title"]))
            picked = set(rnd.sample(CANON[:kidx], pos)) | set(rnd.sample(CANON[kidx + 1:], 4 - pos)) | {k}
            card["choices"] = [x for x in CANON if x in picked]
            card["answerIndex"] = card["choices"].index(k)
            assert card["answerIndex"] == pos

    # ---- multiple choice: key positions spread evenly ----
    mcs = [card for card, _ in out if card["type"] == "mc" and not card["_ordered"]]
    positions = []
    while len(positions) < len(mcs):
        block = list(range(5))
        random.Random(seed(f"m68-mc-block-{len(positions)}")).shuffle(block)
        positions += block
    for card, pos in zip(mcs, positions):
        key = card["options"][card["answerIndex"]]
        rest = [o for o in card["options"] if o != key]
        random.Random(seed("m68-mc-" + card["stem"])).shuffle(rest)
        rest.insert(pos, key)
        card["options"], card["answerIndex"] = rest, pos
    for card, _ in out:
        card.pop("_ordered", None)

    clean = [card for card, _ in out]
    audit = [dict(card, concepts=concepts) for card, concepts in out]
    if not only:
        json.dump(clean, open(W("cards_m68.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(audit, open(W("cards_m68_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---------------------------------------------------------------- report
    C = collections.Counter
    warn = []
    print(f"{len(clean)} cards from {len(files)} file(s)")
    print("module | 보기 (case) | matching | T/F | MC | total | with diagram")
    for m in MOD_ORDER:
        cs = [c for c in clean if c["mod"] == m]
        if not cs:
            continue
        n = C(c["type"] for c in cs)
        ncase = sum(1 for c in cs if c.get("caseStudy"))
        nd = sum(1 for c in cs if c.get("diagram"))
        print(f"  {('Bridge' if m == 0 else 'Mod ' + str(m)):7}| {n['combo']:3} ({ncase}) | {n['match']:8} | {n['tf']:3} | {n['mc']:3} | {len(cs):5} | {nd} ({round(100 * nd / len(cs))}%)")
    for t, (lo, hi) in ID_RANGES.items():
        ids = [c["id"] for c in clean if c["type"] == t]
        if ids:
            print(f"  ids {t}: {min(ids)}-{max(ids)}")

    cov = C(k for _, concepts in out for k in concepts)
    for sec in ledger_tree:
        slugs = list(ledger_tree[sec]) if isinstance(ledger_tree[sec], dict) else []
        thin = [k for k in slugs if cov[k] < 2]
        tested = sum(1 for k in slugs if cov[k] >= 1)
        print(f"coverage {sec}: {tested}/{len(slugs)} concepts tested, {len(slugs) - len(thin)} by 2+ cards")
        if sec in FULL_SET_MODULES and thin and not only:   # (a part check can't judge whole-module coverage)
            warn.append(f"{sec}: {len(thin)} concept(s) tested by fewer than 2 cards: " + ", ".join(f"{k}({cov[k]})" for k in thin))

    if combos:
        print("보기 keys:", dict(C(c["choices"][c["answerIndex"]] for c in combos)),
              "| positions ①-⑤:", [C(c["answerIndex"] for c in combos)[p] for p in range(5)])
        nt = C(sum(s["correct"] for s in c["statements"]) for c in combos)
        print("true statements per 보기 card:", dict(sorted(nt.items())),
              "(the existing deck: about 1 in 4 one-true, 3 in 5 two-true, 1 in 7 all-three-true)")
        pos = [C(c["answerIndex"] for c in combos)[p] for p in range(5)]
        if len(combos) >= 10:
            if nt[3] / len(combos) > 0.2:
                warn.append(f"{nt[3]} of {len(combos)} 보기 cards have all three statements true: 'ㄱ, ㄴ, ㄷ' can only be "
                            "choice ⑤, so too many of them pile keys onto ⑤. Make some of them two-true (about 1 in 7 all-true)")
            if max(pos) - min(pos) > max(2, round(0.25 * len(combos) / 5)):
                warn.append(f"보기 key positions ①-⑤ are uneven {pos}: usually too many all-true cards (only fit ⑤) or "
                            "one-true cards (the builder makes 1 in 4 of them 'ㄱ', which only fits ①); change some true/false mixes")
        one = [c for c in combos if sum(s["correct"] for s in c["statements"]) == 1]
        if one:
            lt = sum(max(c["statements"], key=lambda s: len(s["text"]))["correct"] for c in one)
            print(f"1-true 보기 cards whose true statement is the longest: {lt}/{len(one)} (aim for about a third)")
            if lt > max(1, round(len(one) * 0.45)):
                warn.append("in 1-true 보기 cards the true statement is too often the longest: trim some, lengthen some false ones")
    tfs = [c for c in clean if c["type"] == "tf"]
    if tfs:
        nT = sum(c["answer"] for c in tfs)
        print(f"true/false: {nT} true, {len(tfs) - nT} false")
        if len(tfs) >= 10 and not (0.4 <= nT / len(tfs) <= 0.6):
            warn.append("true/false answers should be roughly half true, half false")
    allmc = [c for c in clean if c["type"] == "mc"]
    if allmc:
        print("multiple-choice key positions ①-⑤:", [C(c["answerIndex"] for c in allmc)[p] for p in range(5)])
        longest = sum(1 for c in allmc if len(c["options"][c["answerIndex"]]) == max(len(o) for o in c["options"]))
        print(f"multiple-choice keys that are the longest option: {longest}/{len(allmc)} (aim for about a fifth)")
        if len(allmc) >= 10 and longest / len(allmc) > 0.35:
            warn.append("multiple-choice keys are too often the longest option")

    def rate(items, rx):
        return sum(bool(rx.search(x)) for x in items), len(items)
    st_t = [s["text"] for c in combos for s in c["statements"] if s["correct"]] + [c["claim"] for c in tfs if c["answer"]]
    st_f = [s["text"] for c in combos for s in c["statements"] if not s["correct"]] + [c["claim"] for c in tfs if not c["answer"]]
    (ht, nt_), (hf, nf_) = rate(st_t, HEDGES), rate(st_f, HEDGES)
    (at, _), (af, _) = rate(st_t, ABSOLUTES), rate(st_f, ABSOLUTES)
    if nt_ and nf_:
        print(f"hedge words (can/could/may/might/likely) in true vs false statements and claims: {ht}/{nt_} vs {hf}/{nf_}")
        print(f"absolute words (must/only/always/never/all/every/just as/cannot): {at}/{nt_} vs {af}/{nf_}")
        if ht / nt_ - hf / nf_ > 0.2:
            warn.append("hedge words sit mostly in TRUE statements: make some true ones declarative, hedge some false ones")
        if af / nf_ - at / nt_ > 0.2:
            warn.append("absolute words sit mostly in FALSE statements: rephrase some false ones, use some in true ones")

    # possible near-duplicates (within the set, and against the 500+ cards already on the study page)
    mine = [(label(c), words(text_of(c))) for c in clean]
    live = [(f"#{c['id']} {label(c)}", words(text_of(c))) for c in live_cards]
    near = []
    for i in range(len(mine)):
        for j in range(i + 1, len(mine)):
            if jacc(mine[i][1], mine[j][1]) >= 0.55:
                near.append(f"within the set: {mine[i][0]!r} ~ {mine[j][0]!r}")
        for lbl, w in live:
            if jacc(mine[i][1], w) >= 0.5:
                near.append(f"vs study page: {mine[i][0]!r} ~ {lbl!r}")
    if near:
        print(f"possible near-duplicates to look at ({len(near)}):")
        for x in near[:25]:
            print("  " + x)
        if len(near) > 25:
            print(f"  ... and {len(near) - 25} more")
    for w in warn:
        print("WARNING", w)
    if only:
        print(f"checked {', '.join(os.path.basename(f) for f in files)} only (ids are provisional; nothing written)")
    else:
        print("wrote work/cards_m68.json and work/cards_m68_audit.json")


if __name__ == "__main__":
    main()
