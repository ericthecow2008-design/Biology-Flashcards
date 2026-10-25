"""Module 7 diagrams (cellular respiration), including the five case-study diagrams."""
import math
from svgkit import *
from dkit import node, arrow, axes, table


def m7_cell_compartments():
    K = "m7_cell_compartments"
    p = [rect(10, 10, 620, 250, rx=28, fill=MOD2, fill_opacity=0.05, stroke=MOD2, width=2.4)]
    cx, cy = 330, 140
    p.append(ellipse(cx, cy, 170, 82, fill=ACCENT, fill_opacity=0.10, stroke=ACCENT, width=2.2))
    p.append(ellipse(cx, cy, 148, 62, fill=ACCENT, fill_opacity=0.14, stroke=ACCENT, width=2))
    for x in (230, 300, 370):
        p.append(path(f"M{x},{cy-61} L{x},{cy-28} Q{x+9},{cy-20} {x+18},{cy-28} L{x+18},{cy-60}", stroke=ACCENT, width=2))
    for x in (265, 335, 405):
        p.append(path(f"M{x},{cy+61} L{x},{cy+28} Q{x+9},{cy+20} {x+18},{cy+28} L{x+18},{cy+60}", stroke=ACCENT, width=2))
    p.append(text(cx - 5, cy + 4, "matrix", size=11, weight="700"))
    p.append(text(80, 60, "cytosol", size=12, weight="700"))
    # leader-lined labels
    p.append(line(470, 92, 516, 72, stroke=SOFT, width=1))
    p.append(text(520, 76, "outer membrane", size=10.5, anchor="start"))
    p.append(line(478, 140, 516, 140, stroke=SOFT, width=1))
    p.append(text(520, 144, "inner membrane", size=10.5, anchor="start"))
    p.append(line(489, 172, 516, 196, stroke=SOFT, width=1))
    p.append(lines(520, 200, ["intermembrane", "space"], size=10.5, anchor="start"))
    p.append(line(60, 230, 30, 246, stroke=SOFT, width=1))
    p.append(text(64, 232, "plasma membrane", size=10.5, anchor="start"))
    return ("A cell's cytosol and one mitochondrion", svg(640, 270,
            "A cell bounded by its plasma membrane, with the cytosol labelled and one mitochondrion drawn inside. "
            "The mitochondrion's outer membrane, its folded inner membrane, the intermembrane space between them and "
            "the matrix inside the inner membrane are labelled.", p))


def m7_glycolysis_map():
    K = "m7_glycolysis_map"
    A = f"{K}_a"
    mols = ["glucose (6C)", "glucose 6-phosphate", "fructose 6-phosphate", "fructose 1,6-bisphosphate (6C)",
            "G3P + DHAP (3C each)", "G3P (×2)", "1,3-bisphosphoglycerate (×2)", "3-phosphoglycerate (×2)",
            "2-phosphoglycerate (×2)", "phosphoenolpyruvate (×2)", "pyruvate (3C, ×2)"]
    left = {1: "1  hexokinase", 2: "2", 3: "3  phosphofructokinase", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
            9: "9  enolase", 10: "10"}
    right = {1: "ATP → ADP", 3: "ATP → ADP", 6: "2 NAD+ → 2 NADH", 7: "2 ADP → 2 ATP", 10: "2 ADP → 2 ATP"}
    cx, y0, dy = 230, 26, 36
    p = []
    for i, m in enumerate(mols):
        y = y0 + i * dy
        p.append(text(cx, y, m, size=11, weight="700" if i in (0, 10) else None))
        if i < 10:
            p.append(arrow(cx, y + 6, cx, y + dy - 14, A))
            mid = y + dy / 2 + 2
            p.append(text(cx - 16, mid, left[i + 1], size=10, anchor="end", fill=SOFT))
            if (i + 1) in right:
                p.append(text(cx + 16, mid, right[i + 1], size=10, anchor="start", fill=ACCENT, weight="700"))
    p.append(text(cx, y0 + 10 * dy + 26, "G3P = glyceraldehyde 3-phosphate · DHAP = dihydroxyacetone phosphate",
                  size=9.5, fill=SOFT))
    p.append(text(cx, y0 + 10 * dy + 41, "From step 5 on, every count is for one glucose (two 3-carbon molecules).",
                  size=9.5, fill=SOFT))
    return ("Glycolysis, step by step", svg(470, y0 + 10 * dy + 52,
            "Glycolysis drawn as ten numbered steps from glucose (6 carbons) to 2 pyruvate (3 carbons each). Step 1, "
            "hexokinase, and step 3, phosphofructokinase, each convert ATP to ADP. Step 4 splits fructose "
            "1,6-bisphosphate into G3P and DHAP; step 5 gives 2 G3P. Step 6 converts 2 NAD+ to 2 NADH; steps 7 and 10 "
            "each convert 2 ADP to 2 ATP; step 9 is enolase.", p, defs=[arrow_marker(A)]))


def m7_fdg_cell():
    K = "m7_fdg_cell"
    A = f"{K}_a"
    p = [rect(220, 34, 22, 186, fill=ACCENT, fill_opacity=0.25, stroke=ACCENT, width=1.4),
         text(110, 24, "blood", size=11, weight="700", fill=SOFT), text(430, 24, "cell (cytosol)", size=11, weight="700", fill=SOFT)]
    for y in (82, 182):
        p.append(rect(208, y - 16, 46, 32, rx=8, fill=SURFACE))
        p.append(rect(208, y - 16, 46, 32, rx=8, fill=VISUAL, fill_opacity=0.3, stroke=VISUAL, width=1.4))
        p.append(text(231, y + 4, "GLUT", size=9, weight="700"))
    p += [node(40, 62, 130, 40, "glucose", color=MOD1),
          node(40, 162, 130, 40, "FDG", color=REVIEW),
          arrow(170, 82, 204, 82, A), arrow(170, 182, 204, 182, A),
          node(300, 62, 170, 40, "glucose 6-phosphate", color=MOD1, size=10.5),
          node(300, 162, 170, 40, "FDG 6-phosphate", color=REVIEW, size=10.5),
          arrow(254, 82, 296, 82, A), arrow(254, 182, 296, 182, A),
          text(282, 128, "hexokinase", size=9.5, fill=SOFT), text(282, 141, "+ ATP", size=9.5, fill=SOFT),
          arrow(470, 82, 520, 82, A), lines(578, 78, ["rest of", "glycolysis"], size=10, fill=INK),
          text(30, 240, "FDG: glucose with 18F (radioactive fluorine) in place of the -OH on carbon 2", size=9.5,
               anchor="start", fill=SOFT)]
    return ("Glucose and FDG at a cell", svg(640, 252,
            "Glucose and FDG in the blood each enter a cell through a GLUT carrier in the plasma membrane. Inside, "
            "hexokinase with ATP converts glucose to glucose 6-phosphate, which continues into the rest of glycolysis, "
            "and FDG to FDG 6-phosphate, which has no further arrow. A note says FDG is glucose with radioactive "
            "fluorine-18 in place of the -OH on carbon 2.", p, defs=[arrow_marker(A)]))


def m7_pyruvate_fates():
    K = "m7_pyruvate_fates"
    A = f"{K}_a"
    p = [text(120, 22, "cytosol", size=11, weight="700", fill=SOFT),
         rect(300, 34, 330, 214, rx=40, fill=ACCENT, fill_opacity=0.06, stroke=ACCENT, width=2),
         rect(314, 48, 302, 186, rx=32, fill=ACCENT, fill_opacity=0.08, stroke=ACCENT, width=1.6),
         text(465, 70, "mitochondrial matrix", size=11, weight="700", fill=SOFT),
         node(40, 40, 130, 34, "glucose", color=MOD1),
         arrow(105, 74, 105, 104, A), text(115, 93, "glycolysis", size=10, anchor="start", fill=SOFT),
         node(40, 108, 130, 34, "pyruvate (3C)", color=MOD1),
         arrow(105, 142, 105, 180, A), text(115, 166, "NADH → NAD+", size=10, anchor="start", fill=ACCENT, weight="700"),
         node(40, 184, 130, 34, "lactate (3C)", color=REVIEW),
         arrow(170, 125, 344, 125, A),
         node(348, 96, 236, 58, ["pyruvate dehydrogenase", "complex (its cofactor TPP", "is made from thiamine)"],
              color=MOD2, size=10),
         arrow(466, 154, 466, 172, A),
         node(380, 174, 172, 32, "acetyl-CoA (2C) + CO2", color=MOD1, size=10.5),
         text(466, 224, "→ citric acid cycle", size=10, fill=SOFT),
         text(258, 117, "NAD+ → NADH", size=9.5, fill=ACCENT, weight="700")]
    return ("Where pyruvate can go", svg(640, 258,
            "In the cytosol, glycolysis turns glucose into pyruvate (3 carbons). One arrow takes pyruvate to lactate "
            "(3 carbons) while NADH becomes NAD+. Another takes pyruvate into the mitochondrial matrix to the pyruvate "
            "dehydrogenase complex, whose cofactor TPP is made from thiamine, giving acetyl-CoA (2 carbons) and CO2 "
            "while NAD+ becomes NADH; acetyl-CoA goes on to the citric acid cycle.", p, defs=[arrow_marker(A)]))


def m7_cac_cycle():
    K = "m7_cac_cycle"
    A = f"{K}_a"
    cx, cy, r = 300, 178, 100
    names = ["citrate (6C)", "isocitrate (6C)", "α-ketoglutarate (5C)", "succinyl-CoA (4C)", "succinate (4C)",
             "fumarate (4C)", "malate (4C)", "oxaloacetate (4C)"]
    angs = [22.5 + 45 * k for k in range(8)]
    pt = lambda a, rr=r: (cx + rr * math.sin(math.radians(a)), cy - rr * math.cos(math.radians(a)))
    p = []
    for k in range(8):
        a1, a2 = angs[k] + 9, angs[(k + 1) % 8] - 9
        if k == 7:
            a2 = 360 + angs[0] - 9
        x1, y1 = pt(a1)
        x2, y2 = pt(a2)
        p.append(path(f"M{n(x1)},{n(y1)} A{r},{r} 0 0 1 {n(x2)},{n(y2)}", stroke=MOD1, width=2, end=A))
    for k, nm in enumerate(names):
        x, y = pt(angs[k])
        p.append(circle(x, y, 5, fill=MOD1))
        s = math.sin(math.radians(angs[k]))
        lx, ly = pt(angs[k], r + 14)
        anchor = "start" if s > 0.2 else ("end" if s < -0.2 else "middle")
        p.append(text(lx, ly + 4, nm, size=10.5, anchor=anchor, weight="700"))
    p.append(text(cx, cy - 4, "citric acid", size=11, fill=SOFT))
    p.append(text(cx, cy + 10, "cycle", size=11, fill=SOFT))
    p.append(text(cx, 24, "acetyl-CoA (2C)", size=11, weight="700"))
    p.append(arrow(cx, 30, cx, cy - r - 4, A))
    return ("The citric acid cycle's carbon skeletons", svg(600, 310,
            "The citric acid cycle drawn as a clockwise circle of eight intermediates with their carbon counts: citrate "
            "6C, isocitrate 6C, alpha-ketoglutarate 5C, succinyl-CoA 4C, succinate 4C, fumarate 4C, malate 4C and "
            "oxaloacetate 4C. Acetyl-CoA (2C) enters from above at the point between oxaloacetate and citrate.",
            p, defs=[arrow_marker(A, color=MOD1)]))


def m7_etc_membrane():
    K = "m7_etc_membrane"
    p = [text(20, 30, "intermembrane space", size=11, anchor="start", weight="700", fill=SOFT),
         text(20, 250, "matrix", size=11, anchor="start", weight="700", fill=SOFT),
         rect(10, 110, 600, 50, fill=ACCENT, fill_opacity=0.18),
         line(10, 110, 610, 110, stroke=ACCENT, width=1.4), line(10, 160, 610, 160, stroke=ACCENT, width=1.4)]
    p.append(rect(40, 88, 70, 98, rx=12, fill=MOD1, fill_opacity=0.35, stroke=MOD1, width=1.6))
    p.append(text(75, 140, "I", size=14, weight="700"))
    p.append(rect(128, 134, 50, 52, rx=10, fill=MOD2, fill_opacity=0.35, stroke=MOD2, width=1.6))
    p.append(text(153, 179, "II", size=13, weight="700"))
    p.append(circle(206, 135, 13, fill=SURFACE, stroke=INK, width=1.4))
    p.append(text(206, 139, "Q", size=11, weight="700"))
    p.append(rect(234, 88, 70, 98, rx=12, fill=MOD1, fill_opacity=0.35, stroke=MOD1, width=1.6))
    p.append(text(269, 140, "III", size=14, weight="700"))
    p.append(circle(334, 96, 15, fill=SURFACE, stroke=INK, width=1.4))
    p.append(text(334, 74, "cyt c", size=10.5, weight="700"))
    p.append(rect(364, 88, 70, 98, rx=12, fill=MOD1, fill_opacity=0.35, stroke=MOD1, width=1.6))
    p.append(text(399, 140, "IV", size=14, weight="700"))
    # ATP synthase: Fo in membrane, stalk, F1 in matrix
    p.append(rect(484, 104, 74, 62, rx=8, fill=VISUAL, fill_opacity=0.3, stroke=VISUAL, width=1.6))
    p.append(text(521, 140, "Fo", size=11, weight="700"))
    p.append(rect(514, 166, 14, 16, fill=VISUAL, fill_opacity=0.5))
    p.append(ellipse(521, 204, 40, 22, fill=VISUAL, fill_opacity=0.3, stroke=VISUAL, width=1.6))
    p.append(text(521, 208, "F1", size=11, weight="700"))
    p.append(text(521, 82, "ATP synthase", size=10.5, weight="700"))
    p += [text(75, 206, "NADH → NAD+", size=10, fill=ACCENT, weight="700"),
          text(153, 206, "FADH2 → FAD", size=10, fill=ACCENT, weight="700"),
          text(399, 206, "O2 → H2O", size=10, fill=ACCENT, weight="700"),
          text(521, 246, "ADP + Pi → ATP", size=10, fill=ACCENT, weight="700"),
          text(240, 60, "inner mitochondrial membrane", size=10, fill=SOFT)]
    return ("The inner mitochondrial membrane", svg(620, 262,
            "The inner mitochondrial membrane with the intermembrane space above and the matrix below. From left to "
            "right: complex I (NADH to NAD+ on the matrix side), complex II (FADH2 to FAD), coenzyme Q in the membrane, "
            "complex III, cytochrome c on the intermembrane-space side, complex IV (O2 to H2O on the matrix side), and "
            "ATP synthase with its Fo part in the membrane and its F1 part in the matrix (ADP + Pi to ATP).", p))


def m7_o2_trace():
    K = "m7_o2_trace"
    x0, y0, w, h = 70, 230, 450, 180
    pts = [(0, 100), (2, 96), (4, 80), (6, 77), (8, 55), (10, 55)]
    X = lambda t: x0 + t / 10 * w
    Y = lambda v: y0 - (v - 40) / 60 * h
    p = [axes(x0, y0, w, h, [(i * w / 5, i * 2) for i in range(6)], [((v - 40) / 60 * h, v) for v in (40, 60, 80, 100)],
              "time (minutes)", "O2 left in the chamber (% of start)", ylab_dx=40)]
    adds = [(2, "+ ADP"), (4, "+ oligomycin"), (6, "+ DNP"), (8, "+ cyanide")]
    for t, lab in adds:
        p.append(line(X(t), y0 - h - 2, X(t), y0, stroke=FAINT, width=1, dash="3 3"))
        p.append(label_box(X(t), y0 - h - 8, lab, size=10, weight="700"))
    p.append(polyline([(X(t), Y(v)) for t, v in pts], stroke=MOD1, width=2.6))
    return ("O2 use by isolated mitochondria", svg(560, 272,
            "Line graph of the oxygen left in a sealed chamber of isolated mitochondria supplied with fuel, over 10 "
            "minutes. It falls slowly from 100% to 96% by minute 2; after ADP is added it falls faster to 80% by minute 4; "
            "after oligomycin is added it falls slowly to 77% by minute 6; after DNP is added it falls steeply to 55% "
            "by minute 8; after cyanide is added it stays flat at 55%.", p))


def m7_dnp_bars():
    K = "m7_dnp_bars"
    x0, y0, h = 70, 210, 160
    data = [("O2 used", 100, 180), ("ATP made", 100, 35), ("heat released", 100, 230)]
    vmax = 250
    p = [axes(x0, y0, 420, h, [], [(v / vmax * h, v) for v in (0, 50, 100, 150, 200, 250)], None,
              "% of untreated value", ylab_dx=40)]
    for i, (lab, a, b) in enumerate(data):
        gx = x0 + 40 + i * 135
        for j, (v, col) in enumerate(((a, MOD1), (b, REVIEW))):
            bh = v / vmax * h
            p.append(rect(gx + j * 42, y0 - bh, 34, bh, rx=2, fill=col, fill_opacity=0.85))
            p.append(label_box(gx + j * 42 + 17, y0 - bh - 6, str(v), size=10, weight="700"))
        p.append(text(gx + 38, y0 + 18, lab, size=10.5, weight="700"))
    p += [rect(330, 18, 12, 12, fill=MOD1, fill_opacity=0.85), text(348, 28, "untreated", size=10, anchor="start"),
          rect(420, 18, 12, 12, fill=REVIEW, fill_opacity=0.85), text(438, 28, "with DNP", size=10, anchor="start"),
          text(270, 248, "Illustrative values for mitochondria given the same fuel", size=9.5, fill=SOFT)]
    return ("Mitochondria with and without DNP", svg(520, 258,
            "Grouped bar chart, as a percentage of the untreated value, for mitochondria given the same fuel with and "
            "without DNP: O2 used 100 versus 180, ATP made 100 versus 35, heat released 100 versus 230. Illustrative values.", p))


def m7_yield_table():
    K = "m7_yield_table"
    rows = [["stage (per glucose)", "ATP", "NADH", "FADH2", "CO2"],
            ["glycolysis", "2 (net)", "2", "0", "0"],
            ["pyruvate oxidation", "0", "2", "0", "2"],
            ["citric acid cycle", "2", "6", "2", "4"]]
    p = [table(20, 16, [190, 80, 80, 80, 80], rows, row_h=28, size=11),
         text(275, 146, "ATP column: ATP made directly by substrate-level phosphorylation", size=9.5, fill=SOFT)]
    return ("Products of the first three stages", svg(550, 156,
            "Table of products per glucose for the first three stages of respiration. Glycolysis: 2 ATP (net), 2 NADH, "
            "0 FADH2, 0 CO2. Pyruvate oxidation: 0 ATP, 2 NADH, 0 FADH2, 2 CO2. Citric acid cycle: 2 ATP, 6 NADH, 2 FADH2, "
            "4 CO2. The ATP column counts ATP made directly by substrate-level phosphorylation.", p))


def m7_dough_sprint():
    K = "m7_dough_sprint"
    p = []
    for i, (title, sub, rows, col) in enumerate([
            ("yeast in bread dough", "covered, little O2, 2 hours", ["fuel: sugars from flour", "gas bubbles: CO2",
                                                                  "ethanol: detected", "lactate: none"], MOD2),
            ("sprinter's thigh muscle", "30-second all-out effort", ["fuel: glucose from glycogen", "gas bubbles: none",
                                                                     "ethanol: none", "lactate: rises sharply"], REVIEW)]):
        x = 20 + i * 305
        p.append(rect(x, 14, 285, 186, rx=12, fill=col, fill_opacity=0.08, stroke=col, width=1.6))
        p.append(text(x + 142, 40, title, size=12, weight="700"))
        p.append(text(x + 142, 58, sub, size=10, fill=SOFT))
        for j, r in enumerate(rows):
            p.append(text(x + 24, 94 + j * 26, r, size=11, anchor="start"))
    return ("Two cells short of O2", svg(630, 212,
            "Two panels of measurements. Yeast in covered bread dough with little O2 for 2 hours: fuel is sugars from "
            "flour; CO2 gas bubbles; ethanol detected; no lactate. A sprinter's thigh muscle during a 30-second all-out "
            "effort: fuel is glucose from glycogen; no gas bubbles; no ethanol; lactate rises sharply.", p))


def m7_fuel_map():
    K = "m7_fuel_map"
    A = f"{K}_a"
    cx = 320
    col = [("glycolysis", 40), ("pyruvate", 104), ("acetyl-CoA", 168), ("citric acid cycle", 232), ("electron transport chain", 296)]
    p = []
    for i, (nm, y) in enumerate(col):
        p.append(node(cx - 85, y, 170, 34, nm, color=MOD1, size=11))
        if i < 4:
            p.append(arrow(cx, y + 34, cx, col[i + 1][1] - 4, A))
    p += [node(20, 40, 150, 34, "glucose, other sugars", color=MOD2, size=10.5), arrow(170, 57, cx - 89, 57, A),
          node(480, 30, 140, 34, "glycerol", color=ACCENT, size=10.5), arrow(480, 47, cx + 89, 52, A),
          node(480, 160, 140, 34, "fatty acids", color=ACCENT, size=10.5), arrow(480, 182, cx + 89, 185, A),
          text(446, 176, "β-oxidation", size=9.5, fill=SOFT),
          node(480, 95, 140, 34, ["fats", "(triacylglycerols)"], color=ACCENT, size=10),
          line(550, 95, 550, 68, stroke=ACCENT, width=1.4, end=A), line(550, 129, 550, 156, stroke=ACCENT, width=1.4, end=A),
          node(20, 168, 150, 34, "amino acids", color=REVIEW, size=10.5),
          node(20, 104, 150, 34, "proteins", color=REVIEW, size=10.5), line(95, 138, 95, 164, stroke=REVIEW, width=1.4, end=A),
          arrow(170, 178, cx - 89, 125, A), arrow(170, 185, cx - 89, 185, A), arrow(170, 194, cx - 89, 245, A)]
    return ("How different fuels enter respiration", svg(640, 340,
            "Pathway map. A central column runs glycolysis, pyruvate, acetyl-CoA, citric acid cycle, electron transport "
            "chain. Glucose and other sugars enter at glycolysis. Fats (triacylglycerols) split into glycerol, which enters "
            "at glycolysis, and fatty acids, which enter at acetyl-CoA by an arrow labelled beta-oxidation. Proteins give "
            "amino acids, with arrows into pyruvate, acetyl-CoA and the citric acid cycle.", p, defs=[arrow_marker(A)]))


def m7_energy_staircase():
    K = "m7_energy_staircase"
    p = []
    for i, (title, steps) in enumerate([("A: burning in a flame", 1), ("B: inside a cell", 14)]):
        x0, y0, w, h = 60 + i * 300, 230, 220, 180
        p.append(axes(x0, y0, w, h, [], [], None, "free energy" if i == 0 else None, grid=False, ylab_dx=24))
        p.append(text(x0 + w / 2, 22, title, size=11.5, weight="700"))
        top, bot = y0 - h + 30, y0 - 30
        p.append(text(x0 + 6, top - 8, "glucose + 6 O2", size=10, anchor="start"))
        p.append(text(x0 + w - 4, bot + 18, "6 CO2 + 6 H2O", size=10, anchor="end"))
        if steps == 1:
            p.append(polyline([(x0 + 10, top), (x0 + 70, top), (x0 + 70, bot), (x0 + w - 10, bot)], stroke=REVIEW, width=2.4))
        else:
            pts = [(x0 + 10, top)]
            xx, yy = x0 + 10, top
            sw = (w - 20) / (steps + 1)
            dy = (bot - top) / steps
            for s in range(steps):
                xx += sw
                pts.append((xx, yy))
                yy += dy
                pts.append((xx, yy))
            pts.append((x0 + w - 10, bot))
            p.append(polyline(pts, stroke=MOD1, width=2.2))
    p.append(text(310, 262, "Same starting molecules and the same end products in A and B (not to scale)", size=9.5, fill=SOFT))
    return ("Oxidizing glucose: one drop or many steps", svg(620, 272,
            "Two free-energy diagrams side by side, each starting at glucose + 6 O2 and ending at 6 CO2 + 6 H2O. "
            "A, burning in a flame: one large drop. B, inside a cell: a staircase of many small drops between the same "
            "start and end levels.", p))


ALL = {"m7_cell_compartments": m7_cell_compartments, "m7_glycolysis_map": m7_glycolysis_map, "m7_fdg_cell": m7_fdg_cell,
       "m7_pyruvate_fates": m7_pyruvate_fates, "m7_cac_cycle": m7_cac_cycle, "m7_etc_membrane": m7_etc_membrane,
       "m7_o2_trace": m7_o2_trace, "m7_dnp_bars": m7_dnp_bars, "m7_yield_table": m7_yield_table,
       "m7_dough_sprint": m7_dough_sprint, "m7_fuel_map": m7_fuel_map, "m7_energy_staircase": m7_energy_staircase}
