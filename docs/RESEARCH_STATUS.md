# Research status and next experiments

## Current evidence and supported conclusion

This repository contains multiple recorded protocols. Keep the archived random-split run, the later aligned random-split comparison, and the Friday source-day stress test in separate tables; thresholds and metrics from one run must not be substituted into another.

In the newer aligned random-split comparison (565,536 test flows), AE+RF [Z,re] has the strongest overall aggregate metrics among the RF variants: accuracy 97.97%, precision 91.51%, recall 98.87%, F1 95.05%, ROC-AUC 0.9984 and FPR 2.25%. AE–GNN–RF [Z,re,H] reaches 98.98% recall, but its precision (90.31%), F1 (94.45%), accuracy (97.71%) and FPR (2.60%) are worse. The random test partition was inspected during prior exploration, so this result is exploratory.

The Friday source-day stress test trains on Monday–Thursday, then evaluates on 702,713 Friday flows at thresholds selected on development validation. At the validation-selected F2 thresholds, attack recall is 26.99% for AE+RF [Z,re] and 27.11% for full fusion. Bot, DDoS and PortScan were absent from the Monday–Thursday development training pool. Friday was inspected in earlier experiments, so this is also an exploratory stress test rather than untouched confirmation. It shows that random-split scores do not establish cross-day robustness.

## Completed follow-up analyses

- Fixed-validation-recall sensitivity comparison at targets 0.980, 0.985, 0.988, 0.989 and 0.990.
- Friday attack-family recall for Bot, DDoS and PortScan.
- Confusion-matrix and metric consistency checks for the six Friday models.
- Frozen source-day configuration and result tables audited; summary is in docs/FRIDAY_SOURCE_DAY_HOLDOUT_AUDIT.md.
- Thursday Morning WebAttacks CSV audit completed. The 288,602 missing-label rows were entirely blank across all 85 fields. A further 135 labelled BENIGN records had infinite numeric values (20 also had a missing Flow Bytes/s value). The retained pre-dedup file subset comprised 168,051 BENIGN and 2,180 attack flows; the source-file cleaning audit recorded one duplicate row removed. This explains the high exclusion count as predominantly blank CSV records rather than labelled attacks. Compact audit summaries are in results/thursday_webattacks_audit_summary.csv, results/thursday_webattacks_label_counts.csv and results/thursday_webattacks_excluded_rows.csv.

## Repository review status

- Manuscript metrics and decision thresholds have been reconciled against the available saved experiment artifacts, including aligned and Friday confusion-matrix counts, F2 thresholds, fixed-validation-recall sensitivity results, and Friday attack-family counts. This is an artifact-consistency audit, not a fresh end-to-end experiment rerun or independent validation.
- The repository's public CSVs and documentation have been checked. The README's stale audit status and duplicate heading marker were corrected; the Friday fixed-recall report path was aligned with the actual repository filename. The aligned six-model metrics are available in `results/aligned_random_split_metrics_f2.csv`.
- CSV schema validation found and fixed missing quotes around comma-containing model names in the Friday metric and attack-family result tables. Each data row now has the expected column count.
- The notebook has not been rerun end-to-end as part of this repository audit. These checks validate file structure and consistency of saved artifacts; they are not new model-training results or independent validation.

## Remaining work beyond this repository update

1. If compute allows, repeat the aligned within-dataset protocol across multiple seeds and report uncertainty; this is an optional robustness check, not external validation.
2. Measure time, peak memory, and inference protocol constraints if feasible; the current GCN builds a graph over the complete evaluation cohort, so it is offline cohort inference, not streaming.
3. Complete manuscript author details, funding/competing-interest/AI-use declarations, data/code availability and target-journal formatting after the target journal and its instructions for authors are selected. These are manuscript-submission tasks, not blockers for documenting the current research status.

## Scope decision

The current manuscript is intentionally limited to CIC-IDS2017. Evaluation on additional datasets is future work, not a requirement for this version. The Friday run is a source-day stress test, not an untouched independent confirmation.

## Guardrails

- Do not repeatedly tune against Friday.
- Do not claim graph fusion improves the overall aggregate trade-off.
- Do not describe either previously inspected test partition as a pristine confirmatory test.
- Do not upload public CIC datasets, raw traffic, or trained checkpoint binaries to this repository.
