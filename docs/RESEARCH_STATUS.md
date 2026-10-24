# Research status and next experiments

## Current evidence and supported conclusion

The repository contains multiple recorded protocols. Keep the archived random-split run, the later aligned random-split comparison, and the Friday source-day stress test in separate tables; thresholds and metrics from one run must not be substituted into another.

In the newer aligned random-split comparison (565,536 test flows), AE+RF [Z,re] has the strongest overall aggregate metrics among the RF variants: accuracy 97.97%, precision 91.51%, recall 98.87%, F1 95.05%, ROC-AUC 0.9984 and FPR 2.25%. AE–GNN–RF [Z,re,H] reaches 98.98% recall, but its precision (90.31%), F1 (94.45%), accuracy (97.71%) and FPR (2.60%) are worse. The random test partition was inspected during prior exploration, so this result is exploratory.

The Friday source-day stress test trains on Monday–Thursday, then evaluates on 702,713 Friday flows at thresholds selected on development validation. At the validation-selected F2 thresholds, attack recall is 26.99% for AE+RF [Z,re] and 27.11% for full fusion. Bot, DDoS and PortScan were absent from the Monday–Thursday development training pool. Friday was inspected in earlier experiments, so this is also an exploratory stress test rather than untouched confirmation. It shows that random-split scores do not establish cross-day robustness.

## Completed follow-up analyses

- Fixed-validation-recall sensitivity comparison at targets 0.980, 0.985, 0.988, 0.989 and 0.990.
- Friday attack-family recall for Bot, DDoS and PortScan.
- Confusion-matrix and metric consistency checks for the six Friday models.
- Frozen source-day configuration and result tables audited locally; summary is in docs/FRIDAY_SOURCE_DAY_HOLDOUT_AUDIT.md.
- Thursday source-file cleaning anomaly documented: 288,737 of 458,968 rows from Thursday Morning WebAttacks were excluded by the all-column missing/non-finite filter. The excluded rows' detailed missingness and label composition still require audit on the original source CSV.

## Remaining work — in order

1. Run scripts/audit_thursday_webattacks.py against the original Thursday Morning WebAttacks CSV. Review missing values per column, infinities, label mix before/after filtering, CSV field-count mismatches, and duplicate fingerprints. Verify any duplicate finding exactly if it affects a conclusion. Do not alter historical results silently.
2. Keep evaluation on other datasets as future work; the current manuscript is intentionally limited to CIC-IDS2017.
3. Decide whether repeated-seed confidence intervals are feasible without changing the frozen protocol; if run, document them as within-dataset robustness checks, not external validation.
4. Measure time, peak memory, and inference protocol constraints if feasible; current GCN builds a graph over the complete evaluation cohort, so it is offline cohort inference, not streaming.
5. Complete manuscript authorship/declarations and target-journal formatting after supervisor review.

## Guardrails

- Do not repeatedly tune against Friday.
- Do not claim graph fusion improves the overall aggregate trade-off.
- Do not describe either previously inspected test partition as a pristine confirmatory test.
- Do not upload public CIC datasets, raw traffic, or trained checkpoint binaries to this repository.
