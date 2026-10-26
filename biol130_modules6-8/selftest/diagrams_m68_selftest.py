"""SELFTEST ONLY: three small diagrams that exercise the checks. Never ship these."""
from svgkit import *


def selftest_energy_profile():
    K = "selftest_energy_profile"
    parts = [line(40, 20, 40, 150), line(40, 150, 300, 150),
             path("M50,110 C110,110 120,40 170,40 C220,40 230,125 290,125", stroke=MOD1, width=2),
             path("M50,110 C110,110 125,80 170,80 C215,80 230,125 290,125", stroke=ACCENT, width=2, dash="5 4"),
             text(46, 16, "free energy", size=10, anchor="start", fill=SOFT),
             text(170, 168, "reaction progress", size=10, fill=SOFT),
             text(170, 32, "path 1", size=10, fill=MOD1), text(170, 96, "path 2", size=10, fill=ACCENT)]
    return "Selftest: two reaction paths", svg(330, 180, "Selftest diagram: free energy against reaction progress for two paths with different peak heights.", parts)


def selftest_atp_tally():
    K = "selftest_atp_tally"
    ARR = f"{K}_arr"
    parts = [rect(20, 30, 120, 40, rx=6, fill=MOD2, fill_opacity=0.15, stroke=MOD2, width=1.4),
             text(80, 55, "glucose", weight="700"), line(140, 50, 220, 50, end=ARR),
             label_box(180, 54, "10 steps", size=10),
             rect(222, 30, 120, 40, rx=6, fill=MOD1, fill_opacity=0.15, stroke=MOD1, width=1.4),
             text(282, 55, "2 pyruvate", weight="700")]
    return "Selftest: glucose to pyruvate", svg(360, 90, "Selftest diagram: a glucose box with an arrow labelled 10 steps leading to a box labelled 2 pyruvate.", parts, defs=[arrow_marker(ARR)])


def selftest_cycle():
    K = "selftest_cycle"
    parts = [circle(120, 80, 50, stroke=GOOD, width=2), text(120, 84, "cycle", weight="700"),
             pill(120, 20, "CO2 in", color=REVIEW), text(120, 150, "sugar out", fill=SOFT)]
    return "Selftest: a cycle", svg(240, 160, "Selftest diagram: a circle labelled cycle, with CO2 entering at the top and sugar leaving at the bottom.", parts)


ALL = {"selftest_energy_profile": selftest_energy_profile, "selftest_atp_tally": selftest_atp_tally, "selftest_cycle": selftest_cycle}
