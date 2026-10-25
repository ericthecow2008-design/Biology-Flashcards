"""Check outputs/BIOL130_Modules6-8.apkg before it goes to Eric.

Usage (from the kit folder):  python3 tools/verify_apkg.py
Package checks: one deck "BIOL 130::Modules 6-8" holding exactly the cards in work/cards_m68.json;
note types identical to Eric's (ref/note_types.json); no id or GUID shared with any card already on
the study page; every note that should carry a diagram does.
Anki-engine checks (the real importer, pip package "anki"): a fresh import gives every card in the
deck and each renders with its diagram on the question side; importing next to Eric's existing
Modules 3-6 deck leaves that deck untouched and adds exactly the new notes.
"""
import json, os, sqlite3, sys, tempfile, zipfile
import genanki

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *a: os.path.join(ROOT, *a)
NEW = R("outputs", "BIOL130_Modules6-8.apkg")
DECK = "BIOL 130::Modules 6-8"
EXISTING = [R("ref", "BIOL130_Modules3-6.apkg")]

fails = []


def check(ok, msg):
    print(("OK   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def load(path):
    d = tempfile.mkdtemp()
    z = zipfile.ZipFile(path)
    name = "collection.anki21" if "collection.anki21" in z.namelist() else "collection.anki2"
    z.extract(name, d)
    con = sqlite3.connect(os.path.join(d, name))
    models = json.loads(con.execute("select models from col").fetchone()[0])
    decks = json.loads(con.execute("select decks from col").fetchone()[0])
    notes = con.execute("select guid, mid, flds, tags from notes").fetchall()
    cards = con.execute("select id, nid, did from cards").fetchall()
    return {"models": models, "decks": decks, "notes": notes, "cards": cards}


batch = json.load(open(R("work", "cards_m68.json"), encoding="utf-8"))
live = json.load(open(R("ref", "live_cards.json"), encoding="utf-8"))
ref_types = json.load(open(R("ref", "note_types.json"), encoding="utf-8"))
n = load(NEW)

check({v["name"] for v in n["decks"].values()} == {"Default", DECK}, f"deck: {sorted(v['name'] for v in n['decks'].values())}")
check(len(n["notes"]) == len(batch) == len(n["cards"]), f"{len(n['notes'])} notes and {len(n['cards'])} cards for {len(batch)} cards in work/cards_m68.json")
same_types = all(mid in ref_types and m["name"] == ref_types[mid]["name"]
                 and [f["name"] for f in m["flds"]] == ref_types[mid]["fields"]
                 and [{"name": t["name"], "qfmt": t["qfmt"], "afmt": t["afmt"]} for t in m["tmpls"]] == ref_types[mid]["templates"]
                 and m["css"] == ref_types[mid]["css"] for mid, m in n["models"].items())
check(same_types, "note types identical to Eric's (" + ", ".join(sorted(m["name"] for m in n["models"].values())) + ")")
live_ids = {c["id"] for c in live}
check(not (live_ids & {c["id"] for c in batch}), "no card id is already used on the study page")
live_guids = {genanki.guid_for(f"biol130-card-v4-{c['type']}-{c['id']}") for c in live}
check(not (live_guids & {g for g, _, _, _ in n["notes"]}), "no GUID collides with a card already on the study page")
want_svg = {genanki.guid_for(f"biol130-card-v4-{c['type']}-{c['id']}") for c in batch if c.get("diagram")}
check(all(("<svg" in f) == (g in want_svg) for g, _, f, _ in n["notes"]), f"every note that should carry a diagram does ({len(want_svg)})")

try:
    from anki.collection import Collection  # noqa: E402
    try:
        from anki.collection import ImportAnkiPackageRequest, ImportAnkiPackageOptions
    except ImportError:
        from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportAnkiPackageOptions
except ImportError:
    print("\nWARNING: the Anki engine checks were SKIPPED because the 'anki' package isn't installed "
          "(pip install --break-system-packages anki). Install it and run this again if at all possible; "
          "if it can't be installed here, say so in your report to Eric.")
    print("\nPACKAGE CHECKS PASSED (engine checks skipped)" if not fails else f"\n{len(fails)} FAILURE(S)")
    sys.exit(1 if fails else 0)


def fresh():
    return Collection(os.path.join(tempfile.mkdtemp(), "collection.anki2"))


def imp(col, path):
    col.import_anki_package(ImportAnkiPackageRequest(package_path=path, options=ImportAnkiPackageOptions()))


def counts(col):
    cc = dict(col.db.all("select did, count() from cards group by did"))
    return {d.name: cc.get(d.id, 0) for d in col.decks.all_names_and_ids() if d.name != "Default"}


col = fresh()
imp(col, NEW)
check(counts(col).get(DECK) == len(batch), f"fresh import: {counts(col)}")
bad = []
for cid in col.find_cards(f'"deck:{DECK}"'):
    c = col.get_card(cid)
    q, a = c.question(), c.answer()
    if "{{" in q + a or len(a) <= len(q) or ("<svg" not in q and c.note().guid in want_svg):
        bad.append(cid)
check(not bad, "every card renders through Anki's template engine, with its diagram on the question side")
col.close()

col = fresh()
for p in EXISTING:
    imp(col, p)
before, notes_before = counts(col), col.note_count()
imp(col, NEW)
after = counts(col)
check(all(after.get(k) == v for k, v in before.items()) and after.get(DECK) == len(batch)
      and col.note_count() == notes_before + len(batch),
      f"next to Eric's Modules 3-6 deck: {after} (notes {notes_before} -> {col.note_count()})")
col.close()
print("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
