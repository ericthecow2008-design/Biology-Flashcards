"""Module 8: Photosynthesis (full set)."""
from cardkit import S, combo, case, tf, mc, match, box, with_mod, STEM_TAIL

READ = "Read (가) and (나). Which statements in <보기> are correct?"
DIAG = "Using the diagram, which statements in <보기> are correct?"
OV, PG, PS, CC = ("Overview of Photosynthesis", "Pigments & Light Absorption", "Photosystems & Electron Transport",
                  "Calvin Cycle")

CARDS = with_mod(8, [
    # ================================================================ Overview of Photosynthesis
    case(OV, "Where does the oxygen come from?",
         "In 1941, Samuel Ruben, Martin Kamen and colleagues used the heavy oxygen isotope 18O to find out where the O2 "
         "released by photosynthesis comes from." + STEM_TAIL,
         box("In each experiment, only one of the two raw materials, water or CO2, was enriched in 18O.",
             "Photosynthesis overall: 6 CO2 + 12 H2O → C6H12O6 + 6 O2 + 6 H2O."),
         [S("In experiment 2, the CO2's extra 18O would reach the sugar only after the light was switched off, since sugar "
            "is made in the light-independent reactions.", False,
            "The Calvin cycle runs in the light, using ATP and NADPH as the thylakoids make them; 'light-independent' means "
            "it doesn't use light directly."),
          S("The O2 released matches the label in the water because water is the electron donor that is oxidized in the light reactions.", True,
            "Oxidizing water releases electrons, protons and O2, so the O2 carries water's oxygen atoms (experiment 1)."),
          S("In experiment 2, the extra 18O from the CO2 would end up in the sugar and in the water on the right side of (나).", True,
            "CO2's oxygen atoms go into the carbohydrate and the product water; that is why the equation lists water on both sides."),
          ],
         "Water is the electron donor · Overall equation · Real-world: Ruben and Kamen's 18O experiments",
         ["m8_water_electron_donor", "m8_overall_equation", "m8_two_stages_linked"], points=3, diagram="m8_o18_table"),
    combo(OV, "When the lights go out", READ,
          box("A spinach leaf in bright light is suddenly put in the dark.",
              "CO2 fixation goes on for a few seconds in the dark, then stops."),
          [S("Fixation continues briefly in (나) because RuBP, and the ATP and NADPH made in the light, have not yet run out "
             "in the stroma.", True,
             "Rubisco keeps adding CO2 to the RuBP already present, and leftover ATP and NADPH remake a little more; once they "
             "are used up, RuBP can't be regenerated and fixation stops."),
           S("Extra CO2 supplied when the light went off would keep fixation in (나) going much longer.", False,
             "Fixation stops because RuBP can't be regenerated once ATP and NADPH run out; extra CO2 doesn't replace them."),
           S("During the few seconds of fixation in (나), the thylakoids keep releasing O2 at the rate they did in the light.", False,
             "Splitting water at PSII needs light, so O2 release stops at once; only the Calvin cycle coasts on what the "
             "light reactions already made."),
           ],
          "The two stages are linked · Calvin cycle needs ATP and NADPH · Regeneration of RuBP",
          ["m8_two_stages_linked", "m8_calvin_overview", "m8_regeneration_rubp"], points=2),
    combo(OV, "The same atoms, two directions", READ,
          box("Photosynthesis: 6 CO2 + 12 H2O + light → C6H12O6 + 6 O2 + 6 H2O.",
              "Cellular respiration: C6H12O6 + 6 O2 → 6 CO2 + 6 H2O."),
          [S("In (가), carbon is reduced as CO2 becomes carbohydrate, and the oxygen of water is oxidized to O2.", True,
             "CO2 gains electrons (reduction) to become sugar; water loses electrons (oxidation), releasing O2."),
           S("Turning CO2 and water into carbohydrate and O2 has a positive ΔG, which is why light energy is needed, while "
             "(나) has a negative ΔG.", True,
             "Building high-energy carbohydrate from CO2 is endergonic; light supplies the energy that respiration later releases."),
           S("The energy that (나) releases from glucose was originally captured from light by a process like (가).", True,
             "Photosynthesis stores light energy in carbohydrate; respiration later releases it, as ATP and heat, by "
             "running the reverse overall reaction through different pathways and enzymes."),
           ],
          "Photosynthesis is a redox process · Endergonic vs exergonic · Energy entry point",
          ["m8_photosynthesis_redox", "m6_delta_g_sign", "m8_photosynthesis_definition"], points=3),
    combo(OV, "Life in the sunlit layer", READ,
          box("In clear ocean water, only about 1% of the surface light remains at a depth of about 100-200 m.",
              "Phytoplankton, microscopic photosynthesizers of the ocean's sunlit layer, carry out about half of Earth's photosynthesis."),
          [S("Most animals living far below the sunlit layer still depend on photosynthesis, eating food that sinks from above.", True,
             "Food webs are supported by the biomass of photosynthesizers; deep animals live on organic matter that sinks down."),
           S("Phytoplankton carried below about 200 m would photosynthesize far more slowly, even with plenty of CO2 in the seawater.", True,
             "Photosynthesis needs light as its energy source; with about 1% of surface light or less, light, not CO2, limits it."),
           S("The chemical energy that the phytoplankton in (나) store in sugar comes from the CO2 they take up from seawater.", False,
             "The energy comes from light; CO2 is a low-energy carbon source that gets reduced to carbohydrate."),
           ],
          "Photosynthesis needs light · Energy entry point for food webs · CO2 is reduced",
          ["m8_light_limits_habitat", "m8_photosynthesis_definition", "m8_photosynthesis_redox"], points=2),
    match(OV, "Parts of a chloroplast", "Match each part of the chloroplast to the fact that fits it best.", "Part", "Fact",
          [("Thylakoid membrane", "Where the herbicide diuron binds and blocks electron flow"),
           ("Thylakoid lumen", "Where H+ from split water builds up"),
           ("Stroma", "Where 14C from 14CO2 first turns up, in 3-phosphoglycerate"),
           ("Granum", "Seen in electron micrographs as a pile of coin-like discs"),
           ("Inner and outer membranes", "Two membranes separated by a narrow space, as around a mitochondrion")],
          "Diuron binds photosystem II in the thylakoid membrane; H+ collects in the lumen; CO2 is fixed into "
          "3-phosphoglycerate in the stroma; and the double envelope wraps the organelle. A granum is made of thylakoids, "
          "but only its stacking is unique to it.",
          "Chloroplast structure · Stage locations · Thylakoid H+ gradient",
          ["m8_chloroplast_structure", "m8_stage_locations", "m8_thylakoid_proton_gradient"], points=3),
    tf(OV, "If the dry wood were burned completely, most of its mass would leave as CO2 and water vapour, with only a small "
           "fraction left as mineral ash.", True,
       "Wood is mostly carbohydrate that photosynthesis built from CO2 and water; burning oxidizes it back to CO2 and H2O, "
       "leaving only the minerals taken from the soil.",
       "Photosynthesis builds biomass from CO2", ["m8_photosynthesis_definition"], points=2,
       box="An oak seedling grows into a tree weighing several tonnes, while the soil around it loses only a little mass."),
    tf(OV, "Of the sunlight in the range plants can use, at most about a tenth ends up stored in carbohydrate.", True,
       "40% of the sunlight is in the usable range and at most 4% is stored: 4 / 40 = 10%.",
       "Efficiency of photosynthesis", ["m8_photosynthesis_efficiency"], points=2,
       box="The diagram shows what happens to the sunlight reaching a leaf.", diagram="m8_sunlight_budget"),
    tf(OV, "At least a quarter of the sunlight reaching the leaf ends up as heat.", True,
       "Energy isn't destroyed: the 8% converted into heat plus the 20% 'lost' during carbohydrate synthesis, which also "
       "ends up as heat, already make 28%; much of the infrared outside the usable range is absorbed as heat too.",
       "Efficiency of photosynthesis · First law", ["m8_photosynthesis_efficiency", "m6_first_law"], points=2,
       box="The diagram shows what happens to the sunlight reaching a leaf.", diagram="m8_sunlight_budget"),
    tf(OV, "Isolated thylakoids given light, water and an artificial electron acceptor, but no CO2, can still release O2.", True,
       "Water is split by photosystem II in the thylakoid membranes and the acceptor takes its electrons; CO2 is needed "
       "only later, in the stroma.",
       "Stage locations · Water is the electron donor · Real-world: Hill's experiment",
       ["m8_stage_locations", "m8_water_electron_donor"], points=2,
       box="Thylakoids can be separated from the stroma by breaking chloroplasts open and spinning them in a centrifuge."),
    tf(OV, "It will fix CO2 for as long as the light stays on.", False,
       "The stroma's Calvin cycle needs ATP and NADPH, which only the thylakoids' light reactions make; light alone does nothing for it.",
       "The two stages are linked · Stage locations", ["m8_two_stages_linked", "m8_stage_locations"], points=2,
       box="Stroma separated from thylakoids, with rubisco and all the Calvin cycle enzymes, is given CO2 and placed in bright light."),
    tf(OV, "All 12 hydrogen atoms in the glucose came from water.", True,
       "CO2 carries no hydrogen, so every H in the sugar came from water; water's electrons and H+ reach CO2 by way of NADPH.",
       "Overall equation · Water is the electron donor", ["m8_overall_equation", "m8_water_electron_donor"], points=2,
       box="Photosynthesis overall: 6 CO2 + 12 H2O + light → C6H12O6 + 6 O2 + 6 H2O."),
    tf(OV, "Light supplies the electrons that reduce CO2, so no other molecule has to be oxidized.", False,
       "Light supplies energy, not electrons. Reduction always pairs with an oxidation; here water is oxidized, and its "
       "electrons (carried by NADPH) reduce CO2.",
       "Photosynthesis is a redox process · Water is the electron donor",
       ["m8_photosynthesis_redox", "m8_water_electron_donor"], points=1,
       box="In photosynthesis, CO2 is reduced to carbohydrate."),
    tf(OV, "A blight that killed most of the grass would leave the wolves' food supply unchanged, since wolves eat deer "
           "rather than grass.", False,
       "The deer live on the grass, so the energy entering this food chain comes from the grass's photosynthesis; with "
       "less grass there are fewer deer, and the wolves go short of food.",
       "Photosynthesis is the energy entry point", ["m8_photosynthesis_definition"], points=1,
       box="A wolf eats deer, and the deer eat grass."),
    tf(OV, "The cave's food web depends on organic matter carried in from outside, such as bat droppings and washed-in leaves.", True,
       "With no light, nothing in the cave photosynthesizes, so the energy its animals use must come in as food made by "
       "photosynthesis outside.",
       "Photosynthesis needs light · Energy entry point for food webs · Real-world: cave animals",
       ["m8_light_limits_habitat", "m8_photosynthesis_definition"], points=1,
       box="Many caves are home to insects, fish and salamanders but no plants, since no light reaches them."),
    mc(OV, "Using the diagram, where in the chloroplast are the enzymes that split water and release O2?",
       "Thylakoid membrane", ["Stroma", "Inner membrane, which holds the electron transport chain as in mitochondria",
                              "Outer membrane", "Space between the inner and outer membranes"],
       "Water is split by photosystem II in the thylakoid membrane, the site of the light-dependent reactions; a "
       "chloroplast's inner membrane, unlike a mitochondrion's, holds no electron transport chain.",
       "Stage locations · Chloroplast structure", ["m8_stage_locations", "m8_chloroplast_structure"], points=1,
       diagram="m8_chloroplast"),
    mc(OV, "Which pair of molecules does the Calvin cycle return to the light reactions to be recharged?",
       "ADP and NADP+", ["ATP and NADPH", "ADP and NAD+", "ATP and NADP+", "ADP and NADPH"],
       "The Calvin cycle spends ATP and NADPH and returns ADP (with Pi) and NADP+, which the light reactions turn back into "
       "ATP and NADPH; NAD+ is respiration's carrier.",
       "The two stages are linked", ["m8_two_stages_linked"], points=1),
    mc(OV, "Using the overall equation, how many water molecules must be split to release the O2 that goes with one glucose?",
       "12", ["3", "6", "12", "18", "24"],
       "One glucose comes with 6 O2, which hold 12 oxygen atoms; each split water molecule supplies one of them.",
       "Overall equation · Water is the electron donor", ["m8_overall_equation", "m8_water_electron_donor"], points=2,
       ordered=True, key_index=2),
    mc(OV, "The O2 in a weedy pond rises during a sunny day and falls overnight. Which explanation fits best?",
       "By day photosynthesis outpaces respiration; at night only respiration runs",
       ["Plants respire only at night, when they use up the O2 that they made by day",
        "By day respiration releases O2, and at night photosynthesis uses it up",
        "At night, photosynthesis runs in reverse and takes O2 back up from the water",
        "Cool night water holds less dissolved O2, so the O2 escapes into the air"],
       "Photosynthesis releases O2 only in light, while all organisms, plants included, respire day and night. (Cool water "
       "holds more dissolved O2, not less.)",
       "Photosynthesis needs light · Plants respire day and night", ["m8_photosynthesis_definition"], points=2),
    mc(OV, "Using the diagram, what is the largest single reason a leaf stores so little of the sunlight it receives?",
       "Most of the energy is in wavelengths the pigments can't use",
       ["Leaves reflect or transmit most of the light that reaches them",
        "Most of the sunlight's energy is lost during carbohydrate synthesis",
        "Most of the sunlight is turned into heat as soon as the leaf absorbs it",
        "Chlorophyll absorbs mainly green light, which carries little energy"],
       "60% of the sunlight is outside the usable range, by far the biggest loss; reflection and heat take 8% each, and "
       "synthesis losses 20%.",
       "Efficiency of photosynthesis", ["m8_photosynthesis_efficiency"], points=1, diagram="m8_sunlight_budget"),

    # ================================================================ Pigments & Light Absorption
    case(PG, "Purple light in an indoor farm",
         "Indoor vertical farms often grow lettuce under purple-looking light from panels of red and blue LEDs, which are "
         "among the most energy-efficient grow lights." + STEM_TAIL,
         box("Each LED colour gives off a narrow band of wavelengths, shown in the diagram.",
             "Many farms also add some green or white LEDs, partly so workers can see the plants' true colour."),
         [S("Swapping the red LEDs for green LEDs of the same power would not lower photosynthesis, since every visible "
            "photon carries energy.", False,
            "Only absorbed photons drive photosynthesis. Chlorophyll absorbs 530 nm far more weakly than 660 nm, so a leaf "
            "captures green light less completely, and a watt of green light also carries fewer photons than a watt of red."),
          S("Red and blue LEDs are chosen because their wavelengths fall near the peaks of chlorophyll's absorption.", True,
            "The blue (450 nm) and red (660 nm) bands sit on the two absorption peaks, so most of their photons are absorbed."),
          S("Without the extra light in (나), the lettuce would look dark, having little green light to reflect.", True,
            "Leaves look green because they reflect green light; under red and blue light alone there is almost no green to reflect."),
          ],
         "Chlorophyll absorbs blue and red · Only absorbed light is used · Real-world: LED grow lights",
         ["m8_chlorophyll_absorption"], points=3, diagram="m8_led_bands"),
    combo(PG, "Reading three absorption spectra", DIAG,
          box("Leaves contain chlorophyll a, chlorophyll b and carotenoids.",
              "A dilute suspension of isolated chloroplasts is lit with one wavelength at a time while its O2 release is measured."),
          [S("O2 release in (나) would be close to zero at 662 nm, since red light's photons carry less energy than those "
             "of the other visible colours.", False,
             "Chlorophyll a absorbs strongly at 662 nm, and a red photon carries enough energy to excite it, so red light "
             "drives O2 release well."),
           S("Carotenoids widen the range of light a leaf can use, absorbing blue-green light near 480 nm that chlorophyll a absorbs poorly.", True,
             "At 480 nm the carotenoid curve is high while chlorophyll a's is near zero; accessory pigments fill such gaps."),
           S("Chlorophyll b's red peak lies at a longer wavelength than chlorophyll a's, so it extends absorption further into the red.", False,
             "Chlorophyll b's red peak (about 642 nm) lies at a shorter wavelength than chlorophyll a's (about 662 nm)."),
           ],
          "Chlorophyll absorption · Accessory pigments", ["m8_chlorophyll_absorption", "m8_accessory_pigments"], points=2,
          diagram="m8_absorption_spectra"),
    combo(PG, "Red seaweeds in deep water", READ,
          box("Seawater absorbs red light within the top several metres, but blue and green light reach much deeper.",
              "Red algae that grow deep on reefs carry accessory pigments (phycoerythrins) that absorb green and blue-green "
              "light."),
          [S("In white light, these algae look red because their pigments absorb green and blue-green light and reflect "
             "relatively more red.", True,
             "An object's colour is the light it doesn't absorb; phycoerythrins absorb green and blue-green, so relatively "
             "more red is reflected."),
           S("The pigments in (나) pass on absorbed energy, not electrons, to chlorophyll, as antenna pigments do.", True,
             "Accessory pigments act like antenna pigments, transferring excitation energy toward the reaction center."),
           S("At depth, these algae still get most of their energy from red light absorbed at chlorophyll's red peak.", False,
             "Red light is absorbed by the water near the surface (가), so very little reaches deep algae; they rely on green "
             "and blue-green light."),
           ],
          "Accessory pigments · Antenna energy transfer · Light limits where photosynthesis can occur · Real-world: deep red algae",
          ["m8_accessory_pigments", "m8_antenna_transfer", "m8_light_limits_habitat"], points=3),
    match(PG, "Across the spectrum", "Match each kind of light to the description that fits it.", "Light", "Description",
          [("Ultraviolet (below 400 nm)", "More energy per photon than any visible light"),
           ("Blue (about 440 nm)", "Absorbed strongly by both chlorophylls and carotenoids"),
           ("Green (about 550 nm)", "The visible light chlorophyll absorbs least"),
           ("Red (about 660 nm)", "Absorbed strongly by chlorophyll a but not by carotenoids"),
           ("Infrared (beyond about 750 nm)", "Less energy per photon than visible light, and plant pigments barely absorb it")],
          "Photon energy rises as wavelength shortens; within the visible range, chlorophyll's peaks are blue and red, and "
          "carotenoids absorb only in the blue to blue-green.",
          "Wavelength and energy · Chlorophyll absorption · Accessory pigments",
          ["m8_spectrum_wavelength_energy", "m8_chlorophyll_absorption", "m8_accessory_pigments"], points=3),
    match(PG, "After a photon is absorbed", "Match each situation to what happens to the absorbed energy.", "Situation",
          "What happens",
          [("Laundry brightener glowing blue under an ultraviolet lamp", "Light is given off again, at a longer wavelength"),
           ("A leaf in full sun absorbing more light than it can use", "Much of the extra energy is released as heat"),
           ("An antenna chlorophyll packed among others", "The excitation passes to a neighbouring pigment"),
           ("The reaction-center pair of a photosystem", "The excited electron itself leaves for an acceptor molecule")],
          "An excited pigment loses its energy as heat or fluorescence, or passes it on. In a photosystem, antenna pigments "
          "pass energy along and the reaction-center pair passes an electron to an acceptor.",
          "Fates of an excited state · Antenna and reaction center",
          ["m8_excited_state_fates", "m8_antenna_transfer", "m8_reaction_center"], points=3),
    tf(PG, "Since the blue photon carries about 1.5 times the energy of the red one, it drives about 1.5 times as much photosynthesis.", False,
       "Each absorbed photon raises one electron to the same lowest excited state; the blue photon's extra energy is lost "
       "as heat first, so the two drive about the same amount.",
       "Wavelength and photon energy", ["m8_spectrum_wavelength_energy"], points=1,
       box="A plant absorbs one blue photon (450 nm) and one red photon (680 nm)."),
    tf(PG, "A dye that absorbs mainly green light (about 530 nm) could fluoresce blue (about 450 nm).", False,
       "Some absorbed energy is lost as heat first, so fluorescence has a longer wavelength, with less energy per photon, "
       "than the light absorbed.",
       "Fates of an excited state", ["m8_excited_state_fates"], points=2,
       box="A highlighter dye absorbs light and quickly re-emits light (fluorescence)."),
    tf(PG, "Because the difference lies in the ring rather than the tail, the two absorb different wavelengths but anchor "
           "in the membrane the same way.", True,
       "The porphyrin ring is the light-absorbing part, so changing one of its side groups shifts the absorption peaks "
       "(chlorophyll a near 430 and 662 nm, chlorophyll b near 455 and 642 nm).",
       "Chlorophyll structure", ["m8_chlorophyll_structure"], points=2,
       box="Chlorophylls a and b have the same tail and differ only in one side group on the porphyrin ring shown in the diagram.",
       diagram="m8_chlorophyll"),
    tf(PG, "Adding magnesium to the soil would let new leaves make normal amounts of chlorophyll again.", True,
       "Every chlorophyll molecule has a Mg ion at the centre of its porphyrin ring, so without enough Mg the plant can't "
       "make enough chlorophyll; with Mg restored, new leaves can green up.",
       "Chlorophyll structure · Real-world: magnesium deficiency", ["m8_chlorophyll_structure"], points=1,
       box="Crops grown in soil low in magnesium develop yellowing leaves."),
    tf(PG, "The yellow pigments are a dark-only substitute that the seedlings break down once they turn green.", False,
       "The yellow pigments are carotenoids, which stay and work alongside the new chlorophyll; the seedlings were pale "
       "because chlorophyll was missing, not because they had different pigments.",
       "Accessory pigments · Real-world: dark-grown seedlings", ["m8_accessory_pigments"], points=1,
       box="Bean seedlings sprouted in the dark are pale yellow; moved into light, they turn green within a day."),
    tf(PG, "In dim light, the mutant would photosynthesize about as fast as a normal alga, since its reaction centers are normal.", False,
       "In dim light, few photons strike a reaction center directly; the antenna gathers light over a much larger area and "
       "passes the energy on, so with a small antenna each reaction center is excited less often.",
       "Antenna energy transfer", ["m8_antenna_transfer"], points=2,
       box="In the diagram, many antenna chlorophylls surround one reaction-center pair. A mutant alga has normal reaction "
           "centers but only a small fraction of the usual antenna.", diagram="m8_photosystem"),
    tf(PG, "The leaf captures green light (about 550 nm) mainly because its carotenoids absorb strongly there.", False,
       "The diagram shows carotenoids absorb almost nothing beyond about 510 nm. Green light is captured because light "
       "scattered through many chlorophyll-filled cell layers gets many chances to be absorbed.",
       "Leaves absorb most of the spectrum · Accessory pigments", ["m8_accessory_pigments", "m8_chlorophyll_absorption"], points=2,
       box="An intact leaf absorbs most of the visible light that strikes it, even though a chlorophyll solution absorbs "
           "green light poorly. The diagram shows the absorption of three leaf pigments.", diagram="m8_absorption_spectra"),
    tf(PG, "Each infrared photon has too little energy to raise chlorophyll to an excited state, so even very bright infrared "
           "light drives almost no photosynthesis.", True,
       "A photon is absorbed only if its energy matches a jump to an excited state. Infrared photons carry less energy than "
       "red ones, and adding more of them doesn't give any single photon enough.",
       "Photon excitation · Wavelength and photon energy", ["m8_photon_excitation", "m8_spectrum_wavelength_energy"], points=2,
       box="Sunlight includes a great deal of infrared light, with wavelengths longer than about 750 nm."),
    mc(PG, "In 1882, Theodor Engelmann lit a strand of green alga with light spread into a spectrum and watched O2-seeking "
           "bacteria gather along it. Where did most bacteria gather?",
       "At the blue and red parts of the strand",
       ["At the green and yellow parts of the strand",
        "Evenly along the whole strand",
        "At the violet end, where photons carry the most energy",
        "Past the red end, in the infrared"],
       "O2 is released fastest where photosynthesis is fastest, which is where chlorophyll absorbs best: blue and red.",
       "Chlorophyll absorbs blue and red · Real-world: Engelmann's experiment", ["m8_chlorophyll_absorption"], points=1),
    mc(PG, "Five LED lamps each give off the same light energy per second, each in one colour. Which lamp gives off the "
           "fewest photons per second?",
       "Blue, 450 nm", ["Blue, 450 nm", "Green, 530 nm", "Amber, 590 nm", "Red, 660 nm", "Far-red, 730 nm"],
       "Each blue photon carries the most energy, so the blue lamp needs the fewest photons to deliver the same energy per second.",
       "Wavelength and photon energy", ["m8_spectrum_wavelength_energy"], points=2, ordered=True, key_index=0),
    mc(PG, "Chlorophyllide is chlorophyll without the hydrocarbon tail shown in the diagram. Compared with chlorophyll, "
           "what would you expect of it?",
       "It still absorbs light, since the ring is intact, but no longer anchors in the membrane",
       ["It no longer absorbs light, since the tail is the part of chlorophyll that absorbs it",
        "It loses its Mg ion, since the tail is what holds the ion in the ring",
        "It moves deeper into the membrane, since the tail was the water-loving part of the molecule",
        "It is unchanged, since the tail plays no part in where chlorophyll sits"],
       "The porphyrin ring absorbs light and holds the Mg, so both stay; the hydrophobic tail is what anchors chlorophyll "
       "in the membrane's lipid bilayer.",
       "Chlorophyll structure", ["m8_chlorophyll_structure"], points=2, diagram="m8_chlorophyll"),
    mc(PG, "A molecule absorbs a photon only if the photon's energy matches the energy needed to raise one of its electrons "
           "to an excited state. Which observation does this rule explain?",
       "Chlorophyll absorbs blue and red light but little green",
       ["Fluorescence has a longer wavelength than the light absorbed",
        "Blue photons carry more energy than red photons",
        "Antenna pigments pass their energy to the reaction center",
        "Excited electrons fall back within billionths of a second"],
       "Only photons whose energy matches one of chlorophyll's excitation jumps are absorbed, which is why it takes blue "
       "and red but lets most green pass. The other observations are true but have other causes, such as heat loss "
       "(fluorescence) or wavelength (photon energy).",
       "Photon excitation · Chlorophyll absorption", ["m8_photon_excitation", "m8_chlorophyll_absorption"], points=2),
    mc(PG, "A corn mutant can't make carotenoids. In bright sunlight its seedlings turn white and die. Which explanation fits best?",
       "Without carotenoids, excess light damages the photosynthetic machinery",
       ["Without carotenoids, the seedlings can no longer absorb red light well",
        "Without carotenoids, chlorophyll is made but can't pass its energy on to the reaction centers",
        "Without carotenoids, the seedlings can't make chlorophyll in the first place",
        "Without carotenoids, the leaves reflect most of the blue light falling on them"],
       "Carotenoids protect the photosynthetic components from damage; without them, bright light destroys chlorophyll (photobleaching).",
       "Accessory pigments protect", ["m8_accessory_pigments"], points=2),

    # ================================================================ Photosystems & Electron Transport
    case(PS, "Weed killers that jam photosystem II",
         "Atrazine and diuron, two widely used weed killers, kill plants by binding photosystem II in the pocket where "
         "plastoquinone normally docks." + STEM_TAIL,
         box("With the pocket blocked, electrons can't pass from photosystem II to plastoquinone.",
             "Some weeds have become resistant to atrazine through a single amino-acid change in the pocket that greatly "
             "weakens its binding."),
         [S("Treated plants die mainly because the herbicide stops their chlorophyll from absorbing light, so no energy can "
            "enter the leaf.", False,
            "The pigments still absorb light, but the energy can't leave photosystem II as electron flow; it forms reactive "
            "oxygen that wrecks membranes, which kills the weed faster than starvation would."),
          S("With the QB pocket blocked, the plastoquinone pool in the diagram gets no electrons from photosystem II, so "
            "linear electron flow stops making NADPH and the Calvin cycle stalls.", True,
            "PSII and PSI work in series, so no electrons from water reach PSI and NADP+ (가); without NADPH the cycle can't "
            "run, even though cyclic flow around PSI can still make some ATP."),
          S("In a resistant weed from (나), plastoquinone still docks in the pocket, so electrons keep flowing even when "
            "atrazine is present.", True,
            "If atrazine can't bind well, plastoquinone still docks and electrons keep flowing, though usually a little more "
            "slowly than in unaltered weeds."),
          ],
         "Photosystems in series · NADPH from PSI · Real-world: PSII herbicides",
         ["m8_two_photosystems_series", "m8_psi_nadph"], points=3, diagram="m8_herbicide_site"),
    combo(PS, "Reading the Z", DIAG,
          box("An asterisk (*) marks a photosystem whose reaction center has just been excited by light.",
              "The cytochrome b6f complex sits between plastoquinone (PQ) and plastocyanin (PC)."),
          [S("Electrons end at NADP+ with more energy than they had in H2O, so their overall flow needs an input of light energy.", True,
             "NADP+ sits above H2O on the energy axis; light absorbed at the two photosystems supplies the difference."),
           S("Electrons reach PSI with more energy than they had at PSII*, because the b6f complex adds energy.", False,
             "Energy falls from PSII* through PQ, b6f and PC, so electrons arrive at PSI lower than they were at PSII*."),
           S("As electrons fall from PQ to PC, the energy they release moves H+ out of the lumen into the stroma.", False,
             "The b6f complex (나) uses it to move H+ from the stroma into the lumen, building the gradient that drives ATP synthase."),
           ],
          "Z scheme · Thylakoid H+ gradient",
          ["m8_z_scheme", "m8_thylakoid_proton_gradient"], points=3, diagram="m8_z_scheme"),
    combo(PS, "ATP from an acid bath", READ,
          box("In 1966, isolated thylakoids were soaked in pH 4 buffer until their lumens were acidic, then moved quickly into "
              "pH 8 buffer containing ADP and Pi, in the dark.",
              "The thylakoids made a burst of ATP without any light."),
          [S("(나) shows that an H+ gradient alone is enough to drive ATP synthase.", True,
             "With no light and no electron flow, the only energy source was the imposed gradient."),
           S("Once the thylakoids were in the pH 8 buffer, the ATP was made as H+ flowed through ATP synthase from the buffer "
             "into the acidic lumen.", False,
             "H+ flows down its gradient, from the acidic lumen (high H+) out to the pH 8 buffer (low H+), through ATP synthase."),
           S("The burst soon stops because, in the dark, nothing rebuilds the H+ gradient once it has run down.", True,
             "In a leaf, light-driven electron flow keeps refilling the lumen with H+; here the gradient was used up and not replaced."),
           ],
          "Photophosphorylation · Thylakoid H+ gradient · Real-world: Jagendorf's acid-bath experiment",
          ["m8_photophosphorylation", "m8_thylakoid_proton_gradient"], points=3),
    combo(PS, "Electrons that loop back to b6f", READ,
          box("Linear electron flow: H2O → PSII → PQ → b6f → PC → PSI → ferredoxin → NADP+.",
              "In cyclic electron flow, electrons leaving PSI pass back to the b6f complex and then return to PSI."),
          [S("Cyclic flow in (나) still moves H+ into the lumen, so it can make ATP.", True,
             "Electrons still pass through the b6f complex, which builds the H+ gradient that drives ATP synthase."),
           S("A chloroplast running only cyclic flow would soon stop fixing CO2, even in bright light.", True,
             "Cyclic flow makes no NADPH, so 1,3-bisphosphoglycerate can't be reduced to triose phosphate and the Calvin cycle stalls."),
           S("Cyclic flow in (나) needs light just as linear flow does, since the electrons lose energy at b6f and PSI must "
             "raise them again on every turn.", True,
             "Electrons returning from b6f reach PSI with less energy than they had at PSI*; only a new photon at PSI can lift "
             "them again, so cyclic flow stops in the dark."),
           ],
          "Cyclic electron transport · Calvin cycle needs NADPH",
          ["m8_cyclic_electron_transport", "m8_calvin_overview"], points=2),
    match(PS, "Knocking out the thylakoid chain", "Match each blocked component to its most direct effect in the light.",
          "Blocked component", "Most direct effect",
          [("Photosystem II", "Water is no longer split, so no O2 is released"),
           ("Plastoquinone", "Electrons can't leave PSII for the b6f complex"),
           ("Plastocyanin", "PSI's oxidized reaction center isn't refilled"),
           ("Photosystem I", "Electrons reach plastocyanin but aren't raised high enough to reduce NADP+"),
           ("ATP synthase", "H+ piles up in the lumen, but no ATP is made")],
          "Electrons go water → PSII → plastoquinone → b6f → plastocyanin → PSI → NADP+, so blocking a carrier stops the step "
          "it serves; blocking ATP synthase leaves the H+ gradient unused.",
          "PSII takes electrons from water · PQ and PC carriers · PSI makes NADPH · Photophosphorylation",
          ["m8_psii_water", "m8_carriers_pq_pc", "m8_psi_nadph", "m8_photophosphorylation"], points=3),
    match(PS, "Take one thing away",
          "Isolated chloroplasts work normally in bright light until one item is taken away. Match each item removed to its most direct effect.",
          "Item removed", "Most direct effect",
          [("Light", "Neither photosystem's reaction center is excited"),
           ("NADP+", "Electrons leaving PSI have no final acceptor"),
           ("CO2", "Carboxylation stops, so ATP and NADPH stop being used"),
           ("O2", "Photosynthesis carries on, since O2 is a product, not an input")],
          "Light drives both photosystems; NADP+ is the final acceptor of linear electron flow; CO2 is the Calvin cycle's "
          "substrate, and the cycle is what spends ATP and NADPH; O2 is released from water, not used.",
          "Light excites the photosystems · NADP+ the final acceptor · Two linked stages · Water is the electron donor",
          ["m8_psi_nadph", "m8_two_stages_linked", "m8_water_electron_donor", "m8_carboxylation_rubisco"], points=3),
    tf(PS, "In light, its PSII keeps splitting water at the normal rate, since PSII hands its electrons to plastoquinone "
           "(PQ), not to plastocyanin.", False,
       "With plastocyanin stuck, electrons back up through b6f and the plastoquinone pool, so PSII has nowhere to send them "
       "and soon stops splitting water.",
       "Plastoquinone and plastocyanin · Photosystems in series", ["m8_carriers_pq_pc", "m8_two_photosystems_series"], points=2,
       box="In the chain shown in the diagram, a mutant plant's plastocyanin (PC) cannot pass electrons to PSI.",
       diagram="m8_thylakoid_membrane"),
    tf(PS, "A chemical that lets H+ leak freely across the thylakoid membrane would stop ATP synthesis, but electron flow "
           "from water to NADP+ would continue.", True,
       "ATP synthase runs on the H+ gradient, which the leak collapses; electron flow doesn't depend on making ATP, so "
       "with NADP+ supplied it continues (as with DNP in mitochondria). In a leaf it would soon stop, because without ATP "
       "the Calvin cycle can't turn NADPH back into NADP+.",
       "Photophosphorylation · Thylakoid H+ gradient", ["m8_photophosphorylation", "m8_thylakoid_proton_gradient"], points=2,
       box="Isolated thylakoids like the membrane in the diagram are lit brightly and given ADP, Pi, ferredoxin and plenty "
           "of NADP+. Electron flow keeps their lumens far more acidic than the surrounding buffer.",
       diagram="m8_thylakoid_membrane"),
    tf(PS, "The ATP made here has to cross the thylakoid membrane before the Calvin cycle can use it.", False,
       "CF1, the part that makes ATP, faces the stroma, so the ATP is released right where the Calvin cycle runs.",
       "Photophosphorylation · Stage locations", ["m8_photophosphorylation", "m8_stage_locations"], points=1,
       box="Chloroplast ATP synthase sits in the thylakoid membrane."),
    tf(PS, "The cytosol of the leaf's cells would soon run short of ATP for making proteins.", False,
       "Chloroplast ATP stays in the chloroplast for the Calvin cycle; the cytosol depends on mitochondrial respiration "
       "for much of its ATP, and the mitochondria still work, so it is carbon fixation that stops.",
       "Chloroplast ATP stays in the chloroplast", ["m8_chloroplast_atp_stays"], points=2,
       box="In bright light, a drug blocks only the chloroplasts' ATP synthase in a leaf."),
    tf(PS, "These cells get most of their ATP from respiration in their mitochondria, by oxidizing sugar made in the leaves.", True,
       "Roots don't photosynthesize; like all plant cells they respire, using sugar carried down from the leaves.",
       "Non-green cells respire sugar from the leaves · Real-world: carrot roots",
       ["m8_photosynthesis_definition"],
       points=1, box="The cells of a carrot root are not green and carry out no photosynthesis."),
    tf(PS, "If PSII could not take electrons from water, it would soon stop passing electrons on, even in bright light.", True,
       "An oxidized reaction center must get an electron back from a donor before it can work again, and water is PSII's donor.",
       "Reaction center · PSII takes electrons from water", ["m8_reaction_center", "m8_psii_water"], points=1,
       box="Each time PSII's reaction center is excited, it loses an electron to an acceptor."),
    tf(PS, "PSI therefore takes its replacement electrons from the lumen side of the membrane, while it hands electrons "
           "to ferredoxin on the stroma side.", True,
       "Plastocyanin refills PSI's oxidized reaction center from the lumen side, and the excited electron leaves on the "
       "stroma side, where ferredoxin carries it on to NADP+.",
       "Reaction center · Plastocyanin feeds PSI", ["m8_reaction_center", "m8_carriers_pq_pc"], points=2,
       box="Plastocyanin is a small protein that diffuses through the thylakoid lumen."),
    tf(PS, "For each O2 released, 4 electrons pass along the chain, enough to reduce 2 NADP+ to NADPH.", True,
       "2 H2O → O2 + 4 H+ + 4 e−, and each NADP+ takes 2 electrons, so 4 electrons reduce 2 NADP+.",
       "PSII takes electrons from water · Electrons per NADPH", ["m8_psii_water"], points=2,
       box="Linear electron flow carries electrons from water all the way to NADP+."),
    tf(PS, "In light, the mutant would still release some O2, though more slowly than a normal alga.", False,
       "Only PSII splits water, so without it no O2 is released; cyclic flow still makes ATP because its electrons pass through b6f.",
       "Cyclic electron transport · PSII splits water", ["m8_cyclic_electron_transport", "m8_psii_water"], points=2,
       box="A mutant alga lacks photosystem II but can still run cyclic electron flow through photosystem I and the b6f complex."),
    mc(PS, "Thylakoids supplied with NADP+ and ferredoxin are treated with diuron (which blocks electron flow from PSII to "
           "plastoquinone) and given an artificial donor that feeds electrons straight into plastocyanin. In light, what happens?",
       "NADPH forms again, but no O2 is released",
       ["NADPH forms again, and O2 is now released at photosystem I",
        "Both O2 release and NADPH formation resume",
        "Neither O2 release nor NADPH formation resumes",
        "O2 is released again, but no NADPH forms"],
       "The donor feeds PSI, which can still reduce NADP+ by way of ferredoxin; PSII stays blocked, so it stops splitting "
       "water and no O2 is released.",
       "Photosystems in series · PSII splits water · PSI makes NADPH · Real-world: diuron and artificial electron donors",
       ["m8_two_photosystems_series", "m8_psii_water", "m8_psi_nadph"], points=2, diagram="m8_z_scheme"),
    mc(PS, "A leaf is moved from darkness into bright light. Within a minute, how do the pH values of the thylakoid lumen "
           "and the stroma change?",
       "The lumen's pH falls and the stroma's rises",
       ["Both fall, since the light reactions release H+",
        "Both rise, since the light reactions use up H+",
        "The lumen's pH rises and the stroma's falls",
        "Neither changes, since H+ is moved between them rather than made"],
       "Electron flow moves H+ from the stroma into the lumen, and splitting water adds H+ to the lumen, so the lumen "
       "becomes more acidic and the stroma more alkaline.",
       "Thylakoid H+ gradient · pH", ["m8_thylakoid_proton_gradient", "m2_ph_hydrogen_ions"], points=2,
       diagram="m8_thylakoid_membrane"),
    mc(PS, "Why do the light reactions need two photosystems working in series?",
       "Energy lost along the chain must be restored by a second light input",
       ["PSI splits water, while PSII reduces NADP+ at the very end of the chain",
        "Two photosystems can split water twice as fast as one",
        "PSII works only in bright light, and PSI takes over in dim light",
        "One photosystem absorbs only blue light and the other only red"],
       "Electrons lose energy from PSII through PQ, b6f and PC; PSI's second boost lifts them high enough to reduce NADP+ "
       "(the Z scheme). Both photosystems absorb red and blue light, and water is split at PSII, not PSI.",
       "Z scheme · Two photosystems in series", ["m8_z_scheme", "m8_two_photosystems_series"], points=2),
    mc(PS, "At least how many photons must the two photosystems absorb for each O2 that linear electron flow releases?",
       "8", ["2", "4", "6", "8", "12"],
       "Each O2 comes from 2 H2O, which give up 4 electrons, and each electron is boosted once at PSII and once at PSI: "
       "4 × 2 = 8. Four would count only one photon per electron.",
       "Two photosystems in series · PSII takes electrons from water", ["m8_two_photosystems_series", "m8_psii_water"],
       points=2, ordered=True, key_index=3),
    mc(PS, "A mutant plant that can't run cyclic electron flow is grown in bright light. Which change would you expect "
           "in its chloroplasts?",
       "Too little ATP for the Calvin cycle, while NADPH builds up",
       ["Too little NADPH for the Calvin cycle, while ATP builds up",
        "No O2 release, because photosystem II stops working",
        "No H+ gradient at all across the thylakoid membrane",
        "Both ATP and NADPH run short, since cyclic flow normally supplies both"],
       "Cyclic flow normally adds ATP without NADPH to meet the cycle's 3 ATP : 2 NADPH need; linear flow alone still "
       "splits water and pumps H+, but makes too little ATP for its NADPH.",
       "Cyclic electron transport · Calvin cycle stoichiometry",
       ["m8_cyclic_electron_transport", "m8_calvin_stoichiometry"], points=2),
    mc(PS, "The herbicide paraquat takes electrons from photosystem I before they reach ferredoxin. Which process of the light "
           "reactions does it stop most directly?",
       "Reduction of NADP+ to NADPH",
       ["Splitting of water at photosystem II", "Absorption of light by antenna pigments",
        "Reduction of plastoquinone at photosystem II", "Release of H+ into the lumen from water"],
       "Electrons diverted after PSI never reach ferredoxin and NADP+, so NADPH formation stops; the earlier steps can still run.",
       "PSI makes NADPH · Real-world: paraquat", ["m8_psi_nadph"], points=1),

    # ================================================================ Calvin Cycle
    case(CC, "Pumping CO2 into a greenhouse",
         "Commercial greenhouse growers often pump in extra CO2, raising it to about 1000 ppm, more than twice the outdoor level." + STEM_TAIL,
         box("Rubisco, the enzyme that adds CO2 to RuBP, works well below its top speed at outdoor CO2 levels.",
             "In winter, many growers set a higher CO2 target on bright days than on dull ones."),
         [S("In bright light, enrichment speeds photosynthesis mainly because the extra CO2 supplies more of the NADPH the "
            "Calvin cycle needs to reduce 3-phosphoglycerate.", False,
            "CO2 is rubisco's substrate in carboxylation; NADPH comes from the light reactions, not from CO2."),
          S("In bright light, enrichment from 420 to 1000 ppm raises the rate from about 65% to over 90% of maximum, because "
            "rubisco gets more of its substrate.", True,
            "The bright-light curve is still climbing at 420 ppm, so carboxylation is limited by CO2 there (가)."),
          S("On dull days, extra CO2 adds much less than on bright days, because light rather than CO2 then limits the rate.", True,
            "The dim-light curve rises only from about 33% to 40%: in dim light the light reactions supply ATP and NADPH "
            "slowly, so the cycle is short of them more than of CO2, which fits (나)."),
          ],
         "Rubisco carboxylation · Calvin cycle needs ATP and NADPH · Real-world: greenhouse CO2 enrichment",
         ["m8_carboxylation_rubisco", "m8_calvin_overview", "m8_two_stages_linked"], points=3, diagram="m8_co2_curves"),
    case(CC, "Following a radioactive carbon",
         "In the late 1940s and early 1950s, Melvin Calvin's team fed radioactive 14CO2 to illuminated algae (Chlorella), "
         "killed samples from a few seconds to a minute later, and identified which compounds were radioactive." + STEM_TAIL,
         box("Rubisco joins CO2 to RuBP, a five-carbon sugar.",
             "When the light was switched off, 3-phosphoglycerate levels rose and RuBP levels fell."),
         [S("Since 3-phosphoglycerate holds most of the label at first, it is the carbohydrate the cycle exports to the rest "
            "of the plant.", False,
            "It is the first stable product, but it is then reduced to triose phosphate; the label moves on into sugar "
            "phosphates, and triose phosphate is what leaves the cycle."),
          S("The data fit CO2 joining a five-carbon acceptor whose six-carbon product splits at once into two 3-phosphoglycerate.", True,
            "Rubisco adds CO2 to RuBP (5C); the unstable 6C product splits into two 3-phosphoglycerate, one of which carries "
            "the new 14C, so 3-phosphoglycerate is labelled first."),
          S("(나) happens because carboxylation continues briefly in the dark, while turning 3-phosphoglycerate back into "
            "RuBP needs light-made ATP and NADPH.", True,
            "Carboxylation uses up RuBP and makes 3-phosphoglycerate without ATP, but the steps that reduce "
            "3-phosphoglycerate and remake RuBP need ATP and NADPH."),
          ],
         "Carboxylation by rubisco · Reduction and regeneration need ATP and NADPH · Real-world: Calvin's 14C experiments",
         ["m8_carboxylation_rubisco", "m8_reduction_step", "m8_regeneration_rubp"], points=3, diagram="m8_c14_timecourse"),
    combo(CC, "Counting carbons around the cycle", DIAG,
          box("In steady light, a chloroplast keeps its RuBP pool at a constant size.",
              "Suppose a chloroplast starts exporting triose phosphate faster than usual."),
          [S("Fixing 3 CO2 uses 3 RuBP and produces 6 molecules of 3-phosphoglycerate.", True,
             "Each CO2 joins one RuBP, and each six-carbon product splits into two 3-phosphoglycerate: 3 × 2 = 6."),
           S("For every 3 CO2 fixed, 6 triose phosphates are made; only 3 of them are needed to rebuild the 3 RuBP, so half "
             "can leave the cycle.", False,
             "3 RuBP hold 15 carbons, which takes 5 triose phosphates (5 × 3 = 15); only 1 in 6 can leave if the RuBP pool "
             "is to stay the same size (가)."),
           S("If the chloroplast in (나) exported 2 of every 6 triose phosphates, RuBP would be regenerated faster and the "
             "cycle would speed up.", False,
             "The 4 triose phosphates left (12 C) can't rebuild 3 RuBP (15 C), so the RuBP pool shrinks and the cycle slows."),
           ],
          "Calvin cycle stoichiometry · Regeneration of RuBP · Carboxylation",
          ["m8_calvin_stoichiometry", "m8_regeneration_rubp", "m8_carboxylation_rubisco"], points=3, diagram="m8_calvin_cycle"),
    combo(CC, "Arabidopsis without leaf starch", READ,
          box("Leaves store some of the day's triose phosphate as starch inside their chloroplasts.",
              "Mutants of the small plant Arabidopsis that can't make leaf starch grow normally in continuous light but poorly in "
              "short days with long nights."),
          [S("The mutants in (나) struggle in long nights because they run out of sugar to respire before dawn.", True,
             "Without starch, the mutants have only the sugars left at dusk; in a long night these run out before dawn and "
             "the plants starve. In continuous light the Calvin cycle never stops, so no store is needed."),
           S("At night, the Calvin cycle keeps running on stored starch, which supplies the ATP and NADPH it needs.", False,
             "The Calvin cycle's ATP and NADPH come from the light reactions; starch is broken down for respiration, not to run the cycle."),
           S("Starch stored by day is broken down into sugars at night, which leaf cells respire to make ATP.", True,
             "Starch is a glucose polymer; the sugars released feed glycolysis and respiration for the night-time ATP supply."),
           ],
          "Starch stores carbohydrate for the night · Calvin cycle needs light-made ATP and NADPH · Glucose stores · "
          "Real-world: starchless Arabidopsis mutants",
          ["m8_starch_for_night", "m8_calvin_overview", "m7_glycogen_starch_storage"], points=2),
    match(CC, "Steps of the Calvin cycle", "Match each step to what happens in it.", "Step", "What happens",
          [("Carboxylation", "A five-carbon sugar gains a carbon from the air"),
           ("Reduction, first part", "3-phosphoglycerate gains a phosphate from ATP"),
           ("Reduction, second part", "1,3-bisphosphoglycerate gains electrons from NADPH"),
           ("Regeneration", "Fifteen carbons are reshuffled into three five-carbon acceptors"),
           ("Carbohydrate output", "Three carbons leave for every three CO2 fixed")],
          "Carboxylation adds CO2 to RuBP; ATP then phosphorylates 3-phosphoglycerate, and NADPH reduces the product to "
          "triose phosphate; regeneration rebuilds three RuBP (15 C) from five triose phosphates, so one triose phosphate "
          "(3 C) leaves for every 3 CO2 fixed.",
          "Carboxylation · Reduction · Regeneration · Stoichiometry",
          ["m8_carboxylation_rubisco", "m8_reduction_step", "m8_regeneration_rubp", "m8_calvin_stoichiometry"], points=3),
    tf(CC, "Since each rubisco molecule is reused over and over, halving a leaf's rubisco would barely slow its CO2 fixation "
           "in bright light.", False,
       "Reuse doesn't make any one enzyme faster. Each active site fixes only about 3 CO2 per second, so in bright light "
       "total fixation depends on how much rubisco there is, and halving it cuts fixation a lot.",
       "Enzymes are reused (Module 6) · Real-world: rubisco", ["m6_enzyme_cycle"], points=2,
       box="Rubisco makes up as much as half of the soluble protein in a leaf, yet each of its active sites fixes only about "
           "3 CO2 per second."),
    tf(CC, "The label reaching RuBP shows that some of the newly fixed carbon is used to rebuild the CO2 acceptor.", True,
       "Five of every six triose phosphates are rearranged back into RuBP, so carbon fixed a few seconds earlier soon turns "
       "up in RuBP; this is what makes the pathway a cycle.",
       "Regeneration of RuBP", ["m8_regeneration_rubp"], points=2,
       box="Within a minute of adding 14CO2 to illuminated algae, their RuBP is radioactive too."),
    tf(CC, "If NADPH ran out but ATP stayed plentiful, the cycle could still make triose phosphate using ATP alone.", False,
       "ATP only adds a phosphate, giving 1,3-bisphosphoglycerate; it takes electrons from NADPH to reduce that to "
       "higher-energy triose phosphate.",
       "Reduction step", ["m8_reduction_step"], points=2,
       box="In the reduction step, 3-phosphoglycerate becomes triose phosphate, a three-carbon sugar with more potential energy."),
    tf(CC, "It spent equal numbers of ATP and NADPH to make it, since each 3-phosphoglycerate reduced uses one of each.", False,
       "Reduction uses 6 ATP and 6 NADPH, but regenerating the 3 RuBP takes 3 more ATP: 9 ATP and 6 NADPH.",
       "Calvin cycle stoichiometry", ["m8_calvin_stoichiometry"], points=2,
       box="A chloroplast in steady light exports one triose phosphate."),
    tf(CC, "Both the reduction step and the regeneration of RuBP would slow down.", True,
       "Both steps use ATP: 6 ATP to phosphorylate 3-phosphoglycerate and 3 more to regenerate 3 RuBP. NADPH is spent "
       "only in reduction, so plenty of it can't make up for the missing ATP.",
       "Regeneration of RuBP · Reduction step", ["m8_regeneration_rubp", "m8_reduction_step"], points=2,
       box="A chloroplast in bright light runs short of ATP, while its NADPH stays plentiful."),
    tf(CC, "RuBP builds up and 3-phosphoglycerate falls, because carboxylation stops while regeneration continues.", True,
       "Without CO2, rubisco can no longer carboxylate RuBP, but the light reactions still power reduction and regeneration "
       "for a while, so RuBP accumulates and 3-phosphoglycerate is used up.",
       "Carboxylation · Regeneration of RuBP", ["m8_carboxylation_rubisco", "m8_regeneration_rubp"], points=2,
       box="A leaf in bright light is suddenly given air with no CO2.", diagram="m8_calvin_cycle"),
    tf(CC, "The dawn leaves stain darker, because starch keeps building up overnight while the Calvin cycle rests.", False,
       "Starch made by day is broken down at night to supply sugar for the leaf's respiration and for export to the rest "
       "of the plant, so the dusk leaves stain darker.",
       "Starch is stored by day and used at night", ["m8_starch_for_night"], points=1,
       box="Leaves picked from one plant at dusk and at dawn are tested with iodine, which stains starch blue-black."),
    mc(CC, "Using the diagram, how many triose phosphates must the Calvin cycle make in all, recycled and exported, to "
           "export the carbon for one glucose?",
       "12", ["2", "6", "10", "12", "18"],
       "6 CO2 give 12 3-phosphoglycerate and so 12 triose phosphates; 10 rebuild the 6 RuBP and 2 leave (6 C), enough "
       "for one glucose.",
       "Calvin cycle stoichiometry · Regeneration of RuBP", ["m8_calvin_stoichiometry", "m8_regeneration_rubp"], points=2,
       ordered=True, key_index=3, diagram="m8_calvin_cycle"),
    mc(CC, "How many NADPH does the Calvin cycle use to make the carbon for one glucose?",
       "12", ["6", "9", "12", "18", "24"],
       "Each CO2 fixed needs 2 NADPH (6 NADPH per 3 CO2), so 6 CO2 need 12. 18 is the ATP count (9 per 3 CO2), not the NADPH count.",
       "Calvin cycle stoichiometry · Reduction step", ["m8_calvin_stoichiometry", "m8_reduction_step"], points=2,
       ordered=True, key_index=2),
    mc(CC, "By day, a leaf turns much of its spare triose phosphate into starch rather than keeping it as free sugar. What "
           "is the main advantage?",
       "Huge starch molecules barely add to the chloroplast's solute concentration",
       ["Each glucose unit in starch stores more energy than a free glucose does",
        "Starch can be broken down at night without any enzymes",
        "Free sugar would block rubisco's active site and stop carbon fixation",
        "Starch can leave the chloroplast by diffusion, while free sugar can't cross the membranes"],
       "Packing thousands of glucose units into one polymer keeps the number of dissolved particles low, so the chloroplast "
       "doesn't draw in water as it stores the day's sugar; enzymes free the glucose again at night.",
       "Starch stores carbohydrate for the night · Storage polysaccharides (Module 2)",
       ["m8_starch_for_night", "m2_polysaccharides_storage"], points=2),
    mc(CC, "Photosynthesis reduces CO2 to carbohydrate. At which point in the Calvin cycle does the carbon actually gain electrons?",
       "When NADPH reduces 1,3-bisphosphoglycerate",
       ["When rubisco joins CO2 to RuBP",
        "When ATP adds a phosphate to 3-phosphoglycerate",
        "When triose phosphates are rearranged into RuBP",
        "When triose phosphate leaves the cycle"],
       "Joining CO2 to RuBP fixes carbon but doesn't reduce it, and ATP only adds a phosphate; the electrons come from "
       "NADPH in the second part of the reduction step.",
       "Reduction step · Photosynthesis is a redox process", ["m8_reduction_step", "m8_photosynthesis_redox"], points=2),
    mc(CC, "A potato tuber grows underground and fills with starch. Which sequence traces one of its carbon atoms from the "
           "air into that starch?",
       "CO2 → 3-phosphoglycerate → triose phosphate → sugar sent from the leaf → starch in the tuber",
       ["CO2 → fixed by the tuber's own cells underground → starch in the tuber",
        "CO2 → 3-phosphoglycerate → glycogen stored in the leaf → sugar sent to the tuber → starch in the tuber",
        "Carbon from soil minerals → roots → sugar in the tuber → starch",
        "CO2 → triose phosphate → 3-phosphoglycerate → sugar sent from the leaf → starch in the tuber"],
       "Rubisco fixes CO2 into 3-phosphoglycerate, which is reduced to triose phosphate in the leaf; sugar made from it "
       "travels to the tuber, which can't photosynthesize underground, and is stored as starch.",
       "Calvin cycle makes carbohydrate · Reduction step · Real-world: potato tubers",
       ["m8_calvin_overview", "m8_reduction_step"], points=2),
])
