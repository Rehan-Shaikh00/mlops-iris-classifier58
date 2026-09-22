# get_historical_features.py
import pandas as pd
from feast import FeatureStore

print("=" * 60)
print("FEAST HISTORICAL FEATURE RETRIEVAL TEST")
print("=" * 60)

# Read source data
source_df = pd.read_parquet("data/iris_features.parquet")

# Entity dataframe: which samples, and as of which timestamp
entity_df = source_df[["sample_id", "event_timestamp"]].copy()

print("\nEntity DataFrame (first 5 rows):")
print(entity_df.head().to_string(index=False))

store = FeatureStore(repo_path=".")

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "iris_measurements:sepal length (cm)",
        "iris_measurements:sepal width (cm)",
        "iris_measurements:petal length (cm)",
        "iris_measurements:petal width (cm)",
        "iris_engineered_features:sepal_area",
        "iris_engineered_features:petal_area",
        "iris_engineered_features:sepal_to_petal_length_ratio",
        "iris_engineered_features:petal_length_bin",
    ],
).to_df()

print("\nHistorical Features (first 5 rows):")
print(training_df.head().to_string(index=False))

print("\nNumber of rows retrieved:", len(training_df))
print("Total null values:", int(training_df.isna().sum().sum()))