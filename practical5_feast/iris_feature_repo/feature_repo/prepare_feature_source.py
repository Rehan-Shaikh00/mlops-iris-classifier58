# prepare_feature_source.py
"""
Prepares the iris_features.csv from Experiment 4 into a Feast-ready
Parquet source with entity IDs and event timestamps.
"""
import pandas as pd
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent      # .../feature_repo
    repo_root = here.parents[2]                 # .../mlops-iris-classifier58

    # Input from Practical 4
    input_file = repo_root / "data" / "processed" / "iris_features.csv"

    # Output for Feast
    output_file = here / "data" / "iris_features.parquet"

    # Read feature-engineered data
    df = pd.read_csv(input_file)

    # Create sample_id (entity key)
    df.insert(0, "sample_id", range(len(df)))

    # Create event timestamps (one per minute)
    start_time = pd.Timestamp("2026-08-15 15:20:02", tz="UTC")
    df["event_timestamp"] = pd.date_range(
        start=start_time, periods=len(df), freq="min"
    )

    # Created timestamp
    df["created_timestamp"] = df["event_timestamp"]

    # Save as Parquet
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)

    print(f"Wrote {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()