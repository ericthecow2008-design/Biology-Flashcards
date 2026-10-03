"""Module 6 diagrams, part C: metabolic classes, free-energy profiles, ATP parts,
enzyme/molecule binding, branched pathway.  Question-side figures: structure and
data only -- no classifications, rules or conclusions in labels or aria text."""
import math
from svgkit import *

SOFT = "var(--ink-soft)"
FAINT = "var(--ink-faint)"


def TR(x, y, s, size=9.5, fill=SOFT, angle=-90):
    """Rotated text (vertical axis titles), with an explicit fill like T()."""
    return (f'<text x="{g(x)}" y="{g(y)}" text-anchor="middle" font-size="{g(size)}" fill="{fill}" '
            f'transform="rotate({g(angle)} {g(x)} {g(y)})">{esc(s)}</text>')


def _r(v):
    return round(v, 2)


def hump(x0, y0, xp, yp, x1, y1, k0=0.5, kp=0.4):
    """Path fragment: smooth rise from (x0,y0) to a peak (xp,yp), then a smooth fall to
    (x1,y1); two cubic Beziers with horizontal tangents at all three points."""
    r, f = xp - x0, x1 - xp
    return (f"C{_r(x0 + k0 * r)},{_r(y0)} {_r(xp - kp * r)},{_r(yp)} {_r(xp)},{_r(yp)} "
            f"C{_r(xp + kp * f)},{_r(yp)} {_r(x1 - k0 * f)},{_r(y1)} {_r(x1)},{_r(y1)}")


# ---------------------------------------------------------------------------
def metabolic_classification_grid():
    W, H = 460, 170
    gx, cw, gap = 140, 150, 10          # grid left edge, cell width, gap between cells
    top, ch = 40, 56                    # grid top, cell height
    cols = [gx + cw / 2, gx + cw + gap + cw / 2]
    rows = [top + ch / 2, top + ch + gap + ch / 2]
    b = []
    for cx, word in zip(cols, ("light", "chemical compounds")):
        b += [T(cx, 15, "energy from", 9.5, fill=SOFT), T(cx, 29, word, 10.5, weight="700")]
    for cy, word in zip(rows, ("CO₂", "organic molecules")):
        b += [T(gx - 12, cy - 4, "carbon from", 9.5, anchor="end", fill=SOFT),
              T(gx - 12, cy + 10, word, 10.5, anchor="end", weight="700")]
    letters = iter("ABCD")
    for cy in rows:
        for cx in cols:
            b.append(R(cx - cw / 2, cy - ch / 2, cw, ch, rx=8, fill=FAINT, fo=0.07, stroke=FAINT, sw=1.2))
            b += badge(cx, cy, next(letters), r=12, size=11.5)
    aria = ("A 2 by 2 grid. The two columns are headed energy from light and energy from chemical compounds; the two "
            "rows are headed carbon from CO₂ and carbon from organic molecules. Each cell holds only a letter: A (light, "
            "CO₂), B (chemical compounds, CO₂), C (light, organic molecules) and D (chemical compounds, organic "
            "molecules)")
    return "Sorting organisms by energy source and carbon source", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
def reaction_profiles_two():
    W, H = 640, 234

    def yv(v):
        return 206 - 1.45 * v
    b = [L(320, 10, 320, 226, stroke="var(--border)", w=1)]
    for x0, name, (vr, vp, vq) in ((0, "I", (60, 110, 20)), (320, "II", (30, 55, 50))):
        ax, xend = x0 + 56, x0 + 308
        b.append(T(x0 + 12, 20, name, 11.5, anchor="start", weight="700"))
        for v in range(0, 121, 10):
            y = yv(v)
            if v % 20 == 0:
                b += [L(ax - 4.5, y, ax, y, stroke=SOFT, w=1), T(ax - 7, y + 3.2, str(v), 9, anchor="end", fill=SOFT)]
            else:
                b.append(L(ax - 2.5, y, ax, y, stroke=SOFT, w=1))
        b += [L(ax, yv(120) - 6, ax, yv(0), stroke=SOFT, w=1.2), L(ax, yv(0), xend, yv(0), stroke=SOFT, w=1.2),
              TR(x0 + 22, (yv(0) + yv(120)) / 2, "free energy (kJ/mol)"),
              T((ax + xend) / 2, 226, "course of reaction", 9.5, fill=SOFT)]
        xs, xa, xp, xb, xe = x0 + 70, x0 + 118, x0 + 188, x0 + 258, x0 + 302
        yr, yp, yq = yv(vr), yv(vp), yv(vq)
        # dashed guides from each plateau and the peak back to the y-axis (drawn under the curve)
        for xg, yg in ((xs, yr), (xp, yp), (xb, yq)):
            b.append(L(ax, yg, xg, yg, stroke=FAINT, w=1, dash="3 3"))
        b.append(P(f"M{xs},{_r(yr)} L{xa},{_r(yr)} " + hump(xa, yr, xp, yp, xb, yq, 0.5, 0.38)
                   + f" L{xe},{_r(yq)}", sw=2.2))
        b += [T((xs + xa) / 2, yr + 15, "reactants", 9.5), T((xb + xe) / 2, yq + 15, "products", 9.5)]
    aria = ("Two free-energy plots side by side, panels I and II. In each, the y-axis is free energy (kJ/mol) labelled "
            "0, 20, 40, 60, 80, 100 and 120 with small unlabelled ticks halfway between, the x-axis is course of "
            "reaction, and dashed lines run from each plateau and from the peak back to the y-axis. Panel I: a reactants plateau at 60 rises in one smooth hump to a "
            "peak at 110 and falls to a products plateau at 20. Panel II: a reactants plateau at 30 rises to a peak at "
            "55 and falls to a products plateau at 50")
    return "Free-energy profiles of reactions I and II", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
def enzyme_energy_profile():
    W, H = 496, 250
    ax, ay, xend = 42, 220, 490
    yr, yq, y1, y2 = 136, 194, 30, 94               # reactant, product, peak 1, peak 2
    xs, xa, xp, xb, xe = 54, 124, 264, 404, 484
    MK, MA = "enzyme_energy_profile_arr", "enzyme_energy_profile_acc"
    c1 = f"M{xs},{yr} L{xa},{yr} " + hump(xa, yr, xp, y1, xb, yq, 0.45, 0.34) + f" L{xe},{yq}"
    c2 = f"M{xa},{yr} " + hump(xa, yr, xp, y2, xb, yq, 0.45, 0.45)
    xa_, xb_, xc_ = xp, xp + 14, 456                 # x of arrows a, b, c (b sits on curve 2's broad top)
    b = [L(ax, 12, ax, ay, stroke=SOFT, w=1.2), L(ax, ay, xend, ay, stroke=SOFT, w=1.2),
         TR(28, (12 + ay) / 2, "free energy"), T((ax + xend) / 2, 240, "course of reaction", 9.5, fill=SOFT),
         L(xa, yr, 470, yr, stroke=FAINT, w=1.1, dash="4 3"),
         P(c1, sw=2.2), P(c2, stroke="var(--accent)", sw=2.2, dash="6 4"),
         L(xa_, yr - 1.5, xa_, y1 + 1.5, w=1.4, start=MK, end=MK),
         L(xb_, yr - 1.5, xb_, y2 + 1.5, stroke="var(--accent)", w=1.4, start=MA, end=MA),
         L(xc_, yr + 1.5, xc_, yq - 1.5, w=1.4, start=MK, end=MK)]
    b += badge(xa_, (y1 + y2) / 2 - 2, "a")
    b += badge(xb_, (yr + y2) / 2, "b")
    b += badge(xc_, (yr + yq) / 2, "c")
    b += [T(xp + 20, y1 - 8, "curve 1", 10, anchor="start", weight="700"),
          T(xp - 8, y2 - 8, "curve 2", 10, anchor="end", weight="700", fill="var(--accent)"),
          T((xs + xa) / 2, yr + 15, "reactants", 9.5), T((xb + xe) / 2 - 8, yq + 15, "products", 9.5)]
    aria = ("Plot of free energy (y-axis, no numbers) against course of reaction (x-axis). Two curves leave the same "
            "reactants plateau on the left and end on the same, lower products plateau on the right: curve 1 (solid) "
            "rises to a tall peak and curve 2 (dashed) to a much lower peak at the same point. A dashed line extends the "
            "reactant level to the right. Double-headed arrow a spans from the reactant level up to the peak of curve 1, "
            "arrow b from the reactant level up to the peak of curve 2, and arrow c, near the products, from the "
            "reactant level down to the product level")
    return "One reaction by two different paths", svg(W, H, aria, b, defs=[marker(MK), marker(MA, "var(--accent)")])


# ---------------------------------------------------------------------------
def atp_parts_brackets():
    W, H = 376, 214
    Y0, pr = 66, 12                                  # phosphate row, phosphate radius
    px = [50, 104, 158]                              # outermost (3rd) ... nearest (1st)
    b = [T((px[0] + px[2]) / 2, Y0 - 24, "phosphate groups", 9.5)]
    # bonds: P3-P2 (z), P2-P1 (y), P1-CH2 (x)
    ch2x = 211
    bonds = [(px[0] + pr, px[1] - pr, "z"), (px[1] + pr, px[2] - pr, "y"), (px[2] + pr, ch2x - 12, "x")]
    for x1, x2, tag in bonds:
        b += [L(x1, Y0, x2, Y0, w=1.6), T((x1 + x2) / 2, Y0 + 18, tag, 11, weight="700", italic=True)]
    for x in px:
        b += [C(x, Y0, pr, fill="var(--accent)"), T(x, Y0 + 3.8, "P", 11, weight="700", fill="var(--surface)"),
              T(x + 12.5, Y0 - 6, "⁻", 11, anchor="start", weight="700", fill=SOFT)]
    b.append(T(ch2x, Y0 + 3.4, "CH₂", 9.5, weight="700"))
    # ribose ring: O at the top vertex; C4' (upper left) bonded to CH2; C1' (upper right) to adenine
    rr = 25
    c4 = (240.0, Y0 + 9)
    rcx, rcy = c4[0] + rr * math.sin(2 * math.pi / 5), c4[1] + rr * math.cos(2 * math.pi / 5)
    v = [(rcx + rr * math.sin(2 * math.pi * k / 5), rcy - rr * math.cos(2 * math.pi * k / 5)) for k in range(5)]
    b += [L(ch2x + 11, Y0 + 1, v[4][0], v[4][1], w=1.6),
          PG(v, fill="var(--mod1)", fo=0.16, stroke="var(--mod1)", sw=1.8),
          MASK(v[0][0] - 5.5, v[0][1] - 6.5, 11, 13, rx=3), T(v[0][0], v[0][1] + 3.6, "O", 10, weight="700"),
          T(rcx, rcy + 4.5, "ribose", 9.5)]
    for k in (2, 3):                                 # C2' and C3' carry OH
        b += [L(v[k][0], v[k][1], v[k][0], v[k][1] + 8, w=1.4), T(v[k][0], v[k][1] + 18, "OH", 9)]
    # adenine: hexagon fused to a pentagon; the pentagon's lower-left vertex bonds to C1'
    hr = 20
    r5 = hr / (2 * math.sin(math.pi / 5))
    a5 = r5 * math.cos(math.pi / 5)
    n9 = (v[1][0] + 13, v[1][1] - 13)
    c5 = (n9[0] - r5 * math.cos(math.radians(108)), n9[1] - r5 * math.sin(math.radians(108)))
    hx, hy = c5[0] + a5 + hr * math.cos(math.pi / 6), c5[1]
    pent = [(c5[0] + r5 * math.cos(math.radians(a)), c5[1] + r5 * math.sin(math.radians(a)))
            for a in (36, 108, 180, 252, 324)]
    b += [L(v[1][0], v[1][1], n9[0], n9[1], w=1.6),
          hexagon(hx, hy, hr, fill="var(--bridge)", fo=0.16, stroke="var(--bridge)", sw=1.8),
          PG(pent, fill="var(--bridge)", fo=0.16, stroke="var(--bridge)", sw=1.8),
          T(hx, hy + hr + 14, "adenine", 9.5)]
    xr = hx + hr * math.cos(math.pi / 6)            # adenine's right edge: every bracket ends here
    lefts = [ch2x - 10, px[2] - pr, px[1] - pr, px[0] - pr]
    for i, xl in enumerate(lefts):
        y = 142 + 20 * i
        b.append(P(f"M{_r(xl)},{y - 6} L{_r(xl)},{y} L{_r(xr)},{y} L{_r(xr)},{y - 6}", stroke=SOFT, sw=1.4))
        b += badge(xl - 13, y, str(i + 1))
    aria = ("A molecule drawn left to right: three phosphate groups, each a circle marked P with a minus charge mark, "
            "joined in a row by bonds; a CH₂ group bonded to a five-membered ribose ring with O at its top vertex and "
            "OH on each of its two lower carbons; and adenine, a six-membered ring fused to a five-membered ring, bonded "
            "to the ribose. Italic tags mark three bonds: x between the CH₂ side and the nearest phosphate, y between "
            "the nearest and middle phosphates, and z between the middle and outermost phosphates. Below, four nested "
            "brackets numbered 1 to 4 all end at adenine's right edge: 1 spans adenine and ribose, 2 adds the nearest "
            "phosphate, 3 adds the middle phosphate, and 4 spans all three phosphates")
    return "ATP, piece by piece", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
def _enzyme(cx, cy, notch, w=128, h=74, rr=26):
    """Rounded enzyme blob with a notch cut into the middle of its top edge.
    notch: (dx, dy) points from the left rim to the right rim, relative to (cx, top)."""
    x0, x1, top, bot = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    d = f"M{_r(x0 + rr)},{_r(top)} "
    d += " ".join(f"L{_r(cx + dx)},{_r(top + dy)}" for dx, dy in notch)
    d += (f" L{_r(x1 - rr)},{_r(top)} C{_r(x1 - rr * 0.4)},{_r(top)} {_r(x1)},{_r(top + rr * 0.5)} {_r(x1)},{_r(top + rr)}"
          f" C{_r(x1)},{_r(bot - 6)} {_r(x1 - 26)},{_r(bot)} {_r(cx)},{_r(bot)}"
          f" C{_r(x0 + 26)},{_r(bot)} {_r(x0)},{_r(bot - 6)} {_r(x0)},{_r(top + rr)}"
          f" C{_r(x0)},{_r(top + rr * 0.5)} {_r(x0 + rr * 0.4)},{_r(top)} {_r(x0 + rr)},{_r(top)} Z")
    return P(d, fill="var(--mod2)", fo=0.2, stroke="var(--mod2)", sw=1.8, join="round")


NOTCH = [(-16, 0), (-9, 20), (9, 20), (16, 0)]      # active-site notch: 32 wide at the rim, 18 at the floor
SLOPE = 7 / 20                                      # notch wall slope (dx per dy)


def _wedge(cx, y_bottom, fill, extra=10):
    """Molecule outline that exactly fills NOTCH, sticking out `extra` px above the rim."""
    yt = y_bottom - 20 - extra
    hw_t = 16 + SLOPE * extra
    return PG([(cx - 9, y_bottom), (cx + 9, y_bottom), (cx + hw_t, yt), (cx - hw_t, yt)],
              fill=fill, stroke=fill, sw=1.5)


def _cross(x, y, s=5):
    return [L(x - s, y - s, x + s, y + s, stroke="var(--review)", w=2.2),
            L(x + s, y - s, x - s, y + s, stroke="var(--review)", w=2.2)]


def inhibition_modes():
    W, H = 640, 178
    cy, h = 126, 74
    top = cy - h / 2
    b = [L(213.3, 10, 213.3, H - 10, stroke="var(--border)", w=1), L(426.7, 10, 426.7, H - 10, stroke="var(--border)", w=1)]
    cxs = [106.7, 320, 533.3]
    for i, cx in enumerate(cxs):
        b += badge(cx - 92, 20, str(i + 1))
    # panel 1: substrate bound in the notch
    cx = cxs[0]
    b += [_enzyme(cx, cy, NOTCH), _wedge(cx, top + 20, "var(--accent)"),
          T(cx, top - 17, "substrate", 9.5), T(cx, cy + 14, "enzyme", 10, weight="700"),
          L(cx + 31, top - 11, cx + 15, top + 3, stroke=SOFT, w=1.1),
          T(cx + 34, top - 8, "active site", 9.5, anchor="start", fill=SOFT)]
    # panel 2: X sits in the notch; the substrate hovers just above, unbound
    cx = cxs[1]
    b += [_enzyme(cx, cy, NOTCH), _wedge(cx, top + 20, "var(--bridge)"),
          T(cx, top + 7, "X", 10.5, weight="700", fill="var(--surface)"),
          _wedge(cx, top - 16, "var(--accent)")] + _cross(cx + 32, top - 32)
    # panel 3: Y bound low on the side; notch pinched so the substrate above no longer fits
    cx = cxs[2]
    pinched = [(-8, 0), (-2, 16), (2, 16), (8, 0)]
    yx, yy = cx - 50, cy + 26
    b += [_enzyme(cx, cy, pinched), MASK(yx - 6, yy - 6.5, 12, 13),
          C(yx, yy, 10.5, fill="var(--visual)", stroke="var(--visual)", sw=1.2),
          T(yx, yy + 3.8, "Y", 10.5, weight="700", fill="var(--surface)"),
          _wedge(cx, top - 8, "var(--accent)")] + _cross(cx + 32, top - 24)
    aria = ("Three panels numbered 1 to 3, each showing the same enzyme: a large rounded shape with a notch, the active "
            "site, in its top edge. Panel 1: the substrate, a small wedge that exactly fits the notch, sits in it. "
            "Panel 2: a molecule X with the same wedge outline but a different colour sits in the notch, and the "
            "substrate is drawn just above it, not bound, beside a small ✕. Panel 3: a small round molecule Y is bound "
            "to the lower left side of the enzyme, away from the notch; the notch is drawn as a narrow V, narrower than "
            "the base of the substrate, which is drawn above it beside a small ✕")
    return "One enzyme meets three different molecules", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
def branched_pathway():
    W, H = 440, 166
    MK = "branched_pathway_arr"
    bw, bh = 40, 30
    ty, by = 46, 126
    pos = {"A": (40, ty), "B": (160, ty), "C": (280, ty), "D": (400, ty), "E": (280, by), "F": (400, by)}
    b = []

    def box(k):
        x, y = pos[k]
        return [R(x - bw / 2, y - bh / 2, bw, bh, rx=8, fill="var(--mod1)", fo=0.14, stroke="var(--mod1)", sw=1.8),
                T(x, y + 4.2, k, 11.5, weight="700")]

    def arrow(p, q, label):
        (x1, y1), (x2, y2) = pos[p], pos[q]
        return [L(x1 + bw / 2 + 2, y1, x2 - bw / 2 - 3, y2, w=1.5, end=MK),
                T((x1 + x2) / 2, y1 - 8, label, 10)]
    b += arrow("A", "B", "e1") + arrow("B", "C", "e2") + arrow("C", "D", "e3") + arrow("E", "F", "e5")
    xb, yb = pos["B"]
    xe, ye = pos["E"]
    b += [P(f"M{xb},{yb + bh / 2 + 2} L{xb},{ye} L{xe - bw / 2 - 3},{ye}", sw=1.5, end=MK, join="round"),
          T((xb + xe - bw / 2) / 2, ye - 8, "e4", 10)]
    for k in pos:
        b += box(k)
    for k in ("D", "F"):
        x, y = pos[k]
        b.append(T(x, y + bh / 2 + 14, "end product", 9, fill=SOFT))
    aria = ("Flow diagram of a branched pathway: boxes A, B, C and D in a top row joined by arrows labelled e1 (A to B), "
            "e2 (B to C) and e3 (C to D); a second arrow labelled e4 leaves B and leads down to E, and an arrow labelled "
            "e5 leads from E to F in a lower row. D and F are each labelled end product")
    return "A branched metabolic pathway", svg(W, H, aria, b, defs=[marker(MK)])


ALL = {
    "metabolic_classification_grid": metabolic_classification_grid,
    "reaction_profiles_two": reaction_profiles_two,
    "enzyme_energy_profile": enzyme_energy_profile,
    "atp_parts_brackets": atp_parts_brackets,
    "inhibition_modes": inhibition_modes,
    "branched_pathway": branched_pathway,
}
