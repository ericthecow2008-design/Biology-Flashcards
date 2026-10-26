"""Add the Modules 6-8 cards to Eric's study page, keeping everything already on it.

Usage (from the kit folder):
    python3 tools/update_page.py PATH_TO_LIVE_PAGE.html            (first publish of this set)
    python3 tools/update_page.py PATH_TO_LIVE_PAGE.html --replace  (republishing after fixes: every card
                                                                     in this set's id ranges, 3101-3999, is
                                                                     taken off the page and the current set
                                                                     goes on; the set's diagrams likewise)
PATH_TO_LIVE_PAGE.html is the page as the Artifact tool's read action saved it (the publish-time wrapper
is stripped here). Only if you cannot read the live page, use ref/live_page.html: it is the live page
as of version 1792277057-6c39 (Oct 17), which is only right if nobody has published since.

What changes: the new cards (work/cards_m68.json; case-study cards carry caseStudy: true) and their
diagrams are appended;
Modules 7 and 8 get pills, colours and labels the way Modules 1-6 have them; the page title and the
credit line say "Modules 1-8"; the intro's Case studies note covers the new modules. Nothing else.
Writes outputs/biol130-flashcards.html (publish this file) plus outputs/page_cards.json and
outputs/page_diagrams.json, which tools/page_test.js reads.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *a: os.path.join(ROOT, *a)

SET_IDS = (3101, 3999)   # this set's id ranges: 보기 3101-3299, matching 3301-3399, T/F 3401-3699, MC 3701-3999

# light / dark colours for modules the page doesn't have yet (contrast checked against both themes)
NEW_MODULE_COLORS = {
    7: {"light": ("#A62639", "#F6DFE2"), "dark": ("#F08A98", "#3A1E24")},
    8: {"light": ("#7E5426", "#F1E6D6"), "dark": ("#D9B07A", "#33281A")},
}


def die(msg):
    sys.exit("update_page.py: " + msg)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    replace = "--replace" in sys.argv
    src_path = args[0] if args else die("give the path of the live page as read from the artifact")
    src = open(src_path, encoding="utf-8").read()
    try:
        start = src.index("<title>BIOL 130 Flashcards</title>")
        end = src.rindex("</script>") + len("</script>")
    except ValueError:
        die("this doesn't look like the BIOL 130 study page")
    page = src[start:end] + "\n"
    dec = json.JSONDecoder()

    def span(name):
        hits = [m for m in re.finditer(r"const " + name + r" = ", page)]
        if len(hits) != 1:
            die(f"expected one 'const {name} = ' in the page, found {len(hits)}")
        obj, n = dec.raw_decode(page[hits[0].end():])
        return hits[0].end(), hits[0].end() + n, obj

    c0, c1, cards = span("CARDS")
    d0, d1, diagrams = span("DIAGRAMS")
    batch = json.load(open(R("work", "cards_m68.json"), encoding="utf-8"))
    new_d_all = json.load(open(R("work", "diagrams_m68.json"), encoding="utf-8")) if os.path.exists(R("work", "diagrams_m68.json")) else {}
    in_set = lambda i: SET_IDS[0] <= i <= SET_IDS[1]
    already = sorted(c["id"] for c in cards if in_set(c["id"]))
    if already and not replace:
        die(f"{len(already)} cards in this set's id range (ids {already[:5]}...) are already on this page, so it was "
            "published with them before. If you are republishing after fixes, run again with --replace.")
    if any(not in_set(c["id"]) for c in batch):
        die("work/cards_m68.json has ids outside 3101-3999; rebuild it with tools/build_cards.py")
    used = {c["diagram"] for c in batch if c.get("diagram")}
    new_d = {k: v for k, v in new_d_all.items() if k in used}
    clash = set(new_d) & set(diagrams)
    if clash and not replace:
        die(f"diagram keys already on the page: {sorted(clash)} (republishing after fixes? use --replace)")
    missing = sorted(used - set(diagrams) - set(new_d))
    if missing:
        die(f"cards use diagrams that don't exist: {missing}")
    # (with --replace, cards from an earlier publish of this set go, including any since deleted)
    all_cards = [c for c in cards if not in_set(c["id"])] + batch
    for k in new_d:
        diagrams.pop(k, None)
    # diagrams an earlier publish of this set added that no card uses any more
    original = json.load(open(R("ref", "live_diagrams.json"), encoding="utf-8"))
    still_used = {c.get("diagram") for c in all_cards}
    stale = sorted(k for k in diagrams if k not in original and k not in still_used and k not in new_d)
    if replace:
        for k in stale:
            diagrams.pop(k)
    page_mods = sorted({c["mod"] for c in all_cards if c["mod"] > 0})

    def js(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</script", "<\\/script")

    assert c1 < d0
    page = page[:d0] + js({**diagrams, **new_d}) + page[d1:]
    page = page[:c0] + js(all_cards) + page[c1:]

    def sub(old, new, count=1):
        nonlocal page
        k = page.count(old)
        if k != count:
            die(f"expected {count}x, found {k}: {old[:90]!r}")
        page = page.replace(old, new)

    # ---- modules the page doesn't know yet (7, 8) ----
    label = re.search(r"const MOD_LABEL = \{([^}]*)\};", page)
    known = {int(k) for k in re.findall(r"(\d+):", label.group(1))}
    for m in [m for m in page_mods if m not in known]:
        if m not in NEW_MODULE_COLORS:
            die(f"no colours defined for Module {m}")
        prev = max(k for k in known if k > 0)
        (lc, lbg), (dc, dbg) = NEW_MODULE_COLORS[m]["light"], NEW_MODULE_COLORS[m]["dark"]
        toks = list(re.finditer(rf"--mod{prev}:(#[0-9A-Fa-f]{{6}}); --mod{prev}-bg:(#[0-9A-Fa-f]{{6}});", page))
        if len(toks) != 3:
            die(f"expected the Module {prev} colour tokens 3 times (light, dark, dark), found {len(toks)}")
        light_color = toks[0].group(1)
        for t in reversed(toks):
            add = f" --mod{m}:{lc}; --mod{m}-bg:{lbg};" if t.group(1) == light_color else f" --mod{m}:{dc}; --mod{m}-bg:{dbg};"
            page = page[:t.end()] + add + page[t.end():]
        pill = f".pill.mod{prev}.active{{background:var(--mod{prev}); border-color:var(--mod{prev}); color:var(--surface);}}"
        sub(pill, pill + f"\n  .pill.mod{m}.active{{background:var(--mod{m}); border-color:var(--mod{m}); color:var(--surface);}}")
        tag = f".tag.m{prev}{{background:var(--mod{prev}-bg); color:var(--mod{prev});}}"
        sub(tag, tag + f"\n  .tag.m{m}{{background:var(--mod{m}-bg); color:var(--mod{m});}}")
        sub(f'{prev}:"Mod {prev}"}};', f'{prev}:"Mod {prev}", {m}:"Mod {m}"}};')
        sub(f'{prev}:"m{prev}"}};', f'{prev}:"m{prev}", {m}:"m{m}"}};')
        mods_line = f"    {{key:{prev}, label:'Module {prev}', cls:'mod{prev}'}},\n"
        sub(mods_line, mods_line + f"    {{key:{m}, label:'Module {m}', cls:'mod{m}'}},\n")
        known.add(m)

    # ---- titles ----
    top = max(page_mods)
    page, k1 = re.subn(r"<h1>Modules 1–\d+ Flashcards</h1>", f"<h1>Modules 1–{top} Flashcards</h1>", page)
    page, k2 = re.subn(r"lecture notes, Modules 1–\d+ \(Fall 2026\)", f"lecture notes, Modules 1–{top} (Fall 2026)", page)
    case_mods = sorted({c["mod"] for c in all_cards if c.get("caseStudy")})
    page, k3 = re.subn(r"for the real-case 보기 questions on Modules 1–\d+\.", f"for the real-case 보기 questions on Modules 1–{max(case_mods)}.", page)
    if (k1, k2, k3) != (1, 1, 1):
        die(f"title, credit or intro line not found where expected ({k1}, {k2}, {k3})")

    os.makedirs(R("outputs"), exist_ok=True)
    open(R("outputs", "biol130-flashcards.html"), "w", encoding="utf-8").write(page)
    json.dump(all_cards, open(R("outputs", "page_cards.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({**diagrams, **new_d}, open(R("outputs", "page_diagrams.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"wrote outputs/biol130-flashcards.html ({len(page) // 1024} KB): {len(all_cards)} cards "
          f"({len(batch)} from this set{', replacing ' + str(len(already)) + ' already there' if already else ''}), "
          f"{'removed ' + str(len(stale)) + ' unused diagram(s) from an earlier publish, ' if replace and stale else ''}"
          f"{len(diagrams) + len(new_d)} diagrams ({len(new_d)} from this set), modules {page_mods}, "
          f"{sum(1 for c in all_cards if c.get('caseStudy'))} case studies")


if __name__ == "__main__":
    main()
