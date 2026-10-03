import sqlite3, zipfile, json, sys, tempfile, os
def load(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    colname = 'collection.anki21' if 'collection.anki21' in names else 'collection.anki2'
    tmp = tempfile.mkdtemp()
    z.extract(colname, tmp)
    db = sqlite3.connect(os.path.join(tmp, colname))
    decks = json.loads(db.execute("select decks from col").fetchone()[0])
    models = json.loads(db.execute("select models from col").fetchone()[0])
    notes = db.execute("select guid, mid, flds, tags from notes").fetchall()
    cards = db.execute("select c.did, n.guid, c.ord from cards c join notes n on c.nid=n.id").fetchall()
    media = json.loads(z.read('media')) if 'media' in names else {}
    return dict(names=names, decks=decks, models=models, notes=notes, cards=cards, media=media, zip=z)
if __name__ == "__main__":
    info = {}
    for p in sys.argv[1:]:
        d = load(p); info[p] = d
        print(f"== {p}")
        print("   decks:", {k: v['name'] for k, v in d['decks'].items()})
        print("   models:", sorted(v['name'] for v in d['models'].values()))
        print(f"   notes: {len(d['notes'])}  cards: {len(d['cards'])}  media files: {len(d['media'])}  card decks: {sorted(set(c[0] for c in d['cards']))}")
    ps = list(info)
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            a = {n[0] for n in info[ps[i]]['notes']}; b = {n[0] for n in info[ps[j]]['notes']}
            print(f"guid overlap {os.path.basename(ps[i])} x {os.path.basename(ps[j])}: {len(a & b)}")
