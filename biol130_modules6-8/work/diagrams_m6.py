"""Module 6 case-study diagrams."""
from svgkit import *
from dkit import node, arrow, axes, table


def m6_handwarmer_profile():
    K = "m6_handwarmer_profile"
    x0, y0 = 70, 200
    p = [axes(x0, y0, 340, 170, [], [], "progress of crystallization (at room temperature)", "free energy", ylab_dx=22, xlab_dy=20, grid=False)]
    p.append(path(f"M{x0+10},88 L{x0+95},88 C{x0+135},88 {x0+140},42 {x0+165},42 "
                  f"C{x0+195},42 {x0+200},160 {x0+240},160 L{x0+330},160", stroke=ACCENT, width=2.4))
    p.append(lines(x0 + 52, 66, ["supersaturated", "solution"], size=10.5, fill=INK))
    p.append(lines(x0 + 285, 138, ["sodium acetate", "crystals"], size=10.5, fill=INK))
    p.append(text(x0 + 52, 108, "liquid, clear", size=9.5, fill=SOFT))
    p.append(text(x0 + 285, 180, "solid", size=9.5, fill=SOFT))
    return ("Free energy of a hand-warmer pack", svg(430, 232,
            "Free-energy profile of a reusable hand warmer: a supersaturated sodium acetate solution sits on a "
            "higher plateau, a hump rises between it and a lower plateau labelled sodium acetate crystals.", p))


def m6_phosphate_ladder():
    K = "m6_phosphate_ladder"
    x0, y0 = 170, 40
    scale = 22  # px per kcal/mol
    rows = [("phosphocreatine", 10.3, MOD1), ("ATP (to ADP)", 7.3, ACCENT), ("glucose 6-phosphate", 3.3, MOD2)]
    p = []
    for i, (lab, v, col) in enumerate(rows):
        y = y0 + i * 46
        p.append(text(x0 - 10, y + 18, lab, size=11, anchor="end", weight="700"))
        p.append(rect(x0, y + 4, v * scale, 22, rx=3, fill=col, fill_opacity=0.85))
        p.append(text(x0 + v * scale + 8, y + 19.5, f"−{v} kcal/mol", size=10.5, anchor="start"))
    p.append(line(x0, y0 - 4, x0, y0 + 140, stroke=SOFT, width=1.2))
    p.append(text(260, y0 + 162, "ΔG when one phosphate is hydrolyzed off (standard conditions)", size=10, fill=SOFT))
    return ("Energy released by removing a phosphate", svg(520, 210,
            "Horizontal bar chart of the free-energy change when one phosphate is hydrolyzed off three molecules: "
            "phosphocreatine −10.3, ATP to ADP −7.3, glucose 6-phosphate −3.3 kcal/mol.", p))


def m6_pku_pathway():
    K = "m6_pku_pathway"
    ARR = f"{K}_a"
    p = [node(20, 82, 130, 44, ["phenylalanine", "(from food protein)"], color=MOD1, size=10.5),
         node(270, 82, 110, 44, "tyrosine", color=MOD1),
         node(450, 20, 170, 44, ["melanin", "(skin and hair pigment)"], color=MOD2, size=10.5),
         node(450, 144, 170, 44, ["dopamine, adrenaline", "(nerve signals)"], color=MOD2, size=10.5),
         node(20, 196, 130, 44, ["phenylpyruvate", "(a phenylketone)"], color=REVIEW, size=10.5),
         arrow(150, 104, 266, 104, ARR), label_box(208, 92, "phenylalanine", size=9.5),
         label_box(208, 122, "hydroxylase", size=9.5),
         arrow(380, 96, 446, 50, ARR), arrow(380, 112, 446, 158, ARR),
         arrow(85, 126, 85, 192, ARR, dash="5 4"),
         text(95, 164, "minor side route", size=9.5, anchor="start", fill=SOFT)]
    return ("Where phenylalanine goes", svg(640, 250,
            "Pathway diagram: phenylalanine from food protein is converted by phenylalanine hydroxylase to tyrosine, "
            "which leads on to melanin and to dopamine and adrenaline. A dashed minor side route leads from "
            "phenylalanine to phenylpyruvate, a phenylketone.", p, defs=[arrow_marker(ARR)]))


def m6_statin_curves():
    K = "m6_statin_curves"
    x0, y0, w, h = 70, 210, 330, 170
    xmax = 20.0
    def pt(s, v):
        return x0 + s / xmax * w, y0 - v / 100 * h
    def curve(vmax, km):
        pts = [pt(s, vmax * s / (km + s)) for s in [i * 0.25 for i in range(0, 81)]]
        return "M" + " L".join(f"{n(a)},{n(b)}" for a, b in pts)
    p = [axes(x0, y0, w, h, [(i * w / 4, int(i * 5)) for i in range(5)],
              [(i * h / 4, int(i * 25)) for i in range(5)], "HMG-CoA concentration (arbitrary units)",
              "reaction rate (% of no-drug maximum)", ylab_dx=40)]
    p.append(path(curve(100, 1.0), stroke=MOD1, width=2.2))
    p.append(path(curve(100, 6.0), stroke=ACCENT, width=2.2, dash="7 4"))
    p.append(path(curve(45, 1.0), stroke=REVIEW, width=2.2, dash="2 3"))
    p.append(text(x0 + w + 8, pt(20, 100 * 20 / 21)[1] + 4, "no drug", size=10.5, anchor="start", fill=MOD1, weight="700"))
    p.append(text(x0 + w + 8, pt(20, 100 * 20 / 26)[1] + 4, "statin", size=10.5, anchor="start", fill=ACCENT, weight="700"))
    p.append(text(x0 + w + 8, pt(20, 45 * 20 / 21)[1] + 4, "compound N", size=10.5, anchor="start", fill=REVIEW, weight="700"))
    return ("HMG-CoA reductase rate, three conditions", svg(490, 250,
            "Line graph of HMG-CoA reductase reaction rate against HMG-CoA concentration (0 to 20 units). "
            "No drug: rises steeply and levels off near 100%. Statin: rises more slowly but reaches about 77% by 20 units "
            "and is still climbing. Compound N: levels off early at about 45%.", p))


def m6_gelatin_tubes():
    K = "m6_gelatin_tubes"
    p = []
    labels = [["1", "gelatin only"], ["2", "+ fresh", "pineapple"], ["3", "+ canned", "pineapple"],
              ["4", "+ fresh pineapple,", "boiled 5 min, cooled"]]
    results = ["set", "stays liquid", "set", "set"]
    for i in range(4):
        cx = 80 + i * 150
        p.append(text(cx, 22, labels[i][0], size=12, weight="700"))
        p.append(lines(cx, 40, labels[i][1:], size=10, fill=INK))
        # tube
        p.append(path(f"M{cx-24},78 L{cx-24},178 Q{cx-24},200 {cx},200 Q{cx+24},200 {cx+24},178 L{cx+24},78",
                      stroke=SOFT, width=1.6))
        if results[i] == "set":
            p.append(path(f"M{cx-22},118 L{cx-22},178 Q{cx-22},198 {cx},198 Q{cx+22},198 {cx+22},178 L{cx+22},118 Z",
                          fill=MOD2, fill_opacity=0.55, stroke="none"))
        else:
            p.append(path(f"M{cx-22},150 Q{cx-11},145 {cx},150 Q{cx+11},155 {cx+22},150 L{cx+22},178 Q{cx+22},198 {cx},198 "
                          f"Q{cx-22},198 {cx-22},178 Z", fill=VISUAL, fill_opacity=0.35, stroke="none"))
        if i in (1, 2, 3):
            for dx, dy in ((-8, 170), (7, 182), (-2, 160)):
                p.append(rect(cx + dx - 4, dy - 4 if results[i] == "set" else dy, 8, 8, rx=1.5, fill=ACCENT, fill_opacity=0.8))
        p.append(text(cx, 224, results[i], size=11, weight="700", fill=INK))
    p.append(text(310, 248, "Tubes chilled for 4 hours (the gelatin mix was made the same way in every tube)", size=9.5, fill=SOFT))
    return ("Four gelatin tubes after chilling", svg(620, 258,
            "Four test tubes of gelatin mix after 4 hours in the fridge. Tube 1, gelatin only: set. Tube 2, with fresh "
            "pineapple: stays liquid. Tube 3, with canned pineapple: set. Tube 4, with fresh pineapple that was boiled "
            "5 minutes and cooled: set.", p))


ALL = {"m6_handwarmer_profile": m6_handwarmer_profile, "m6_phosphate_ladder": m6_phosphate_ladder,
       "m6_pku_pathway": m6_pku_pathway, "m6_statin_curves": m6_statin_curves, "m6_gelatin_tubes": m6_gelatin_tubes}
