# Hyperparameter Tuning Analysis

## 1. Baseline Model
- Model: DecisionTreeClassifier (default hyperparameters)
- CV F1 Macro: 0.9663 (+/- 0.0316)
- Test Accuracy: 0.9000

## 2. Grid Search
- Model: RandomForestClassifier
- Total combinations: 72
- Cross-validation: 5-fold
- Total fits: 360
- Best params: max_depth=3, max_features=sqrt, min_samples_split=2, n_estimators=50
- Best CV F1 Macro: 0.9663
- Test Accuracy: 0.9667

## 3. Random Search
- Model: RandomForestClassifier
- Number of iterations: 30
- Cross-validation: 5-fold
- Total fits: 150
- Best params: max_depth=3, max_features=sqrt, min_samples_split=6, n_estimators=100
- Best CV F1 Macro: 0.9663
- Test Accuracy: 0.9667

## 4. Comparison

| Run | CV F1 Macro | Test Accuracy | Total Fits |
|---|---|---|---|
| Baseline Decision Tree | 0.9663 | 0.9000 | 5 |
| Grid Search (RF) | 0.9663 | 0.9667 | 360 |
| Random Search (RF) | 0.9663 | 0.9667 | 150 |

## 5. Findings
- Both searches found configurations with the same CV F1 Macro as the
  baseline (0.9663), so tuning did not improve the cross-validated score
  on this dataset.
- Test accuracy rose from 0.9000 to 0.9667 for both Random Forests, but the
  test set has only 30 samples, so this difference (2 samples) is not
  strong evidence of a real improvement.
- Random Search matched Grid Search's best score using 150 fits versus 360
  (about 42% of the cost), consistent with Bergstra & Bengio (2012).
- Both searches selected max_depth=3 and max_features=sqrt, suggesting these
  hyperparameters matter most here, while min_samples_split and
  n_estimators had little effect.
- The Iris features are highly separable, so a simple baseline is already
  near the performance ceiling and extra tuning effort buys little.
