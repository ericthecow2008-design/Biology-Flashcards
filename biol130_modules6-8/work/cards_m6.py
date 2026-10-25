"""Module 6: five case studies plus four cards for concepts the 46 existing cards miss."""
from cardkit import S, combo, case, tf, mc, match, box, with_mod, STEM_TAIL

CARDS = with_mod(6, [
    # ---------------------------------------------------------------- Energy & Metabolism
    case("Energy & Metabolism", "A warning label on diet soda",
         "Phenylketonuria (PKU) is an inherited disease in which the enzyme phenylalanine hydroxylase doesn't work; "
         "newborns are screened for it with a heel-prick blood test." + STEM_TAIL,
         box("Untreated, phenylalanine builds up in the blood to levels that harm the developing brain.",
             "Drinks sweetened with aspartame carry the warning \"Phenylketonurics: contains phenylalanine\"."),
         [S("Untreated children with PKU often have lighter skin and hair than their relatives, since less tyrosine is made "
            "for the route to melanin.", True,
            "Linked pathways mean a failed step cuts the supply to everything after it: less tyrosine is made from "
            "phenylalanine for the melanin route, and the excess phenylalanine also blocks tyrosinase, the first enzyme on "
            "that route, so less pigment is made."),
          S("Since tyrosine lies beyond the broken step, a PKU diet should cut tyrosine as well as phenylalanine, so that "
            "it doesn't build up as in (가).", False,
            "Tyrosine is the product of the broken step, so it can no longer be made from phenylalanine; it must come "
            "from the diet, and PKU medical formulas are in fact supplemented with tyrosine."),
          S("The warning in (나) matters because the phenylalanine released when aspartame is digested enters the same "
            "pathway as phenylalanine from dietary protein.", True,
            "Aspartame is built from aspartate and phenylalanine; digesting it frees phenylalanine, which adds to the "
            "load the blocked pathway can't clear."),
          ],
         "Metabolic pathways are linked: a product of one step is the next step's reactant · Real-world: phenylketonuria (PKU)",
         ["m6_metabolic_pathways_linked"], points=3, diagram="m6_pku_pathway"),
    tf("Energy & Metabolism",
       "The body's slow route releases less total energy from those fats and carbohydrates than burning them does, "
       "because much of the energy is captured as ATP instead of being given off as heat.", False,
       "Energy is neither created nor destroyed: the same starting molecules ending as the same products release the same "
       "total energy by either route. The body captures part of it as ATP for a while, but the total is unchanged.",
       "First law of thermodynamics · Catabolism releases energy",
       ["m6_first_law"], points=2,
       box="A food lab burns a peanut completely in a calorimeter and measures the heat released. In the body, the same "
           "peanut's fats and digestible carbohydrates (starch and sugars) are oxidized to the same end products, CO2 and H2O, over many enzyme-catalyzed steps."),

    # ---------------------------------------------------------------- ATP & Energetic Coupling
    case("ATP & Energetic Coupling", "The phosphate bank in a sprinter's muscle",
         "Creatine is one of the most popular sports supplements: it raises the amount of phosphocreatine stored in "
         "muscle and modestly improves performance in repeated short sprints." + STEM_TAIL,
         box("In the first seconds of intense exercise, phosphocreatine passes its phosphate directly to ADP, making ATP and creatine.",
             "Each value in the diagram is for removing one phosphate from that molecule."),
         [S("Under standard conditions the transfer in (가) has a ΔG of about −3.0 kcal/mol, so it can run forward without any other energy source.", True,
            "Coupling phosphocreatine hydrolysis (−10.3) with ATP synthesis from ADP + Pi (+7.3) gives −10.3 + 7.3 = −3.0 kcal/mol."),
          S("Creatine supplements help because muscle cells oxidize the extra creatine itself for energy, the way they "
            "oxidize glucose.", False,
            "Creatine is a phosphate carrier, not a fuel: at rest it is recharged to phosphocreatine, and during effort "
            "phosphocreatine hands the phosphate to ADP. Extra creatine means a bigger phosphocreatine store for remaking ATP quickly."),
          S("Recharging creatine at rest (creatine + ATP → phosphocreatine + ADP) can't happen in muscle, since this "
            "reaction's standard ΔG is positive.", False,
            "Its standard ΔG is indeed +10.3 − 7.3 = +3.0 kcal/mol, but resting muscle keeps the ATP/ADP ratio very high "
            "and has plenty of creatine after exercise, which pushes the reaction away from equilibrium toward phosphocreatine."),
          ],
         "Energetic coupling through a shared phosphate · ATP hydrolysis is exergonic · Real-world: creatine supplements",
         ["m6_energetic_coupling", "m6_atp_hydrolysis_exergonic", "m6_driving_positive_dg"], points=3, diagram="m6_phosphate_ladder"),

    # ---------------------------------------------------------------- Thermodynamics & Free Energy
    case("Thermodynamics & Free Energy", "Click, and the pack gets hot",
         "A reusable hand warmer holds a sodium acetate solution that stays liquid at room temperature even though it holds "
         "more dissolved salt than would normally stay dissolved." + STEM_TAIL,
         box("Clicking a small metal disc inside the pack starts crystals forming, and the pack warms to about 50-55 °C as it turns solid.",
             "To reuse the pack, it is boiled in water until the crystals dissolve, then left to cool without crystallizing."),
         [S("Clicking the disc supplies the energy that makes the crystallization's ΔG negative.", False,
            "ΔG is set by the gap between the two plateaus, which the click doesn't change. The click only gets the first "
            "crystals past the activation-energy barrier; after that, crystallization carries on by itself."),
          S("Crystallizing makes the sodium acetate more ordered, so it is spontaneous only because the heat it releases "
            "(negative ΔH) outweighs the drop in entropy.", True,
            "In ΔG = ΔH − TΔS, a negative ΔS makes −TΔS positive; ΔG is still negative because ΔH is more negative."),
          S("Overall, resetting the pack in (나) takes an energy input: going from crystals back to the room-temperature "
            "solution has a positive ΔG, and the stove's heat supplies that energy.", True,
            "At room temperature, crystals → solution is the reverse of an exergonic change, so ΔG is positive. Boiling works "
            "because at high T the −TΔS term makes dissolving spontaneous; careful cooling then leaves the solution on the higher plateau."),
          ],
         "ΔG = ΔH − TΔS · Activation energy · Exergonic vs endergonic · Real-world: reusable hand warmers",
         ["m6_gibbs_equation", "m6_activation_energy", "m6_delta_g_sign"], points=3, diagram="m6_handwarmer_profile"),
    mc("Thermodynamics & Free Energy",
       "Refrigerating food slows its spoilage, which depends on enzyme-catalyzed reactions in microbes and in the food "
       "itself. Which explanation fits best?",
       "The cold leaves fewer molecules with enough kinetic energy to cross the activation barrier",
       ["The cold makes the spoilage reactions endergonic, so they can no longer proceed",
        "The cold unfolds the enzymes, so their active sites can no longer bind substrates",
        "The cold raises the activation energy that each spoilage reaction needs",
        "The cold lowers the free energy each reaction releases until it reaches zero"],
       "Reactants must have enough kinetic energy to reach the transition state; cooling slows molecules, so fewer succeed "
       "per second. ΔG shifts only slightly and stays negative, the barrier's height is unchanged, and fridge temperatures don't denature enzymes.",
       "Activation energy · Kinetic energy · Real-world: refrigeration",
       ["m6_activation_energy", "m6_potential_kinetic"], points=2),

    # ---------------------------------------------------------------- Enzymes & Their Regulation
    case("Enzymes & Their Regulation", "A cholesterol drug and a look-alike",
         "Statins, the most widely prescribed cholesterol-lowering drugs, inhibit HMG-CoA reductase, the enzyme for an "
         "early step in the liver's cholesterol-making pathway." + STEM_TAIL,
         box("Part of each statin molecule is shaped much like HMG-CoA, the enzyme's substrate.",
             "Compound N, an experimental inhibitor, binds the enzyme at a site away from its active site."),
         [S("Because the statin curve lies below compound N's at low HMG-CoA, the statin is the stronger inhibitor at every "
            "HMG-CoA concentration shown.", False,
            "The curves cross near 3-4 units; above that, compound N holds the rate lower, because substrate increasingly "
            "outcompetes the statin but can't displace compound N."),
          S("The statin cuts the rate by about a fifth at 20 units of HMG-CoA but by nearly half at 5 units, because more "
            "substrate outcompetes the drug for the active site.", True,
            "At 20 units the rates are about 95% vs 77%; at 5 units about 83% vs 45%. As (가) suggests, the statin and the "
            "substrate compete for the same site."),
          S("Compound N's curve levels off near 45% because it takes the same share of enzyme molecules out of action "
            "at every HMG-CoA concentration.", True,
            "Compound N binds a separate site (나), so substrate can't compete it off; the share of enzyme it disables is the "
            "same at any HMG-CoA level, which caps the rate."),
          ],
         "Competitive vs noncompetitive inhibition · Real-world: statins",
         ["m6_competitive_inhibition", "m6_noncompetitive_inhibition"], points=3, diagram="m6_statin_curves"),
    case("Enzymes & Their Regulation", "Pineapple that ruins dessert",
         "Boxes of gelatin dessert mix warn that fresh pineapple or kiwi will keep the gelatin from setting, while canned "
         "pineapple is fine." + STEM_TAIL,
         box("Fresh pineapple contains bromelain, an enzyme that hydrolyzes peptide bonds. Gelatin is a protein made from collagen.",
             "Canning heats the fruit to near boiling."),
         [S("Tubes 3 and 4 set because heating made the hydrolysis of gelatin's peptide bonds endergonic, so even a working "
            "enzyme could no longer drive it forward.", False,
            "Boiling the fruit beforehand doesn't change the ΔG of gelatin hydrolysis in the chilled tube; it is still "
            "exergonic. Heating unfolded bromelain, destroying its active site, and without a working enzyme the reaction is too slow to matter."),
          S("In tube 1 almost no peptide bonds are hydrolyzed even though hydrolysis releases energy, because without an "
            "enzyme few of these bonds get over the activation-energy barrier.", True,
            "A negative ΔG says a reaction can proceed, not how fast; with a high barrier and no catalyst, the gel stays intact."),
          S("Comparing tubes 2 and 4 shows that fresh pineapple stops the gel from setting through a heat-sensitive "
            "component such as a protein, not through something heat-stable like its sugar or acid.", True,
            "The same fruit stops working once boiled; sugars and acids survive boiling, but a protein's fold, and so "
            "an enzyme's active site, does not."),
          ],
         "Enzymes lower activation energy · Heat destroys the active site · ΔG vs rate · Real-world: gelatin and fresh pineapple",
         ["m6_enzymes_lower_ea", "m6_active_site", "m6_delta_g_sign"], points=3, diagram="m6_gelatin_tubes"),
    tf("Enzymes & Their Regulation",
       "So dorzagliatin must bind glucokinase's active site in place of glucose, since it changes how fast glucose is "
       "phosphorylated.", False,
       "If the drug sat in the active site, glucose couldn't bind at the same time. It binds a separate pocket and changes the enzyme's shape so the active site works better, the opposite of a "
       "noncompetitive inhibitor. A molecule needn't occupy the active site to change the rate; only a competitive "
       "inhibitor works by competing with the substrate there.",
       "Enzyme activators · Competitive inhibition",
       ["m6_enzyme_activators", "m6_competitive_inhibition"], points=2,
       box="Dorzagliatin, a diabetes drug approved in China in 2022, makes glucokinase (the liver and pancreas form of "
           "hexokinase) phosphorylate glucose faster. Glucose and the drug can both be bound to one enzyme molecule at the same time."),
    mc("Enzymes & Their Regulation",
       "An enzyme early in an ATP-producing pathway is controlled by small molecules that bind away from its active site. "
       "Which pair of controls would best match the cell's energy needs?",
       "ATP inhibits the enzyme, and AMP activates it",
       ["ATP activates the enzyme, and AMP inhibits it",
        "ATP and AMP both activate the enzyme",
        "AMP inhibits the enzyme, and ADP activates it",
        "ATP and AMP both inhibit the enzyme"],
       "Plenty of ATP means the pathway's product is in surplus, so inhibition saves fuel (feedback); a build-up of AMP "
       "signals that ATP has been spent, so activation speeds ATP production.",
       "Enzyme activators · Feedback inhibition",
       ["m6_enzyme_activators", "m6_feedback_inhibition"], points=2),
])
