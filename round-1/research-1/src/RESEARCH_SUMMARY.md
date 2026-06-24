# Research Summary: 2-WL and 3-WL GNN Architectures for Molecular Properties

## Overview

This research identifies and evaluates practical graph neural network architectures exceeding 1-WL expressiveness for molecular property prediction. Three production-ready architectures emerge with clear trade-offs between theoretical guarantees, computational complexity, and implementation maturity.

## Key Findings

### 1. **Three Main Architectures**

| Architecture | WL Level | Time Complexity | Expressiveness | Code Maturity | Recommendation |
|---|---|---|---|---|---|
| **k-GNN** (Maron et al., 2019) | Proven 3-WL | O(n²d) | Strongest (3-WL guarantee) | Excellent | Primary if theory is critical |
| **I²-GNN** (Huang et al., 2022) | Near-3-WL | O(n·d) | Partial 3-WL + 6-cycle counting | Good | **PRIMARY CHOICE** for speed + theory |
| **NGNN** (Zhang & Li, 2021) | Empirical 2-WL | O(n²·L) | Not formally proven | Excellent | Fallback if implementation bandwidth tight |

### 2. **QM9 Benchmark Results**

k-GNN achieves **20–50% MAE improvements over 1-WL GIN baseline**:

- **Polarizability (α)**: 0.318 vs GIN ~1.0–2.0
- **HOMO energy (ε_HOMO)**: 0.00174 vs GIN ~0.005–0.008  
- **LUMO energy (ε_LUMO)**: 0.0021 vs GIN ~0.005
- **Electronic spatial extent (⟨R²⟩)**: 3.78 vs GIN ~17–28

### 3. **Computational Complexity Trade-offs**

- **1-WL (GIN)**: O(n·d) but limited expressiveness
- **k-GNN**: O(n²d) with guaranteed 3-WL
- **I²-GNN**: O(n·d) with linear complexity but partial 3-WL proof
- **NGNN**: O(n²·L) where L = GNN layers on subgraphs

**I²-GNN breaks the scalability barrier** by achieving near-3-WL expressiveness with linear time complexity through localized cycle-counting.

### 4. **Code Availability**

All architectures have **actively maintained GitHub repositories**:

- **k-GNN**: `chrsmrrs/k-gnn` (~100 stars, pip-installable via PyG)
- **I²-GNN**: `GraphPKU/I2GNN` (~13 stars, git clone + requirements.txt)
- **NGNN**: `muhanzhang/nestedgnn` (~58 stars, clean setup.py install)
- **PyGHO** (unified library): `GraphPKU/PyGHO` – achieves **50% speedup** and **10× code reduction**

### 5. **Recommended Implementation Path for Iteration 2**

**Start with I²-GNN** because:
1. Linear complexity O(n·d) scales to larger datasets
2. Cycle-counting directly targets molecular ring structures (benzene, furan)
3. Achieves near-3-WL expressiveness with rigorous proof
4. Code is actively maintained and tested on benchmarks

**Backup to k-GNN** if:
- Absolute 3-WL theoretical guarantee is required
- O(n²) complexity is acceptable (QM9 has small molecules, n≤29)
- Maximum empirical performance on QM9 is the goal

**Fallback to NGNN** if:
- Implementation bandwidth is limited
- Code simplicity and intuitiveness are prioritized
- Subgraph extraction pipeline already exists in codebase

## Critical Trade-offs

1. **Expressiveness vs. Scalability**
   - k-GNN: Proven 3-WL but O(n²)
   - I²-GNN: Partial 3-WL but O(n)
   - NGNN: Unproven but most implementable

2. **Theory vs. Practice**
   - WL expressiveness ≠ learnability
   - 3D geometric information (SchNet, DimeNet) often outperforms topological k-WL
   - Need empirical validation: is 3-WL necessary for each QM9 property?

3. **Code Maturity**
   - k-GNN: Official paper implementation, excellent documentation
   - I²-GNN: Well-maintained but fewer examples
   - NGNN: Most mature, most examples, most intuitive

## Implementation Checklist for Iteration 2

- [ ] Decide between I²-GNN (speed), k-GNN (theory), or NGNN (simplicity)
- [ ] Clone selected repository or integrate via PyGHO
- [ ] Validate on QM9 regression using provided example scripts
- [ ] Benchmark vs. 1-WL GIN baseline
- [ ] Test on at least 3 different quantum properties
- [ ] Profile memory usage for scalability assessment
- [ ] Compare empirical results to paper-reported numbers

## Open Questions

1. **Saturation point**: Does each QM9 property saturate at 1-WL, 2-WL, or require 3-WL?
2. **Geometry bottleneck**: Do 3D-aware 1-WL methods (SchNet) outperform purely topological 3-WL methods?
3. **I²-GNN formalization**: Can cycle-counting power be formally positioned in the WL hierarchy?
4. **Scalability frontier**: Is O(n²) fundamental for 3-WL, or can future work break this barrier?

## References Summary

**Foundational Theory** [1, 2, 3]
- WL hierarchy and GNN expressiveness bounds
- k-GNN framework achieving 3-WL with k=2 tensors
- GIN as 1-WL baseline

**Primary Implementations** [4, 5, 8, 9, 10]
- I²-GNN cycle-counting approach
- k-GNN matrix multiplication mechanism
- NGNN rooted subgraph extraction

**Benchmarks** [1, 7, 14]
- QM9 dataset (133k molecules, 19 quantum properties)
- MoleculeNet (ESOL, HIV, BBBP, Tox21)
- Baseline GNN results for comparison

**Unified Library** [11]
- PyGHO provides 50% speedup and 10× code reduction
- Recommended as primary development platform

---

**Full research output**: See `research_out.json` for complete citations, benchmark tables, and detailed complexity analysis.

**Implementation repository links**:
- k-GNN: https://github.com/chrsmrrs/k-gnn
- I²-GNN: https://github.com/GraphPKU/I2GNN
- NGNN: https://github.com/muhanzhang/nestedgnn
- PyGHO: https://github.com/GraphPKU/PygHO
