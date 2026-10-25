"""Bridge diagrams (Connecting Modules 1-8)."""
from svgkit import *
from dkit import node, arrow, axes, table


def br_nad_structure():
    K = "br_nad_structure"
    p = []
    # left half: adenine - ribose - phosphate; right half: phosphate - ribose - nicotinamide
    p += [node(20, 40, 120, 44, "adenine", color=MOD1, size=11),
          polygon([(190, 44), (226, 60), (214, 92), (166, 92), (154, 60)], fill=ACCENT, fill_opacity=0.25, stroke=ACCENT, width=1.5),
          text(190, 74, "ribose", size=10.5, weight="700"),
          circle(270, 130, 20, fill=REVIEW, fill_opacity=0.25, stroke=REVIEW, width=1.5), text(270, 134, "P", size=12, weight="700"),
          circle(350, 130, 20, fill=REVIEW, fill_opacity=0.25, stroke=REVIEW, width=1.5), text(350, 134, "P", size=12, weight="700"),
          polygon([(430, 44), (466, 60), (454, 92), (406, 92), (394, 60)], fill=ACCENT, fill_opacity=0.25, stroke=ACCENT, width=1.5),
          text(430, 74, "ribose", size=10.5, weight="700"),
          node(480, 40, 140, 44, "nicotinamide", color=GOOD, size=11),
          line(140, 62, 156, 62, stroke=INK, width=1.6), line(470, 62, 480, 62, stroke=INK, width=1.6),
          line(208, 92, 254, 118, stroke=INK, width=1.6), line(290, 130, 330, 130, stroke=INK, width=1.6),
          line(366, 118, 412, 92, stroke=INK, width=1.6),
          text(320, 186, "NAD+ is the oxidized form of the carrier; NADH is the reduced form.", size=9.5, fill=SOFT)]
    return ("The parts of NAD+", svg(640, 200,
            "Schematic of NAD+: adenine joined to a ribose, which is joined to a phosphate; that phosphate is joined to a "
            "second phosphate, which is joined to a second ribose carrying nicotinamide. A note says NAD+ is the oxidized "
            "form of the carrier and NADH the reduced form.", p))


def br_food_chain():
    K = "br_food_chain"
    A = f"{K}_a"
    rows = [("sunlight on the grass", "1,000,000 kJ", ACCENT), ("stored in grass", "10,000 kJ", GOOD),
            ("stored in rabbits", "1,000 kJ", MOD1), ("stored in foxes", "100 kJ", REVIEW)]
    p = []
    for i, (lab, val, col) in enumerate(rows):
        x = 20 + i * 155
        p.append(node(x, 40, 135, 56, [lab, val], color=col, size=10.5))
        if i < 3:
            p.append(arrow(x + 135, 68, x + 151, 68, A))
    p.append(text(320, 130, "Energy per square metre of meadow per year (illustrative values)", size=9.5, fill=SOFT))
    return ("Energy along a food chain", svg(640, 142,
            "Four boxes in a row joined by arrows: sunlight on the grass 1,000,000 kJ; stored in grass 10,000 kJ; "
            "stored in rabbits 1,000 kJ; stored in foxes 100 kJ. Values are per square metre of meadow per year and are illustrative.",
            p, defs=[arrow_marker(A)]))


def br_ph_map():
    K = "br_ph_map"
    p = [text(155, 22, "mitochondrion (respiring)", size=11, weight="700"),
         rect(20, 34, 270, 150, rx=60, fill=ACCENT, fill_opacity=0.08, stroke=ACCENT, width=2),
         rect(44, 58, 222, 102, rx=44, fill=ACCENT, fill_opacity=0.14, stroke=ACCENT, width=1.6),
         text(155, 104, "matrix", size=11, weight="700"), text(155, 122, "pH about 7.8", size=11),
         text(155, 176, "intermembrane space: pH about 7.0", size=10, fill=INK),
         text(485, 22, "chloroplast (in bright light)", size=11, weight="700"),
         rect(340, 34, 290, 150, rx=60, fill=MOD2, fill_opacity=0.08, stroke=MOD2, width=2),
         rect(352, 46, 266, 126, rx=52, fill=MOD2, fill_opacity=0.06, stroke=MOD2, width=1.4),
         text(485, 76, "stroma: pH about 8", size=11, weight="700"),
         rect(420, 104, 130, 34, rx=14, fill=GOOD, fill_opacity=0.3, stroke=GOOD, width=1.4),
         text(485, 126, "lumen: pH about 5", size=10.5, weight="700")]
    return ("pH inside two organelles", svg(640, 196,
            "Two organelles with approximate pH values. A respiring mitochondrion: matrix about pH 7.8, intermembrane space "
            "about pH 7.0. A chloroplast in bright light: stroma about pH 8, thylakoid lumen about pH 5.", p))


ALL = {"br_nad_structure": br_nad_structure, "br_food_chain": br_food_chain, "br_ph_map": br_ph_map}
