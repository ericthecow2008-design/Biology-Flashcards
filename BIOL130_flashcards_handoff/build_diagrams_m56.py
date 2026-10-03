"""Assemble Module 5-6 diagrams from part files, validate, write a JSON.

Usage:  python3 build_diagrams_m56.py OUT.json part_module [part_module ...]
  e.g.  python3 build_diagrams_m56.py diagrams_m56_a.json diagrams_m56_a
        python3 build_diagrams_m56.py diagrams_m56.json diagrams_m56_a diagrams_m56_b diagrams_m56_c

Each part module defines functions returning (title, svg) and a dict ALL = {key: fn}.
Checks: well-formed XML, svg head (viewBox/role/aria-label), no script/style/image/
foreignObject, palette tokens only, no duplicate attributes, width <= 640, every
url(#id) resolves inside the same svg, marker ids unique across ALL existing
diagrams (Modules 1-4) and across the new parts, keys don't clash with existing keys.
"""
import json, re, sys, importlib
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(2)
out_path, parts = sys.argv[1], sys.argv[2:]

out = {}
for p in parts:
    mod = importlib.import_module(p)
    for key, fn in mod.ALL.items():
        assert key not in out, f"duplicate key {key}"
        title, svg = fn()
        out[key] = {"title": title, "svg": svg}

ALLOWED = {'--accent', '--bg', '--border', '--bridge', '--ink-faint', '--ink-soft', '--mod1', '--mod2', '--review',
           '--visual', '--surface', '--ink', '--good'}
existing = {**json.load(open("diagrams_m12.json")), **json.load(open("diagrams_m34.json"))}  # Modules 1-4
issues = []
for k in out:
    if k in existing:
        issues.append(f"key {k!r} already used by a Module 1-4 diagram")
marker_owner = {}
for src, dset in (("m1-4", existing), ("new", out)):
    for k, e in dset.items():
        for mid in re.findall(r'<marker id="([^"]+)"', e["svg"]):
            if mid in marker_owner:
                issues.append(f"marker id {mid!r} used by both {marker_owner[mid]} and {k}")
            marker_owner[mid] = k
for k, e in out.items():
    s = e["svg"]
    try:
        ET.fromstring(s)
    except ET.ParseError as ex:
        issues.append(f"{k}: XML {ex}")
        continue
    if not re.match(r'^<svg viewBox="0 0 [\d.]+ [\d.]+" role="img" aria-label="', s):
        issues.append(f"{k}: svg head/viewBox/role/aria-label")
    for f in ("<script", "<foreignObject", "<image", "<style"):
        if f in s:
            issues.append(f"{k}: forbidden {f}")
    for m in re.finditer(r'var\((--[a-zA-Z0-9-]+)\)', s):
        if m.group(1) not in ALLOWED:
            issues.append(f"{k}: var {m.group(1)}")
    for tag in re.findall(r'<[a-z]+\b[^>]*>', s):
        attrs = re.findall(r'\s([\w:-]+)="', tag)
        if len(attrs) != len(set(attrs)):
            issues.append(f"{k}: duplicate attribute in {tag[:70]}")
    w = float(re.match(r'^<svg viewBox="0 0 ([\d.]+)', s).group(1))
    if w > 640:
        issues.append(f"{k}: width {w} > 640")
    for mid in re.findall(r'url\(#([^)]+)\)', s):
        if f'id="{mid}"' not in s:
            issues.append(f"{k}: references missing #{mid}")
    for m in re.finditer(r'font-size="([\d.]+)"', s):
        if float(m.group(1)) < 8.5:
            issues.append(f"{k}: font-size {m.group(1)} < 8.5 (too small to read on a phone)")
            break
json.dump(out, open(out_path, "w"), ensure_ascii=False)
print(f"{len(out)} diagrams from {parts} -> {out_path}; issues: {len(issues)}")
for i in issues:
    print("  -", i)
sys.exit(1 if issues else 0)
