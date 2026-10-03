"""Module 5 diagrams, part A: amino-acid side chains, backbone H-bonding, tertiary contacts,
codon -> anticodon, and the genetic code table.

Question-side figures: they show structure and data only (no classifications or rules)."""
import math
from svgkit import *

SOFT = "var(--ink-soft)"


def _spline(points, closed=False):
    """Smooth Catmull-Rom curve through `points`, as an SVG path string of cubic Beziers."""
    p = list(points)
    ext = [p[-1]] + p + [p[0], p[1]] if closed else [p[0]] + p + [p[-1]]
    d = f"M{g(round(p[0][0], 1))},{g(round(p[0][1], 1))}"
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += " C" + " ".join(f"{g(round(x, 1))},{g(round(y, 1))}" for x, y in (c1, c2, p2))
    return d + (" Z" if closed else "")


# ---------------------------------------------------------------------------
# 1. Eight side chains on the same backbone
# ---------------------------------------------------------------------------
def r_group_gallery():
    W, H = 640, 278
    SC = "var(--mod1)"          # every side-chain atom and bond
    FS = 11                     # atom label size
    STEP = 20                   # baseline-to-baseline step down a side chain
    LEAD = {"C": 3.9, "O": 4.3, "S": 3.7, "N": 4.0}   # half-width of the first atom letter

    def vbond(x, y_from, y_to, col=SC):
        return L(x, y_from, x, y_to, stroke=col, w=1.4)

    def panel(x0, y0, h, letter, chain=(), kind=None):
        xC, yB = x0 + 84, y0 + 50
        out = [R(x0 + 3, y0 + 3, 154, h - 6, rx=8, stroke="var(--border)", sw=1)]
        out += badge(x0 + 17, y0 + 17, letter)
        out += [T(xC - 17, yB, "H₂N⁺" if kind == "pro" else "H₃N⁺", FS, anchor="end"),
                L(xC - 15, yB - 4, xC - 6, yB - 4, w=1.4),
                T(xC, yB, "C", FS),
                L(xC + 6, yB - 4, xC + 15, yB - 4, w=1.4),
                T(xC + 17, yB, "COO⁻", FS, anchor="start"),
                vbond(xC, yB - 10.5, yB - 19.5, "currentColor"),
                T(xC, yB - 22, "H", FS)]
        for i, grp in enumerate(chain):
            yk = yB + STEP * (i + 1)
            out.append(vbond(xC, yB + STEP * i + 2.5, yk - 10.5))
            if grp == "H":
                out.append(T(xC, yk, "H", FS, fill=SC))
            else:
                out.append(T(xC - LEAD[grp[0]], yk, grp, FS, anchor="start", fill=SC))
        if kind == "ring":            # CH2 then a benzene ring
            y_top = yB + STEP + 2.5
            cy = y_top + 7 + 13
            out += [vbond(xC, y_top, cy - 13),
                    hexagon(xC, cy, 13, stroke=SC, sw=1.4),
                    C(xC, cy, 7.5, stroke=SC, sw=1.2)]
        if kind == "pro":             # N, C-alpha and three CH2 close a five-membered ring
            xN = xC - 27
            xM = (xN + xC) / 2
            y2, y3 = yB + STEP, yB + 42
            out += [vbond(xN, yB + 2.5, y2 - 10.5), vbond(xC, yB + 2.5, y2 - 10.5),
                    T(xN + 4, y2, "H₂C", FS, anchor="end", fill=SC),
                    T(xC - 3.9, y2, "CH₂", FS, anchor="start", fill=SC),
                    L(xN + 1.5, y2 + 3, xM - 1.5, y3 - 11, stroke=SC, w=1.4),
                    L(xC - 1.5, y2 + 3, xM + 1.5, y3 - 11, stroke=SC, w=1.4),
                    T(xM - 3.9, y3, "CH₂", FS, anchor="start", fill=SC)]
        return out

    rows = [(0, 162), (162, 116)]
    specs = [("A", ("CH₃",), None), ("B", ("CH₂", "OH"), None), ("C", ("CH₂", "COO⁻"), None),
             ("D", ("CH₂", "CH₂", "CH₂", "CH₂", "NH₃⁺"), None),
             ("E", ("CH₂", "SH"), None), ("F", ("H",), None), ("G", ("CH₂",), "ring"), ("H", (), "pro")]
    b = []
    for i, (letter, chain, kind) in enumerate(specs):
        y0, h = rows[i // 4]
        b += panel(160 * (i % 4), y0, h, letter, chain, kind)
    aria = ("Eight panels lettered A to H, each drawing the same backbone, H₃N⁺, a central C and COO⁻ bonded in a row "
            "from left to right, with an H bonded above the central C and a different side chain bonded below it. "
            "Side chains, from the central C downward: A, CH₃; B, CH₂ then OH; C, CH₂ then COO⁻; D, four CH₂ groups in "
            "a row then NH₃⁺; E, CH₂ then SH; F, a second H; G, CH₂ then a benzene ring; H, three CH₂ groups that bond "
            "back to the backbone nitrogen (written H₂N⁺ in this panel), closing a five-membered ring of that N, the "
            "central C and the three CH₂ groups")
    return "Eight side chains on the same backbone", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
# 2. Backbone hydrogen bonds in a helix and a sheet
# ---------------------------------------------------------------------------
def backbone_hbond_patterns():
    W, H = 640, 256
    BB = "var(--mod1)"
    RC = "var(--accent)"
    HB = dict(stroke=SOFT, w=1.4, dash="3 2.5")
    b = [T(118, 16, "helix", 11, weight="700"), T(462, 16, "sheet", 11, weight="700"),
         L(268, 8, 268, 248, stroke="var(--border)", w=1)]

    # ---- helix: 4 residues per turn, so residue n and n+4 share a column ----
    # x = cx + rad*sin(phi); phi grows with height, so the front (cos(phi) > 0) climbs left -> right
    # (right-handed). A slight tilt drops the front of each turn so the coil reads as 3-D.
    cx, y1, rise, rad, phi1, tilt, hw = 118, 230, 19, 46, 15, 0.12, 4.5

    def hpos(t):
        ph = math.radians(phi1 + 90 * (t - 1))
        return cx + rad * math.sin(ph), y1 - rise * (t - 1) + tilt * rad * math.cos(ph), math.cos(ph)

    runs, cur, front = [], [], None
    for i in range(0, 201):
        x, y, dz = hpos(1 + i * 0.05)
        f = dz >= 0
        if front is None or f == front:
            cur.append((x, y))
        else:
            runs.append((front, cur))
            cur = [cur[-1], (x, y)]
        front = f
    runs.append((front, cur))

    def band(r, fo, so):
        edge = [(x, y - hw) for x, y in r] + [(x, y + hw) for x, y in reversed(r)]
        return f'<polygon points="{pts(edge)}" fill="{BB}" fill-opacity="{fo}" stroke="{BB}" stroke-width="1" ' \
               f'stroke-opacity="{so}" stroke-linejoin="round"/>'
    rr = 7.5
    pos = {k: hpos(k) for k in range(1, 12)}

    def hbond(n):
        (xa, ya, _), (xb, yb, _) = pos[n], pos[n + 4]
        return L(xa, ya - rr - 1, xb, yb + rr + 1, **HB)
    back_pairs = [n for n in range(1, 8) if pos[n][2] < 0]
    front_pairs = [n for n in range(1, 8) if pos[n][2] >= 0]
    b += [band(r, 0.12, 0.45) for f, r in runs if not f]
    b += [hbond(n) for n in back_pairs]
    b += [band(r, 0.42, 0.9) for f, r in runs if f]
    b += [hbond(n) for n in front_pairs]
    # atom labels on the 1-5 bond: C=O just above residue 1, H-N just below residue 5
    x1_, y1_, _ = pos[1]
    x5_, y5_, _ = pos[5]
    b += [MASK(x1_ - 12, y1_ - 26, 24, 12), T(x1_, y1_ - 16.5, "C=O", 9, weight="700"),
          MASK(x5_ - 12, y5_ + 11, 24, 12), T(x5_, y5_ + 20.5, "H–N", 9, weight="700")]
    # R stubs on the coil's left and right edges
    for k in (4, 8, 2, 6, 10):
        x, y, _ = pos[k]
        sgn = -1 if x < cx else 1
        b += [L(x + sgn * (rr + 1), y, x + sgn * (rr + 11), y, stroke=RC, w=1.6),
              T(x + sgn * (rr + 13), y + 3.6, "R", 10, anchor="end" if sgn < 0 else "start", weight="700", fill=RC)]
    for k in range(1, 12):
        x, y, _ = pos[k]
        b += [MASK(x - rr, y - rr, 2 * rr, 2 * rr, rx=rr), C(x, y, rr, fill=BB),
              T(x, y + 3.2, str(k), 9, weight="700", fill="var(--surface)")]
    b += [T(pos[1][0] - rr - 4, pos[1][1] + 3.5, "N-terminus", 9.5, anchor="end", fill=SOFT),
          T(pos[11][0] - rr - 4, pos[11][1] + 3.5, "C-terminus", 9.5, anchor="end", fill=SOFT)]

    # ---- sheet: two strands as flat arrows, residues directly across ----
    yt, yb_, body, head, hl = 78, 148, 11, 19, 24
    xl, xr = 318, 604
    top = [(xl, yt - body), (xr - hl, yt - body), (xr - hl, yt - head), (xr, yt), (xr - hl, yt + head),
           (xr - hl, yt + body), (xl, yt + body)]
    bot = [(xr, yb_ - body), (xl + hl, yb_ - body), (xl + hl, yb_ - head), (xl, yb_), (xl + hl, yb_ + head),
           (xl + hl, yb_ + body), (xr, yb_ + body)]
    b += [PG(top, fill=BB, fo=0.16, stroke=BB, sw=1.4), PG(bot, fill=BB, fo=0.16, stroke=BB, sw=1.4),
          T(xl - 6, yt + 4, "N", 10.5, anchor="end", weight="700"), T(xr + 6, yt + 4, "C", 10.5, anchor="start", weight="700"),
          T(xl - 6, yb_ + 4, "C", 10.5, anchor="end", weight="700"), T(xr + 6, yb_ + 4, "N", 10.5, anchor="start", weight="700")]
    xs = [360, 410, 460, 510, 560]
    rg, rgr = 30, 7

    def rgroup(x, y, filled):
        if filled:
            return [C(x, y, rgr, fill=RC), T(x, y + 3.4, "R", 9, weight="700", fill="var(--surface)")]
        return [C(x, y, rgr, fill="var(--surface)", stroke=RC, sw=1.5), T(x, y + 3.4, "R", 9, weight="700", fill=RC)]
    for i, x in enumerate(xs):
        filled = i % 2 == 0
        b += [L(x, yt - 5, x, yt - rg + rgr, stroke=RC, w=1.4), L(x, yb_ + 5, x, yb_ + rg - rgr, stroke=RC, w=1.4),
              L(x, yt + 6, x, yb_ - 6, **HB)]
        b += rgroup(x, yt - rg, filled) + rgroup(x, yb_ + rg, filled)
        b += [C(x, yt, 4.5, fill=BB), C(x, yb_, 4.5, fill=BB)]
    b += [MASK(448, 92, 24, 12), T(460, 101.5, "C=O", 9, weight="700"),
          MASK(448, 122, 24, 12), T(460, 131.5, "H–N", 9, weight="700")]
    # key
    b += rgroup(300, 216, True) + [T(311, 219.5, "R above the sheet", 9.5, anchor="start", fill=SOFT)]
    b += rgroup(428, 216, False) + [T(439, 219.5, "R below the sheet", 9.5, anchor="start", fill=SOFT)]
    b += [L(292, 238, 312, 238, **HB), T(318, 241.5, "hydrogen bond", 9.5, anchor="start", fill=SOFT)]
    aria = ("Left, labelled helix: a ribbon coil rising upward through residues numbered 1 at the bottom (N-terminus) to "
            "11 at the top (C-terminus), its front strands climbing from lower left to upper right; dashed lines join "
            "residues 1–5, 2–6, 3–7, 4–8, 5–9, 6–10 and 7–11, the 1–5 line labelled C=O at residue 1 and H–N at "
            "residue 5, and short stubs labelled R point outward from residues 4 and 8 on the left edge and 2, 6 and 10 "
            "on the right edge. Right, labelled sheet: two strands drawn as broad arrows, the top one running from N at "
            "its left end to C at its arrowhead on the right and the bottom one from N at its right end to C at its "
            "arrowhead on the left, each with five residues directly across from the other strand's, and every facing "
            "pair joined by a vertical dashed line, one of them labelled C=O at the top strand and H–N at the bottom "
            "strand. Each sheet residue carries a circle labelled R on the outer side of its strand, alternately filled "
            "and hollow along each strand, with facing residues matching; a key reads filled R circle, R above the "
            "sheet; hollow R circle, R below the sheet; dashed line, hydrogen bond")
    return "Backbone hydrogen bonds in a helix and a sheet", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
# 3. Four contacts inside one folded chain
# ---------------------------------------------------------------------------
def tertiary_interactions_map():
    W, H = 560, 280
    CH = "var(--mod1)"
    DOT = dict(stroke=SOFT, w=1.6, dash="1.5 3", cap="round")
    blob = []                      # a slightly wobbly superellipse: roughly round, roomy corners
    for k in range(20):
        a = 2 * math.pi * k / 20
        c, s = math.cos(a), math.sin(a)
        r = (abs(c / 252) ** 2.5 + abs(s / 121) ** 2.5) ** (-1 / 2.5) * (1 + 0.025 * math.sin(3 * a + 0.7))
        blob.append((280 + r * c, 147 + r * s))
    chain = [(110, 66), (90, 100), (82, 150), (90, 205), (110, 236), (138, 244), (164, 230), (180, 190), (184, 130),
             (176, 84), (186, 56), (210, 45), (234, 56), (240, 84), (226, 132), (230, 190), (250, 228), (302, 244),
             (354, 228), (374, 190), (380, 140), (370, 102), (358, 80), (366, 56), (394, 45), (422, 54), (450, 86),
             (466, 140), (462, 196), (446, 228)]
    b = [P(_spline(blob, closed=True), fill=CH, fo=0.03, stroke="var(--ink-faint)", sw=1.3, dash="5 4"),
         T(14, 20, "water", 9.5, anchor="start", italic=True, fill=SOFT),
         T(546, 274, "water", 9.5, anchor="end", italic=True, fill=SOFT),
         E(300, 166, 70, 56, fill="var(--mod2)", fo=0.14),
         P(_spline(chain), stroke=CH, sw=5, join="round"),
         T(120, 70, "N", 10.5, anchor="start", weight="700"), T(438, 234, "C", 10.5, anchor="end", weight="700")]
    # A: CH2-S-S-CH2 bridge between the first two segments
    b += [L(85, 152, 98, 152, w=1.4), T(133, 156, "CH₂–S–S–CH₂", 10), L(168, 152, 181, 152, w=1.4)]
    b += badge(133, 135, "A")
    # B: COO- facing +H3N at the outer surface (top, between two segment tops)
    b += [L(238, 62, 250, 62, w=1.4), T(252, 66, "COO⁻", 10, anchor="start"),
          L(286, 62, 313, 62, **DOT), T(316, 66, "⁺H₃N", 10, anchor="start"), L(345, 62, 361, 62, w=1.4)]
    b += badge(299, 44, "B")
    # C: OH facing O=C
    b += [L(380, 180, 390, 180, w=1.4), T(392, 184, "OH", 10, anchor="start"),
          L(410, 180, 425, 180, **DOT), T(427, 184, "O=C", 10, anchor="start"), L(453, 180, 462, 180, w=1.4)]
    b += badge(422, 162, "C")
    # D: small side groups from several segments packed inside the shaded oval
    b += [L(229, 140, 246, 140, w=1.4), T(248, 144, "CH(CH₃)₂", 10, anchor="start"),
          L(378, 154, 360, 154, w=1.4), T(358, 158, "H₃C", 10, anchor="end"),
          L(233, 192, 246, 192, w=1.4), T(248, 196, "CH₃", 10, anchor="start"),
          L(316, 239, 316, 216, w=1.4), hexagon(316, 205, 11, stroke="currentColor", sw=1.4),
          C(316, 205, 6.2, stroke="currentColor", sw=1.2)]
    b += badge(347, 122, "D")
    aria = ("One chain, drawn as a thick line from N to C, folds back and forth inside a roughly round dashed outline, "
            "with the word water written outside the outline. Four contacts between different parts of the chain are "
            "lettered: A, CH₂–S–S–CH₂, one CH₂ on each of two segments; B, just inside the outline at the top, COO⁻ on "
            "one segment facing ⁺H₃N on another, joined by a dotted line; C, OH on one segment facing O=C on another, "
            "joined by a dotted line; D, in the middle of the fold, a CH(CH₃)₂, two CH₃ groups and a six-membered ring "
            "reaching in from the segments around it, packed together inside a lightly shaded oval")
    return "Four contacts inside one folded chain", svg(W, H, aria, b)


# ---------------------------------------------------------------------------
# 4. One codon traced from gene to tRNA
# ---------------------------------------------------------------------------
def trna_codon_pairing():
    W, H = 640, 230
    TR = "var(--accent)"
    PAIR = dict(stroke=SOFT, w=1.2)
    # one strand: 5' end -> acceptor stem -> left arm/loop -> anticodon arm/loop -> right arm/loop -> acceptor stem
    d = ("M83,60 V102 H47 A15.8,15.8 0 1 0 47,120 H83 V160 C70,168 64,182 69,194 H115 "
         "C120,182 114,168 101,160 V120 H137 A15.8,15.8 0 1 0 137,102 H101 V60")
    b = [P(d, stroke=TR, sw=2.6, join="round")]
    for y in (68, 77, 86, 95):
        b.append(L(85, y, 99, y, **PAIR))
    for y in (128, 137, 146, 155):
        b.append(L(85, y, 99, y, **PAIR))
    for x in (55, 64, 73):
        b.append(L(x, 104, x, 118, **PAIR))
    for x in (111, 120, 129):
        b.append(L(x, 104, x, 118, **PAIR))
    for x in (77, 92, 107):
        b += [R(x - 6.5, 187.5, 13, 13, rx=2, fill="var(--surface)"),
              R(x - 6.5, 187.5, 13, 13, rx=2, fill=TR, fo=0.18, stroke=TR, sw=1.5)]
    b += [T(83, 54, "5′", 10, weight="700"),
          T(101, 56, "C", 10, weight="700", fill=TR), T(101, 44, "C", 10, weight="700", fill=TR),
          T(101, 32, "A", 10, weight="700", fill=TR), T(101, 19, "3′", 10, weight="700"),
          L(122, 15.5, 110, 15.5, w=1.2, end="trna_codon_pairing_arr"),
          T(125, 19, "amino acid attachment site", 9, anchor="start", fill=SOFT),
          T(122, 186, "anticodon loop", 9.5, anchor="start", fill=SOFT),
          P("M70.5,206 V210 H113.5 V206", stroke=SOFT, sw=1.2), T(92, 222, "anticodon", 9.5, fill=SOFT)]
    # rows: DNA nontemplate, DNA template, mRNA codon, tRNA anticodon
    rows = [(50, "DNA nontemplate strand", "var(--bridge)", "5′", "GCA", "3′"),
            (78, "DNA template strand", "var(--mod1)", "3′", "CGT", "5′"),
            (136, "mRNA codon", "var(--review)", "5′", "GCA", "3′"),
            (194, "tRNA anticodon", TR, "3′", "CGU", "5′")]
    bx = [424, 452, 480]
    for y, name, col, lp, seq, rp in rows:
        b.append(T(240, y + 3.5, name, 10, anchor="start", weight="700", fill=col))
        b += [T(398, y + 4, lp, 10.5, weight="700"), T(506, y + 4, rp, 10.5, weight="700")]
        for x, base in zip(bx, seq):
            b += [R(x - 12, y - 12, 24, 24, rx=3, fill=col, fo=0.18, stroke=col),
                  T(x, y + 4, base, 11.5, weight="700")]
    b += [P("M518,82 H532 V132 H521", stroke="currentColor", sw=1.3, end="trna_codon_pairing_arr"),
          T(539, 110.5, "transcription", 9.5, anchor="start"),
          P("M518,140 H532 V190 H521", stroke="currentColor", sw=1.3, end="trna_codon_pairing_arr"),
          T(539, 168.5, "base pairing", 9.5, anchor="start")]
    aria = ("Left: a tRNA cloverleaf, one strand folded into base-paired stems, with the acceptor stem at the top, where "
            "one strand ends at 5′ and the other continues past the stem as unpaired C, C, A to the 3′ end, labelled "
            "amino acid attachment site; below are a left loop, a right loop and a bottom loop labelled anticodon loop, "
            "in which three empty boxes are labelled anticodon. Right: four aligned rows of three bases in boxes: DNA "
            "nontemplate strand 5′ G C A 3′; DNA template strand 3′ C G T 5′; mRNA codon 5′ G C A 3′; tRNA anticodon "
            "3′ C G U 5′. An arrow labelled transcription runs from the template-strand row to the mRNA row, and an "
            "arrow labelled base pairing runs from the mRNA row to the anticodon row")
    return "One codon traced from gene to tRNA", svg(W, H, aria, b, defs=[marker("trna_codon_pairing_arr")])


# ---------------------------------------------------------------------------
# 5. The standard genetic code
# ---------------------------------------------------------------------------
CODE_TEXT = """
UUU Phe UUC Phe UUA Leu UUG Leu | UCU Ser UCC Ser UCA Ser UCG Ser | UAU Tyr UAC Tyr UAA Stop UAG Stop | UGU Cys UGC Cys UGA Stop UGG Trp
CUU Leu CUC Leu CUA Leu CUG Leu | CCU Pro CCC Pro CCA Pro CCG Pro | CAU His CAC His CAA Gln CAG Gln | CGU Arg CGC Arg CGA Arg CGG Arg
AUU Ile AUC Ile AUA Ile AUG Met | ACU Thr ACC Thr ACA Thr ACG Thr | AAU Asn AAC Asn AAA Lys AAG Lys | AGU Ser AGC Ser AGA Arg AGG Arg
GUU Val GUC Val GUA Val GUG Val | GCU Ala GCC Ala GCA Ala GCG Ala | GAU Asp GAC Asp GAA Glu GAG Glu | GGU Gly GGC Gly GGA Gly GGG Gly
"""


def _genetic_code():
    toks = CODE_TEXT.replace("|", " ").split()
    code = dict(zip(toks[0::2], toks[1::2]))
    assert len(code) == 64 and len(toks) == 128
    assert sum(v == "Stop" for v in code.values()) == 3
    bases = "UCAG"
    assert set(code) == {a + b + c for a in bases for b in bases for c in bases}
    return code


def genetic_code_table():
    code = _genetic_code()
    W, H = 640, 318
    B = "UCAG"
    x_left, x_right, col_w = 48, 596, 137
    y_top, blk = 42, 68
    STOP = "var(--review)"
    b = [T(6, 15, "1st base", 10, anchor="start", fill=SOFT), T(322, 15, "2nd base", 10, fill=SOFT),
         T(634, 15, "3rd base", 10, anchor="end", fill=SOFT)]
    for j, s in enumerate(B):
        b.append(T(x_left + col_w * j + col_w / 2, 36, s, 11.5, weight="700"))
    # grid
    for i in range(5):
        b.append(L(6, y_top + blk * i, 634, y_top + blk * i, stroke="var(--border)", w=1))
    for j in range(5):
        b.append(L(x_left + col_w * j, 23, x_left + col_w * j, y_top + 4 * blk, stroke="var(--border)", w=1))
    for i, first in enumerate(B):
        yb = y_top + blk * i
        b.append(T(25, yb + blk / 2 + 4, first, 11.5, weight="700"))
        for k, third in enumerate(B):
            y = yb + 17 + 14 * k
            b.append(T((x_right + W) / 2, y, third, 10.5, weight="700"))
            for j, second in enumerate(B):
                cod = first + second + third
                aa = code[cod]
                x0 = x_left + col_w * j
                col = STOP if aa == "Stop" else "currentColor"
                b += [T(x0 + 28, y, cod, 10.5, anchor="start", fill=col),
                      T(x0 + 62, y, aa, 10.5, anchor="start", fill=col)]
                if cod == "AUG":
                    b += [R(x0 + 91, y - 9.5, 32, 12.5, rx=6, fill="var(--good)", fo=0.15, stroke="var(--good)", sw=1),
                          T(x0 + 107, y, "start", 9, weight="700", fill="var(--good)")]
    rows_txt = []
    for first in B:
        cells = ", ".join(f"{c} {code[c]}" for c in (first + s + t for s in B for t in B))
        rows_txt.append(f"1st base {first}: {cells}")
    aria = ("A 4 × 4 table of the 64 mRNA codons: row blocks by 1st base (U, C, A, G, down the left), columns by 2nd "
            "base (U, C, A, G, across the top), and the 3rd base (U, C, A, G) listed down the right of every row "
            "block; each codon is followed by a three-letter amino-acid abbreviation or Stop, the three Stop entries "
            "are tinted, and AUG Met carries a small start tag. Entries by row block (2nd base U, C, A, G in turn): "
            + "; ".join(rows_txt))
    return "The standard genetic code (mRNA codons, read 5′→3′)", svg(W, H, aria, b)


ALL = {
    "r_group_gallery": r_group_gallery,
    "backbone_hbond_patterns": backbone_hbond_patterns,
    "tertiary_interactions_map": tertiary_interactions_map,
    "trna_codon_pairing": trna_codon_pairing,
    "genetic_code_table": genetic_code_table,
}
