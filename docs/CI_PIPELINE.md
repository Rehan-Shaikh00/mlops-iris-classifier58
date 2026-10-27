# CI Pipeline Documentation

## 1. Overview
This project uses GitHub Actions for Continuous Integration. The workflow is
defined in `.github/workflows/ci.yml` and runs on `ubuntu-latest` with
Python 3.11. It triggers on pushes to `main` or `develop` and on pull
requests targeting either branch.

Dependencies are pinned in `requirements.txt` (scikit-learn 1.9.1,
pandas 2.3.3, numpy 2.4.6, joblib 1.6.0) so CI uses the same versions that
were tested locally. The pip cache is keyed on `requirements.txt` to speed up
repeat runs.

The pipeline checks code quality, runs the Experiment 8 test suite, produces
test and coverage reports, and enforces a minimum model accuracy.

## 2. CI Jobs

### 2.1 build-and-lint
- **Purpose:** confirm the code compiles and follows the lint standard.
- **Steps:** checkout, set up Python, install dependencies, compile `src`
  and `tests` with `compileall`, run Flake8 on `src/`
  (`--max-line-length=100 --extend-ignore=E203`).
- **Success condition:** compilation and linting report no errors.
- Before the first run, 34 Flake8 findings in `src/` were fixed (autopep8
  for whitespace and blank lines, manual removal of two redundant imports).

### 2.2 test-suite
- **Dependency:** `needs: build-and-lint`
- **Purpose:** verify the data pipeline and model code with the full pytest suite.
- **Steps:** checkout, set up Python, install dependencies, create data
  directories, regenerate data (collect, preprocess, engineer features),
  run pytest with coverage, upload reports.
- **Why data is regenerated:** `data/` is not stored in git, so each job
  rebuilds it.
- **Outputs:** `test-results.xml` and `coverage.xml`, uploaded as the
  artifact `test-and-coverage-reports` (`if: always()`, so reports are
  kept even when tests fail).
- **Success condition:** all 17 tests pass.

### 2.3 model-quality-gate
- **Dependency:** `needs: test-suite`
- **Purpose:** run `tests/test_model_quality.py` as a dedicated gate.
- **Steps:** same environment and data preparation as above, then
  `pytest tests/test_model_quality.py -v`.
- **Threshold:** `MIN_ACCEPTABLE_ACCURACY = 0.90`. The model scores about
  0.9667 on the held-out 20% test set.
- **Success condition:** both quality tests pass.

## 3. Job Dependency Order

    build-and-lint
          |
          v
      test-suite
          |
          v
    model-quality-gate

If an upstream job fails, downstream jobs are skipped. This saves runner
time and shows the developer which category of problem occurred.

## 4. First Successful Run
Run #1 (triggered by the push adding the workflow) passed all three jobs:
build-and-lint in 27s, test-suite in 30s and model-quality-gate in 25s,
for a total of 1m 34s, with one artifact (`test-and-coverage-reports`)
containing `test-results.xml` and `coverage.xml`.

## 5. Branch Protection Ruleset
A ruleset named **Protect main - CI checks** is Active on `main`. It
requires:
- changes to arrive through a pull request (0 required approvals, as this
  is a single-contributor repository);
- the status checks `build-and-lint`, `test-suite` and
  `model-quality-gate` to pass before merging.

As a result, direct pushes to `main` are rejected and every change,
including documentation, goes through a pull request with passing checks.

## 6. Pull Request Verification
The branch `feature/ci-verification-test` contained a harmless README
change. A pull request into `main` triggered the workflow through the
`pull_request` event, all three jobs passed, and the PR was merged.

## 7. Model-Quality Regression Demonstration
To confirm the gate can actually catch a regression, the branch
`feature/simulate-regression` changed `MIN_ACCEPTABLE_ACCURACY` in
`tests/test_model_quality.py` from 0.90 to 0.999, and a pull request was
opened into `main`.

**Observed results**

| Check | Result |
|---|---|
| build-and-lint | Passed |
| test-suite | Failed (16 passed, 1 failed) |
| model-quality-gate | Skipped (depends on test-suite) |
| Merge button | Blocked by the ruleset |

The failing assertion reported: `Model accuracy 0.9667 fell below the
minimum acceptable threshold of 0.999`. The pull request was closed
without merging, the branch was deleted locally and on GitHub, and
`main` was confirmed to still contain `MIN_ACCEPTABLE_ACCURACY = 0.90`.

**Note:** the regression was detected by the quality test running inside
`test-suite`. The separate `model-quality-gate` job was skipped because of
its `needs:` dependency, so it did not run independently in this scenario.

## 8. Conclusion
The pipeline automates compilation, linting, testing, report generation
and model-quality validation. The passing runs show that it works, and
the deliberately failed pull request shows that it detects a model that
falls below the accuracy requirement and that branch protection stops it
from being merged.
