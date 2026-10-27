# Testing Strategy: mlops-iris-classifier

## Overview
Tests are written with pytest and cover three layers: data correctness,
pipeline correctness, and model output correctness. The suite runs with
`pytest --cov=src --cov-report=term-missing --junitxml=test-results.xml`
and produces a JUnit XML report that CI tools can parse (Experiment 9).

## Test Files

| Test file | Layer | Tests | What it checks |
|---|---|---|---|
| tests/test_preprocess.py | Data | 4 | Duplicate removal, median imputation of missing numeric values, dropping rows with a missing label, empty DataFrame |
| tests/test_features.py | Data | 3 | Sepal/petal area and ratio values, petal_length_bin categories, zero petal length gives NaN instead of crashing |
| tests/test_validate.py | Data | 5 | Passes on clean data; fails on a missing column, invalid species, out-of-range value, and null values |
| tests/test_training_pipeline.py | Pipeline | 3 | Training runs without error on synthetic data, predictions have the correct shape, probabilities sum to 1 |
| tests/test_model_quality.py | Model quality | 2 | Predictions fall within the known label set; accuracy is at least 0.90 (quality gate) |

Total: 17 tests, all passing.

## Coverage (pytest-cov)

| Module | Coverage |
|---|---|
| src/pipeline/preprocess.py | 100% |
| src/pipeline/features.py | 100% |
| src/pipeline/validate.py | 100% |
| Overall (all of src/) | 19% |

The overall figure is low because training and tuning scripts (train.py,
the grid/random search scripts, and others) have no unit tests yet.
The tested pipeline modules exceed the 85% target.

`if __name__ == "__main__":` command-line blocks are excluded from coverage
via `.coveragerc`, because unit tests import the functions and do not
launch the files as scripts.

## Quality Gate
MIN_ACCEPTABLE_ACCURACY is 0.90. Current model accuracy on the held-out
20% test set is 0.9667. The gate was verified to fail when the threshold
was temporarily raised to 0.99, then restored to 0.90.

## How to Run
    pytest                                  # run all tests
    pytest --cov=src --cov-report=term-missing --junitxml=test-results.xml
