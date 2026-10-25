"""Bridge: Connecting Modules 1–8."""
from cardkit import S, combo, case, tf, mc, match, box, with_mod, STEM_TAIL

T = "Connecting Modules 1–8"
READ = "Read (가) and (나). Which statements in <보기> are correct?"
DIAG = "Using the diagram, which statements in <보기> are correct?"

CARDS = with_mod(0, [
    # ---------------------------------------------------------------- 보기 combination
    combo(T, "Why electrons fall toward oxygen",
          "Cellular respiration moves electrons from the C-H bonds of fuel molecules to oxygen. " + DIAG,
          box("Oxygen is far more electronegative than carbon or hydrogen.",
              "In respiration, glucose's carbons end up in CO2, and the oxygen atoms of O2 end up in H2O."),
          [S("As electrons pass from glucose's C-H bonds into the O-H bonds of water, they end up held more tightly by a "
             "more electronegative atom, which releases energy.", True,
             "Electrons shared nearly equally in C-H bonds have high potential energy; pulled toward oxygen in polar O-H "
             "bonds, they have less, and the difference is released."),
           S("Fats need more O2 per gram to oxidize than sugars do, because their chains carry many C-H bonds and few "
             "oxygen atoms.", True,
             "Sugars already hold many O atoms, so they are partly oxidized; fatty acid chains are mostly C-H, so more O2 "
             "is needed to accept their electrons, which is also why fats yield more energy per gram."),
           S("If the chain's final acceptor pulled on electrons less strongly than O2 does, less energy would be released "
             "per pair of electrons passed along it.", True,
             "The energy released depends on how far the electrons fall; a weaker acceptor means a shorter fall and less "
             "energy for pumping H+."),
           ],
          "Electronegativity (Module 2) · O2 is the final electron acceptor (Module 7) · Lipids are energy-rich",
          ["m2_electronegativity_redox", "m7_o2_final_acceptor", "m7_lipids_energy_rich"], points=3,
          diagram="electronegativity_spectrum"),
    combo(T, "A vitamin inside an electron carrier",
          "NAD+ carries electrons from glycolysis and the citric acid cycle to the electron transport chain. " + DIAG,
          box("The body makes the nicotinamide part of NAD+ from the vitamin niacin (B3).",
              "Pellagra, caused by severe niacin deficiency, damages the skin, the gut and the brain."),
          [S("NAD+ is built from two nucleotides joined through their phosphate groups, one carrying adenine and one carrying nicotinamide.", True,
             "Each half is a base + ribose + phosphate, and the two phosphates link the halves, which is why it is called a dinucleotide."),
           S("Without enough niacin, as in (나), cells run short of NAD+, slowing glycolysis and the citric acid cycle, which need it to accept electrons.", True,
             "Both pathways stall without an oxidized carrier to accept electrons, so tissues with high energy demand suffer."),
           S("Extra dietary adenine would cure pellagra, since an adenine nucleotide makes up half of NAD+.", False,
             "The missing part is nicotinamide, which comes from niacin (or the amino acid tryptophan); cells can make "
             "adenine nucleotides themselves."),
           ],
          "Nucleotide structure (Module 2) · NAD+ as an electron carrier (Module 7) · Real-world: pellagra",
          ["m2_nucleotide_structure", "m7_carriers_nad_fad"], points=3, diagram="br_nad_structure"),
    combo(T, "Two organelles, two gradients",
          "Mitochondria and chloroplasts both make ATP using an H+ gradient across a membrane. " + DIAG,
          box("In both organelles, electron transport moves H+ across a membrane.",
              "In both, H+ flows back down its gradient through ATP synthase."),
          [S("H+ builds up in compartment 2 of the mitochondrion and in compartment D of the chloroplast.", True,
             "The ETC pumps H+ from the matrix (4) into the intermembrane space (2); in chloroplasts H+ moves from the stroma (F) into the lumen (D)."),
           S("In both organelles, ATP is released into the compartment where H+ is high.", False,
             "H+ flows from the high-H+ side through ATP synthase, and ATP is made on the other side: the matrix (4) and the stroma (F)."),
           S("Membranes 3 and C each hold an electron transport chain and ATP synthase.", True,
             "The inner mitochondrial membrane (3) and the thylakoid membrane (C) are the energy-converting membranes; the outer membranes are leaky."),
           ],
          "Double-membrane organelles (Module 3) · H+ gradients in mitochondria and chloroplasts (Modules 7-8)",
          ["m3_mito_chloro_membranes", "m7_proton_gradient", "m8_thylakoid_proton_gradient", "m8_photophosphorylation"],
          points=3, diagram="mito_chloro_compartments"),
    combo(T, "A bacterium's power plant",
          "E. coli can grow by aerobic respiration, using the same four stages as a human cell. " + READ,
          box("E. coli runs glycolysis, pyruvate oxidation, the citric acid cycle and oxidative phosphorylation.",
              "As a prokaryote, it has no mitochondria or other membrane-bound organelles."),
          [S("Its citric acid cycle enzymes work in the cytoplasm, the region that plays the part of the mitochondrial matrix.", True,
             "With no mitochondria (나), the cycle runs in the cytoplasm, the low-H+ side where ATP is made, as in the matrix."),
           S("Its electron transport chain and ATP synthase sit in its plasma membrane, which plays the part of the inner mitochondrial membrane.", True,
             "The chain needs a membrane that H+ can't cross; in a bacterium that is the plasma membrane."),
           S("Its pumps move H+ into the cytoplasm, which then plays the part of the intermembrane space as the high-H+ side.", False,
             "As in mitochondria, H+ is pumped out across the membrane; the cytoplasm, like the matrix, is the low-H+ side where ATP is made."),
           ],
          "Prokaryotes lack organelles (Module 1) · ETC location and proton pumping (Module 7)",
          ["m1_prokaryote_no_organelles", "m7_etc_location_components", "m7_proton_pumping", "m7_mito_compartments"], points=2),
    combo(T, "Keeping glucose flowing into a neuron",
          "Neurons depend on a steady supply of glucose from the blood. " + READ,
          box("Neurons take up glucose through GLUT3 carriers, by facilitated diffusion.",
              "Inside the neuron, hexokinase phosphorylates glucose as soon as it arrives."),
          [S("(나) keeps the concentration of free glucose inside the neuron low, so glucose keeps diffusing in down its gradient.", True,
             "Converting glucose to glucose 6-phosphate removes it from the pool GLUT3 sees, so the inward gradient is maintained."),
           S("If blood glucose fell sharply, glucose would enter the neuron more slowly, even though hexokinase keeps the "
             "inside concentration low.", True,
             "The inward rate depends on the size of the gradient, which also depends on the outside concentration; with "
             "less glucose outside, facilitated diffusion slows, which is why low blood sugar soon affects the brain."),
           S("The phosphate added in (나) is the first of the two ATP investments of glycolysis's first phase.", True,
             "Hexokinase spends one ATP (step 1) and phosphofructokinase a second (step 3) before the sugar is split."),
           ],
          "Facilitated diffusion (Module 3) · Phosphorylation traps glucose · Glycolysis phase 1 (Module 7)",
          ["m3_facilitated_diffusion_glut", "m7_phosphorylation_traps_glucose", "m7_glycolysis_phase1"], points=2),
    combo(T, "A machine that runs both ways",
          "ATP synthase and the Na+/K+ pump are both membrane proteins that link ATP to the movement of ions. " + DIAG,
          box("The Na+/K+ pump in the diagram uses ATP hydrolysis to move Na+ and K+ against their gradients.",
              "When E. coli ferments sugar with no O2 or other electron acceptor (such as nitrate) available, its ATP "
              "synthase runs backward, splitting ATP to pump H+ out across the plasma membrane."),
          [S("Running backward as in (나), ATP synthase works as primary active transport, like the pump in (가).", True,
             "It then uses energy from ATP hydrolysis directly to move ions against their gradient, the definition of primary active transport."),
           S("Which way ATP synthase runs depends on which releases more free energy under the conditions: H+ flowing down "
             "its gradient or ATP hydrolysis.", True,
             "The direction with a negative overall ΔG wins: a steep gradient drives synthesis; plenty of ATP and a weak gradient drive hydrolysis."),
           S("In the fermenting E. coli of (나), a drug that blocks ATP synthase would let the H+ gradient across its "
             "membrane run down.", True,
             "Here ATP synthase is what builds the gradient, spending ATP from glycolysis; blocked, it stops pumping, and "
             "the gradient leaks away."),
           ],
          "Primary active transport (Module 3) · ΔG sets the direction (Module 6) · ATP synthase and the H+ gradient (Module 7)",
          ["m3_primary_active_transport", "m7_atp_synthase", "m6_delta_g_sign", "m7_proton_gradient"], points=3,
          diagram="na_k_pump_cycle"),
    combo(T, "Two electron transport chains in one cell",
          "Plant cells run two electron transport chains, one in their mitochondria and one in their chloroplasts. " + READ,
          box("In mitochondria, electrons flow from NADH to O2.",
              "In chloroplasts, electrons taken from H2O pass through photosystems II and I."),
          [S("In the dark, a leaf cell can keep the chain in (가) running but not the chain in (나).", True,
             "The mitochondrial chain runs on electrons from food day and night; the chloroplast chain needs light at both "
             "photosystems to move water's electrons."),
           S("Both chains end by passing their electrons to O2.", False,
             "Only the mitochondrial chain ends at O2; the chloroplast chain ends at NADP+, and O2 is a by-product of "
             "splitting water at its start."),
           S("As in (가), the electrons in (나) end with less energy than they had at the start.", False,
             "Water's electrons start low and are raised by light at PSII and PSI, ending in NADPH with more energy than "
             "they had in water; only (가) runs downhill throughout."),
           ],
          "O2 is the final acceptor (Module 7) · NADP+ is the final acceptor and the Z scheme (Module 8)",
          ["m7_o2_final_acceptor", "m8_psi_nadph", "m8_z_scheme"], points=2),
    combo(T, "Three glucose polymers on one plate",
          "A plate of bread, oysters and lettuce contains three different glucose polymers. " + READ,
          box("Starch (bread), glycogen (oysters, which store a lot of it) and cellulose (lettuce) are all polymers of "
              "glucose linked by glycosidic bonds.",
              "Humans digest starch and glycogen but not cellulose."),
          [S("Glycogen's many branches let an animal's enzymes free glucose from many chain ends at once when it needs fuel quickly.", True,
             "Enzymes remove glucose units from chain ends, so a highly branched polymer can release glucose quickly, "
             "which suits an animal's fuel store."),
           S("The lettuce's cellulose passes through us undigested because, as a structural polymer, it holds no usable chemical energy.", False,
             "Cellulose's glucose holds as much energy as starch's (cows live on it, thanks to gut microbes that break it "
             "down); we lack enzymes for its linkages, so our own cells can't release its glucose."),
           S("The energy released when starch's glycosidic bonds are hydrolyzed in the gut is what powers the ATP that cells later make from its glucose.", False,
             "Hydrolysis releases little energy; the ATP comes from oxidizing the released glucose in glycolysis, the citric acid cycle and oxidative phosphorylation."),
           ],
          "Polysaccharides, condensation and hydrolysis (Module 2) · Stored glucose fuels respiration (Module 7) · Real-world: glycogen in oysters",
          ["m2_polysaccharides_storage", "m2_condensation_hydrolysis", "m7_glycogen_starch_storage", "m7_glucose_oxidized_o2_reduced"],
          points=3),

    # ---------------------------------------------------------------- matching
    match(T, "Same job, two organelles",
          "Match each part of respiration to its counterpart in photosynthesis.",
          "In respiration", "In photosynthesis",
          [("Coenzyme Q, which carries electrons within the membrane", "Plastoquinone"),
           ("Cytochrome c, a small carrier in the intermembrane space", "Plastocyanin"),
           ("Complex III, which passes electrons on and moves H+", "Cytochrome b6f complex"),
           ("O2, the chain's final electron acceptor", "NADP+"),
           ("The citric acid cycle, a carbon pathway in the matrix", "The Calvin cycle"),
           ("Glucose, the original electron donor", "Water")],
          "The two chains are built alike: a quinone carries electrons within the membrane to a cytochrome complex that "
          "moves H+, and a small carrier on the high-H+ side takes them on. Electrons run from glucose (via NADH) to O2 in "
          "one, and from water to NADP+ in the other, and a carbon cycle runs beside each.",
          "Mitochondrial and chloroplast chains compared (Modules 7, 8)",
          ["m7_etc_location_components", "m8_carriers_pq_pc", "m7_o2_final_acceptor", "m8_psi_nadph"], points=3),
    match(T, "Nucleotides at work",
          "Match each molecule to its job in energy metabolism.",
          "Molecule", "Job",
          [("ATP", "Spent by hexokinase and phosphofructokinase in glycolysis's first phase"),
           ("NAD+", "Regenerated from NADH by fermentation so glycolysis can continue"),
           ("FAD", "Accepts electrons in the citric acid cycle and delivers them at complex II"),
           ("NADP+", "Accepts electrons at the end of the light reactions"),
           ("Coenzyme A", "Carries acetyl groups into the citric acid cycle")],
          "ATP is the energy currency; NAD+, FAD and NADP+ are electron carriers; and coenzyme A carries acetyl groups. "
          "All five are built on a nucleotide.",
          "ATP (Module 6) · Electron carriers and fermentation (Module 7) · NADP+ (Module 8)",
          ["m6_atp_currency", "m7_glycolysis_phase1", "m7_fermentation_purpose", "m7_carriers_nad_fad", "m8_psi_nadph"], points=3),
    match(T, "Energy changes form",
          "Match each process to the energy conversion it carries out.", "Process", "Energy conversion",
          [("Light absorption by a photosystem", "Light energy → energy of an excited electron"),
           ("Mitochondrial electron transport chain", "Energy of electron transfer → potential energy of an H+ gradient"),
           ("ATP synthase", "Potential energy of an H+ gradient → chemical energy of ATP"),
           ("Na+/glucose symporter", "Potential energy of a Na+ gradient → potential energy of a glucose gradient"),
           ("Calvin cycle", "Chemical energy of ATP and NADPH → chemical energy of sugar")],
          "Each process converts energy from one form to another; none creates energy, and each loses some as heat.",
          "Forms of energy (Module 6) · Secondary active transport (Module 3) · Chemiosmosis (Module 7) · Light capture and the Calvin cycle (Module 8)",
          ["m6_potential_kinetic", "m8_photon_excitation", "m7_chemiosmotic_coupling", "m3_secondary_active_transport",
           "m8_calvin_overview"], points=3),

    # ---------------------------------------------------------------- true/false
    tf(T, "Per gram, oxidizing starch makes more of this water than oxidizing fat, since starch's many OH groups already "
          "hold hydrogen bonded to oxygen.", False,
       "Water forms when O2 accepts electrons and H+ at the end of the ETC; fat is richer in hydrogen, so 1 g of fat yields "
       "about 1.1 g of water against about 0.6 g from starch.",
       "Lipid structure (Module 2) · O2 is reduced to water (Module 7) · Real-world: kangaroo rats",
       ["m2_lipid_structure", "m7_o2_final_acceptor"], points=2,
       box="Desert kangaroo rats rarely drink; most of their water is made by their own metabolism as they oxidize the food they eat."),
    tf(T, "In the mitochondrion, H+ passing through ATP synthase moves from a compartment with about 6 times the H+ "
          "concentration into the one with less.", True,
       "ATP synthase lets H+ flow from the intermembrane space (pH about 7.0) into the matrix (about 7.8); a difference of "
       "0.8 pH units is 10^0.8, about 6 times the H+ concentration.",
       "pH (Module 2) · The mitochondrial H+ gradient and ATP synthase (Module 7)",
       ["m2_ph_hydrogen_ions", "m7_proton_gradient", "m7_atp_synthase"], points=2,
       box="The diagram shows typical pH values in a respiring mitochondrion and in a chloroplast in bright light.",
       diagram="br_ph_map"),
    tf(T, "This fits linezolid also blocking mitochondrial ribosomes: with fewer electron transport proteins made, cells "
          "regenerate more of their NAD+ by reducing pyruvate to lactate.", True,
       "Mitochondria keep bacteria-like ribosomes that make some ETC subunits. With less electron transport, NADH can't "
       "unload its electrons there, so cells reduce pyruvate to lactate to regenerate NAD+ for glycolysis.",
       "Mitochondrial ribosomes (Module 5) · Fermentation regenerates NAD+ (Module 7) · Real-world: linezolid",
       ["m5_translation_ribosomes", "m7_fermentation_purpose", "m7_lactic_acid_fermentation"], points=2,
       box="Linezolid, an antibiotic that blocks bacterial ribosomes, can cause lactic acidosis (lactate building up in the blood) when taken for many weeks."),
    tf(T, "The faulty subunits are made on ribosomes inside the mitochondria, and the affected cells can still make some "
          "ATP from FADH2, whose electrons enter the chain after complex I.", True,
       "Genes in mitochondrial DNA are transcribed and translated inside the mitochondrion. FADH2 hands its electrons to "
       "complex II, so they bypass the faulty complex I, though NADH's electrons can't.",
       "Mitochondrial DNA (Module 4) · Mitochondrial ribosomes (Module 5) · ETC entry points (Module 7) · Real-world: LHON",
       ["m4_mtdna_genome", "m5_translation_ribosomes", "m7_fadh2_enters_complex_ii"], points=2,
       box="Leber hereditary optic neuropathy (LHON) is caused by mutations in mitochondrial DNA genes for subunits of complex I; "
           "it mainly damages the energy-hungry nerve cells of the eye."),
    tf(T, "If a mutation removed the small subunit's targeting signal, small subunits would stay in the cytosol and carbon "
          "fixation in the stroma would fall.", True,
       "Small subunits are made on cytosolic ribosomes and imported using their targeting signal; without it they can't "
       "reach the stroma to join the large subunits, so less working rubisco forms.",
       "Protein targeting (Module 5) · The Calvin cycle runs in the stroma (Module 8)",
       ["m5_protein_targeting", "m8_stage_locations"], points=2,
       box="In plants, rubisco is built from large subunits encoded in chloroplast DNA and small subunits encoded in the "
           "nucleus. The diagram shows a chloroplast.", diagram="m8_chloroplast"),
    tf(T, "Their photosystems sit in their plasma membrane, since a prokaryote has no membranes inside the cell.", False,
       "Cyanobacteria have internal thylakoid membranes, not enclosed in any organelle, that hold the photosystems and the "
       "H+ gradient; chloroplasts inherited this arrangement.",
       "Prokaryote structure (Module 1) · Thylakoids hold the light reactions (Module 8)",
       ["m1_prokaryote_no_organelles", "m8_stage_locations"], points=2,
       box="Cyanobacteria carry out photosynthesis that releases O2, though like other prokaryotes they have no chloroplasts."),
    tf(T, "This suits cytochrome c to shuttling electrons between complexes III and IV, while chlorophyll's ring is suited to absorbing light.", True,
       "An iron ion can switch between Fe3+ and Fe2+, so cytochrome c can accept and pass on one electron at a time; "
       "chlorophyll's Mg-containing ring is tuned to capture photons.",
       "Chlorophyll structure (Module 8) · ETC components (Module 7)",
       ["m8_chlorophyll_structure", "m7_etc_location_components"], points=1,
       box="Chlorophyll's porphyrin ring holds a magnesium ion; the similar heme ring in cytochrome c holds an iron ion."),
    tf(T, "This lets the cell slow glycolysis when ATP, which the pathway produces, is already plentiful.", True,
       "ATP binding at an allosteric site lowers PFK's activity. PFK isn't step 1, but its step commits sugar to "
       "glycolysis, so it acts as the pathway's control point and fuel isn't broken down when ATP is plentiful.",
       "Feedback inhibition of an allosteric enzyme (Module 6) · Glycolysis makes ATP (Module 7)",
       ["m6_feedback_inhibition", "m7_glycolysis_net_yield"], points=1,
       box="Phosphofructokinase (PFK), the enzyme for step 3 of glycolysis, catalyzes the first step committed only to "
           "glycolysis; it is inhibited when ATP binds a site away from its active site."),
    tf(T, "Respiration captures more than 90% of glucose's free energy as ATP, losing less than a tenth as heat.", False,
       "Respiration makes about 32 ATP per glucose: 32 × 7.3 ≈ 234 kcal/mol, about a third of 686; the rest is released "
       "as heat, as the second law predicts.",
       "Second law (Module 6) · ATP yield (Module 7)", ["m7_atp_yield_total", "m6_second_law"], points=2,
       box="Fully oxidizing glucose releases about 686 kcal/mol; hydrolyzing ATP releases about 7.3 kcal/mol (standard values)."),
    tf(T, "Like the carbon in the foxes, the energy the foxes received can return to the grass and be used again.", False,
       "Respiration releases the foxes' carbon as CO2, which grass can fix again by photosynthesis, but their energy leaves "
       "as heat, which plants can't capture: energy flows through a food chain while matter cycles.",
       "Energy is lost as heat (Module 6) · Exhaled CO2 (Module 7) · Photosynthesis feeds food webs (Module 8)",
       ["m6_second_law", "m7_exhaled_co2", "m8_photosynthesis_definition"], points=2,
       box="The diagram traces energy through a meadow food chain.", diagram="br_food_chain"),
    tf(T, "The grass stores about 1% of the sunlight reaching it, well below the roughly 4% maximum; the rest of the "
          "sunlight isn't destroyed but is reflected, passes through or ends up as heat.", True,
       "10,000 / 1,000,000 = 1%. Real plants store less than the maximum because they burn some sugar in their own "
       "respiration, can't use all the light in strong sun, and are often limited by water, CO2, nutrients or temperature.",
       "Efficiency of photosynthesis (Module 8) · Energy is conserved (Module 6)",
       ["m8_photosynthesis_efficiency", "m6_first_law"], points=2,
       box="The diagram traces energy through a meadow food chain.", diagram="br_food_chain"),
    tf(T, "The boiled seeds stay at room temperature because boiling destroyed the chemical energy stored in their starch and fats.", False,
       "The energy is still there (the boiled seeds would still burn); boiling unfolded the seeds' enzymes, so respiration "
       "can't release it, and without enzymes the fuel barely reacts at room temperature.",
       "Protein folding (Module 2) · Enzymes lower activation energy (Module 6) · Respiration uses stored fuels (Module 7)",
       ["m2_protein_folding_bonds", "m6_enzymes_lower_ea", "m7_respiration_fuels"], points=2,
       box="Germinating seeds in a vacuum flask plugged with cotton wool warm up by several degrees over a day, while boiled, "
           "disinfected seeds in a second flask stay at room temperature."),
    tf(T, "Its glycolysis enzymes must be held in shape by more stabilizing interactions than ours, since each active site depends on a fold held by weak bonds that heat disrupts.", True,
       "Heat breaks the weak bonds that hold a protein's fold, and the active site with it; enzymes from heat-loving microbes "
       "have extra stabilizing interactions.",
       "Protein folding (Module 2) · Active site (Module 6) · Real-world: Thermus aquaticus",
       ["m2_protein_folding_bonds", "m6_active_site"], points=2,
       box="Thermus aquaticus, a bacterium from hot springs, grows best at about 70 °C, a temperature that unfolds most human enzymes."),
    tf(T, "Most of the energy a fat supplies comes from its glycerol, since glycerol enters respiration through glycolysis.", False,
       "Each fat holds three long fatty acid chains rich in C-H bonds, which beta-oxidation turns into many acetyl-CoA; "
       "the single three-carbon glycerol supplies only a small share.",
       "Lipid structure (Module 2) · Fats as fuel (Module 7)",
       ["m2_lipid_structure", "m7_lipids_energy_rich", "m7_beta_oxidation"], points=1,
       box="Lipases in fat cells break stored fats down by hydrolyzing the bonds that join each fatty acid to glycerol."),
    tf(T, "A plant cell respiring its own sugar at night is acting as a heterotroph.", False,
       "Autotroph and heterotroph describe where an organism gets its carbon. The plant made that sugar from CO2, so "
       "respiring it doesn't make the plant a heterotroph, even though it releases energy the same way the deer does.",
       "Autotrophs and heterotrophs (Module 6) · Respiration of stored fuel (Module 7)",
       ["m6_autotroph_heterotroph", "m7_respiration_fuels"], points=1,
       box="Plants are autotrophs; the deer that eat them are heterotrophs."),
    tf(T, "Some of the 14C will end up built into the caterpillar's own body rather than breathed out as 14CO2.", True,
       "The caterpillar respires part of the leaf's sugar, releasing its carbon as CO2, but it uses other parts to build "
       "its own molecules as it grows (anabolism).",
       "Anabolism and catabolism (Module 6) · Respiration (Module 7) · Carbon fixation (Module 8)",
       ["m6_anabolism_catabolism", "m7_respiration_fuels", "m8_photosynthesis_definition"], points=1,
       box="A bean plant is given 14CO2 for an hour in the light; the next day a caterpillar eats one of its leaves."),
    tf(T, "The leaf's Calvin cycle keeps running, while the H+ gradient across its mitochondria's inner membrane builds up.", True,
       "Chloroplast ATP synthase still makes ATP in the stroma for carbon fixation. In the mitochondria, H+ can no longer "
       "flow back through Fo, so the gradient builds up (and electron transport slows).",
       "Chloroplast ATP stays in the chloroplast (Module 8) · ATP synthase and the H+ gradient (Module 7)",
       ["m8_chloroplast_atp_stays", "m7_atp_synthase", "m7_proton_gradient"], points=2,
       box="Oligomycin blocks the Fo channel of mitochondrial ATP synthase but not of the chloroplast's. A treated leaf is "
           "kept in bright light."),

    # ---------------------------------------------------------------- multiple choice
    mc(T, "Which of these molecules is NOT built on a nucleotide (base + sugar + phosphate), as the NAD+ in the diagram is?",
       "RuBP", ["Coenzyme A", "FAD", "GTP", "NADP+"],
       "Coenzyme A, FAD, GTP and NADP+ each contain a nucleotide; RuBP (ribulose 1,5-bisphosphate), the Calvin cycle's CO2 "
       "acceptor, is a five-carbon sugar with two phosphates but no base.",
       "Nucleotide structure (Module 2) · RuBP (Module 8)", ["m2_nucleotide_structure", "m8_carboxylation_rubisco"],
       points=1, diagram="br_nad_structure"),
    mc(T, "Pyruvate kinase catalyzes step 10 of glycolysis. People who inherit two faulty copies of the gene for the "
          "pyruvate kinase made in red blood cells and liver mainly suffer anemia, because their red blood cells break "
          "down early. Why are their muscle and brain cells largely unaffected?",
       "Those cells make their pyruvate kinase from a different gene",
       ["Their mitochondria make pyruvate from glucose without glycolysis",
        "Those cells get step 10's ATP from steps 1 and 3 instead",
        "Those cells make all their ATP in mitochondria and don't need glycolysis",
        "Those cells make no ATP at step 10, so losing the enzyme changes nothing"],
       "The faulty gene makes only the red-cell and liver form of the enzyme; other tissues make pyruvate kinase from a "
       "separate gene, so their glycolysis is normal. Mature red blood cells, with no mitochondria, rely on glycolysis "
       "alone, so they are hit hardest.",
       "Genes and enzymes (Module 5) · Glycolysis payoff phase (Module 7) · Real-world: pyruvate kinase deficiency",
       ["m5_gene_mutation_protein", "m7_glycolysis_phase3", "m7_stage_locations"], points=2),
    mc(T, "Taking electrons from water, as photosystem II does, needs far more energy than taking them from the C-H bonds "
          "of glucose. Which fact best explains why?",
       "Oxygen is highly electronegative, so water holds its electrons tightly",
       ["Water has fewer electrons than glucose, so each one is harder to find",
        "Water's electrons sit at a higher energy level than glucose's do",
        "Water must first be split into H2 and O2 gases before its electrons can be used",
        "Glucose's electrons are held in bonds to oxygen, which give them up easily"],
       "Oxygen's pull holds the shared electrons of O-H bonds close, so they sit low in energy; electrons shared nearly "
       "equally in C-H bonds sit higher. Light energy at PSII pulls them away from water.",
       "Electronegativity (Module 2) · PSII takes electrons from water (Module 8)",
       ["m2_electronegativity_redox", "m8_psii_water"], points=2),
    mc(T, "The body builds both FAD and FMN, a cofactor inside complex I, from riboflavin (vitamin B2). Using the diagram, "
          "in severe riboflavin deficiency, which entries of electrons into the mitochondrial chain would be weakened?",
       "Entry at both complex I and complex II",
       ["Entry at complex I only",
        "Entry at complex II only",
        "Neither, since riboflavin isn't part of a nucleotide",
        "Neither, since electrons enter the chain only from NADH"],
       "NADH's electrons go first to the FMN in complex I, and FADH2 from the citric acid cycle hands its electrons in at "
       "complex II, so with less riboflavin both entries weaken. FMN is riboflavin with a phosphate, and FAD adds an "
       "adenine nucleotide.",
       "Nucleotide carriers (Module 2) · FADH2 enters at complex II (Module 7)",
       ["m2_nucleotide_structure", "m7_fadh2_enters_complex_ii", "m7_carriers_nad_fad"], points=2,
       diagram="m7_etc_membrane"),
    mc(T, "Using the diagram, a carbon atom is fixed from 14CO2 in a leaf cell and later released as 14CO2 by the same "
          "cell's respiration. Which route does it most likely take?",
       "Stroma (F), then the cytosol, then the matrix (4)",
       ["Matrix (4), then the cytosol, then the stroma (F)",
        "Thylakoid lumen (D), then the intermembrane space (2)",
        "Stroma (F), then straight into the matrix (4) without entering the cytosol",
        "Stroma (F) only, since the Calvin cycle releases CO2 as well as fixing it"],
       "Rubisco fixes the carbon in the stroma; sugar made from it goes to the cytosol, where glycolysis makes pyruvate, "
       "which enters the matrix, where pyruvate oxidation and the citric acid cycle release the carbon as CO2.",
       "The Calvin cycle runs in the stroma (Module 8) · Glycolysis in the cytosol, CO2 released in the matrix (Module 7)",
       ["m8_stage_locations", "m7_stage_locations", "m7_exhaled_co2"], points=2, diagram="mito_chloro_compartments"),
    mc(T, "How is ATP synthase like the Na+/glucose symporter that intestinal cells use to absorb glucose?",
       "Both are driven by an ion flowing down its gradient",
       ["Both hydrolyze ATP to move ions against a gradient",
        "Both use the energy of electron transport directly",
        "Both carry two different solutes across together",
        "Both move every solute they carry down its gradient"],
       "The symporter uses Na+ flowing in to move glucose uphill; ATP synthase uses H+ flowing down its gradient to make "
       "ATP. The symporter never hydrolyzes ATP, and ATP synthase normally makes ATP rather than spending it.",
       "Secondary active transport (Module 3) · ATP synthase and chemiosmosis (Module 7)",
       ["m3_secondary_active_transport", "m7_atp_synthase", "m7_chemiosmotic_coupling"], points=2),
    mc(T, "Water takes part in many reactions in Modules 6-8. In which process is water a product rather than a reactant?",
       "Electron transport at complex IV",
       ["ATP powering the Na+/K+ pump",
        "Photosystem II replacing its lost electrons",
        "Digestion of starch into glucose",
        "Breaking a fat into glycerol and fatty acids"],
       "At complex IV, O2 accepts electrons and H+ and becomes water; the other processes all use water up (ATP, starch and "
       "fat are hydrolyzed, and PSII takes its electrons from water).",
       "Hydrolysis (Module 2) · O2 is reduced to water (Module 7) · Water is split at PSII (Module 8)",
       ["m2_condensation_hydrolysis", "m7_o2_final_acceptor", "m8_psii_water"], points=1),
    mc(T, "Why must the inner mitochondrial membrane be almost impermeable to H+?",
       "So H+ flows back through ATP synthase instead of leaking across",
       ["So the matrix becomes the high-H+ side of the membrane",
        "So H+ can't reach complex IV to form water",
        "So the gradient's energy is released as heat",
        "So the gradient forms without any energy input"],
       "A gradient stores energy only if H+ can't leak back across the bilayer; then H+ returns mostly through ATP synthase, "
       "which captures the energy as ATP. (A little leaks back anyway, and DNP or UCP1 makes the leak much bigger.)",
       "Membrane permeability (Module 3) · Proton gradient and chemiosmosis (Module 7)",
       ["m3_membrane_permeability", "m7_proton_gradient", "m7_chemiosmotic_coupling"], points=1),
    mc(T, "Both a cyanobacterium and a plant leaf cell carry out photosynthesis and cellular respiration. Which of these is "
          "found in the leaf cell but not in the cyanobacterium?",
       "Mitochondria", ["Ribosomes", "Chlorophyll a", "A respiratory electron transport chain", "Photosystem II"],
       "Cyanobacteria have ribosomes, chlorophyll a, photosystem II and a respiratory electron transport chain in their own "
       "membranes, but no membrane-bound organelles such as mitochondria.",
       "Prokaryotes lack organelles (Module 1) · The respiratory chain (Module 7)",
       ["m1_prokaryote_no_organelles", "m7_etc_location_components"], points=1),
    mc(T, "Which of these reductions uses electrons that came from water?",
       "NADP+ → NADPH at the end of the light reactions",
       ["NAD+ → NADH in glycolysis",
        "FAD → FADH2 in the citric acid cycle",
        "O2 → H2O at complex IV",
        "NAD+ → NADH in pyruvate oxidation"],
       "The light reactions take electrons from water at photosystem II and deliver them to NADP+; the other reductions use "
       "electrons taken from fuel molecules, and the water made at complex IV is a product, not the source.",
       "Electron carriers (Module 7) · Water splitting and NADPH (Module 8)",
       ["m7_carriers_nad_fad", "m8_psii_water", "m8_psi_nadph"], points=1),
    mc(T, "Earth's air held almost no O2 until about 2.4 billion years ago, after cyanobacteria became widespread. Which "
          "statement best links that event to the O2 a maple tree releases today?",
       "Its chloroplasts descend from cyanobacteria and split water the same way",
       ["Its mitochondria descend from cyanobacteria and release the O2 instead",
        "It splits CO2 to release O2, a process that cyanobacteria never used",
        "Its O2 is released when its cells break down glucose in respiration",
        "Living cyanobacteria inside every leaf cell still release the O2"],
       "Chloroplasts arose from engulfed cyanobacteria and kept their water-splitting photosystems, so plant O2 comes from "
       "water, as cyanobacterial O2 does. Mitochondria came from proteobacteria and use O2 rather than release it.",
       "Endosymbiosis (Modules 1, 3) · Water is the electron donor (Module 8)",
       ["m1_endosymbiosis", "m8_water_electron_donor"], points=2),
    mc(T, "The citric acid cycle needs only a little oxaloacetate to process a great deal of acetyl-CoA. Which Module 6 idea is "
          "the closest parallel?",
       "An enzyme is released unchanged and used again",
       ["A catalyst lowers the activation energy barrier",
        "A pathway's end product shuts off its first enzyme",
        "ATP hydrolysis drives endergonic reactions forward",
        "A competitive inhibitor occupies the active site"],
       "Oxaloacetate is regenerated at the end of each turn, just as an enzyme is regenerated after each E + S → E + P cycle, "
       "so a small amount of either can process many molecules.",
       "Enzymes are reused (Module 6) · Oxaloacetate is regenerated (Module 7)",
       ["m6_enzyme_cycle", "m7_cac_cycle_regenerates"], points=2),
])
