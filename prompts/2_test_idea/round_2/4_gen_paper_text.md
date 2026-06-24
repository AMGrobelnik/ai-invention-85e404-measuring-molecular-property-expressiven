# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_7KogxZ5PgvFN` — Measuring Molecular Property Expressiveness Ceilings via 1-WL Color Refinement
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-24 21:07:39 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A research paper writer (Step 3.4: GEN_PAPER_TEXT in the invention loop)

You received the hypothesis, all artifacts, the previous paper draft (if any), and reviewer feedback.
Write a complete paper draft with figure placeholders.

Publication-quality paper → strong contribution. Weak paper → wasted iteration.
</your_role>
</ai_inventor_context>

<research_methodology>
Write like a researcher drafting a paper, not a chatbot summarizing bullet points.

- Structure as a paper would: research question → methodology → results → analysis → limitations. Not a list of "we did X, then Y."
- Ground every claim in specific artifacts and specific numbers. "Results show improvement" is empty — state effect sizes, baselines, and conditions.
- Be honest about what worked, what didn't, and why. Don't spin failures as "future work."
- The paper's headline contribution should be a positive or surprising finding. Negative results are valuable context but should not be the primary narrative — lead with what works.
- Address reviewer feedback from previous iterations explicitly — show you've thought about each critique.
</research_methodology>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# Introduction

Graph neural networks (GNNs) have emerged as the dominant paradigm for molecular property prediction, enabling end-to-end learning from molecular graphs for applications in drug discovery, materials design, and quantum chemistry [1]. Yet a fundamental question remains unanswered: given a specific molecular property, how much of its variation is fundamentally unlearnable by any GNN operating on 2D molecular topology?

The Weisfeiler-Leman (WL) test provides the theoretical answer. The WL hierarchy establishes that any k-WL-bounded GNN cannot distinguish molecular graphs that share the same k-WL certificate—a canonical label produced by k rounds of color refinement [2, 3]. This hierarchy has become the dominant lens for measuring GNN expressiveness [4]. Higher-order GNNs (k≥2) are provably more expressive than 1-WL message-passing networks (e.g., GIN [5]). Yet in practice, practitioners face a paralyzing question: Does my property need 2-WL expressiveness, or would investing in expensive 3D geometric methods yield more? Current practice offers no principled answer—it is heuristic trial-and-error across datasets [6].

We address this gap with a quantitative diagnostic: the WL expressiveness *floor* for each molecular property. The floor is the minimum achievable mean-squared error (MSE) for any WL-bounded predictor, measured as the conditional variance of the property *within* WL equivalence classes [ARTIFACT:art_3HtZDPW8AgTh]. This floor is an information-theoretic lower bound—no predictor, no matter how expressive at the WL level, can beat it without additional features (e.g., 3D geometry).

We computed k-WL certificates for 63,007 molecules (50K QM9 quantum properties + 13K MoleculeNet pharmacokinetic targets) [ARTIFACT:art_PA8MCYxkbsL8], measuring both the k-WL collision rate (fraction of molecule pairs with the same certificate but meaningfully different property values) and the k-dependent variance floor. This yields a tractable 2×2 typology [ARTIFACT:art_3HtZDPW8AgTh]:

1. **WL-bottlenecked**: High collision rate, low k=3 floor. Topology is the limiting factor; higher-k GNNs should yield >10% relative error reduction.
2. **3D-geometry-limited**: High collision rate persisting at k=3. Molecular 3D conformation dominates; topology alone is insufficient even at k=3.
3. **WL-sufficient**: Low collision rate. 1-WL GINs are already near-optimal; minimal GNN improvement possible.
4. **Noise-dominated**: Low collision but high residual variance. Measurement error or stochasticity dominates.

Our key empirical finding: QM9 quantum properties (HOMO, LUMO, dipole moment, HOMO-LUMO gap) fall into the geometry-limited quadrant, with k=1 collision rates of 7.4–26.6% and k=3 variance floors of 0.0009–0.050 (15–50% of total variance unexplained even at k=3). In contrast, QM9 thermochemical energies (u0, h298, g298) show zero collision and near-zero floors, confirming that molecular formula alone determines them—topology refinement adds nothing. This explains why SchNet and DimeNet's 3D information yields dramatic improvements on quantum properties but minimal gains on thermochemical targets. We validate this across MoleculeNet benchmarks: FreeSolv solvation exhibits strong bottlenecking (floor drops 413× from k=1 to k=3), while ESOL solubility remains geometry-limited despite high k=1 collision.

[FIGURE:fig1]

Our contributions are:
1. A quantitative per-property WL expressiveness floor diagnostic, grounded in information theory and measurable on standard benchmarks.
2. Empirical verification of the 2×2 typology across 24 properties in QM9 and MoleculeNet, with concrete collision rates and variance floors.
3. An explanation for why higher-order GNNs and 3D methods show such disparate improvements across benchmarks—the typology predicts which will help.
4. A reproducible computational framework (k-WL certificate computation, collision measurement, typology assignment) applicable to any molecular benchmark.

## Related Work

The theoretical foundations for GNN expressiveness lie in the Weisfeiler-Leman test. Xu et al. [2] established that Graph Isomorphism Networks (GINs) are maximally expressive within the 1-WL hierarchy—they can provably distinguish all graphs that 1-WL can distinguish, but no more. Maron et al. [3] and subsequent work on higher-order GNNs (k-GNN, NGNN, I²-GNN) demonstrated that k-WL-bounded architectures strictly exceed 1-WL expressiveness and that the WL hierarchy is indeed the correct measure [4, 7]. However, this literature makes *qualitative* claims only: "k-WL GNNs are more expressive" [3]. It does not measure per-property floors or predict which real tasks benefit from each tier.

On molecular GNNs, two camps have emerged. The 2D topology camp focuses on 1-WL and 2-WL GNNs, showing that message-passing networks excel at functional-group-level predictions [5, 8]. The 3D geometry camp argues that quantum properties require 3D atomic coordinates: SchNet [9] and DimeNet [10] use continuous distance and angle features, achieving state-of-the-art QM9 results. Yet the literature lacks clarity on *when* each approach is necessary. Wang et al.'s BREC benchmark [11] measures GNN expressiveness on synthetic graphs but does not connect expressiveness to real molecular properties or collision-rate-based floors.

The contribution of this work is the bridge: we quantify the WL expressiveness floor per property, enabling practitioners to diagnose which architectural investment (higher-order GNN vs. 3D geometry) will yield returns. This shifts the field from trial-and-error to principled engineering.

# Methods

## WL Certificate Computation

For each dataset, we compute k-WL certificates (k=1,2,3) using the standard Weisfeiler-Leman color refinement algorithm. Let G = (V, E, c₀) be a molecule represented as a graph with hydrogen-explicit atoms as vertices and bonds as edges, with initial colors c₀(v) = atom_type(v).

For each refinement round r = 1, ..., k:
$$c_r(v) = \text{HASH}(c_{r-1}(v), \text{MULTISET}\{c_{r-1}(u) : u \in N(v)\})$$

where HASH is a deterministic hash function (SHA256 in our implementation) and N(v) is the neighborhood of v. The k-WL certificate is the canonical graph hash, computed by sorting and hashing all final-round color counts.

We process molecules via RDKit SMILES parsing, explicitly retaining all hydrogen atoms to ensure canonical representations [ARTIFACT:art_3HtZDPW8AgTh].

## Collision Rate and Variance Floor

For each (dataset, property, k) triple:

**Collision rate**: Fraction of molecule pairs (m_i, m_j) such that WL_k(m_i) = WL_k(m_j) but |y_i - y_j| > 0.5·σ_y (meaningful disagreement threshold).

**Variance floor**: The conditional variance of y given the k-WL certificate:
$$\text{VF}_k = E[\text{Var}(y | \text{WL}_k)] / \text{Var}(y)$$

This is the Bayes error lower bound—the minimum achievable MSE by any deterministic WL_k-based predictor, normalized by total variance for cross-property comparability.

We compute collision rates on all pairs where WL_k assignments are identical, capping the computation to tractable subsets for QM9 (136,963 k=1 pairs analyzed; full dataset too large for exhaustive pair enumeration, so collision rates are estimated on random samples with replacement when necessary).

## Typology Assignment

We assign each property to a quadrant based on adaptive thresholds (median-based):
- **Collision rate threshold**: 0.00761 (median across all k=1 collisions)
- **Variance floor threshold** (k=3): 7.47e-05 (median across all k=3 floors)

These thresholds are dataset-agnostic and preserve balance across quadrants.

# Results

## Overall Typology Distribution

Across 24 properties (QM9 + MoleculeNet), we observe:
- **WL-bottlenecked**: 2 properties (FreeSolv solvation, HIV activity)
- **3D-geometry-limited**: 10 properties (QM9 quantum + MoleculeNet pharmacokinetic)
- **WL-sufficient**: 10 properties (QM9 thermochemical energies)
- **Noise-dominated**: 2 properties (QM9 rotational constant B, polarizability alpha)

[FIGURE:fig2]

## Quantum Properties (QM9)

All five QM9 quantum-mechanical properties exhibit high k=1 collision rates, confirming the geometry-limited classification:

- **HOMO (ε_HOMO)**: collision_rate_k1 = 0.266, variance_floor_k3 = 0.00169. Despite k=3 refinement, 0.17% of variance (1.69e-3) remains irreducible by topology alone. This reflects that two isomers (identical 2D topology, different 3D conformations) have vastly different HOMO energies.

- **LUMO (ε_LUMO)**: collision_rate_k1 = 0.074, variance_floor_k3 = 0.000278. Lower collision than HOMO but still substantial residual variance, again attributable to 3D-conformation dependence.

- **Dipole moment (μ)**: collision_rate_k1 = 0.267, variance_floor_k3 = 0.00164. Highest k=1 collision among quantum properties; strongly geometry-limited.

- **HOMO-LUMO gap (Δε)**: collision_rate_k1 = 0.164, variance_floor_k3 = 0.000836.

- **Electronic spatial extent (r²)**: collision_rate_k1 = 0.317, variance_floor_k3 = 0.00300. Highest collision overall; nearly one-third of r² variance depends on 3D geometry beyond any k-WL refinement.

In contrast, QM9 thermochemical properties (u0, h298, g298, zpve, A) show near-zero k=1 collision rates and vanishing k=3 floors (e.g., u0: 0% collision, floor = 7.85e-08). This is expected: molecular formula determines energy; 2D graph refinement captures all topology-dependent variation.

## MoleculeNet Pharmacokinetic Properties

**FreeSolv solvation (expt)**: collision_rate_k1 = 0.069, variance_floor_k1 = 0.00573, variance_floor_k3 = 1.38e-05. The dramatic floor collapse (413× reduction) signals **WL-bottlenecking**: k=2 and k=3 refinement nearly eliminate collision, recovering most variance.

**HIV activity (HIV_active)**: collision_rate_k1 = 0.075, variance_floor_k3 = 0.0 (complete collapse at k=2). Strong bottlenecking signal.

**ESOL solubility**: collision_rate_k1 = 0.092, variance_floor_k3 = 0.000118. High k=1 collision with persistent k=3 floor indicates **geometry-limitation**: aqueous solubility depends on both functional groups (2D) and 3D hydrogen bonding geometry.

**BBBP BBB penetration**: collision_rate_k1 = 0.143, variance_floor_k3 = 0.0182. Strongly geometry-limited; penetration correlates with both lipophilicity (2D functional groups) and 3D molecular shape.

**Lipophilicity (exp)**: collision_rate_k1 = 0.109, variance_floor_k3 = 0.000479. Borderline 3D-geometry-limited; primarily driven by 2D functional groups (partition coefficient) but with conformational contributions.

[FIGURE:fig3]

## Variance Floor Monotonicity

All 24 properties exhibit variance_floor_k1 ≥ variance_floor_k2 ≥ variance_floor_k3, confirming that higher-k refinement reduces residual variance. The *magnitude* of this reduction, however, varies dramatically:

- **Geometry-limited properties**: Floors plateau early (e.g., ESOL drops 18.3× from k=1 to k=2 but only further 21× to k=3).
- **Bottlenecked properties**: Floors drop steeply across all k (e.g., HIV_active: k=1→k=2 floor collapses from 0.041 to 0.0, a 413× drop in FreeSolv's case).
- **WL-sufficient properties**: Already near-zero at k=1 (no room to drop further).

This monotonicity confirms the WL hierarchy is faithfully represented in our computation.

# Discussion

## Interpretation and Implications

Our typology directly explains empirical observations in the molecular GNN literature:

**Why do higher-order GNNs help some tasks but not others?** The answer is the typology. Bottlenecked properties (e.g., HIV activity) benefit greatly from k-GNN or I²-GNN because the collision bottleneck is genuine—resolving it via higher-order refinement recovers substantial variance. Geometry-limited properties (e.g., HOMO energy) show minimal or no improvement from k-GNN alone; practitioners must integrate 3D information (SchNet, DimeNet, GraphDTA).

**Why do quantum properties respond so dramatically to 3D methods?** Geometry-limitation: the k=3 variance floors (0.0008–0.050) are non-negligible, indicating that even perfect k=3 prediction leaves substantial error. This error is the irreducible 3D-conformation contribution. SchNet's continuous distance features directly encode this, bypassing the 2D-topology bottleneck entirely.

**Why are thermochemical properties "solved" by 1-WL GINs?** WL-sufficiency: zero collision and near-zero floors mean that molecular formula (captured by 1-WL counts) determines these properties. Higher-k GNNs add no signal.

## Validation Against GNN Architectures

Our framework makes falsifiable predictions about relative GNN performance. Consider two architectures: GIN (1-WL) and k-GNN (3-WL). On a WL-bottlenecked property, we predict k-GNN will substantially outperform GIN; on geometry-limited properties, we predict minimal improvement. While we did not train these models in this iteration, prior work supports these predictions:

- Maron et al. [3] report k-GNN improvements of 20–50% on QM9 electronic properties. However, these properties are geometry-limited in our framework, so the improvements are modest relative to 3D baselines (SchNet outperforms k-GNN on the same tasks).
- On MPNN-friendly tasks (e.g., graph classification benchmarks), higher-order GNNs show dramatic improvements [11], consistent with tasks in the bottlenecked or WL-sufficient quadrants.

## Limitations

1. **Collision rate estimation**: For QM9 (50K molecules), exhaustive pair enumeration is intractable. We estimate collision rates on representative samples, introducing sampling variance. Future work should use more efficient collision-counting algorithms or larger random samples.

2. **2D-only analysis**: We do not incorporate 3D coordinates or molecular conformation information. The framework measures what 2D topology alone can achieve. A full predictive model would augment this floor with 3D data and re-measure achievable accuracy.

3. **Binary threshold on "meaningful disagreement"**: We threshold collisions at |Δy| > 0.5σ_y. This is arbitrary. A sensitivity analysis varying this threshold would strengthen the framework.

4. **Limited property scope**: 24 properties across two benchmarks. Broader coverage (more MoleculeNet datasets, more QM9 properties) would strengthen the typology's generalizability.

5. **No causal mechanistic explanation**: The framework is diagnostic—it identifies where barriers exist—but does not mechanistically explain *why* geometry dominates for HOMO vs. why solvation exhibits bottlenecking. Integrating chemical intuition (e.g., "HOMO depends on 3D electron cloud shape") is future work.

# Conclusion

We have introduced a quantitative framework for diagnosing the WL expressiveness floor of molecular properties. By measuring k-WL collision rates and conditional variance floors across 24 properties, we reveal a 2×2 typology that explains when higher-order GNNs will help, when 3D geometry is essential, and when 1-WL message-passing suffices.

This diagnostic transforms the WL hierarchy from theoretical abstraction into a practical tool for molecular GNN design. Practitioners can now compute the floor for any property on any benchmark, predict architectural benefit with principled confidence, and avoid expensive dead-ends (e.g., investing in higher-order GNNs for geometry-limited properties).

Future work includes: (i) training higher-order GNNs and 3D-geometry models on properties from each quadrant to validate performance predictions; (ii) extending the framework to temporal molecular dynamics, where collision rates may vary as molecular conformation evolves; (iii) integrating active learning to intelligently sample molecules and reduce collision-rate estimation variance; and (iv) bridging to chemical interpretability by connecting specific bottlenecks (e.g., r² high collision) to chemical structure classes (e.g., rigid vs. flexible molecules).

# References

[1] J. Gilmer, S. Schoenholz, P. F. Riley, O. Vinyals, and G. E. Dahl, "Neural Message Passing for Quantum Chemistry," in Proc. Int. Conf. Mach. Learn., 2017, pp. 1263–1272.

[2] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, "How Powerful are Graph Neural Networks?" in Proc. Int. Conf. Learn. Represent., 2019.

[3] C. Morris, M. Ritzert, M. Fey, W. L. Hamilton, J. E. Lenssen, G. Rattan, and M. Grohe, "Weisfeiler and Leman Go Neural: Higher-order Graph Neural Networks," in AAAI Conf. Artif. Intell., 2019, pp. 4602–4609.

[4] B. Zhang, C. Fan, S. Liu, K. Huang, X. Zhao, J. Huang, and Z. Liu, "The Expressive Power of Graph Neural Networks: A Survey," IEEE Trans. Knowl. Data Eng., vol. 37, pp. 1455–1474, 2023.

[5] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, "How Powerful are Graph Neural Networks?" in Proc. Int. Conf. Learn. Represent., 2019.

[6] K. T. Schütt, P.-J. Kindermans, H. E. S. Felix, S. Chmiela, A. Tkatchenko, and K.-R. Müller, "SchNet: A continuous-filter convolutional neural network for modeling quantum interactions," in Adv. Neural Inf. Process. Syst., 2017, pp. 991–1001.

[7] Y. Huang, X. Peng, J. Ma, and M. Zhang, "Boosting the Cycle Counting Power of Graph Neural Networks with I²-GNNs," in Proc. Int. Conf. Learn. Represent., 2022.

[8] T. Kipf and M. Welling, "Semi-Supervised Classification with Graph Convolutional Networks," in Proc. Int. Conf. Learn. Represent., 2017.

[9] K. T. Schütt, P.-J. Kindermans, H. E. S. Felix, S. Chmiela, A. Tkatchenko, and K.-R. Müller, "SchNet: A continuous-filter convolutional neural network for modeling quantum interactions," in Adv. Neural Inf. Process. Syst., 2017, pp. 991–1001.

[10] J. Gasteiger, J. Groß, and S. Günnemann, "Directional Message Passing for Molecular Graphs," in Int. Conf. Learn. Represent., 2020.

[11] B. Wang, Z. L. Zhang, and Z. Wang, "An Empirical Study of Realized GNN Expressiveness," in ICML 2024 Workshop, 2024.

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (methodology) Critical conflation of k rounds of 1-WL with the k-dimensional WL test (k-WL). The code in method.py runs k iterations of standard 1-WL neighborhood aggregation and labels the result 'k-WL certificate.' However, in the GNN expressiveness literature, k-WL refers to the k-dimensional WL test operating on k-tuples of nodes (e.g., Maron et al. 2019's Folklore WL). These are provably different: 2-WL is strictly more powerful than any number of 1-WL rounds; it can distinguish graphs that 1-WL cannot distinguish even after convergence (e.g., the Shrikhande graph vs. the 4x4 rook graph). Running 1-WL for 2 or 3 rounds converges to the same stable partition as running it to completion—there is no new expressiveness from adding rounds once convergence is reached for small molecular graphs. The paper's claim that k=3 certificates correspond to '3-WL expressiveness floors' and predict k-GNN performance is therefore incorrect.
  Action: Either (a) implement genuine 2-WL and 3-WL by operating on node tuples (computationally expensive but correct), using code from PyGHO or BREC benchmark implementations; or (b) reframe the entire paper as measuring 'WL certificate refinement over r=1,2,3 rounds of 1-WL' and make clear that the k=2,3 floors are NOT the floors for 2-WL and 3-WL GNNs. In case (b), remove all references to k-GNN, I²-GNN, and NGNN as architecture-level predictions, since those architectures implement k-WL, not k-rounds-of-1-WL.
- [MAJOR] (evidence) No GNN training experiments to validate the typology's predictive claims. The paper's main practical contribution is predicting when higher-order GNNs or 3D methods will help. Yet it contains zero training experiments. The Discussion section validates predictions by citing prior literature (e.g., 'Maron et al. report k-GNN improvements of 20–50%'), but this is post-hoc reinterpretation, not prospective validation. The paper explicitly acknowledges this: 'While we did not train these models in this iteration.' Without at least one controlled experiment—train GIN and a k-WL GNN on a bottlenecked vs. geometry-limited property and show the typology correctly predicts relative improvement—the typology remains a plausible hypothesis, not a demonstrated result.
  Action: Run at minimum a 2×2 experiment: (WL-bottlenecked × geometry-limited) × (1-WL GIN × higher-k GNN or SchNet). FreeSolv (n=642) and HOMO from QM9 (n=50K) are natural choices. Report test MAE or RMSE relative improvement from 1-WL→higher architecture. If the typology is correct, FreeSolv should show large improvement from k-GNN while HOMO should show large improvement from SchNet but not k-GNN. This single experiment would transform the paper from diagnostic proposal to validated tool.
- [MAJOR] (methodology) Collision rate sampling for QM9 is statistically inadequate. The paper analyzes '136,963 k=1 pairs' for QM9 (50,000 molecules), which represents approximately 0.011% of the C(50000,2) ≈ 1.25 billion total pairs. With a reported collision rate of 26.6% for HOMO at k=1, the effective sample of collision pairs is approximately 36,445, which is reasonable for the rate estimate itself. However, the sampling is restricted to pairs sharing the same certificate (same-certificate pairs), not all pairs. The paper conflates these. The collision rate denominator is not all pairs but only same-certificate pairs—this is correct per the Bayes error formulation—but the text says '136,963 k=1 pairs analyzed; full dataset too large for exhaustive pair enumeration' without clarifying this distinction. For small collision rates (e.g., LUMO at 7.4%), the number of observed collision pairs could be very small.
  Action: Clarify in the Methods section whether '136,963 pairs' refers to all sampled pairs or only same-certificate pairs. Report the number of same-certificate groups and the average group size for each property. For properties with few same-certificate groups (e.g., FreeSolv at k=1 with only 61 groups), add bootstrap confidence intervals on the collision rate. Report effective sample sizes explicitly.
- [MAJOR] (methodology) Collision rates increase with k for many QM9 electronic properties, which is unexplained and internally inconsistent with the paper's narrative. From the artifact data: HOMO collision rate goes from 0.266 (k=1) → 0.298 (k=2) → 0.391 (k=3); gap: 0.164→0.184→0.258; cv: 0.159→0.248→0.377; B: 0.003→0.015→0.033. The paper claims 'All 24 properties exhibit variance_floor_k1 ≥ variance_floor_k2 ≥ variance_floor_k3' (which is true), but the collision RATES increase for these properties. The paper says nothing about this. This counterintuitive behavior occurs because higher-k certificates split many molecules into more refined groups, and the groups that remain (those 1-WL still cannot distinguish after more rounds) are the hardest cases with more property disagreement—so the ratio of conflicting pairs among same-certificate pairs rises. This means the 'collision rate' metric behaves differently than a reviewer would expect from a 'more refinement = fewer ambiguities' narrative.
  Action: Add a section or table explicitly showing collision rates at k=1,2,3 for all 24 properties. Explain why rates increase for some properties: the denominator (total same-certificate pairs) shrinks as certificates refine, but the remaining same-certificate pairs are disproportionately 'hard' collision cases. Consider using a normalized metric that accounts for this, or use only the variance floor (which is monotone) as the primary metric and demote collision rate to secondary.
- [MAJOR] (methodology) The 2×2 typology thresholds are median-based, guaranteeing by construction that approximately half of properties fall above and half below each threshold. From the artifact: collision_rate threshold = 0.00761 (median of k=1 collision rates across 24 properties), variance_floor threshold = 7.47e-5 (median of k=3 floors). This makes the typology assignment a tautology: it divides the property space into quadrants at the population median, not at any principled chemical or statistical threshold. A dataset with 24 properties will always produce roughly 6 properties per quadrant regardless of the actual distribution. This undermines any claim that the typology reveals something non-trivial about the distribution of properties across categories.
  Action: Replace median-based thresholds with principled alternatives. Options: (a) derive null distributions for collision rate and variance floor by randomly permuting property labels across molecules (within each dataset), and set thresholds at the 95th percentile of null distributions; (b) use physically motivated thresholds (e.g., variance floor > 1% total variance indicates non-negligible 3D contribution); (c) use a clustering approach (e.g., k-means on the 2D floor/collision space) to let the data reveal natural groupings. Report sensitivity of typology assignments to threshold choice.
- [MINOR] (evidence) ESOL is classified as 'geometry-limited' but the collision rate drops to exactly 0.0 at k=2 (from the artifact data: cr_k2=0.0, cr_k3=0.0). The paper says ESOL shows 'high k=1 collision with persistent k=3 floor indicates geometry-limitation: aqueous solubility depends on both functional groups (2D) and 3D hydrogen bonding geometry.' But 'persistent collision' implies collisions remain at k=3, which is false—all collisions are resolved at k=2. The geometry-limited label is driven entirely by the above-median k=3 variance floor (1.18e-4 > 7.47e-5), not by persistent collisions. The paper's chemical explanation ('3D hydrogen bonding') is speculative and inconsistent with the actual data (no k=2 or k=3 collisions).
  Action: Correct the ESOL discussion to accurately state that collisions are resolved at k=2 (not persistent). Reclassify if the 'geometry-limited' label requires persistent collisions, or redefine the quadrant criterion as based solely on variance floor (independent of collision persistence). Remove the speculative 3D hydrogen bonding explanation unless it can be supported by a mechanistic analysis.
- [MINOR] (evidence) Numerical error in Results: the paper states ESOL variance floor 'drops 18.3× from k=1 to k=2 but only further 21× to k=3.' From the artifact: vf1=4.30e-3, vf2=2.49e-4, vf3=1.18e-4. The k=1→k=2 drop is 4.30e-3/2.49e-4 = 17.3× (not 18.3×), and the k=2→k=3 drop is 2.49e-4/1.18e-4 = 2.1× (not 21×). The 21× is off by a factor of 10.
  Action: Correct to: 'drops 17.3× from k=1 to k=2 and a further 2.1× to k=3.' Also cross-check all other reported ratios against the artifact JSON.
- [MINOR] (scope) FreeSolv and Lipophilicity are used as key results (FreeSolv's 413× floor drop is the central example of WL-bottlenecking) but neither dataset appears in the dataset artifact (art_PA8MCYxkbsL8), which lists QM9, HIV, ESOL, BBBP, Tox21. FreeSolv (n=642) is in the experiment artifact but is undocumented in the dataset pipeline.
  Action: Add FreeSolv and Lipophilicity to the dataset artifact description. Report the data source (e.g., MoleculeNet FreeSolv via scikit-fingerprints) and confirm they are processed through the same data.py pipeline as the other datasets.
- [MINOR] (novelty) The variance floor as conditional variance within WL equivalence classes is mathematically natural, but the paper should more carefully distinguish this from existing work. Papers such as 'Rethinking the Expressive Power of GNNs for Molecular Graphs' (Zhu et al. 2022, ICLR) and the BREC benchmark (Wang et al. 2024) have measured WL collision rates on molecular and synthetic graphs. The paper cites Wang et al. [11] for BREC but does not engage with whether Zhu et al. or similar works have computed per-property floors. A literature search should confirm this gap is real.
  Action: Search for Zhu et al. (2022) 'Rethinking the Expressive Power of GNNs for Molecular Graphs' and similar works that measure per-property WL collisions on molecular benchmarks. If they exist, characterize what is novel here (e.g., variance floor vs. binary collision, typology framework, multi-k analysis). If a prior paper has done essentially the same thing, this must be acknowledged prominently.
- [MINOR] (clarity) References [1] and [5] are identical (both cite Xu et al. 2019, How Powerful are Graph Neural Networks), and references [6] and [9] are identical (both cite SchNet, Schütt et al. 2017). The paper has 11 numbered references but only 9 distinct sources.
  Action: Deduplicate references. Replace duplicate [5] with the MPNN paper (Gilmer et al. 2017, already cited as [1]) and distinguish them correctly, or use a different relevant citation. Fix [6] and [9] to use a single SchNet entry.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

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
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 5 research artifacts across all iterations.

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
NEW THIS ITERATION: These 2 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

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
type: research
id: art_eIA2xIm1xmvs

title: WL Expressiveness Floor Robustness Validation
summary: |-
  Robustness evaluation of the WL expressiveness floor framework for molecular property prediction across 24 (dataset, property) pairs from QM9, ESOL, FreeSolv, Lipophilicity, BBBP, and HIV datasets.

  **Numerical validation (24/24 pass):** All collision rates and variance floors reported in collision_variance_profiles.json were recomputed from raw wl_certificates.json and confirmed to match to within 0.1% relative tolerance. Specific spot-checks confirmed: ESOL k=1→k=2 collision rate collapse (0.0916→0.0000), FreeSolv k=3 floor collapse to 1.383e-05, HIV variance_floor_k1=0.0410.

  **Bootstrap 95% CIs for collision rates:** For each of the 72 (dataset, property, k) triplets, 1000 bootstrap resamples of same-certificate pairs were computed. Key small-sample flags: FreeSolv k=1 has only 116 pairs (CI width ~0.09), ESOL k=2/k=3 have 13-15 pairs. QM9 properties benefit from large pair counts (up to 136,963 pairs at k=1) yielding tight CIs (width <0.005).

  **Permutation-null analysis:** 1000 label shuffles per dataset revealed that ALL 24 observed collision rates are far BELOW the null distribution (pooled null 95th percentile CR~0.73, VF~0.029). This confirms that WL certificates capture genuine structure for every property — none are explainable by chance. Properties with high original CR (e.g. QM9/homo=0.266, QM9/r2=0.317) are still far below the random-label baseline (~0.72), confirming structurally similar molecules (same WL cert) have more similar properties than random pairs.

  **Typology robustness:** Using null-based thresholds at 80th/85th/90th/95th/99th percentiles, 23/24 properties are stable across all threshold choices (Jaccard mean=0.74-1.00). Only 1 property sits at the boundary between WL-sufficient and noise-dominated under lower percentile thresholds. Under null-based classification, all 24 properties are WL-sufficient relative to random — confirming that the original median-based typology captures informative distinctions within the space of WL-informative properties, not noise-level variation.

  **Core finding validated:** The original typology (thermochemical = WL-sufficient, quantum electronic = geometry-limited) reflects genuine signal — all properties have collision rates significantly below permutation null.
type: evaluation
id: art_1qOubuYW4T38
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
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
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-24 21:07:39 UTC

```
Graph neural network expressiveness under the Weisfeiler-Leman hierarchy for molecular property prediction
```

### [3] SKILL-INPUT — TaskCreate · 2026-06-24 21:07:53 UTC

The agent loaded the **TaskCreate** skill.

```
Tool: Skill
TaskCreate
```

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-06-24 21:08:23 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
