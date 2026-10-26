"""Module 8 diagrams (photosynthesis), including the five case-study diagrams."""
import math
from svgkit import *
from dkit import node, arrow, axes, table


def _g(x, mu, sd):
    return math.exp(-0.5 * ((x - mu) / sd) ** 2)


def _chl_a(w):
    return 0.95 * _g(w, 430, 15) + 0.2 * _g(w, 412, 10) + 0.74 * _g(w, 662, 11) + 0.12 * _g(w, 615, 14) + 0.03


def _chl_b(w):
    return 1.0 * _g(w, 455, 15) + 0.33 * _g(w, 642, 11) + 0.12 * _g(w, 595, 14) + 0.03


def _carot(w):
    return 0.62 * _g(w, 425, 11) + 0.85 * _g(w, 450, 12) + 0.72 * _g(w, 478, 11)


def _spectrum_frame(x0, y0, w, h, ylabel="absorbance (relative)"):
    X = lambda nm: x0 + (nm - 400) / 300 * w
    p = [axes(x0, y0, w, h, [(X(nm) - x0, nm) for nm in (400, 450, 500, 550, 600, 650, 700)],
              [(f * h, lab) for f, lab in ((0, "0"), (0.5, "0.5"), (1, "1.0"))], "wavelength (nm)", ylabel, ylab_dx=34)]
    for lo, hi, nm in ((400, 490, "violet-blue"), (490, 570, "green"), (570, 700, "yellow-orange-red")):
        p.append(text((X(lo) + X(hi)) / 2, y0 + 44, nm, size=9.5, fill=SOFT))
    return p, X


def _curve(fn, X, y0, h, color, dash=None, width=2.2):
    pts = [(X(nm), y0 - min(fn(nm), 1.05) * h) for nm in range(400, 701, 2)]
    return path("M" + " L".join(f"{n(a)},{n(b)}" for a, b in pts), stroke=color, width=width, dash=dash)


def m8_chloroplast():
    K = "m8_chloroplast"
    p = [rect(30, 30, 420, 200, rx=95, fill=MOD2, fill_opacity=0.08, stroke=MOD2, width=2.2),
         rect(42, 42, 396, 176, rx=84, fill=MOD2, fill_opacity=0.08, stroke=MOD2, width=1.6)]
    for gx in (130, 240, 350):
        for k in range(5):
            y = 92 + k * 17
            p.append(rect(gx - 32, y, 64, 13, rx=6, fill=GOOD, fill_opacity=0.35, stroke=GOOD, width=1.2))
    for gx in (162, 272):
        p.append(line(gx, 133, gx + 46, 133, stroke=GOOD, width=3))
    p += [text(250, 70, "stroma", size=11, weight="700"),
          line(382, 98, 470, 60, stroke=SOFT, width=1), text(474, 60, "thylakoid membrane", size=10.5, anchor="start"),
          line(366, 132, 470, 112, stroke=SOFT, width=1), text(474, 116, "thylakoid lumen", size=10.5, anchor="start"),
          line(386, 152, 470, 162, stroke=SOFT, width=1), text(474, 166, "granum (stack)", size=10.5, anchor="start"),
          line(400, 204, 470, 212, stroke=SOFT, width=1), text(474, 216, "inner membrane", size=10.5, anchor="start"),
          line(388, 224, 470, 246, stroke=SOFT, width=1), text(474, 250, "outer membrane", size=10.5, anchor="start")]
    return ("A chloroplast", svg(600, 262,
            "A chloroplast drawn as two nested rounded outlines, the outer and inner membranes. Inside, the fluid stroma "
            "surrounds three stacks of flattened thylakoid sacs (grana) joined by short connecting membranes. Labels point "
            "to a thylakoid membrane, the thylakoid lumen inside one sac, a granum, the inner membrane and the outer membrane.", p))


def m8_sunlight_budget():
    K = "m8_sunlight_budget"
    rows = [("outside the range plants can use", 60, FAINT), ("reflected or transmitted", 8, VISUAL),
            ("converted into heat", 8, REVIEW), ("lost during carbohydrate synthesis", 20, ACCENT),
            ("stored in carbohydrate (maximum)", 4, GOOD)]
    x0, scale = 250, 5.2
    p = [text(20, 22, "Share of the sunlight that reaches a leaf (100%)", size=11, anchor="start", weight="700")]
    for i, (lab, v, col) in enumerate(rows):
        y = 40 + i * 34
        p.append(text(x0 - 10, y + 17, lab, size=10.5, anchor="end"))
        p.append(rect(x0, y + 4, v * scale, 20, rx=3, fill=col, fill_opacity=0.85))
        p.append(text(x0 + v * scale + 8, y + 19, f"{v}%", size=10.5, anchor="start", weight="700"))
    p.append(text(20, 222, "\"Lost during carbohydrate synthesis\" includes photorespiration.", size=9.5, anchor="start", fill=SOFT))
    return ("Where a leaf's sunlight goes", svg(640, 232,
            "Horizontal bar chart of the sunlight reaching a leaf: 60% is outside the range plants can use, 8% is "
            "reflected or transmitted, 8% is converted into heat, 20% is lost during carbohydrate synthesis (including "
            "photorespiration), and at most 4% is stored in carbohydrate.", p))


def m8_o18_table():
    K = "m8_o18_table"
    rows = [["experiment", "18O in water", "18O in CO2", "18O in O2 released"],
            ["1", "0.85%", "0.20%", "0.84%"],
            ["2", "0.20%", "0.68%", "0.20%"]]
    p = [table(20, 16, [110, 130, 130, 170], rows, row_h=30, size=11, first_col_anchor="middle"),
         text(290, 124, "Values are the % of oxygen atoms that are the heavy isotope 18O (natural level: about 0.20%).",
              size=9.5, fill=SOFT),
         text(290, 140, "Algae photosynthesizing in light; CO2 supplied as bicarbonate. Based on Ruben and colleagues, 1941.",
              size=9.5, fill=SOFT)]
    return ("Two oxygen-labelling experiments", svg(580, 152,
            "Table of two experiments with photosynthesizing algae, giving the percentage of oxygen atoms that are 18O. "
            "Experiment 1: water 0.85%, CO2 0.20%, O2 released 0.84%. Experiment 2: water 0.20%, CO2 0.68%, O2 released "
            "0.20%. The natural level is about 0.20%.", p))


def m8_absorption_spectra():
    K = "m8_absorption_spectra"
    x0, y0, w, h = 66, 214, 420, 180
    p, X = _spectrum_frame(x0, y0, w, h)
    p.append(_curve(_chl_a, X, y0, h, MOD2))
    p.append(_curve(_chl_b, X, y0, h, MOD1, dash="7 4"))
    p.append(_curve(_carot, X, y0, h, ACCENT, dash="2 3"))
    lx, ly = 506, 50
    for i, (lab, col, dash) in enumerate((("chlorophyll a", MOD2, None), ("chlorophyll b", MOD1, "7 4"),
                                          ("a carotenoid", ACCENT, "2 3"))):
        p.append(line(lx, ly + i * 22 - 4, lx + 26, ly + i * 22 - 4, stroke=col, width=2.4, dash=dash))
        p.append(text(lx + 32, ly + i * 22, lab, size=10.5, anchor="start"))
    return ("Absorption by three leaf pigments", svg(640, 272,
            "Absorption spectra from 400 to 700 nm. Chlorophyll a peaks near 430 nm and near 662 nm. Chlorophyll b peaks "
            "near 455 nm and near 642 nm. A carotenoid absorbs only between about 400 and 520 nm, with peaks near 425, 450 "
            "and 478 nm. All three absorb little between about 520 and 600 nm, the green-yellow region.", p))


def m8_led_bands():
    K = "m8_led_bands"
    x0, y0, w, h = 66, 224, 420, 180
    p, X = _spectrum_frame(x0, y0, w, h)
    for nm, lab, col in ((450, "blue LED", VISUAL), (530, "green LED", GOOD), (660, "red LED", REVIEW)):
        p.append(rect(X(nm) - 8, y0 - h, 16, h, fill=col, fill_opacity=0.18))
        p.append(text(X(nm), y0 - h - 10, f"{lab} ({nm} nm)", size=9.5, weight="700", fill=col))
    comb = lambda w_: _chl_a(w_) + _chl_b(w_)
    top = max(comb(nm) for nm in range(400, 701))
    p.append(_curve(lambda w_: 0.92 * comb(w_) / top, X, y0, h, MOD2, width=2.4))
    p.append(text(520, 40, "chlorophyll a + b", size=10.5, anchor="start", fill=MOD2, weight="700"))
    p.append(text(520, 54, "(combined absorption)", size=9.5, anchor="start", fill=SOFT))
    return ("Chlorophyll and three LED colours", svg(640, 282,
            "The combined absorption spectrum of chlorophylls a and b from 400 to 700 nm, high in the blue (peak near 440 "
            "nm) and red (near 650-660 nm) and low between about 520 and 600 nm. Three shaded bands mark LEDs: blue at 450 "
            "nm, green at 530 nm and red at 660 nm.", p))


def m8_chlorophyll():
    K = "m8_chlorophyll"
    cx, cy = 130, 110
    p = []
    rings = {}
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        px, py = cx + 48 * math.cos(a), cy + 48 * math.sin(a)
        # one vertex (the N atom) points at the Mg in the centre
        pts = [(px + 18 * math.cos(a + math.pi + math.radians(72 * k)), py + 18 * math.sin(a + math.pi + math.radians(72 * k)))
               for k in range(5)]
        rings[ang] = pts
        p.append(polygon(pts, fill=MOD2, fill_opacity=0.25, stroke=MOD2, width=1.6))
    for ang in (45, 135, 225, 315):
        # a one-carbon bridge joins each pyrrole to the next, closing the big ring
        m = math.radians(ang + 45)
        mx, my = cx + 60 * math.cos(m), cy + 60 * math.sin(m)
        va = min(rings[ang], key=lambda v: (v[0] - mx) ** 2 + (v[1] - my) ** 2)
        vb = min(rings[(ang + 90) % 360], key=lambda v: (v[0] - mx) ** 2 + (v[1] - my) ** 2)
        p.append(polyline([va, (mx, my), vb], stroke=MOD2, width=1.6))
    for ang in (45, 135, 225, 315):
        nx, ny = rings[ang][0]
        a = math.radians(ang)
        p.append(line(nx, ny, cx + 15 * math.cos(a), cy + 15 * math.sin(a), stroke=INK, width=1.4))
        p.append(label_box(nx, ny + 3.2, "N", size=9, pad=1.5, weight="700"))
    p.append(circle(cx, cy, 15, fill=SURFACE, stroke=ACCENT, width=1.6))
    p.append(text(cx, cy + 4, "Mg", size=11, weight="700"))
    # the tail is bonded to the lower-right pyrrole
    a = math.radians(45)
    tx, ty = min(rings[45], key=lambda v: (v[0] - 172) ** 2 + (v[1] - 182) ** 2)
    zig = [(tx, ty), (172, 182)]
    for k in range(1, 14):
        zig.append((172 + 26 * k, 182 + (10 if k % 2 else 0)))
    p.append(polyline(zig, stroke=ACCENT, width=2.4))
    p += [text(cx, 26, "porphyrin ring", size=11, weight="700"),
          text(300, 214, "hydrocarbon (phytol) tail", size=11, weight="700"),
          text(250, 92, "N atoms of the ring hold the", size=9.5, anchor="start", fill=SOFT),
          text(250, 106, "Mg ion at the centre", size=9.5, anchor="start", fill=SOFT)]
    return ("Chlorophyll's two parts", svg(560, 230,
            "Schematic of a chlorophyll molecule: a flat porphyrin ring made of four five-membered rings joined by short "
            "bridges into one large ring, whose four N atoms are bonded to a central Mg ion, and a long zigzag hydrocarbon "
            "(phytol) tail bonded to one of the small rings.", p))


def m8_photosystem():
    K = "m8_photosystem"
    A = f"{K}_a"
    cx, cy = 210, 130
    p = [ellipse(cx, cy, 170, 92, fill=MOD2, fill_opacity=0.07, stroke=MOD2, width=1.6)]
    for k in range(12):
        a = math.radians(30 * k + 15)
        for rr in (72, 128):
            if rr == 120 and k % 2:
                continue
            x, y = cx + rr * math.cos(a), cy + rr * 0.62 * math.sin(a)
            p.append(circle(x, y, 9, fill=GOOD, fill_opacity=0.45, stroke=GOOD, width=1.2))
    p.append(circle(cx - 11, cy, 10, fill=ACCENT, fill_opacity=0.6, stroke=ACCENT, width=1.4))
    p.append(circle(cx + 11, cy, 10, fill=ACCENT, fill_opacity=0.6, stroke=ACCENT, width=1.4))
    p += [node(420, 40, 150, 34, "electron acceptor", color=VISUAL, size=10.5),
          node(420, 186, 150, 34, "electron donor", color=VISUAL, size=10.5),
          line(cx + 24, cy - 6, 416, 60, stroke=SOFT, width=1, dash="3 3"),
          line(cx + 24, cy + 6, 416, 200, stroke=SOFT, width=1, dash="3 3"),
          text(cx, 22, "light", size=10.5, fill=ACCENT, weight="700"),
          path(f"M{cx-60},28 q6,8 0,16 q-6,8 0,16 q6,8 0,16", stroke=ACCENT, width=1.8, end=A),
          label_box(cx, cy + 26, "reaction-center pair", size=9.5, weight="700"),
          text(cx - 140, 236, "green circles: antenna chlorophylls (with accessory pigments)", size=9.5, anchor="start", fill=SOFT)]
    return ("Inside one photosystem", svg(600, 246,
            "Schematic of one photosystem: many antenna chlorophylls (green circles) surround a central reaction-center pair "
            "of chlorophylls. Light arrives from above. Dashed lines connect the reaction-center pair to an electron "
            "acceptor and to an electron donor drawn beside the complex.", p, defs=[arrow_marker(A, color=ACCENT)]))


def m8_z_scheme():
    K = "m8_z_scheme"
    A = f"{K}_a"
    y_of = lambda e: 230 - e * 190  # e from 0 (low) to 1 (high)
    pts = [("H2O", 50, 0.17), ("PSII", 110, 0.08), ("PSII*", 160, 0.70), ("PQ", 215, 0.55), ("b6f", 270, 0.42),
           ("PC", 325, 0.32), ("PSI", 380, 0.26), ("PSI*", 430, 0.86), ("Fd", 490, 0.65), ("NADP+", 560, 0.58)]
    p = [line(20, 236, 20, 22, stroke=SOFT, width=1.2, end=A),
         f'<text x="12" y="140" text-anchor="middle" font-size="10" fill="{SOFT}" transform="rotate(-90 12 140)">electron energy</text>']
    for (a, xa, ea), (b, xb, eb) in zip(pts, pts[1:]):
        p.append(line(xa, y_of(ea), xb, y_of(eb), stroke=MOD2, width=2, dash="5 3" if a in ("PSII", "PSI") else None))
    for lab, x, e in pts:
        p.append(label_box(x, y_of(e) + 4, lab, size=10.5, weight="700", pad=6))
    for x, e0 in ((110, 0.08), (380, 0.26)):
        p.append(path(f"M{x-22},{n(y_of(e0)-64)} q6,8 0,16 q-6,8 0,16 q6,8 0,16", stroke=ACCENT, width=1.8, end=f"{K}_b"))
        p.append(text(x - 22, y_of(e0) - 70, "light", size=10, fill=ACCENT, weight="700"))
    p.append(text(330, 250, "PQ = plastoquinone · PC = plastocyanin · Fd = ferredoxin · * = excited by light", size=9.5, fill=SOFT))
    return ("Electron energy in the light reactions", svg(620, 260,
            "Energy diagram of the light reactions, shaped like a Z. Electrons from water drop slightly to photosystem II, "
            "which light raises to an excited state (PSII*); they step down through plastoquinone, the cytochrome b6f "
            "complex and plastocyanin to photosystem I, which light raises to PSI*, the highest level; then they step down "
            "through ferredoxin to NADP+.", p,
            defs=[arrow_marker(A, color=SOFT), arrow_marker(f"{K}_b", color=ACCENT)]))


def m8_thylakoid_membrane():
    K = "m8_thylakoid_membrane"
    A = f"{K}_a"
    p = [text(20, 30, "stroma", size=11, anchor="start", weight="700", fill=SOFT),
         text(20, 252, "thylakoid lumen", size=11, anchor="start", weight="700", fill=SOFT),
         rect(10, 112, 610, 50, fill=MOD2, fill_opacity=0.15),
         line(10, 112, 620, 112, stroke=MOD2, width=1.4), line(10, 162, 620, 162, stroke=MOD2, width=1.4)]
    p.append(rect(40, 92, 78, 92, rx=12, fill=GOOD, fill_opacity=0.35, stroke=GOOD, width=1.6))
    p.append(text(79, 142, "PSII", size=12, weight="700"))
    p.append(circle(146, 137, 13, fill=SURFACE, stroke=INK, width=1.4)); p.append(text(146, 141, "PQ", size=9, weight="700"))
    p.append(rect(176, 92, 74, 92, rx=12, fill=MOD1, fill_opacity=0.3, stroke=MOD1, width=1.6))
    p.append(text(213, 142, "b6f", size=12, weight="700"))
    p.append(circle(278, 182, 14, fill=SURFACE, stroke=INK, width=1.4)); p.append(text(278, 186, "PC", size=9, weight="700"))
    p.append(rect(306, 92, 78, 92, rx=12, fill=GOOD, fill_opacity=0.35, stroke=GOOD, width=1.6))
    p.append(text(345, 142, "PSI", size=12, weight="700"))
    p.append(circle(372, 78, 13, fill=SURFACE, stroke=INK, width=1.4)); p.append(text(372, 82, "Fd", size=9, weight="700"))
    p.append(rect(398, 50, 86, 46, rx=10, fill=ACCENT, fill_opacity=0.25, stroke=ACCENT, width=1.4))
    p.append(lines(441, 69, ["NADP+", "reductase"], size=9.5, weight="700"))
    p.append(rect(516, 108, 70, 58, rx=8, fill=VISUAL, fill_opacity=0.3, stroke=VISUAL, width=1.6))
    p.append(text(551, 141, "CFo", size=10.5, weight="700"))
    p.append(rect(545, 90, 12, 18, fill=VISUAL, fill_opacity=0.5))
    p.append(ellipse(551, 70, 38, 22, fill=VISUAL, fill_opacity=0.3, stroke=VISUAL, width=1.6))
    p.append(text(551, 74, "CF1", size=10.5, weight="700"))
    p += [text(551, 200, "ATP synthase", size=10.5, weight="700"),
          text(79, 212, "H2O → O2", size=10, fill=ACCENT, weight="700"),
          text(441, 34, "NADP+ → NADPH", size=10, fill=ACCENT, weight="700"),
          text(551, 34, "ADP + Pi → ATP", size=10, fill=ACCENT, weight="700"),
          text(260, 236, "thylakoid membrane", size=10, fill=SOFT)]
    for x in (64, 330):
        p.append(path(f"M{x},14 q6,8 0,16 q-6,8 0,16 q6,8 0,16", stroke=ACCENT, width=1.8, end=A))
    p.append(text(96, 30, "light", size=10, fill=ACCENT, anchor="start"))
    p.append(text(300, 30, "light", size=10, fill=ACCENT, anchor="end"))
    return ("The thylakoid membrane", svg(630, 262,
            "The thylakoid membrane with the stroma above and the thylakoid lumen below. From left: photosystem II (light "
            "arrives; water is converted to O2 on the lumen side), plastoquinone in the membrane, the cytochrome b6f complex, "
            "plastocyanin on the lumen side, photosystem I (light arrives), ferredoxin and NADP+ reductase on the stroma side "
            "(NADP+ to NADPH), and ATP synthase with CFo in the membrane and CF1 in the stroma (ADP + Pi to ATP).", p,
            defs=[arrow_marker(A, color=ACCENT)]))


def m8_herbicide_site():
    K = "m8_herbicide_site"
    p = [text(20, 30, "stroma", size=11, anchor="start", weight="700", fill=SOFT),
         text(20, 236, "thylakoid lumen", size=11, anchor="start", weight="700", fill=SOFT),
         rect(10, 100, 600, 60, fill=MOD2, fill_opacity=0.15),
         line(10, 100, 610, 100, stroke=MOD2, width=1.4), line(10, 160, 610, 160, stroke=MOD2, width=1.4),
         rect(60, 70, 230, 120, rx=16, fill=GOOD, fill_opacity=0.25, stroke=GOOD, width=1.8),
         text(118, 136, "photosystem II", size=11.5, weight="700"),
         rect(214, 90, 60, 40, rx=8, fill=SURFACE, stroke=INK, width=1.4, dash="4 3"),
         text(244, 84, "QB pocket", size=10, weight="700"),
         polygon([(232, 104), (256, 104), (262, 116), (244, 124), (226, 116)], fill=REVIEW, fill_opacity=0.7,
                 stroke=REVIEW, width=1.4)]
    for x in (340, 380, 420, 460):
        p.append(ellipse(x, 130, 15, 9, fill=SURFACE, stroke=INK, width=1.3))
    p += [text(400, 92, "plastoquinone (PQ) pool", size=10.5, weight="700"),
          text(540, 134, "→ to b6f", size=10, fill=SOFT),
          line(244, 160, 244, 196, stroke=SOFT, width=1),
          text(250, 210, "herbicide (atrazine or diuron) bound in the QB pocket", size=10, anchor="start", fill=REVIEW, weight="700")]
    return ("Where PSII herbicides bind", svg(620, 246,
            "Photosystem II in the thylakoid membrane, with its QB pocket, where a plastoquinone molecule normally docks, "
            "drawn on the right of the complex. A herbicide molecule (atrazine or diuron) sits in the QB pocket. Free "
            "plastoquinone molecules form a pool in the membrane to the right, leading on toward the b6f complex.", p))


def m8_calvin_cycle():
    K = "m8_calvin_cycle"
    A = f"{K}_a"
    B = f"{K}_b"
    p = [node(60, 40, 170, 40, "RuBP (5C)", color=MOD2),
         node(410, 40, 200, 40, "2 × 3-phosphoglycerate (3C)", color=MOD2, size=10.5),
         node(410, 210, 200, 40, "1,3-bisphosphoglycerate", color=MOD2, size=10.5),
         node(60, 210, 170, 40, "triose phosphate (3C)", color=MOD2, size=10.5),
         arrow(230, 60, 406, 60, A), label_box(318, 56, "1 carboxylation (rubisco)", size=10, weight="700"),
         line(318, 98, 318, 66, stroke=ACCENT, width=1.4, end=B), text(318, 112, "CO2 (1C) in", size=10.5, weight="700", fill=ACCENT),
         arrow(510, 80, 510, 206, A), label_box(510, 132, "2 reduction", size=10, weight="700"),
         label_box(510, 152, "ATP → ADP", size=10, weight="700"),
         arrow(406, 230, 234, 230, A), label_box(320, 234, "NADPH → NADP+", size=10, weight="700", pad=12),
         arrow(145, 206, 145, 84, A), label_box(145, 132, "3 regeneration", size=10, weight="700"),
         label_box(145, 152, "ATP → ADP", size=10, weight="700"),
         line(145, 250, 145, 280, stroke=ACCENT, width=1.6, end=B),
         text(156, 284, "carbohydrate out", size=10.5, anchor="start", weight="700", fill=ACCENT)]
    return ("The Calvin cycle", svg(640, 296,
            "The Calvin cycle in three numbered steps. Step 1, carboxylation by rubisco: CO2 (1 carbon) joins RuBP (5 "
            "carbons) to give two 3-phosphoglycerate (3 carbons each). Step 2, reduction: ATP converts 3-phosphoglycerate to "
            "1,3-bisphosphoglycerate, and NADPH reduces that to triose phosphate (3 carbons). Some triose phosphate leaves as "
            "carbohydrate; step 3, regeneration, uses ATP to turn the rest back into RuBP.", p,
            defs=[arrow_marker(A), arrow_marker(B, color=ACCENT)]))


def m8_co2_curves():
    K = "m8_co2_curves"
    x0, y0, w, h = 70, 220, 420, 180
    X = lambda c: x0 + c / 1200 * w
    Y = lambda v: y0 - v / 100 * h
    hi = lambda c: max(0.0, 100 * (1 - math.exp(-(c - 50) / 350)))
    lo = lambda c: max(0.0, 40.5 * (1 - math.exp(-(c - 50) / 220)))
    p = [axes(x0, y0, w, h, [(X(c) - x0, c) for c in (0, 300, 600, 900, 1200)], [(v / 100 * h, v) for v in (0, 25, 50, 75, 100)],
              "CO2 in the air (ppm)", "photosynthesis rate (% of maximum)", ylab_dx=40)]
    for c, lab in ((420, "outdoor air"), (1000, "enriched greenhouse")):
        p.append(line(X(c), y0, X(c), y0 - h - 4, stroke=FAINT, width=1, dash="3 3"))
        p.append(label_box(X(c), y0 - h - 10, f"{lab} ({c})", size=9.5))
    for fn, col, dash in ((hi, MOD2, None), (lo, ACCENT, "7 4")):
        pts = [(X(c), Y(fn(c))) for c in range(0, 1201, 20)]
        p.append(path("M" + " L".join(f"{n(a)},{n(b)}" for a, b in pts), stroke=col, width=2.4, dash=dash))
    p.append(text(x0 + w + 8, Y(hi(1200)) + 4, "bright light", size=10.5, anchor="start", fill=MOD2, weight="700"))
    p.append(text(x0 + w + 8, Y(lo(1200)) + 4, "dim light", size=10.5, anchor="start", fill=ACCENT, weight="700"))
    p.append(text(x0 + w / 2, y0 + 50, "Illustrative values for a C3 crop", size=9.5, fill=SOFT))
    return ("Photosynthesis rate vs CO2 level", svg(590, 282,
            "Line graph of a crop's photosynthesis rate (as % of maximum) against CO2 in the air from 0 to 1200 ppm, at two "
            "light levels (illustrative). In bright light the rate is about 65% at outdoor air (420 ppm) and about 93% at "
            "an enriched greenhouse level (1000 ppm). In dim light the rate rises only gently, from about 33% at 420 ppm to "
            "about 40% at 1000 ppm. Illustrative values for a C3 crop.", p))


def m8_c14_timecourse():
    K = "m8_c14_timecourse"
    x0, y0, w, h = 70, 210, 400, 170
    pga = [(2, 88), (5, 80), (10, 66), (20, 50), (30, 40), (45, 31), (60, 26)]
    sug = [(2, 6), (5, 12), (10, 24), (20, 38), (30, 47), (45, 54), (60, 58)]
    X = lambda t: x0 + t / 60 * w
    Y = lambda v: y0 - v / 100 * h
    p = [axes(x0, y0, w, h, [(X(t) - x0, t) for t in (0, 10, 20, 30, 40, 50, 60)], [(v / 100 * h, v) for v in (0, 25, 50, 75, 100)],
              "seconds after 14CO2 was added", "% of the 14C in the cells", ylab_dx=40)]
    for data, col, dash in ((pga, MOD2, None), (sug, ACCENT, "7 4")):
        p.append(polyline([(X(t), Y(v)) for t, v in data], stroke=col, width=2.4, dash=dash))
        for t, v in data:
            p.append(circle(X(t), Y(v), 3.2, fill=col))
    p.append(text(X(60) + 8, Y(26) + 4, "3-phosphoglycerate", size=10.5, anchor="start", fill=MOD2, weight="700"))
    p.append(text(X(60) + 8, Y(58) + 4, "sugar phosphates", size=10.5, anchor="start", fill=ACCENT, weight="700"))
    p.append(text(270, 262, "Illustrative values; the rest of the label is in other compounds", size=9.5, fill=SOFT))
    return ("Where the 14C label goes", svg(600, 272,
            "Line graph of the share of radioactive carbon-14 found in two kinds of compound in algae at times after 14CO2 "
            "was added (illustrative). 3-phosphoglycerate holds about 88% at 2 seconds, falling to about 26% at 60 seconds. "
            "Sugar phosphates hold about 6% at 2 seconds, rising to about 58% at 60 seconds.", p))


ALL = {"m8_chloroplast": m8_chloroplast, "m8_sunlight_budget": m8_sunlight_budget, "m8_o18_table": m8_o18_table,
       "m8_absorption_spectra": m8_absorption_spectra, "m8_led_bands": m8_led_bands, "m8_chlorophyll": m8_chlorophyll,
       "m8_photosystem": m8_photosystem, "m8_z_scheme": m8_z_scheme, "m8_thylakoid_membrane": m8_thylakoid_membrane,
       "m8_herbicide_site": m8_herbicide_site, "m8_calvin_cycle": m8_calvin_cycle, "m8_co2_curves": m8_co2_curves,
       "m8_c14_timecourse": m8_c14_timecourse}
