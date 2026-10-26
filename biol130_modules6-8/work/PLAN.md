# Plan: BIOL 130 Modules 6–8 flashcards

Target: about 225 cards. Module 6: 5 case studies + 4 gap cards. Module 7: 100. Module 8: 75. Bridge: 40.
All slugs are in `work/concept_ledger_m68.json`.

## 1. Topics and format counts

### Module 6 (case studies + gaps) — 9 cards

| Topic | Concepts | 보기 (case) | Match | T/F | MC |
|---|---|---|---|---|---|
| Energy & Metabolism | metabolic_pathways_linked, anabolism_catabolism, first_law | 1 (1) PKU | – | 1 (calorimeter vs body: first law) | – |
| ATP & Energetic Coupling | atp_hydrolysis_exergonic, energetic_coupling, delta_g_sign | 1 (1) creatine | – | – | – |
| Thermodynamics & Free Energy | gibbs_equation, delta_g_sign, activation_energy, second_law | 1 (1) hand warmer | – | – | 1 (refrigerated food: kinetic energy vs Ea) |
| Enzymes & Their Regulation | competitive/noncompetitive, enzyme_cycle, active_site, activators | 2 (2) statins, pineapple + gelatin | – | 1 (activator drug) | 1 (activator logic) |

Gap check against the 46 existing cards: activators (only one matching item) and the first law (no direct card) were thin; the Ea-temperature link had no everyday case.

### Module 7 — 100 cards (20 보기 incl. 5 case, 8 matching, 45 T/F, 27 MC)

| Topic | Concepts | 보기 (case) | Match | T/F | MC |
|---|---|---|---|---|---|
| Overview of Cellular Respiration | respiration_fuels, four_stages_order, stage_locations, substrate_level, oxphos_most_atp, redox_definitions, glucose_oxidized_o2_reduced, carriers_nad_fad, stepwise_energy_release | 3 | 1 | 7 | 4 |
| Glycolysis | glycolysis_overview, glycolysis_no_o2, phase1, phosphorylation_traps_glucose, phase2, phase3, net_yield | 3 (1) FDG-PET | 1 | 8 | 5 |
| Pyruvate Oxidation & Citric Acid Cycle | mito_compartments, pyruvate_oxidation_step, pyruvate_oxidation_totals, cac_cycle_regenerates, cac_completes_oxidation, cac_yield, cac_intermediates_biosynthesis, exhaled_co2 | 4 (1) thiamine deficiency | 2 | 8 | 4 |
| Oxidative Phosphorylation | etc_location_components, o2_final_acceptor, fadh2_enters_complex_ii, proton_pumping, proton_gradient, atp_synthase, chemiosmotic_coupling, atp_yield_total | 4 (1) DNP diet pill | 2 | 10 | 6 |
| Anaerobic Conditions & Fermentation | fermentation_purpose, lactic_acid_fermentation, ethanol_fermentation, fermentation_yield | 3 (1) dough vs sprint | 1 | 6 | 4 |
| Metabolic Integration | glycogen_starch_storage, liver_vs_muscle_glycogen, other_sugars_enter, lipids_energy_rich, beta_oxidation, proteins_as_fuel | 3 (1) keto diet | 1 | 6 | 4 |

### Module 8 — 75 cards (15 보기 incl. 5 case, 6 matching, 33 T/F, 21 MC)

| Topic | Concepts | 보기 (case) | Match | T/F | MC |
|---|---|---|---|---|---|
| Overview of Photosynthesis | photosynthesis_definition, efficiency, light_limits_habitat, photosynthesis_redox, water_electron_donor, two_stages_linked, chloroplast_structure, stage_locations, overall_equation | 4 (1) 18O water experiment | 1 | 9 | 5 |
| Pigments & Light Absorption | photon_excitation, excited_state_fates, spectrum_wavelength_energy, chlorophyll_absorption, chlorophyll_structure, accessory_pigments, antenna_transfer | 3 (1) LED grow lights | 2 | 8 | 5 |
| Photosystems & Electron Transport | reaction_center, two_photosystems_series, psii_water, psi_nadph, z_scheme, carriers_pq_pc, thylakoid_proton_gradient, photophosphorylation, chloroplast_atp_stays, cyclic_electron_transport | 4 (1) PSII herbicide | 2 | 9 | 6 |
| Calvin Cycle | calvin_overview, carboxylation_rubisco, reduction_step, regeneration_rubp, calvin_stoichiometry, starch_for_night | 4 (2) greenhouse CO2, Calvin's 14C algae | 1 | 7 | 5 |

### Bridge — 40 cards (8 보기, 3 matching, 17 T/F, 12 MC), topic "Connecting Modules 1–8"

At least 24 of 40 tie Modules 6–8 to Modules 1–5. Planned links:
- redox and electronegativity (M2) · NAD+/FAD as nucleotides, vitamins niacin/riboflavin (M2)
- H+ gradients and pH in mitochondria vs thylakoids, pumps (M2 pH, M3 transport)
- endosymbiosis, bacterial plasma-membrane ETC, cyanobacterial thylakoids (M1, M3)
- mitochondrial DNA and ribosomes: LHON, linezolid lactic acidosis; rubisco's chloroplast-encoded large subunit (M4, M5)
- glycogen/starch/cellulose and fats as fuels; hydrolysis; metabolic water in kangaroo rats (M2)
- GLUT + hexokinase trapping keeping the gradient (M3 + M7); ATP synthase reversing as a pump (M3 + M6 + M7)
- enzymes as proteins: PFK allosteric control, rubisco's slowness (M6 + M7/M8, M2)
- photosynthesis vs respiration comparisons; isotope tracing of C and O atoms between them (M6–8)
- energy flow through a food chain: thermodynamics + 4% efficiency (M6 + M8)

## 2. Case studies (15)

Truth marks: T = true, F = false. Each has a trap, an explanation and a what-if; (가) and (나) each feed a statement.

**Module 6**
1. *Reusable hand warmer* (Thermodynamics). (가) Clicking a metal disc in a supersaturated sodium acetate pack starts crystallization, and the pack heats to about 54 °C. (나) Boiling the pack re-dissolves the crystals so it can be reused. Trap: the click supplies the energy that makes ΔG negative (F). Explanation: crystallizing lowers entropy yet is spontaneous because enough heat is released (ΔH negative enough) (T). What-if: resetting by boiling is endergonic, paid for by the stove's heat (T).
2. *Creatine supplements* (ATP & coupling). (가) Muscle stores phosphocreatine, which hands its phosphate to ADP in the first seconds of a sprint. (나) ΔG of hydrolysis: phosphocreatine −10.3, ATP −7.3, glucose 6-phosphate −3.3 kcal/mol. Trap: creatine is itself oxidized for energy (F). Explanation: PCr + ADP → Cr + ATP has ΔG = −3.0 (T). What-if: glucose 6-phosphate cannot remake ATP by the same direct transfer (+4.0) (T).
3. *PKU and diet-soda labels* (Energy & Metabolism). (가) In PKU, phenylalanine hydroxylase (Phe → Tyr) is missing. (나) Aspartame-sweetened drinks carry the warning "Phenylketonurics: contains phenylalanine". Trap: patients must cut tyrosine too (F). Explanation: Phe builds up and is diverted to phenylpyruvate (T). What-if: products downstream of tyrosine such as melanin fall unless tyrosine is supplied (T).
4. *Statins* (Enzymes). Rate-vs-[HMG-CoA] curves with no drug, a statin, and compound N. (가) statins resemble HMG-CoA. (나) compound N binds away from the active site. Trap: the statin binds an allosteric site (F). Explanation: at high substrate the statin curve approaches the no-drug maximum (T). What-if: raising HMG-CoA would restore compound N's curve too (F).
5. *Fresh pineapple ruins gelatin* (Enzymes). Four-tube results table. (가) bromelain is a protease. (나) canned (heated) pineapple lets gelatin set. Trap: heating changed the hydrolysis ΔG (F). Explanation: heat unfolded bromelain's active site (T). What-if: a small amount of enzyme suffices because it is not used up (T).

**Module 7**
6. *FDG-PET scans* (Glycolysis). FDG enters through GLUT, hexokinase phosphorylates it, and the product can't continue. (가) FDG is glucose with F replacing the 2-OH. (나) tumours light up more than most tissue. Trap: FDG accumulates because GLUT can't carry it back out unphosphorylated (F, the phosphate charge traps it). Explanation (T). What-if: a hexokinase inhibitor would reduce the signal (T).
7. *Thiamine deficiency in heavy drinkers* (Pyruvate oxidation). (가) thiamine forms a cofactor of the pyruvate dehydrogenase complex. (나) blood lactate rises. Trap: CO2 output from glycolysis falls (F, glycolysis makes no CO2). Explanation: pyruvate backs up and is reduced to lactate (T). What-if: fatty acids could still feed acetyl-CoA into the cycle (T).
8. *DNP "diet pill"* (Oxidative phosphorylation). Bar chart: O2 use, ATP made, heat, control vs DNP (illustrative). (가) DNP carries H+ across the inner membrane. (나) patients overheat. Trap: DNP blocks the ETC (F; O2 use rises). Explanation: H+ return without ATP synthase, energy lost as heat (T). What-if: brown fat's UCP1 does the same on purpose (T).
9. *Bread dough vs sprinting muscle* (Fermentation). Measured products panel. (가) dough rises. (나) muscle lactate rises. Trap: both make CO2 (F). Explanation: both regenerate NAD+ (T). What-if: if yeast had O2, it would release more CO2 per glucose (T).
10. *Keto diet* (Metabolic integration). Fuel-entry map. (가) carbs < 50 g/day. (나) liver makes ketone bodies from acetyl-CoA. Trap: fats yield ATP directly in beta-oxidation (F). Explanation: fatty acids → acetyl-CoA, NADH, FADH2 (T). What-if: glycerol from fat can feed glycolysis (T).

**Module 8**
11. *Where does the O2 come from? (18O)* (Overview). Two-experiment table (illustrative values). Trap: O2 comes from CO2 (F). Explanation: water is oxidized (T). What-if: the label in CO2 appears in sugar (T).
12. *Red and blue LED grow lights* (Pigments). Absorption spectra + LED bands. Trap: green LEDs would work equally well because all visible photons have energy (F). Explanation: blue and red sit near chlorophyll's peaks (T). What-if: carotenoid absorption extends usefulness into blue-green (T).
13. *PSII herbicides (atrazine, diuron)* (Photosystems). Herbicide binding site between PSII and plastoquinone. Trap: plants starve because they can't absorb light (F). Explanation: NADPH and ATP production stop (T). What-if: PSI-driven cyclic flow could still make some ATP (T).
14. *Greenhouse CO2 enrichment* (Calvin). Rate vs CO2 at two light levels. Trap: enrichment raises rate by supplying more NADPH (F). Explanation: more CO2 for rubisco carboxylation at high light (T). What-if: at low light extra CO2 helps little (T).
15. *Calvin's 14C algae* (Calvin). Label-vs-time graph. Trap: the first labelled product is a six-carbon sugar (F). Explanation: CO2 + RuBP → 2 PGA (T). What-if: switch off the light → PGA rises, RuBP falls (T).

(Builder balances patterns; I will turn some T into F during writing to hit 1-true / 2-true / 3-true mix.)

## 3. Diagrams

| Key | Title | Draw | Must not show | Cards |
|---|---|---|---|---|
| m6_handwarmer_profile | Free energy of a hand-warmer pack | G vs progress: supersaturated solution, barrier, crystals | ΔG sign words, "spontaneous" | case 1 |
| m6_phosphate_ladder | Free energy of phosphate hydrolysis | three bars: PCr, ATP, G6P (−10.3, −7.3, −3.3) | coupled ΔG results | case 2 |
| m6_pku_pathway | Phenylalanine's pathways | Phe → Tyr → melanin/dopamine; side branch to phenylpyruvate | which branch fills, "blocked" | case 3 |
| m6_statin_curves | Enzyme rate vs substrate, three conditions | three saturation curves | inhibitor type labels | case 4 |
| m6_gelatin_tubes | Four gelatin tubes after 4 h | tubes with additions and set/liquid results | the reason | case 5 |
| m7_cell_compartments | Compartments of a cell's energy machinery | cell membrane, cytosol, mitochondrion with outer/inner membranes, IMS, matrix | stage names | overview/location cards |
| m7_glycolysis_map | Glycolysis, step by step | 10 numbered steps with intermediates, carbons, ATP/NADH marks | net totals, phase verdicts | glycolysis cards, fluoride |
| m7_fdg_cell | Glucose and FDG at a cell | GLUT, hexokinase, glucose vs FDG structure | "trapped" | case 6 |
| m7_pyruvate_fates | Where pyruvate can go | cytosol vs matrix, PDH (thiamine cofactor), lactate branch | which route rises | case 7, cards |
| m7_cac_cycle | The citric acid cycle | eight intermediates with carbon counts, acetyl-CoA entry | CO2 steps (left for carbon counting) | CAC cards |
| m7_etc_membrane | The inner mitochondrial membrane | complexes I–IV, Q, cyt c, ATP synthase, NADH/FADH2 entry, O2 | H+ arrows | ETC/inhibitor cards |
| m7_o2_trace | O2 in a flask of mitochondria | O2 vs time, additions marked | slope verdicts | inhibitor cards |
| m7_dnp_bars | Mitochondria with and without DNP | bars: O2 use, ATP, heat | the explanation | case 8 |
| m7_yield_table | Per-glucose products by stage | table of ATP/NADH/FADH2/CO2 by stage | total ATP | yield cards |
| m7_dough_sprint | Two cells without O2 | yeast in dough vs muscle: inputs, measured products | NAD+ loop | case 9 |
| m7_fuel_map | How fuels enter respiration | carbs, fats, proteins into pathway | beta-oxidation ATP | case 10, integration |
| m7_energy_staircase | Glucose's free energy, step by step | stepwise descent glucose → CO2 + H2O, −686 total | "efficient" | overview cards |
| m8_chloroplast | A chloroplast | membranes, thylakoids, granum, lumen, stroma | where reactions occur | overview cards |
| m8_sunlight_budget | Where a leaf's sunlight goes | the notes' percentages | final 4% figure arithmetic | efficiency cards |
| m8_o18_table | Two labelling experiments | 18O % in water, CO2, O2 | conclusion | case 11 |
| m8_absorption_spectra | Absorption of three pigments | chl a, chl b, carotenoid curves 400–700 nm | "green reflected" | pigment cards |
| m8_led_bands | Leaf pigments and three LEDs | chl a + b curves, three LED bands | which LED wins | case 12 |
| m8_chlorophyll | Chlorophyll's two parts | porphyrin ring with Mg, phytol tail | function labels | structure cards |
| m8_photosystem | Inside one photosystem | antenna chlorophylls, reaction-center pair, acceptor, donor | energy vs electron arrows | antenna cards |
| m8_z_scheme | Electron energy along the light reactions | energy levels of H2O, PSII, PQ, b6f, PC, PSI, Fd, NADP+ | blockage effects | Z cards |
| m8_thylakoid_membrane | The thylakoid membrane | PSII, PQ, b6f, PC, PSI, Fd, reductase, ATP synthase, stroma/lumen | H+ arrows | ETC cards |
| m8_herbicide_site | Where PSII herbicides bind | PSII with QB site, herbicide, PQ | consequences | case 13 |
| m8_calvin_cycle | The Calvin cycle | carboxylation/reduction/regeneration, RuBP 5C, PGA 3C, BPG, triose P | molecule counts | Calvin cards |
| m8_co2_curves | Photosynthesis rate vs CO2 | two light levels, ambient and enriched marks | limiting factor labels | case 14 |
| m8_c14_timecourse | Where the 14C label goes | % label in PGA vs sugars vs time | first product label | case 15 |
| br_two_gradients | Two organelles, two H+ gradients | mitochondrion and chloroplast with compartments and pH | where ATP synthase points | bridge gradient cards |
| br_nad_structure | NAD+ as two nucleotides | schematic: adenine–ribose–P–P–ribose–nicotinamide | names of vitamins | bridge nucleotide cards |
| br_food_chain | Energy along a food chain | sun → grass → rabbit with energy values | percentages computed | bridge thermodynamics cards |

Study-page diagrams reused where they fit (none planned yet).

## 4. Duplicate checks done

Grepped `ref/existing_cards_index.txt`: no existing card mentions NADH, FADH, rubisco, Calvin, photosystem, proton gradient, statins, creatine, PKU, hand warmers, DNP, thiamine, fluoride, herbicides, greenhouse CO2, 18O, LEDs (as lights), keto, oligomycin or beta-oxidation. Avoided: autumn leaves (#1314), cyanide (#1234), red blood cells without mitochondria (#1221), lactose/lactase (#38), mitochondrial protein import (#2106, #2024), chlorophyll fluorescence (#2245), the sprinter's ATP (#2236).
