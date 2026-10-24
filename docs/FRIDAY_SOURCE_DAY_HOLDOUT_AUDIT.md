# Friday source-day holdout: audited exploratory results

Date: 2026-10-24

## Scope and status

This document summarizes the frozen Friday source-day experiment. Monday–Thursday were the development pool; Friday (702,713 flows) was the test cohort. The split and metrics are internally consistent with the supplied configuration and CSVs. However, Friday had been inspected during earlier exploratory experiments, so this is a source-day stress test, not a pristine independent confirmation.

## Main finding

At model-specific thresholds selected by maximizing F2 on the Monday–Thursday validation sample, attack recall on Friday ranges from 26.99% to 27.95% for the evaluated supervised/AE-RF variants. The false-negative rate is approximately 72–73% for those variants. This is a major distribution-shift/generalization warning and must be reported alongside the high random-split scores.

| Model | Accuracy | Attack precision | Attack recall | F1 | ROC-AUC | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|---:|
| AE reconstruction error | 62.14% | 58.19% | 27.95% | 37.76% | 0.5608 | 14.01% | 72.05% |
| AE+RF [Z,re] | 69.56% | 96.22% | 26.99% | 42.15% | 0.7595 | 0.74% | 73.01% |
| AE+GNN direct scores | 69.55% | 93.49% | 27.85% | 42.91% | 0.7715 | 1.35% | 72.15% |
| AE+GNN+RF [H] | 69.09% | 91.60% | 27.28% | 42.04% | 0.8013 | 1.75% | 72.72% |
| AE+GNN+RF [Z,H] | 69.56% | 96.03% | 27.05% | 42.20% | 0.7004 | 0.78% | 72.95% |
| AE+GNN+RF [Z,re,H] | 69.60% | 96.16% | 27.11% | 42.29% | 0.7746 | 0.76% | 72.89% |

## Attack-family analysis

Bot (1,956 flows), DDoS (128,025) and PortScan (158,804) were not represented in the Monday–Thursday development training pool. At the chosen F2 thresholds, recall by family was poor for Bot (0–5.06%) and PortScan (0.05–0.97%). DDoS recall was approximately 60.75–62.75%. The exact model-by-family counts are in results/friday_source_day_holdout_attack_family_recall.csv.

## Threshold-transfer sensitivity

At a validation target recall of 98.8%, Friday test recall for AE+RF [Z,re] was only 25.96% (FPR 0.64%); full fusion [Z,re,H] reached 26.86% recall (FPR 0.71%). Direct AE+GNN reached 99.77% recall but with 96.80% FPR. The chosen operating point did not transfer reliably to Friday. See results/friday_source_day_fixed_recall_0988.csv.

## Aligned random-split benchmark

The aligned random-split benchmark used the same 565,536-flow test partition across models and model-specific thresholds selected on a common 100,000-node validation graph. AE+RF [Z,re] remains strongest on overall aggregate metrics among the RF variants; AE+GNN+RF [Z,re,H] has slightly higher recall but worse precision, F1, accuracy and FPR. This random-split test was also inspected in earlier exploration, so it is exploratory.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|---:|
| AE reconstruction error | 34.11% | 22.75% | 97.97% | 36.92% | 0.6646 | 81.54% | 2.03% |
| AE+RF [Z,re] | 97.97% | 91.51% | 98.87% | 95.05% | 0.9984 | 2.25% | 1.13% |
| AE+GNN direct scores | 73.89% | 42.47% | 92.16% | 58.15% | 0.8755 | 30.59% | 7.84% |
| AE+GNN+RF [H] | 96.13% | 84.85% | 97.80% | 90.87% | 0.9952 | 4.28% | 2.20% |
| AE+GNN+RF [Z,H] | 97.81% | 90.87% | 98.82% | 94.68% | 0.9982 | 2.43% | 1.19% |
| AE+GNN+RF [Z,re,H] | 97.71% | 90.31% | 98.98% | 94.45% | 0.9982 | 2.60% | 1.02% |

## Open data-quality gate

The current source-day cleaning procedure removes 288,737 of 458,968 rows from Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv because of missing or non-finite values. The source audit shows 288,622 rows with at least one missing value, 135 rows with at least one numeric infinity, and 20 rows in both groups. The cause and label composition of excluded rows still require review on the original CSV. Do not silently change the filter or reinterpret the Friday experiment before this audit is complete.

## Interpretation limits

- Friday was consulted during prior exploration; do not tune repeatedly against it or call it an untouched independent test.
- The GCN graph is built over the full evaluation cohort; the experiment measures offline cohort inference, not one-flow-at-a-time online detection.
- External validation, repeated-seed confidence intervals, and latency/throughput measurements remain outstanding.
- CIC-IDS2018 is a candidate for external evaluation, but the frozen 72-feature schema must be matched by feature meaning and units before any scores are valid; external test labels must not be used for fitting or threshold selection.