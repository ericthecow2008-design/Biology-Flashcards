"""Tiny helpers for hand-authored diagram SVGs.

Conventions (shared with the Modules 1-2 diagrams):
  * every <text> gets an explicit fill (default currentColor) -- SVG's own
    default text fill is black, which vanishes in dark mode;
  * colours only via the shared palette tokens (var(--ink-soft), var(--mod1)...);
  * the svg element starts with viewBox (the web artifact and Anki builders
    read the native width from it);
  * marker ids are prefixed per diagram so several diagrams can share a page.
"""
import html as _html
import math


def esc(s):
    return _html.escape(str(s), quote=False)


def aesc(s):
    return _html.escape(str(s), quote=True)


def g(v):
    return f"{v:g}" if isinstance(v, (int, float)) else str(v)


def _paint(fill, stroke, sw, fo, opacity, dash):
    out = f' fill="{fill}"'
    if fo is not None:
        out += f' fill-opacity="{g(fo)}"'
    if stroke:
        out += f' stroke="{stroke}" stroke-width="{g(sw)}"'
    if dash:
        out += f' stroke-dasharray="{dash}"'
    if opacity is not None:
        out += f' opacity="{g(opacity)}"'
    return out


def T(x, y, s, size=10, anchor="middle", weight=None, fill="currentColor", italic=False):
    out = f'<text x="{g(x)}" y="{g(y)}"'
    if anchor and anchor != "start":
        out += f' text-anchor="{anchor}"'
    out += f' font-size="{g(size)}"'
    if weight:
        out += f' font-weight="{weight}"'
    if italic:
        out += ' font-style="italic"'
    return out + f' fill="{fill}">{esc(s)}</text>'


def L(x1, y1, x2, y2, stroke="currentColor", w=1.5, end=None, start=None, dash=None, opacity=None, cap=None):
    out = f'<line x1="{g(x1)}" y1="{g(y1)}" x2="{g(x2)}" y2="{g(y2)}" stroke="{stroke}" stroke-width="{g(w)}"'
    if dash:
        out += f' stroke-dasharray="{dash}"'
    if cap:
        out += f' stroke-linecap="{cap}"'
    if opacity is not None:
        out += f' opacity="{g(opacity)}"'
    if start:
        out += f' marker-start="url(#{start})"'
    if end:
        out += f' marker-end="url(#{end})"'
    return out + "/>"


def R(x, y, w, h, fill="none", stroke=None, sw=1.5, rx=0, opacity=None, dash=None, fo=None):
    out = f'<rect x="{g(x)}" y="{g(y)}" width="{g(w)}" height="{g(h)}"'
    if rx:
        out += f' rx="{g(rx)}"'
    return out + _paint(fill, stroke, sw, fo, opacity, dash) + "/>"


def MASK(x, y, w, h, rx=0):
    """Surface-coloured rect painted between a line and a label so the line
    visibly passes *behind* the label (check_overlaps.js treats these as masks)."""
    return R(x, y, w, h, fill="var(--surface)", rx=rx)


def C(cx, cy, r, fill="none", stroke=None, sw=1.5, opacity=None, dash=None, fo=None):
    return f'<circle cx="{g(cx)}" cy="{g(cy)}" r="{g(r)}"' + _paint(fill, stroke, sw, fo, opacity, dash) + "/>"


def E(cx, cy, rx, ry, fill="none", stroke=None, sw=1.5, opacity=None, dash=None, fo=None):
    return (f'<ellipse cx="{g(cx)}" cy="{g(cy)}" rx="{g(rx)}" ry="{g(ry)}"'
            + _paint(fill, stroke, sw, fo, opacity, dash) + "/>")


def P(d, fill="none", stroke="currentColor", sw=1.5, opacity=None, dash=None, end=None, fo=None, join=None):
    out = f'<path d="{d}"' + _paint(fill, stroke, sw, fo, opacity, dash)
    if join:
        out += f' stroke-linejoin="{join}"'
    if end:
        out += f' marker-end="url(#{end})"'
    return out + "/>"


def pts(points):
    return " ".join(f"{g(round(x, 1))},{g(round(y, 1))}" for x, y in points)


def PG(points, fill="none", stroke=None, sw=1.5, opacity=None, fo=None):
    return f'<polygon points="{pts(points)}"' + _paint(fill, stroke, sw, fo, opacity, None) + "/>"


def PL(points, stroke="currentColor", sw=1.5, dash=None, end=None, opacity=None):
    out = f'<polyline points="{pts(points)}" fill="none" stroke="{stroke}" stroke-width="{g(sw)}"'
    if dash:
        out += f' stroke-dasharray="{dash}"'
    if opacity is not None:
        out += f' opacity="{g(opacity)}"'
    if end:
        out += f' marker-end="url(#{end})"'
    return out + "/>"


def marker(mid, color="currentColor", size=6):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size}" markerHeight="{size}" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


def badge(x, y, label, fill="var(--ink-soft)", r=7.5, size=9):
    """Numbered/lettered callout: a filled disc with surface-coloured text,
    plus a same-size round mask so a line passing under the badge counts as masked."""
    return [MASK(x - r, y - r, 2 * r, 2 * r, rx=r), C(x, y, r, fill=fill),
            T(x, y + size * 0.35, label, size=size, weight="700", fill="var(--surface)")]


def svg(w, h, aria, body, defs=()):
    out = f'<svg viewBox="0 0 {g(w)} {g(h)}" role="img" aria-label="{aesc(aria)}">'
    if defs:
        out += "<defs>" + "".join(defs) + "</defs>"
    flat = []
    for b in body:
        if isinstance(b, (list, tuple)):
            flat.extend(b)
        else:
            flat.append(b)
    for b in flat:
        assert isinstance(b, str) and b.startswith("<"), f"bad svg fragment: {b!r}"
    return out + "".join(flat) + "</svg>"


# ---------- recurring biology glyphs ----------

def lipid(x, y_head, direction=1, tail_len=22, head_r=6, tails=2, kinked=False, gap=4,
          head="var(--accent)", tail="var(--mod2)", sw=1.8):
    """One phospholipid: head disc + 1 or 2 tails going down (direction=1) or up (-1)."""
    out = [C(x, y_head, head_r, fill=head, opacity=0.85)]
    y0 = y_head + direction * head_r
    offs = [0] if tails == 1 else [-gap / 2, gap / 2]
    for i, dx in enumerate(offs):
        if kinked and i == len(offs) - 1:
            ym = y0 + direction * tail_len * 0.45
            out.append(PL([(x + dx, y0), (x + dx, ym), (x + dx + 6, y0 + direction * tail_len)], stroke=tail, sw=sw))
        else:
            out.append(L(x + dx, y0, x + dx, y0 + direction * tail_len, stroke=tail, w=sw))
    return out


def bilayer(x0, x1, y_top, y_bot, step=14, tail_len=20, skip=(), head_r=5.5):
    """Horizontal bilayer: heads at y_top (tails down) and y_bot (tails up).
    skip = list of (xa, xb) ranges left empty for proteins."""
    out = []
    x = x0
    while x <= x1 + 0.1:
        if not any(a <= x <= b for a, b in skip):
            out += lipid(x, y_top, 1, tail_len, head_r)
            out += lipid(x, y_bot, -1, tail_len, head_r)
        x += step
    return out


def pentagon(cx, cy, r, fill="none", stroke=None, sw=1.5, opacity=None, fo=None):
    p = [(cx + r * math.sin(2 * math.pi * k / 5), cy - r * math.cos(2 * math.pi * k / 5)) for k in range(5)]
    return PG(p, fill=fill, stroke=stroke, sw=sw, opacity=opacity, fo=fo)


def hexagon(cx, cy, r, fill="none", stroke=None, sw=1.5, opacity=None, fo=None):
    p = [(cx + r * math.cos(math.pi / 6 + math.pi * k / 3), cy + r * math.sin(math.pi / 6 + math.pi * k / 3)) for k in range(6)]
    return PG(p, fill=fill, stroke=stroke, sw=sw, opacity=opacity, fo=fo)
