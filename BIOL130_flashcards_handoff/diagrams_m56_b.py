"""Module 5 diagrams, part B: translation snapshot, translation start sites, SRP targeting, signal-anchor orientation."""
import math
from svgkit import *

SOFT = "var(--ink-soft)"
RNA = "var(--review)"       # mRNA (as in the Module 4 diagrams)
RIBO = "var(--accent)"      # ribosome subunits (as in prok_vs_euk_expression)
TRNA = "var(--mod1)"        # tRNA
AA = "var(--good)"          # amino acids / polypeptide chain (as in prok_vs_euk_expression)
SIG = "var(--bridge)"       # signal sequence / signal-anchor sequence


# ---------- small geometry helpers ----------

def _f(v):
    return f"{round(v, 1):g}"


def _path(points):
    return "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in points)


def _catmull(ctrl, n=24):
    """Dense points along a Catmull-Rom spline through ctrl points."""
    pts = [ctrl[0]] + list(ctrl) + [ctrl[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3)
                             for a, b, c, d in zip(p0, p1, p2, p3)))
    out.append(ctrl[-1])
    return out


def _wave_pts(ctrl, amp=2.4, wl=8.0, sign=1):
    """Wavy polypeptide along a Catmull-Rom centre line through ctrl: one quadratic Bezier per half-wave.
    Returns [P0, C1, P1, C2, P2, ...]; the wave starts and ends on the centre line."""
    center = _catmull(ctrl)
    cum = [0.0]
    for (xa, ya), (xb, yb) in zip(center, center[1:]):
        cum.append(cum[-1] + math.hypot(xb - xa, yb - ya))
    total = cum[-1]
    n = max(1, round(total / (wl / 2)))
    h = total / n

    def at(s):
        j = 1
        while j < len(cum) - 1 and cum[j] < s:
            j += 1
        (xa, ya), (xb, yb) = center[j - 1], center[j]
        t = 0.0 if cum[j] == cum[j - 1] else (s - cum[j - 1]) / (cum[j] - cum[j - 1])
        d = math.hypot(xb - xa, yb - ya) or 1.0
        return xa + (xb - xa) * t, ya + (yb - ya) * t, -(yb - ya) / d, (xb - xa) / d

    out = [at(0)[:2]]
    for k in range(n):
        mx, my, nx, ny = at((k + 0.5) * h)
        sgn = sign * (1 if k % 2 == 0 else -1)
        out += [(mx + nx * 2 * amp * sgn, my + ny * 2 * amp * sgn), at((k + 1) * h)[:2]]
    return out


def _wave_d(pts):
    d = f"M{_f(pts[0][0])},{_f(pts[0][1])}"
    for i in range(1, len(pts), 2):
        d += f" Q{_f(pts[i][0])},{_f(pts[i][1])} {_f(pts[i + 1][0])},{_f(pts[i + 1][1])}"
    return d


def chain(ctrl, color=AA, sw=2, amp=2.4, wl=8.0, sign=1):
    return P(_wave_d(_wave_pts(ctrl, amp, wl, sign)), stroke=color, sw=sw, join="round")


# ======================================================================
# 1) ribosome partway along an mRNA
# ======================================================================

def _trna(c, y_top, letters, color=TRNA, ends=None, lsize=11):
    """tRNA icon: rounded acceptor stem on top, two rounded side lobes, anticodon foot at the bottom.
    The anticodon letters sit at c-12, c, c+12 so they line up with the codon letters."""
    s, a, h = 6, 23, 7                         # stem half-width, arm half-length, arm half-height
    ya1, ya2 = y_top + 32, y_top + 46          # arms
    yf = y_top + 76                            # foot top
    d = (f"M{c - s},{y_top + s} A{s},{s} 0 0 1 {c + s},{y_top + s} V{ya1} H{c + a - h} "
         f"A{h},{h} 0 0 1 {c + a - h},{ya2} H{c + s} V{yf} H{c - s} V{ya2} H{c - a + h} "
         f"A{h},{h} 0 0 1 {c - a + h},{ya1} H{c - s} Z")
    out = [P(d, fill=color, fo=0.26, stroke=color, sw=1.3, join="round"),
           R(c - 18.5, yf, 37, 20, rx=6, fill=color, fo=0.26, stroke=color, sw=1.3)]
    yb = yf + 14
    for dx, ch in zip((-12, 0, 12), letters):
        out.append(T(c + dx, yb, ch, lsize, weight="700", fill=color))
    if ends:
        out += [T(c - 21.5, yb, ends[0], 9, anchor="end", fill=color),
                T(c + 21.5, yb, ends[1], 9, anchor="start", fill=color)]
    return out


def _bead(x, y, label, r=12):
    return [C(x, y, r, fill=AA, fo=0.22, stroke=AA, sw=1.4), T(x, y + 3.2, label, 9, weight="700")]


def ribosome_snapshot():
    W, H = 572, 248
    pitch, X0 = 72, 70
    codons = ["ACC", "AUG", "GCU", "UGG", "AAA", "UAG", "GCA"]
    cx = [X0 + pitch * i for i in range(len(codons))]
    yl, yc = 194, 187                     # mRNA backbone, codon-letter baseline
    sE, sP, sA = cx[1], cx[2], cx[3]
    xl, xr, yt, yb = 100, 328, 38, 172    # large subunit box
    b = []
    # large subunit (rounded top) and small subunit
    b.append(P(f"M{xl},{yb - 8} V{yt + 34} Q{xl},{yt} {xl + 34},{yt} H{xr - 34} Q{xr},{yt} {xr},{yt + 34} V{yb - 8} "
               f"Q{xr},{yb} {xr - 8},{yb} H{xl + 8} Q{xl},{yb} {xl},{yb - 8} Z",
               fill=RIBO, fo=0.13, stroke=RIBO, sw=1.8))
    b.append(R(108, 200, 212, 42, rx=21, fill=RIBO, fo=0.22, stroke=RIBO, sw=1.8))
    # three slots (arches open at the bottom)
    for c, name in ((sE, "E"), (sP, "P"), (sA, "A")):
        b.append(P(f"M{c - 33},146 V58 Q{c - 33},46 {c - 21},46 H{c + 21} Q{c + 33},46 {c + 33},58 V146",
                   stroke=RIBO, sw=1.2))
        b.append(T(c - 25, 62, name, 11.5, anchor="start", weight="700"))
    # mRNA
    b.append(L(30, yl, 548, yl, stroke=RNA, w=3))
    for i in range(len(codons) - 1):
        xb = (cx[i] + cx[i + 1]) / 2
        b.append(L(xb, yl - 5, xb, yl + 5, stroke=SOFT, w=1.2))
    for c, cod in zip(cx, codons):
        for dx, ch in zip((-12, 0, 12), cod):
            b.append(T(c + dx, yc, ch, 11, weight="700", fill=RNA))
    b += [T(cx[0] - 34, yc, "…", 11, weight="700", fill=RNA), T(cx[-1] + 34, yc, "…", 11, weight="700", fill=RNA),
          T(24, yl + 4, "5′", 11, anchor="end", weight="700"), T(554, yl + 4, "3′", 11, anchor="start", weight="700")]
    # codon-anticodon pairing ticks (E and P sites)
    for c in (sE, sP):
        for dx in (-12, 0, 12):
            b.append(L(c + dx, 169.5, c + dx, 177, stroke=SOFT, w=1.2, dash="2 1.5"))
    # E-site tRNA (no amino acid), P-site tRNA carrying Met-Ala
    b += _trna(sE, 72, "UAC", ends=("3′-", "-5′"))
    b += _trna(sP, 72, "CGA", ends=("3′-", "-5′"))
    b.append(L(sP, 32, sP, 48, stroke=AA, w=2))
    b += _bead(sP, 60, "Ala") + _bead(sP, 20, "Met")
    # approaching tRNA, upper right
    xq = 400
    b += _trna(xq, 36, "???")
    b += _bead(xq, 24, "?")
    # part names
    b += [T(94, 56, "large subunit", 9.5, anchor="end", fill=SOFT),
          T(102, 226, "small subunit", 9.5, anchor="end", fill=SOFT),
          T(548, 214, "mRNA", 9.5, anchor="end", fill=SOFT)]
    aria = ("A ribosome, its large subunit on top and its small subunit below, sits on an mRNA that runs between them from "
            "5′ on the left to 3′ on the right, written in codons as 5′ … ACC AUG GCU UGG AAA UAG GCA … 3′. Inside the "
            "large subunit are three slots labelled E, P and A, from left to right, directly over the codons AUG, GCU and "
            "UGG; ACC lies to the left of the ribosome and AAA, UAG and GCA to its right. The E slot holds a tRNA with "
            "anticodon 3′-UAC-5′ paired to AUG and nothing attached; the P slot holds a tRNA with anticodon 3′-CGA-5′ "
            "paired to GCU, carrying a two-bead chain whose bead Ala is bonded to the tRNA and whose bead Met is the free "
            "end, reaching up out of the large subunit; the A slot is empty above UGG. Outside the ribosome, upper right, "
            "is a tRNA carrying one bead labelled ? with anticodon ? ? ?.")
    return "A ribosome partway along an mRNA", svg(W, H, aria, b)


# ======================================================================
# 2) two mRNAs: where can a ribosome start?
# ======================================================================

def _box(x, y, w, h, color, rx=4, fo=0.22, sw=1.4):
    """Tinted box on the mRNA; a surface underlay hides the strand line behind it."""
    return [R(x, y - h / 2, w, h, rx=rx, fill="var(--surface)"),
            R(x, y - h / 2, w, h, rx=rx, fill=color, fo=fo, stroke=color, sw=sw)]


def _codon_box(x, y, w, label, color, h=20, size=9.5):
    return _box(x, y, w, h, color) + [T(x + w / 2, y + size * 0.36, label, size, weight="700")]


def translation_start_prok_euk():
    W, H = 640, 132
    START, STOP, SD, CDS = "var(--good)", "var(--bridge)", "var(--visual)", "var(--mod1)"
    y1, y2 = 34, 104
    x0, x1 = 84, 600
    b = [T(12, y1 + 4, "mRNA 1", 10.5, anchor="start", weight="700"),
         T(12, y2 + 4, "mRNA 2", 10.5, anchor="start", weight="700"),
         L(107, y1, 548, y1, stroke=RNA, w=2.5), L(x0, y2, x1, y2, stroke=RNA, w=2.5)]
    for y in (y1, y2):
        b += [T(x0 - 6, y + 4, "5′", 10.5, anchor="end", weight="700"),
              T(x1 + 6, y + 4, "3′", 10.5, anchor="start", weight="700")]
    # mRNA 1: cap, leader, AUG, long coding bar with an internal AUG, UAA, trailer, tail
    b += [C(96, y1, 11, fill="var(--accent)"), T(96, y1 + 3.2, "cap", 9, weight="700", fill="var(--surface)")]
    b += _codon_box(136, y1, 34, "AUG", START)
    b += _box(170, y1, 330, 14, CDS, rx=0, fo=0.2, sw=1.2)
    b += _codon_box(300, y1, 30, "AUG", START, h=12, size=9)
    b += _codon_box(500, y1, 34, "UAA", STOP)
    b += [T(552, y1 + 3.6, "AAAA…A", 10, anchor="start", weight="700", fill="var(--accent)")]
    # mRNA 2: three AGGAGGU - AUG - coding - stop units
    x = 94
    for stop in ("UAA", "UGA", "UAG"):
        b += _box(x, y2, 24, 10, SD, rx=3, fo=0.3, sw=1.2) + [T(x + 12, y2 - 12, "AGGAGGU", 9.5, weight="700", fill=SD)]
        x += 24 + 8
        b += _codon_box(x, y2, 34, "AUG", START)
        x += 34
        b += _box(x, y2, 53, 14, CDS, rx=0, fo=0.2, sw=1.2)
        x += 53
        b += _codon_box(x, y2, 34, stop, STOP)
        x += 34 + 18
    aria = ("Two mRNAs, each drawn 5′ to 3′ from left to right. mRNA 1: a cap at the 5′ end, a short stretch, an AUG box, a "
            "long coding bar that contains a second, smaller AUG mark partway along it, a UAA box, a short stretch and a "
            "tail AAAA…A. mRNA 2: no cap; three coding regions in a row, each preceded by a small box labelled AGGAGGU and "
            "then an AUG box, followed by a coding bar and a box reading UAA, UGA and UAG respectively, with short "
            "stretches between the regions.")
    return "Two mRNAs: where can a ribosome start?", svg(W, H, aria, b)


# ======================================================================
# 3) four snapshots at the rough ER membrane
# ======================================================================

def _ribo(cx, cyl):
    """Ribosome with its large subunit facing the membrane: small subunit on top, large below, mRNA between."""
    return [E(cx, cyl - 22, 21, 10, fill=RIBO, fo=0.3, stroke=RIBO, sw=1.4),
            E(cx, cyl, 30, 16, fill=RIBO, fo=0.3, stroke=RIBO, sw=1.4)]


def _channel(xc, yt, yb, open_=False):
    g_ = 4.5 if open_ else 0
    col = "var(--visual)"
    return [R(xc - g_ - 12, yt, 12, yb - yt, rx=4, fill=col, fo=0.25, stroke=col, sw=1.4),
            R(xc + g_, yt, 12, yb - yt, rx=4, fill=col, fo=0.25, stroke=col, sw=1.4)]


def _receptor(xc, yt, yb):
    return R(xc - 9, yt, 18, yb - yt, rx=6, fill=SOFT, fo=0.22, stroke=SOFT, sw=1.4)


def _srp(x, y, ang=0.0, rx=13, ry=7.5):
    """SRP particle: an ellipse rotated by ang degrees (drawn as a path)."""
    a = math.radians(ang)
    pts = [(x + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a),
            y + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
           for t in (2 * math.pi * k / 48 for k in range(48))]
    return P(_path(pts) + " Z", fill="var(--mod1)", fo=0.5, stroke="var(--mod1)", sw=1.4)


def srp_targeting_steps():
    W, H = 640, 240
    pw, gap = 145, 20
    mt, mb = 158, 184            # lipid head rows
    yr, yc, ybot = 140, 146, 194  # receptor top, channel top, protein bottoms
    X = [i * (pw + gap) for i in range(4)]
    xr, xch = 34, 106            # receptor and channel x (panel-relative)
    b = []
    for i, x0 in enumerate(X):
        b += bilayer(x0 + 4, x0 + pw - 2, mt, mb, step=9, tail_len=9.6, head_r=3.4,
                     skip=[(x0 + xr - 12, x0 + xr + 12), (x0 + xch - 16, x0 + xch + 16)])
        b += badge(x0 + pw / 2, 12, str(i + 1))
        if i < 3:
            b.append(L(x0 + pw + 4, 100, x0 + pw + gap - 4, 100, w=1.5, end="srp_targeting_steps_arr"))
        b.append(_receptor(x0 + xr, yr, ybot))
    # panel 1: ribosome with SRP, well above the membrane
    x0 = X[0]
    b += _channel(x0 + xch, yc, ybot)
    b.append(L(x0 + 40, 50, x0 + 140, 50, stroke=RNA, w=2.2))
    b += _ribo(x0 + 90, 64)
    b.append(chain([(x0 + 90, 80), (x0 + 86, 92), (x0 + 72, 98)]))
    b.append(chain([(x0 + 72, 98), (x0 + 58, 99), (x0 + 48, 94)], color=SIG, sw=3, sign=-1))
    b.append(_srp(x0 + 64, 84, ang=-40, rx=14))
    b += [T(x0 + 4, 30, "cytosol", 9.5, anchor="start", fill=SOFT),
          T(x0 + 47, 80, "SRP", 9.5, anchor="end", weight="700", fill="var(--mod1)"),
          T(x0 + 4, 119, "signal sequence", 9.5, anchor="start", weight="700", fill=SIG),
          T(x0 + xch, 139, "channel", 9.5, weight="700"),
          T(x0 + 4, 208, "SRP receptor", 9.5, anchor="start", weight="700"),
          T(x0 + 4, 234, "ER lumen", 9.5, anchor="start", fill=SOFT)]
    # panel 2: the same complex sitting on the SRP receptor, beside the channel
    x0 = X[1]
    b += _channel(x0 + xch, yc, ybot)
    b.append(L(x0 + 12, 98, x0 + 108, 98, stroke=RNA, w=2.2))
    b += _ribo(x0 + 60, 112)
    b.append(chain([(x0 + 60, 128), (x0 + 57, 138), (x0 + 48, 143)]))
    b.append(chain([(x0 + 48, 143), (x0 + 39, 142), (x0 + 33, 136)], color=SIG, sw=3, sign=-1))
    b.append(_srp(x0 + 38, 131, ang=-50))
    # panel 3: ribosome on the open channel, chain through it, SRP free in the cytosol
    x0 = X[2]
    b.append(L(x0 + 58, 116, x0 + 145, 116, stroke=RNA, w=2.2))
    b.append(L(x0 + xch, 140, x0 + xch, 198, stroke=AA, w=2))
    b.append(chain([(x0 + xch, 198), (x0 + 100, 210), (x0 + 86, 216)]))
    b.append(chain([(x0 + 86, 216), (x0 + 72, 215), (x0 + 62, 208)], color=SIG, sw=3, sign=-1))
    b += _channel(x0 + xch, yc, ybot, open_=True)
    b += _ribo(x0 + xch, 130)
    b.append(_srp(x0 + 34, 74, ang=-35))
    # panel 4: finished protein in the lumen, signal-sequence piece, subunits apart
    x0 = X[3]
    b += _channel(x0 + xch, yc, ybot)
    b.append(L(x0 + 22, 38, x0 + 122, 38, stroke=RNA, w=2.2))
    b += [E(x0 + 46, 66, 21, 10, fill=RIBO, fo=0.3, stroke=RIBO, sw=1.4),
          E(x0 + 104, 94, 30, 16, fill=RIBO, fo=0.3, stroke=RIBO, sw=1.4)]
    b.append(chain([(x0 + 12, 216), (x0 + 24, 230), (x0 + 42, 226), (x0 + 40, 210), (x0 + 58, 208),
                    (x0 + 70, 220), (x0 + 64, 232), (x0 + 84, 232)]))
    b.append(chain([(x0 + 112, 205), (x0 + 122, 210), (x0 + 134, 207)], color=SIG, sw=3))
    aria = ("Four numbered panels, 1 to 4, joined by arrows, each a stretch of rough ER membrane with the cytosol above "
            "and the ER lumen below, and in every panel the membrane holds an SRP receptor and, beside it, a channel. "
            "In panel 1 a ribosome on an mRNA sits well above the membrane, with a short polypeptide coming out of it "
            "whose tip, the signal "
            "sequence, is held by an SRP particle that also touches the ribosome, and the channel is closed; in panel 2 "
            "the same ribosome, SRP and short polypeptide sit with the SRP on the SRP receptor and the ribosome beside "
            "the closed channel. In panel 3 the ribosome sits directly on the open channel, its polypeptide runs through "
            "the channel into the lumen with the signal sequence at the far end, and the SRP is by itself in the cytosol. "
            "In panel 4 a folded polypeptide lies free in the lumen, a short signal-sequence piece lies by itself near the "
            "closed channel, and the ribosome's two subunits lie apart from each other and from the mRNA in the cytosol.")
    return "Four snapshots at the rough ER membrane", svg(W, H, aria, b,
                                                        defs=[marker("srp_targeting_steps_arr", size=5)])


# ======================================================================
# 4) one membrane protein, two membranes
# ======================================================================

def signal_anchor_orientation():
    W, H = 600, 214
    mt, mb = 96, 134             # lipid head rows

    def panel(x0, x1, xc):
        """Membrane crossed once at xc. The chain is point-symmetric about the membrane centre, so its
        shape says nothing about which end is which."""
        out = bilayer(x0 + 6, x1 - 6, mt, mb, step=12, tail_len=14.5, head_r=4.5, skip=[(xc - 9, xc + 9)])
        top = _wave_pts([(xc, mt - 8), (xc + 6, mt - 22), (xc + 22, mt - 34), (xc + 30, mt - 50), (xc + 48, mt - 58)])
        bot = [(2 * xc - x, (mt + mb) - y) for x, y in top]      # the top tail turned 180 degrees
        out += [P(_wave_d(top), stroke=AA, sw=2.2, join="round"), P(_wave_d(bot), stroke=AA, sw=2.2, join="round"),
                L(xc, mt - 9, xc, mb + 9, stroke=SIG, w=6, cap="round")]
        return out, top[-1], bot[-1]

    # left panel: rough ER (cytosol above, lumen below)
    xcL = 118
    b, tL, bL = panel(0, 240, xcL)
    b += [T(120, 16, "rough ER", 10.5, weight="700"),
          T(10, 40, "cytosol", 9.5, anchor="start", fill=SOFT),
          T(232, 206, "ER lumen", 9.5, anchor="end", fill=SOFT),
          T(tL[0] + 6, tL[1] + 4, "COO⁻", 10, anchor="start", weight="700"),
          T(bL[0] - 6, bL[1] + 4, "NH₃⁺", 10, anchor="end", weight="700"),
          T(xcL + 12, mb + 26, "signal-anchor", 9.5, anchor="start", weight="700", fill=SIG),
          T(xcL + 12, mb + 38, "sequence", 9.5, anchor="start", weight="700", fill=SIG)]
    # arrow between the panels
    b += [L(250, 115, 350, 115, w=1.6, end="signal_anchor_orientation_arr"),
          T(300, 106, "vesicle traffic", 9.5, fill=SOFT)]
    # right panel: plasma membrane (extracellular fluid above, cytosol below)
    xcR = 478
    p, tR, bR = panel(360, 600, xcR)
    b += p
    b += [T(480, 16, "plasma membrane", 10.5, weight="700"),
          T(370, 40, "extracellular fluid", 9.5, anchor="start", fill=SOFT),
          T(592, 206, "cytosol", 9.5, anchor="end", fill=SOFT),
          T(tR[0] + 6, tR[1] + 4, "?", 10.5, anchor="start", weight="700"),
          T(bR[0] - 6, bR[1] + 4, "?", 10.5, anchor="end", weight="700")]
    aria = ("Two panels joined by an arrow labelled vesicle traffic. Left panel, rough ER: a membrane with the cytosol above "
            "and the ER lumen below, crossed once by a protein chain whose NH₃⁺ end lies in the lumen and whose COO⁻ end "
            "lies in the cytosol; the straight stretch inside the membrane is highlighted and labelled signal-anchor "
            "sequence. Right panel, plasma membrane: a membrane with the extracellular fluid above and the cytosol below, "
            "crossed once by the same protein chain, with the same highlighted straight stretch inside the membrane; one "
            "end of the chain lies above the membrane and one below, and each end is labelled ?.")
    return "One membrane protein, two membranes", svg(W, H, aria, b, defs=[marker("signal_anchor_orientation_arr")])


ALL = {
    "ribosome_snapshot": ribosome_snapshot,
    "translation_start_prok_euk": translation_start_prok_euk,
    "srp_targeting_steps": srp_targeting_steps,
    "signal_anchor_orientation": signal_anchor_orientation,
}
