# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_7KogxZ5PgvFN` — Measuring Molecular Property Expressiveness Ceilings via 1-WL Color Refinement
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-24 19:26:27 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: WL Expressiveness Floor Computation for Molecular Properties
summary: >-
  Compute k-WL certificates (k=1,2,3) for QM9 and MoleculeNet datasets, measure collision rates and conditional variance for
  all properties, and assign each to a 2×2 typology (WL-bottlenecked vs 3D-geometry-limited vs WL-sufficient vs noise-dominated).
  Output collision/variance profiles, typology matrix, and per-property expressiveness floors.
runpod_compute_profile: cpu_heavy
implementation_pseudocode: "## Phase 0: Setup & Data Loading (5% time)\n- Import: networkx, pandas, numpy, scipy, rdkit (molecule\
  \ I/O), PyTorch Geometric (optional QM9 loader), aii-json (validation)\n- Load QM9 (130K molecules, 19 properties) from\
  \ PyG or raw source\n- Load MoleculeNet datasets: ESOL, BBBP, HIV, Tox21 (total ~10-20K molecules across all, multiple binary/regression\
  \ targets)\n- Convert to canonical graph representation: atoms as nodes (features = atom type, atomic number), bonds as\
  \ edges (features = bond type)\n- Store as: dataset_molecules.json with schema {molecule_id, smiles, atom_types, bonds,\
  \ properties: {prop1: value1, ...}, atom_count}\n\n## Phase 1: k-WL Certificate Computation (30% time)\n### For k=1,2,3:\n\
  \  **1a. Canonical WL Color Refinement**\n  - For each molecule:\n    - Initialize node colors: λ⁽⁰⁾(v) = atom_type (or\
  \ more detailed: tuple(atomic_number, formal_charge, num_hydrogens))\n    - For each iteration i from 1 to max_k:\n    \
  \  - For each node v: λ⁽ⁱ⁾(v) = hash(λ⁽ⁱ⁻¹⁾(v), sorted_multiset({λ⁽ⁱ⁻¹⁾(u) : u ∈ N(v)}))\n      - Use deterministic hash:\
  \ convert multiset to tuple, hash with stable hash (e.g., SHA256 first 16 chars or int hash)\n    - Extract feature vector:\
  \ count frequencies of each color → color histogram\n    - **k-WL Certificate**: tuple of (k, graph_structure_signature).\
  \ For canonicalization, compute a graph-level hash from:\n      - Sorted concatenation of all iteration-k node color histograms\n\
  \      - Include edge type frequencies in hash\n      - Result: a single canonical string/hash per (molecule, k) pair\n\
  \  \n  **1b. Store WL certificates:**\n  - Output: wl_certificates.json with schema:\n    ```json\n    {\n      \"molecules\"\
  : [\n        {\"mol_id\": 0, \"dataset\": \"QM9\",\n         \"wl_certificates\": {\"k=1\": \"hash_1\", \"k=2\": \"hash_2\"\
  , \"k=3\": \"hash_3\"},\n         \"properties\": {\"HOMO\": -0.5, \"LUMO\": 0.2, ...}}\n      ]\n    }\n    ```\n  - Index:\
  \ collision_index[k][certificate] = [list of mol_ids with this certificate]\n\n## Phase 2: Collision Detection & Within-Class\
  \ Variance (40% time)\n### For each (dataset, property, k) triple:\n  **2a. Collision Rate Measurement**\n  - Group molecules\
  \ by k-WL certificate\n  - For each group with ≥2 molecules:\n    - Extract property values: y_group = [y₁, y₂, ..., yₙ]\n\
  \    - Compute group property std: σ_group = std(y_group)\n    - Count \"meaningful collisions\": pairs (i,j) where |y_i\
  \ - y_j| > σ_total/2 (σ_total = std over entire dataset)\n    - collision_rate[k] = (# meaningful collision pairs) / (total\
  \ # same-certificate pairs) ∈ [0,1]\n  \n  **2b. Conditional Variance (Expressiveness Floor)**\n  - For each k:\n    - Compute:\
  \ Var[y | WL_k] = Σ_g P(cert_g) * Var[y | cert_g]\n      where P(cert_g) = (# molecules with cert_g) / (# total molecules)\n\
  \      and Var[y | cert_g] = variance of property values within group g\n    - This is the HARD LOWER BOUND on prediction\
  \ error (Bayes error for property given WL features)\n    - Normalize: ratio_unexplained[k] = Var[y | WL_k] / Var[y | total]\
  \ ∈ [0,1]\n      (= fraction of variance NOT explained by k-WL)\n  \n  **2c. Store collision/variance profiles:**\n  - Output:\
  \ collision_variance_profiles.json with schema:\n    ```json\n    {\n      \"properties\": [\n        {\"property_name\"\
  : \"HOMO\", \"dataset\": \"QM9\",\n         \"k_profiles\": [\n           {\"k\": 1, \"collision_rate\": 0.15, \"variance_explained\"\
  : 0.82, \"variance_floor\": 0.18},\n           {\"k\": 2, \"collision_rate\": 0.08, \"variance_explained\": 0.91, \"variance_floor\"\
  : 0.09},\n           {\"k\": 3, \"collision_rate\": 0.05, \"variance_explained\": 0.94, \"variance_floor\": 0.06}\n    \
  \     ],\n         \"total_variance\": 1.52, \"std_dev\": 1.23}\n      ]\n    }\n    ```\n\n## Phase 3: Typology Assignment\
  \ (10% time)\n### Compute 2D thresholds and assign quadrants:\n  **3a. Define thresholds** (adaptive to data, not hard-coded):\n\
  \  - **Collision rate threshold**: median of {collision_rate[k=1] across all properties}\n    - Properties with k=1 collision_rate\
  \ > threshold → \"high collision\"\n    - Properties with k=1 collision_rate ≤ threshold → \"low collision\"\n  \n  - **Within-class\
  \ variance threshold**: median of {ratio_unexplained[k=3] across all properties}\n    - Properties with k=3 variance_floor\
  \ > threshold → \"high within-class variance\" (3D-geometry-limited)\n    - Properties with k=3 variance_floor ≤ threshold\
  \ → \"low within-class variance\" (WL-bottlenecked)\n  \n  **3b. Assign quadrants:**\n  - **Quadrant 1 (WL-bottlenecked)**:\
  \ high collision_rate[k=1] + low variance_floor[k=3]\n    - Prediction: will show >10% relative error reduction from k=1→k=2\
  \ GNNs\n  \n  - **Quadrant 2 (3D-geometry-limited)**: high collision_rate[k=1] + high variance_floor[k=3]\n    - Prediction:\
  \ will show <5% relative error reduction from k=1→k=3 GNNs (floor ceiling)\n  \n  - **Quadrant 3 (WL-sufficient)**: low\
  \ collision_rate[k=1] + low variance_floor[k=3]\n    - Prediction: 1-WL GINs already near-optimal, minimal improvement from\
  \ higher k\n  \n  - **Quadrant 4 (noise-dominated)**: low collision_rate[k=1] + high variance_floor[k=3]\n    - Prediction:\
  \ low WL signal → measurement noise / irreducible randomness dominates\n  \n  **3c. Output typology matrix:**\n  - Output:\
  \ typology_matrix.json with schema:\n    ```json\n    {\n      \"thresholds\": {\"collision_rate\": 0.12, \"variance_floor\"\
  : 0.25},\n      \"quadrants\": {\n        \"WL-bottlenecked\": [list of (dataset, property) pairs],\n        \"3D-geometry-limited\"\
  : [...],\n        \"WL-sufficient\": [...],\n        \"noise-dominated\": [...]\n      },\n      \"property_assignments\"\
  : [\n        {\"dataset\": \"QM9\", \"property\": \"HOMO\", \"quadrant\": \"3D-geometry-limited\",\n         \"collision_rate_k1\"\
  : 0.18, \"variance_floor_k3\": 0.32, \"reasoning\": \"quantum properties depend on 3D geometry\"}\n      ]\n    }\n    ```\n\
  \n## Phase 4: Validation Signals (10% time) [OPTIONAL/FALLBACK]\n  **4a. Verify typology predictions via fast surrogate\
  \ tasks:**\n  - For each property in Quadrant 1 (WL-bottlenecked, small subset):\n    - Train a simple k=1 baseline: logistic\
  \ regression on k-WL color histogram features\n    - Record: Baseline MSE\n    - Train k=2 baseline with higher-order features\n\
  \    - If Improvement_k1_to_k2 > 10%, confirms typology assignment ✓\n  \n  - For Quadrant 2 (3D-geometry-limited, quantum\
  \ properties):\n    - If k=1 → k=3 improvement < 5%, confirms prediction ✓\n    - No need to train full GNNs; conditional\
  \ variance alone is diagnostic\n  \n  **4b. Spot-check with GNN training (OPTIONAL, if budget allows):**\n  - Pick 1 representative\
  \ property from each quadrant\n  - Train 1-WL GIN, 2-WL (NGNN via higher-order pooling), 3-WL (I²-GNN or cycle GNN)\n  -\
  \ Compare test error to predicted variance_floor[k]\n  - Expected: actual test_error ≥ variance_floor[k] (Bayes error lower\
  \ bound always holds)\n\n## Output Artifacts:\n1. **dataset_molecules.json** (130K+ molecules with canonical graphs)\n2.\
  \ **wl_certificates.json** (all k-WL certificates + collision index)\n3. **collision_variance_profiles.json** (per-property\
  \ collision rates & conditional variances for k=1,2,3)\n4. **typology_matrix.json** (2×2 assignments + reasoning)\n5. **validation_results.json**\
  \ (optional: surrogate task MSEs, GNN comparisons if time permits)\n6. **method_out.json** (final summary: typology counts,\
  \ representative examples, key findings)\n\n## Key Constants & Thresholds:\n- Max WL iterations: k ∈ {1, 2, 3} (k≥4 rarely\
  \ adds new information for small molecules)\n- Meaningful property difference threshold: |Δy| > σ_total/2 (half a standard\
  \ deviation)\n- Color hash function: SHA256 (first 16 hex chars) or Python's built-in hash if deterministic\n- Variance\
  \ explained threshold: median computed adaptively from data\n- Min group size for variance: require ≥2 molecules per certificate\
  \ (no singletons)\n"
fallback_plan: |
  ## If WL Certificate Computation Bottlenecks (Memory/Time):
  1. **Reduce to mini-dataset first**: Run on QM9 subset (first 10K molecules) to validate pipeline, then scale
  2. **Use pre-computed graph hashes**: Check if PyG/RDKit already provides WL kernel matrices; leverage rather than recomputing
  3. **Implement incremental hashing**: Compute WL colors in batches per molecule, don't hold all certificates in memory simultaneously
  4. **Cache certificates**: Write wl_certificates.json incrementally; don't recompute

  ## If Variance Computation Is Slow:
  1. **Vectorize with NumPy**: Group molecules by certificate using pd.groupby + numpy, avoid Python loops
  2. **Skip k=3 initially**: Compute k=1,2 first; k=3 only if budget allows (diminishing returns)
  3. **Sample collision pairs**: If certificate groups are huge (e.g., >1000 molecules), sample pairs rather than exhaustive comparison

  ## If Dataset Loading Fails:
  1. **Fall back to SMILES strings**: Use RDKit's Chem.MolFromSmiles to build graphs on-the-fly (slower but avoids dependency on PyG data loaders)
  2. **Download raw CSVs**: QM9 available via Figshare; MoleculeNet via DeepChem GitHub
  3. **Use synthetic mini-dataset**: Generate 1K random molecules with known properties to test pipeline logic

  ## If Typology Assignment Is Ambiguous (Overlapping Thresholds):
  1. **Use percentile-based thresholds**: Use 33rd/67th percentiles instead of median
  2. **Compute distance to quadrant centroid**: Assign property to closest quadrant in (collision_rate, variance_floor) space
  3. **Mark borderline cases**: Flag properties near threshold boundaries; don't force quadrant assignment

  ## If Validation (GNN Training) Exceeds Time Budget:
  1. **Skip it entirely**: Typology is defined by WL analysis alone; validation is confirmation, not required for core result
  2. **Use fast linear baselines only**: No GNN training; just fit logistic regression on color histograms (10× faster)
  3. **Train on mini-batch**: Pick 1 property per quadrant, train on 1K molecules (not full dataset)
testing_plan: |
  ## Phase 0: Sanity Checks (5 min)
  1. **Dataset loading**: Load QM9 subset (100 molecules); verify 19 properties present, all molecules have atom counts ≤9
     - Expected: 100 rows, no missing values
     - Failure mode: FileNotFoundError → Check PyG/Figshare links; fall back to raw CSV download

  2. **Graph conversion**: Convert 10 random molecules to networkx.Graph; verify edges/nodes match SMILES string
     - Expected: Graph with N_atoms nodes, reasonable edge count (2-3× atoms for typical organic molecules)
     - Failure mode: Atoms/bonds mismatch → Debug RDKit molecule parsing; verify bond orders handled correctly

  ## Phase 1: WL Algorithm Correctness (10 min)
  1. **Known graph test**: Run WL on benzene (C₆H₆) and naphthalene (C₁₀H₈)
     - Expected behavior: Different k-WL certificates (naphthalene has larger cycle)
     - Specific check: k=1 should give same certificate (both all-C aromatics), k=2 should differ (different neighborhoods)
     - If not: Debug hash function; verify color refinement loop updates correctly

  2. **Collision detection (synthetic test)**: Create 3 isomers (e.g., xylene ortho/meta/para) with property values [1.0, 1.1, 1.5]
     - Expected: k=1 collision rate >0 (isomers share 1-WL), within-class variance = Var[1.0, 1.1, 1.5] ≈ 0.04
     - Verify: collision_rate = (# pairs with |Δy| > σ/2) / (# total pairs) computed correctly

  3. **Variance floor sanity**: Test that Var[y | WL_k] ≤ Var[y | WL_{k-1}] for all properties
     - Expected: Variance strictly decreases (or stays same) as k increases (monotonicity)
     - Failure mode: Variance increases → Bug in conditional variance formula; check grouping logic

  ## Phase 2: Scaling Test (20 min)
  1. **Small dataset**: Run full pipeline on QM9 subset (1K molecules, 5 properties)
     - Expected output: wl_certificates.json (1K entries), collision_variance_profiles.json (5 properties × 3 k-values)
     - Metrics: Runtime <5 min, no memory errors
     - Failure mode: OOM → Reduce to 100 molecules; profile memory usage; implement batching

  2. **Dataset verification**: Spot-check 10 random molecules' certificates and property values
     - For each: manually verify WL k=1 hash is reasonable (deterministic)
     - For each: verify collision_rate[k=1] ∈ [0, 1] (sanity bound)

  ## Phase 3: Collision Rate Diagnostics (10 min)
  1. **Expected patterns**:
     - **QM9 quantum properties (HOMO, LUMO, μ)**: collision_rate[k=1] should be >10% (many isomers)
     - **MoleculeNet pharmacokinetic (solubility, BBBP)**: collision_rate[k=1] should be <5% (unique scaffolds)
     - If opposite pattern: May indicate data quality issue or mislabeled properties

  2. **Within-class variance decomposition**: For 1-2 properties, manually verify:
     - ratio_unexplained[k=1] > ratio_unexplained[k=2] > ratio_unexplained[k=3] (monotonic decrease)
     - At least one QM9 property should have ratio_unexplained[k=3] >30% (geometry-limited signal)
     - At least one MoleculeNet property should have ratio_unexplained[k=1] <10% (well-separated)

  ## Phase 4: Typology Assignment Validation (10 min)
  1. **Quadrant distribution**: Count properties in each quadrant
     - Expected: QM9 properties skew toward Quadrant 2 (3D-geometry-limited), MoleculeNet toward Quadrant 3 (WL-sufficient)
     - Failure mode: All properties in one quadrant → Thresholds may be poorly calibrated; inspect distribution and adjust

  2. **Representative examples**: For each quadrant, output 2-3 representative (dataset, property) pairs
     - Quadrant 1 (WL-bottlenecked): Should show significant drop in collision rate from k=1→k=2
     - Quadrant 2 (3D-geometry-limited): Should show high collision rate persisting across k=1,2,3
     - Quadrant 3 (WL-sufficient): Should show very low collision rate at k=1

  ## Phase 5: Final Artifact Quality (5 min)
  1. **JSON schema validation**: Validate all output JSONs against aii-json schema (use aii-json skill)
     - All required fields present
     - All numeric values in reasonable ranges
     - No duplicate entries

  2. **README generation**: Create brief summary explaining:
     - What each output file contains
     - How to interpret typology matrix
     - Limitations (e.g., 2D WL cannot detect 3D geometry, so variance_floor is proxy for geometry-dependence)

  ## Success Criteria (Confirmation Signals):
  ✓ **Core result**: Typology matrix with ≥2 properties assigned to each quadrant
  ✓ **QM9 pattern**: ≥5 quantum properties in Quadrant 2 (geometry-limited) with variance_floor[k=3] >25%
  ✓ **MoleculeNet pattern**: ≥2 pharmacokinetic properties in Quadrant 3 (WL-sufficient) with collision_rate[k=1] <3%
  ✓ **No monotonicity violations**: variance_floor strictly decreases from k=1→k=3
  ✓ **Sensible collision rates**: All collision_rate values ∈ [0, 0.5] for reasonable datasets (>50% collision rate suggests broken WL implementation)

  ## Disconfirmation Signals (Failure Scenarios):
  ✗ **Typo in results**: Typology matrix has <2 properties per quadrant (empty quadrants)
  ✗ **No WL signal**: collision_rate[k=1] ≈ 0 for all properties (suggests bonds/atoms not distinguished in WL coloring)
  ✗ **Variance increases with k**: ratio_unexplained[k=2] > ratio_unexplained[k=1] (algorithm bug)
  ✗ **Contradicts hypothesis**: QM9 quantum properties in Quadrant 3 (contradicts expected geometry-limited classification)
  ✗ **Numeric instability**: variance_floor contains NaNs or extreme values (>10× property std) → Fix: Clamp variance_floor to [0, total_var]
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [2] HUMAN-USER prompt · 2026-06-24 19:26:27 UTC

```
Graph neural network expressiveness under the Weisfeiler-Leman hierarchy for molecular property prediction
```

### [3] SKILL-INPUT — aii-python · 2026-06-24 19:26:45 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-24 19:26:45 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [5] SKILL-INPUT — aii-long-running-tasks · 2026-06-24 19:26:45 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [6] SKILL-INPUT — aii-json · 2026-06-24 19:26:47 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [7] SKILL-INPUT — aii-parallel-computing · 2026-06-24 19:26:47 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [8] SKILL-INPUT — aii-file-size-limit · 2026-06-24 19:26:47 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [9] SYSTEM-USER prompt · 2026-06-24 19:34:08 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: WL Expressiveness Floor Computation for Molecular Properties
summary: >-
  Compute k-WL certificates (k=1,2,3) for QM9 and MoleculeNet datasets, measure collision rates and conditional variance for
  all properties, and assign each to a 2×2 typology (WL-bottlenecked vs 3D-geometry-limited vs WL-sufficient vs noise-dominated).
  Output collision/variance profiles, typology matrix, and per-property expressiveness floors.
runpod_compute_profile: cpu_heavy
implementation_pseudocode: "## Phase 0: Setup & Data Loading (5% time)\n- Import: networkx, pandas, numpy, scipy, rdkit (molecule\
  \ I/O), PyTorch Geometric (optional QM9 loader), aii-json (validation)\n- Load QM9 (130K molecules, 19 properties) from\
  \ PyG or raw source\n- Load MoleculeNet datasets: ESOL, BBBP, HIV, Tox21 (total ~10-20K molecules across all, multiple binary/regression\
  \ targets)\n- Convert to canonical graph representation: atoms as nodes (features = atom type, atomic number), bonds as\
  \ edges (features = bond type)\n- Store as: dataset_molecules.json with schema {molecule_id, smiles, atom_types, bonds,\
  \ properties: {prop1: value1, ...}, atom_count}\n\n## Phase 1: k-WL Certificate Computation (30% time)\n### For k=1,2,3:\n\
  \  **1a. Canonical WL Color Refinement**\n  - For each molecule:\n    - Initialize node colors: λ⁽⁰⁾(v) = atom_type (or\
  \ more detailed: tuple(atomic_number, formal_charge, num_hydrogens))\n    - For each iteration i from 1 to max_k:\n    \
  \  - For each node v: λ⁽ⁱ⁾(v) = hash(λ⁽ⁱ⁻¹⁾(v), sorted_multiset({λ⁽ⁱ⁻¹⁾(u) : u ∈ N(v)}))\n      - Use deterministic hash:\
  \ convert multiset to tuple, hash with stable hash (e.g., SHA256 first 16 chars or int hash)\n    - Extract feature vector:\
  \ count frequencies of each color → color histogram\n    - **k-WL Certificate**: tuple of (k, graph_structure_signature).\
  \ For canonicalization, compute a graph-level hash from:\n      - Sorted concatenation of all iteration-k node color histograms\n\
  \      - Include edge type frequencies in hash\n      - Result: a single canonical string/hash per (molecule, k) pair\n\
  \  \n  **1b. Store WL certificates:**\n  - Output: wl_certificates.json with schema:\n    ```json\n    {\n      \"molecules\"\
  : [\n        {\"mol_id\": 0, \"dataset\": \"QM9\",\n         \"wl_certificates\": {\"k=1\": \"hash_1\", \"k=2\": \"hash_2\"\
  , \"k=3\": \"hash_3\"},\n         \"properties\": {\"HOMO\": -0.5, \"LUMO\": 0.2, ...}}\n      ]\n    }\n    ```\n  - Index:\
  \ collision_index[k][certificate] = [list of mol_ids with this certificate]\n\n## Phase 2: Collision Detection & Within-Class\
  \ Variance (40% time)\n### For each (dataset, property, k) triple:\n  **2a. Collision Rate Measurement**\n  - Group molecules\
  \ by k-WL certificate\n  - For each group with ≥2 molecules:\n    - Extract property values: y_group = [y₁, y₂, ..., yₙ]\n\
  \    - Compute group property std: σ_group = std(y_group)\n    - Count \"meaningful collisions\": pairs (i,j) where |y_i\
  \ - y_j| > σ_total/2 (σ_total = std over entire dataset)\n    - collision_rate[k] = (# meaningful collision pairs) / (total\
  \ # same-certificate pairs) ∈ [0,1]\n  \n  **2b. Conditional Variance (Expressiveness Floor)**\n  - For each k:\n    - Compute:\
  \ Var[y | WL_k] = Σ_g P(cert_g) * Var[y | cert_g]\n      where P(cert_g) = (# molecules with cert_g) / (# total molecules)\n\
  \      and Var[y | cert_g] = variance of property values within group g\n    - This is the HARD LOWER BOUND on prediction\
  \ error (Bayes error for property given WL features)\n    - Normalize: ratio_unexplained[k] = Var[y | WL_k] / Var[y | total]\
  \ ∈ [0,1]\n      (= fraction of variance NOT explained by k-WL)\n  \n  **2c. Store collision/variance profiles:**\n  - Output:\
  \ collision_variance_profiles.json with schema:\n    ```json\n    {\n      \"properties\": [\n        {\"property_name\"\
  : \"HOMO\", \"dataset\": \"QM9\",\n         \"k_profiles\": [\n           {\"k\": 1, \"collision_rate\": 0.15, \"variance_explained\"\
  : 0.82, \"variance_floor\": 0.18},\n           {\"k\": 2, \"collision_rate\": 0.08, \"variance_explained\": 0.91, \"variance_floor\"\
  : 0.09},\n           {\"k\": 3, \"collision_rate\": 0.05, \"variance_explained\": 0.94, \"variance_floor\": 0.06}\n    \
  \     ],\n         \"total_variance\": 1.52, \"std_dev\": 1.23}\n      ]\n    }\n    ```\n\n## Phase 3: Typology Assignment\
  \ (10% time)\n### Compute 2D thresholds and assign quadrants:\n  **3a. Define thresholds** (adaptive to data, not hard-coded):\n\
  \  - **Collision rate threshold**: median of {collision_rate[k=1] across all properties}\n    - Properties with k=1 collision_rate\
  \ > threshold → \"high collision\"\n    - Properties with k=1 collision_rate ≤ threshold → \"low collision\"\n  \n  - **Within-class\
  \ variance threshold**: median of {ratio_unexplained[k=3] across all properties}\n    - Properties with k=3 variance_floor\
  \ > threshold → \"high within-class variance\" (3D-geometry-limited)\n    - Properties with k=3 variance_floor ≤ threshold\
  \ → \"low within-class variance\" (WL-bottlenecked)\n  \n  **3b. Assign quadrants:**\n  - **Quadrant 1 (WL-bottlenecked)**:\
  \ high collision_rate[k=1] + low variance_floor[k=3]\n    - Prediction: will show >10% relative error reduction from k=1→k=2\
  \ GNNs\n  \n  - **Quadrant 2 (3D-geometry-limited)**: high collision_rate[k=1] + high variance_floor[k=3]\n    - Prediction:\
  \ will show <5% relative error reduction from k=1→k=3 GNNs (floor ceiling)\n  \n  - **Quadrant 3 (WL-sufficient)**: low\
  \ collision_rate[k=1] + low variance_floor[k=3]\n    - Prediction: 1-WL GINs already near-optimal, minimal improvement from\
  \ higher k\n  \n  - **Quadrant 4 (noise-dominated)**: low collision_rate[k=1] + high variance_floor[k=3]\n    - Prediction:\
  \ low WL signal → measurement noise / irreducible randomness dominates\n  \n  **3c. Output typology matrix:**\n  - Output:\
  \ typology_matrix.json with schema:\n    ```json\n    {\n      \"thresholds\": {\"collision_rate\": 0.12, \"variance_floor\"\
  : 0.25},\n      \"quadrants\": {\n        \"WL-bottlenecked\": [list of (dataset, property) pairs],\n        \"3D-geometry-limited\"\
  : [...],\n        \"WL-sufficient\": [...],\n        \"noise-dominated\": [...]\n      },\n      \"property_assignments\"\
  : [\n        {\"dataset\": \"QM9\", \"property\": \"HOMO\", \"quadrant\": \"3D-geometry-limited\",\n         \"collision_rate_k1\"\
  : 0.18, \"variance_floor_k3\": 0.32, \"reasoning\": \"quantum properties depend on 3D geometry\"}\n      ]\n    }\n    ```\n\
  \n## Phase 4: Validation Signals (10% time) [OPTIONAL/FALLBACK]\n  **4a. Verify typology predictions via fast surrogate\
  \ tasks:**\n  - For each property in Quadrant 1 (WL-bottlenecked, small subset):\n    - Train a simple k=1 baseline: logistic\
  \ regression on k-WL color histogram features\n    - Record: Baseline MSE\n    - Train k=2 baseline with higher-order features\n\
  \    - If Improvement_k1_to_k2 > 10%, confirms typology assignment ✓\n  \n  - For Quadrant 2 (3D-geometry-limited, quantum\
  \ properties):\n    - If k=1 → k=3 improvement < 5%, confirms prediction ✓\n    - No need to train full GNNs; conditional\
  \ variance alone is diagnostic\n  \n  **4b. Spot-check with GNN training (OPTIONAL, if budget allows):**\n  - Pick 1 representative\
  \ property from each quadrant\n  - Train 1-WL GIN, 2-WL (NGNN via higher-order pooling), 3-WL (I²-GNN or cycle GNN)\n  -\
  \ Compare test error to predicted variance_floor[k]\n  - Expected: actual test_error ≥ variance_floor[k] (Bayes error lower\
  \ bound always holds)\n\n## Output Artifacts:\n1. **dataset_molecules.json** (130K+ molecules with canonical graphs)\n2.\
  \ **wl_certificates.json** (all k-WL certificates + collision index)\n3. **collision_variance_profiles.json** (per-property\
  \ collision rates & conditional variances for k=1,2,3)\n4. **typology_matrix.json** (2×2 assignments + reasoning)\n5. **validation_results.json**\
  \ (optional: surrogate task MSEs, GNN comparisons if time permits)\n6. **method_out.json** (final summary: typology counts,\
  \ representative examples, key findings)\n\n## Key Constants & Thresholds:\n- Max WL iterations: k ∈ {1, 2, 3} (k≥4 rarely\
  \ adds new information for small molecules)\n- Meaningful property difference threshold: |Δy| > σ_total/2 (half a standard\
  \ deviation)\n- Color hash function: SHA256 (first 16 hex chars) or Python's built-in hash if deterministic\n- Variance\
  \ explained threshold: median computed adaptively from data\n- Min group size for variance: require ≥2 molecules per certificate\
  \ (no singletons)\n"
fallback_plan: |
  ## If WL Certificate Computation Bottlenecks (Memory/Time):
  1. **Reduce to mini-dataset first**: Run on QM9 subset (first 10K molecules) to validate pipeline, then scale
  2. **Use pre-computed graph hashes**: Check if PyG/RDKit already provides WL kernel matrices; leverage rather than recomputing
  3. **Implement incremental hashing**: Compute WL colors in batches per molecule, don't hold all certificates in memory simultaneously
  4. **Cache certificates**: Write wl_certificates.json incrementally; don't recompute

  ## If Variance Computation Is Slow:
  1. **Vectorize with NumPy**: Group molecules by certificate using pd.groupby + numpy, avoid Python loops
  2. **Skip k=3 initially**: Compute k=1,2 first; k=3 only if budget allows (diminishing returns)
  3. **Sample collision pairs**: If certificate groups are huge (e.g., >1000 molecules), sample pairs rather than exhaustive comparison

  ## If Dataset Loading Fails:
  1. **Fall back to SMILES strings**: Use RDKit's Chem.MolFromSmiles to build graphs on-the-fly (slower but avoids dependency on PyG data loaders)
  2. **Download raw CSVs**: QM9 available via Figshare; MoleculeNet via DeepChem GitHub
  3. **Use synthetic mini-dataset**: Generate 1K random molecules with known properties to test pipeline logic

  ## If Typology Assignment Is Ambiguous (Overlapping Thresholds):
  1. **Use percentile-based thresholds**: Use 33rd/67th percentiles instead of median
  2. **Compute distance to quadrant centroid**: Assign property to closest quadrant in (collision_rate, variance_floor) space
  3. **Mark borderline cases**: Flag properties near threshold boundaries; don't force quadrant assignment

  ## If Validation (GNN Training) Exceeds Time Budget:
  1. **Skip it entirely**: Typology is defined by WL analysis alone; validation is confirmation, not required for core result
  2. **Use fast linear baselines only**: No GNN training; just fit logistic regression on color histograms (10× faster)
  3. **Train on mini-batch**: Pick 1 property per quadrant, train on 1K molecules (not full dataset)
testing_plan: |
  ## Phase 0: Sanity Checks (5 min)
  1. **Dataset loading**: Load QM9 subset (100 molecules); verify 19 properties present, all molecules have atom counts ≤9
     - Expected: 100 rows, no missing values
     - Failure mode: FileNotFoundError → Check PyG/Figshare links; fall back to raw CSV download

  2. **Graph conversion**: Convert 10 random molecules to networkx.Graph; verify edges/nodes match SMILES string
     - Expected: Graph with N_atoms nodes, reasonable edge count (2-3× atoms for typical organic molecules)
     - Failure mode: Atoms/bonds mismatch → Debug RDKit molecule parsing; verify bond orders handled correctly

  ## Phase 1: WL Algorithm Correctness (10 min)
  1. **Known graph test**: Run WL on benzene (C₆H₆) and naphthalene (C₁₀H₈)
     - Expected behavior: Different k-WL certificates (naphthalene has larger cycle)
     - Specific check: k=1 should give same certificate (both all-C aromatics), k=2 should differ (different neighborhoods)
     - If not: Debug hash function; verify color refinement loop updates correctly

  2. **Collision detection (synthetic test)**: Create 3 isomers (e.g., xylene ortho/meta/para) with property values [1.0, 1.1, 1.5]
     - Expected: k=1 collision rate >0 (isomers share 1-WL), within-class variance = Var[1.0, 1.1, 1.5] ≈ 0.04
     - Verify: collision_rate = (# pairs with |Δy| > σ/2) / (# total pairs) computed correctly

  3. **Variance floor sanity**: Test that Var[y | WL_k] ≤ Var[y | WL_{k-1}] for all properties
     - Expected: Variance strictly decreases (or stays same) as k increases (monotonicity)
     - Failure mode: Variance increases → Bug in conditional variance formula; check grouping logic

  ## Phase 2: Scaling Test (20 min)
  1. **Small dataset**: Run full pipeline on QM9 subset (1K molecules, 5 properties)
     - Expected output: wl_certificates.json (1K entries), collision_variance_profiles.json (5 properties × 3 k-values)
     - Metrics: Runtime <5 min, no memory errors
     - Failure mode: OOM → Reduce to 100 molecules; profile memory usage; implement batching

  2. **Dataset verification**: Spot-check 10 random molecules' certificates and property values
     - For each: manually verify WL k=1 hash is reasonable (deterministic)
     - For each: verify collision_rate[k=1] ∈ [0, 1] (sanity bound)

  ## Phase 3: Collision Rate Diagnostics (10 min)
  1. **Expected patterns**:
     - **QM9 quantum properties (HOMO, LUMO, μ)**: collision_rate[k=1] should be >10% (many isomers)
     - **MoleculeNet pharmacokinetic (solubility, BBBP)**: collision_rate[k=1] should be <5% (unique scaffolds)
     - If opposite pattern: May indicate data quality issue or mislabeled properties

  2. **Within-class variance decomposition**: For 1-2 properties, manually verify:
     - ratio_unexplained[k=1] > ratio_unexplained[k=2] > ratio_unexplained[k=3] (monotonic decrease)
     - At least one QM9 property should have ratio_unexplained[k=3] >30% (geometry-limited signal)
     - At least one MoleculeNet property should have ratio_unexplained[k=1] <10% (well-separated)

  ## Phase 4: Typology Assignment Validation (10 min)
  1. **Quadrant distribution**: Count properties in each quadrant
     - Expected: QM9 properties skew toward Quadrant 2 (3D-geometry-limited), MoleculeNet toward Quadrant 3 (WL-sufficient)
     - Failure mode: All properties in one quadrant → Thresholds may be poorly calibrated; inspect distribution and adjust

  2. **Representative examples**: For each quadrant, output 2-3 representative (dataset, property) pairs
     - Quadrant 1 (WL-bottlenecked): Should show significant drop in collision rate from k=1→k=2
     - Quadrant 2 (3D-geometry-limited): Should show high collision rate persisting across k=1,2,3
     - Quadrant 3 (WL-sufficient): Should show very low collision rate at k=1

  ## Phase 5: Final Artifact Quality (5 min)
  1. **JSON schema validation**: Validate all output JSONs against aii-json schema (use aii-json skill)
     - All required fields present
     - All numeric values in reasonable ranges
     - No duplicate entries

  2. **README generation**: Create brief summary explaining:
     - What each output file contains
     - How to interpret typology matrix
     - Limitations (e.g., 2D WL cannot detect 3D geometry, so variance_floor is proxy for geometry-dependence)

  ## Success Criteria (Confirmation Signals):
  ✓ **Core result**: Typology matrix with ≥2 properties assigned to each quadrant
  ✓ **QM9 pattern**: ≥5 quantum properties in Quadrant 2 (geometry-limited) with variance_floor[k=3] >25%
  ✓ **MoleculeNet pattern**: ≥2 pharmacokinetic properties in Quadrant 3 (WL-sufficient) with collision_rate[k=1] <3%
  ✓ **No monotonicity violations**: variance_floor strictly decreases from k=1→k=3
  ✓ **Sensible collision rates**: All collision_rate values ∈ [0, 0.5] for reasonable datasets (>50% collision rate suggests broken WL implementation)

  ## Disconfirmation Signals (Failure Scenarios):
  ✗ **Typo in results**: Typology matrix has <2 properties per quadrant (empty quadrants)
  ✗ **No WL signal**: collision_rate[k=1] ≈ 0 for all properties (suggests bonds/atoms not distinguished in WL coloring)
  ✗ **Variance increases with k**: ratio_unexplained[k=2] > ratio_unexplained[k=1] (algorithm bug)
  ✗ **Contradicts hypothesis**: QM9 quantum properties in Quadrant 3 (contradicts expected geometry-limited classification)
  ✗ **Numeric instability**: variance_floor contains NaNs or extreme values (>10× property std) → Fix: Clamp variance_floor to [0, total_var]
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [10] SYSTEM-USER prompt · 2026-06-24 19:35:04 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `layman_summary`: 'This experiment measures how well graph-based molecular fingerprints (Weisfeiler-Leman, k=1,2,3) can distinguish molecules with different property values, revealing which properties hit a fundamental expressiveness ceiling and which benefit from more powerful graph neural networks.' is too long (at most 250 characters, got 282)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
