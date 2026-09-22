# reuse_features_for_clustering.py
"""
A different model (unsupervised clustering) reusing the SAME registered
features via the feature service, without re-deriving any of them.
"""
import pandas as pd
from feast import FeatureStore
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("FEAST FEATURE SERVICE TEST")
print("=" * 60)

store = FeatureStore(repo_path=".")
feature_service = store.get_feature_service("iris_feature_service")

# --- Part 1: single-sample fetch via the feature service ---
result = store.get_online_features(
    features=feature_service,
    entity_rows=[{"sample_id": 1}],
)
print("\nFeatures retrieved using Feature Service (sample_id = 1):")
print(result.to_dict())

# --- Part 2: fetch ALL samples via the same feature service ---
source_df = pd.read_parquet("data/iris_features.parquet")
entity_rows = [{"sample_id": int(i)} for i in source_df["sample_id"]]

features_df = pd.DataFrame(
    store.get_online_features(
        features=feature_service,
        entity_rows=entity_rows,
    ).to_dict()
)
print("\nRows fetched via feature service:", len(features_df))

# --- Part 3: cluster on the numeric features ---
X = features_df.drop(columns=["sample_id", "petal_length_bin"])
X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
features_df["cluster"] = kmeans.fit_predict(X_scaled)

print("\nCluster counts:")
print(features_df["cluster"].value_counts().sort_index().to_string())

# Sanity check only: species is NOT a feature and was not used for clustering
check = features_df[["sample_id", "cluster"]].merge(
    source_df[["sample_id", "species"]], on="sample_id"
)
print("\nClusters vs true species (sanity check):")
print(pd.crosstab(check["cluster"], check["species"]))