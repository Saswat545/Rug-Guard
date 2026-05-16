"""
BUILD_DATASET.PY
================
Step 2.2 of the RugGuard ML pipeline.

What this does:
  1. Loads your 2,391 confirmed rug pull addresses (label = 1)
  2. Loads ~85 curated legitimate contracts (label = 0)
  3. For each address → fetches source code → extracts 53 features
  4. Saves features.csv — the training-ready dataset for XGBoost

How to run:
  python build_dataset.py --api_key YOUR_ETHERSCAN_KEY

The script is RESUMABLE — if it crashes midway, re-run and it
will skip addresses already in the output file.

Expected runtime: ~45-90 minutes for all 2,400+ contracts
(Etherscan free tier = 5 req/sec, we stay at 4 to be safe)

Output files:
  data/features.csv          — full training dataset
  data/build_log.txt         — progress log
  data/failed_addresses.txt  — addresses where source fetch failed
"""

import os
import time
import argparse
import pandas as pd
from tqdm import tqdm
from datetime import datetime

from backend.feature_extractor import extract_features_from_address
from legit_contracts import get_all_legit_addresses

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

RUG_CSV = "rugpull_full_dataset_new.csv"   # Your uploaded dataset (same folder as this script)
OUTPUT_DIR = "data"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "features.csv")
LOG_FILE = os.path.join(OUTPUT_DIR, "build_log.txt")
FAILED_FILE = os.path.join(OUTPUT_DIR, "failed_addresses.txt")

# Etherscan free = 5 req/sec. We use 4 to stay safe.
DELAY_SECONDS = 0.25   # 4 requests/sec
BATCH_SAVE_EVERY = 50  # Save progress every 50 contracts


# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# LOAD RUG ADDRESSES
# ─────────────────────────────────────────────────────────────────────────────

def load_rug_addresses(csv_path: str) -> list[dict]:
    """Load confirmed rug pull addresses from your dataset."""
    df = pd.read_csv(csv_path)

    # Normalise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Keep ETH contracts only (BSC has different Etherscan API)
    eth_df = df[df["chain"].str.upper() == "ETH"].copy()
    bsc_df = df[df["chain"].str.upper() == "BSC"].copy()

    records = []

    for _, row in eth_df.iterrows():
        records.append({
            "address": row["address"].strip(),
            "chain": "ETH",
            "label": 1,
            "attack_type": row.get("type", "Unknown"),
            "root_cause": row.get("root_causes", "Unknown"),
        })

    for _, row in bsc_df.iterrows():
        records.append({
            "address": row["address"].strip(),
            "chain": "BSC",
            "label": 1,
            "attack_type": row.get("type", "Unknown"),
            "root_cause": row.get("root_causes", "Unknown"),
        })

    return records


# ─────────────────────────────────────────────────────────────────────────────
# LOAD LEGIT ADDRESSES
# ─────────────────────────────────────────────────────────────────────────────

def load_legit_addresses() -> list[dict]:
    """Load curated legitimate contract addresses."""
    raw = get_all_legit_addresses()
    return [
        {
            "address": item["address"].strip(),
            "chain": item["chain"],
            "label": 0,
            "attack_type": "LEGITIMATE",
            "root_cause": "LEGITIMATE",
        }
        for item in raw
    ]


# ─────────────────────────────────────────────────────────────────────────────
# LOAD ALREADY-PROCESSED (RESUME SUPPORT)
# ─────────────────────────────────────────────────────────────────────────────

def load_already_done() -> set:
    """Return set of addresses already in features.csv."""
    if not os.path.exists(OUTPUT_CSV):
        return set()
    try:
        df = pd.read_csv(OUTPUT_CSV)
        if "address" in df.columns:
            return set(df["address"].str.lower().tolist())
    except Exception:
        pass
    return set()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN BUILD LOOP
# ─────────────────────────────────────────────────────────────────────────────

def build_dataset(api_key: str, limit: int = None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    log("=" * 60)
    log("RugGuard ML — Dataset Builder v2.0")
    log("=" * 60)

    # Load all addresses
    rug_records = load_rug_addresses(RUG_CSV)
    legit_records = load_legit_addresses()

    log(f"Rug pull addresses:    {len(rug_records)}")
    log(f"Legitimate addresses:  {len(legit_records)}")

    all_records = rug_records + legit_records

    if limit:
        all_records = all_records[:limit]
        log(f"[DEV MODE] Limited to {limit} contracts")

    # Resume support
    already_done = load_already_done()
    todo = [r for r in all_records if r["address"].lower() not in already_done]

    log(f"Already processed:     {len(already_done)}")
    log(f"Remaining to process:  {len(todo)}")
    log("")

    if not todo:
        log("All contracts already processed. Dataset is ready.")
        return

    # Batch accumulator
    batch_rows = []
    failed = []
    write_header = not os.path.exists(OUTPUT_CSV)

    for i, record in enumerate(tqdm(todo, desc="Extracting features")):
        address = record["address"]
        chain = record["chain"]

        # Fetch features
        try:
            features = extract_features_from_address(
                address=address,
                api_key=api_key,
                chain=chain,
                retry=2,
            )
        except Exception as e:
            log(f"ERROR on {address}: {e}")
            failed.append(address)
            features = {}

        if not features:
            failed.append(address)
            continue

        # Build row
        row = {
            "address": address,
            "chain": chain,
            "label": record["label"],
            "attack_type": record["attack_type"],
            "root_cause": record["root_cause"],
        }
        row.update(features)
        batch_rows.append(row)

        # Rate limit — stay under 5 req/sec
        time.sleep(DELAY_SECONDS)

        # Save batch every N contracts
        if len(batch_rows) >= BATCH_SAVE_EVERY or i == len(todo) - 1:
            df_batch = pd.DataFrame(batch_rows)

            if write_header:
                df_batch.to_csv(OUTPUT_CSV, mode="w", index=False, header=True)
                write_header = False
            else:
                df_batch.to_csv(OUTPUT_CSV, mode="a", index=False, header=False)

            fetched = df_batch["source_fetched"].sum() if "source_fetched" in df_batch else 0
            log(f"Saved batch of {len(batch_rows)} | source fetched: {fetched}/{len(batch_rows)}")
            batch_rows = []

    # Save failed addresses
    if failed:
        with open(FAILED_FILE, "a") as f:
            for addr in failed:
                f.write(addr + "\n")
        log(f"Failed addresses saved: {len(failed)} → {FAILED_FILE}")

    # Final summary
    log("")
    log("=" * 60)
    log("BUILD COMPLETE")
    if os.path.exists(OUTPUT_CSV):
        df_final = pd.read_csv(OUTPUT_CSV)
        log(f"Total rows in dataset:  {len(df_final)}")
        log(f"Rug pull (label=1):     {(df_final['label']==1).sum()}")
        log(f"Legitimate (label=0):   {(df_final['label']==0).sum()}")
        log(f"Source fetched:         {df_final['source_fetched'].sum()}")
        log(f"Features per row:       {len(df_final.columns)}")
        log(f"Output:                 {OUTPUT_CSV}")
    log("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RugGuard Dataset Builder")
    parser.add_argument(
        "--api_key",
        type=str,
        default=os.getenv("ETHERSCAN_API_KEY", ""),
        help="Etherscan API key (or set ETHERSCAN_API_KEY env var)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of contracts (for testing). Default = all.",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("ERROR: No API key provided.")
        print("Usage: python build_dataset.py --api_key YOUR_KEY")
        print("   or: export ETHERSCAN_API_KEY=YOUR_KEY && python build_dataset.py")
        exit(1)

    build_dataset(api_key=args.api_key, limit=args.limit)