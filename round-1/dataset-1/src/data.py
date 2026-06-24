#!/usr/bin/env python3
"""Standardize molecular property datasets to exp_sel_data_out schema for WL expressiveness analysis."""

# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru"]
# ///

import json
import sys
from pathlib import Path

from loguru import logger

WORKSPACE = Path(__file__).parent
DATASETS_DIR = WORKSPACE / "temp" / "datasets"
OUTPUT_PATH = WORKSPACE / "full_data_out.json"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WORKSPACE / "logs" / "data.log", rotation="30 MB", level="DEBUG")


DATASET_CONFIGS = [
    # TOP 5 selected for WL expressiveness analysis:
    # QM9 is THE canonical GNN benchmark (HOMO/LUMO/gap), used in GIN, MPNN, SchNet papers.
    # HIV is in OGB benchmark — largest, most cited binary classification task.
    # ESOL is the most-cited small regression benchmark for GNN papers.
    # BBBP is the standard binary classification benchmark in GNN expressiveness papers.
    # Tox21 tests multi-task expressiveness across 12 diverse toxicity targets.
    {
        "file": "full_n0w0f_qm9csv_train.json",
        "name": "QM9_Properties",
        "smiles_col": "smiles",
        "label_cols": ["homo", "lumo", "gap", "dipole_moment", "polarizability"],
        "task_type": "multi_target_regression",
        "description": "QM9 quantum properties (HOMO/LUMO/gap/dipole/polarizability) — 50k of 133885 molecules from Ramakrishnan et al. 2014",
        "n_classes": None,
    },
    {
        "file": "full_scikit-fingerprints_MoleculeNet_HIV_train.json",
        "name": "MoleculeNet_HIV",
        "smiles_col": "SMILES",
        "label_cols": ["label"],
        "task_type": "binary_classification",
        "description": "HIV replication inhibition (OGB benchmark) — 41127 molecules",
        "n_classes": 2,
    },
    {
        "file": "full_scikit-fingerprints_MoleculeNet_ESOL_train.json",
        "name": "MoleculeNet_ESOL",
        "smiles_col": "SMILES",
        "label_cols": ["label"],
        "task_type": "regression",
        "description": "Aqueous solubility (log Mol/L) — 1128 small organic molecules (Delaney 2004)",
        "n_classes": None,
    },
    {
        "file": "full_scikit-fingerprints_MoleculeNet_BBBP_train.json",
        "name": "MoleculeNet_BBBP",
        "smiles_col": "SMILES",
        "label_cols": ["label"],
        "task_type": "binary_classification",
        "description": "Blood-brain barrier penetration — 2039 drug-like molecules",
        "n_classes": 2,
    },
    {
        "file": "full_scikit-fingerprints_MoleculeNet_Tox21_train.json",
        "name": "MoleculeNet_Tox21",
        "smiles_col": "SMILES",
        "label_cols": [
            "NR-AR", "NR-AR-LBD", "NR-AhR", "NR-Aromatase",
            "NR-ER", "NR-ER-LBD", "NR-PPAR-gamma",
            "SR-ARE", "SR-ATAD5", "SR-HSE", "SR-MMP", "SR-p53",
        ],
        "task_type": "multi_label_classification",
        "description": "12 toxicity targets (nuclear receptors + stress response) — 7831 molecules",
        "n_classes": 2,
    },
]


def get_smiles(row: dict, smiles_col: str) -> str | None:
    for key in [smiles_col, "SMILES", "smiles", "Smiles"]:
        v = row.get(key)
        if v and isinstance(v, str) and len(v.strip()) > 0:
            return v.strip()
    return None


@logger.catch(reraise=True)
def process_dataset(cfg: dict) -> dict | None:
    fpath = DATASETS_DIR / cfg["file"]
    if not fpath.exists():
        logger.warning(f"Missing file: {cfg['file']}")
        return None

    logger.info(f"Loading {cfg['name']} from {fpath.name}")
    rows = json.loads(fpath.read_text())
    logger.info(f"  Loaded {len(rows)} rows")

    # Auto-detect label cols for SIDER
    label_cols = cfg["label_cols"]
    if label_cols is None and rows:
        smiles_col = cfg["smiles_col"]
        label_cols = [k for k in rows[0].keys() if k not in (smiles_col, "SMILES", "smiles")]
        logger.info(f"  Auto-detected {len(label_cols)} label cols")

    examples = []
    skipped = 0
    for i, row in enumerate(rows):
        smiles = get_smiles(row, cfg["smiles_col"])
        if not smiles:
            skipped += 1
            continue

        # Build label dict from available label columns
        labels: dict[str, object] = {}
        for lc in (label_cols or []):
            v = row.get(lc)
            if v is not None:
                labels[lc] = v

        # input: SMILES string (molecular graph representation for WL analysis)
        input_str = smiles
        # output: JSON string of property labels
        output_str = json.dumps(labels, default=str)

        ex: dict = {
            "input": input_str,
            "output": output_str,
            "metadata_smiles": smiles,
            "metadata_dataset": cfg["name"],
            "metadata_task_type": cfg["task_type"],
            "metadata_label_names": json.dumps(list(label_cols) if label_cols else []),
            "metadata_row_index": i,
        }
        if cfg["n_classes"] is not None:
            ex["metadata_n_classes"] = cfg["n_classes"]

        examples.append(ex)

    if skipped:
        logger.warning(f"  Skipped {skipped} rows with missing SMILES")

    logger.info(f"  -> {len(examples)} examples for {cfg['name']}")
    return {"dataset": cfg["name"], "examples": examples}


@logger.catch(reraise=True)
def main():
    (WORKSPACE / "logs").mkdir(exist_ok=True)
    logger.info("Starting molecular dataset standardization")

    datasets = []
    for cfg in DATASET_CONFIGS:
        result = process_dataset(cfg)
        if result and result["examples"]:
            datasets.append(result)

    total = sum(len(d["examples"]) for d in datasets)
    logger.info(f"Total: {len(datasets)} datasets, {total} examples")

    output = {
        "metadata": {
            "description": "MoleculeNet + QM9 molecular property datasets for WL expressiveness analysis",
            "num_datasets": len(datasets),
            "total_examples": total,
            "domain": "molecular_property_prediction",
        },
        "datasets": datasets,
    }

    OUTPUT_PATH.write_text(json.dumps(output))
    size_mb = OUTPUT_PATH.stat().st_size / 1e6
    logger.info(f"Saved full_data_out.json: {size_mb:.1f}MB")

    # Summary table
    logger.info("Dataset summary:")
    for d in datasets:
        logger.info(f"  {d['dataset']}: {len(d['examples'])} examples")


if __name__ == "__main__":
    main()
