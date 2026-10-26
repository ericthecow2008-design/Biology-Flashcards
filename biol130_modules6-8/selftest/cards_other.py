"""SELFTEST ONLY: throwaway Module 6, Module 8 and bridge cards. Never ship these."""
from cardkit import S, case, tf, box, with_mod, STEM_TAIL

CARDS = (with_mod(6, [case("Enzymes & Their Regulation", "SELFTEST enzyme case card",
    "Selftest stem for Module 6." + STEM_TAIL, box("Selftest fact A.", "Selftest fact B."),
    [S("Selftest statement one.", True, "Selftest explanation one."),
     S("Selftest statement two.", False, "Selftest explanation two."),
     S("Selftest statement three.", True, "Selftest explanation three.")],
    "Selftest link", ["selftest_activation_energy"], points=3, diagram="selftest_energy_profile")])
 + with_mod(8, [case("Calvin Cycle", "SELFTEST Calvin case card",
    "Selftest stem for Module 8." + STEM_TAIL, box("Selftest fact A.", "Selftest fact B."),
    [S("Selftest statement one.", True, "Selftest explanation one."),
     S("Selftest statement two.", True, "Selftest explanation two."),
     S("Selftest statement three.", True, "Selftest explanation three.")],
    "Selftest link", ["selftest_calvin_carboxylation"], points=3, diagram="selftest_cycle")])
 + with_mod(0, [tf("Connecting Modules 1–8", "Selftest bridge claim.", False, "Selftest explanation.",
    "Selftest link", ["selftest_glycolysis_net_atp", "selftest_m2_hydrolysis"], points=2, box="Selftest bridge scenario.")]))
