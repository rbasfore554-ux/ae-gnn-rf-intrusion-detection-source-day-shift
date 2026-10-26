# Reproducibility notes

## Required raw files

Download CIC-IDS2017 from the Canadian Institute for Cybersecurity. The following CSVs are expected under `data/raw/cicids2017/`:

- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

The public repository intentionally excludes raw data and model checkpoint files.

## Run order

1. Start a fresh Jupyter kernel.
2. Run every cell in `notebooks/01_full_experiment_pipeline.ipynb` from top to bottom. Do not execute isolated cells using variables from older notebook sessions.
3. Run `notebooks/02_cicids2017_cleaning_audit.ipynb` separately to regenerate the dataset cleaning audit. It writes summary CSVs into `results/`.

The full experiment is memory- and compute-intensive. The notebook uses full-batch AE training, sampled GNN training/validation graphs of 100,000 nodes each, and a graph built over all held-out test flows. Hardware-dependent runtime and memory use are expected.

## What the published CSVs mean

- `results/final_model_metrics.csv`: recorded final AE–GNN–RF `[Z || H]` fusion run.
- `results/model_comparison.csv`: recorded ablation/fusion comparison. Metric scores are fractions from 0 to 1; TN, FP, FN and TP are counts.
- `results/cicids2017_*_audit.csv`: observed counts from the cleaning audit.

Notebook code is provided for transparency. The package was not re-executed end-to-end during preparation, so saved CSVs should be treated as the recorded project outputs, not as freshly verified outputs from this packaging step.


## Friday source-day stress test (additional run)

Notebook path in the local project package: hybrid_ae_gnn_rf_friday_source_day_holdout_v1.ipynb. This run used seed 42, Monday–Thursday development rows, an 80/20 stratified train/validation split, 100,000 graph nodes for GNN training and validation, and all 702,713 Friday rows as the test cohort. It trained fresh AE/GCN/RF artifacts for that source-day protocol.

Recorded outputs in the local project folder include source_day_holdout_metrics_f2.csv, source_day_holdout_attack_family_recall.csv, source_day_holdout_fixed_recall.csv, source_day_holdout_config.json and source_day_cleaning_audit.csv. The GitHub summary is in docs/FRIDAY_SOURCE_DAY_HOLDOUT_AUDIT.md.

Friday was inspected in earlier exploration. This run must be described as a source-day stress test, not an untouched independent confirmation. It evaluates a graph built over the full Friday cohort, so it is not a streaming test.

## Thursday Morning WebAttacks source-file audit (completed)

A direct read-only audit of the original source CSV found 458,968 parsed records across 85 columns. Exactly 288,602 rows were entirely blank across all fields, including Label. The audit counted 135 labelled BENIGN records with infinite numeric values; 20 of those also had a missing Flow Bytes/s value. The invalid-row union excluded 288,737 rows and retained 170,231 labelled records before de-duplication (168,051 BENIGN, 2,180 attacks). The prior source-file cleaning audit records one duplicate removed, leaving 170,230 rows from this file after de-duplication. Zero rows had wrong field counts. Compact summary files are provided in results/thursday_webattacks_audit_summary.csv, results/thursday_webattacks_label_counts.csv, and results/thursday_webattacks_excluded_rows.csv. The raw CSV remains excluded from the public repository.

This explains the large exclusion count as predominantly completely blank CSV records. It does not resolve the separate evaluation caveats: Friday was previously inspected, unseen attack-family effects are confounded with source-day shift, and inference remains offline cohort-based.

## Scope decision

The current manuscript is intentionally limited to CIC-IDS2017. Evaluation on any additional dataset is future work, not a required task for this submission. The Friday run is reported as an exploratory within-dataset source-day stress test and must not be described as independent external validation.
