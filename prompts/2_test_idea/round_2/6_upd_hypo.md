# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_7KogxZ5PgvFN` — Measuring Molecular Property Expressiveness Ceilings via 1-WL Color Refinement
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-24 21:13:25 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: 1-WL Refinement Floors Diagnose Molecular Property Predictability
hypothesis: >-
  For each molecular property in a benchmark dataset, the r-round 1-WL conditional variance floor — the fraction of total
  property variance unresolved within WL equivalence classes after r rounds of standard color refinement — defines a measurable
  expressiveness ceiling for any message-passing GNN operating on 2D molecular topology. Crucially, this floor is NOT equivalent
  to the floor for k-dimensional WL GNNs (k-WL as in Maron et al. 2019): r rounds of 1-WL converge to the same stable partition
  for small molecular graphs, so increasing r beyond convergence adds no new expressiveness and does not correspond to 2-WL
  or 3-WL architectural capability. Within this corrected framing, the variance floor after 1-WL convergence decomposes the
  property space along two orthogonal dimensions — (floor magnitude) × (floor collapse rate from r=1 to convergence) — creating
  a testable 2×2 typology: (1) 'topology-bottlenecked' properties (high r=1 collision rate, near-zero converged floor) where
  the variance is recoverable by any architecture that refines 2D topology beyond 1-WL message-passing; (2) '3D-geometry-limited'
  properties (high r=1 collision rate, persistently high converged floor) where variation within WL equivalence classes is
  attributable to 3D conformation unresolvable by any 2D graph descriptor; (3) 'topology-sufficient' properties (near-zero
  r=1 collision rate) where 1-WL message-passing already near-optimally distinguishes all relevant pairs; and (4) 'noise-dominated'
  properties. Empirical measurements on 63,007 molecules across 24 properties (QM9 + MoleculeNet) confirm: QM9 thermochemical
  energies (u0, h298, g298) are topology-sufficient (collision rate ≈0, floor ≈0); QM9 electronic properties (HOMO, LUMO,
  dipole moment, gap) show high r=1 collision rates (7–27%) with persistently non-zero converged floors (0.03–1.7% of total
  variance), classifying them as geometry-limited; FreeSolv solvation and HIV activity show high r=1 collision but near-zero
  converged floors, classifying them as topology-bottlenecked. ESOL solubility exhibits an important nuance: collisions resolve
  completely at r=2 (not persistent), yet retains an above-median converged floor, indicating measurement noise rather than
  true geometry-limitation. The typology further predicts: geometry-limited properties (HOMO, dipole moment) should benefit
  from 3D architectures (SchNet, DimeNet) but not from higher-order 2D GNNs; topology-bottlenecked properties (FreeSolv, HIV)
  should benefit from architectures more expressive than 1-WL message-passing (e.g., graph transformers, subgraph GNNs, structural
  encodings). These predictions remain to be validated by controlled GNN training experiments comparing 1-WL GIN vs. higher-expressiveness
  architectures on properties from each quadrant. Threshold assignment should use principled criteria (e.g., permutation-null
  baselines or variance-floor >1% physically motivated cutoffs) rather than median-based splits, which by construction guarantee
  balanced quadrant occupancy regardless of true distributional structure.
motivation: >-
  The WL hierarchy is the dominant theoretical lens for measuring GNN expressiveness, yet it is almost exclusively used qualitatively
  ('higher-order GNNs are more expressive') rather than quantitatively ('this specific property needs exactly k=2 WL iterations').
  Practitioners who want to improve molecular property prediction face a difficult choice: invest in computationally expensive
  higher-order GNNs, or integrate 3D geometric information. Currently, this choice is made heuristically or by trial-and-error
  across benchmarks. A systematic diagnostic that measures the per-property WL expressiveness floor would change this from
  guesswork to principled engineering. Furthermore, the field lacks clarity on why some benchmark improvements from higher-order
  GNNs are large while others are negligible — the proposed typology directly explains this variance and would guide where
  future architectural innovation should focus.
assumptions:
- >-
  WL certificates can be computed exactly for drug-like molecules (bounded size, finite atom types) using the canonical WL
  color-refinement algorithm in polynomial time.
- >-
  The distinction between 'WL-bottlenecked' and '3D-geometry-limited' is testable because 3D-geometry-limited properties will
  show high within-class conditional variance even at high WL levels, while WL-bottlenecked properties show low conditional
  variance (property is nearly constant within a WL class) that becomes zero as k increases.
- >-
  Standard molecular benchmark datasets (QM9, MoleculeNet) contain enough isomers and structurally similar molecules to produce
  measurable WL collision rates.
- >-
  A property's WL expressiveness floor is an upper bound on the best achievable test error for any message-passing GNN trained
  on that property, regardless of depth, width, or training strategy.
investigation_approach: >-
  Step 1: WL certificate computation. Implement the standard k-WL color refinement algorithm (k=1,2,3) for molecules in QM9
  (133K molecules, 19 quantum properties) and MoleculeNet ESOL/HIV/BBBP/Tox21 datasets. Use canonical graph hashing (e.g.,
  Weisfeiler-Lehman graph kernel certificates). Step 2: Collision rate and conditional variance measurement. For each (dataset,
  property, k) triple, compute: (a) the k-WL collision rate — fraction of molecule pairs assigned the same certificate but
  with |Δy| > σ_y/2; (b) the within-class conditional variance Var[y | WL_k(molecule)], which bounds minimum achievable MSE.
  Step 3: Typology assignment. Place each (dataset, property) pair in the 2×2 typology based on normalized collision rate
  and within-class variance. Step 4: GNN training. Train 1-WL (GIN), 2-WL (NGNN or GSN), and 3-WL (I²-GNN or DRFWL) GNNs on
  each property using the same training protocol. Compare achieved test errors to the computed expressiveness floors. Step
  5: Validation. Verify the predicted pattern: 3D-geometry-limited properties (quantum) show no improvement as k increases
  (floor unchanged); WL-bottlenecked properties show improvement correlated with the floor drop. This is fully implementable
  with standard Python libraries (networkx for WL, PyTorch Geometric for GNNs) within the compute budget.
success_criteria: >-
  Confirmation: (a) QM9 quantum properties (ε_HOMO, ε_LUMO, μ) have 1-WL collision rates >10% with high within-class variance
  (>50% of total variance unexplained by 2-WL certificates), and GNN improvement from k=1 to k=3 is <5% relative error reduction.
  (b) At least two MoleculeNet properties have 1-WL collision rates <2%, and 1-WL GINs achieve near-optimal performance on
  them. (c) At least one property shows high collision rate but low within-class variance (WL-bottlenecked), and there is
  a statistically significant improvement (>10% relative) from k=1 to k=2 GNNs. Disconfirmation: if the within-class variance
  does not differentiate quantum from pharmacokinetic properties, or if higher-order GNNs improve equally across all property
  types regardless of collision-rate typology.
related_works:
- >-
  Xu et al. (2019) 'How Powerful are Graph Neural Networks?' establishes that GINs are maximally expressive within 1-WL, but
  does not measure property-specific WL floors or partition properties by typology.
- >-
  Wang and Zhang (2024) 'An Empirical Study of Realized GNN Expressiveness' (BREC benchmark) measures GNN expressiveness on
  synthetic WL-indistinguishable graphs, not on real molecular property datasets or real WL collision distributions.
- >-
  Maron et al. (2019) 'Provably Powerful Graph Networks' and related k-WL GNN papers theoretically establish the hierarchy
  but make no property-specific predictions about which molecular tasks benefit from each level.
- >-
  I²-GNN and DRFWL (2022–2023) papers on cycle-counting GNNs identify benzene 6-cycles as important, but address a specific
  structural feature rather than providing a general per-property diagnostic framework.
- >-
  Klicpera et al. DimeNet and Schütt et al. SchNet show 3D geometry improves quantum property prediction, implicitly suggesting
  these are geometry-limited — but do not provide the WL-floor mechanism or the 2×2 typology connecting expressiveness limits
  to actionable architecture choices.
inspiration: >-
  The core idea is a cross-domain transfer from **measurement theory and ANOVA (Analysis of Variance)**: in statistics, ANOVA
  decomposes total variance into variance explained by a grouping factor vs. residual variance. Here, the WL certificate plays
  the role of the grouping factor, and 'within-class property variance' is the residual unexplainable by any perfect WL predictor.
  The insight that this residual variance is a hard lower bound on prediction error mirrors the information-theoretic concept
  of irreducible entropy. A secondary inspiration from **ecology**: the species occupancy-abundance relationship (common species
  are widespread, rare species are localized) maps onto WL certificate occupancy — if most molecules share common WL certificates,
  the 'within-certificate' diversity determines predictability. This ecological framing prompted looking at how 'information
  is distributed' within equivalence classes, rather than only asking whether classes can be distinguished.
terms:
- term: k-WL certificate
  definition: >-
    A canonical label (hash) assigned to a graph by running k rounds of Weisfeiler-Leman color refinement. Two graphs with
    the same k-WL certificate are indistinguishable by any k-WL-bounded GNN.
- term: WL collision rate
  definition: >-
    The fraction of molecule pairs in a dataset that share the same k-WL certificate but have property values differing by
    more than a threshold (e.g., half the standard deviation of the property).
- term: expressiveness floor
  definition: >-
    The minimum achievable mean squared prediction error for a molecular property when using any k-WL-bounded GNN, equal to
    the conditional variance of the property given the k-WL certificate.
- term: WL-bottlenecked property
  definition: >-
    A molecular property where the 1-WL collision rate is high but within-class variance is low — meaning molecules with the
    same 2D topology but distinguishable at 2-WL have different property values. Such properties strictly benefit from higher-order
    GNNs.
- term: 3D-geometry-limited property
  definition: >-
    A molecular property where WL collision rate is high but within-class variance remains high at all WL levels — meaning
    property variation within WL equivalence classes is due to 3D conformational differences not encodable by any 2D graph
    descriptor.
summary: >-
  We propose measuring a per-property 'WL expressiveness floor' in standard molecular benchmarks — the conditional variance
  of each property within WL equivalence classes — which tells precisely how much GNN performance can improve from higher
  WL orders vs. requiring 3D geometry. This creates a testable 2×2 typology (WL-bottlenecked vs. 3D-geometry-limited vs. WL-sufficient
  vs. noise-dominated) that explains when investing in higher-order GNNs will or will not help, turning a theoretical hierarchy
  into a practical molecular dataset diagnostic.
_relation_rationale: >-
  Same 2×2 typology frame; narrowed to correct 1-WL-rounds framing, dropped false k-WL GNN claims.
_confidence_delta: decreased
_key_changes:
- >-
  CRITICAL CORRECTION: Reframed 'k-WL certificates' as 'r rounds of 1-WL refinement' throughout — the measured floors are
  NOT floors for k-dimensional WL GNNs (Maron et al.), which is a fundamentally different and strictly more powerful test.
- >-
  Removed all predictive claims linking measured r=1,2,3 floors to k-GNN, I²-GNN, or NGNN architectural performance, since
  those architectures implement k-dimensional WL, not iterated 1-WL.
- >-
  Renamed 'WL-bottlenecked' to 'topology-bottlenecked' and 'WL-sufficient' to 'topology-sufficient' to reflect that the floor
  measures 1-WL topology expressiveness, not the full k-WL hierarchy.
- >-
  Added explicit caveat that GNN training validation (GIN vs. higher-expressiveness architectures on bottlenecked vs. geometry-limited
  properties) is a required next step — the typology remains a diagnostic hypothesis, not a validated tool.
- >-
  Noted that ESOL collisions resolve at r=2 (not persistent), correcting the claim that ESOL is 'geometry-limited' due to
  persistent collisions; reclassified as above-median noise floor.
- >-
  Flagged the median-based threshold problem: thresholds derived from the population median guarantee balanced quadrant occupancy
  by construction and should be replaced with permutation-null or physically motivated cutoffs.
- >-
  Acknowledged the counterintuitive collision rate increase at higher r for geometry-limited properties (e.g., HOMO: 0.266→0.391
  from r=1→r=3): the denominator (same-certificate pairs) shrinks as refinement proceeds, making remaining collisions proportionally
  harder — collision rate is therefore a secondary metric; variance floor (monotone) should be primary.
- >-
  Added requirement to report confidence intervals on collision rates, especially for small groups (FreeSolv n=642, 61 same-certificate
  groups at r=1).
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_PA8MCYxkbsL8
type: dataset
title: QM9 and MoleculeNet Molecular Datasets
summary: |-
  Five molecular property benchmark datasets prepared for Weisfeiler-Leman (WL) GNN expressiveness analysis, totalling 102,125 molecules with SMILES strings and labeled properties:

  1. **QM9_Properties** (50,000 molecules, multi-target regression): Quantum-mechanical properties (HOMO energy, LUMO energy, HOMO-LUMO gap, dipole moment, polarizability) from the canonical QM9 dataset (Ramakrishnan et al. 2014, Scientific Data). Source: n0w0f/qm9-csv (HuggingFace, 741 downloads). THE standard GNN expressiveness benchmark used in GIN, MPNN, SchNet, DimeNet papers.

  2. **MoleculeNet_HIV** (41,127 molecules, binary classification): HIV replication inhibition. Included in the Open Graph Benchmark (OGB) as ogbg-molhiv — the go-to large-scale molecular GNN benchmark. Source: scikit-fingerprints/MoleculeNet_HIV (HuggingFace, 1,569 downloads, graph-ml tagged).

  3. **MoleculeNet_ESOL** (1,128 molecules, regression): Aqueous solubility (log Mol/L) from Delaney 2004. The most-cited small-molecule regression benchmark in GNN papers. Source: scikit-fingerprints/MoleculeNet_ESOL (HuggingFace, 2,446 downloads, graph-ml tagged).

  4. **MoleculeNet_BBBP** (2,039 molecules, binary classification): Blood-brain barrier penetration for drug-like molecules. Standard binary classification MoleculeNet benchmark used in GNN expressiveness comparisons. Source: scikit-fingerprints/MoleculeNet_BBBP (HuggingFace, 2,206 downloads, graph-ml tagged).

  5. **MoleculeNet_Tox21** (7,831 molecules, multi-label classification): 12 toxicity targets covering nuclear receptors and stress response pathways. Tests expressiveness across diverse multi-task molecular classification. Source: scikit-fingerprints/MoleculeNet_Tox21 (HuggingFace, 1,826 downloads, graph-ml tagged).

  All examples use SMILES as input (the molecular graph string representation) and JSON-encoded property labels as output, with metadata fields for task type, label names, and row index. Format validated against exp_sel_data_out schema. Full dataset: 39.9MB (well under 100MB limit).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_3HtZDPW8AgTh
type: experiment
title: WL Expressiveness Floor for Molecular Properties
summary: |-
  Computed k-WL (k=1,2,3) graph certificates for 63,007 molecules (50K QM9 + 13K MoleculeNet: ESOL, FreeSolv, Lipophilicity, BBBP, HIV). For each (dataset, property) pair, measured: (1) collision rate = fraction of same-certificate molecule pairs whose property values differ by >0.5σ (meaningful disagreement), and (2) conditional variance floor = E[Var(y|WL_k)] / Var(y), the Bayes error lower bound for any WL_k-based predictor.

  Key findings across 24 properties:
  - WL-bottlenecked (2 props): FreeSolv/expt, HIV/HIV_active — high k=1 collision rate but near-zero k=3 variance floor; higher-k GNNs should help.
  - 3D-geometry-limited (10 props): QM9 electronic properties (HOMO, LUMO, mu, gap, r2, cv, alpha) + MoleculeNet pharmacokinetic (BBBP, ESOL, Lipophilicity) — high collision rate persists with residual variance even at k=3, indicating 3D conformation dominates.
  - WL-sufficient (10 props): QM9 thermochemical energies (u0, u298, h298, g298, zpve, A, g298_atom, h298_atom, u0_atom, u298_atom) — near-zero k=1 collision rate; 1-WL GINs already near-optimal.
  - Noise-dominated (2 props): QM9/B, QM9/alpha — low collision but above-median residual variance floor.

  Thresholds (adaptive, median-based): collision_rate_k1=0.0076, variance_floor_k3=7.47e-5.

  All QM9 quantum electronic properties (HOMO cr1=0.266, LUMO cr1=0.074, mu cr1=0.267) show high collision rates at k=1, confirming that 1-WL GNNs hit an expressiveness ceiling for these targets. Thermochemical energies (u0, h298, g298) have cr1≈0 and vf3≈0, meaning topology fully determines them — consistent with molecular formula dominance.

  Output files: collision_variance_profiles.json (24 property profiles with k=1,2,3 metrics), typology_matrix.json (2×2 quadrant assignments with reasoning), method_out.json (exp_gen_sol_out schema, validated). WL implementation uses SHA256-based deterministic hashing with hydrogen-explicit graphs. Monotonicity of variance floor (vf1 ≥ vf2 ≥ vf3) confirmed for all properties.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_OpP2YltYtXU0
type: research
title: 2-WL and 3-WL GNN Architectures for Molecules
summary: >-
  This research identifies and evaluates three main practical higher-order GNN architectures for molecular property prediction:
  (1) **k-GNN (Maron et al., 2019)** achieves proven 3-WL expressiveness using only 2-order tensors with O(n²d) complexity
  via matrix multiplication—no cubic tensor operations required. QM9 results show 20–50% MAE improvements over 1-WL GIN on
  key properties (polarizability, HOMO/LUMO gaps). (2) **I²-GNN (Huang et al., 2022)** combines Subgraph-MPNN with cycle-counting
  to achieve near-3-WL discriminative power while maintaining linear O(n·d) complexity. Proven to count 3–6-cycles (covering
  benzene rings), directly addressing molecular structural features. (3) **NGNN (Zhang & Li, 2021)** extracts rooted k-hop
  subgraphs and applies hierarchical GNN pooling; most implementable but expressiveness level not formally proven at 2-WL.
  All three have maintained GitHub implementations. PyGHO library (Wang & Zhang, 2023) provides unified integration achieving
  50% speedup and 10× code reduction. Key trade-off: k-GNN is theoretically strongest but quadratic complexity; I²-GNN balances
  theory and scalability; NGNN is most practical with good code maturity. Recommended implementation path for iteration 2:
  start with I²-GNN for cycle-counting molecular relevance or k-GNN for guaranteed 3-WL theory, fall back to NGNN if implementation
  bandwidth is tight.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 4 ---
id: art_eIA2xIm1xmvs
type: research
title: WL Expressiveness Hierarchy and Molecular Property Bottlenecks
summary: >-
  Comprehensive literature research addressing five critical theoretical and methodological questions underlying the WL expressiveness
  hypothesis for molecular property prediction. Key findings: (1) k-WL operates fundamentally differently from iterated 1-WL
  (uses vertex k-tuples, not repeated 1-hop refinement), making the measured r-round variance floors inapplicable to k-WL
  GNNs—only message-passing 1-WL models are correctly bounded; (2) Color refinement converges in 1-2 iterations for typical
  random graphs but requires up to n-1 iterations worst-case; for drug-like molecules (<50 atoms), empirical validation is
  needed but convergence likely occurs at r≤3, potentially weakening r-dependence diagnostics; (3) NO prior work measures
  per-property WL collision rates or variance floors on real molecular datasets—the proposed diagnostic is genuinely novel
  and fills a genuine gap in the literature; (4) Message-passing GNNs (GIN, GraphSAGE) are bounded by 1-WL [Xu 2019], while
  k-GNNs achieve k-WL expressiveness [Maron 2019], subgraph GNNs achieve 3-WL [Frasca 2022], and 3D geometric models (SchNet,
  DimeNet) bypass WL constraints via coordinate information; (5) BREC benchmark uses statistical paired comparisons with Fisher's
  T²-test for threshold selection rather than ad-hoc cutoffs, providing a principled methodology. Critical implementation
  consideration: Testing whether geometry-limited properties show no improvement from k>1 GNNs requires clear specification
  of which architectures are compared, as k-WL and geometric models operate orthogonally to 1-WL bounds. Recommendation: Validate
  core assumptions (1-WL convergence rate on actual drug molecules, collision-rate/performance correlation) via pilot study
  before full-scale execution.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 5 ---
id: art_1qOubuYW4T38
type: evaluation
in_dependencies:
- id: art_3HtZDPW8AgTh
  label: WL measurement results
- id: art_PA8MCYxkbsL8
  label: dataset metadata
title: WL Expressiveness Floor Robustness Validation
summary: |-
  Robustness evaluation of the WL expressiveness floor framework for molecular property prediction across 24 (dataset, property) pairs from QM9, ESOL, FreeSolv, Lipophilicity, BBBP, and HIV datasets.

  **Numerical validation (24/24 pass):** All collision rates and variance floors reported in collision_variance_profiles.json were recomputed from raw wl_certificates.json and confirmed to match to within 0.1% relative tolerance. Specific spot-checks confirmed: ESOL k=1→k=2 collision rate collapse (0.0916→0.0000), FreeSolv k=3 floor collapse to 1.383e-05, HIV variance_floor_k1=0.0410.

  **Bootstrap 95% CIs for collision rates:** For each of the 72 (dataset, property, k) triplets, 1000 bootstrap resamples of same-certificate pairs were computed. Key small-sample flags: FreeSolv k=1 has only 116 pairs (CI width ~0.09), ESOL k=2/k=3 have 13-15 pairs. QM9 properties benefit from large pair counts (up to 136,963 pairs at k=1) yielding tight CIs (width <0.005).

  **Permutation-null analysis:** 1000 label shuffles per dataset revealed that ALL 24 observed collision rates are far BELOW the null distribution (pooled null 95th percentile CR~0.73, VF~0.029). This confirms that WL certificates capture genuine structure for every property — none are explainable by chance. Properties with high original CR (e.g. QM9/homo=0.266, QM9/r2=0.317) are still far below the random-label baseline (~0.72), confirming structurally similar molecules (same WL cert) have more similar properties than random pairs.

  **Typology robustness:** Using null-based thresholds at 80th/85th/90th/95th/99th percentiles, 23/24 properties are stable across all threshold choices (Jaccard mean=0.74-1.00). Only 1 property sits at the boundary between WL-sufficient and noise-dominated under lower percentile thresholds. Under null-based classification, all 24 properties are WL-sufficient relative to random — confirming that the original median-based typology captures informative distinctions within the space of WL-informative properties, not noise-level variation.

  **Core finding validated:** The original typology (thermochemical = WL-sufficient, quantum electronic = geometry-limited) reflects genuine signal — all properties have collision rates significantly below permutation null.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 2 artifacts were created THIS iteration.

id: art_eIA2xIm1xmvs
type: research
title: WL Expressiveness Hierarchy and Molecular Property Bottlenecks
summary: >-
  Comprehensive literature research addressing five critical theoretical and methodological questions underlying the WL expressiveness
  hypothesis for molecular property prediction. Key findings: (1) k-WL operates fundamentally differently from iterated 1-WL
  (uses vertex k-tuples, not repeated 1-hop refinement), making the measured r-round variance floors inapplicable to k-WL
  GNNs—only message-passing 1-WL models are correctly bounded; (2) Color refinement converges in 1-2 iterations for typical
  random graphs but requires up to n-1 iterations worst-case; for drug-like molecules (<50 atoms), empirical validation is
  needed but convergence likely occurs at r≤3, potentially weakening r-dependence diagnostics; (3) NO prior work measures
  per-property WL collision rates or variance floors on real molecular datasets—the proposed diagnostic is genuinely novel
  and fills a genuine gap in the literature; (4) Message-passing GNNs (GIN, GraphSAGE) are bounded by 1-WL [Xu 2019], while
  k-GNNs achieve k-WL expressiveness [Maron 2019], subgraph GNNs achieve 3-WL [Frasca 2022], and 3D geometric models (SchNet,
  DimeNet) bypass WL constraints via coordinate information; (5) BREC benchmark uses statistical paired comparisons with Fisher's
  T²-test for threshold selection rather than ad-hoc cutoffs, providing a principled methodology. Critical implementation
  consideration: Testing whether geometry-limited properties show no improvement from k>1 GNNs requires clear specification
  of which architectures are compared, as k-WL and geometric models operate orthogonally to 1-WL bounds. Recommendation: Validate
  core assumptions (1-WL convergence rate on actual drug molecules, collision-rate/performance correlation) via pilot study
  before full-scale execution.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

id: art_1qOubuYW4T38
type: evaluation
in_dependencies:
- id: art_3HtZDPW8AgTh
  label: WL measurement results
- id: art_PA8MCYxkbsL8
  label: dataset metadata
title: WL Expressiveness Floor Robustness Validation
summary: |-
  Robustness evaluation of the WL expressiveness floor framework for molecular property prediction across 24 (dataset, property) pairs from QM9, ESOL, FreeSolv, Lipophilicity, BBBP, and HIV datasets.

  **Numerical validation (24/24 pass):** All collision rates and variance floors reported in collision_variance_profiles.json were recomputed from raw wl_certificates.json and confirmed to match to within 0.1% relative tolerance. Specific spot-checks confirmed: ESOL k=1→k=2 collision rate collapse (0.0916→0.0000), FreeSolv k=3 floor collapse to 1.383e-05, HIV variance_floor_k1=0.0410.

  **Bootstrap 95% CIs for collision rates:** For each of the 72 (dataset, property, k) triplets, 1000 bootstrap resamples of same-certificate pairs were computed. Key small-sample flags: FreeSolv k=1 has only 116 pairs (CI width ~0.09), ESOL k=2/k=3 have 13-15 pairs. QM9 properties benefit from large pair counts (up to 136,963 pairs at k=1) yielding tight CIs (width <0.005).

  **Permutation-null analysis:** 1000 label shuffles per dataset revealed that ALL 24 observed collision rates are far BELOW the null distribution (pooled null 95th percentile CR~0.73, VF~0.029). This confirms that WL certificates capture genuine structure for every property — none are explainable by chance. Properties with high original CR (e.g. QM9/homo=0.266, QM9/r2=0.317) are still far below the random-label baseline (~0.72), confirming structurally similar molecules (same WL cert) have more similar properties than random pairs.

  **Typology robustness:** Using null-based thresholds at 80th/85th/90th/95th/99th percentiles, 23/24 properties are stable across all threshold choices (Jaccard mean=0.74-1.00). Only 1 property sits at the boundary between WL-sufficient and noise-dominated under lower percentile thresholds. Under null-based classification, all 24 properties are WL-sufficient relative to random — confirming that the original median-based typology captures informative distinctions within the space of WL-informative properties, not noise-level variation.

  **Core finding validated:** The original typology (thermochemical = WL-sufficient, quantum electronic = geometry-limited) reflects genuine signal — all properties have collision rates significantly below permutation null.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Graph neural networks (GNNs) have become the standard approach for molecular property prediction, enabling end-to-end learning on drug discovery, materials design, and quantum chemistry tasks [1]. Yet fundamental questions remain unanswered: given a specific molecular property, what is the minimum achievable prediction error imposed by the 2D molecular topology alone, independent of any neural network architecture? Equivalently, how much of a property's variation is fundamentally unlearnable by any GNN constrained to 1-WL expressiveness—the limit of message-passing networks?

The Weisfeiler-Leman (WL) test provides the theoretical framework. The WL hierarchy establishes that message-passing GNNs (e.g., GIN, GraphSAGE) are bounded by 1-WL expressiveness [2, 3]: they cannot distinguish molecular graphs that are indistinguishable by the 1-WL color refinement algorithm. This is not a limitation of current architectures but a fundamental information-theoretic ceiling. Higher-order architectures like k-GNNs and subgraph GNNs operate on k-tuples of vertices (k-WL expressiveness, k ≥ 2) and are provably strictly more powerful [4, 5]. Yet 3D geometric models (SchNet, DimeNet) bypass the WL hierarchy entirely by incorporating atomic coordinates—information orthogonal to graph topology [6, 7].

Practitioners developing GNNs for molecular tasks face a paralyzing choice: invest in expensive higher-order message-passing architectures, incorporate 3D geometric information, or accept that topology alone may be insufficient. Current practice offers no principled answer—the decision defaults to trial-and-error benchmarking across datasets [8].

We address this gap with a quantitative per-property diagnostic: the **1-WL expressiveness floor**. For each molecular property, we measure the conditional variance of the property within WL equivalence classes—molecules assigned identical 1-WL certificates but with different property values. This conditional variance is the Bayes error lower bound: no message-passing GNN, regardless of depth, width, or training strategy, can achieve lower test error than this floor without incorporating additional features (e.g., 3D geometry) [ARTIFACT:art_3HtZDPW8AgTh].

By measuring how this floor changes as 1-WL color refinement progresses (r=1, 2, 3 rounds of refinement), we partition properties into a 2×2 typology:

1. **Topology-bottlenecked**: High initial collision rate (molecules with different property values share the same r=1 certificate), but near-zero converged floor. The 1-WL refinement recovers most variance by r=2 or r=3. These properties strictly benefit from architectures more expressive than 1-WL message-passing.

2. **3D-geometry-limited**: High collision rate persisting at convergence, with non-negligible within-class variance even at r=3. Variation within equivalence classes is attributable to 3D conformation unresolvable by any 2D graph descriptor. These properties require geometric information; higher-order topology refinement alone will not help.

3. **Topology-sufficient**: Near-zero collision rates at r=1. The 1-WL algorithm already distinguishes all relevant molecule pairs; 1-WL GINs should perform near-optimally, and further refinement adds minimal signal.

4. **Noise-dominated**: Low collision rates but high residual variance, indicating measurement error or stochasticity dominates over structural variation.

Our empirical findings across 63,007 molecules and 24 properties [ARTIFACT:art_3HtZDPW8AgTh] confirm these patterns. QM9 quantum-mechanical properties (HOMO energy, LUMO energy, dipole moment, HOMO-LUMO gap) exhibit high r=1 collision rates (7.4%–31.7%) with persistent within-class variance at convergence (0.03%–1.7% of total variance unexplained), confirming geometry-limitation. In contrast, QM9 thermochemical properties (u0, h298, g298) show near-zero collision rates and vanishing floors, confirming topology-sufficiency. MoleculeNet properties show mixed patterns: FreeSolv solvation exhibits strong topology-bottlenecking (collision rate drops 413× from r=1 to r=3), while ESOL solubility and blood-brain barrier penetration exhibit geometry-limitation.

Critically, robustness validation via bootstrap confidence intervals and permutation-null analysis [ARTIFACT:art_1qOubuYW4T38] confirms that all 24 observed collision rates are far below the 95th percentile of permutation-shuffled null distributions (~0.73), indicating that WL certificates capture genuine property structure. The typology remains stable across alternative null-based threshold choices (80th–99th percentiles of permutation-null distributions, with 23/24 properties unchanged), supporting its robustness.

[FIGURE:fig1]

Our contributions:

1. **Per-property 1-WL expressiveness floor diagnostic**: A quantitative, information-theoretic measure of the minimum achievable error for message-passing GNNs on any molecular property, grounded in conditional variance and the WL hierarchy [ARTIFACT:art_3HtZDPW8AgTh].

2. **2×2 property typology with empirical validation**: A classification framework across 24 properties in QM9 and MoleculeNet, with concrete collision rates and variance floors for each category. Typology robustness validated against permutation-null and bootstrap uncertainty [ARTIFACT:art_1qOubuYW4T38].

3. **Structural explanation for disparate GNN improvements**: The typology explains why higher-order GNNs and 3D models show such different improvements across benchmarks—geometry-limited properties require 3D information, not higher-order topology; topology-bottlenecked properties benefit from any architecture exceeding 1-WL message-passing [ARTIFACT:art_eIA2xIm1xmvs].

4. **Reproducible computational framework**: A Python pipeline for computing 1-WL certificates, collision rates, conditional variance floors, and typology assignment, applicable to any molecular benchmark.

# Methods

## 1-WL Color Refinement and Certificate Computation

We compute 1-WL certificates by iterating the color refinement algorithm [ARTIFACT:art_3HtZDPW8AgTh]. For each molecule, we construct a hydrogen-explicit graph G = (V, E, c₀) where vertices are atoms (including hydrogens) and edges are bonds. Initial colors c₀(v) = atom_type(v) encode element identity.

For r = 1, 2, 3 rounds of refinement:
$$c_r(v) = \text{HASH}(c_{r-1}(v), \text{MULTISET}\{c_{r-1}(u) : u \in N(v)\})$$

where N(v) is the neighborhood of v and HASH is a deterministic function (SHA256 in our implementation). The r-round certificate is the canonical graph hash, computed by sorting all final-round color counts and hashing the result. Two molecules with identical r-WL certificates are indistinguishable by any message-passing GNN with r neighborhood aggregation rounds.

We process molecules via RDKit SMILES parsing, explicitly retaining all hydrogen atoms to ensure canonical representations [ARTIFACT:art_3HtZDPW8AgTh].

## Collision Rate and Variance Floor Measurement

For each (dataset, property, r) triple, we measure two metrics:

**Collision rate**: The fraction of molecule pairs (m_i, m_j) satisfying:
- WL_r(m_i) = WL_r(m_j) (same r-WL certificate), AND
- |y_i - y_j| > 0.5·σ_y (meaningful disagreement: property values differ by more than half the standard deviation)

This captures the proportion of "hard" cases: molecules the algorithm cannot distinguish but which have meaningfully different property values. Small collision rates indicate the r-WL refinement successfully partitions molecules by property; high rates indicate the refinement is insufficient.

**Variance floor**: The conditional variance of the property given the r-WL certificate:
$$\text{VF}_r = \frac{E[\text{Var}(y | \text{WL}_r)]}{\text{Var}(y)}$$

This is the Bayes error lower bound (normalized by total variance for cross-property comparability): the minimum achievable mean-squared error for any deterministic r-WL-based predictor. A floor of 0.01 means that even a perfect r-WL classifier leaves 1% of property variance unexplained—an irreducible lower bound.

For efficient computation, we enumerate all pairs of molecules sharing the same r-WL certificate (exact enumeration for small groups, stratified random sampling for large groups) [ARTIFACT:art_3HtZDPW8AgTh]. For properties with small numbers of same-certificate groups (e.g., FreeSolv at r=1 with only 116 molecule pairs), we compute bootstrap 95% confidence intervals via 1000 resamples of same-certificate pairs [ARTIFACT:art_1qOubuYW4T38].

## Typology Assignment and Threshold Justification

We assign each (dataset, property) to a quadrant based on **collision rate at r=1** and **variance floor at convergence (r=3)**. The original paper used median-based thresholds (CR_k1 = 0.00761, VF_k3 = 7.47e-05), which by construction divide properties into balanced quadrants regardless of true distribution.

To validate the typology is not an artifact of median-based splitting, we conducted permutation-null analysis [ARTIFACT:art_1qOubuYW4T38]: we shuffled property labels 1000 times per dataset and recomputed collision rates and variance floors. Under label permutation, the null distribution reached 95th percentiles of CR_k1 ≈ 0.73 and VF_k3 ≈ 0.029. All 24 observed collision rates and variance floors are far below these null thresholds, confirming that WL certificates capture genuine property structure.

We then re-classified all properties using null-based thresholds at the 80th, 85th, 90th, 95th, and 99th percentiles. Results show 23/24 properties remain in their original quadrant across all percentile choices (mean Jaccard stability index 0.74–1.00), with only 1 property (BBBP/p_np) shifting between quadrants under lower percentiles [ARTIFACT:art_1qOubuYW4T38]. This demonstrates the typology captures stable, non-arbitrary distinctions.

For the final paper, we report both the median-based assignments (for comparability with prior iteration) and null-based robustness analysis (for principled justification).

## Distinguishing 1-WL Rounds from k-Dimensional WL

A critical clarification from reviewer feedback: the measured r-round-1-WL variance floors do NOT correspond to the expressiveness ceilings of k-WL architectures (k-GNNs, I²-GNNs, NGNN) [ARTIFACT:art_eIA2xIm1xmvs]. 

Maron et al. (2019) define k-dimensional WL as a color refinement operating on k-tuples of vertices with fundamentally different update rules than iterating standard 1-WL [4]. The key distinction:
- **1-WL (iterated)**: Each round refines single-vertex colors based on 1-hop neighborhoods. Iteration converges to a stable partition in O(log n) or O(n) rounds depending on graph structure.
- **k-WL (k ≥ 2)**: Directly colors k-tuples of vertices with update rules over k-neighborhoods. Strictly more powerful than any number of 1-WL rounds.

For small drug-like molecules (< 50 atoms), 1-WL color refinement converges in r ≤ 3 rounds: further iterations produce no new color classes. Thus, measuring r=1, 2, 3 variance floors captures the "topological expressiveness" of message-passing GNNs but does not measure the expressiveness of k-WL architectures. This distinction is crucial: claims that "geometry-limited properties show no improvement from k-GNNs" would require comparing message-passing GINs against genuine k-GNN architectures, not simply more rounds of 1-WL color refinement.

# Results

## Overall Typology Distribution

Across 24 properties (QM9 + MoleculeNet), the median-based typology assignment yields [ARTIFACT:art_3HtZDPW8AgTh]:

- **Topology-bottlenecked**: 2 properties (FreeSolv solvation, HIV activity)
- **3D-geometry-limited**: 10 properties (QM9 electronic properties + MoleculeNet pharmacokinetic)
- **Topology-sufficient**: 10 properties (QM9 thermochemical energies)
- **Noise-dominated**: 2 properties (QM9 rotational constant B, polarizability alpha)

These assignments are stable across null-based threshold choices: 23/24 properties remain classified in the same quadrant when thresholds are set at the 80th–99th percentiles of permutation-null distributions [ARTIFACT:art_1qOubuYW4T38].

[FIGURE:fig2]

## QM9 Quantum-Electronic Properties (Geometry-Limited)

All five QM9 quantum-mechanical properties exhibit high r=1 collision rates and non-negligible converged floors, confirming geometry-limitation:

- **HOMO (ε_HOMO)**: CR_k1 = 0.266, VF_k3 = 0.00169. One-third of molecules share the same r=1 certificate despite differing HOMO energies by >0.5σ. Even after 3-round refinement, 0.17% of variance remains within-class, attributable to 3D electron cloud shape variation among molecules with identical 2D topology.

- **LUMO (ε_LUMO)**: CR_k1 = 0.074, VF_k3 = 0.000278. Lower collision than HOMO but persistent residual variance.

- **Dipole moment (μ)**: CR_k1 = 0.267, VF_k3 = 0.00164. Highest k=1 collision, strongly geometry-dependent (3D charge distribution).

- **HOMO-LUMO gap (Δε)**: CR_k1 = 0.164, VF_k3 = 0.000836.

- **Electronic spatial extent (r²)**: CR_k1 = 0.317, VF_k3 = 0.00300. Nearly one-third collision at r=1; the highest collision rate in the QM9 dataset.

These findings align with the chemistry: electronic properties depend on orbital shapes and 3D electron density distributions, not merely graph connectivity. SchNet and DimeNet incorporate 3D distance information and achieve substantial improvements on these properties precisely because geometry matters.

## QM9 Thermochemical Properties (Topology-Sufficient)

In stark contrast, QM9 thermochemical properties exhibit near-zero collision rates and vanishing variance floors:

- **Internal energy at 0K (u0)**: CR_k1 = 0.0%, VF_k3 ≈ 7.85e-08. Perfect topology-sufficiency: molecular formula alone determines energy; 2D graph refinement captures all topology-dependent variation.

- **Enthalpy at 298K (h298)**: CR_k1 ≈ 0.0%, VF_k3 ≈ 0.0. Identical results.

- **Free energy at 298K (g298)**: CR_k1 ≈ 0.0%, VF_k3 ≈ 0.0.

- **Zero-point vibrational energy (zpve)**: CR_k1 ≈ 0.0%, VF_k3 ≈ 0.0.

- **Heat capacity at 298K (A)**: CR_k1 ≈ 0.0%, VF_k3 ≈ 0.0.

This pattern is theoretically expected: thermochemical properties are determined by molecular composition (formula), not 3D conformation. The constant-energy relationship holds across all possible 3D structures of the same molecule.

## MoleculeNet Properties: Mixed Patterns

**FreeSolv Solvation (Topology-Bottlenecked)** [ARTIFACT:art_3HtZDPW8AgTh]:
- CR_k1 = 0.069, VF_k1 = 0.00573, VF_k2 ≈ 0.00001, VF_k3 ≈ 0.00001
- **Key signature**: High initial collision (6.9%) but dramatic floor collapse (413× reduction from k=1 to k=2, further 2× to k=3). Remaining collision pairs at r=1 are resolved by r=2 refinement; the within-class variance drops to near-zero.
- This signals strong **topology-bottlenecking**: molecular graphs that 1-WL cannot initially distinguish are resolved by 2-WL refinement. The property is deterministic given sufficient topological information; 3D geometry contributes minimally.

**ESOL Solubility (Reclassified: Noise-Dominated)** [ARTIFACT:art_1qOubuYW4T38]:
- CR_k1 = 0.092, VF_k1 = 0.0043, VF_k2 = 0.0002, VF_k3 = 0.000118
- **Correction to prior iteration**: Collisions are FULLY RESOLVED at r=2 (CR_k2 = 0.0, CR_k3 = 0.0), not persistent. The r=1 collision rate is not indicative of persistent geometry-limitation.
- The above-median variance floor (VF_k3 > 7.47e-05) drives the original "3D-geometry-limited" classification, but this is misleading: the floor reflects measurement noise in solubility data, not true 3D conformation dependence.
- **Revised classification**: ESOL should be classified as **noise-dominated** (high r=1 collision, but noise rather than geometry explains residual variance).

**BBBP Blood-Brain Barrier (Geometry-Limited)**:
- CR_k1 = 0.143, VF_k3 = 0.0182. High collision persists despite refinement; above-median floor indicates 3D conformation effects (membrane permeability depends on 3D molecular shape and flexibility).

**HIV Replication Inhibition (Topology-Bottlenecked)**:
- CR_k1 = 0.075, VF_k3 ≈ 0.0. High initial collision but complete collapse by convergence; strong bottlenecking signal.

## Variance Floor Monotonicity and Interpretation

All 24 properties exhibit VF_k1 ≥ VF_k2 ≥ VF_k3, confirming the 1-WL hierarchy is faithfully represented: increasing refinement reduces unexplained variance. However, collision rates increase for some properties (e.g., HOMO: CR goes 0.266→0.298→0.391 from k=1→k=2→k=3) [ARTIFACT:art_3HtZDPW8AgTh].

This counterintuitive behavior reflects a key insight: as certificates refine, the total number of same-certificate groups increases, but the TOTAL NUMBER of same-certificate pairs shrinks (many molecules now have unique certificates). The collision rate—defined as the ratio of conflicting pairs within same-certificate groups—can therefore rise even as refinement progresses, because the remaining same-certificate groups are disproportionately "hard" cases with higher property disagreement.

For this reason, **variance floor is the primary metric** (monotone, information-theoretically justified as Bayes error), while collision rate is secondary (interpretable but non-monotone for some properties). We emphasize VF in the typology, though collision rate provides additional interpretability.

# Discussion

## Interpretation and Implications for GNN Architecture Selection

The typology directly explains observed patterns in molecular GNN literature:

**Topology-bottlenecked properties (FreeSolv, HIV)**: These properties have high initial 1-WL collision rates but near-zero converged floors. The message is clear: a message-passing GNN (bounded by 1-WL) will hit an expressiveness ceiling, but that ceiling is recoverable by any architecture exceeding 1-WL refinement. Higher-order message-passing (e.g., 2-hop neighborhoods, subgraph sampling) should help. However, we emphasize that k-GNN architectures (which implement k-WL on vertex tuples) are fundamentally different from multi-round 1-WL refinement, and their applicability requires validation [ARTIFACT:art_eIA2xIm1xmvs].

**3D-geometry-limited properties (HOMO, LUMO, dipole moment, BBBP)**: These show high collision rates that persist through r=3 convergence, with non-negligible residual variance (0.1%–2% of total). This indicates within-class variation is due to 3D conformation, not further topological refinement. Practitioners should invest in 3D geometric models (SchNet, DimeNet) or equivariant architectures that incorporate distance/angle features. Multi-round 1-WL refinement will provide minimal additional signal.

**Topology-sufficient properties (u0, h298, g298, zpve, A)**: Zero collision and near-zero floors across all rounds. These properties are fully determined by molecular formula; message-passing GINs should achieve near-optimal performance. Architects should not invest in higher complexity.

**Noise-dominated properties (B, alpha in QM9; potentially ESOL)**: Low collision but high residual variance. Measurement error or stochasticity dominates; improving GNN expressiveness is unlikely to reduce error below the noise floor. Focus instead on data quality and outlier detection.

## Validation Status and Limitations

We emphasize that this typology is a **diagnostic framework**, not yet a validated predictive tool. The key limitation is the absence of GNN training experiments. The original reviewer feedback [referenced in prompt] critiqued that we made architectural claims (e.g., "geometry-limited properties should show minimal improvement from k-GNNs") without prospective validation via controlled experiments.

For the paper to be fully compelling, we would need to:

1. Train 1-WL GIN (baseline message-passing) on properties from each quadrant.
2. Train higher-expressiveness architectures (e.g., subgraph GNNs, simplified k-GNNs) on the same properties.
3. Train 3D geometric models (SchNet) on geometry-limited properties.
4. Measure test error for each (property, architecture) pair.
5. Verify that: geometry-limited properties show large improvements from 3D models but minimal from higher-order topology; topology-bottlenecked properties show improvements from higher-order topology but large improvements from geometric models; topology-sufficient properties show no improvement from either.

We acknowledge this as future work. However, the typology itself—the diagnostic measurement of variance floors and collision rates—is sound and novel, and the framework provides falsifiable predictions that can be tested in subsequent work.

## Methodological Robustness

We validate the typology against multiple threats to validity [ARTIFACT:art_1qOubuYW4T38]:

**Numerical accuracy**: All collision rates and variance floors were recomputed from raw WL certificates and confirmed to match to within 0.1% relative tolerance (24/24 properties pass).

**Sampling variability**: Bootstrap 95% confidence intervals on collision rates were computed via 1000 resamples. Small-sample properties (FreeSolv, ESOL at high r) have wider CIs (width ~0.09 for FreeSolv r=1), but the general patterns (bottlenecking vs. geometry-limitation) are robust.

**Threshold arbitrariness**: Permutation-null analysis shows all 24 properties have collision rates far below the null 95th percentile (~0.73), confirming WL certificates capture genuine structure. Typology classifications are stable across alternative null-based thresholds (80th–99th percentiles), with 23/24 properties unchanged (mean Jaccard 0.74–1.0).

**Convergence assumption**: We assume 1-WL converges by r=3 for drug-like molecules. For small molecules (<50 atoms with typical atom counts), this is plausible [ARTIFACT:art_eIA2xIm1xmvs], but empirical validation on the actual QM9/MoleculeNet molecules would strengthen the assumption.

## Novelty and Positioning

Per-property collision rate measurement and variance floor analysis for molecular properties is novel [ARTIFACT:art_eIA2xIm1xmvs]. Existing work measures WL expressiveness theoretically (Xu et al. 2019, Maron et al. 2019) or on synthetic graph isomorphism benchmarks (BREC, Wang & Zhang 2023), but not on continuous molecular property values. The proposed typology framework is a new contribution to the intersection of WL theory and practical molecular GNN design.

What is NOT novel: the WL hierarchy, k-GNN architectures, 3D geometric models, and WL convergence properties are all established.

# Conclusion

We have introduced a quantitative diagnostic for measuring the 1-WL expressiveness floor of molecular properties. By computing collision rates and within-class variance across 24 properties in QM9 and MoleculeNet, we reveal a 2×2 typology that explains when higher-order message-passing, 3D geometry, or simple 1-WL models suffice for accurate prediction.

This framework transforms the WL hierarchy from a theoretical abstraction into a practical tool. Practitioners can now:

1. Compute the expressiveness floor for any property on any benchmark in minutes.
2. Diagnose whether a property is geometry-limited, topology-bottlenecked, or topology-sufficient.
3. Guide architectural investment with principled confidence, avoiding expensive dead-ends.

Future work includes: (i) controlled GNN training experiments to validate predictive claims about architecture benefit; (ii) extension to temporal molecular dynamics, where collisions may vary as conformation evolves; (iii) mechanistic analysis connecting specific bottlenecks (e.g., high r² collision) to chemical structure classes (rigid vs. flexible molecules); and (iv) integration with active learning to reduce collision-rate estimation variance.

# References

[1] J. Gilmer, S. S. Schoenholz, P. F. Riley, O. Vinyals, and G. E. Dahl, "Neural message passing for quantum chemistry," in Proc. Int. Conf. Mach. Learn., 2017, pp. 1263–1272.

[2] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, "How powerful are graph neural networks?" in Proc. Int. Conf. Learn. Represent., 2019.

[3] T. Kipf and M. Welling, "Semi-supervised classification with graph convolutional networks," in Proc. Int. Conf. Learn. Represent., 2017.

[4] H. Maron, H. Ben-Hamu, H. Serviansky, and Y. Lipman, "Provably powerful graph networks," in Neural Inf. Process. Syst., 2019.

[5] M. Frasca, P. Barceló, and E. Sandi, "Expressive power of graph neural networks: A functional perspective," in Neural Inf. Process. Syst., 2022.

[6] K. T. Schütt, P.-J. Kindermans, H. E. S. Felix, S. Chmiela, A. Tkatchenko, and K.-R. Müller, "SchNet: A continuous-filter convolutional neural network for modeling quantum interactions," in Adv. Neural Inf. Process. Syst., 2017, pp. 991–1001.

[7] J. Gasteiger, J. Groß, and S. Günnemann, "Directional message passing for molecular graphs," in Int. Conf. Learn. Represent., 2020.

[8] L. Wu, Z. Cui, C. Zhou, and S. Pan, "A comprehensive survey on graph neural networks," IEEE Trans. Knowl. Data Eng., vol. 34, no. 8, pp. 3440–3463, 2021.

[9] R. Ramakrishnan, P. O. Dral, M. Rupp, and O. A. von Lilienfeld, "Quantum chemistry structures and properties of 134 kilo molecules," Sci. Data, vol. 1, p. 140022, 2014.

[10] B. Wang and M. Zhang, "An empirical study of realized GNN expressiveness," in Proc. Int. Conf. Mach. Learn., 2023, pp. 52134–52155.

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) No GNN training experiments validate the typology's predictive claims. The central practical contribution of the paper is predicting when higher-order GNNs or 3D geometric models will improve over 1-WL GINs. The paper explicitly defers this validation to future work ('the typology is a diagnostic framework, not yet a validated predictive tool'). This means the typology's predictive accuracy is entirely untested. A typology with wrong predictions would be worse than useless (it would misdirect architecture investment). Without at least one controlled experiment, no reader can trust the framework's utility.
  Action: Run a minimal 2×2 experiment: (FreeSolv, QM9-HOMO) × (GIN, higher-expressiveness GNN or SchNet). FreeSolv (n=642) can be trained in minutes; QM9-HOMO on a subset is feasible. If the typology is correct: FreeSolv should show larger improvements from higher-order GNNs than from SchNet; HOMO should show larger improvements from SchNet than from higher-order GNNs. Report test MAE or RMSE. This one experiment would raise the score by 1-2 points.
- [MAJOR] (methodology) HIV dataset subsampling is undisclosed. The dataset artifact states HIV has 41,127 molecules, but the experiment artifact (mini_method_out.json) shows only 4,998 molecules used for HIV (about 12%). This 88% data reduction is never mentioned in the paper — the reader is led to believe the full HIV dataset was analyzed. Subsampling can substantially alter collision rates (especially for rare certificate collisions), and class imbalance in HIV (active vs. inactive) makes random subsampling risky.
  Action: Disclose the HIV subsampling explicitly in Methods: how many molecules were used, how they were selected (random, stratified by class, etc.), and how sensitive the WL-bottlenecked classification is to subsampling. Either use the full dataset (OGB provides it) or justify the subsample with a sensitivity analysis showing the collision rate and variance floor are stable across random subsamples.
- [MAJOR] (rigor) The ESOL reclassification in the paper text conflicts with the code artifact. The paper states ESOL has been 'Reclassified: Noise-Dominated' in the Results section. However, the experiment artifact (mini_method_out.json, line: 'predict_quadrant: 3D-geometry-limited') still classifies ESOL as '3D-geometry-limited'. The typology_matrix.json output from the experiment has not been updated. This is a direct inconsistency between the paper's claims and the code output.
  Action: Update the experiment artifact code to reflect the ESOL reclassification, or explicitly note in the Methods that the paper applies a post-hoc correction to the automated classification for ESOL. Add a table showing all 24 properties with both the automated (code-based) classification and any manual corrections, with justification for each correction.
- [MAJOR] (methodology) The 1-WL convergence assumption (convergence by r=3 for drug-like molecules) is stated as an assumption but never empirically validated on the actual QM9/MoleculeNet molecules. The paper says 'for small drug-like molecules (<50 atoms), this is plausible, but empirical validation would strengthen the assumption.' For the variance floor to correctly represent the Bayes error lower bound of 1-WL GNNs, it is critical that the certificate at r=3 equals the stable certificate at convergence. If convergence occurs at r=4 or r=5 for some molecules, the reported r=3 floors are underestimates of the true ceiling.
  Action: Add a simple convergence check: for each molecule in the dataset, compute WL certificates until the certificate does not change between rounds. Report the distribution of convergence rounds across all molecules. If 99%+ of molecules converge by r=3, this validates the assumption. This is a zero-cost addition to the existing code pipeline.
- [MINOR] (scope) Lipophilicity (4,200 molecules, 3D-geometry-limited in artifact) and Tox21 (7,831 molecules, 12 toxicity targets) are included in the dataset artifact and presumably processed in the experiment, but are completely absent from the Results section. The paper presents results for only 24 properties, which appear to include QM9 (19 properties based on results) and 5 MoleculeNet properties (ESOL, FreeSolv, BBBP, HIV, Lipophilicity). Tox21's 12 targets are entirely unaccounted for. The introduction says '24 properties' — if Tox21 was excluded, this should be explained.
  Action: Either include Lipophilicity and Tox21 results in the main table (they are already computed per the artifacts) or explicitly state in Methods that these datasets were excluded from the typology analysis and why. The current omission makes the property count inconsistent with the dataset descriptions.
- [MINOR] (clarity) The dual threshold system (median-based for 'comparability with prior iteration' AND null-based for 'principled justification') creates ambiguity about the official typology. The paper reports both systems and says typology assignments are presented using median-based thresholds with null-based robustness analysis. But the permutation-null analysis shows all 24 properties are 'WL-informative' relative to random shuffling — the null-based thresholds tell us something different from the median-based thresholds. A reader cannot tell which classification is the paper's actual finding.
  Action: Designate one threshold system as primary (recommend null-based at 95th percentile, which is principled). Present the median-based classification in a supplementary table as a secondary analysis for reproducibility with prior iteration. Add a sentence explicitly stating 'all results in the main text use null-based thresholds at the 95th percentile of permutation distributions.'
- [MINOR] (clarity) The paper describes the collision rate as 'the fraction of molecule pairs satisfying same certificate AND meaningful disagreement' but the denominator is ambiguous. Is the denominator (a) all molecule pairs, (b) all same-certificate pairs, or (c) all meaningfully-disagreeing pairs? The definition as stated ('fraction of molecule pairs') implies (a), but the Bayes error interpretation requires (b). The artifact confirms it is computed over same-certificate pairs, but the paper text is misleading.
  Action: Rewrite the collision rate definition to make the denominator explicit: 'Among all pairs (m_i, m_j) with WL_r(m_i) = WL_r(m_j) [same certificate], the fraction whose property values differ by more than 0.5σ.' Add the total number of same-certificate pairs per property to the results table so readers can assess statistical power.
- [MINOR] (novelty) The paper does not engage with 'Rethinking the Expressive Power of GNNs for Molecular Graphs' (Zhu et al. 2022, ICLR) mentioned in the prior review. This paper measures WL collision rates on molecular graphs and could be closely related. The prior review flagged this and the current paper does not acknowledge whether this work was checked.
  Action: Search for Zhu et al. 2022 'Rethinking the Expressive Power of GNNs for Molecular Graphs' and characterize what is different: the variance floor formulation, the 2×2 typology, the multi-round analysis, and the per-property diagnostic are all potentially distinct. If Zhu et al. compute per-property collision rates, the paper must clearly distinguish what is new here.
</reviewer_feedback>



<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-24 21:13:25 UTC

```
Graph neural network expressiveness under the Weisfeiler-Leman hierarchy for molecular property prediction
```

### [3] SYSTEM-USER prompt · 2026-06-24 21:14:11 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 2 problems — fix ALL of them at once:
  - at `artifact_relations.0.relation_rationale`: "Evaluation artifact recomputes and validates collision rates and variance floors from the experiment's raw WL certificates." is too long (at most 120 characters, got 123)
  - at `relation_rationale`: 'Same typology frame; adds GNN validation gap as critical unresolved requirement and addresses all four MAJORs structurally.' is too long (at most 120 characters, got 123)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
