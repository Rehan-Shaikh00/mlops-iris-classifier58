# Feature Store Analysis (Experiment 5)

## Setup
- Tool: Feast 0.66.0, Python 3.11.9
- Offline store: Parquet file (`data/iris_features.parquet`, 149 rows)
- Online store: SQLite (`data/online_store.db`)
- Registry: `data/registry.db`
- Entity: `sample_id`
- Feature views: `iris_measurements` (4 features), `iris_engineered_features` (4 features)
- Feature service: `iris_feature_service` (all 8 features)

## 1. Elimination of training-serving skew
The `iris_engineered_features` view was defined once in `features.py` and served
through two paths:
- Online (`get_online_features.py`, Step 6)
- Offline (`get_historical_features.py`, Step 7)

For `sample_id = 1` both paths returned identical values: sepal_area = 14.70,
petal_area = 0.28, sepal_to_petal_length_ratio = 3.5, petal_length_bin = short.
Both stores are populated from the same definition and source, so the values
served at inference match those used for training.

## 2. Point-in-time correct training data
`get_historical_features` retrieved 149 rows with 0 null values for the 8
requested features. Each row was joined using its own event timestamp, so only
values valid at or before that time were used. This prevents future data
leakage. (Note: our timestamps are synthetic, one per minute, and each sample
has a single row, so the as-of join is trivially satisfied here. The mechanism
matters more with several feature versions per entity.)

## 3. Feature reusability
Step 8 fetched all 149 samples through `iris_feature_service` and clustered them
with KMeans (k = 3) without re-implementing any feature. Cluster sizes were
56 / 50 / 43. Setosa formed its own cluster (50 of 50), while versicolor and
virginica overlapped, as is well known for Iris. A second, different model
consumed the exact same registered features.

## 4. Centralized governance
`features.py` is the single source of truth for feature names, types, TTL and
sources. Changing a feature means changing one definition and running
`feast apply`, and every consumer (training, serving, clustering) picks it up.

## 5. Limitations of this setup
- Local Parquet and SQLite only, so nothing here is production-scale.
- Synthetic timestamps; real data would carry real event times.
- Features were precomputed in Experiment 4 and are only registered and served
  by Feast, not transformed by it.

## Conclusion
A feature store gives one definition, two consistent serving paths, reusable
features and a central registry. That reduces duplicated engineering and
removes the main sources of training-serving skew.