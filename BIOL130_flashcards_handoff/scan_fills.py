"""Scan every diagram for elements whose paint won't adapt to dark mode:
  (1) <text> with no fill anywhere up its ancestor chain -> SVG default black
  (2) any hardcoded (non-var, non-currentColor, non-none) fill/stroke colour
  (3) filled shapes with no fill anywhere up the chain -> default black
"""
import json, re, sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
import os
d = json.load(open(os.environ.get("DIAGRAMS", "diagrams.json")))
SHAPES = {"circle", "rect", "ellipse", "polygon", "path", "polyline"}
ADAPTIVE = re.compile(r"^(none|currentColor|var\(--[a-z0-9-]+\)|transparent)$")


def tag(el):
    return el.tag.replace(NS, "")


def walk(el, inherited_fill, out):
    own = el.get("fill")
    style = el.get("style") or ""
    m = re.search(r"fill\s*:\s*([^;]+)", style)
    if m:
        own = m.group(1).strip()
    eff = own if own is not None else inherited_fill
    out.append((el, own, eff))
    for ch in el:
        walk(ch, eff, out)


totals = {"text_default": 0, "hardcoded": 0, "shape_default": 0}
report = {}
for key, entry in d.items():
    root = ET.fromstring(entry["svg"])
    items = []
    walk(root, None, items)
    probs = []
    for el, own, eff in items:
        t = tag(el)
        if t == "text" and eff is None:
            probs.append(f"text-default-black: {''.join(el.itertext())!r}")
            totals["text_default"] += 1
        if t in SHAPES and eff is None:
            probs.append(f"shape-default-black: <{t}> {dict(el.attrib)}")
            totals["shape_default"] += 1
        for attr in ("fill", "stroke"):
            v = el.get(attr)
            if v is not None and not ADAPTIVE.match(v):
                probs.append(f"hardcoded-{attr}={v} on <{t}> text={''.join(el.itertext())[:30]!r}")
                totals["hardcoded"] += 1
    report[key] = probs

for key, probs in report.items():
    if probs:
        print(f"== {key} ({len(probs)})")
        for p in probs:
            print("   ", p)
print()
print("TOTALS:", totals)
