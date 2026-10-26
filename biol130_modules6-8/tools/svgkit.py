"""svgkit: small helpers for hand-drawn inline-SVG diagrams in the BIOL 130 style.

Every helper returns a string of SVG markup. Collect the pieces in a list and pass it to svg():

    from svgkit import *

    def atp_cycle():
        K = "atp_cycle"                       # the diagram key; every id inside must start with it
        ARR = f"{K}_arr"
        parts = [
            rect(40, 30, 120, 44, rx=8, fill=MOD1, fill_opacity=0.12, stroke=MOD1, width=1.5),
            text(100, 57, "ATP", size=13, weight="700"),
            line(160, 52, 260, 52, end=ARR),
            label_box(210, 44, "hydrolysis"),  # a label sitting on a line: the box hides the line behind it
        ]
        return "ATP and ADP", svg(320, 110, "ATP is hydrolysed to ADP ...", parts, defs=[arrow_marker(ARR)])

    ALL = {"atp_cycle": atp_cycle}           # each diagrams file ends with this dict

Rules the checkers enforce (tools/build_diagrams.py, tools/scan_fills.py, tools/check_overlaps.js):
- colours are palette variables only (constants below) or "currentColor"; never hex codes or names;
- every <text> has an explicit fill (the helpers default to INK);
- font size at least 8.5 (default 11); width at most 640;
- ids (markers) start with the diagram key, so they never clash with another diagram;
- labels never overlap each other or cross a line, unless a label_box() masks the line.
"""
import html

INK, SOFT, FAINT = "var(--ink)", "var(--ink-soft)", "var(--ink-faint)"
SURFACE, BG, BORDER = "var(--surface)", "var(--bg)", "var(--border)"
ACCENT, BRIDGE, MOD1, MOD2 = "var(--accent)", "var(--bridge)", "var(--mod1)", "var(--mod2)"
REVIEW, VISUAL, GOOD = "var(--review)", "var(--visual)", "var(--good)"
PALETTE = ("--ink", "--ink-soft", "--ink-faint", "--bg", "--surface", "--border", "--accent",
           "--bridge", "--mod1", "--mod2", "--review", "--visual", "--good")

__all__ = ["INK", "SOFT", "FAINT", "SURFACE", "BG", "BORDER", "ACCENT", "BRIDGE", "MOD1", "MOD2",
           "REVIEW", "VISUAL", "GOOD", "PALETTE", "svg", "text", "lines", "line", "rect", "circle",
           "ellipse", "path", "polygon", "polyline", "group", "arrow_marker", "label_box", "pill",
           "text_width", "n"]


def n(v):
    """Compact number formatting: 12.0 -> '12', 3.14159 -> '3.14'."""
    if isinstance(v, int):
        return str(v)
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _esc(s):
    return html.escape(str(s), quote=True)


def _attrs(pairs):
    return "".join(f' {k}="{v if isinstance(v, str) else n(v)}"' for k, v in pairs if v is not None)


def svg(width, height, aria, parts, defs=()):
    """The outer <svg>. aria: one or two sentences saying what the picture shows (never the answer)."""
    assert width <= 640, "diagrams are at most 640 wide"
    d = f"<defs>{''.join(defs)}</defs>" if defs else ""
    return (f'<svg viewBox="0 0 {n(width)} {n(height)}" role="img" aria-label="{_esc(aria)}">'
            f'{d}{"".join(parts)}</svg>')


def text(x, y, s, size=11, anchor="middle", weight=None, fill=INK, italic=False, opacity=None):
    """One line of text. y is the baseline. anchor: start | middle | end."""
    assert size >= 8.5, "font size must be at least 8.5"
    return (f'<text{_attrs([("x", x), ("y", y), ("font-size", size), ("text-anchor", anchor if anchor != "start" else None), ("font-weight", weight), ("font-style", "italic" if italic else None), ("fill", fill), ("opacity", opacity)])}>'
            f"{_esc(s)}</text>")


def lines(x, y, rows, size=11, gap=1.25, **kw):
    """Several lines of text, one <text> each, starting at baseline y."""
    return "".join(text(x, y + i * size * gap, r, size=size, **kw) for i, r in enumerate(rows))


def line(x1, y1, x2, y2, stroke=INK, width=1.4, dash=None, end=None, start=None, opacity=None, linecap=None):
    """A straight line. end/start: a marker id from arrow_marker() for an arrowhead."""
    return (f'<line{_attrs([("x1", x1), ("y1", y1), ("x2", x2), ("y2", y2), ("stroke", stroke), ("stroke-width", width), ("stroke-dasharray", dash), ("stroke-linecap", linecap), ("opacity", opacity)])}'
            f'{_attrs([("marker-end", f"url(#{end})" if end else None), ("marker-start", f"url(#{start})" if start else None)])}/>')


def rect(x, y, w, h, rx=0, fill="none", fill_opacity=None, stroke=None, width=None, dash=None, opacity=None):
    return (f'<rect{_attrs([("x", x), ("y", y), ("width", w), ("height", h), ("rx", rx or None), ("fill", fill), ("fill-opacity", fill_opacity), ("stroke", stroke), ("stroke-width", width), ("stroke-dasharray", dash), ("opacity", opacity)])}/>')


def circle(cx, cy, r, fill="none", fill_opacity=None, stroke=None, width=None, dash=None, opacity=None):
    return (f'<circle{_attrs([("cx", cx), ("cy", cy), ("r", r), ("fill", fill), ("fill-opacity", fill_opacity), ("stroke", stroke), ("stroke-width", width), ("stroke-dasharray", dash), ("opacity", opacity)])}/>')


def ellipse(cx, cy, rx, ry, fill="none", fill_opacity=None, stroke=None, width=None, dash=None, opacity=None):
    return (f'<ellipse{_attrs([("cx", cx), ("cy", cy), ("rx", rx), ("ry", ry), ("fill", fill), ("fill-opacity", fill_opacity), ("stroke", stroke), ("stroke-width", width), ("stroke-dasharray", dash), ("opacity", opacity)])}/>')


def path(d, fill="none", fill_opacity=None, stroke=INK, width=1.4, dash=None, end=None, start=None,
         linejoin=None, linecap=None, opacity=None):
    """Any path. d uses absolute or relative SVG path commands."""
    return (f'<path{_attrs([("d", d), ("fill", fill), ("fill-opacity", fill_opacity), ("stroke", stroke), ("stroke-width", width if stroke not in (None, "none") else None), ("stroke-dasharray", dash), ("stroke-linejoin", linejoin), ("stroke-linecap", linecap), ("opacity", opacity)])}'
            f'{_attrs([("marker-end", f"url(#{end})" if end else None), ("marker-start", f"url(#{start})" if start else None)])}/>')


def polygon(points, fill="none", fill_opacity=None, stroke=None, width=None, opacity=None):
    pts = " ".join(f"{n(x)},{n(y)}" for x, y in points)
    return (f'<polygon{_attrs([("points", pts), ("fill", fill), ("fill-opacity", fill_opacity), ("stroke", stroke), ("stroke-width", width), ("opacity", opacity)])}/>')


def polyline(points, stroke=INK, width=1.4, fill="none", dash=None, end=None, linejoin="round"):
    pts = " ".join(f"{n(x)},{n(y)}" for x, y in points)
    return (f'<polyline{_attrs([("points", pts), ("fill", fill), ("stroke", stroke), ("stroke-width", width), ("stroke-dasharray", dash), ("stroke-linejoin", linejoin)])}'
            f'{_attrs([("marker-end", f"url(#{end})" if end else None)])}/>')


def group(parts, transform=None, opacity=None):
    return f'<g{_attrs([("transform", transform), ("opacity", opacity)])}>{"".join(parts)}</g>'


def arrow_marker(marker_id, color=INK, size=7):
    """Arrowhead definition for defs=[...]; use with line(..., end=marker_id). The id must start with the diagram key."""
    return (f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{n(size)}" '
            f'markerHeight="{n(size)}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


def text_width(s, size=11):
    """Rough rendered width of a label, for sizing boxes (about 0.56 em per character)."""
    return len(str(s)) * size * 0.56


def label_box(x, y, s, size=10.5, pad=3, fill=SURFACE, text_fill=INK, anchor="middle", weight=None):
    """A label with a background box in the card colour, so a line running behind it is hidden.
    (x, y) is the text baseline, as in text()."""
    w = text_width(s, size) + 2 * pad
    left = {"start": x - pad, "middle": x - w / 2, "end": x - w + pad}[anchor]
    return (rect(left, y - size * 0.95, w, size * 1.3, rx=2, fill=fill) +
            text(x, y, s, size=size, anchor=anchor, weight=weight, fill=text_fill))


def pill(x, y, s, color=ACCENT, size=10, weight="700"):
    """A small rounded tag (outline in `color`, text in `color`) centred on x, baseline y."""
    w = text_width(s, size) + 12
    return (rect(x - w / 2, y - size - 1, w, size + 7, rx=(size + 7) / 2, fill=SURFACE, stroke=color, width=1.2) +
            text(x, y, s, size=size, weight=weight, fill=color))
