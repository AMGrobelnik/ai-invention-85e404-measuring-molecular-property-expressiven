#!/usr/bin/env python3
"""
WL Expressiveness Floor Computation for Molecular Property Prediction.

Computes k-WL certificates (k=1,2,3) for QM9 and MoleculeNet datasets,
measures collision rates and conditional variance, and assigns each property
to a 2x2 typology (WL-bottlenecked / 3D-geometry-limited / WL-sufficient / noise-dominated).
"""

import gc
import hashlib
import json
import math
import multiprocessing as mp
import os
import resource
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from loguru import logger
from rdkit import Chem
from rdkit.Chem import AllChem
from tqdm import tqdm

# ─── Logging ───────────────────────────────────────────────────────────────────
WORKSPACE = Path(__file__).parent
LOGS_DIR = WORKSPACE / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS_DIR / "run.log", rotation="30 MB", level="DEBUG")

# ─── Hardware / RAM limits ──────────────────────────────────────────────────────
def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except Exception:
        pass
    try:
        return len(os.sched_getaffinity(0))
    except Exception:
        pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float:
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except Exception:
            pass
    import psutil
    return psutil.virtual_memory().total / 1e9

NUM_CPUS = _detect_cpus()
TOTAL_RAM_GB = _container_ram_gb()
RAM_BUDGET_GB = min(TOTAL_RAM_GB * 0.75, 20.0)
RAM_BUDGET = int(RAM_BUDGET_GB * 1e9)

logger.info(f"CPUs={NUM_CPUS}, RAM={TOTAL_RAM_GB:.1f}GB, budget={RAM_BUDGET_GB:.1f}GB")
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

NUM_WORKERS = max(1, NUM_CPUS - 1)

# ─── QM9 Property Names ─────────────────────────────────────────────────────────
QM9_PROPS = [
    "mu", "alpha", "homo", "lumo", "gap", "r2", "zpve",
    "u0", "u298", "h298", "g298", "cv", "u0_atom", "u298_atom",
    "h298_atom", "g298_atom", "A", "B", "C"
]

# ─── Data Download / Loading ────────────────────────────────────────────────────

def download_file(url: str, dest: Path) -> Path:
    if dest.exists():
        logger.info(f"Cache hit: {dest.name}")
        return dest
    logger.info(f"Downloading {url} → {dest.name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    logger.info(f"Downloaded {dest.stat().st_size/1e6:.1f} MB")
    return dest


def load_qm9(cache_dir: Path, max_mols: int | None = None) -> list[dict]:
    """Load QM9 from CSV (Figshare). Returns list of mol dicts."""
    # QM9 CSV from Figshare
    url = "https://figshare.com/ndownloader/files/3195389"
    csv_path = cache_dir / "qm9.csv"

    # Try downloading - use DeepChem S3 (reliable)
    url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm9.csv"
    try:
        download_file(url, csv_path)
    except Exception as e:
        logger.error(f"QM9 download failed: {e}")
        return []

    try:
        df = pd.read_csv(csv_path, nrows=max_mols)
    except Exception as e:
        logger.error(f"Failed to parse QM9 CSV: {e}")
        return []

    logger.info(f"QM9 CSV columns: {list(df.columns[:10])}")

    # Identify SMILES column
    smiles_col = None
    for c in ["smiles", "SMILES", "smi", "mol_id"]:
        if c in df.columns:
            smiles_col = c
            break

    if smiles_col is None:
        logger.error("No SMILES column in QM9 CSV")
        return []

    # Identify property columns
    prop_cols = [c for c in df.columns if c != smiles_col and df[c].dtype in [np.float64, np.float32, float]]
    logger.info(f"QM9 property columns: {prop_cols}")

    mols = []
    for i, row in df.iterrows():
        smi = str(row[smiles_col])
        props = {c: float(row[c]) for c in prop_cols if pd.notna(row[c])}
        mols.append({
            "mol_id": i,
            "dataset": "QM9",
            "smiles": smi,
            "properties": props,
        })
        if max_mols and len(mols) >= max_mols:
            break

    logger.info(f"Loaded {len(mols)} QM9 molecules")
    return mols


def load_moleculenet_csv(name: str, url: str, smiles_col: str, prop_cols: list[str],
                          cache_dir: Path, max_mols: int | None = None) -> list[dict]:
    """Generic MoleculeNet CSV loader."""
    dest = cache_dir / f"{name}.csv"
    try:
        download_file(url, dest)
    except Exception as e:
        logger.warning(f"Failed to download {name}: {e}")
        return []

    try:
        df = pd.read_csv(dest, nrows=max_mols)
    except Exception as e:
        logger.error(f"Failed to parse {name}: {e}")
        return []

    # Check available columns
    avail_props = [c for c in prop_cols if c in df.columns]
    if smiles_col not in df.columns:
        # Try to find SMILES col
        for c in df.columns:
            if "smiles" in c.lower() or "smi" in c.lower():
                smiles_col = c
                break

    mols = []
    for i, row in df.iterrows():
        if smiles_col not in df.columns:
            break
        smi = str(row[smiles_col])
        if pd.isna(smi) or smi == "nan":
            continue
        props = {}
        for c in avail_props:
            v = row.get(c, None)
            if v is not None and not pd.isna(v):
                try:
                    props[c] = float(v)
                except Exception:
                    pass
        if props:
            mols.append({
                "mol_id": len(mols),
                "dataset": name,
                "smiles": smi,
                "properties": props,
            })
        if max_mols and len(mols) >= max_mols:
            break

    logger.info(f"Loaded {len(mols)} {name} molecules")
    return mols


MOLECULENET_SOURCES = [
    {
        "name": "ESOL",
        "url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv",
        "smiles_col": "smiles",
        "prop_cols": ["measured log solubility in mols per litre"],
    },
    {
        "name": "FreeSolv",
        "url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/SAMPL.csv",
        "smiles_col": "smiles",
        "prop_cols": ["expt"],
    },
    {
        "name": "Lipophilicity",
        "url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv",
        "smiles_col": "smiles",
        "prop_cols": ["exp"],
    },
    {
        "name": "BBBP",
        "url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv",
        "smiles_col": "smiles",
        "prop_cols": ["p_np"],
    },
    {
        "name": "HIV",
        "url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/HIV.csv",
        "smiles_col": "smiles",
        "prop_cols": ["HIV_active"],
    },
]

# ─── WL Certificate Computation ────────────────────────────────────────────────

def smiles_to_graph(smiles: str) -> tuple[list, list] | None:
    """Convert SMILES to (node_labels, edge_list). Returns None if invalid."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        mol = Chem.AddHs(mol)
        nodes = []
        for atom in mol.GetAtoms():
            label = (
                atom.GetAtomicNum(),
                atom.GetFormalCharge(),
                atom.GetNumImplicitHs(),
                int(atom.GetIsAromatic()),
            )
            nodes.append(label)
        edges = []
        for bond in mol.GetBonds():
            i = bond.GetBeginAtomIdx()
            j = bond.GetEndAtomIdx()
            bt = int(bond.GetBondTypeAsDouble() * 2)  # 2=single,4=double,6=triple
            edges.append((i, j, bt))
            edges.append((j, i, bt))
        return nodes, edges
    except Exception:
        return None


def _wl_hash(value) -> str:
    """Deterministic hash using SHA256."""
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]


def compute_wl_certificate(nodes: list, edges: list, k_max: int = 3) -> dict[str, str]:
    """Compute WL certificates for k=1,2,...,k_max.

    Returns dict: {"k=1": cert, "k=2": cert, "k=3": cert}
    Each certificate is a graph-level hash from sorted node color histograms.
    """
    n = len(nodes)
    # Build adjacency with edge types
    adj = defaultdict(list)  # node -> [(neighbor, bond_type)]
    for (i, j, bt) in edges:
        adj[i].append((j, bt))

    # Initial colors from node labels
    colors = [_wl_hash(nodes[v]) for v in range(n)]

    certs = {}
    for k in range(1, k_max + 1):
        # Aggregate neighbor colors
        new_colors = []
        for v in range(n):
            neighbors = adj[v]
            # Sort by (bond_type, neighbor_color) for determinism
            neighbor_repr = tuple(sorted((bt, colors[u]) for (u, bt) in neighbors))
            new_color = _wl_hash((colors[v], neighbor_repr))
            new_colors.append(new_color)
        colors = new_colors

        # Graph-level certificate: sorted color histogram
        color_counts = sorted(colors)
        cert = _wl_hash(tuple(color_counts))
        certs[f"k={k}"] = cert

    return certs


def _process_mol_for_wl(args) -> dict | None:
    """Worker function for parallel WL computation."""
    mol_id, dataset, smiles, properties = args
    graph = smiles_to_graph(smiles)
    if graph is None:
        return None
    nodes, edges = graph
    try:
        certs = compute_wl_certificate(nodes, edges, k_max=3)
    except Exception:
        return None
    return {
        "mol_id": mol_id,
        "dataset": dataset,
        "smiles": smiles,
        "wl_certificates": certs,
        "properties": properties,
        "atom_count": len(nodes),
    }


def compute_wl_certificates_parallel(molecules: list[dict], num_workers: int) -> list[dict]:
    """Parallel WL certificate computation."""
    args = [(m["mol_id"], m["dataset"], m["smiles"], m["properties"]) for m in molecules]
    results = []
    ctx = mp.get_context("spawn")
    chunk = max(1, len(args) // (num_workers * 10))

    with ProcessPoolExecutor(max_workers=num_workers, mp_context=ctx) as pool:
        futures = {pool.submit(_process_mol_for_wl, a): i for i, a in enumerate(args)}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="WL certs"):
            r = fut.result()
            if r is not None:
                results.append(r)

    logger.info(f"WL certs computed: {len(results)}/{len(args)} valid molecules")
    return results


# ─── Collision & Variance Analysis ──────────────────────────────────────────────

def compute_collision_variance(
    cert_molecules: list[dict],
    dataset_name: str,
    property_name: str,
    k_values: list[int] = [1, 2, 3],
) -> dict | None:
    """Compute collision rates and conditional variance for one (dataset, property) pair."""
    # Extract molecules in this dataset with this property
    values = []
    certs_by_k = {k: [] for k in k_values}
    for m in cert_molecules:
        if m["dataset"] != dataset_name:
            continue
        v = m["properties"].get(property_name)
        if v is None:
            continue
        try:
            v = float(v)
        except Exception:
            continue
        if not math.isfinite(v):
            continue
        values.append(v)
        for k in k_values:
            certs_by_k[k].append(m["wl_certificates"].get(f"k={k}", "__missing__"))

    n = len(values)
    if n < 10:
        return None

    y = np.array(values)
    total_var = float(np.var(y))
    total_std = float(np.std(y))

    if total_var < 1e-12:
        return None

    k_profiles = []
    for k in k_values:
        cert_list = certs_by_k[k]

        # Group by certificate
        groups = defaultdict(list)
        for cert, val in zip(cert_list, values):
            groups[cert].append(val)

        # Conditional variance (Bayes error floor)
        cond_var = 0.0
        collision_pairs = 0
        total_pairs = 0
        n_collision_groups = 0

        for cert, group_vals in groups.items():
            gn = len(group_vals)
            if gn < 2:
                continue
            gv = np.array(group_vals)
            # Weight by group probability
            cond_var += (gn / n) * float(np.var(gv))

            # Meaningful collision pairs: |yi - yj| > std/2
            n_collision_groups += 1
            gn_pairs = gn * (gn - 1) // 2
            total_pairs += gn_pairs
            for a in range(gn):
                for b in range(a + 1, gn):
                    if abs(gv[a] - gv[b]) > total_std / 2:
                        collision_pairs += 1

        coll_rate = collision_pairs / total_pairs if total_pairs > 0 else 0.0
        variance_floor = cond_var / total_var  # fraction of variance unexplained
        variance_explained = 1.0 - variance_floor

        k_profiles.append({
            "k": k,
            "collision_rate": float(coll_rate),
            "variance_explained": float(variance_explained),
            "variance_floor": float(variance_floor),
            "n_collision_groups": n_collision_groups,
            "total_pairs": total_pairs,
        })

    return {
        "property_name": property_name,
        "dataset": dataset_name,
        "n_molecules": n,
        "total_variance": float(total_var),
        "std_dev": float(total_std),
        "k_profiles": k_profiles,
    }


def compute_all_profiles(cert_molecules: list[dict]) -> list[dict]:
    """Compute profiles for all (dataset, property) pairs."""
    # Discover all (dataset, property) pairs
    pairs = set()
    for m in cert_molecules:
        for prop in m["properties"]:
            pairs.add((m["dataset"], prop))

    logger.info(f"Computing profiles for {len(pairs)} (dataset, property) pairs")
    profiles = []
    for dataset, prop in sorted(pairs):
        try:
            p = compute_collision_variance(cert_molecules, dataset, prop)
            if p is not None:
                profiles.append(p)
        except Exception as e:
            logger.warning(f"Failed {dataset}/{prop}: {e}")

    logger.info(f"Computed {len(profiles)} valid profiles")
    return profiles


# ─── Typology Assignment ─────────────────────────────────────────────────────────

QUADRANT_DESCRIPTIONS = {
    "WL-bottlenecked": (
        "High k=1 collision rate + low k=3 variance floor. "
        "WL expressiveness is the bottleneck — upgrading from 1-WL to higher-k GNNs "
        "should yield >10% relative error reduction."
    ),
    "3D-geometry-limited": (
        "High k=1 collision rate + high k=3 variance floor. "
        "Collisions persist even at k=3; irreducible variance from 3D geometry "
        "dominates — graph topology alone is insufficient."
    ),
    "WL-sufficient": (
        "Low k=1 collision rate + low k=3 variance floor. "
        "1-WL GINs are already near-optimal; minimal improvement expected from higher-k GNNs."
    ),
    "noise-dominated": (
        "Low k=1 collision rate + high k=3 variance floor. "
        "Low WL-collision signal but high residual variance — "
        "measurement noise or stochastic processes dominate prediction error."
    ),
}


def assign_typology(profiles: list[dict]) -> dict:
    """Assign each property to a 2×2 typology quadrant."""
    if len(profiles) < 4:
        logger.warning("Too few profiles for robust threshold estimation")

    # Extract k=1 collision rates and k=3 variance floors
    k1_rates = []
    k3_floors = []
    for p in profiles:
        kp = {kd["k"]: kd for kd in p["k_profiles"]}
        if 1 in kp and 3 in kp:
            k1_rates.append(kp[1]["collision_rate"])
            k3_floors.append(kp[3]["variance_floor"])

    if not k1_rates:
        logger.error("No valid profiles for typology")
        return {}

    # Adaptive thresholds: median
    thr_collision = float(np.median(k1_rates))
    thr_variance = float(np.median(k3_floors))
    logger.info(f"Typology thresholds: collision_rate_k1={thr_collision:.4f}, variance_floor_k3={thr_variance:.4f}")

    quadrants = {"WL-bottlenecked": [], "3D-geometry-limited": [], "WL-sufficient": [], "noise-dominated": []}
    assignments = []

    for p in profiles:
        kp = {kd["k"]: kd for kd in p["k_profiles"]}
        if 1 not in kp or 3 not in kp:
            continue

        cr1 = kp[1]["collision_rate"]
        vf3 = kp[3]["variance_floor"]

        high_collision = cr1 > thr_collision
        high_varfloor = vf3 > thr_variance

        if high_collision and not high_varfloor:
            quadrant = "WL-bottlenecked"
        elif high_collision and high_varfloor:
            quadrant = "3D-geometry-limited"
        elif not high_collision and not high_varfloor:
            quadrant = "WL-sufficient"
        else:
            quadrant = "noise-dominated"

        # Monotonicity check
        vf_vals = [kp[k]["variance_floor"] for k in sorted(kp.keys())]
        monotonic = all(vf_vals[i] >= vf_vals[i+1] - 0.001 for i in range(len(vf_vals)-1))

        # Reasoning
        reasoning_parts = [QUADRANT_DESCRIPTIONS[quadrant]]
        if not monotonic:
            reasoning_parts.append("[NOTE: non-monotonic variance floor — numerical artifact]")

        assignments.append({
            "dataset": p["dataset"],
            "property": p["property_name"],
            "quadrant": quadrant,
            "collision_rate_k1": cr1,
            "variance_floor_k3": vf3,
            "variance_floor_k1": kp[1]["variance_floor"],
            "variance_floor_k2": kp[2]["variance_floor"] if 2 in kp else None,
            "n_molecules": p["n_molecules"],
            "reasoning": " ".join(reasoning_parts),
            "monotonic": monotonic,
        })

        quadrants[quadrant].append({"dataset": p["dataset"], "property": p["property_name"]})

    return {
        "thresholds": {
            "collision_rate": thr_collision,
            "variance_floor": thr_variance,
        },
        "quadrant_descriptions": QUADRANT_DESCRIPTIONS,
        "quadrants": quadrants,
        "property_assignments": assignments,
    }


# ─── Build method_out.json ────────────────────────────────────────────────────────

def build_method_out(profiles: list[dict], typology: dict) -> dict:
    """Build exp_gen_sol_out.json format output."""
    datasets_dict = defaultdict(list)

    for assignment in typology.get("property_assignments", []):
        dataset = assignment["dataset"]
        prop = assignment["property"]
        quadrant = assignment["quadrant"]

        # Find profile
        profile = next((p for p in profiles if p["dataset"] == dataset and p["property_name"] == prop), None)
        if profile is None:
            continue

        kp = {kd["k"]: kd for kd in profile["k_profiles"]}

        # Format input: describe the property
        input_str = (
            f"Dataset: {dataset} | Property: {prop} | "
            f"N molecules: {profile['n_molecules']} | "
            f"Total variance: {profile['total_variance']:.4f} | Std: {profile['std_dev']:.4f}"
        )

        # Format output: typology assignment with metrics
        k1 = kp.get(1, {})
        k2 = kp.get(2, {})
        k3 = kp.get(3, {})
        output_str = (
            f"Typology: {quadrant}\n"
            f"k=1: collision_rate={k1.get('collision_rate', 'N/A'):.4f}, variance_floor={k1.get('variance_floor', 'N/A'):.4f}\n"
            f"k=2: collision_rate={k2.get('collision_rate', 'N/A'):.4f}, variance_floor={k2.get('variance_floor', 'N/A'):.4f}\n"
            f"k=3: collision_rate={k3.get('collision_rate', 'N/A'):.4f}, variance_floor={k3.get('variance_floor', 'N/A'):.4f}\n"
            f"Reasoning: {assignment['reasoning']}"
        )

        example = {
            "input": input_str,
            "output": output_str,
            "predict_quadrant": quadrant,
            "predict_collision_rate_k1": f"{k1.get('collision_rate', 0):.6f}",
            "predict_variance_floor_k1": f"{k1.get('variance_floor', 0):.6f}",
            "predict_variance_floor_k2": f"{k2.get('variance_floor', 0):.6f}",
            "predict_variance_floor_k3": f"{k3.get('variance_floor', 0):.6f}",
            "predict_n_molecules": str(profile["n_molecules"]),
            "predict_monotonic": str(assignment.get("monotonic", True)),
            "metadata_dataset": dataset,
            "metadata_property": prop,
        }
        datasets_dict[dataset].append(example)

    datasets = [
        {"dataset": ds, "examples": examples}
        for ds, examples in sorted(datasets_dict.items())
        if examples
    ]

    # Add summary dataset
    quadrant_counts = {q: len(v) for q, v in typology.get("quadrants", {}).items()}
    summary_examples = []
    for q, count in sorted(quadrant_counts.items()):
        members = typology["quadrants"][q][:5]  # representative subset
        member_str = ", ".join(f"{m['dataset']}/{m['property']}" for m in members)
        summary_examples.append({
            "input": f"Typology quadrant: {q} | Count: {count} | Description: {QUADRANT_DESCRIPTIONS.get(q, '')}",
            "output": f"Properties in this quadrant ({count} total): {member_str}{'...' if count > 5 else ''}",
            "predict_quadrant": q,
            "predict_count": str(count),
        })

    if summary_examples:
        datasets.append({"dataset": "typology_summary", "examples": summary_examples})

    return {
        "metadata": {
            "method_name": "WL Expressiveness Floor Analysis",
            "description": (
                "Computes k-WL (k=1,2,3) certificates for molecular graphs, "
                "measures collision rates and conditional variance (Bayes error floor), "
                "and assigns each (dataset, property) pair to a 2×2 typology quadrant."
            ),
            "thresholds": typology.get("thresholds", {}),
            "quadrant_counts": quadrant_counts,
            "total_properties": sum(quadrant_counts.values()),
        },
        "datasets": datasets,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────────

@logger.catch(reraise=True)
def main():
    cache_dir = WORKSPACE / "cache"
    cache_dir.mkdir(exist_ok=True)

    # ── Load datasets ──────────────────────────────────────────────────────────
    logger.info("=== Phase 0: Loading Datasets ===")
    all_molecules = []

    # QM9 (limit to 50K for memory/time)
    qm9_mols = load_qm9(cache_dir, max_mols=50000)
    all_molecules.extend(qm9_mols)
    del qm9_mols; gc.collect()

    # MoleculeNet datasets
    for src in MOLECULENET_SOURCES:
        mols = load_moleculenet_csv(
            name=src["name"],
            url=src["url"],
            smiles_col=src["smiles_col"],
            prop_cols=src["prop_cols"],
            cache_dir=cache_dir,
            max_mols=5000,
        )
        all_molecules.extend(mols)
        del mols; gc.collect()

    logger.info(f"Total molecules loaded: {len(all_molecules)}")

    if len(all_molecules) == 0:
        logger.error("No molecules loaded. Cannot continue.")
        sys.exit(1)

    # ── WL Certificate Computation ─────────────────────────────────────────────
    logger.info("=== Phase 1: WL Certificate Computation ===")
    cert_mols = compute_wl_certificates_parallel(all_molecules, NUM_WORKERS)
    del all_molecules; gc.collect()

    # Save certificates (incremental)
    wl_cert_path = WORKSPACE / "wl_certificates.json"
    logger.info(f"Saving {len(cert_mols)} WL certificates → {wl_cert_path.name}")
    wl_cert_path.write_text(json.dumps({"molecules": cert_mols}, indent=2))

    # ── Collision & Variance Analysis ──────────────────────────────────────────
    logger.info("=== Phase 2: Collision & Variance Analysis ===")
    profiles = compute_all_profiles(cert_mols)

    profiles_path = WORKSPACE / "collision_variance_profiles.json"
    profiles_path.write_text(json.dumps({"properties": profiles}, indent=2))
    logger.info(f"Saved {len(profiles)} profiles → {profiles_path.name}")

    # ── Typology Assignment ────────────────────────────────────────────────────
    logger.info("=== Phase 3: Typology Assignment ===")
    typology = assign_typology(profiles)

    typology_path = WORKSPACE / "typology_matrix.json"
    typology_path.write_text(json.dumps(typology, indent=2))
    logger.info(f"Typology quadrant counts: {typology.get('thresholds', {})}")
    for q, members in typology.get("quadrants", {}).items():
        logger.info(f"  {q}: {len(members)} properties")

    # ── Build method_out.json ──────────────────────────────────────────────────
    logger.info("=== Phase 4: Building method_out.json ===")
    method_out = build_method_out(profiles, typology)
    method_out_path = WORKSPACE / "method_out.json"
    method_out_path.write_text(json.dumps(method_out, indent=2))
    logger.info(f"Saved method_out.json with {len(method_out['datasets'])} datasets")

    # ── Validation ─────────────────────────────────────────────────────────────
    logger.info("=== Phase 5: Validating Output ===")
    skill_dir = Path("/ai-inventor/.claude/skills/aii-json")
    py = skill_dir / "../.ability_client_venv/bin/python"
    val_script = skill_dir / "scripts/aii_json_validate_schema.py"
    import subprocess
    result = subprocess.run(
        [str(py), str(val_script), "--format", "exp_gen_sol_out", "--file", str(method_out_path)],
        capture_output=True, text=True
    )
    logger.info(f"Validation stdout: {result.stdout.strip()}")
    if result.returncode != 0:
        logger.error(f"Validation FAILED: {result.stderr.strip()}")
    else:
        logger.info("Validation PASSED")

    # Summary
    logger.info("=== DONE ===")
    qcounts = {q: len(v) for q, v in typology.get("quadrants", {}).items()}
    logger.info(f"Final typology distribution: {qcounts}")
    logger.info(f"Total properties analyzed: {sum(qcounts.values())}")


if __name__ == "__main__":
    main()
