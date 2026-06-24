#!/usr/bin/env python3
"""WL Expressiveness Floor Robustness Validation.

Bootstrap CIs for collision rates, permutation-null thresholds,
numerical validation, and typology robustness across threshold percentiles.
"""

import json
import sys
import gc
import math
import resource
from pathlib import Path
from collections import defaultdict

import numpy as np
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent
EXPERIMENT_DIR = Path("/ai-inventor/aii_data/runs/run_7KogxZ5PgvFN/3_invention_loop/iter_1/gen_art/gen_art_experiment_1")

N_BOOTSTRAP = 1000
N_PERMUTATIONS = 1000
RNG_SEED = 42
COLLISION_SIGMA_FACTOR = 0.5
REFERENCE_PERCENTILE = 95
ALTERNATIVE_PERCENTILES = [80, 85, 90, 99]
ALL_PERCENTILES = [80, 85, 90, 95, 99]

# Container memory limit
RAM_LIMIT = 24 * 1024**3  # 24 GB (container has 29 GB)
resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT, RAM_LIMIT))


def load_certificates(path: Path) -> list[dict]:
    logger.info(f"Loading WL certificates from {path}")
    data = json.loads(path.read_text())
    mols = data["molecules"]
    logger.info(f"Loaded {len(mols)} molecules")
    return mols


def load_profiles(path: Path) -> list[dict]:
    logger.info(f"Loading collision/variance profiles from {path}")
    data = json.loads(path.read_text())
    props = data["properties"]
    logger.info(f"Loaded {len(props)} property profiles")
    return props


def build_dataset_index(mols: list[dict]) -> dict:
    """Group molecules by dataset."""
    ds_mols = defaultdict(list)
    for m in mols:
        ds_mols[m["dataset"]].append(m)
    return dict(ds_mols)


def build_group_structures(mol_list: list[dict]) -> dict:
    """For a list of molecules in one dataset, build group structures for k=1,2,3."""
    k_labels = ["k=1", "k=2", "k=3"]
    result = {}
    n = len(mol_list)

    for k_str in k_labels:
        # Map certificate -> list of indices
        cert_to_idx = defaultdict(list)
        for idx, m in enumerate(mol_list):
            cert = m["wl_certificates"][k_str]
            cert_to_idx[cert].append(idx)

        # Filter to groups with >=2 molecules
        groups = [idxs for idxs in cert_to_idx.values() if len(idxs) >= 2]

        # Build pair arrays (vectorized)
        pair_i, pair_j = [], []
        group_ids = np.full(n, -1, dtype=np.int32)
        group_id = 0
        for idxs in cert_to_idx.values():
            for idx in idxs:
                group_ids[idx] = group_id
            group_id += 1

        for idxs in groups:
            arr = np.array(idxs)
            for a in range(len(arr)):
                for b in range(a + 1, len(arr)):
                    pair_i.append(arr[a])
                    pair_j.append(arr[b])

        pair_i = np.array(pair_i, dtype=np.int32)
        pair_j = np.array(pair_j, dtype=np.int32)
        n_groups = group_id

        result[k_str] = {
            "pair_i": pair_i,
            "pair_j": pair_j,
            "group_ids": group_ids,
            "n_groups": n_groups,
            "total_pairs": len(pair_i),
        }

    return result


def compute_collision_rate(y: np.ndarray, pair_i: np.ndarray, pair_j: np.ndarray,
                           sigma: float) -> float:
    if len(pair_i) == 0:
        return 0.0
    threshold = COLLISION_SIGMA_FACTOR * sigma
    diffs = np.abs(y[pair_i] - y[pair_j])
    return float(np.mean(diffs > threshold))


def compute_variance_floor(y: np.ndarray, group_ids: np.ndarray, n_groups: int) -> float:
    total_var = np.var(y)
    if total_var == 0:
        return 0.0
    n = len(y)
    group_counts = np.bincount(group_ids, minlength=n_groups)
    group_sums = np.bincount(group_ids, weights=y, minlength=n_groups)
    group_means = np.divide(group_sums, group_counts, where=group_counts > 0, out=np.zeros(n_groups))
    within_ss = np.sum((y - group_means[group_ids]) ** 2)
    within_var = within_ss / n
    return float(within_var / total_var)


def bootstrap_collision_ci(y: np.ndarray, pair_i: np.ndarray, pair_j: np.ndarray,
                            sigma: float, rng: np.random.Generator) -> tuple[float, float, float]:
    if len(pair_i) == 0:
        return 0.0, 0.0, 0.0
    threshold = COLLISION_SIGMA_FACTOR * sigma
    n_pairs = len(pair_i)
    diffs = np.abs(y[pair_i] - y[pair_j])
    point = float(np.mean(diffs > threshold))

    # Bootstrap over pairs
    boot_rates = np.zeros(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, n_pairs, size=n_pairs)
        boot_rates[b] = np.mean(diffs[idx] > threshold)

    ci_lo = float(np.percentile(boot_rates, 2.5))
    ci_hi = float(np.percentile(boot_rates, 97.5))
    return point, ci_lo, ci_hi


def run_permutation_null(y_dict: dict[str, np.ndarray], sigmas: dict[str, float],
                          group_struct: dict, rng: np.random.Generator) -> dict:
    """Run permutation null for all properties in a dataset at all k levels.

    Returns: {prop_name: {k_str: {collision_rates: [], variance_floors: []}}}
    """
    prop_names = list(y_dict.keys())
    results = {p: {k: {"collision_rates": [], "variance_floors": []} for k in ["k=1", "k=2", "k=3"]}
               for p in prop_names}

    n = len(next(iter(y_dict.values())))
    perm_idx = np.arange(n, dtype=np.int32)

    for perm in range(N_PERMUTATIONS):
        rng.shuffle(perm_idx)
        for prop in prop_names:
            y_orig = y_dict[prop]
            y_perm = y_orig[perm_idx]
            sigma = sigmas[prop]
            for k_str in ["k=1", "k=2", "k=3"]:
                gs = group_struct[k_str]
                pi, pj = gs["pair_i"], gs["pair_j"]
                gids = gs["group_ids"]
                ng = gs["n_groups"]
                cr = compute_collision_rate(y_perm, pi, pj, sigma)
                vf = compute_variance_floor(y_perm, gids, ng)
                results[prop][k_str]["collision_rates"].append(cr)
                results[prop][k_str]["variance_floors"].append(vf)

        if (perm + 1) % 100 == 0:
            logger.info(f"  Permutation {perm+1}/{N_PERMUTATIONS}")

    return results


def assign_quadrant(cr_k1: float, vf_k3: float, cr_thresh: float, vf_thresh: float) -> str:
    high_cr = cr_k1 > cr_thresh
    high_vf = vf_k3 > vf_thresh
    if high_cr and not high_vf:
        return "WL-bottlenecked"
    elif high_cr and high_vf:
        return "3D-geometry-limited"
    elif not high_cr and not high_vf:
        return "WL-sufficient"
    else:  # not high_cr and high_vf
        return "noise-dominated"


def jaccard(set1: set, set2: set) -> float:
    if not set1 and not set2:
        return 1.0
    union = set1 | set2
    intersection = set1 & set2
    return len(intersection) / len(union)


@logger.catch(reraise=True)
def main():
    rng = np.random.default_rng(RNG_SEED)

    # Load data
    profiles = load_profiles(EXPERIMENT_DIR / "collision_variance_profiles.json")
    mols = load_certificates(EXPERIMENT_DIR / "wl_certificates.json")

    ds_index = build_dataset_index(mols)
    logger.info(f"Datasets: {list(ds_index.keys())}")

    # Build a lookup from (dataset, property) -> profile
    profile_lookup = {(p["dataset"], p["property_name"]): p for p in profiles}

    # ---- Step 1: Build group structures per dataset ----
    logger.info("Building WL group structures per dataset...")
    ds_group_structs = {}
    for ds_name, mol_list in ds_index.items():
        logger.info(f"  {ds_name}: {len(mol_list)} molecules")
        ds_group_structs[ds_name] = build_group_structures(mol_list)
        gc.collect()

    # ---- Step 2: Build property arrays per dataset ----
    logger.info("Building property value arrays...")
    ds_props = {}  # {dataset: {prop: np.array}}
    ds_sigmas = {}  # {dataset: {prop: float}}

    # Collect all property names per dataset
    for ds_name, mol_list in ds_index.items():
        prop_vals = defaultdict(list)
        for m in mol_list:
            for prop, val in m["properties"].items():
                if val is not None:
                    prop_vals[prop].append(val)
        ds_props[ds_name] = {p: np.array(v, dtype=np.float64) for p, v in prop_vals.items()
                              if len(v) == len(mol_list)}
        ds_sigmas[ds_name] = {p: float(np.std(v)) for p, v in ds_props[ds_name].items()}
        logger.info(f"  {ds_name}: {len(ds_props[ds_name])} properties")

    # ---- Step 3: Numerical Validation ----
    logger.info("=== Step 3: Numerical Validation ===")
    validation_results = {}

    for prof in profiles:
        ds = prof["dataset"]
        prop = prof["property_name"]
        key = (ds, prop)

        if ds not in ds_props or prop not in ds_props[ds]:
            logger.warning(f"Property {prop} not found in {ds} molecules")
            continue

        y = ds_props[ds][prop]
        sigma = ds_sigmas[ds][prop]
        gs = ds_group_structs[ds]

        prop_validation = {"dataset": ds, "property": prop}
        all_match = True

        for k_profile in prof["k_profiles"]:
            k = k_profile["k"]
            k_str = f"k={k}"
            gs_k = gs[k_str]

            # Recompute collision rate
            recomputed_cr = compute_collision_rate(y, gs_k["pair_i"], gs_k["pair_j"], sigma)
            reported_cr = k_profile["collision_rate"]
            cr_diff = abs(recomputed_cr - reported_cr)

            # Recompute variance floor
            recomputed_vf = compute_variance_floor(y, gs_k["group_ids"], gs_k["n_groups"])
            reported_vf = k_profile["variance_floor"]
            vf_diff = abs(recomputed_vf - reported_vf)

            tol_cr = max(1e-6, abs(reported_cr) * 0.001)
            tol_vf = max(1e-10, abs(reported_vf) * 0.001)
            cr_match = cr_diff < tol_cr
            vf_match = vf_diff < tol_vf
            match = cr_match and vf_match
            if not match:
                all_match = False

            prop_validation[f"k{k}_cr_reported"] = reported_cr
            prop_validation[f"k{k}_cr_recomputed"] = recomputed_cr
            prop_validation[f"k{k}_cr_diff"] = cr_diff
            prop_validation[f"k{k}_cr_match"] = cr_match
            prop_validation[f"k{k}_vf_reported"] = reported_vf
            prop_validation[f"k{k}_vf_recomputed"] = recomputed_vf
            prop_validation[f"k{k}_vf_diff"] = vf_diff
            prop_validation[f"k{k}_vf_match"] = vf_match

            if not match:
                logger.warning(f"MISMATCH {ds}/{prop} k={k}: CR diff={cr_diff:.2e}, VF diff={vf_diff:.2e}")

        prop_validation["all_match"] = all_match
        if all_match:
            logger.info(f"VALIDATED {ds}/{prop}")
        validation_results[key] = prop_validation

    n_validated = sum(1 for v in validation_results.values() if v["all_match"])
    logger.info(f"Numerical validation: {n_validated}/{len(validation_results)} properties fully match")

    # ---- Step 4: Bootstrap CIs ----
    logger.info("=== Step 4: Bootstrap Confidence Intervals ===")
    bootstrap_results = {}

    for prof in profiles:
        ds = prof["dataset"]
        prop = prof["property_name"]
        key = (ds, prop)

        if ds not in ds_props or prop not in ds_props[ds]:
            continue

        y = ds_props[ds][prop]
        sigma = ds_sigmas[ds][prop]
        gs = ds_group_structs[ds]

        prop_boot = {"dataset": ds, "property": prop}
        for k_profile in prof["k_profiles"]:
            k = k_profile["k"]
            k_str = f"k={k}"
            gs_k = gs[k_str]

            point, ci_lo, ci_hi = bootstrap_collision_ci(y, gs_k["pair_i"], gs_k["pair_j"], sigma, rng)
            ci_width = ci_hi - ci_lo
            small_sample = gs_k["total_pairs"] < 50

            prop_boot[f"k{k}_cr_point"] = point
            prop_boot[f"k{k}_cr_ci_lo"] = ci_lo
            prop_boot[f"k{k}_cr_ci_hi"] = ci_hi
            prop_boot[f"k{k}_cr_ci_width"] = ci_width
            prop_boot[f"k{k}_total_pairs"] = gs_k["total_pairs"]
            prop_boot[f"k{k}_small_sample"] = small_sample

        bootstrap_results[key] = prop_boot
        logger.info(f"Bootstrap CI {ds}/{prop}: k1=[{prop_boot.get('k1_cr_ci_lo', 0):.4f}, {prop_boot.get('k1_cr_ci_hi', 0):.4f}]")

    # ---- Step 5: Permutation Null ----
    logger.info("=== Step 5: Permutation Null Distributions ===")
    perm_null = {}  # {dataset: results}

    for ds_name in ds_index.keys():
        if ds_name not in ds_props:
            continue
        logger.info(f"  Permutation null for {ds_name}...")
        y_dict = ds_props[ds_name]
        sigmas = ds_sigmas[ds_name]
        gs = ds_group_structs[ds_name]

        # Only include properties that are in profiles
        profile_props = {p["property_name"] for p in profiles if p["dataset"] == ds_name}
        y_dict_filtered = {p: v for p, v in y_dict.items() if p in profile_props}

        null_results = run_permutation_null(y_dict_filtered, sigmas, gs, rng)
        perm_null[ds_name] = null_results
        gc.collect()

    # ---- Step 6: Compute null thresholds and classify ----
    logger.info("=== Step 6: Null Thresholds and Classification ===")

    # Collect all null CR k=1 and VF k=3 distributions across all properties/datasets
    # We build per-property null distributions and then set thresholds

    # For reference: use 95th percentile of pooled null per metric
    null_cr_k1_all = []
    null_vf_k3_all = []

    for ds_name, ds_null in perm_null.items():
        for prop, k_nulls in ds_null.items():
            null_cr_k1_all.extend(k_nulls["k=1"]["collision_rates"])
            null_vf_k3_all.extend(k_nulls["k=3"]["variance_floors"])

    null_cr_k1_all = np.array(null_cr_k1_all)
    null_vf_k3_all = np.array(null_vf_k3_all)

    # Compute thresholds at each percentile
    thresh_by_pct = {}
    for pct in ALL_PERCENTILES:
        cr_thresh = float(np.percentile(null_cr_k1_all, pct))
        vf_thresh = float(np.percentile(null_vf_k3_all, pct))
        thresh_by_pct[pct] = {"cr_k1": cr_thresh, "vf_k3": vf_thresh}
        logger.info(f"  Threshold @{pct}th pct: CR_k1={cr_thresh:.6f}, VF_k3={vf_thresh:.6f}")

    # Reference thresholds (95th percentile)
    ref_cr_thresh = thresh_by_pct[REFERENCE_PERCENTILE]["cr_k1"]
    ref_vf_thresh = thresh_by_pct[REFERENCE_PERCENTILE]["vf_k3"]

    # Original thresholds from the experiment (median-based)
    orig_cr_thresh = 0.007611544723757511
    orig_vf_thresh = 7.474115714695203e-05

    # ---- Step 7: Typology assignments ----
    logger.info("=== Step 7: Typology Robustness ===")

    # For each property, get its CR_k1 and VF_k3
    prop_cr_k1 = {}
    prop_vf_k3 = {}
    prop_orig_quadrant = {}

    for prof in profiles:
        key = (prof["dataset"], prof["property_name"])
        cr_k1 = prof["k_profiles"][0]["collision_rate"]
        vf_k3 = prof["k_profiles"][2]["variance_floor"]
        prop_cr_k1[key] = cr_k1
        prop_vf_k3[key] = vf_k3
        prop_orig_quadrant[key] = None  # will get from typology_matrix

    # Load typology_matrix for original quadrant assignments
    typology_path = EXPERIMENT_DIR / "typology_matrix.json"
    if typology_path.exists():
        typology_data = json.loads(typology_path.read_text())
        # Build lookup from typology_matrix
        for quadrant_name, entries in typology_data.items():
            if isinstance(entries, list):
                for entry in entries:
                    ds = entry.get("dataset", "")
                    prop = entry.get("property", "")
                    key = (ds, prop)
                    if key in prop_orig_quadrant:
                        prop_orig_quadrant[key] = quadrant_name
    else:
        logger.warning("typology_matrix.json not found, will use recomputed assignments")

    # Assign quadrants at each threshold percentile
    quadrant_assignments = {}  # {key: {pct: quadrant_name}}
    for key in prop_cr_k1:
        cr1 = prop_cr_k1[key]
        vf3 = prop_vf_k3[key]
        quadrant_assignments[key] = {}
        for pct in ALL_PERCENTILES:
            cr_t = thresh_by_pct[pct]["cr_k1"]
            vf_t = thresh_by_pct[pct]["vf_k3"]
            quadrant_assignments[key][pct] = assign_quadrant(cr1, vf3, cr_t, vf_t)
        # Also with original median-based threshold
        quadrant_assignments[key]["orig"] = assign_quadrant(cr1, vf3, orig_cr_thresh, orig_vf_thresh)

    # Compute quadrant counts at each percentile
    quadrant_counts_by_pct = {}
    for pct in ALL_PERCENTILES:
        counts = defaultdict(int)
        for key in quadrant_assignments:
            counts[quadrant_assignments[key][pct]] += 1
        quadrant_counts_by_pct[pct] = dict(counts)

    # Compute Jaccard indices between reference (95th) and alternatives
    ref_assignments = {k: v[REFERENCE_PERCENTILE] for k, v in quadrant_assignments.items()}
    ref_sets = {q: {k for k, v in ref_assignments.items() if v == q} for q in
                ["WL-bottlenecked", "3D-geometry-limited", "WL-sufficient", "noise-dominated"]}

    jaccard_indices = {}
    for pct in ALTERNATIVE_PERCENTILES:
        pct_assignments = {k: v[pct] for k, v in quadrant_assignments.items()}
        pct_sets = {q: {k for k, v in pct_assignments.items() if v == q} for q in
                    ["WL-bottlenecked", "3D-geometry-limited", "WL-sufficient", "noise-dominated"]}
        jaccards = {q: jaccard(ref_sets[q], pct_sets[q]) for q in ref_sets}
        mean_j = float(np.mean(list(jaccards.values())))
        jaccard_indices[pct] = {"per_quadrant": jaccards, "mean": mean_j}
        logger.info(f"  Jaccard {REFERENCE_PERCENTILE}th vs {pct}th: mean={mean_j:.4f}, {jaccards}")

    # Properties that change quadrant between any alternative and reference
    unstable_props = {}
    for key in quadrant_assignments:
        ref_q = quadrant_assignments[key][REFERENCE_PERCENTILE]
        changes = {pct: quadrant_assignments[key][pct]
                   for pct in ALTERNATIVE_PERCENTILES
                   if quadrant_assignments[key][pct] != ref_q}
        if changes:
            unstable_props[str(key)] = {"reference": ref_q, "changes": {str(k): v for k, v in changes.items()}}

    logger.info(f"Properties that change quadrant across thresholds: {len(unstable_props)}")

    # ---- Step 8: Significance testing ----
    logger.info("=== Step 8: Significance vs Null ===")
    significance_results = {}

    for prof in profiles:
        ds = prof["dataset"]
        prop = prof["property_name"]
        key = (ds, prop)

        if ds not in perm_null or prop not in perm_null[ds]:
            continue

        null_k = perm_null[ds][prop]
        cr_k1 = prop_cr_k1[key]
        vf_k3 = prop_vf_k3[key]

        null_cr = np.array(null_k["k=1"]["collision_rates"])
        null_vf = np.array(null_k["k=3"]["variance_floors"])

        # p-value: fraction of null >= observed
        p_cr = float(np.mean(null_cr >= cr_k1))
        p_vf = float(np.mean(null_vf >= vf_k3))

        # Percentile of observed in null distribution
        cr_pct_in_null = float(np.mean(null_cr < cr_k1) * 100)
        vf_pct_in_null = float(np.mean(null_vf < vf_k3) * 100)

        # Is it significant above null 95th?
        null_cr_95 = float(np.percentile(null_cr, 95))
        null_vf_95 = float(np.percentile(null_vf, 95))
        cr_significant = cr_k1 > null_cr_95
        vf_significant = vf_k3 > null_vf_95

        significance_results[key] = {
            "p_cr_k1": p_cr,
            "p_vf_k3": p_vf,
            "cr_k1_percentile_in_null": cr_pct_in_null,
            "vf_k3_percentile_in_null": vf_pct_in_null,
            "cr_k1_significant_above_null95": cr_significant,
            "vf_k3_significant_above_null95": vf_significant,
            "null_cr_k1_95th": null_cr_95,
            "null_vf_k3_95th": null_vf_95,
        }

    # ---- Assemble eval_out.json ----
    logger.info("=== Assembling eval_out.json ===")

    # Aggregate metrics
    n_props = len(profiles)
    n_val_pass = sum(1 for v in validation_results.values() if v["all_match"])
    n_sig_cr = sum(1 for v in significance_results.values() if v["cr_k1_significant_above_null95"])
    n_sig_vf = sum(1 for v in significance_results.values() if v["vf_k3_significant_above_null95"])
    mean_ci_width_k1 = float(np.mean([v["k1_cr_ci_width"] for v in bootstrap_results.values()
                                       if "k1_cr_ci_width" in v]))
    mean_jaccard_80 = jaccard_indices[80]["mean"]
    mean_jaccard_99 = jaccard_indices[99]["mean"]

    # Count quadrant assignments at reference threshold
    ref_quad_counts = quadrant_counts_by_pct[REFERENCE_PERCENTILE]

    metrics_agg = {
        "n_properties_total": float(n_props),
        "n_numerical_validated": float(n_val_pass),
        "numerical_validation_rate": float(n_val_pass / n_props),
        "n_cr_k1_significant_above_null95": float(n_sig_cr),
        "n_vf_k3_significant_above_null95": float(n_sig_vf),
        "fraction_cr_significant": float(n_sig_cr / n_props),
        "fraction_vf_significant": float(n_sig_vf / n_props),
        "mean_bootstrap_ci_width_k1": mean_ci_width_k1,
        "n_properties_changing_quadrant": float(len(unstable_props)),
        "fraction_stable_quadrant": float((n_props - len(unstable_props)) / n_props),
        "mean_jaccard_95th_vs_80th": float(mean_jaccard_80),
        "mean_jaccard_95th_vs_99th": float(mean_jaccard_99),
        "null_cr_k1_95th_threshold": float(ref_cr_thresh),
        "null_vf_k3_95th_threshold": float(ref_vf_thresh),
        "orig_cr_k1_median_threshold": float(orig_cr_thresh),
        "orig_vf_k3_median_threshold": float(orig_vf_thresh),
        "n_wl_bottlenecked_null95": float(ref_quad_counts.get("WL-bottlenecked", 0)),
        "n_3d_geometry_limited_null95": float(ref_quad_counts.get("3D-geometry-limited", 0)),
        "n_wl_sufficient_null95": float(ref_quad_counts.get("WL-sufficient", 0)),
        "n_noise_dominated_null95": float(ref_quad_counts.get("noise-dominated", 0)),
    }

    # Build per-example outputs grouped by dataset
    dataset_examples = defaultdict(list)

    for prof in profiles:
        ds = prof["dataset"]
        prop = prof["property_name"]
        key = (ds, prop)

        boot = bootstrap_results.get(key, {})
        val = validation_results.get(key, {})
        sig = significance_results.get(key, {})
        quads = quadrant_assignments.get(key, {})

        # Construct output string summarizing results
        output_lines = []
        output_lines.append(f"Bootstrap CIs:")
        for k in [1, 2, 3]:
            pt = boot.get(f"k{k}_cr_point", float("nan"))
            lo = boot.get(f"k{k}_cr_ci_lo", float("nan"))
            hi = boot.get(f"k{k}_cr_ci_hi", float("nan"))
            n_pairs = boot.get(f"k{k}_total_pairs", 0)
            output_lines.append(f"  k={k}: CR={pt:.4f} CI=[{lo:.4f},{hi:.4f}] n_pairs={n_pairs}")

        output_lines.append(f"Numerical validation: {'PASS' if val.get('all_match') else 'FAIL'}")
        for k in [1, 2, 3]:
            cr_r = val.get(f"k{k}_cr_reported", float("nan"))
            cr_c = val.get(f"k{k}_cr_recomputed", float("nan"))
            vf_r = val.get(f"k{k}_vf_reported", float("nan"))
            vf_c = val.get(f"k{k}_vf_recomputed", float("nan"))
            output_lines.append(f"  k={k}: CR {cr_r:.6f}→{cr_c:.6f}, VF {vf_r:.2e}→{vf_c:.2e}")

        output_lines.append(f"Significance (null 95th):")
        output_lines.append(f"  CR_k1: p={sig.get('p_cr_k1', float('nan')):.4f} "
                            f"{'SIGNIFICANT' if sig.get('cr_k1_significant_above_null95') else 'marginal'}")
        output_lines.append(f"  VF_k3: p={sig.get('p_vf_k3', float('nan')):.4f} "
                            f"{'SIGNIFICANT' if sig.get('vf_k3_significant_above_null95') else 'marginal'}")

        output_lines.append(f"Quadrant assignments:")
        for pct in ALL_PERCENTILES:
            q = quads.get(pct, "unknown")
            output_lines.append(f"  @{pct}th pct: {q}")
        output_lines.append(f"  Original (median): {quads.get('orig', 'unknown')}")

        example = {
            "input": f"Dataset: {ds} | Property: {prop} | N molecules: {prof['n_molecules']}",
            "output": "\n".join(output_lines),
            "metadata_dataset": ds,
            "metadata_property": prop,
            "predict_quadrant_null95": str(quads.get(REFERENCE_PERCENTILE, "unknown")),
            "predict_quadrant_orig": str(quads.get("orig", "unknown")),
            "predict_quadrant_stable": str(len([p for p in ALTERNATIVE_PERCENTILES
                                                 if quads.get(p) == quads.get(REFERENCE_PERCENTILE)]) == len(ALTERNATIVE_PERCENTILES)),
            "eval_cr_k1_point": float(boot.get("k1_cr_point", 0.0)),
            "eval_cr_k1_ci_lo": float(boot.get("k1_cr_ci_lo", 0.0)),
            "eval_cr_k1_ci_hi": float(boot.get("k1_cr_ci_hi", 0.0)),
            "eval_cr_k1_ci_width": float(boot.get("k1_cr_ci_width", 0.0)),
            "eval_vf_k3": float(prof["k_profiles"][2]["variance_floor"]),
            "eval_cr_k1_p_value": float(sig.get("p_cr_k1", 1.0)),
            "eval_vf_k3_p_value": float(sig.get("p_vf_k3", 1.0)),
            "eval_numerical_validated": float(1.0 if val.get("all_match") else 0.0),
            "eval_n_quadrant_changes": float(len([p for p in ALTERNATIVE_PERCENTILES
                                                   if quads.get(p) != quads.get(REFERENCE_PERCENTILE)])),
        }
        dataset_examples[ds].append(example)

    datasets_out = [
        {"dataset": ds, "examples": examples}
        for ds, examples in sorted(dataset_examples.items())
    ]

    # Build detailed robustness analysis metadata
    robustness_summary = {}
    for pct in ALL_PERCENTILES:
        robustness_summary[f"pct_{pct}_counts"] = quadrant_counts_by_pct[pct]
    robustness_summary["jaccard_indices"] = {
        str(pct): jaccard_indices[pct] for pct in ALTERNATIVE_PERCENTILES
    }
    # Convert tuple keys to strings for JSON serialization
    robustness_summary["unstable_properties"] = unstable_props
    robustness_summary["thresholds_by_percentile"] = {str(p): v for p, v in thresh_by_pct.items()}

    eval_out = {
        "metadata": {
            "evaluation_name": "WL Expressiveness Floor Robustness Validation",
            "n_bootstrap": N_BOOTSTRAP,
            "n_permutations": N_PERMUTATIONS,
            "rng_seed": RNG_SEED,
            "collision_sigma_factor": COLLISION_SIGMA_FACTOR,
            "reference_null_percentile": REFERENCE_PERCENTILE,
            "alternative_percentiles": ALTERNATIVE_PERCENTILES,
            "robustness_summary": robustness_summary,
        },
        "metrics_agg": metrics_agg,
        "datasets": datasets_out,
    }

    # Validate JSON serializable
    out_path = WORKSPACE / "eval_out.json"
    out_str = json.dumps(eval_out, indent=2)
    out_path.write_text(out_str)
    logger.info(f"Saved eval_out.json ({len(out_str)/1024:.1f} KB)")

    # Summary
    logger.info("=== SUMMARY ===")
    logger.info(f"Numerical validation: {n_val_pass}/{n_props} properties pass")
    logger.info(f"Significant CR (null 95th): {n_sig_cr}/{n_props}")
    logger.info(f"Significant VF (null 95th): {n_sig_vf}/{n_props}")
    logger.info(f"Stable quadrant assignments: {n_props - len(unstable_props)}/{n_props}")
    logger.info(f"Mean Jaccard (95th vs 80th): {mean_jaccard_80:.4f}")
    logger.info(f"Mean Jaccard (95th vs 99th): {mean_jaccard_99:.4f}")
    logger.info(f"Null thresholds @95th: CR={ref_cr_thresh:.6f}, VF={ref_vf_thresh:.2e}")
    logger.info(f"Quadrant counts @95th pct null: {ref_quad_counts}")


if __name__ == "__main__":
    main()
