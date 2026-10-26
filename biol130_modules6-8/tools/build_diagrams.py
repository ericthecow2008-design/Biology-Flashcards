"""Collect the new diagrams from work/diagrams_*.py, validate them, and write work/diagrams_m68.json.

Usage (from the kit folder):  python3 tools/build_diagrams.py [--only PART]
  --only m7   builds and checks just work/diagrams_*m7*.py into work/diagrams_check.json (point the
              other checks at it with DIAGRAMS=work/diagrams_check.json), leaving the set file alone.

Each work/diagrams_*.py file defines functions returning (title, svg) and ends with ALL = {key: function}.
Checks: well-formed XML; <svg viewBox role="img" aria-label>; width at most 640; no script, style,
foreignObject or image; colours are palette variables or currentColor only; every text and filled
shape has an explicit fill (SVG's default black disappears in dark mode); font sizes at least 8.5;
every id starts with its diagram key and is unique across all diagrams (old and new); url(#id)
references resolve inside the same svg; keys don't clash with the study page's existing diagrams;
the title is short and the aria-label says what the picture shows.
Exit code 1 if anything fails.
"""
import glob, importlib.util, json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "work")]
from svgkit import PALETTE  # noqa: E402

OUT = os.path.join(ROOT, "work", "diagrams_m68.json")
existing = json.load(open(os.path.join(ROOT, "ref", "live_diagrams.json"), encoding="utf-8"))

ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
if ONLY:
    OUT = os.path.join(ROOT, "work", "diagrams_check.json")
files = sorted(glob.glob(os.path.join(ROOT, "work", "diagrams_*.py")))
if ONLY:
    files = [f for f in files if ONLY in os.path.basename(f)]
if not files:
    sys.exit("no matching work/diagrams_*.py files")
out, issues = {}, []
for fn in files:
    spec = importlib.util.spec_from_file_location(os.path.basename(fn)[:-3], fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for key, f in mod.ALL.items():
        if key in out:
            issues.append(f"{key}: defined twice")
        title, svgtext = f()
        out[key] = {"title": title, "svg": svgtext}

ALLOWED_VARS = set(PALETTE)


def _ancestors(el, parent):
    out = []
    while el in parent:
        el = parent[el]
        out.append(el)
    return out


COLOR_ATTRS = ("fill", "stroke", "stop-color", "color")
ids_seen = {}
for k, d in existing.items():
    for i in re.findall(r'\bid="([^"]+)"', d["svg"]):
        ids_seen[i] = f"existing diagram {k}"

for key, d in out.items():
    s, t = d["svg"], d["title"]
    where = f"{key}:"
    if key in existing:
        issues.append(f"{where} key already used by a diagram on the study page")
    if not re.fullmatch(r"[a-z0-9_]+", key):
        issues.append(f"{where} keys are lowercase letters, digits and underscores")
    if not (3 <= len(t) <= 90):
        issues.append(f"{where} title should be a short caption (3-90 characters)")
    try:
        root = ET.fromstring(s)
    except ET.ParseError as e:
        issues.append(f"{where} not well-formed XML ({e})")
        continue
    tag = lambda el: el.tag.split("}")[-1]
    if tag(root) != "svg":
        issues.append(f"{where} root element must be <svg>")
    vb = root.get("viewBox", "")
    m = re.fullmatch(r"0 0 ([\d.]+) ([\d.]+)", vb)
    if not m:
        issues.append(f"{where} needs viewBox=\"0 0 W H\"")
    elif float(m.group(1)) > 640:
        issues.append(f"{where} wider than 640")
    if root.get("role") != "img":
        issues.append(f'{where} needs role="img"')
    aria = root.get("aria-label", "")
    if len(aria) < 40:
        issues.append(f"{where} aria-label missing or too short: describe what the picture shows")
    parent = {c: p for p in root.iter() for c in p}

    def inherited(el, attr):
        while el is not None:
            if el.get(attr) is not None:
                return el.get(attr)
            el = parent.get(el)
        return None

    for el in root.iter():
        name = tag(el)
        if name in ("script", "style", "foreignObject", "image"):
            issues.append(f"{where} <{name}> is not allowed")
        in_defs = any(tag(a) in ("defs", "marker") for a in _ancestors(el, parent))
        # SVG paints a missing fill black, which vanishes in dark mode
        if name == "text" and inherited(el, "fill") is None:
            issues.append(f"{where} text \"{(el.text or '')[:30]}\" has no fill")
        if name in ("rect", "circle", "ellipse", "polygon", "path") and not in_defs and inherited(el, "fill") is None:
            issues.append(f"{where} <{name}> has no fill attribute (set fill=\"none\" or a palette colour)")
        for a in COLOR_ATTRS:
            v = el.get(a)
            if v is None or v in ("none", "currentColor", "transparent"):
                continue
            mv = re.fullmatch(r"var\((--[a-z0-9-]+)\)", v)
            if not mv or mv.group(1) not in ALLOWED_VARS:
                issues.append(f"{where} <{name} {a}=\"{v}\"> is not a palette variable")
        if el.get("style"):
            issues.append(f"{where} <{name}> has a style attribute; use plain attributes")
        if name == "text":
            fs = el.get("font-size")
            if fs is None or float(fs) < 8.5:
                issues.append(f"{where} text \"{(el.text or '')[:30]}\" needs font-size >= 8.5")
        i = el.get("id")
        if i:
            if not i.startswith(key):
                issues.append(f'{where} id "{i}" must start with the diagram key')
            if i in ids_seen:
                issues.append(f'{where} id "{i}" already used by {ids_seen[i]}')
            ids_seen[i] = f"new diagram {key}"
    ids_here = set(re.findall(r'\bid="([^"]+)"', s))
    for ref in re.findall(r"url\(#([^)]+)\)", s) + re.findall(r'href="#([^"]+)"', s):
        if ref not in ids_here:
            issues.append(f"{where} url(#{ref}) does not resolve inside this svg")

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(out)} diagrams from {len(files)} file(s) -> work/{os.path.basename(OUT)}; issues: {len(issues)}")
for i in issues:
    print("  ISSUE", i)
sys.exit(1 if issues else 0)
