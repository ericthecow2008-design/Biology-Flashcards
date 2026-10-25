"""dkit: shared drawing helpers for the Modules 6-8 diagrams (built on tools/svgkit.py)."""
from svgkit import *


def node(x, y, w, h, rows, color=MOD1, size=11, weight="700", fill_opacity=0.12, rx=7, text_fill=INK, dash=None):
    """A rounded box with one or more centred text lines."""
    parts = [rect(x, y, w, h, rx=rx, fill=color, fill_opacity=fill_opacity, stroke=color, width=1.4, dash=dash)]
    if isinstance(rows, str):
        rows = [rows]
    gap = size * 1.25
    y0 = y + h / 2 - (len(rows) - 1) * gap / 2 + size * 0.35
    for i, r in enumerate(rows):
        parts.append(text(x + w / 2, y0 + i * gap, r, size=size, weight=weight if i == 0 else None, fill=text_fill))
    return "".join(parts)


def arrow(x1, y1, x2, y2, mid, color=INK, width=1.4, dash=None):
    return line(x1, y1, x2, y2, stroke=color, width=width, end=mid, dash=dash)


def axes(x0, y0, w, h, xticks, yticks, xlabel, ylabel, xfmt=str, yfmt=str, grid=True, xlab_dy=30, ylab_dx=34):
    """Plot frame. x0,y0 = bottom-left corner in px. xticks/yticks: list of (value_px_offset, label)."""
    p = []
    for off, lab in yticks:
        yy = y0 - off
        if grid and off > 0:
            p.append(line(x0, yy, x0 + w, yy, stroke=BORDER, width=1))
        p.append(line(x0 - 4, yy, x0, yy, stroke=SOFT, width=1))
        p.append(text(x0 - 7, yy + 3.4, yfmt(lab), size=9.5, anchor="end", fill=SOFT))
    for off, lab in xticks:
        xx = x0 + off
        p.append(line(xx, y0, xx, y0 + 4, stroke=SOFT, width=1))
        p.append(text(xx, y0 + 16, xfmt(lab), size=9.5, fill=SOFT))
    p.append(line(x0, y0 - h, x0, y0, stroke=SOFT, width=1.2))
    p.append(line(x0, y0, x0 + w, y0, stroke=SOFT, width=1.2))
    if xlabel:
        p.append(text(x0 + w / 2, y0 + xlab_dy, xlabel, size=10, fill=SOFT))
    if ylabel:
        yl = x0 - ylab_dx
        p.append(f'<text x="{n(yl)}" y="{n(y0 - h / 2)}" text-anchor="middle" font-size="10" fill="{SOFT}" '
                 f'transform="rotate(-90 {n(yl)} {n(y0 - h / 2)})">{ylabel}</text>')
    return "".join(p)


def table(x, y, widths, rows, row_h=22, header_fill=MOD1, size=10.5, first_col_anchor="start", bold_first=True):
    """A simple table: rows[0] is the header. Grid lines run between cells, never through text."""
    p = []
    W = sum(widths)
    H = row_h * len(rows)
    p.append(rect(x, y, W, H, rx=4, fill=SURFACE, stroke=BORDER, width=1))
    p.append(rect(x, y, W, row_h, rx=4, fill=header_fill, fill_opacity=0.14))
    for i in range(1, len(rows)):
        p.append(line(x, y + i * row_h, x + W, y + i * row_h, stroke=BORDER, width=1))
    cx = x
    for w in widths[:-1]:
        cx += w
        p.append(line(cx, y, cx, y + H, stroke=BORDER, width=1))
    for r, row in enumerate(rows):
        cx = x
        for c, cell in enumerate(row):
            w = widths[c]
            ty = y + r * row_h + row_h / 2 + size * 0.36
            if c == 0 and first_col_anchor == "start":
                p.append(text(cx + 7, ty, cell, size=size, anchor="start", weight="700" if (r == 0 or bold_first) else None))
            else:
                p.append(text(cx + w / 2, ty, cell, size=size, weight="700" if r == 0 else None))
            cx += w
    return "".join(p)
