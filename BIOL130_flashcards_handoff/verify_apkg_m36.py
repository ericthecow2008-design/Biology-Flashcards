"""Verify BIOL130_Modules3-6.apkg before it goes to Eric.

1. Package checks (sqlite only, always run):
   - the only deck is "BIOL 130::Modules 3-6" and every card is in it
   - the four note types are IDENTICAL to the delivered Modules 3-4 deck
     (reference/BIOL130_Modules3-4.apkg): same ids, names, fields, templates, CSS
   - every Modules 3-4 note is still there with the same GUID, fields and tags
   - one new note per card in cards_m56.json, no duplicate GUIDs
2. Anki-engine checks (run when `import anki` works; `pip install anki` if not):
   - fresh profile: import -> one deck holding every card; one card of each
     note type renders through Anki's own template engine
   - Eric's real situation: the Modules 3-4 deck is already in Anki. Rename it
     to "BIOL 130::Modules 3-6", import the new file -> the new cards join the
     same deck, no duplicates, no cards left anywhere else.
Usage: python3 verify_apkg_m36.py
"""
import json, os, sys, tempfile
from inspect_apkg import load

NEW = "BIOL130_Modules3-6.apkg"
OLD = "reference/BIOL130_Modules3-4.apkg"
DECK = "BIOL 130::Modules 3-6"
OLD_DECK_NAMES = ("BIOL 130::Modules 3-4", "BIOL 130::Modules 3-4 (Suneung + Diagrams)")

def model_sig(m):
    return (m["name"], [f["name"] for f in m["flds"]], [(t["name"], t["qfmt"], t["afmt"]) for t in m["tmpls"]],
            m["css"], m.get("type"), m.get("sortf"))

fails = []
def check(ok, msg):
    print(("OK   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)

n, o = load(NEW), load(OLD)
m56 = json.load(open("cards_m56.json"))
decks = {k: v["name"] for k, v in n["decks"].items()}
check(set(decks.values()) == {"Default", DECK}, f"deck names: {sorted(decks.values())}")
did = [k for k, v in decks.items() if v == DECK]
check(bool(did) and {str(c[0]) for c in n["cards"]} == set(did), "every card is in the Modules 3-6 deck")
check({k: model_sig(v) for k, v in n["models"].items()} == {k: model_sig(v) for k, v in o["models"].items()},
      "note types identical to the delivered Modules 3-4 deck")
nn = {g: (mid, f, t) for g, mid, f, t in n["notes"]}
on = {g: (mid, f, t) for g, mid, f, t in o["notes"]}
check(len(nn) == len(n["notes"]), "no duplicate GUIDs")
check(set(on) <= set(nn), f"all {len(on)} Modules 3-4 notes present (by GUID)")
changed = [g for g in on if g in nn and nn[g] != on[g]]
check(not changed, f"Modules 3-4 notes unchanged (fields, tags, note type): {len(changed)} differ")
check(len(set(nn) - set(on)) == len(m56), f"new notes: {len(set(nn) - set(on))} (cards_m56.json has {len(m56)})")
check(len(n["cards"]) == len(nn), f"one card per note: {len(n['cards'])} cards / {len(nn)} notes")

try:
    from anki.collection import Collection
    try:
        from anki.collection import ImportAnkiPackageRequest, ImportAnkiPackageOptions
    except ImportError:
        from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportAnkiPackageOptions
except ImportError:
    print("\nSKIPPED Anki-engine checks: `pip install anki` (add --break-system-packages if pip asks) and re-run.")
    sys.exit(1 if fails else 0)

def fresh():
    return Collection(os.path.join(tempfile.mkdtemp(), "collection.anki2"))
def imp(col, path):
    col.import_anki_package(ImportAnkiPackageRequest(package_path=os.path.abspath(path), options=ImportAnkiPackageOptions()))
def deck_counts(col):
    counts = dict(col.db.all("select did, count() from cards group by did"))
    return {d.name: counts.get(d.id, 0) for d in col.decks.all_names_and_ids() if d.name != "Default"}

total = len(nn)
col = fresh(); imp(col, NEW); dc = deck_counts(col)
check(dc.get(DECK) == total and col.card_count() == total, f"fresh import: {dc}")
new_guids = set(nn) - set(on)
seen, bad = {}, []
for cid in col.find_cards(f'"deck:{DECK}"'):
    c = col.get_card(cid); note = c.note()
    if note.guid not in new_guids or note.mid in seen:
        continue
    q, a = c.question(), c.answer()
    seen[note.mid] = True
    if not (len(q) > 200 and len(a) > len(q) and "{{" not in q + a):
        bad.append(note.mid)
check(len(seen) == 4 and not bad, f"a new card of each of the 4 note types renders in Anki ({len(seen)} types checked)")
col.close()

col = fresh(); imp(col, OLD)
old_name = next(nm for nm in deck_counts(col) if nm in OLD_DECK_NAMES)
col.decks.rename(col.decks.id_for_name(old_name), DECK)
imp(col, NEW); dc = deck_counts(col)
check(dc.get(DECK) == total and col.note_count() == total and sum(dc.values()) == total,
      f"rename existing deck to '{DECK}', then import: {dc}")
col.close()
print("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
