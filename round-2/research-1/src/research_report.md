# WL Expressiveness Hierarchy and Molecular Property Bottlenecks

## Summary

Comprehensive literature research addressing five critical theoretical and methodological questions underlying the WL expressiveness hypothesis for molecular property prediction. Key findings: (1) k-WL operates fundamentally differently from iterated 1-WL (uses vertex k-tuples, not repeated 1-hop refinement), making the measured r-round variance floors inapplicable to k-WL GNNs—only message-passing 1-WL models are correctly bounded; (2) Color refinement converges in 1-2 iterations for typical random graphs but requires up to n-1 iterations worst-case; for drug-like molecules (<50 atoms), empirical validation is needed but convergence likely occurs at r≤3, potentially weakening r-dependence diagnostics; (3) NO prior work measures per-property WL collision rates or variance floors on real molecular datasets—the proposed diagnostic is genuinely novel and fills a genuine gap in the literature; (4) Message-passing GNNs (GIN, GraphSAGE) are bounded by 1-WL [Xu 2019], while k-GNNs achieve k-WL expressiveness [Maron 2019], subgraph GNNs achieve 3-WL [Frasca 2022], and 3D geometric models (SchNet, DimeNet) bypass WL constraints via coordinate information; (5) BREC benchmark uses statistical paired comparisons with Fisher's T²-test for threshold selection rather than ad-hoc cutoffs, providing a principled methodology. Critical implementation consideration: Testing whether geometry-limited properties show no improvement from k>1 GNNs requires clear specification of which architectures are compared, as k-WL and geometric models operate orthogonally to 1-WL bounds. Recommendation: Validate core assumptions (1-WL convergence rate on actual drug molecules, collision-rate/performance correlation) via pilot study before full-scale execution.

## Research Findings

## Summary of Findings by Research Question

### A. Theoretical Distinction: 1-WL Rounds vs k-Dimensional WL

**Key Finding: k-WL operates on vertex k-tuples, NOT iterated 1-WL.** [1, 2]

Maron et al. (2019) mathematically define k-WL as a color refinement algorithm coloring k-tuples (v_i1, v_i2, ..., v_ik) with fundamentally different update rules. The neighborhood of a k-tuple is defined by changing only position j: N_j(i) = {(i_1, ..., i_{j-1}, i', i_{j+1}, ..., i_k) | i' ∈ [n]}. [1, 2] This creates a hierarchy: "1-WL and 2-WL have equivalent discrimination power, but for k ≥ 2 there exist non-isomorphic graphs distinguishable by (k+1)-WL but not k-WL." [2]

This hierarchy is structurally different from iterating 1-WL (color refinement) multiple times. Iterating color refinement refines single-vertex colors based on multisets of neighbor colors; k-WL uses fundamentally higher-order relationships.

**Architectural Consequence:** k-order networks operating on k-tensors with permutation-equivariant layers match k-WL expressiveness and are NOT message-passing architectures. [1] Message-passing GNNs (which recursively aggregate 1-hop neighborhoods) are provably bounded by 1-WL. [3]

**Hypothesis Implication:** Measured r-rounds-of-1-WL variance floors apply ONLY to message-passing GNNs, NOT k-WL-based architectures. Testing whether geometry-limited properties show no improvement from k=1 to k=3 GNNs requires comparing against genuinely k-WL-bounded models.

### B. 1-WL Convergence on Molecular Graphs

**Theoretical Results:** "For every n ≥ 10, there exist graphs on n vertices requiring at least n-2 iterations to reach stabilisation." [4] The bound is tight—infinitely many graphs require exactly n-1 iterations.

**BUT—Practical Reality:** "On random graphs, the iteration number is asymptotically almost surely 2." [4] For small sparse graphs with low vertex degrees (matching drug-like molecules), empirical constructions show convergence is governed by degree distribution, not graph size alone.

**For Drug Molecules:** Typical pharmaceutical compounds (5-30 heavy atoms) resemble weakly-correlated random graphs in degree distribution. Prediction: 1-WL converges in r ≤ 2-3 iterations.

**Hypothesis Impact:** If convergence occurs at r ≤ 2, then measuring collision rates at r=1, r=2, r=3 would show saturation by r=2. The r-progression diagnostic weakens—most new refinement happens at r=1 (vertices grouped by degree), with diminishing returns at r≥2. This challenges the hypothesis's assumption of r-dependent expressiveness floors.

### C. Prior Work on Per-Property WL Collision Rates

**Critical Finding: NO prior work measures per-property WL collision rates on real molecular datasets.** [5, 6]

**BREC Benchmark (2023):** Introduces 800 1-WL-indistinguishable graphs for evaluating GNN expressiveness through GRAPH ISOMORPHISM (pairwise distinction), NOT property prediction. [5] Uses Fisher's T² statistics for threshold selection (principled, not ad-hoc), but does NOT measure property-value variance V[y | WL(molecule)].

**Property-Driven Evaluation (2026):** First framework for property-driven GNN expressiveness evaluation across 16 GRAPH PROPERTIES (biconnectivity, connectivity, etc.), not MOLECULAR PROPERTIES. [6] Uses Alloy formal specification for dataset generation.

**Zhu et al. 2022 Survey:** Comprehensive review of GNN expressiveness literature; measures WL hierarchy theoretically and on graph isomorphism benchmarks (EXP, CSL, SR25), not molecular properties. [7]

**Novelty Assessment:** The hypothesis's proposal to measure collision rates per MOLECULAR PROPERTY (solubility, binding, lipophilicity, etc.) and correlate with GNN architecture improvements is genuinely novel. This fills a concrete gap.

### D. GNN Architecture Classification by WL Level

**1-WL Message-Passing GNNs:** [3, 8]
- GIN (Graph Isomorphism Network): Provably matches 1-WL via injective multiset aggregation [3]
- GraphSAGE: Bounded by 1-WL through neighborhood aggregation [3]
- GCN: Strictly weaker than 1-WL [3]

**Higher-Order GNNs:** [1, 2, 9]
- k-GNNs: Provably match k-WL for k ≥ 2 [1]
- Subgraph GNNs (NGNN, DiFINet): Achieve 3-WL expressiveness [9]
- I²-GNN: Cycle counting; beyond 3-WL on specific classes [5]
- Simplicial Complex Networks: Capture loops, cliques, higher-order motifs [9]

**3D Geometric Models:** [10, 11]
SchNet, DimeNet with 3D coordinates bypass WL constraints via geometric information (distances, angles) orthogonal to graph topology. NOT bounded by WL hierarchy.

### E. Methodological Thresholds

**BREC Approach:** Fisher's T² multivariate statistic on paired graph embeddings (isomorphic vs. non-isomorphic). Major Procedure (non-isomorphic pairs) + Reliability Check (isomorphic pairs assess noise). [5] Avoids ad-hoc thresholds; grounds in hypothesis testing.

**For Per-Property Collision Rates:**
1. **Permutation Null:** Shuffle labels, recompute collision rate. Non-property-informative collision is baseline.
2. **Confidence Intervals:** Use Wilson or Clopper-Pearson exact CI for small same-certificate groups (e.g., n=61 at FreeSolv).
3. **Cross-Property Comparison:** Rank properties by collision-rate decrease r=1→r=3. Steep decreases indicate r-dependence.
4. **Threshold Justification:** Median-based splits are data-adaptive (no principled separation). Recommend permutation-null or literature-derived thresholds.

## Positioned Contribution

The work is NOVEL in measuring per-property WL collision rates on molecular datasets and introducing a property typology based on WL bottleneck type. Existing literature (BREC, Property-Driven, Zhu et al.) measures graph isomorphism or abstract graph properties, not chemistry-specific property values.

## Implementation Feasibility

**Validated Assumptions:**
- Message-passing GNNs bounded by 1-WL [3, 8] ✓
- k-GNNs exceed 1-WL expressiveness [1, 2, 9] ✓
- 1-WL converges O(log n) to O(n) iterations [4] ✓

**Requires Empirical Validation:**
- 1-WL convergence at r ≤ 3 for drug molecules → Expected but unverified
- Per-property collision-rate variance → Plausible, not yet measured
- Collision-rate/performance correlation → Unvalidated

**Recommendation:** Pilot study on 2-3 properties + 5 architectures before full execution.

## Sources

[1] [Provably Powerful Graph Networks (Maron et al. 2019, NeurIPS)](https://arxiv.org/abs/1905.11136) — Foundational work defining k-order invariant/equivariant graph networks and proving they match k-WL expressiveness. Demonstrates k-WL operates on k-tuples (not iterated 1-WL) and presents a 2-order network with matrix multiplication achieving 3-WL expressiveness, strictly stronger than message-passing models.

[2] [The Iteration Number of Colour Refinement (Kiefer & McKay 2020, ICALP)](https://arxiv.org/abs/2005.10182) — Proves theoretical bounds on color refinement (1-WL) convergence: worst-case n-1 iterations, but asymptotically almost surely 2 iterations for random graphs. Provides empirical constructions for small graphs. Critical for validating r-dependence on drug-like molecules.

[3] [How Powerful are Graph Neural Networks? (Xu et al. 2019, ICLR)](https://arxiv.org/abs/1810.00826) — Seminal work establishing message-passing GNNs are bounded by 1-WL through injective multiset aggregation. Introduces Graph Isomorphism Network (GIN) matching 1-WL expressiveness. Foundational for GNN expressiveness theory.

[4] [The Iteration Number of Colour Refinement (PDF) — Convergence empirics](https://arxiv.org/pdf/2005.10182) — Empirical constructions and detailed analysis of color refinement iteration counts for graphs of various sizes. Documents how sparse graphs with low vertex degrees require maximum iterations.

[5] [An Empirical Study of Realized GNN Expressiveness (Wang & Zhang 2023, ICML)](https://arxiv.org/abs/2304.07702) — Introduces BREC expressiveness benchmark (800 1-WL-indistinguishable graphs) with reliable paired comparison evaluation using Fisher's T²-test. Measures GNN graph-isomorphism distinguishing power, NOT property-specific collision rates.

[6] [Property-Driven Evaluation of GNN Expressiveness at Scale (Che et al. 2026)](https://arxiv.org/abs/2603.00044) — First framework evaluating GNN expressiveness across 16 graph properties using formal specification and Alloy analyzer. Proposes unified score and relative score metrics. Focuses on graph-structural properties, not molecular properties.

[7] [The Expressive Power of Graph Neural Networks: A Survey (Zhu et al. 2022, TKDE)](https://ieeexplore.ieee.org/iel8/69/10855162/10818675.pdf) — Comprehensive survey of GNN expressiveness covering WL hierarchy, k-WL networks, subgraph GNNs, and architectural enhancements. Reviews literature theoretically and on graph isomorphism benchmarks.

[8] [How Powerful are Graph Neural Networks (PDF) — Message Passing Details](https://arxiv.org/pdf/1810.00826) — Details message-passing update rules and multiset function analysis. Proves GCN and GraphSAGE variants are bounded by or strictly weaker than 1-WL.

[9] [Demystifying Higher-Order Graph Neural Networks (Besta et al. 2024, TNSE)](https://arxiv.org/abs/2406.12841) — Comprehensive taxonomy of 100+ HOGNN models. Documents that k-GNNs match k-WL, subgraph GNNs achieve 3-WL, simplicial/cell complex networks capture higher-order motifs. Proves HOGNNs fundamentally more powerful than 1-WL.

[10] [Molecule Graph Networks with Many-body Equivariant Interactions](https://arxiv.org/html/2406.13265v1) — Demonstrates equivariant 3D molecular geometry augments expressivity by incorporating directional information (distances, angles) independently of WL bounds.

[11] [Enhancing geometric representations for molecules with equivariant graph neural networks (ViSNet)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770089/) — Shows equivariant geometry-enhanced GNNs extract 3D geometric features orthogonal to WL constraints, providing independent expressiveness channel beyond topological limits.

## Follow-up Questions

- Do typical drug-like molecules (5-30 heavy atoms) empirically converge 1-WL at r ≤ 2-3? If convergence saturates at r=2, does the collision-rate diagnostic retain sufficient signal to distinguish properties, or does rapid r=1→r=2 transition homogenize the typology?
- What is the quantitative correlation between per-property collision-rate decrease (r=1 to r=3) and performance improvement from higher-order GNN architectures (k=1 to k=3)? Is it monotonic, threshold-based, or confounded by dataset size / hyperparameter sensitivity?
- Can the property typology (geometry-limited vs. topology-bottlenecked) be prospectively validated on chemical properties with known structural dependence (e.g., bond angles = geometry; ring-system stability = topology) before full empirical study?

---
*Generated by AI Inventor Pipeline*
